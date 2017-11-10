package integration

import (
	"testing"
	"time"

	extensionsv1beta1 "k8s.io/api/extensions/v1beta1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/wait"
	internalextensionsv1beta1 "k8s.io/kubernetes/pkg/apis/extensions/v1beta1"

	deployapi "github.com/openshift/origin/pkg/apps/apis/apps"
	deploytest "github.com/openshift/origin/pkg/apps/apis/apps/test"
	appsclient "github.com/openshift/origin/pkg/apps/generated/internalclientset"
	deployutil "github.com/openshift/origin/pkg/apps/util"
	testutil "github.com/openshift/origin/test/util"
	testserver "github.com/openshift/origin/test/util/server"
)

func TestDeployScale(t *testing.T) {
	const namespace = "test-deploy-scale"

	masterConfig, clusterAdminKubeConfig, err := testserver.StartTestMaster()
	if err != nil {
		t.Fatal(err)
	}
	defer testserver.CleanupMasterEtcd(t, masterConfig)
	clusterAdminClientConfig, err := testutil.GetClusterAdminClientConfig(clusterAdminKubeConfig)
	if err != nil {
		t.Fatal(err)
	}
	_, _, err = testserver.CreateNewProject(clusterAdminClientConfig, namespace, "my-test-user")
	if err != nil {
		t.Fatal(err)
	}
	_, adminConfig, err := testutil.GetClientForUser(clusterAdminClientConfig, "my-test-user")
	if err != nil {
		t.Fatal(err)
	}
	adminAppsClient := appsclient.NewForConfigOrDie(adminConfig).Apps()

	config := deploytest.OkDeploymentConfig(0)
	config.Namespace = namespace
	config.Spec.Triggers = []deployapi.DeploymentTriggerPolicy{}
	config.Spec.Replicas = 1

	dc, err := adminAppsClient.DeploymentConfigs(namespace).Create(config)
	if err != nil {
		t.Fatalf("Couldn't create DeploymentConfig: %v %#v", err, config)
	}
	generation := dc.Generation

	condition := func() (bool, error) {
		config, err := adminAppsClient.DeploymentConfigs(namespace).Get(dc.Name, metav1.GetOptions{})
		if err != nil {
			return false, nil
		}
		return deployutil.HasSynced(config, generation), nil
	}
	if err := wait.PollImmediate(500*time.Millisecond, 10*time.Second, condition); err != nil {
		t.Fatalf("Deployment config never synced: %v", err)
	}

	scale, err := adminAppsClient.DeploymentConfigs(namespace).GetScale(config.Name, metav1.GetOptions{})
	if err != nil {
		t.Fatalf("Couldn't get DeploymentConfig scale: %v", err)
	}
	if scale.Spec.Replicas != 1 {
		t.Fatalf("Expected scale.spec.replicas=1, got %#v", scale)
	}

	scaleUpdate := deployapi.ScaleFromConfig(dc)
	scaleUpdate.Spec.Replicas = 3
	scaleUpdatev1beta1 := &extensionsv1beta1.Scale{}
	if err := internalextensionsv1beta1.Convert_extensions_Scale_To_v1beta1_Scale(scaleUpdate, scaleUpdatev1beta1, nil); err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	updatedScale, err := adminAppsClient.DeploymentConfigs(namespace).UpdateScale(config.Name, scaleUpdatev1beta1)
	if err != nil {
		// If this complains about "Scale" not being registered in "v1", check the kind overrides in the API registration in SubresourceGroupVersionKind
		t.Fatalf("Couldn't update DeploymentConfig scale to %#v: %v", scaleUpdate, err)
	}
	if updatedScale.Spec.Replicas != 3 {
		t.Fatalf("Expected scale.spec.replicas=3, got %#v", scale)
	}

	persistedScale, err := adminAppsClient.DeploymentConfigs(namespace).GetScale(config.Name, metav1.GetOptions{})
	if err != nil {
		t.Fatalf("Couldn't get DeploymentConfig scale: %v", err)
	}
	if persistedScale.Spec.Replicas != 3 {
		t.Fatalf("Expected scale.spec.replicas=3, got %#v", scale)
	}
}
