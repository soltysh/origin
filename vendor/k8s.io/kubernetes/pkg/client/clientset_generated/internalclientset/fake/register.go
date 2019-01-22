/*
Copyright The Kubernetes Authors.

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

// Code generated by client-gen. DO NOT EDIT.

package fake

import (
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	schema "k8s.io/apimachinery/pkg/runtime/schema"
	serializer "k8s.io/apimachinery/pkg/runtime/serializer"
	utilruntime "k8s.io/apimachinery/pkg/util/runtime"
	admissionregistrationinternalversion "k8s.io/kubernetes/pkg/apis/admissionregistration"
	appsinternalversion "k8s.io/kubernetes/pkg/apis/apps"
	authenticationinternalversion "k8s.io/kubernetes/pkg/apis/authentication"
	authorizationinternalversion "k8s.io/kubernetes/pkg/apis/authorization"
	autoscalinginternalversion "k8s.io/kubernetes/pkg/apis/autoscaling"
	batchinternalversion "k8s.io/kubernetes/pkg/apis/batch"
	certificatesinternalversion "k8s.io/kubernetes/pkg/apis/certificates"
	coordinationinternalversion "k8s.io/kubernetes/pkg/apis/coordination"
	coreinternalversion "k8s.io/kubernetes/pkg/apis/core"
	eventsinternalversion "k8s.io/kubernetes/pkg/apis/events"
	extensionsinternalversion "k8s.io/kubernetes/pkg/apis/extensions"
	networkinginternalversion "k8s.io/kubernetes/pkg/apis/networking"
	policyinternalversion "k8s.io/kubernetes/pkg/apis/policy"
	rbacinternalversion "k8s.io/kubernetes/pkg/apis/rbac"
	schedulinginternalversion "k8s.io/kubernetes/pkg/apis/scheduling"
	settingsinternalversion "k8s.io/kubernetes/pkg/apis/settings"
	storageinternalversion "k8s.io/kubernetes/pkg/apis/storage"
)

var scheme = runtime.NewScheme()
var codecs = serializer.NewCodecFactory(scheme)
var parameterCodec = runtime.NewParameterCodec(scheme)
var localSchemeBuilder = runtime.SchemeBuilder{
	admissionregistrationinternalversion.AddToScheme,
	coreinternalversion.AddToScheme,
	appsinternalversion.AddToScheme,
	authenticationinternalversion.AddToScheme,
	authorizationinternalversion.AddToScheme,
	autoscalinginternalversion.AddToScheme,
	batchinternalversion.AddToScheme,
	certificatesinternalversion.AddToScheme,
	coordinationinternalversion.AddToScheme,
	eventsinternalversion.AddToScheme,
	extensionsinternalversion.AddToScheme,
	networkinginternalversion.AddToScheme,
	policyinternalversion.AddToScheme,
	rbacinternalversion.AddToScheme,
	schedulinginternalversion.AddToScheme,
	settingsinternalversion.AddToScheme,
	storageinternalversion.AddToScheme,
}

// AddToScheme adds all types of this clientset into the given scheme. This allows composition
// of clientsets, like in:
//
//   import (
//     "k8s.io/client-go/kubernetes"
//     clientsetscheme "k8s.io/client-go/kubernetes/scheme"
//     aggregatorclientsetscheme "k8s.io/kube-aggregator/pkg/client/clientset_generated/clientset/scheme"
//   )
//
//   kclientset, _ := kubernetes.NewForConfig(c)
//   _ = aggregatorclientsetscheme.AddToScheme(clientsetscheme.Scheme)
//
// After this, RawExtensions in Kubernetes types will serialize kube-aggregator types
// correctly.
var AddToScheme = localSchemeBuilder.AddToScheme

func init() {
	v1.AddToGroupVersion(scheme, schema.GroupVersion{Version: "v1"})
	utilruntime.Must(AddToScheme(scheme))
}
