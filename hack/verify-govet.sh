#!/bin/bash

set -o nounset
set -o pipefail

OS_ROOT=$(dirname "${BASH_SOURCE}")/..
source "${OS_ROOT}/hack/lib/init.sh"

os::golang::verify_go_version

cd "${OS_ROOT}"
mkdir -p _output/govet

os::build::setup_env

vetexceptions=(
  "pkg/auth/ldaputil/client.go:69: assignment copies lock value to c: crypto/tls.Config contains sync.Once contains sync.Mutex"
)
function is_vetexception()
{
  text=$1
  echo "checking ${text}"
  for ve in "${vetexceptions[@]}"
  do
    if [[ ve == ${text} ]]
    then
    echo "returning true"
      return 0
    fi
  done
  return 1
}

FAILURE=false
test_dirs=$(find_files | cut -d '/' -f 1-2 | sort -u)
for test_dir in $test_dirs
do
  result=$(go tool vet -shadow=false $test_dir)
  if [ "$?" -ne 0 ] && [ ! is_vetexception "${result}" ]
  then
    FAILURE=true
  fi
done

# We don't want to exit on the first failure of go vet, so just keep track of
# whether a failure occurred or not.
if $FAILURE
then
  echo "FAILURE: go vet failed!"
  exit 1
else
  echo "SUCCESS: go vet succeded!"
  exit 0
fi
