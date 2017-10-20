// +build !ignore_autogenerated_openshift

// This file was autogenerated by deepcopy-gen. Do not edit it manually!

package template

import (
	conversion "k8s.io/apimachinery/pkg/conversion"
	runtime "k8s.io/apimachinery/pkg/runtime"
	api "k8s.io/kubernetes/pkg/api"
	reflect "reflect"
	unsafe "unsafe"
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
			in.(*BrokerTemplateInstance).DeepCopyInto(out.(*BrokerTemplateInstance))
			return nil
		}, InType: reflect.TypeOf(new(BrokerTemplateInstance))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*BrokerTemplateInstanceList).DeepCopyInto(out.(*BrokerTemplateInstanceList))
			return nil
		}, InType: reflect.TypeOf(new(BrokerTemplateInstanceList))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*BrokerTemplateInstanceSpec).DeepCopyInto(out.(*BrokerTemplateInstanceSpec))
			return nil
		}, InType: reflect.TypeOf(new(BrokerTemplateInstanceSpec))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*ExtraValue).DeepCopyInto(out.(*ExtraValue))
			return nil
		}, InType: reflect.TypeOf(new(ExtraValue))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*Parameter).DeepCopyInto(out.(*Parameter))
			return nil
		}, InType: reflect.TypeOf(new(Parameter))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*Template).DeepCopyInto(out.(*Template))
			return nil
		}, InType: reflect.TypeOf(new(Template))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstance).DeepCopyInto(out.(*TemplateInstance))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstance))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceCondition).DeepCopyInto(out.(*TemplateInstanceCondition))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceCondition))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceConditionType).DeepCopyInto(out.(*TemplateInstanceConditionType))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceConditionType))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceList).DeepCopyInto(out.(*TemplateInstanceList))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceList))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceObject).DeepCopyInto(out.(*TemplateInstanceObject))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceObject))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceRequester).DeepCopyInto(out.(*TemplateInstanceRequester))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceRequester))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceSpec).DeepCopyInto(out.(*TemplateInstanceSpec))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceSpec))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateInstanceStatus).DeepCopyInto(out.(*TemplateInstanceStatus))
			return nil
		}, InType: reflect.TypeOf(new(TemplateInstanceStatus))},
		conversion.GeneratedDeepCopyFunc{Fn: func(in interface{}, out interface{}, c *conversion.Cloner) error {
			in.(*TemplateList).DeepCopyInto(out.(*TemplateList))
			return nil
		}, InType: reflect.TypeOf(new(TemplateList))},
	)
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *BrokerTemplateInstance) DeepCopyInto(out *BrokerTemplateInstance) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ObjectMeta.DeepCopyInto(&out.ObjectMeta)
	in.Spec.DeepCopyInto(&out.Spec)
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new BrokerTemplateInstance.
func (in *BrokerTemplateInstance) DeepCopy() *BrokerTemplateInstance {
	if in == nil {
		return nil
	}
	out := new(BrokerTemplateInstance)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *BrokerTemplateInstance) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *BrokerTemplateInstanceList) DeepCopyInto(out *BrokerTemplateInstanceList) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]BrokerTemplateInstance, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new BrokerTemplateInstanceList.
