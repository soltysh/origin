package admission

import (
	"bytes"
	"io"
	"io/ioutil"
	"os"
	"reflect"

	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/util/sets"
	"k8s.io/apiserver/pkg/admission"
	"k8s.io/apiserver/pkg/admission/plugin/namespace/lifecycle"
	mutatingwebhook "k8s.io/apiserver/pkg/admission/plugin/webhook/mutating"
	validatingwebhook "k8s.io/apiserver/pkg/admission/plugin/webhook/validating"
	"k8s.io/apiserver/pkg/apis/apiserver"
	"k8s.io/kubernetes/plugin/pkg/admission/noderestriction"
	expandpvcadmission "k8s.io/kubernetes/plugin/pkg/admission/storage/persistentvolume/resize"
	storageclassdefaultadmission "k8s.io/kubernetes/plugin/pkg/admission/storage/storageclass/setdefault"

	configv1 "github.com/openshift/api/config/v1"
	oadmission "github.com/openshift/origin/pkg/cmd/server/admission"
	configapi "github.com/openshift/origin/pkg/cmd/server/apis/config"
	configapilatest "github.com/openshift/origin/pkg/cmd/server/apis/config/latest"
	"github.com/openshift/origin/pkg/image/apiserver/admission/apis/imagepolicy"
	imageadmission "github.com/openshift/origin/pkg/image/apiserver/admission/limitrange"
	ingressadmission "github.com/openshift/origin/pkg/network/apiserver/admission"
	overrideapi "github.com/openshift/origin/pkg/quota/apiserver/admission/apis/clusterresourceoverride"
	"github.com/openshift/origin/pkg/security/apiserver/admission/sccadmission"
	"github.com/openshift/origin/pkg/service/admission/externalipranger"
	"github.com/openshift/origin/pkg/service/admission/restrictedendpoints"
)

var (
	// these are admission plugins that cannot be applied until after the kubeapiserver starts.
	// TODO if nothing comes to mind in 3.10, kill this
	SkipRunLevelZeroPlugins = sets.NewString()
	// these are admission plugins that cannot be applied until after the openshiftapiserver apiserver starts.
	SkipRunLevelOnePlugins = sets.NewString(
		"ProjectRequestLimit",
		"openshift.io/RestrictSubjectBindings",
		"openshift.io/ClusterResourceQuota",
		imagepolicy.PluginName,
		overrideapi.PluginName,
		"OriginPodNodeEnvironment",
		"RunOnceDuration",
		sccadmission.PluginName,
		"SCCExecRestrictions",
	)

	// OpenShiftAdmissionPlugins gives the in-order default admission chain for openshift resources.
	OpenShiftAdmissionPlugins = []string{
		lifecycle.PluginName,
		"ProjectRequestLimit",
		"openshift.io/JenkinsBootstrapper",
		"openshift.io/BuildConfigSecretInjector",
		"BuildByStrategy",
		imageadmission.PluginName,
		"PodNodeConstraints",
		"OwnerReferencesPermissionEnforcement",
		"Initializers",
		"MutatingAdmissionWebhook",
		"ValidatingAdmissionWebhook",
		"ResourceQuota",
		"openshift.io/ClusterResourceQuota",
	}

	// KubeAdmissionPlugins gives the in-order default admission chain for kube resources.
	KubeAdmissionPlugins = []string{
		"AlwaysAdmit",
		"NamespaceAutoProvision",
		"NamespaceExists",
		lifecycle.PluginName,
		"EventRateLimit",
		"openshift.io/RestrictSubjectBindings",
		"RunOnceDuration",
		"PodNodeConstraints",
		"OriginPodNodeEnvironment",
		"PodNodeSelector",
		overrideapi.PluginName,
		externalipranger.ExternalIPPluginName,
		restrictedendpoints.RestrictedEndpointsPluginName,
		imagepolicy.PluginName,
		"ImagePolicyWebhook",
		"PodPreset",
		"LimitRanger",
		"ServiceAccount",
		noderestriction.PluginName,
		"SecurityContextDeny",
		sccadmission.PluginName,
		"PodSecurityPolicy",
		"DenyEscalatingExec",
		"DenyExecOnPrivileged",
		storageclassdefaultadmission.PluginName,
		expandpvcadmission.PluginName,
		"AlwaysPullImages",
		"LimitPodHardAntiAffinityTopology",
		"SCCExecRestrictions",
		"PersistentVolumeLabel",
		"OwnerReferencesPermissionEnforcement",
		ingressadmission.IngressAdmission,
		"Priority",
		"ExtendedResourceToleration",
		"DefaultTolerationSeconds",
		"StorageObjectInUseProtection",
		"Initializers",
		mutatingwebhook.PluginName,
		validatingwebhook.PluginName,
		"PodTolerationRestriction",
		"AlwaysDeny",
		// NOTE: ResourceQuota and ClusterResourceQuota must be the last 2 plugins.
		// DO NOT ADD ANY PLUGINS AFTER THIS LINE!
		"ResourceQuota",
		"openshift.io/ClusterResourceQuota",
	}
)

// fixupAdmissionPlugins fixes the input plugins to handle deprecation and duplicates.
func fixupAdmissionPlugins(plugins []string) []string {
	result := replace(plugins, "openshift.io/OriginResourceQuota", "ResourceQuota")
	result = dedupe(result)
	return result
}

