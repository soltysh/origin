// +build !ignore_autogenerated_openshift

// This file was autogenerated by conversion-gen. Do not edit it manually!

package v1

import (
	user "github.com/openshift/origin/pkg/user/apis/user"
	conversion "k8s.io/apimachinery/pkg/conversion"
	runtime "k8s.io/apimachinery/pkg/runtime"
	unsafe "unsafe"
)

func init() {
	localSchemeBuilder.Register(RegisterConversions)
}

// RegisterConversions adds conversion functions to the given scheme.
// Public to allow building arbitrary schemes.
func RegisterConversions(scheme *runtime.Scheme) error {
	return scheme.AddGeneratedConversionFuncs(
		Convert_v1_Group_To_user_Group,
		Convert_user_Group_To_v1_Group,
		Convert_v1_GroupList_To_user_GroupList,
		Convert_user_GroupList_To_v1_GroupList,
		Convert_v1_Identity_To_user_Identity,
		Convert_user_Identity_To_v1_Identity,
		Convert_v1_IdentityList_To_user_IdentityList,
		Convert_user_IdentityList_To_v1_IdentityList,
		Convert_v1_User_To_user_User,
		Convert_user_User_To_v1_User,
		Convert_v1_UserIdentityMapping_To_user_UserIdentityMapping,
		Convert_user_UserIdentityMapping_To_v1_UserIdentityMapping,
		Convert_v1_UserList_To_user_UserList,
		Convert_user_UserList_To_v1_UserList,
	)
}

func autoConvert_v1_Group_To_user_Group(in *Group, out *user.Group, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.Users = *(*[]string)(unsafe.Pointer(&in.Users))
	return nil
}

// Convert_v1_Group_To_user_Group is an autogenerated conversion function.
func Convert_v1_Group_To_user_Group(in *Group, out *user.Group, s conversion.Scope) error {
	return autoConvert_v1_Group_To_user_Group(in, out, s)
}

func autoConvert_user_Group_To_v1_Group(in *user.Group, out *Group, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.Users = *(*OptionalNames)(unsafe.Pointer(&in.Users))
	return nil
}

// Convert_user_Group_To_v1_Group is an autogenerated conversion function.
func Convert_user_Group_To_v1_Group(in *user.Group, out *Group, s conversion.Scope) error {
	return autoConvert_user_Group_To_v1_Group(in, out, s)
}

func autoConvert_v1_GroupList_To_user_GroupList(in *GroupList, out *user.GroupList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]user.Group)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_GroupList_To_user_GroupList is an autogenerated conversion function.
func Convert_v1_GroupList_To_user_GroupList(in *GroupList, out *user.GroupList, s conversion.Scope) error {
	return autoConvert_v1_GroupList_To_user_GroupList(in, out, s)
}

func autoConvert_user_GroupList_To_v1_GroupList(in *user.GroupList, out *GroupList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]Group)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_user_GroupList_To_v1_GroupList is an autogenerated conversion function.
func Convert_user_GroupList_To_v1_GroupList(in *user.GroupList, out *GroupList, s conversion.Scope) error {
	return autoConvert_user_GroupList_To_v1_GroupList(in, out, s)
}

func autoConvert_v1_Identity_To_user_Identity(in *Identity, out *user.Identity, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.ProviderName = in.ProviderName
	out.ProviderUserName = in.ProviderUserName
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.User, &out.User, 0); err != nil {
		return err
	}
	out.Extra = *(*map[string]string)(unsafe.Pointer(&in.Extra))
	return nil
}

// Convert_v1_Identity_To_user_Identity is an autogenerated conversion function.
func Convert_v1_Identity_To_user_Identity(in *Identity, out *user.Identity, s conversion.Scope) error {
	return autoConvert_v1_Identity_To_user_Identity(in, out, s)
}

func autoConvert_user_Identity_To_v1_Identity(in *user.Identity, out *Identity, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.ProviderName = in.ProviderName
	out.ProviderUserName = in.ProviderUserName
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.User, &out.User, 0); err != nil {
		return err
	}
	out.Extra = *(*map[string]string)(unsafe.Pointer(&in.Extra))
	return nil
}

