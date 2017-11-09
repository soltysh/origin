package internalversion

import (
	kapi "k8s.io/kubernetes/pkg/api/install"

	authorizationv1 "github.com/openshift/origin/pkg/authorization/apis/authorization/v1"
	authorization "github.com/openshift/origin/pkg/authorization/generated/internalclientset/scheme"
)

func init() {
	// This is needed in order to be able to convert the PodSpec which is part of
	// DeploymentConfig template.
	kapi.Install(authorization.GroupFactoryRegistry, authorization.Registry, authorization.Scheme)

	// FIXME: This is needed so the client scheme has all generated conversions
	// available. Without this the deployment config controller will fail
	// conversion of deployment config status reason.
	authorizationv1.RegisterConversions(authorization.Scheme)
}
