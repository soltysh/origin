package sccadmission

import (
	"fmt"
	"io"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apiserver/pkg/admission"
	"k8s.io/apiserver/pkg/admission/initializer"
	"k8s.io/apiserver/pkg/authorization/authorizer"
	"k8s.io/client-go/kubernetes"
	coreapi "k8s.io/kubernetes/pkg/apis/core"
	coreapiv1conversions "k8s.io/kubernetes/pkg/apis/core/v1"

	securityv1informers "github.com/openshift/client-go/security/informers/externalversions/security/v1"
	oadmission "github.com/openshift/origin/pkg/cmd/server/admission"
)

func RegisterSCCExecRestrictions(plugins *admission.Plugins) {
	plugins.Register("security.openshift.io/SCCExecRestrictions",
		func(config io.Reader) (admission.Interface, error) {
			execAdmitter := NewSCCExecRestrictions()
			return execAdmitter, nil
		})
}

var (
	_ = initializer.WantsAuthorizer(&sccExecRestrictions{})
	_ = initializer.WantsExternalKubeClientSet(&sccExecRestrictions{})
	_ = oadmission.WantsSecurityInformer(&sccExecRestrictions{})
	_ = admission.ValidationInterface(&sccExecRestrictions{})
)

// sccExecRestrictions is an implementation of admission.ValidationInterface which says no to a pod/exec on
// a pod that the user would not be allowed to create
type sccExecRestrictions struct {
	*admission.Handler
	constraintAdmission *constraint
	client              kubernetes.Interface
}

func (d *sccExecRestrictions) Validate(a admission.Attributes, o admission.ObjectInterfaces) (err error) {
	if a.GetOperation() != admission.Connect {
		return nil
	}
	if a.GetResource().GroupResource() != coreapi.Resource("pods") {
		return nil
	}
	if a.GetSubresource() != "attach" && a.GetSubresource() != "exec" {
		return nil
	}

	pod, err := d.client.CoreV1().Pods(a.GetNamespace()).Get(a.GetName(), metav1.GetOptions{})
	if err != nil {
		return admission.NewForbidden(a, err)
	}
	// we have to convert to the internal pod because admission uses internal types for now
	internalPod := &coreapi.Pod{}
	if err := coreapiv1conversions.Convert_v1_Pod_To_core_Pod(pod, internalPod, nil); err != nil {
		return admission.NewForbidden(a, err)
	}

	// TODO, if we want to actually limit who can use which service account, then we'll need to add logic here to make sure that
	// we're allowed to use the SA the pod is using.  Otherwise, user-A creates pod and user-B (who can't use the SA) can exec into it.
	createAttributes := admission.NewAttributesRecord(internalPod, nil, coreapi.Kind("Pod").WithVersion(""), a.GetNamespace(), a.GetName(), a.GetResource(), "", admission.Create, false, a.GetUserInfo())
	// call SCC.Admit instead of SCC.Validate because we accept that a different SCC is chosen. SCC.Validate would require
	// that the chosen SCC (stored in the "openshift.io/scc" annotation) does not change.
	if err := d.constraintAdmission.Admit(createAttributes, o); err != nil {
		return admission.NewForbidden(a, fmt.Errorf("%s operation is not allowed because the pod's security context exceeds your permissions: %v", a.GetSubresource(), err))
	}

	return nil
}

// NewSCCExecRestrictions creates a new admission controller that denies an exec operation on a privileged pod
func NewSCCExecRestrictions() *sccExecRestrictions {
	return &sccExecRestrictions{
		Handler:             admission.NewHandler(admission.Connect),
		constraintAdmission: NewConstraint(),
	}
}

func (d *sccExecRestrictions) SetExternalKubeClientSet(c kubernetes.Interface) {
	d.client = c
	d.constraintAdmission.SetExternalKubeClientSet(c)
}

func (d *sccExecRestrictions) SetSecurityInformers(informers securityv1informers.SecurityContextConstraintsInformer) {
	d.constraintAdmission.SetSecurityInformers(informers)
}

func (d *sccExecRestrictions) SetAuthorizer(authorizer authorizer.Authorizer) {
	d.constraintAdmission.SetAuthorizer(authorizer)
}

// Validate defines actions to validate sccExecRestrictions
func (d *sccExecRestrictions) ValidateInitialization() error {
	return d.constraintAdmission.ValidateInitialization()
}
