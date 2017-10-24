package apiserver

import (
	"sync"

	"k8s.io/apimachinery/pkg/apimachinery/registered"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	genericregistry "k8s.io/apiserver/pkg/registry/generic"
	"k8s.io/apiserver/pkg/registry/rest"
	genericapiserver "k8s.io/apiserver/pkg/server"
	restclient "k8s.io/client-go/rest"
	kclientsetinternal "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset"
	kinternalinformers "k8s.io/kubernetes/pkg/client/informers/informers_generated/internalversion"

	securityapiv1 "github.com/openshift/origin/pkg/security/apis/security/v1"
	securityinformer "github.com/openshift/origin/pkg/security/generated/informers/internalversion"
	"github.com/openshift/origin/pkg/security/registry/podsecuritypolicyreview"
	"github.com/openshift/origin/pkg/security/registry/podsecuritypolicyselfsubjectreview"
	"github.com/openshift/origin/pkg/security/registry/podsecuritypolicysubjectreview"
	sccstorage "github.com/openshift/origin/pkg/security/registry/securitycontextconstraints/etcd"
	oscc "github.com/openshift/origin/pkg/security/securitycontextconstraints"
)

type ExtraConfig struct {
	CoreAPIServerClientConfig *restclient.Config
	// SCCStorage is actually created with a kubernetes restmapper options to have the correct prefix,
	// so we have to have it special cased here to point to the right spot.
	SCCStorage            *sccstorage.REST
	SecurityInformers     securityinformer.SharedInformerFactory
	KubeInternalInformers kinternalinformers.SharedInformerFactory

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}

type SecurityAPIServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

type SecurityAPIServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *SecurityAPIServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of SecurityAPIServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*SecurityAPIServer, error) {
	genericServer, err := c.GenericConfig.New("security.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &SecurityAPIServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.RESTOptionsGetter)
	if err != nil {
		return nil, err
	}

	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(securityapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, metav1.ParameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = securityapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[securityapiv1.SchemeGroupVersion.Version] = v1Storage
	if err := s.GenericAPIServer.InstallAPIGroup(&apiGroupInfo); err != nil {
		return nil, err
	}

	return s, nil
}

func (c *ExtraConfig) V1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter) (map[string]rest.Storage, error) {
	c.makeV1Storage.Do(func() {
		c.v1Storage, c.v1StorageErr = c.newV1RESTStorage(RESTOptionsGetter)
	})

	return c.v1Storage, c.v1StorageErr
}

func (c *ExtraConfig) newV1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter) (map[string]rest.Storage, error) {
	kubeInternalClient, err := kclientsetinternal.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}

	sccStorage := c.SCCStorage
	// TODO allow this when we're sure that its storing correctly and we want to allow starting up without embedding kube
	if false && sccStorage == nil {
		sccStorage = sccstorage.NewREST(RESTOptionsGetter)
	}
	podSecurityPolicyReviewStorage := podsecuritypolicyreview.NewREST(
		oscc.NewDefaultSCCMatcher(c.SecurityInformers.Security().InternalVersion().SecurityContextConstraints().Lister()),
		c.KubeInternalInformers.Core().InternalVersion().ServiceAccounts().Lister(),
		kubeInternalClient,
	)
	podSecurityPolicySubjectStorage := podsecuritypolicysubjectreview.NewREST(
		oscc.NewDefaultSCCMatcher(c.SecurityInformers.Security().InternalVersion().SecurityContextConstraints().Lister()),
		kubeInternalClient,
	)
	podSecurityPolicySelfSubjectReviewStorage := podsecuritypolicyselfsubjectreview.NewREST(
		oscc.NewDefaultSCCMatcher(c.SecurityInformers.Security().InternalVersion().SecurityContextConstraints().Lister()),
		kubeInternalClient,
	)

	v1Storage := map[string]rest.Storage{}
	v1Storage["securityContextConstraints"] = sccStorage
	v1Storage["podSecurityPolicyReviews"] = podSecurityPolicyReviewStorage
	v1Storage["podSecurityPolicySubjectReviews"] = podSecurityPolicySubjectStorage
	v1Storage["podSecurityPolicySelfSubjectReviews"] = podSecurityPolicySelfSubjectReviewStorage
	return v1Storage, nil
}
