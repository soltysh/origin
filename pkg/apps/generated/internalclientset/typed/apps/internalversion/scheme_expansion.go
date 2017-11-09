package internalversion

import (
	kapi "k8s.io/kubernetes/pkg/api/install"

	appsv1 "github.com/openshift/origin/pkg/apps/apis/apps/v1"
	apps "github.com/openshift/origin/pkg/apps/generated/internalclientset/scheme"
)

func init() {
	// This is needed in order to be able to convert the PodSpec which is part of
	// DeploymentConfig template.
	kapi.Install(apps.GroupFactoryRegistry, apps.Registry, apps.Scheme)

	// FIXME: This is needed so the client scheme has all generated conversions
	// available. Without this the deployment config controller will fail
	// conversion of deployment config status reason.
	appsv1.RegisterConversions(apps.Scheme)
}
