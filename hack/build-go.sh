#!/usr/bin/env bash

set -x

go test -c -trimpath -o $(pwd)/origin-e2e.test github.com/openshift/origin/cmd/e2e
go build -trimpath github.com/openshift/origin/cmd/openshift-tests
go build -trimpath github.com/onsi/ginkgo/v2/ginkgo
