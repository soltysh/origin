package main

import (
	"strings"
	"os"
	"flag"
	"fmt"

	"github.com/blang/semver"
)

const (
	versionBumpUsageLong = `Speculatively generate the next RPM release version of Origin.

%[1]s consumes the ${OS_GIT_VERSION} as generated by os::build::get_version_vars
and speculatively generates the version that would exist after the next bump. This
is useful in generating release-like RPMs and artifacts for test builds. The output
from this utility will not be a semantic version.
`

	versionBumpUsage = `Usage:
  %[1]s "${OS_GIT_VERSION}"
`

	versionBumpExamples = `Examples:
  # Generate the next release version
  %[1]s "${OS_GIT_VERSION}"

  # Parse the output into version and release
  next_release_version="$( %[1]s "${OS_GIT_VERSION}" )"
  next_version="${next_release_version%%%%-*}"
  next_release="${next_release_version#*-}"
`
)

func main() {
	executable := os.Args[0]
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, versionBumpUsageLong+"\n", executable)
		fmt.Fprintf(os.Stderr, versionBumpUsage+"\n", executable)
		fmt.Fprintf(os.Stderr, versionBumpExamples+"\n", executable)
		os.Exit(2)
	}
	flag.Parse()

	arguments := flag.Args()
	if len(arguments) != 1 {
		fmt.Fprintf(os.Stderr, "Incorrect usage of %[1]s, see '%[1]s --help' for more details.\n", executable)
		os.Exit(1)
	}

	// Origin version start with a `v` that we strip off
	currentVersion := arguments[0][1:]
	currentSemver, err := semver.Make(currentVersion)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing ${OS_GIT_VERSION}: %v.\n", err)
		os.Exit(1)
	}

	if len(currentSemver.Pre) > 0 {
		// if we're at a pre-release state, we can just remove it to bump the version
		currentSemver.Pre = nil
	} else {
		// if we're in a post-release state, we can bump the patch version
		currentSemver.Patch = currentSemver.Patch + 1
	}

	// for RPM, we cannot have the character `-` in any build metadata, so we replace it with `.`
	sanitizedMetadata := []string{}
	for _, data := range currentSemver.Build {
		sanitizedMetadata = append(sanitizedMetadata, strings.Replace(data, "-", ".", -1))
	}
	currentSemver.Build = sanitizedMetadata

	// for RPM, we want to have a post-release patch level of 0, which we can fake with Pre
	currentSemver.Pre = []semver.PRVersion{
		semver.PRVersion{
			VersionStr: "0",
		},
	}

	fmt.Fprintf(os.Stderr, "%s\n", currentSemver.String())
}