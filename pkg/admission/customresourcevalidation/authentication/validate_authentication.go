package authentication

import (
	"fmt"
	"io"

	"k8s.io/apimachinery/pkg/api/validation"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/util/validation/field"
	"k8s.io/apiserver/pkg/admission"

	configv1 "github.com/openshift/api/config/v1"
	"github.com/openshift/origin/pkg/admission/customresourcevalidation"
)

const PluginName = "config.openshift.io/ValidateAuthentication"

// Register registers a plugin
func Register(plugins *admission.Plugins) {
	plugins.Register(PluginName, func(config io.Reader) (admission.Interface, error) {
		return customresourcevalidation.NewValidator(
			map[schema.GroupResource]bool{
				configv1.GroupVersion.WithResource("authentications").GroupResource(): true,
			},
			map[schema.GroupVersionKind]customresourcevalidation.ObjectValidator{
				configv1.GroupVersion.WithKind("Authentication"): authenticationV1{},
			})
	})
}

func toAuthenticationV1(uncastObj runtime.Object) (*configv1.Authentication, field.ErrorList) {
	if uncastObj == nil {
		return nil, nil
	}

	errs := field.ErrorList{}

	obj, ok := uncastObj.(*configv1.Authentication)
	if !ok {
		return nil, append(errs,
			field.NotSupported(field.NewPath("kind"), fmt.Sprintf("%T", uncastObj), []string{"Authentication"}),
			field.NotSupported(field.NewPath("apiVersion"), fmt.Sprintf("%T", uncastObj), []string{"config.openshift.io/v1"}))
	}

	return obj, nil
}

type authenticationV1 struct{}

func (authenticationV1) ValidateCreate(uncastObj runtime.Object) field.ErrorList {
	obj, errs := toAuthenticationV1(uncastObj)
	if len(errs) > 0 {
		return errs
	}

	errs = append(errs, validation.ValidateObjectMeta(&obj.ObjectMeta, false, customresourcevalidation.RequireNameCluster, field.NewPath("metadata"))...)
	errs = append(errs, validateAuthenticationSpec(obj.Spec)...)

	return errs
}

func (authenticationV1) ValidateUpdate(uncastObj runtime.Object, uncastOldObj runtime.Object) field.ErrorList {
	obj, errs := toAuthenticationV1(uncastObj)
	if len(errs) > 0 {
		return errs
	}
	oldObj, errs := toAuthenticationV1(uncastOldObj)
	if len(errs) > 0 {
		return errs
	}

	errs = append(errs, validation.ValidateObjectMetaUpdate(&obj.ObjectMeta, &oldObj.ObjectMeta, field.NewPath("metadata"))...)
	errs = append(errs, validateAuthenticationSpec(obj.Spec)...)

	return errs
}

func (authenticationV1) ValidateStatusUpdate(uncastObj runtime.Object, uncastOldObj runtime.Object) field.ErrorList {
	obj, errs := toAuthenticationV1(uncastObj)
	if len(errs) > 0 {
		return errs
	}
	oldObj, errs := toAuthenticationV1(uncastOldObj)
	if len(errs) > 0 {
		return errs
	}

	// TODO validate the obj.  remember that status validation should *never* fail on spec validation errors.
	errs = append(errs, validation.ValidateObjectMetaUpdate(&obj.ObjectMeta, &oldObj.ObjectMeta, field.NewPath("metadata"))...)
	errs = append(errs, validateAuthenticationStatus(obj.Status)...)

	return errs
}

func validateAuthenticationSpec(spec configv1.AuthenticationSpec) field.ErrorList {
	errs := field.ErrorList{}

	// TODO

	return errs
}

func validateAuthenticationStatus(status configv1.AuthenticationStatus) field.ErrorList {
	errs := field.ErrorList{}

	// TODO

	return errs
}
