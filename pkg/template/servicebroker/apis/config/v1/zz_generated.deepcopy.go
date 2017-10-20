// +build !ignore_autogenerated_openshift

// This file was autogenerated by deepcopy-gen. Do not edit it manually!

package v1

import (
	conversion "k8s.io/apimachinery/pkg/conversion"
	runtime "k8s.io/apimachinery/pkg/runtime"
	reflect "reflect"
)

func init() {
	SchemeBuilder.Register(RegisterDeepCopies)
}

// RegisterDeepCopies adds deep-copy functions to the given scheme. Public
// to allow building arbitrary schemes.
//
// Deprecated: deepcopy registration will go away when static deepcopy is fully implemented.
func RegisterDeepCopies(scheme *runtime.Scheme) error {
	return scheme.AddGeneratedDeepCopyFuncs(
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateServiceBrokerConfig).DeepCopyInto(out.(*TemplateServiceBrokerConfig))
			return nil
		}, InType: reflect.TypeOf(new(TemplateServiceBrokerConfig))},
	)
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateServiceBrokerConfig) DeepCopyInto(out *TemplateServiceBrokerConfig) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	if in.TemplateNamespaces != nil {
		in, out := &in.TemplateNamespaces, &out.TemplateNamespaces
		*out = make([]string, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateServiceBrokerConfig.
func (in *TemplateServiceBrokerConfig) DeepCopy() *TemplateServiceBrokerConfig {
	if in == nil {
		return nil
	}
	out := new(TemplateServiceBrokerConfig)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *TemplateServiceBrokerConfig) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}
