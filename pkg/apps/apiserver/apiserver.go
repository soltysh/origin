package apiserver

import (
	"fmt"
	"sync"

	"k8s.io/apimachinery/pkg/apimachinery/registered"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	kadmission "k8s.io/apiserver/pkg/admission"
	genericregistry "k8s.io/apiserver/pkg/registry/generic"
	"k8s.io/apiserver/pkg/registry/rest"
	genericapiserver "k8s.io/apiserver/pkg/server"
	kclientsetexternal "k8s.io/client-go/kubernetes"
	restclient "k8s.io/client-go/rest"
	kapi "k8s.io/kubernetes/pkg/api"
	kclientsetinternal "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset"
	kubeletclient "k8s.io/kubernetes/pkg/kubelet/client"

	appsapiv1 "github.com/openshift/origin/pkg/apps/apis/apps/v1"
	appsclientinternal "github.com/openshift/origin/pkg/apps/generated/internalclientset"
	oappsclient "github.com/openshift/origin/pkg/apps/generated/internalclientset"
	deployconfigetcd "github.com/openshift/origin/pkg/apps/registry/deployconfig/etcd"
	deploylogregistry "github.com/openshift/origin/pkg/apps/registry/deploylog"
	deployconfiginstantiate "github.com/openshift/origin/pkg/apps/registry/instantiate"
	deployrollback "github.com/openshift/origin/pkg/apps/registry/rollback"
	imageclientinternal "github.com/openshift/origin/pkg/image/generated/internalclientset"
)

type ExtraConfig struct {
	CoreAPIServerClientConfig *restclient.Config
	KubeletClientConfig       *kubeletclient.KubeletClientConfig

	// TODO these should all become local eventually
	Scheme   *runtime.Scheme
	Registry *registered.APIRegistrationManager
	Codecs   serializer.CodecFactory

	makeV1Storage sync.Once
	v1Storage     map[string]rest.Storage
	v1StorageErr  error
}

type AppsServerConfig struct {
	GenericConfig *genericapiserver.RecommendedConfig
	ExtraConfig   ExtraConfig
}

type AppsServer struct {
	GenericAPIServer *genericapiserver.GenericAPIServer
}

type completedConfig struct {
	GenericConfig genericapiserver.CompletedConfig
	ExtraConfig   *ExtraConfig
}

// Complete fills in any fields not set that are required to have valid data. It's mutating the receiver.
func (c *AppsServerConfig) Complete() completedConfig {
	cfg := completedConfig{
		c.GenericConfig.Complete(),
		&c.ExtraConfig,
	}

	return cfg
}

// New returns a new instance of AppsServer from the given config.
func (c completedConfig) New(delegationTarget genericapiserver.DelegationTarget) (*AppsServer, error) {
	genericServer, err := c.GenericConfig.New("apps.openshift.io-apiserver", delegationTarget)
	if err != nil {
		return nil, err
	}

	s := &AppsServer{
		GenericAPIServer: genericServer,
	}

	v1Storage, err := c.ExtraConfig.V1RESTStorage(c.GenericConfig.RESTOptionsGetter, c.GenericConfig.LoopbackClientConfig, c.GenericConfig.AdmissionControl)
	if err != nil {
		return nil, err
	}

	parameterCodec := runtime.NewParameterCodec(c.ExtraConfig.Scheme)
	apiGroupInfo := genericapiserver.NewDefaultAPIGroupInfo(appsapiv1.GroupName, c.ExtraConfig.Registry, c.ExtraConfig.Scheme, parameterCodec, c.ExtraConfig.Codecs)
	apiGroupInfo.GroupMeta.GroupVersion = appsapiv1.SchemeGroupVersion
	apiGroupInfo.VersionedResourcesStorageMap[appsapiv1.SchemeGroupVersion.Version] = v1Storage
	if err := s.GenericAPIServer.InstallAPIGroup(&apiGroupInfo); err != nil {
		return nil, err
	}

	return s, nil
}