// Convert_user_Identity_To_v1_Identity is an autogenerated conversion function.
func Convert_user_Identity_To_v1_Identity(in *user.Identity, out *Identity, s conversion.Scope) error {
	return autoConvert_user_Identity_To_v1_Identity(in, out, s)
}

func autoConvert_v1_IdentityList_To_user_IdentityList(in *IdentityList, out *user.IdentityList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]user.Identity)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_IdentityList_To_user_IdentityList is an autogenerated conversion function.
func Convert_v1_IdentityList_To_user_IdentityList(in *IdentityList, out *user.IdentityList, s conversion.Scope) error {
	return autoConvert_v1_IdentityList_To_user_IdentityList(in, out, s)
}

func autoConvert_user_IdentityList_To_v1_IdentityList(in *user.IdentityList, out *IdentityList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]Identity)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_user_IdentityList_To_v1_IdentityList is an autogenerated conversion function.
func Convert_user_IdentityList_To_v1_IdentityList(in *user.IdentityList, out *IdentityList, s conversion.Scope) error {
	return autoConvert_user_IdentityList_To_v1_IdentityList(in, out, s)
}

func autoConvert_v1_User_To_user_User(in *User, out *user.User, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.FullName = in.FullName
	out.Identities = *(*[]string)(unsafe.Pointer(&in.Identities))
	out.Groups = *(*[]string)(unsafe.Pointer(&in.Groups))
	return nil
}

// Convert_v1_User_To_user_User is an autogenerated conversion function.
func Convert_v1_User_To_user_User(in *User, out *user.User, s conversion.Scope) error {
	return autoConvert_v1_User_To_user_User(in, out, s)
}

func autoConvert_user_User_To_v1_User(in *user.User, out *User, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.FullName = in.FullName
	out.Identities = *(*[]string)(unsafe.Pointer(&in.Identities))
	out.Groups = *(*[]string)(unsafe.Pointer(&in.Groups))
	return nil
}

// Convert_user_User_To_v1_User is an autogenerated conversion function.
func Convert_user_User_To_v1_User(in *user.User, out *User, s conversion.Scope) error {
	return autoConvert_user_User_To_v1_User(in, out, s)
}

func autoConvert_v1_UserIdentityMapping_To_user_UserIdentityMapping(in *UserIdentityMapping, out *user.UserIdentityMapping, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.Identity, &out.Identity, 0); err != nil {
		return err
	}
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.User, &out.User, 0); err != nil {
		return err
	}
	return nil
}

// Convert_v1_UserIdentityMapping_To_user_UserIdentityMapping is an autogenerated conversion function.
func Convert_v1_UserIdentityMapping_To_user_UserIdentityMapping(in *UserIdentityMapping, out *user.UserIdentityMapping, s conversion.Scope) error {
	return autoConvert_v1_UserIdentityMapping_To_user_UserIdentityMapping(in, out, s)
}

func autoConvert_user_UserIdentityMapping_To_v1_UserIdentityMapping(in *user.UserIdentityMapping, out *UserIdentityMapping, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.Identity, &out.Identity, 0); err != nil {
		return err
	}
	// TODO: Inefficient conversion - can we improve it?
	if err := s.Convert(&in.User, &out.User, 0); err != nil {
		return err
	}
	return nil
}

// Convert_user_UserIdentityMapping_To_v1_UserIdentityMapping is an autogenerated conversion function.
func Convert_user_UserIdentityMapping_To_v1_UserIdentityMapping(in *user.UserIdentityMapping, out *UserIdentityMapping, s conversion.Scope) error {
	return autoConvert_user_UserIdentityMapping_To_v1_UserIdentityMapping(in, out, s)
}

func autoConvert_v1_UserList_To_user_UserList(in *UserList, out *user.UserList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]user.User)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_UserList_To_user_UserList is an autogenerated conversion function.
func Convert_v1_UserList_To_user_UserList(in *UserList, out *user.UserList, s conversion.Scope) error {
	return autoConvert_v1_UserList_To_user_UserList(in, out, s)
}

func autoConvert_user_UserList_To_v1_UserList(in *user.UserList, out *UserList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]User)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_user_UserList_To_v1_UserList is an autogenerated conversion function.
func Convert_user_UserList_To_v1_UserList(in *user.UserList, out *UserList, s conversion.Scope) error {
	return autoConvert_user_UserList_To_v1_UserList(in, out, s)
}
