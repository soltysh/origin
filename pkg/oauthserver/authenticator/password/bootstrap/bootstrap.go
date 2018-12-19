package bootstrap

import (
	"crypto/sha512"
	"encoding/base64"
	"fmt"
	"time"

	"github.com/golang/glog"
	"golang.org/x/crypto/bcrypt"

	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/sets"
	"k8s.io/apiserver/pkg/authentication/authenticator"
	"k8s.io/apiserver/pkg/authentication/user"
	"k8s.io/client-go/kubernetes/typed/core/v1"
)

const (
	// BootstrapUser is the magic bootstrap OAuth user that can perform any action
	BootstrapUser = "kube:admin"
	// support basic auth which does not allow : in username
	bootstrapUserBasicAuth = "kubeadmin"
	// force the use of a secure password length
	// expected format is 5char-5char-5char-5char
	minPasswordLen = 23
)

var (
	// make it obvious that we refuse to honor short passwords
	errPasswordTooShort = fmt.Errorf("%s password must be at least %d characters long", bootstrapUserBasicAuth, minPasswordLen)

	// we refuse to honor a secret that is too new when compared to kube-system
	// since kube-system always exists and cannot be deleted
	// and creation timestamp is controlled by the api, we can use this to
	// detect if the secret was recreated after the initial bootstrapping
	errSecretRecreated = fmt.Errorf("%s secret cannot be recreated", bootstrapUserBasicAuth)
)

func New(secrets v1.SecretsGetter, namespaces v1.NamespacesGetter) authenticator.Password {
	return &bootstrapPassword{
		secrets:    secrets.Secrets(metav1.NamespaceSystem),
		namespaces: namespaces.Namespaces(),
		names:      sets.NewString(BootstrapUser, bootstrapUserBasicAuth),
	}
}

type bootstrapPassword struct {
	secrets    v1.SecretInterface
	namespaces v1.NamespaceInterface
	names      sets.String
}

func (b *bootstrapPassword) AuthenticatePassword(username, password string) (user.Info, bool, error) {
	if !b.names.Has(username) {
		return nil, false, nil
	}

	hashedPassword, uid, ok, err := HashAndUID(b.secrets, b.namespaces)
	if err != nil || !ok {
		return nil, ok, err
	}

	// check length after we know that the secret is functional since
	// we do not want to complain when the bootstrap user is disabled
	if len(password) < minPasswordLen {
		return nil, false, errPasswordTooShort
	}

	if err := bcrypt.CompareHashAndPassword(hashedPassword, []byte(password)); err != nil {
		if err == bcrypt.ErrMismatchedHashAndPassword {
			glog.V(4).Infof("%s password mismatch", bootstrapUserBasicAuth)
			return nil, false, nil
		}
		return nil, false, err
	}

	// do not set other fields, see identitymapper.userToInfo func
	return &user.DefaultInfo{
		Name: BootstrapUser,
		UID:  uid, // uid ties this authentication to the current state of the secret
	}, true, nil
}

func HashAndUID(secrets v1.SecretInterface, namespaces v1.NamespaceInterface) ([]byte, string, bool, error) {
	secret, err := secrets.Get(bootstrapUserBasicAuth, metav1.GetOptions{})
	if errors.IsNotFound(err) {
		glog.V(4).Infof("%s secret does not exist", bootstrapUserBasicAuth)
		return nil, "", false, nil
	}
	if err != nil {
		return nil, "", false, err
	}
	if secret.DeletionTimestamp != nil {
		glog.V(4).Infof("%s secret is being deleted", bootstrapUserBasicAuth)
		return nil, "", false, nil
	}
	namespace, err := namespaces.Get(metav1.NamespaceSystem, metav1.GetOptions{})
	if err != nil {
		return nil, "", false, err
	}
	if secret.CreationTimestamp.After(namespace.CreationTimestamp.Add(time.Hour)) {
		return nil, "", false, errSecretRecreated
	}

	hashedPassword := secret.Data[bootstrapUserBasicAuth]

	// make sure the value is a valid bcrypt hash
	if _, err := bcrypt.Cost(hashedPassword); err != nil {
		return nil, "", false, err
	}

	exactSecret := string(secret.UID) + secret.ResourceVersion
	both := append([]byte(exactSecret), hashedPassword...)

	// use a hash to avoid leaking any derivative of the password
	// this makes it easy for us to tell if the secret changed
	uidBytes := sha512.Sum512(both)

	return hashedPassword, base64.RawURLEncoding.EncodeToString(uidBytes[:]), true, nil
}