func (c *ExtraConfig) V1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter, LoopbackClientConfig *restclient.Config, AdmissionControl kadmission.Interface) (map[string]rest.Storage, error) {
	c.makeV1Storage.Do(func() {
		c.v1Storage, c.v1StorageErr = c.newV1RESTStorage(RESTOptionsGetter, LoopbackClientConfig, AdmissionControl)
	})

	return c.v1Storage, c.v1StorageErr
}

func (c *ExtraConfig) newV1RESTStorage(RESTOptionsGetter genericregistry.RESTOptionsGetter, LoopbackClientConfig *restclient.Config, AdmissionControl kadmission.Interface) (map[string]rest.Storage, error) {
	// TODO sort out who is using this and why.  it was hardcoded before the migration and I suspect that it is being used
	// to serialize out objects into annotations.
	externalVersionCodec := kapi.Codecs.LegacyCodec(schema.GroupVersion{Group: "", Version: "v1"})
	openshiftInternalAppsClient, err := appsclientinternal.NewForConfig(LoopbackClientConfig)
	if err != nil {
		return nil, err
	}
	// This client is using the core api server client config, since the apps server doesn't host images
	openshiftInternalImageClient, err := imageclientinternal.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	kubeInternalClient, err := kclientsetinternal.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	kubeExternalClient, err := kclientsetexternal.NewForConfig(c.CoreAPIServerClientConfig)
	if err != nil {
		return nil, err
	}
	nodeConnectionInfoGetter, err := kubeletclient.NewNodeConnectionInfoGetter(kubeExternalClient.CoreV1().Nodes(), *c.KubeletClientConfig)
	if err != nil {
		return nil, fmt.Errorf("unable to configure the node connection info getter: %v", err)
	}

	deployConfigStorage, deployConfigStatusStorage, deployConfigScaleStorage, err := deployconfigetcd.NewREST(RESTOptionsGetter)
	if err != nil {
		return nil, err
	}
	dcInstantiateStorage := deployconfiginstantiate.NewREST(
		*deployConfigStorage.Store,
		openshiftInternalImageClient,
		kubeInternalClient,
		externalVersionCodec,
		AdmissionControl,
	)
	deployConfigRollbackStorage := deployrollback.NewREST(openshiftInternalAppsClient, kubeInternalClient, externalVersionCodec)

	v1Storage := map[string]rest.Storage{}
	v1Storage["deploymentConfigs"] = deployConfigStorage
	v1Storage["deploymentConfigs/scale"] = deployConfigScaleStorage
	v1Storage["deploymentConfigs/status"] = deployConfigStatusStorage
	v1Storage["deploymentConfigs/rollback"] = deployConfigRollbackStorage
	v1Storage["deploymentConfigs/log"] = deploylogregistry.NewREST(openshiftInternalAppsClient.Apps(), kubeInternalClient.Core(), kubeInternalClient.Core(), nodeConnectionInfoGetter)
	v1Storage["deploymentConfigs/instantiate"] = dcInstantiateStorage
	return v1Storage, nil
}

// LegacyLegacyDCRollbackMutator allows us to inject a one-off endpoint into oapi
type LegacyLegacyDCRollbackMutator struct {
	CoreAPIServerClientConfig *restclient.Config
	Version                   schema.GroupVersion
}

func (l LegacyLegacyDCRollbackMutator) Mutate(legacyStorage map[schema.GroupVersion]map[string]rest.Storage) {
	externalVersionCodec := kapi.Codecs.LegacyCodec(schema.GroupVersion{Group: "", Version: "v1"})
	originAppsClient := oappsclient.NewForConfigOrDie(l.CoreAPIServerClientConfig)
	kubeInternalClient := kclientsetinternal.NewForConfigOrDie(l.CoreAPIServerClientConfig)
	deployRollbackClient := deployrollback.Client{
		GRFn: deployrollback.NewRollbackGenerator().GenerateRollback,
		DeploymentConfigGetter:      originAppsClient.Apps(),
		ReplicationControllerGetter: kubeInternalClient.Core(),
	}
	// TODO: Deprecate this
	legacyStorage[l.Version]["deploymentConfigRollbacks"] = deployrollback.NewDeprecatedREST(deployRollbackClient, externalVersionCodec)
}
