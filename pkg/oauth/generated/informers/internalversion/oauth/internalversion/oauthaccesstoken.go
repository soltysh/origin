// This file was automatically generated by informer-gen

package internalversion

import (
	oauth "github.com/openshift/origin/pkg/oauth/apis/oauth"
	internalinterfaces "github.com/openshift/origin/pkg/oauth/generated/informers/internalversion/internalinterfaces"
	internalclientset "github.com/openshift/origin/pkg/oauth/generated/internalclientset"
	internalversion "github.com/openshift/origin/pkg/oauth/generated/listers/oauth/internalversion"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
	time "time"
)

// OAuthAccessTokenInformer provides access to a shared informer and lister for
// OAuthAccessTokens.
type OAuthAccessTokenInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() internalversion.OAuthAccessTokenLister
}

type oAuthAccessTokenInformer struct {
	factory internalinterfaces.SharedInformerFactory
}

// NewOAuthAccessTokenInformer constructs a new informer for OAuthAccessToken type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewOAuthAccessTokenInformer(client internalclientset.Interface, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options v1.ListOptions) (runtime.Object, error) {
				return client.Oauth().OAuthAccessTokens().List(options)
			},
			WatchFunc: func(options v1.ListOptions) (watch.Interface, error) {
				return client.Oauth().OAuthAccessTokens().Watch(options)
			},
		},
		&oauth.OAuthAccessToken{},
		resyncPeriod,
		indexers,
	)
}

func defaultOAuthAccessTokenInformer(client internalclientset.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewOAuthAccessTokenInformer(client, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc})
}

func (f *oAuthAccessTokenInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&oauth.OAuthAccessToken{}, defaultOAuthAccessTokenInformer)
}

func (f *oAuthAccessTokenInformer) Lister() internalversion.OAuthAccessTokenLister {
	return internalversion.NewOAuthAccessTokenLister(f.Informer().GetIndexer())
}
