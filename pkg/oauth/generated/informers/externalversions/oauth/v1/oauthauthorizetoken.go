// This file was automatically generated by informer-gen

package v1

import (
	oauth_v1 "github.com/openshift/origin/pkg/oauth/apis/oauth/v1"
	clientset "github.com/openshift/origin/pkg/oauth/generated/clientset"
	internalinterfaces "github.com/openshift/origin/pkg/oauth/generated/informers/externalversions/internalinterfaces"
	v1 "github.com/openshift/origin/pkg/oauth/generated/listers/oauth/v1"
	meta_v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// OAuthAuthorizeTokenInformer provides access to a shared informer and lister for
// OAuthAuthorizeTokens.
type OAuthAuthorizeTokenInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() v1.OAuthAuthorizeTokenLister
}

type oAuthAuthorizeTokenInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewOAuthAuthorizeTokenInformer constructs a new informer for OAuthAuthorizeToken type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewOAuthAuthorizeTokenInformer(client clientset.Interface, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options meta_v1.ListOptions) (runtime.Object, error) {
				return client.OauthV1().OAuthAuthorizeTokens().List(options)
			},
			WatchFunc: func(options meta_v1.ListOptions) (watch.Interface, error) {
				return client.OauthV1().OAuthAuthorizeTokens().Watch(options)
			},
		},
		&oauth_v1.OAuthAuthorizeToken{},
		resyncPeriod,
		indexers,
	)
}

func defaultOAuthAuthorizeTokenInformer(client clientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewOAuthAuthorizeTokenInformer(client, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *oAuthAuthorizeTokenInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&oauth_v1.OAuthAuthorizeToken{}, defaultOAuthAuthorizeTokenInformer)
}

func (f *oAuthAuthorizeTokenInformer) Lister() v1.OAuthAuthorizeTokenLister {
	return v1.NewOAuthAuthorizeTokenLister(f.Informer().GetIndexer())
}
