package v1beta3

import (
	"k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/registered"
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/runtime"
)

// SchemeGroupVersion is group version used to register these objects
var SchemeGroupVersion = unversioned.GroupVersion{Group: "", Version: "v1beta3"}

// Codec encodes internal objects to the v1beta3 scheme
var Codec = runtime.CodecFor(api.Scheme, SchemeGroupVersion.String())

func init() {
	// Check if v1beta3 is in the list of supported API versions.
	if !registered.IsRegisteredAPIGroupVersion(SchemeGroupVersion) {
		return
	}

	// Register the API.
	addKnownTypes()
}

// Adds the list of known types to api.Scheme.
func addKnownTypes() {
	api.Scheme.AddKnownTypes(SchemeGroupVersion,
		&Project{},
		&ProjectList{},
		&ProjectRequest{},
	)
}

func (*ProjectRequest) IsAnAPIObject() {}
func (*Project) IsAnAPIObject()        {}
func (*ProjectList) IsAnAPIObject()    {}
