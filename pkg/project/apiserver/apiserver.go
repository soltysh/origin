package apiserver

import (
	"sync"

	"github.com/golang/glog"

	"k8s.io/apimachinery/pkg/apimachinery/registered"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	"k8s.io/apiserver/pkg/registry/rest"
	genericapiserver "k8s.io/apiserver/pkg/server"
	restclient "k8s.io/client-go/rest"
	kclientsetinternal "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset"
	authorizationclient "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authorization/internalversion"
	kinternalinformers "k8s.io/kubernetes/pkg/client/informers/informers_generated/internalversion"

	configapi "github.com/openshift/origin/pkg/cmd/server/api"
	projectapiv1 "github.com/openshift/origin/pkg/project/apis/project/v1"
	projectauth "github.com/openshift/origin/pkg/project/auth"
	projectcache "github.com/openshift/origin/pkg/project/cache"
	projectclient "github.com/openshift/origin/pkg/project/generated/internalclientset"
	projectproxy "github.com/openshift/origin/pkg/project/registry/project/proxy"
	projectrequeststorage "github.com/openshift/origin/pkg/project/registry/projectrequest/delegated"
	templateclient "github.com/openshift/origin/pkg/template/generated/internalclientset"
)

type ExtraConfig struct {
	CoreAPIServerClientConfig *restclient.Config
	KubeInternalInformers     kinternalinformers.SharedInformerFactory
	ProjectAuthorizationCache *projectauth.AuthorizationCache
	ProjectCache              *projectcache.ProjectCache
	ProjectRequestTemplate    string
	ProjectRequestMessage     string

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}

type ProjectAPIServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

// ProjectAPIServer contains state for a Kubernetes cluster master/api server.
type ProjectAPIServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *ProjectAPIServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of ProjectAPIServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*ProjectAPIServer, error) {
	genericServer, err := c.GenericConfig.New("project.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &ProjectAPIServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.LoopbackClientConfig)
	if err != nil {
		return nil, err
	}

	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(projectapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, metav1.ParameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = projectapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[projectapiv1.SchemeGroupVersion.Version] = v1Storage
	if err := s.GenericAPIServer.InstallAPIGroup(&apiGroupInfo); err != nil {
		return nil, err
	}

	return s, nil
}

func (c *ExtraConfig) V1RESTStorage(LoopbackClientConfig *restclient.Config) (map[string]rest.Storage, error) {
	c.makeV1Storage.Do(func() {
		c.v1Storage, c.v1StorageErr = c.newV1RESTStorage(LoopbackClientConfig)
	})

	return c.v1Storage, c.v1StorageErr
}

func (c *ExtraConfig) newV1RESTStorage(LoopbackClientConfig *restclient.Config) (map[string]rest.Storage, error) {
	kubeInternalClient, err := kclientsetinternal.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	projectClient, err := projectclient.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	templateClient, err := templateclient.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	authorizationClient, err := authorizationclient.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}

	projectStorage := projectproxy.NewREST(kubeInternalClient.Core().Namespaces(), c.ProjectAuthorizationCache, c.ProjectAuthorizationCache, c.ProjectCache)

	namespace, templateName, err := configapi.ParseNamespaceAndName(c.ProjectRequestTemplate)
	if err != nil {
		glog.Errorf("Error parsing project request template value: %v", err)
		// we can continue on, the storage that gets created will be valid, it simply won't work properly.  There's no reason to kill the master
	}

	projectRequestStorage := projectrequeststorage.NewREST(
		c.ProjectRequestMessage,
		namespace, templateName,
		projectClient.Project(),
		templateClient,
		authorizationClient.SubjectAccessReviews(),
		LoopbackClientConfig,
		c.KubeInternalInformers.Rbac().InternalVersion().RoleBindings().Lister(),
	)

	v1Storage := map[string]rest.Storage{}
	v1Storage["projects"] = projectStorage
	v1Storage["projectRequests"] = projectRequestStorage
	return v1Storage, nil
}
