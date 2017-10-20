// This file was automatically generated by informer-gen

package v1

import (
	authorization_v1 "github.com/openshift/origin/pkg/authorization/apis/authorization/v1"
	clientset "github.com/openshift/origin/pkg/authorization/generated/clientset"
	internalinterfaces "github.com/openshift/origin/pkg/authorization/generated/informers/externalversions/internalinterfaces"
	v1 "github.com/openshift/origin/pkg/authorization/generated/listers/authorization/v1"
	meta_v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// ClusterPolicyInformer provides access to a shared informer and lister for
// ClusterPolicies.
type ClusterPolicyInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() v1.ClusterPolicyLister
}

type clusterPolicyInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewClusterPolicyInformer constructs a new informer for ClusterPolicy type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewClusterPolicyInformer(client clientset.Interface, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options meta_v1.ListOptions) (runtime.Object, error) {
				return client.AuthorizationV1().ClusterPolicies().List(options)
			},
			WatchFunc: func(options meta_v1.ListOptions) (watch.Interface, error) {
				return client.AuthorizationV1().ClusterPolicies().Watch(options)
			},
		},
		&authorization_v1.ClusterPolicy{},
		resyncPeriod,
		indexers,
	)
}

func defaultClusterPolicyInformer(client clientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewClusterPolicyInformer(client, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *clusterPolicyInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&authorization_v1.ClusterPolicy{}, defaultClusterPolicyInformer)
}

func (f *clusterPolicyInformer) Lister() v1.ClusterPolicyLister {
	return v1.NewClusterPolicyLister(f.Informer().GetIndexer())
}
