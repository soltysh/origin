// This file was automatically generated by informer-gen

package internalversion

import (
	user "github.com/openshift/origin/pkg/user/apis/user"
	internalinterfaces "github.com/openshift/origin/pkg/user/generated/informers/internalversion/internalinterfaces"
	internalclientset "github.com/openshift/origin/pkg/user/generated/internalclientset"
	internalversion "github.com/openshift/origin/pkg/user/generated/listers/user/internalversion"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// IdentityInformer provides access to a shared informer and lister for
// Identities.
type IdentityInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() internalversion.IdentityLister
}

type identityInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewIdentityInformer constructs a new informer for Identity type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewIdentityInformer(client internalclientset.Interface, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options v1.ListOptions) (runtime.Object, error) {
				return client.User().Identities().List(options)
			},
			WatchFunc: func(options v1.ListOptions) (watch.Interface, error) {
				return client.User().Identities().Watch(options)
			},
		},
		&user.Identity{},
		resyncPeriod,
		indexers,
	)
}

func defaultIdentityInformer(client internalclientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewIdentityInformer(client, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *identityInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&user.Identity{}, defaultIdentityInformer)
}

func (f *identityInformer) Lister() internalversion.IdentityLister {
	return internalversion.NewIdentityLister(f.Informer().GetIndexer())
}
