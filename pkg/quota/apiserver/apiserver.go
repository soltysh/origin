package apiserver

import (
	"fmt"
	"sync"

	"k8s.io/apimachinery/pkg/apimachinery/registered"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	genericregistry "k8s.io/apiserver/pkg/registry/generic"
	"k8s.io/apiserver/pkg/registry/rest"
	genericapiserver "k8s.io/apiserver/pkg/server"
	kinternalinformers "k8s.io/kubernetes/pkg/client/informers/informers_generated/internalversion"

	quotaapiv1 "github.com/openshift/origin/pkg/quota/apis/quota/v1"
	"github.com/openshift/origin/pkg/quota/controller/clusterquotamapping"
	quotainformer "github.com/openshift/origin/pkg/quota/generated/informers/internalversion"
	appliedclusterresourcequotaregistry "github.com/openshift/origin/pkg/quota/registry/appliedclusterresourcequota"
	clusterresourcequotaetcd "github.com/openshift/origin/pkg/quota/registry/clusterresourcequota/etcd"
)

type ExtraConfig struct {
	ClusterQuotaMappingController *clusterquotamapping.ClusterQuotaMappingController
	QuotaInformers                quotainformer.SharedInformerFactory
	KubeInternalInformers         kinternalinformers.SharedInformerFactory

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}

type QuotaAPIServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

type QuotaAPIServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *QuotaAPIServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of QuotaAPIServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*QuotaAPIServer, error) {
	genericServer, err := c.GenericConfig.New("quota.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &QuotaAPIServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.RESTOptionsGetter)
	if err != nil {
		return nil, err
	}

	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(quotaapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, metav1.ParameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = quotaapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[quotaapiv1.SchemeGroupVersion.Version] = v1Storage
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
	clusterResourceQuotaStorage, clusterResourceQuotaStatusStorage, err := clusterresourcequotaetcd.NewREST(RESTOptionsGetter)
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}

	v1Storage := map[string]rest.Storage{}
	v1Storage["clusterResourceQuotas"] = clusterResourceQuotaStorage
	v1Storage["clusterResourceQuotas/status"] = clusterResourceQuotaStatusStorage
	v1Storage["appliedClusterResourceQuotas"] = appliedclusterresourcequotaregistry.NewREST(
		c.ClusterQuotaMappingController.GetClusterQuotaMapper(),
		c.QuotaInformers.Quota().InternalVersion().ClusterResourceQuotas().Lister(),
		c.KubeInternalInformers.Core().InternalVersion().Namespaces().Lister(),
	)
	return v1Storage, nil
}
