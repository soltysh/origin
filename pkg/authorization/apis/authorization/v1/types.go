package v1

import (
	"fmt"

	kapi "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kruntime "k8s.io/apimachinery/pkg/runtime"
)

// Authorization is calculated against
// 1. all deny RoleBinding PolicyRules in the master namespace - short circuit on match
// 2. all allow RoleBinding PolicyRules in the master namespace - short circuit on match
// 3. all deny RoleBinding PolicyRules in the namespace - short circuit on match
// 4. all allow RoleBinding PolicyRules in the namespace - short circuit on match
// 5. deny by default

// PolicyRule holds information that describes a policy rule, but does not contain information
// about who the rule applies to or which namespace the rule applies to.
type PolicyRule struct {
	// Verbs is a list of Verbs that apply to ALL the ResourceKinds and AttributeRestrictions contained in this rule.  VerbAll represents all kinds.
	Verbs []string `json:"verbs" protobuf:"bytes,1,rep,name=verbs"`
	// AttributeRestrictions will vary depending on what the Authorizer/AuthorizationAttributeBuilder pair supports.
	// If the Authorizer does not recognize how to handle the AttributeRestrictions, the Authorizer should report an error.
	AttributeRestrictions kruntime.RawExtension `json:"attributeRestrictions,omitempty" protobuf:"bytes,2,opt,name=attributeRestrictions"`
	// APIGroups is the name of the APIGroup that contains the resources.  If this field is empty, then both kubernetes and origin API groups are assumed.
	// That means that if an action is requested against one of the enumerated resources in either the kubernetes or the origin API group, the request
	// will be allowed
	APIGroups []string `json:"apiGroups" protobuf:"bytes,3,rep,name=apiGroups"`
	// Resources is a list of resources this rule applies to.  ResourceAll represents all resources.
	Resources []string `json:"resources" protobuf:"bytes,4,rep,name=resources"`
	// ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.
	ResourceNames []string `json:"resourceNames,omitempty" protobuf:"bytes,5,rep,name=resourceNames"`
	// NonResourceURLsSlice is a set of partial urls that a user should have access to.  *s are allowed, but only as the full, final step in the path
	// This name is intentionally different than the internal type so that the DefaultConvert works nicely and because the ordering may be different.
	NonResourceURLsSlice []string `json:"nonResourceURLs,omitempty" protobuf:"bytes,6,rep,name=nonResourceURLs"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// IsPersonalSubjectAccessReview is a marker for PolicyRule.AttributeRestrictions that denotes that subjectaccessreviews on self should be allowed
type IsPersonalSubjectAccessReview struct {
	metav1.TypeMeta `json:",inline"`
}

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// Role is a logical grouping of PolicyRules that can be referenced as a unit by RoleBindings.
type Role struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Rules holds all the PolicyRules for this Role
	Rules []PolicyRule `json:"rules" protobuf:"bytes,2,rep,name=rules"`
}

// OptionalNames is an array that may also be left nil to distinguish between set and unset.
// +protobuf.nullable=true
// +protobuf.options.(gogoproto.goproto_stringer)=false
type OptionalNames []string

func (t OptionalNames) String() string {
	return fmt.Sprintf("%v", []string(t))
}

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// RoleBinding references a Role, but not contain it.  It can reference any Role in the same namespace or in the global namespace.
// It adds who information via (Users and Groups) OR Subjects and namespace information by which namespace it exists in.
// RoleBindings in a given namespace only have effect in that namespace (excepting the master namespace which has power in all namespaces).
type RoleBinding struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// UserNames holds all the usernames directly bound to the role.
	// This field should only be specified when supporting legacy clients and servers.
	// See Subjects for further details.
	// +k8s:conversion-gen=false
	UserNames OptionalNames `json:"userNames" protobuf:"bytes,2,rep,name=userNames"`
	// GroupNames holds all the groups directly bound to the role.
	// This field should only be specified when supporting legacy clients and servers.
	// See Subjects for further details.
	// +k8s:conversion-gen=false
	GroupNames OptionalNames `json:"groupNames" protobuf:"bytes,3,rep,name=groupNames"`
	// Subjects hold object references to authorize with this rule.
	// This field is ignored if UserNames or GroupNames are specified to support legacy clients and servers.
	// Thus newer clients that do not need to support backwards compatibility should send
	// only fully qualified Subjects and should omit the UserNames and GroupNames fields.
	// Clients that need to support backwards compatibility can use this field to build the UserNames and GroupNames.
	Subjects []kapi.ObjectReference `json:"subjects" protobuf:"bytes,4,rep,name=subjects"`

	// RoleRef can only reference the current namespace and the global namespace.
	// If the RoleRef cannot be resolved, the Authorizer must return an error.
	// Since Policy is a singleton, this is sufficient knowledge to locate a role.
	RoleRef kapi.ObjectReference `json:"roleRef" protobuf:"bytes,5,opt,name=roleRef"`
}

type NamedRoles []NamedRole

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// Policy is a object that holds all the Roles for a particular namespace.  There is at most
// one Policy document per namespace.
type Policy struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// LastModified is the last time that any part of the Policy was created, updated, or deleted
	LastModified metav1.Time `json:"lastModified" protobuf:"bytes,2,opt,name=lastModified"`

	// Roles holds all the Roles held by this Policy, mapped by Role.Name
	Roles NamedRoles `json:"roles" protobuf:"bytes,3,rep,name=roles"`
}

type NamedRoleBindings []NamedRoleBinding

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// PolicyBinding is a object that holds all the RoleBindings for a particular namespace.  There is
// one PolicyBinding document per referenced Policy namespace
type PolicyBinding struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// LastModified is the last time that any part of the PolicyBinding was created, updated, or deleted
	LastModified metav1.Time `json:"lastModified" protobuf:"bytes,2,opt,name=lastModified"`

	// PolicyRef is a reference to the Policy that contains all the Roles that this PolicyBinding's RoleBindings may reference
	PolicyRef kapi.ObjectReference `json:"policyRef" protobuf:"bytes,3,opt,name=policyRef"`
	// RoleBindings holds all the RoleBindings held by this PolicyBinding, mapped by RoleBinding.Name
	RoleBindings NamedRoleBindings `json:"roleBindings" protobuf:"bytes,4,rep,name=roleBindings"`
}

// NamedRole relates a Role with a name
type NamedRole struct {
	// Name is the name of the role
	Name string `json:"name" protobuf:"bytes,1,opt,name=name"`
	// Role is the role being named
	Role Role `json:"role" protobuf:"bytes,2,opt,name=role"`
}

// NamedRoleBinding relates a role binding with a name
type NamedRoleBinding struct {
	// Name is the name of the role binding
	Name string `json:"name" protobuf:"bytes,1,opt,name=name"`
	// RoleBinding is the role binding being named
	RoleBinding RoleBinding `json:"roleBinding" protobuf:"bytes,2,opt,name=roleBinding"`
}

// +genclient
// +genclient:onlyVerbs=create
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// SelfSubjectRulesReview is a resource you can create to determine which actions you can perform in a namespace
type SelfSubjectRulesReview struct {
	metav1.TypeMeta `json:",inline"`

	// Spec adds information about how to conduct the check
	Spec SelfSubjectRulesReviewSpec `json:"spec" protobuf:"bytes,1,opt,name=spec"`

	// Status is completed by the server to tell which permissions you have
	Status SubjectRulesReviewStatus `json:"status,omitempty" protobuf:"bytes,2,opt,name=status"`
}

// SelfSubjectRulesReviewSpec adds information about how to conduct the check
type SelfSubjectRulesReviewSpec struct {
	// Scopes to use for the evaluation.  Empty means "use the unscoped (full) permissions of the user/groups".
	// Nil means "use the scopes on this request".
	// +k8s:conversion-gen=false
	Scopes OptionalScopes `json:"scopes" protobuf:"bytes,1,rep,name=scopes"`
}

// +genclient
// +genclient:onlyVerbs=create
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// SubjectRulesReview is a resource you can create to determine which actions another user can perform in a namespace
type SubjectRulesReview struct {
	metav1.TypeMeta `json:",inline"`

	// Spec adds information about how to conduct the check
	Spec SubjectRulesReviewSpec `json:"spec" protobuf:"bytes,1,opt,name=spec"`

	// Status is completed by the server to tell which permissions you have
	Status SubjectRulesReviewStatus `json:"status,omitempty" protobuf:"bytes,2,opt,name=status"`
}

// SubjectRulesReviewSpec adds information about how to conduct the check
type SubjectRulesReviewSpec struct {
	// User is optional.  At least one of User and Groups must be specified.
	User string `json:"user" protobuf:"bytes,1,opt,name=user"`
	// Groups is optional.  Groups is the list of groups to which the User belongs.  At least one of User and Groups must be specified.
	Groups []string `json:"groups" protobuf:"bytes,2,rep,name=groups"`
	// Scopes to use for the evaluation.  Empty means "use the unscoped (full) permissions of the user/groups".
	Scopes OptionalScopes `json:"scopes" protobuf:"bytes,3,opt,name=scopes"`
}

// SubjectRulesReviewStatus is contains the result of a rules check
type SubjectRulesReviewStatus struct {
	// Rules is the list of rules (no particular sort) that are allowed for the subject
	Rules []PolicyRule `json:"rules" protobuf:"bytes,1,rep,name=rules"`
	// EvaluationError can appear in combination with Rules.  It means some error happened during evaluation
	// that may have prevented additional rules from being populated.
	EvaluationError string `json:"evaluationError,omitempty" protobuf:"bytes,2,opt,name=evaluationError"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ResourceAccessReviewResponse describes who can perform the action
type ResourceAccessReviewResponse struct {
	metav1.TypeMeta `json:",inline"`

	// Namespace is the namespace used for the access review
	Namespace string `json:"namespace,omitempty" protobuf:"bytes,1,opt,name=namespace"`
	// UsersSlice is the list of users who can perform the action
	// +k8s:conversion-gen=false
	UsersSlice []string `json:"users" protobuf:"bytes,2,rep,name=users"`
	// GroupsSlice is the list of groups who can perform the action
	// +k8s:conversion-gen=false
	GroupsSlice []string `json:"groups" protobuf:"bytes,3,rep,name=groups"`

	// EvaluationError is an indication that some error occurred during resolution, but partial results can still be returned.
	// It is entirely possible to get an error and be able to continue determine authorization status in spite of it.  This is
	// most common when a bound role is missing, but enough roles are still present and bound to reason about the request.
	EvaluationError string `json:"evalutionError" protobuf:"bytes,4,opt,name=evalutionError"`
}

// +genclient
// +genclient:nonNamespaced
// +genclient:skipVerbs=get,list,create,update,patch,delete,deleteCollection,watch
// +genclient:method=Create,verb=create,result=ResourceAccessReviewResponse
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ResourceAccessReview is a means to request a list of which users and groups are authorized to perform the
// action specified by spec
type ResourceAccessReview struct {
	metav1.TypeMeta `json:",inline"`

	// Action describes the action being tested.
	Action `json:",inline" protobuf:"bytes,1,opt,name=Action"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// SubjectAccessReviewResponse describes whether or not a user or group can perform an action
type SubjectAccessReviewResponse struct {
	metav1.TypeMeta `json:",inline"`

	// Namespace is the namespace used for the access review
	Namespace string `json:"namespace,omitempty" protobuf:"bytes,1,opt,name=namespace"`
	// Allowed is required.  True if the action would be allowed, false otherwise.
	Allowed bool `json:"allowed" protobuf:"varint,2,opt,name=allowed"`
	// Reason is optional.  It indicates why a request was allowed or denied.
	Reason string `json:"reason,omitempty" protobuf:"bytes,3,opt,name=reason"`
	// EvaluationError is an indication that some error occurred during the authorization check.
	// It is entirely possible to get an error and be able to continue determine authorization status in spite of it.  This is
	// most common when a bound role is missing, but enough roles are still present and bound to reason about the request.
	EvaluationError string `json:"evaluationError,omitempty" protobuf:"bytes,4,opt,name=evaluationError"`
}

// OptionalScopes is an array that may also be left nil to distinguish between set and unset.
// +protobuf.nullable=true
// +protobuf.options.(gogoproto.goproto_stringer)=false
type OptionalScopes []string

func (t OptionalScopes) String() string {
	return fmt.Sprintf("%v", []string(t))
}

// +genclient
// +genclient:nonNamespaced
// +genclient:skipVerbs=get,list,create,update,patch,delete,deleteCollection,watch
// +genclient:method=Create,verb=create,result=SubjectAccessReviewResponse
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// SubjectAccessReview is an object for requesting information about whether a user or group can perform an action
type SubjectAccessReview struct {
	metav1.TypeMeta `json:",inline"`

	// Action describes the action being tested.
	Action `json:",inline" protobuf:"bytes,1,opt,name=Action"`
	// User is optional. If both User and Groups are empty, the current authenticated user is used.
	User string `json:"user" protobuf:"bytes,2,opt,name=user"`
	// GroupsSlice is optional. Groups is the list of groups to which the User belongs.
	// +k8s:conversion-gen=false
	GroupsSlice []string `json:"groups" protobuf:"bytes,3,rep,name=groups"`
	// Scopes to use for the evaluation.  Empty means "use the unscoped (full) permissions of the user/groups".
	// Nil for a self-SAR, means "use the scopes on this request".
	// Nil for a regular SAR, means the same as empty.
	// +k8s:conversion-gen=false
	Scopes OptionalScopes `json:"scopes" protobuf:"bytes,4,rep,name=scopes"`
}

// +genclient
// +genclient:skipVerbs=get,list,create,update,patch,delete,deleteCollection,watch
// +genclient:method=Create,verb=create,result=ResourceAccessReviewResponse
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// LocalResourceAccessReview is a means to request a list of which users and groups are authorized to perform the action specified by spec in a particular namespace
type LocalResourceAccessReview struct {
	metav1.TypeMeta `json:",inline"`

	// Action describes the action being tested.  The Namespace element is FORCED to the current namespace.
	Action `json:",inline" protobuf:"bytes,1,opt,name=Action"`
}

// +genclient
// +genclient:skipVerbs=get,list,create,update,patch,delete,deleteCollection,watch
// +genclient:method=Create,verb=create,result=SubjectAccessReviewResponse
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// LocalSubjectAccessReview is an object for requesting information about whether a user or group can perform an action in a particular namespace
type LocalSubjectAccessReview struct {
	metav1.TypeMeta `json:",inline"`

	// Action describes the action being tested.  The Namespace element is FORCED to the current namespace.
	Action `json:",inline" protobuf:"bytes,1,opt,name=Action"`
	// User is optional.  If both User and Groups are empty, the current authenticated user is used.
	User string `json:"user" protobuf:"bytes,2,opt,name=user"`
	// Groups is optional.  Groups is the list of groups to which the User belongs.
	// +k8s:conversion-gen=false
	GroupsSlice []string `json:"groups" protobuf:"bytes,3,rep,name=groups"`
	// Scopes to use for the evaluation.  Empty means "use the unscoped (full) permissions of the user/groups".
	// Nil for a self-SAR, means "use the scopes on this request".
	// Nil for a regular SAR, means the same as empty.
	// +k8s:conversion-gen=false
	Scopes OptionalScopes `json:"scopes" protobuf:"bytes,4,rep,name=scopes"`
}

// Action describes a request to the API server
type Action struct {
	// Namespace is the namespace of the action being requested.  Currently, there is no distinction between no namespace and all namespaces
	Namespace string `json:"namespace" protobuf:"bytes,1,opt,name=namespace"`
	// Verb is one of: get, list, watch, create, update, delete
	Verb string `json:"verb" protobuf:"bytes,2,opt,name=verb"`
	// Group is the API group of the resource
	// Serialized as resourceAPIGroup to avoid confusion with the 'groups' field when inlined
	Group string `json:"resourceAPIGroup" protobuf:"bytes,3,opt,name=resourceAPIGroup"`
	// Version is the API version of the resource
	// Serialized as resourceAPIVersion to avoid confusion with TypeMeta.apiVersion and ObjectMeta.resourceVersion when inlined
	Version string `json:"resourceAPIVersion" protobuf:"bytes,4,opt,name=resourceAPIVersion"`
	// Resource is one of the existing resource types
	Resource string `json:"resource" protobuf:"bytes,5,opt,name=resource"`
	// ResourceName is the name of the resource being requested for a "get" or deleted for a "delete"
	ResourceName string `json:"resourceName" protobuf:"bytes,6,opt,name=resourceName"`
	// Path is the path of a non resource URL
	Path string `json:"path" protobuf:"bytes,8,opt,name=path"`
	// IsNonResourceURL is true if this is a request for a non-resource URL (outside of the resource hieraarchy)
	IsNonResourceURL bool `json:"isNonResourceURL" protobuf:"varint,9,opt,name=isNonResourceURL"`
	// Content is the actual content of the request for create and update
	Content kruntime.RawExtension `json:"content,omitempty" protobuf:"bytes,7,opt,name=content"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// PolicyList is a collection of Policies
type PolicyList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of Policies
	Items []Policy `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// PolicyBindingList is a collection of PolicyBindings
type PolicyBindingList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of PolicyBindings
	Items []PolicyBinding `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// RoleBindingList is a collection of RoleBindings
type RoleBindingList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of RoleBindings
	Items []RoleBinding `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// RoleList is a collection of Roles
type RoleList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of Roles
	Items []Role `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +genclient
// +genclient:nonNamespaced
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterRole is a logical grouping of PolicyRules that can be referenced as a unit by ClusterRoleBindings.
type ClusterRole struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Rules holds all the PolicyRules for this ClusterRole
	Rules []PolicyRule `json:"rules" protobuf:"bytes,2,rep,name=rules"`
}

// +genclient
// +genclient:nonNamespaced
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterRoleBinding references a ClusterRole, but not contain it.  It can reference any ClusterRole in the same namespace or in the global namespace.
// It adds who information via (Users and Groups) OR Subjects and namespace information by which namespace it exists in.
// ClusterRoleBindings in a given namespace only have effect in that namespace (excepting the master namespace which has power in all namespaces).
type ClusterRoleBinding struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// UserNames holds all the usernames directly bound to the role.
	// This field should only be specified when supporting legacy clients and servers.
	// See Subjects for further details.
	// +k8s:conversion-gen=false
	UserNames OptionalNames `json:"userNames" protobuf:"bytes,2,rep,name=userNames"`
	// GroupNames holds all the groups directly bound to the role.
	// This field should only be specified when supporting legacy clients and servers.
	// See Subjects for further details.
	// +k8s:conversion-gen=false
	GroupNames OptionalNames `json:"groupNames" protobuf:"bytes,3,rep,name=groupNames"`
	// Subjects hold object references to authorize with this rule.
	// This field is ignored if UserNames or GroupNames are specified to support legacy clients and servers.
	// Thus newer clients that do not need to support backwards compatibility should send
	// only fully qualified Subjects and should omit the UserNames and GroupNames fields.
	// Clients that need to support backwards compatibility can use this field to build the UserNames and GroupNames.
	Subjects []kapi.ObjectReference `json:"subjects" protobuf:"bytes,4,rep,name=subjects"`

	// RoleRef can only reference the current namespace and the global namespace.
	// If the ClusterRoleRef cannot be resolved, the Authorizer must return an error.
	// Since Policy is a singleton, this is sufficient knowledge to locate a role.
	RoleRef kapi.ObjectReference `json:"roleRef" protobuf:"bytes,5,opt,name=roleRef"`
}

