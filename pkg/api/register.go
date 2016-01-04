package api

import (
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/runtime"

	_ "github.com/openshift/origin/pkg/authorization/api"
	_ "github.com/openshift/origin/pkg/build/api"
	_ "github.com/openshift/origin/pkg/deploy/api"
	_ "github.com/openshift/origin/pkg/image/api"
	_ "github.com/openshift/origin/pkg/oauth/api"
	_ "github.com/openshift/origin/pkg/project/api"
	_ "github.com/openshift/origin/pkg/route/api"
	_ "github.com/openshift/origin/pkg/sdn/api"
	_ "github.com/openshift/origin/pkg/template/api"
	_ "github.com/openshift/origin/pkg/user/api"
)

// Scheme is the default instance of runtime.Scheme to which types in the Kubernetes API are already registered.
var Scheme = runtime.NewScheme()

// SchemeGroupVersion is group version used to register these objects
var SchemeGroupVersion = unversioned.GroupVersion{Group: "", Version: ""}

// Kind takes an unqualified kind and returns back a Group qualified GroupKind
func Kind(kind string) unversioned.GroupKind {
	return SchemeGroupVersion.WithKind(kind).GroupKind()
}

// Resource takes an unqualified resource and returns back a Group qualified GroupResource
func Resource(resource string) unversioned.GroupResource {
	return SchemeGroupVersion.WithResource(resource).GroupResource()
}

func init() {
	Scheme.AddKnownTypes(SchemeGroupVersion)
}
