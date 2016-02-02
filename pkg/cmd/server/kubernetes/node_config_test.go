package kubernetes

import (
	"net"
	"reflect"
	"testing"
	"time"

	proxyoptions "k8s.io/kubernetes/cmd/kube-proxy/app"
	"k8s.io/kubernetes/pkg/kubelet/qos"
)

func TestProxyConfig(t *testing.T) {
	// This is a snapshot of the default config
	// If the default changes (new fields are added, or default values change), we want to know
	// Once we've reacted to the changes appropriately in buildKubeProxyConfig(), update this expected default to match the new upstream defaults
	expectedDefaultConfig := &proxyoptions.ProxyServerConfig{
		BindAddress:        net.ParseIP("0.0.0.0"),
		HealthzPort:        10249,
		HealthzBindAddress: net.ParseIP("127.0.0.1"),
		OOMScoreAdj:        qos.KubeProxyOOMScoreAdj,
		ResourceContainer:  "/kube-proxy",
		SyncPeriod:         30 * time.Second,
		KubeApiQps:         5.0,
		KubeApiBurst:       10,
	}

	actualDefaultConfig := proxyoptions.NewProxyConfig()

	if !reflect.DeepEqual(expectedDefaultConfig, actualDefaultConfig) {
		t.Errorf("Default kube proxy config has changed. Adjust buildKubeProxyConfig() as needed to disable or make use of additions.")
		t.Logf("Expected default config:\n%#v\n\n", expectedDefaultConfig)
		t.Logf("Actual default config:\n%#v\n\n", actualDefaultConfig)
	}

}
