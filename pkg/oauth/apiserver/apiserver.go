package apiserver

import (
	"fmt"
	"sync"

	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	genericregistry "k8s.io/apiserver/pkg/registry/generic"
	"k8s.io/apiserver/pkg/registry/rest"
	genericapiserver "k8s.io/apiserver/pkg/server"
	corev1 "k8s.io/client-go/kubernetes/typed/core/v1"
	restclient "k8s.io/client-go/rest"
	coreclient "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/core/internalversion"

	configapi "github.com/openshift/origin/pkg/cmd/server/api"
	oauthapi "github.com/openshift/origin/pkg/oauth/apis/oauth"
	oauthapiv1 "github.com/openshift/origin/pkg/oauth/apis/oauth/v1"
	oauthclient "github.com/openshift/origin/pkg/oauth/generated/internalclientset/typed/oauth/internalversion"
	accesstokenetcd "github.com/openshift/origin/pkg/oauth/registry/oauthaccesstoken/etcd"
	authorizetokenetcd "github.com/openshift/origin/pkg/oauth/registry/oauthauthorizetoken/etcd"
	clientetcd "github.com/openshift/origin/pkg/oauth/registry/oauthclient/etcd"
	clientauthetcd "github.com/openshift/origin/pkg/oauth/registry/oauthclientauthorization/etcd"
	routeclient "github.com/openshift/origin/pkg/route/generated/internalclientset"
	saoauth "github.com/openshift/origin/pkg/serviceaccounts/oauthclient"
	"k8s.io/apimachinery/pkg/apimachinery/registered"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type ExtraConfig struct {
	CoreAPIServerClientConfig *restclient.Config
	ServiceAccountMethod      configapi.GrantHandlerType

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}
type OAuthAPIServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

type OAuthAPIServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *OAuthAPIServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of OAuthAPIServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*OAuthAPIServer, error) {
	genericServer, err := c.GenericConfig.New("oauth.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &OAuthAPIServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.RESTOptionsGetter, c.GenericConfig.LoopbackClientConfig)
	if err != nil {
		return nil, err
	}

	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(oauthapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, metav1.ParameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = oauthapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[oauthapiv1.SchemeGroupVersion.Version] = v1Storage
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

	clientStorage, err := clientetcd.NewREST(RESTOptionsGetter)
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}

	// If OAuth is disabled, set the strategy to Deny
	saAccountGrantMethod := oauthapi.GrantHandlerDeny
	if len(c.ServiceAccountMethod) > 0 {
		// Otherwise, take the value provided in master-config.yaml
		saAccountGrantMethod = oauthapi.GrantHandlerType(c.ServiceAccountMethod)
	}

	oauthClient, err := oauthclient.NewForConfig(LoopbackClientConfig)
	if err != nil {
		return nil, err
	}
	coreClient, err := coreclient.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	routeClient, err := routeclient.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	coreV1Client, err := corev1.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}

	combinedOAuthClientGetter := saoauth.NewServiceAccountOAuthClientGetter(
		coreClient,
		coreClient,
		coreV1Client.Events(""),
		routeClient.Route(),
		oauthClient.OAuthClients(),
		saAccountGrantMethod,
	)
	authorizeTokenStorage, err := authorizetokenetcd.NewREST(RESTOptionsGetter, combinedOAuthClientGetter)
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}
	accessTokenStorage, err := accesstokenetcd.NewREST(RESTOptionsGetter, combinedOAuthClientGetter)
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}
	clientAuthorizationStorage, err := clientauthetcd.NewREST(RESTOptionsGetter, combinedOAuthClientGetter)
	if err != nil {
		return nil, fmt.Errorf("error building REST storage: %v", err)
	}

	v1Storage := map[string]rest.Storage{}
	v1Storage["oAuthAuthorizeTokens"] = authorizeTokenStorage
	v1Storage["oAuthAccessTokens"] = accessTokenStorage
	v1Storage["oAuthClients"] = clientStorage
	v1Storage["oAuthClientAuthorizations"] = clientAuthorizationStorage
	return v1Storage, nil
}