func NewAdmissionChains(
	admissionConfigFiles []string,
	explicitOn, explicitOff []string,
	pluginConfig map[string]configv1.AdmissionPluginConfig,
	admissionInitializer admission.PluginInitializer,
	admissionDecorator admission.Decorator,
) (admission.Interface, error) {
	admissionPluginConfigFilename := ""
	if len(admissionConfigFiles) > 0 {
		admissionPluginConfigFilename = admissionConfigFiles[0]

	} else {
		upstreamAdmissionConfig, err := ConvertOpenshiftAdmissionConfigToKubeAdmissionConfig(pluginConfig)
		if err != nil {
			return nil, err
		}
		configBytes, err := configapilatest.WriteYAML(upstreamAdmissionConfig)
		if err != nil {
			return nil, err
		}

		tempFile, err := ioutil.TempFile("", "master-config.yaml")
		if err != nil {
			return nil, err
		}
		defer os.Remove(tempFile.Name())
		if _, err := tempFile.Write(configBytes); err != nil {
			return nil, err
		}
		tempFile.Close()
		admissionPluginConfigFilename = tempFile.Name()
	}

	allOffPlugins := append(DefaultOffPlugins.List(), explicitOff...)
	disabledPlugins := sets.NewString(allOffPlugins...)
	enabledPlugins := sets.NewString(explicitOn...)
	disabledPlugins = disabledPlugins.Difference(enabledPlugins)
	orderedPlugins := []string{}
	for _, plugin := range OpenShiftAdmissionPlugins {
		if !disabledPlugins.Has(plugin) {
			orderedPlugins = append(orderedPlugins, plugin)
		}
	}
	admissionChain, err := newAdmissionChainFunc(fixupAdmissionPlugins(orderedPlugins), admissionPluginConfigFilename, admissionInitializer, admissionDecorator)
	if err != nil {
		return nil, err
	}

	return admissionChain, err
}

// newAdmissionChainFunc is for unit testing only.  You should NEVER OVERRIDE THIS outside of a unit test.
var newAdmissionChainFunc = newAdmissionChain

func newAdmissionChain(pluginNames []string, admissionConfigFilename string, admissionInitializer admission.PluginInitializer, admissionDecorator admission.Decorator) (admission.Interface, error) {
	plugins := []admission.Interface{}
	for _, pluginName := range pluginNames {
		var (
			plugin admission.Interface
		)

		// TODO this needs to be refactored to use the admission scheme we created upstream.  I think this holds us for the rebase.
		pluginsConfigProvider, err := admission.ReadAdmissionConfiguration([]string{pluginName}, admissionConfigFilename, configapi.Scheme)
		if err != nil {
			return nil, err
		}
		plugin, err = OriginAdmissionPlugins.NewFromPlugins([]string{pluginName}, pluginsConfigProvider, admissionInitializer, admissionDecorator)
		if err != nil {
			// should have been caught with validation
			return nil, err
		}
		if plugin == nil {
			continue
		}

		plugins = append(plugins, plugin)

	}

	// ensure that plugins have been properly initialized
	if err := oadmission.Validate(plugins); err != nil {
		return nil, err
	}

	return admission.NewChainHandler(plugins...), nil
}

// replace returns a slice where each instance of the input that is x is replaced with y
func replace(input []string, x, y string) []string {
	result := []string{}
	for i := range input {
		if input[i] == x {
			result = append(result, y)
		} else {
			result = append(result, input[i])
		}
	}
	return result
}

// dedupe removes duplicate items from the input list.
// the last instance of a duplicate is kept in the input list.
func dedupe(input []string) []string {
	items := sets.NewString()
	result := []string{}
	for i := len(input) - 1; i >= 0; i-- {
		if items.Has(input[i]) {
			continue
		}
		items.Insert(input[i])
		result = append([]string{input[i]}, result...)
	}
	return result
}

func init() {
	// add a filter that will remove DefaultAdmissionConfig
	admission.FactoryFilterFn = filterEnableAdmissionConfigs
}

func filterEnableAdmissionConfigs(delegate admission.Factory) admission.Factory {
	return func(config io.Reader) (admission.Interface, error) {
		config1, config2, err := splitStream(config)
		if err != nil {
			return nil, err
		}
		// if the config isn't a DefaultAdmissionConfig, then assume we're enabled (we were called after all)
		// if the config *is* a DefaultAdmissionConfig and it explicitly said
		obj, err := configapilatest.ReadYAML(config1)
		// if we can't read it, let the plugin deal with it
		if err != nil {
			return delegate(config2)
		}
		// if nothing was there, let the plugin deal with it
		if obj == nil {
			return delegate(config2)
		}
		// if it wasn't a DefaultAdmissionConfig object, let the plugin deal with it
		if _, ok := obj.(*configapi.DefaultAdmissionConfig); !ok {
			return delegate(config2)
		}

		// if it was a DefaultAdmissionConfig, then it must have said "enabled" and it wasn't really meant for the
		// admission plugin
		return delegate(nil)
	}
}

// splitStream reads the stream bytes and constructs two copies of it.
func splitStream(config io.Reader) (io.Reader, io.Reader, error) {
	if config == nil || reflect.ValueOf(config).IsNil() {
		return nil, nil, nil
	}

	configBytes, err := ioutil.ReadAll(config)
	if err != nil {
		return nil, nil, err
	}

	return bytes.NewBuffer(configBytes), bytes.NewBuffer(configBytes), nil
}

func ConvertOpenshiftAdmissionConfigToKubeAdmissionConfig(in map[string]configv1.AdmissionPluginConfig) (*apiserver.AdmissionConfiguration, error) {
	ret := &apiserver.AdmissionConfiguration{}

	for _, pluginName := range sets.StringKeySet(in).List() {
		openshiftConfig := in[pluginName]

		kubeConfig := apiserver.AdmissionPluginConfiguration{
			Name: pluginName,
			Path: openshiftConfig.Location,
		}

		kubeConfig.Configuration = &runtime.Unknown{
			Raw: openshiftConfig.Configuration.Raw,
		}
		ret.Plugins = append(ret.Plugins, kubeConfig)
	}

	return ret, nil
}
