/*
Copyright 2014 Google Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package admission

import (
	"fmt"
	"io"
	"math/rand"
	"strings"
	"time"

	"github.com/golang/glog"

	"k8s.io/kubernetes/pkg/admission"
	kapi "k8s.io/kubernetes/pkg/api"
	apierrors "k8s.io/kubernetes/pkg/api/errors"
	"k8s.io/kubernetes/pkg/api/meta"
	client "k8s.io/kubernetes/pkg/client/unversioned"
	"k8s.io/kubernetes/pkg/util/sets"

	"github.com/openshift/origin/pkg/api/latest"
	"github.com/openshift/origin/pkg/project/cache"
	projectutil "github.com/openshift/origin/pkg/project/util"
)

// TODO: modify the upstream plug-in so this can be collapsed
// need ability to specify a RESTMapper on upstream version
func init() {
	admission.RegisterPlugin("OriginNamespaceLifecycle", func(client client.Interface, config io.Reader) (admission.Interface, error) {
		return NewLifecycle(client, recommendedCreatableResources)
	})
}

type lifecycle struct {
	client client.Interface

	// creatableResources is a set of resources that can be created even if the namespace is terminating
	creatableResources sets.String
}

var recommendedCreatableResources = sets.NewString("resourceaccessreviews", "localresourceaccessreviews")

// Admit enforces that a namespace must exist in order to associate content with it.
// Admit enforces that a namespace that is terminating cannot accept new content being associated with it.
func (e *lifecycle) Admit(a admission.Attributes) (err error) {
	if len(a.GetNamespace()) == 0 {
		return nil
	}
	// always allow a SAR request through, the SAR will return information about
	// the ability to take action on the object, no need to verify it here.
	if isSubjectAccessReview(a) {
		return nil
	}
	gvk, err := latest.RESTMapper.KindFor(a.GetResource().Resource)
	if err != nil {
		glog.V(4).Infof("Ignoring life-cycle enforcement for resource %v; no associated default version and kind could be found.", a.GetResource())
		return nil
	}
	mapping, err := latest.RESTMapper.RESTMapping(gvk.GroupKind(), gvk.Version)
	if err != nil {
		return admission.NewForbidden(a, err)
	}
	if mapping.Scope.Name() != meta.RESTScopeNameNamespace {
		return nil
	}

	// we want to allow someone to delete something in case it was phantom created somehow
	if a.GetOperation() == "DELETE" {
		return nil
	}

	name := "Unknown"
	obj := a.GetObject()
	if obj != nil {
		name, _ = meta.NewAccessor().Name(obj)
	}

	projects, err := cache.GetProjectCache()
	if err != nil {
		return admission.NewForbidden(a, err)
	}

	namespace, err := projects.GetNamespaceObject(a.GetNamespace())
	if err != nil {
		return admission.NewForbidden(a, err)
	}

	if a.GetOperation() != "CREATE" {
		return nil
	}

	if namespace.Status.Phase == kapi.NamespaceTerminating && !e.creatableResources.Has(strings.ToLower(a.GetResource().Resource)) {
		return apierrors.NewForbidden(gvk.Kind, name, fmt.Errorf("Namespace %s is terminating", a.GetNamespace()))
	}

	// in case of concurrency issues, we will retry this logic
	numRetries := 10
	interval := time.Duration(rand.Int63n(90)+int64(10)) * time.Millisecond
	for retry := 1; retry <= numRetries; retry++ {

		// associate this namespace with openshift
		_, err = projectutil.Associate(e.client, namespace)
		if err == nil {
			break
		}

		// we have exhausted all reasonable efforts to retry so give up now
		if retry == numRetries {
			return admission.NewForbidden(a, err)
		}

		// get the latest namespace for the next pass in case of resource version updates
		time.Sleep(interval)

		// it's possible the namespace actually was deleted, so just forbid if this occurs
		namespace, err = e.client.Namespaces().Get(a.GetNamespace())
		if err != nil {
			return admission.NewForbidden(a, err)
		}
	}
	return nil
}

func (e *lifecycle) Handles(operation admission.Operation) bool {
	return true
}

func NewLifecycle(client client.Interface, creatableResources sets.String) (admission.Interface, error) {
	return &lifecycle{client: client, creatableResources: creatableResources}, nil
}

func isSubjectAccessReview(a admission.Attributes) bool {
	return a.GetResource().Resource == "subjectaccessreviews" ||
		a.GetResource().Resource == "localsubjectaccessreviews"
}
