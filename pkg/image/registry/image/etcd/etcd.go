package etcd

import (
	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/errors"
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/fields"
	"k8s.io/kubernetes/pkg/labels"
	"k8s.io/kubernetes/pkg/registry/generic"
	etcdgeneric "k8s.io/kubernetes/pkg/registry/generic/etcd"
	"k8s.io/kubernetes/pkg/runtime"
	"k8s.io/kubernetes/pkg/storage"
	"k8s.io/kubernetes/pkg/watch"

	"github.com/openshift/origin/pkg/image/api"
	"github.com/openshift/origin/pkg/image/registry/image"
)

// REST implements a RESTStorage for images against etcd.
type REST struct {
	*etcdgeneric.Etcd
}

// NewREST returns a new REST.
func NewREST(s storage.Interface) *REST {
	prefix := "/images"

	store := &etcdgeneric.Etcd{
		NewFunc: func() runtime.Object { return &api.Image{} },

		// NewListFunc returns an object capable of storing results of an etcd list.
		NewListFunc: func() runtime.Object { return &api.ImageList{} },
		// Produces a path that etcd understands, to the root of the resource
		// by combining the namespace in the context with the given prefix.
		// Yet images are not namespace scoped, so we're returning just prefix here.
		KeyRootFunc: func(ctx kapi.Context) string {
			return prefix
		},
		// Produces a path that etcd understands, to the resource by combining
		// the namespace in the context with the given prefix
		// Yet images are not namespace scoped, so we're returning just prefix here.
		KeyFunc: func(ctx kapi.Context, name string) (string, error) {
			return etcdgeneric.NoNamespaceKeyFunc(ctx, prefix, name)
		},
		// Retrieve the name field of an image
		ObjectNameFunc: func(obj runtime.Object) (string, error) {
			return obj.(*api.Image).Name, nil
		},
		// Used to match objects based on labels/fields for list and watch
		PredicateFunc: func(label labels.Selector, field fields.Selector) generic.Matcher {
			return image.MatchImage(label, field)
		},
		EndpointName: "image",

		// Used to validate image creation
		CreateStrategy: image.Strategy,

		// Used to validate image updates
		UpdateStrategy: image.Strategy,

		ReturnDeletedObject: false,

		Storage: s,
	}
	return &REST{store}
}

// Watch begins watching for new, changed, or deleted images.
func (r *REST) Watch(ctx kapi.Context, options *unversioned.ListOptions) (watch.Interface, error) {
	if options != nil && options.FieldSelector.Selector != nil {
		return nil, errors.NewBadRequest("field selectors are not supported on images")
	}
	label := labels.Everything()
	if options != nil && options.LabelSelector.Selector != nil {
		label = options.LabelSelector.Selector
	}
	field := fields.Everything()
	resourceVersion := ""
	if options != nil {
		resourceVersion = options.ResourceVersion
	}
	return r.WatchPredicate(ctx, image.MatchImage(label, field), resourceVersion)
}
