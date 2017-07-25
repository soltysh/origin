package images

import (
	"fmt"
	"regexp"
	"sort"
	"strconv"
	"strings"

	g "github.com/onsi/ginkgo"
	//o "github.com/onsi/gomega"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/client/unversioned"
	"k8s.io/kubernetes/pkg/labels"

	dockerregistryserver "github.com/openshift/origin/pkg/dockerregistry/server"
	exutil "github.com/openshift/origin/test/extended/util"
)

const (
	readOnlyEnvVar       = "REGISTRY_STORAGE_MAINTENANCE_READONLY"
	defaultAcceptSchema2 = false
)

// GetDockerRegistryURL returns a cluster URL of internal docker registry if available.
func GetDockerRegistryURL(oc *exutil.CLI) (string, error) {
	svc, err := oc.AdminKubeREST().Services("default").Get("docker-registry")
	if err != nil {
		return "", err
	}
	url := svc.Spec.ClusterIP
	for _, p := range svc.Spec.Ports {
		url = fmt.Sprintf("%s:%d", url, p.Port)
		break
	}
	return url, nil
}

// GetRegistryStorageSize returns a number of bytes occupied by registry's data on its filesystem.
func GetRegistryStorageSize(oc *exutil.CLI) (int64, error) {
	defer func(ns string) { oc.SetNamespace(ns) }(oc.Namespace())
	out, err := oc.SetNamespace(kapi.NamespaceDefault).AsAdmin().Run("rsh").Args(
		"dc/docker-registry", "du", "--bytes", "--summarize", "/registry/docker/registry").Output()
	if err != nil {
		return 0, err
	}
	m := regexp.MustCompile(`^\d+`).FindString(out)
	if len(m) == 0 {
		return 0, fmt.Errorf("failed to parse du output: %s", out)
	}

	size, err := strconv.ParseInt(m, 10, 64)
	if err != nil {
		return 0, fmt.Errorf("failed to parse du output: %s", m)
	}

	return size, nil
}

// DoesRegistryAcceptSchema2 returns true if the integrated registry is configured to accept manifest V2
// schema 2.
func DoesRegistryAcceptSchema2(oc *exutil.CLI) (bool, error) {
	defer func(ns string) { oc.SetNamespace(ns) }(oc.Namespace())
	env, err := oc.SetNamespace(kapi.NamespaceDefault).AsAdmin().Run("env").Args("dc/docker-registry", "--list").Output()
	if err != nil {
		return defaultAcceptSchema2, err
	}

	if strings.Contains(env, fmt.Sprintf("%s=", dockerregistryserver.AcceptSchema2EnvVar)) {
		return strings.Contains(env, fmt.Sprintf("%s=true", dockerregistryserver.AcceptSchema2EnvVar)), nil
	}

	return defaultAcceptSchema2, nil
}

// RegistriConfiguration holds desired configuration options for the integrated registry. *nil* stands for
// "no change".
type RegistryConfiguration struct {
	ReadOnly      *bool
	AcceptSchema2 *bool
}

type byAgeDesc []kapi.Pod

func (ba byAgeDesc) Len() int      { return len(ba) }
func (ba byAgeDesc) Swap(i, j int) { ba[i], ba[j] = ba[j], ba[i] }
func (ba byAgeDesc) Less(i, j int) bool {
	return ba[j].CreationTimestamp.Before(ba[i].CreationTimestamp)
}

// GetRegistryPod returns the youngest registry pod deployed.
func GetRegistryPod(podsGetter unversioned.PodsNamespacer) (*kapi.Pod, error) {
	podList, err := podsGetter.Pods(kapi.NamespaceDefault).List(kapi.ListOptions{
		LabelSelector: labels.SelectorFromSet(labels.Set{"deploymentconfig": "docker-registry"}),
	})
	if err != nil {
		return nil, err
	}
	if len(podList.Items) == 0 {
		return nil, fmt.Errorf("failed to find any docker-registry pod")
	}

	sort.Sort(byAgeDesc(podList.Items))

	return &podList.Items[0], nil
}

// ConfigureRegistry re-deploys the registry pod if its configuration doesn't match the desiredState. The
// function blocks until the registry is ready.
func ConfigureRegistry(oc *exutil.CLI, desiredState RegistryConfiguration) error {
	defer func(ns string) { oc.SetNamespace(ns) }(oc.Namespace())
	oc = oc.SetNamespace(kapi.NamespaceDefault).AsAdmin()
	env, err := oc.Run("env").Args("dc/docker-registry", "--list").Output()
	if err != nil {
		return err
	}

	envOverrides := []string{}

	if desiredState.AcceptSchema2 != nil {
		current := defaultAcceptSchema2
		if strings.Contains(env, fmt.Sprintf("%s=%t", dockerregistryserver.AcceptSchema2EnvVar, !defaultAcceptSchema2)) {
			current = !defaultAcceptSchema2
		}
		if current != *desiredState.AcceptSchema2 {
			new := fmt.Sprintf("%s=%t", dockerregistryserver.AcceptSchema2EnvVar, *desiredState.AcceptSchema2)
			envOverrides = append(envOverrides, new)
		}
	}
	if desiredState.ReadOnly != nil {
		value := fmt.Sprintf("%s=%s", readOnlyEnvVar, makeReadonlyEnvValue(*desiredState.ReadOnly))
		if !strings.Contains(env, value) {
			envOverrides = append(envOverrides, value)
		}
	}
	if len(envOverrides) == 0 {
		g.By("docker-registry is already in the desired state of configuration")
		return nil
	}

	dc, err := oc.REST().DeploymentConfigs(kapi.NamespaceDefault).Get("docker-registry")
	if err != nil {
		return err
	}
	waitForVersion := dc.Status.LatestVersion + 1

	err = oc.Run("env").Args(append([]string{"dc/docker-registry"}, envOverrides...)...).Execute()
	if err != nil {
		return fmt.Errorf("failed to update registry's environment with %s: %v", &waitForVersion, err)
	}
	return exutil.WaitForRegistry(oc.AdminREST(), oc.AdminKubeREST(), &waitForVersion, oc)
}

// EnsureRegistryAcceptsSchema2 checks whether the registry is configured to accept manifests V2 schema 2 or
// not. If the result doesn't match given accept argument, registry's deployment config will be updated
// accordingly and the function will block until the registry have been re-deployed and ready for new
// requests.
func EnsureRegistryAcceptsSchema2(oc *exutil.CLI, accept bool) error {
	return ConfigureRegistry(oc, RegistryConfiguration{AcceptSchema2: &accept})
}

func makeReadonlyEnvValue(on bool) string {
	return fmt.Sprintf(`{"enabled":%t}`, on)
}
