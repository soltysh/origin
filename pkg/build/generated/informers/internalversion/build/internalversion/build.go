// This file was automatically generated by informer-gen

package internalversion

import (
	build "github.com/openshift/origin/pkg/build/apis/build"
	internalinterfaces "github.com/openshift/origin/pkg/build/generated/informers/internalversion/internalinterfaces"
	internalclientset "github.com/openshift/origin/pkg/build/generated/internalclientset"
	internalversion "github.com/openshift/origin/pkg/build/generated/listers/build/internalversion"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// BuildInformer provides access to a shared informer and lister for
// Builds.
type BuildInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() internalversion.BuildLister
}

type buildInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewBuildInformer constructs a new informer for Build type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewBuildInformer(client internalclientset.Interface, namespace string, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options v1.ListOptions) (runtime.Object, error) {
				return client.Build().Builds(namespace).List(options)
			},
			WatchFunc: func(options v1.ListOptions) (watch.Interface, error) {
				return client.Build().Builds(namespace).Watch(options)
			},
		},
		&build.Build{},
		resyncPeriod,
		indexers,
	)
}

func defaultBuildInformer(client internalclientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewBuildInformer(client, v1.NamespaceAll, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *buildInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&build.Build{}, defaultBuildInformer)
}

func (f *buildInformer) Lister() internalversion.BuildLister {
	return internalversion.NewBuildLister(f.Informer().GetIndexer())
}
