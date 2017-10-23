#!/bin/bash
source "$(dirname "${BASH_SOURCE}")/lib/init.sh"

if [[ "${PROTO_OPTIONAL:-}" == "1" ]]; then
  os::log::warning "Skipping protobuf generation as \$PROTO_OPTIONAL is set."
  exit 0
fi

os::util::ensure::system_binary_exists 'protoc'
if [[ "$(protoc --version)" != "libprotoc 3.0."* ]]; then
  os::log::fatal "Generating protobuf requires protoc 3.0.x. Please download and
install the platform appropriate Protobuf package for your OS:

  https://github.com/google/protobuf/releases

To skip protobuf generation, set \$PROTO_OPTIONAL."
fi

os::util::ensure::gopath_binary_exists 'goimports'
os::build::setup_env

os::util::ensure::built_binary_exists 'go-to-protobuf' vendor/k8s.io/code-generator/cmd/go-to-protobuf
os::util::ensure::built_binary_exists 'protoc-gen-gogo' vendor/k8s.io/code-generator/cmd/go-to-protobuf/protoc-gen-gogo

PACKAGES=(
  k8s.io/apiserver/pkg/apis/example/v1
  k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/v1beta1
  k8s.io/kube-aggregator/pkg/apis/apiregistration/v1beta1
  k8s.io/api/core/v1
  k8s.io/api/policy/v1beta1
  k8s.io/api/extensions/v1beta1
  k8s.io/api/autoscaling/v1
  k8s.io/api/authorization/v1
  k8s.io/api/autoscaling/v2beta1
  k8s.io/api/authorization/v1beta1
  k8s.io/api/batch/v1
  k8s.io/api/batch/v1beta1
  k8s.io/api/batch/v2alpha1
  k8s.io/api/apps/v1beta1
  k8s.io/api/apps/v1beta2
  k8s.io/api/authentication/v1
  k8s.io/api/authentication/v1beta1
  k8s.io/api/rbac/v1alpha1
  k8s.io/api/rbac/v1beta1
  k8s.io/api/certificates/v1beta1
  k8s.io/api/imagepolicy/v1alpha1
  k8s.io/api/scheduling/v1alpha1
  k8s.io/api/settings/v1alpha1
  k8s.io/api/storage/v1beta1
  k8s.io/api/storage/v1
  k8s.io/api/admissionregistration/v1alpha1
  k8s.io/api/admission/v1alpha1
  k8s.io/api/networking/v1
  k8s.io/kubernetes/federation/apis/federation/v1beta1
  k8s.io/metrics/pkg/apis/metrics/v1alpha1
  k8s.io/metrics/pkg/apis/metrics/v1beta1
  k8s.io/metrics/pkg/apis/custom_metrics/v1beta1
  k8s.io/apiserver/pkg/apis/audit/v1alpha1
  k8s.io/apiserver/pkg/apis/audit/v1beta1
  github.com/openshift/origin/pkg/authorization/apis/authorization/v1
  github.com/openshift/origin/pkg/build/apis/build/v1
  github.com/openshift/origin/pkg/apps/apis/apps/v1
  github.com/openshift/origin/pkg/image/apis/image/v1
  github.com/openshift/origin/pkg/oauth/apis/oauth/v1
  github.com/openshift/origin/pkg/project/apis/project/v1
  github.com/openshift/origin/pkg/quota/apis/quota/v1
  github.com/openshift/origin/pkg/route/apis/route/v1
  github.com/openshift/origin/pkg/network/apis/network/v1
  github.com/openshift/origin/pkg/security/apis/security/v1
  github.com/openshift/origin/pkg/template/apis/template/v1
  github.com/openshift/origin/pkg/user/apis/user/v1

)

# requires the 'proto' tag to build (will remove when ready)
# searches for the protoc-gen-gogo extension in the output directory
# satisfies import of github.com/gogo/protobuf/gogoproto/gogo.proto and the
# core Google protobuf types
go-to-protobuf \
  --go-header-file="${OS_ROOT}/hack/boilerplate.txt" \
  --proto-import="${OS_ROOT}/vendor" \
  --proto-import="${OS_ROOT}/vendor/k8s.io/kubernetes/third_party/protobuf" \
  --packages=$(IFS=, ; echo "${PACKAGES[*]}") \
  "$@"
