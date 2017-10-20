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

// PolicyBindingInformer provides access to a shared informer and lister for
// PolicyBindings.
type PolicyBindingInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() v1.PolicyBindingLister
}

type policyBindingInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewPolicyBindingInformer constructs a new informer for PolicyBinding type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewPolicyBindingInformer(client clientset.Interface, namespace string, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options meta_v1.ListOptions) (runtime.Object, error) {
				return client.AuthorizationV1().PolicyBindings(namespace).List(options)
			},
			WatchFunc: func(options meta_v1.ListOptions) (watch.Interface, error) {
				return client.AuthorizationV1().PolicyBindings(namespace).Watch(options)
			},
		},
		&authorization_v1.PolicyBinding{},
		resyncPeriod,
		indexers,
	)
}

func defaultPolicyBindingInformer(client clientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewPolicyBindingInformer(client, meta_v1.NamespaceAll, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *policyBindingInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&authorization_v1.PolicyBinding{}, defaultPolicyBindingInformer)
}

func (f *policyBindingInformer) Lister() v1.PolicyBindingLister {
	return v1.NewPolicyBindingLister(f.Informer().GetIndexer())
}