func (in *BrokerTemplateInstanceList) DeepCopy() *BrokerTemplateInstanceList {
	if in == nil {
		return nil
	}
	out := new(BrokerTemplateInstanceList)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *BrokerTemplateInstanceList) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *BrokerTemplateInstanceSpec) DeepCopyInto(out *BrokerTemplateInstanceSpec) {
	*out = *in
	out.TemplateInstance = in.TemplateInstance
	out.Secret = in.Secret
	if in.BindingIDs != nil {
		in, out := &in.BindingIDs, &out.BindingIDs
		*out = make([]string, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new BrokerTemplateInstanceSpec.
func (in *BrokerTemplateInstanceSpec) DeepCopy() *BrokerTemplateInstanceSpec {
	if in == nil {
		return nil
	}
	out := new(BrokerTemplateInstanceSpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *ExtraValue) DeepCopyInto(out *ExtraValue) {
	{
		in := (*[]string)(unsafe.Pointer(in))
		out := (*[]string)(unsafe.Pointer(out))
		*out = make([]string, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new ExtraValue.
func (in *ExtraValue) DeepCopy() *ExtraValue {
	if in == nil {
		return nil
	}
	out := new(ExtraValue)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *Parameter) DeepCopyInto(out *Parameter) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new Parameter.
func (in *Parameter) DeepCopy() *Parameter {
	if in == nil {
		return nil
	}
	out := new(Parameter)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *Template) DeepCopyInto(out *Template) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ObjectMeta.DeepCopyInto(&out.ObjectMeta)
	if in.Parameters != nil {
		in, out := &in.Parameters, &out.Parameters
		*out = make([]Parameter, len(*in))
		copy(*out, *in)
	}
	if in.Objects != nil {
		in, out := &in.Objects, &out.Objects
		*out = make([]runtime.Object, len(*in))
		for i := range *in {
			if (*in)[i] == nil {
				(*out)[i] = nil
			} else {
				(*out)[i] = (*in)[i].DeepCopyObject()
			}
		}
	}
	if in.ObjectLabels != nil {
		in, out := &in.ObjectLabels, &out.ObjectLabels
		*out = make(map[string]string, len(*in))
		for key, val := range *in {
			(*out)[key] = val
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new Template.
func (in *Template) DeepCopy() *Template {
	if in == nil {
		return nil
	}
	out := new(Template)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *Template) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstance) DeepCopyInto(out *TemplateInstance) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ObjectMeta.DeepCopyInto(&out.ObjectMeta)
	in.Spec.DeepCopyInto(&out.Spec)
	in.Status.DeepCopyInto(&out.Status)
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstance.
func (in *TemplateInstance) DeepCopy() *TemplateInstance {
	if in == nil {
		return nil
	}
	out := new(TemplateInstance)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *TemplateInstance) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceCondition) DeepCopyInto(out *TemplateInstanceCondition) {
	*out = *in
	in.LastTransitionTime.DeepCopyInto(&out.LastTransitionTime)
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceCondition.
func (in *TemplateInstanceCondition) DeepCopy() *TemplateInstanceCondition {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceCondition)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceConditionType) DeepCopyInto(out *TemplateInstanceConditionType) {
	{
		in := (*string)(unsafe.Pointer(in))
		out := (*string)(unsafe.Pointer(out))
		*out = *in
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceConditionType.
func (in *TemplateInstanceConditionType) DeepCopy() *TemplateInstanceConditionType {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceConditionType)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceList) DeepCopyInto(out *TemplateInstanceList) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]TemplateInstance, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceList.
func (in *TemplateInstanceList) DeepCopy() *TemplateInstanceList {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceList)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *TemplateInstanceList) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceObject) DeepCopyInto(out *TemplateInstanceObject) {
	*out = *in
	out.Ref = in.Ref
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceObject.
func (in *TemplateInstanceObject) DeepCopy() *TemplateInstanceObject {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceObject)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceRequester) DeepCopyInto(out *TemplateInstanceRequester) {
	*out = *in
	if in.Groups != nil {
		in, out := &in.Groups, &out.Groups
		*out = make([]string, len(*in))
		copy(*out, *in)
	}
	if in.Extra != nil {
		in, out := &in.Extra, &out.Extra
		*out = make(map[string]ExtraValue, len(*in))
		for key, val := range *in {
			newVal := new(ExtraValue)
			val.DeepCopyInto(newVal)
			(*out)[key] = *newVal
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceRequester.
func (in *TemplateInstanceRequester) DeepCopy() *TemplateInstanceRequester {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceRequester)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceSpec) DeepCopyInto(out *TemplateInstanceSpec) {
	*out = *in
	in.Template.DeepCopyInto(&out.Template)
	if in.Secret != nil {
		in, out := &in.Secret, &out.Secret
		if *in == nil {
			*out = nil
		} else {
			*out = new(api.LocalObjectReference)
			**out = **in
		}
	}
	if in.Requester != nil {
		in, out := &in.Requester, &out.Requester
		if *in == nil {
			*out = nil
		} else {
			*out = new(TemplateInstanceRequester)
			(*in).DeepCopyInto(*out)
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceSpec.
func (in *TemplateInstanceSpec) DeepCopy() *TemplateInstanceSpec {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceSpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateInstanceStatus) DeepCopyInto(out *TemplateInstanceStatus) {
	*out = *in
	if in.Conditions != nil {
		in, out := &in.Conditions, &out.Conditions
		*out = make([]TemplateInstanceCondition, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	if in.Objects != nil {
		in, out := &in.Objects, &out.Objects
		*out = make([]TemplateInstanceObject, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateInstanceStatus.
func (in *TemplateInstanceStatus) DeepCopy() *TemplateInstanceStatus {
	if in == nil {
		return nil
	}
	out := new(TemplateInstanceStatus)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *TemplateList) DeepCopyInto(out *TemplateList) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]Template, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new TemplateList.
func (in *TemplateList) DeepCopy() *TemplateList {
	if in == nil {
		return nil
	}
	out := new(TemplateList)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *TemplateList) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	} else {
		return nil
	}
}
