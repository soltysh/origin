#!/bin/bash
set -x

TEST_SUITE_START_TIME="1668687872" \
  KUBE_TEST_REPO_LIST="" \
  KUBE_TEST_REPO="quay.io/openshift/community-e2e-images" \
  TEST_PROVIDER="" \
  TEST_JUNIT_DIR="" \
  TEST_UPGRADE_OPTIONS="" \
  ./ginkgo \
  --flake-attempts=3 \
  --timeout="24h" \
  --nodes=30 \
  --progress \
  --no-color \
  --output-interceptor-mode=none \
  --focus='\[sig-apps\] Job should apply changes to a job status \[Conformance\]' \
  ./origin-e2e.test


