package latest

import (
	"fmt"
	"strings"

	"k8s.io/kubernetes/pkg/api"
	kmeta "k8s.io/kubernetes/pkg/api/meta"
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/runtime"
	"k8s.io/kubernetes/pkg/util/sets"

	"github.com/golang/glog"

	_ "github.com/openshift/origin/pkg/api"
	"github.com/openshift/origin/pkg/api/v1"
	"github.com/openshift/origin/pkg/api/v1beta3"
)

// Version is the string that represents the current external default version.
var Version = unversioned.GroupVersion{"", "v1"}

// OldestVersion is the string that represents the oldest server version supported,
// for client code that wants to hardcode the lowest common denominator.
var OldestVersion = unversioned.GroupVersion{"", "v1beta3"}

// Versions is the list of versions that are recognized in code. The order provided
// may be assumed to be least feature rich to most feature rich, and clients may
// choose to prefer the latter items in the list over the former items when presented
// with a set of versions to choose.
var Versions = []unversioned.GroupVersion{Version, OldestVersion}

// TODO: this should be removed, it's here to make the storage related stuff work
// as before.
var VersionsStrings = []string{"v1", "v1beta3"}

// Codec is the default codec for serializing output that should use
// the latest supported version.  Use this Codec when writing to
// disk, a data store that is not dynamically versioned, or in tests.
// This codec can decode any object that OpenShift is aware of.
var Codec = v1.Codec

// accessor is the shared static metadata accessor for the API.
var accessor = kmeta.NewAccessor()

// ResourceVersioner describes a default versioner that can handle all types
// of versioning.
// TODO: when versioning changes, make this part of each API definition.
var ResourceVersioner runtime.ResourceVersioner = accessor

// SelfLinker can set or get the SelfLink field of all API types.
// TODO: when versioning changes, make this part of each API definition.
// TODO(lavalamp): Combine SelfLinker & ResourceVersioner interfaces, force all uses
// to go through the InterfacesFor method below.
var SelfLinker runtime.SelfLinker = accessor

// RESTMapper provides the default mapping between REST paths and the objects declared in api.Scheme and all known
// Kubernetes versions.
var RESTMapper kmeta.RESTMapper

// InterfacesFor returns the default Codec and ResourceVersioner for a given version
// string, or an error if the version is not known.
func InterfacesFor(version unversioned.GroupVersion) (*kmeta.VersionInterfaces, error) {
	switch version {
	case v1beta3.SchemeGroupVersion:
		return &kmeta.VersionInterfaces{
			Codec:            v1beta3.Codec,
			ObjectConvertor:  api.Scheme,
			MetadataAccessor: accessor,
		}, nil
	case v1.SchemeGroupVersion:
		return &kmeta.VersionInterfaces{
			Codec:            v1.Codec,
			ObjectConvertor:  api.Scheme,
			MetadataAccessor: accessor,
		}, nil
	default:
		return nil, fmt.Errorf("unsupported storage version: %q (valid: %v)", version, Versions)
	}
}

// originTypes are the hardcoded types defined by the OpenShift API.
var originTypes = sets.String{}

// UserResources are the resource names that apply to the primary, user facing resources used by
// client tools. They are in deletion-first order - dependent resources should be last.
var UserResources = []string{
	"buildConfigs", "builds",
	"imageStreams",
	"deploymentConfigs", "replicationControllers",
	"routes", "services",
	"pods",
}

// OriginKind returns true if OpenShift owns the kind described in a given apiVersion.
func OriginKind(gvk unversioned.GroupVersionKind) bool {
	return originTypes.Has(gvk.Kind)
}

func init() {
	// this keeps us consistent with old code.  We can decide if we want to expand our RESTMapper to cover
	// api.RESTMapper, which is different than what you'd get from latest.
	kubeMapper := api.RESTMapper

	// list of versions we support on the server, in preferred order
	versions := []unversioned.GroupVersion{Version, OldestVersion}

	originMapper := kmeta.NewDefaultRESTMapper(
		versions,
		func(version unversioned.GroupVersion) (*kmeta.VersionInterfaces, error) {
			interfaces, err := InterfacesFor(version)
			if err != nil {
				return nil, err
			}
			return interfaces, nil
		},
	)

	// the list of kinds that are scoped at the root of the api hierarchy
	// if a kind is not enumerated here, it is assumed to have a namespace scope
	kindToRootScope := map[string]bool{
		"Status": true,

		"Project":        true,
		"ProjectRequest": true,

		"Image": true,

		"User":                true,
		"Identity":            true,
		"UserIdentityMapping": true,
		"Group":               true,

		"OAuthAccessToken":         true,
		"OAuthAuthorizeToken":      true,
		"OAuthClient":              true,
		"OAuthClientAuthorization": true,

		"ClusterRole":          true,
		"ClusterRoleBinding":   true,
		"ClusterPolicy":        true,
		"ClusterPolicyBinding": true,

		"ClusterNetwork": true,
		"HostSubnet":     true,
		"NetNamespace":   true,
	}

	// enumerate all supported versions, get the kinds, and register with the mapper how to address our resources
	for _, version := range versions {
		for kind, t := range api.Scheme.KnownTypes(version) {
			if !strings.Contains(t.PkgPath(), "openshift/origin") {
				if _, ok := kindToRootScope[kind]; !ok {
					continue
				}
			}
			originTypes.Insert(kind)
			scope := kmeta.RESTScopeNamespace
			_, found := kindToRootScope[kind]
			if found || (strings.HasSuffix(kind, "List") && kindToRootScope[strings.TrimSuffix(kind, "List")]) {
				scope = kmeta.RESTScopeRoot
			}
			gvk := version.WithKind(kind)
			glog.V(6).Infof("Registering %s %s", gvk.String(), scope.Name())
			originMapper.Add(gvk, scope, false)
		}
	}

	// For Origin we use MultiRESTMapper that handles both Origin and Kubernetes
	// objects
	RESTMapper = kmeta.MultiRESTMapper{originMapper, kubeMapper}
}
