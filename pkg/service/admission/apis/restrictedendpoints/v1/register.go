package v1

import (
	"github.com/openshift/origin/pkg/service/admission/apis/restrictedendpoints"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
)

// SchemeGroupVersion is group version used to register these objects
var DeprecatedSchemeGroupVersion = schema.GroupVersion{Group: "", Version: "v1"}

var (
	DeprecatedSchemeBuilder = runtime.NewSchemeBuilder(
		deprecatedAddKnownTypes,
		restrictedendpoints.InstallLegacy,
	)
	DeprecatedInstall = DeprecatedSchemeBuilder.AddToScheme
)

// Adds the list of known types to api.Scheme.
func deprecatedAddKnownTypes(scheme *runtime.Scheme) error {
	scheme.AddKnownTypes(DeprecatedSchemeGroupVersion,
		&RestrictedEndpointsAdmissionConfig{},
	)
	return nil
}