type NamedClusterRoles []NamedClusterRole

// +genclient
// +genclient:nonNamespaced
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterPolicy is a object that holds all the ClusterRoles for a particular namespace.  There is at most
// one ClusterPolicy document per namespace.
type ClusterPolicy struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// LastModified is the last time that any part of the ClusterPolicy was created, updated, or deleted
	LastModified metav1.Time `json:"lastModified" protobuf:"bytes,2,opt,name=lastModified"`

	// Roles holds all the ClusterRoles held by this ClusterPolicy, mapped by ClusterRole.Name
	Roles NamedClusterRoles `json:"roles" protobuf:"bytes,3,rep,name=roles"`
}

type NamedClusterRoleBindings []NamedClusterRoleBinding

// +genclient
// +genclient:nonNamespaced
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterPolicyBinding is a object that holds all the ClusterRoleBindings for a particular namespace.  There is
// one ClusterPolicyBinding document per referenced ClusterPolicy namespace
type ClusterPolicyBinding struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// LastModified is the last time that any part of the ClusterPolicyBinding was created, updated, or deleted
	LastModified metav1.Time `json:"lastModified" protobuf:"bytes,2,opt,name=lastModified"`

	// PolicyRef is a reference to the ClusterPolicy that contains all the ClusterRoles that this ClusterPolicyBinding's RoleBindings may reference
	PolicyRef kapi.ObjectReference `json:"policyRef" protobuf:"bytes,3,opt,name=policyRef"`
	// RoleBindings holds all the ClusterRoleBindings held by this ClusterPolicyBinding, mapped by ClusterRoleBinding.Name
	RoleBindings NamedClusterRoleBindings `json:"roleBindings" protobuf:"bytes,4,rep,name=roleBindings"`
}

