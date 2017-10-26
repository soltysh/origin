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
	restclient "k8s.io/client-go/rest"

	routeapiv1 "github.com/openshift/origin/pkg/route/apis/route/v1"
	routeallocationcontroller "github.com/openshift/origin/pkg/route/controller/allocation"
	routeetcd "github.com/openshift/origin/pkg/route/registry/route/etcd"
	authorizationclient "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authorization/internalversion"
)

type ExtraConfig struct {
	CoreAPIServerClientConfig *restclient.Config
	RouteAllocator            *routeallocationcontroller.RouteAllocationController

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}

type RouteAPIServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

type RouteAPIServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *RouteAPIServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of RouteAPIServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*RouteAPIServer, error) {
	genericServer, err := c.GenericConfig.New("route.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &RouteAPIServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.RESTOptionsGetter, c.GenericConfig.LoopbackClientConfig)
	if err != nil {
		return nil, err
	}

	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(routeapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, metav1.ParameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = routeapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[routeapiv1.SchemeGroupVersion.Version] = v1Storage
	if err := s.GenericAPIServer.InstallAPIGroup(&apiGroupInfo); err != nil {
		return nil, err
	}

	return s, nil
}

func (c *ExtraConfig) V1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter, LoopbackClientConfig *restclient.Config) (map[string]rest.Storage, error) {
	c.makeV1Storage.Do(func() {
		c.v1Storage, c.v1StorageErr = c.newV1RESTStorage(RESTOptionsGetter, LoopbackClientConfig)
	})

	return c.v1Storage, c.v1StorageErr
}

func (c *ExtraConfig) newV1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter, LoopbackClientConfig *restclient.Config) (map[string]rest.Storage, error) {
	authorizationClient, err := authorizationclient.NewForConfig(LoopbackClientConfig)
	if err != nil {
		return nil, err
	}
	routeStorage, routeStatusStorage, err := routeetcd.NewREST(RESTOptionsGetter, c.RouteAllocator, authorizationClient.SubjectAccessReviews())
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}

	v1Storage := map[string]rest.Storage{}
	v1Storage["routes"] = routeStorage
	v1Storage["routes/status"] = routeStatusStorage
	return v1Storage, nil
}
