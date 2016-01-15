package validation

import (
	"github.com/openshift/origin/pkg/cmd/server/api"
	"k8s.io/kubernetes/pkg/util/validation/field"
)

func ValidateAllInOneConfig(master *api.MasterConfig, node *api.NodeConfig) ValidationResults {
	validationResults := ValidationResults{}

	validationResults.Append(ValidateMasterConfig(master, field.NewPath("masterConfig")))

	validationResults.Append(ValidateNodeConfig(node, field.NewPath("nodeConfig")))

	// Validation between the configs

	return validationResults
}
