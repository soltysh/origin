// This file was automatically generated by informer-gen

package v1

import (
	template_v1 "github.com/openshift/origin/pkg/template/apis/template/v1"
	clientset "github.com/openshift/origin/pkg/template/generated/clientset"
	internalinterfaces "github.com/openshift/origin/pkg/template/generated/informers/externalversions/internalinterfaces"
	v1 "github.com/openshift/origin/pkg/template/generated/listers/template/v1"
	meta_v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// TemplateInformer provides access to a shared informer and lister for
// Templates.
type TemplateInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() v1.TemplateLister
}

type templateInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewTemplateInformer constructs a new informer for Template type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewTemplateInformer(client clientset.Interface, namespace string, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options meta_v1.ListOptions) (runtime.Object, error) {
				return client.TemplateV1().Templates(namespace).List(options)
			},
			WatchFunc: func(options meta_v1.ListOptions) (watch.Interface, error) {
				return client.TemplateV1().Templates(namespace).Watch(options)
			},
		},
		&template_v1.Template{},
		resyncPeriod,
		indexers,
	)
}

func defaultTemplateInformer(client clientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewTemplateInformer(client, meta_v1.NamespaceAll, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *templateInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&template_v1.Template{}, defaultTemplateInformer)
}

func (f *templateInformer) Lister() v1.TemplateLister {
	return v1.NewTemplateLister(f.Informer().GetIndexer())
}
