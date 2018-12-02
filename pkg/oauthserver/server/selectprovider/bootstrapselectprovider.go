package selectprovider

import (
	"net/http"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/typed/core/v1"

	"github.com/openshift/origin/pkg/oauthserver/api"
	"github.com/openshift/origin/pkg/oauthserver/authenticator/password/bootstrap"
	"github.com/openshift/origin/pkg/oauthserver/oauth/handlers"
)

func NewBootstrapSelectProvider(delegate handlers.AuthenticationSelectionHandler, secretsGetter v1.SecretsGetter) handlers.AuthenticationSelectionHandler {
	return &bootstrapSelectProvider{
		delegate: delegate,
		secrets:  secretsGetter.Secrets(metav1.NamespaceSystem),
	}
}

type bootstrapSelectProvider struct {
	delegate handlers.AuthenticationSelectionHandler
	secrets  v1.SecretInterface
}

func (b *bootstrapSelectProvider) SelectAuthentication(providers []api.ProviderInfo, w http.ResponseWriter, req *http.Request) (*api.ProviderInfo, bool, error) {
	// this should never happen but let us not panic the server in case we screwed up
	if len(providers) == 0 || providers[0].Name != bootstrap.BootstrapUser {
		return b.delegate.SelectAuthentication(providers, w, req)
	}

	_, _, ok, err := bootstrap.HashAndUID(b.secrets)
	// filter out the bootstrap IDP if the secret is not functional
	if err != nil || !ok {
		return b.delegate.SelectAuthentication(providers[1:], w, req)
	}

	return b.delegate.SelectAuthentication(providers, w, req)
}
