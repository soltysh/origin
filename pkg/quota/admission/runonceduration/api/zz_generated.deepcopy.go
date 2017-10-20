// +build !ignore_autogenerated_openshift

// This file was autogenerated by deepcopy-gen. Do not edit it manually!

package api

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
			in.(*RunOnceDurationConfig).DeepCopyInto(out.(*RunOnceDurationConfig))
			return nil
		}, InType: reflect.TypeOf(&RunOnceDurationConfig{})},
	)
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *RunOnceDurationConfig) DeepCopyInto(out *RunOnceDurationConfig) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	if in.ActiveDeadlineSecondsLimit != nil {
		in, out := &in.ActiveDeadlineSecondsLimit, &out.ActiveDeadlineSecondsLimit
		if *in == nil {
			*out = nil
		} else {
			*out = new(int64)
			**out = **in
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new RunOnceDurationConfig.
func (in *RunOnceDurationConfig) DeepCopy() *RunOnceDurationConfig {
	if in == nil {
		return nil
	}
	out := new(RunOnceDurationConfig)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *RunOnceDurationConfig) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}