// NamedClusterRole relates a name with a cluster role
type NamedClusterRole struct {
	// Name is the name of the cluster role
	Name string `json:"name" protobuf:"bytes,1,opt,name=name"`
	// Role is the cluster role being named
	Role ClusterRole `json:"role" protobuf:"bytes,2,opt,name=role"`
}

// NamedClusterRoleBinding relates a name with a cluster role binding
type NamedClusterRoleBinding struct {
	// Name is the name of the cluster role binding
	Name string `json:"name" protobuf:"bytes,1,opt,name=name"`
	// RoleBinding is the cluster role binding being named
	RoleBinding ClusterRoleBinding `json:"roleBinding" protobuf:"bytes,2,opt,name=roleBinding"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterPolicyList is a collection of ClusterPolicies
type ClusterPolicyList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of ClusterPolicies
	Items []ClusterPolicy `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterPolicyBindingList is a collection of ClusterPolicyBindings
type ClusterPolicyBindingList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of ClusterPolicyBindings
	Items []ClusterPolicyBinding `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterRoleBindingList is a collection of ClusterRoleBindings
type ClusterRoleBindingList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of ClusterRoleBindings
	Items []ClusterRoleBinding `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// ClusterRoleList is a collection of ClusterRoles
type ClusterRoleList struct {
	metav1.TypeMeta `json:",inline"`
	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of ClusterRoles
	Items []ClusterRole `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// RoleBindingRestriction is an object that can be matched against a subject
// (user, group, or service account) to determine whether rolebindings on that
// subject are allowed in the namespace to which the RoleBindingRestriction
// belongs.  If any one of those RoleBindingRestriction objects matches
// a subject, rolebindings on that subject in the namespace are allowed.
type RoleBindingRestriction struct {
	metav1.TypeMeta `json:",inline"`

	// Standard object's metadata.
	metav1.ObjectMeta `json:"metadata" protobuf:"bytes,1,opt,name=metadata"`

	// Spec defines the matcher.
	Spec RoleBindingRestrictionSpec `json:"spec" protobuf:"bytes,2,opt,name=spec"`
}

// RoleBindingRestrictionSpec defines a rolebinding restriction.  Exactly one
// field must be non-nil.
type RoleBindingRestrictionSpec struct {
	// UserRestriction matches against user subjects.
	UserRestriction *UserRestriction `json:"userrestriction" protobuf:"bytes,1,opt,name=userrestriction"`

	// GroupRestriction matches against group subjects.
	GroupRestriction *GroupRestriction `json:"grouprestriction" protobuf:"bytes,2,opt,name=grouprestriction"`

	// ServiceAccountRestriction matches against service-account subjects.
	ServiceAccountRestriction *ServiceAccountRestriction `json:"serviceaccountrestriction" protobuf:"bytes,3,opt,name=serviceaccountrestriction"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// RoleBindingRestrictionList is a collection of RoleBindingRestriction objects.
type RoleBindingRestrictionList struct {
	metav1.TypeMeta `json:",inline"`

	// Standard object's metadata.
	metav1.ListMeta `json:"metadata,omitempty" protobuf:"bytes,1,opt,name=metadata"`

	// Items is a list of RoleBindingRestriction objects.
	Items []RoleBindingRestriction `json:"items" protobuf:"bytes,2,rep,name=items"`
}

// UserRestriction matches a user either by a string match on the user name,
// a string match on the name of a group to which the user belongs, or a label
// selector applied to the user labels.
type UserRestriction struct {
	// Users specifies a list of literal user names.
	Users []string `json:"users" protobuf:"bytes,1,rep,name=users"`

	// Groups specifies a list of literal group names.
	Groups []string `json:"groups" protobuf:"bytes,2,rep,name=groups"`

	// Selectors specifies a list of label selectors over user labels.
	Selectors []metav1.LabelSelector `json:"labels" protobuf:"bytes,3,rep,name=labels"`
}

// GroupRestriction matches a group either by a string match on the group name
// or a label selector applied to group labels.
type GroupRestriction struct {
	// Groups is a list of groups used to match against an individual user's
	// groups. If the user is a member of one of the whitelisted groups, the user
	// is allowed to be bound to a role.
	Groups []string `json:"groups" protobuf:"bytes,1,rep,name=groups"`

	// Selectors specifies a list of label selectors over group labels.
	Selectors []metav1.LabelSelector `json:"labels" protobuf:"bytes,2,rep,name=labels"`
}

// ServiceAccountRestriction matches a service account by a string match on
// either the service-account name or the name of the service account's
// namespace.
type ServiceAccountRestriction struct {
	// ServiceAccounts specifies a list of literal service-account names.
	ServiceAccounts []ServiceAccountReference `json:"serviceaccounts" protobuf:"bytes,1,rep,name=serviceaccounts"`

	// Namespaces specifies a list of literal namespace names.
	Namespaces []string `json:"namespaces" protobuf:"bytes,2,rep,name=namespaces"`
}

// ServiceAccountReference specifies a service account and namespace by their
// names.
type ServiceAccountReference struct {
	// Name is the name of the service account.
	Name string `json:"name" protobuf:"bytes,1,opt,name=name"`

	// Namespace is the namespace of the service account.  Service accounts from
	// inside the whitelisted namespaces are allowed to be bound to roles.  If
	// Namespace is empty, then the namespace of the RoleBindingRestriction in
	// which the ServiceAccountReference is embedded is used.
	Namespace string `json:"namespace" protobuf:"bytes,2,opt,name=namespace"`
}
