package validation

import (
	"fmt"
	"strings"
	"time"

	kapp "k8s.io/kubernetes/cmd/kubelet/app"
	"k8s.io/kubernetes/pkg/util/validation/field"

	"github.com/openshift/origin/pkg/cmd/server/api"
)

func ValidateNodeConfig(config *api.NodeConfig) ValidationResults {
	validationResults := ValidationResults{}

	if len(config.NodeName) == 0 {
		validationResults.AddErrors(field.Required(field.NewPath("nodeName")))
	}
	if len(config.NodeIP) > 0 {
		validationResults.AddErrors(ValidateSpecifiedIP(config.NodeIP, field.NewPath("nodeIP"))...)
	}

	servingInfoPath := field.NewPath("servingInfo")
	validationResults.Append(ValidateServingInfo(config.ServingInfo, servingInfoPath))
	if config.ServingInfo.BindNetwork == "tcp6" {
		validationResults.AddErrors(servingInfoPath.Child("bindNetwork"), config.ServingInfo.BindNetwork, "tcp6 is not a valid bindNetwork for nodes, must be tcp or tcp4")
	}
	validationResults.AddErrors(ValidateKubeConfig(config.MasterKubeConfig, field.NewPath("masterKubeConfig"))...)

	if len(config.DNSIP) > 0 {
		validationResults.AddErrors(ValidateSpecifiedIP(config.DNSIP, field.NewPath("dnsIP"))...)
	}

	validationResults.AddErrors(ValidateImageConfig(config.ImageConfig, field.NewPath("imageConfig"))...)

	if config.PodManifestConfig != nil {
		validationResults.AddErrors(ValidatePodManifestConfig(config.PodManifestConfig, field.NewPath("podManifestConfig"))...)
	}

	validationResults.AddErrors(ValidateNetworkConfig(config.NetworkConfig, field.NewPath("networkConfig"))...)

	validationResults.AddErrors(ValidateDockerConfig(config.DockerConfig, field.NewPath("dockerConfig"))...)

	validationResults.AddErrors(ValidateNodeAuthConfig(config.AuthConfig, field.NewPath("authConfig"))...)

	validationResults.AddErrors(ValidateKubeletExtendedArguments(config.KubeletArguments, field.NewPath("kubeletArguments"))...)

	if _, err := time.ParseDuration(config.IPTablesSyncPeriod); err != nil {
		validationResults.AddErrors(field.Invalid(field.NewPath("iptablesSyncPeriod"), config.IPTablesSyncPeriod, fmt.Sprintf("unable to parse iptablesSyncPeriod: %v. Examples with correct format: '5s', '1m', '2h22m'", err)))
	}

	return validationResults
}

func ValidateNodeAuthConfig(config api.NodeAuthConfig, fldPath *field.Path) field.ErrorList {
	allErrs := field.ErrorList{}

	authenticationCacheTTLPath := fldPath.Child("authenticationCacheTTL")
	if len(config.AuthenticationCacheTTL) == 0 {
		allErrs = append(allErrs, field.Required(authenticationCacheTTLPath))
	} else if ttl, err := time.ParseDuration(config.AuthenticationCacheTTL); err != nil {
		allErrs = append(allErrs, field.Invalid(authenticationCacheTTLPath, config.AuthenticationCacheTTL, fmt.Sprintf("%v", err)))
	} else if ttl < 0 {
		allErrs = append(allErrs, field.Invalid(authenticationCacheTTLPath, config.AuthenticationCacheTTL, fmt.Sprintf("cannot be less than zero")))
	}

	if config.AuthenticationCacheSize <= 0 {
		allErrs = append(allErrs, field.Invalid(fldPath.Child("authenticationCacheSize"), config.AuthenticationCacheSize, fmt.Sprintf("must be greater than zero")))
	}

	authorizationCacheTTLPath := fldPath.Child("authorizationCacheTTL")
	if len(config.AuthorizationCacheTTL) == 0 {
		allErrs = append(allErrs, field.Required(authorizationCacheTTLPath))
	} else if ttl, err := time.ParseDuration(config.AuthorizationCacheTTL); err != nil {
		allErrs = append(allErrs, field.Invalid(authorizationCacheTTLPath, config.AuthorizationCacheTTL, fmt.Sprintf("%v", err)))
	} else if ttl < 0 {
		allErrs = append(allErrs, field.Invalid(authorizationCacheTTLPath, config.AuthorizationCacheTTL, fmt.Sprintf("cannot be less than zero")))
	}

	if config.AuthorizationCacheSize <= 0 {
		allErrs = append(allErrs, field.Invalid(fldPath.Child("authorizationCacheSize"), config.AuthorizationCacheSize, fmt.Sprintf("must be greater than zero")))
	}

	return allErrs
}

func ValidateNetworkConfig(config api.NodeNetworkConfig, fldPath *field.Path) field.ErrorList {
	allErrs := field.ErrorList{}

	if len(config.NetworkPluginName) > 0 {
		if config.MTU == 0 {
			allErrs = append(allErrs, field.Invalid(fldPath.Child("mtu"), config.MTU, fmt.Sprintf("must be greater than zero")))
		}
	}
	return allErrs
}

func ValidateDockerConfig(config api.DockerConfig, fldPath *field.Path) field.ErrorList {
	allErrs := field.ErrorList{}

	switch config.ExecHandlerName {
	case api.DockerExecHandlerNative, api.DockerExecHandlerNsenter:
		// ok
	default:
		validValues := strings.Join([]string{string(api.DockerExecHandlerNative), string(api.DockerExecHandlerNsenter)}, ", ")
		allErrs = append(allErrs, field.Invalid(fldPath.Child("execHandlerName"), config.ExecHandlerName, fmt.Sprintf("must be one of %s", validValues)))
	}

	return allErrs
}

func ValidateKubeletExtendedArguments(config api.ExtendedArguments, fldPath *field.Path) field.ErrorList {
	return ValidateExtendedArguments(config, kapp.NewKubeletServer().AddFlags, fldPath)
}
