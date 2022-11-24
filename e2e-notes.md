# Tasks

1. Build `origin-e2e.test` binary.
2. Run tests using `ginkgo` rather than `openshift-test run-test`.
3. Extract k8s-e2e.test binary from #1 and re-use the one from o/k.


Compiling the binary:

```
go build -trimpath -ldflags "-X github.com/openshift/origin/pkg/version.versionFromGit="v1.4.12-410-gb0d753c" -X github.com/openshift/origin/pkg/version.commitFromGit="b0d753ca48" -X github.com/openshift/origin/pkg/version.gitTreeState="dirty" -X github.com/openshift/origin/pkg/version.buildDate="2022-11-24T14:54:23Z" " github.com/onsi/ginkgo/v2/ginkgo
```

```
go test -c -trimpath -ldflags "-X github.com/openshift/origin/pkg/version.versionFromGit="v1.4.12-394-g403f0a4" -X github.com/openshift/origin/pkg/version.commitFromGit="403f0a4fe2" -X github.com/openshift/origin/pkg/version.gitTreeState="clean" -X github.com/openshift/origin/pkg/version.buildDate="2022-11-17T15:13:17Z" " -o $(pwd)/origin-e2e.test github.com/openshift/origin/cmd/e2e
```

NOTE: all the flags are just like for normal builds, the gist is basically:
```
go test -c _all the usual flags_ -o _output file_ package
```


```
TEST_SUITE_START_TIME="1668687872" \
  KUBE_TEST_REPO_LIST="" \
  KUBE_TEST_REPO="quay.io/openshift/community-e2e-images" \
  TEST_PROVIDER="" \
  TEST_JUNIT_DIR="" \
  TEST_UPGRADE_OPTIONS="" \
  ./ginkgo \
  --flake-attempts=3 \
  --timeout="24h" \
  -nodes 30 -no-color -focus '[sig-apps] Job should delete a job [Conformance] [Suite:openshift/conformance/parallel/minimal] [Suite:k8s]' \
  ./k8s-e2e.test  -- \
  -report-dir "${test_report_dir}" \
  -host https://api.maszulik.group-b.devcluster.openshift.com:6443 \
  -allowed-not-ready-nodes 3 \
  2>&1 | tee -a "${test_report_dir}/k8s-e2e.log"
```

How tests are invoked, ie. what are the actions when you call `/openshift-tests run openshift/conformance/parallel --dry-run`?
1. Pick a suite (in PreSuite function initialize provider details from cmd/openshift-tests/e2e.go#suiteWithProviderPreSuite).
2. All tests are walked in pkg/test/ginkgo/ginkgo.go#testsForSuite with ginkgo to create the final list.
   While walking through tests (how the initial tree is build, where from?) we annotate test based on the
   values from test/extended/util/annotate/generated/zz_generated.annotations.go.
