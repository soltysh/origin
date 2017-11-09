package internalversion

import (
	kapi "k8s.io/kubernetes/pkg/api/install"

	userv1 "github.com/openshift/origin/pkg/user/apis/user/v1"
	user "github.com/openshift/origin/pkg/user/generated/internalclientset/scheme"
)

func init() {
	kapi.Install(user.GroupFactoryRegistry, user.Registry, user.Scheme)

	userv1.RegisterConversions(user.Scheme)
}
