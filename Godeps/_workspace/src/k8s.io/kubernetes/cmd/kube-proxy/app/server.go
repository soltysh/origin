/*
Copyright 2014 The Kubernetes Authors All rights reserved.

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

// Package app does all of the work necessary to configure and run a
// Kubernetes app process.
package app

import (
	"errors"
	"net"
	"net/http"
	_ "net/http/pprof"
	"strconv"
	"time"

	"k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/client/record"
	kubeclient "k8s.io/kubernetes/pkg/client/unversioned"
	"k8s.io/kubernetes/pkg/client/unversioned/clientcmd"
	clientcmdapi "k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api"
	"k8s.io/kubernetes/pkg/kubelet/qos"
	"k8s.io/kubernetes/pkg/proxy"
	proxyconfig "k8s.io/kubernetes/pkg/proxy/config"
	"k8s.io/kubernetes/pkg/proxy/iptables"
	"k8s.io/kubernetes/pkg/proxy/userspace"
	"k8s.io/kubernetes/pkg/types"
	"k8s.io/kubernetes/pkg/util"
	utildbus "k8s.io/kubernetes/pkg/util/dbus"
	"k8s.io/kubernetes/pkg/util/exec"
	utiliptables "k8s.io/kubernetes/pkg/util/iptables"
	nodeutil "k8s.io/kubernetes/pkg/util/node"
	"k8s.io/kubernetes/pkg/util/oom"

	"github.com/golang/glog"
	"github.com/spf13/cobra"
	"github.com/spf13/pflag"
)

// ProxyServerConfig contains configures and runs a Kubernetes proxy server
type ProxyServerConfig struct {
	BindAddress        net.IP
	HealthzPort        int
	HealthzBindAddress net.IP
	OOMScoreAdj        int
	ResourceContainer  string
	Master             string
	Kubeconfig         string
	PortRange          util.PortRange
	HostnameOverride   string
	ProxyMode          string
	IptablesSyncPeriod time.Duration
	ConfigSyncPeriod   time.Duration
	NodeRef            *api.ObjectReference // Reference to this node.
	MasqueradeAll      bool
	CleanupAndExit     bool
	KubeAPIQPS         float32
	KubeAPIBurst       int
	UDPIdleTimeout     time.Duration
}

type ProxyServer struct {
	Client       *kubeclient.Client
	Config       *ProxyServerConfig
	IptInterface utiliptables.Interface
	Proxier      proxy.ProxyProvider
	Broadcaster  record.EventBroadcaster
	Recorder     record.EventRecorder
}

// AddFlags adds flags for a specific ProxyServer to the specified FlagSet
func (s *ProxyServerConfig) AddFlags(fs *pflag.FlagSet) {
	fs.IPVar(&s.BindAddress, "bind-address", s.BindAddress, "The IP address for the proxy server to serve on (set to 0.0.0.0 for all interfaces)")
	fs.StringVar(&s.Master, "master", s.Master, "The address of the Kubernetes API server (overrides any value in kubeconfig)")
	fs.IntVar(&s.HealthzPort, "healthz-port", s.HealthzPort, "The port to bind the health check server. Use 0 to disable.")
	fs.IPVar(&s.HealthzBindAddress, "healthz-bind-address", s.HealthzBindAddress, "The IP address for the health check server to serve on, defaulting to 127.0.0.1 (set to 0.0.0.0 for all interfaces)")
	fs.IntVar(&s.OOMScoreAdj, "oom-score-adj", s.OOMScoreAdj, "The oom-score-adj value for kube-proxy process. Values must be within the range [-1000, 1000]")
	fs.StringVar(&s.ResourceContainer, "resource-container", s.ResourceContainer, "Absolute name of the resource-only container to create and run the Kube-proxy in (Default: /kube-proxy).")
	fs.MarkDeprecated("resource-container", "This feature will be removed in a later release.")
	fs.StringVar(&s.Kubeconfig, "kubeconfig", s.Kubeconfig, "Path to kubeconfig file with authorization information (the master location is set by the master flag).")
	fs.Var(&s.PortRange, "proxy-port-range", "Range of host ports (beginPort-endPort, inclusive) that may be consumed in order to proxy service traffic. If unspecified (0-0) then ports will be randomly chosen.")
	fs.StringVar(&s.HostnameOverride, "hostname-override", s.HostnameOverride, "If non-empty, will use this string as identification instead of the actual hostname.")
	fs.StringVar(&s.ProxyMode, "proxy-mode", "", "Which proxy mode to use: 'userspace' (older) or 'iptables' (faster). If blank, look at the Node object on the Kubernetes API and respect the '"+experimentalProxyModeAnnotation+"' annotation if provided.  Otherwise use the best-available proxy (currently iptables).  If the iptables proxy is selected, regardless of how, but the system's kernel or iptables versions are insufficient, this always falls back to the userspace proxy.")
	fs.DurationVar(&s.IptablesSyncPeriod, "iptables-sync-period", s.IptablesSyncPeriod, "How often iptables rules are refreshed (e.g. '5s', '1m', '2h22m').  Must be greater than 0.")
	fs.DurationVar(&s.ConfigSyncPeriod, "config-sync-period", s.ConfigSyncPeriod, "How often configuration from the apiserver is refreshed.  Must be greater than 0.")
	fs.BoolVar(&s.MasqueradeAll, "masquerade-all", false, "If using the pure iptables proxy, SNAT everything")
	fs.BoolVar(&s.CleanupAndExit, "cleanup-iptables", false, "If true cleanup iptables rules and exit.")
	fs.Float32Var(&s.KubeAPIQPS, "kube-api-qps", s.KubeAPIQPS, "QPS to use while talking with kubernetes apiserver")
	fs.IntVar(&s.KubeAPIBurst, "kube-api-burst", s.KubeAPIBurst, "Burst to use while talking with kubernetes apiserver")
	fs.DurationVar(&s.UDPIdleTimeout, "udp-timeout", s.UDPIdleTimeout, "How long an idle UDP connection will be kept open (e.g. '250ms', '2s').  Must be greater than 0. Only applicable for proxy-mode=userspace")
}

const (
	proxyModeUserspace              = "userspace"
	proxyModeIptables               = "iptables"
	experimentalProxyModeAnnotation = "net.experimental.kubernetes.io/proxy-mode"
	betaProxyModeAnnotation         = "net.beta.kubernetes.io/proxy-mode"
)

func checkKnownProxyMode(proxyMode string) bool {
	switch proxyMode {
	case "", proxyModeUserspace, proxyModeIptables:
		return true
	}
	return false
}

func NewProxyConfig() *ProxyServerConfig {
	return &ProxyServerConfig{
		BindAddress:        net.ParseIP("0.0.0.0"),
		HealthzPort:        10249,
		HealthzBindAddress: net.ParseIP("127.0.0.1"),
		OOMScoreAdj:        qos.KubeProxyOOMScoreAdj,
		ResourceContainer:  "/kube-proxy",
		IptablesSyncPeriod: 30 * time.Second,
		ConfigSyncPeriod:   15 * time.Minute,
		KubeAPIQPS:         5.0,
		KubeAPIBurst:       10,
		UDPIdleTimeout:     250 * time.Millisecond,
	}
}

func NewProxyServer(
	client *kubeclient.Client,
	config *ProxyServerConfig,
	iptInterface utiliptables.Interface,
	proxier proxy.ProxyProvider,
	broadcaster record.EventBroadcaster,
	recorder record.EventRecorder,
) (*ProxyServer, error) {
	return &ProxyServer{
		Client:       client,
		Config:       config,
		IptInterface: iptInterface,
		Proxier:      proxier,
		Broadcaster:  broadcaster,
		Recorder:     recorder,
	}, nil
}

// NewProxyCommand creates a *cobra.Command object with default parameters
func NewProxyCommand() *cobra.Command {
	s := NewProxyConfig()
	s.AddFlags(pflag.CommandLine)
	cmd := &cobra.Command{
		Use: "kube-proxy",
		Long: `The Kubernetes network proxy runs on each node. This
reflects services as defined in the Kubernetes API on each node and can do simple
TCP,UDP stream forwarding or round robin TCP,UDP forwarding across a set of backends.
Service cluster ips and ports are currently found through Docker-links-compatible
environment variables specifying ports opened by the service proxy. There is an optional
addon that provides cluster DNS for these cluster IPs. The user must create a service
with the apiserver API to configure the proxy.`,
		Run: func(cmd *cobra.Command, args []string) {
		},
	}

	return cmd
}

// NewProxyServerDefault creates a new ProxyServer object with default parameters.
func NewProxyServerDefault(config *ProxyServerConfig) (*ProxyServer, error) {
	protocol := utiliptables.ProtocolIpv4
	if config.BindAddress.To4() == nil {
		protocol = utiliptables.ProtocolIpv6
	}

	// Create a iptables utils.
	execer := exec.New()
	dbus := utildbus.New()
	iptInterface := utiliptables.New(execer, dbus, protocol)

	// We ommit creation of pretty much everything if we run in cleanup mode
	if config.CleanupAndExit {
		return &ProxyServer{
			Config:       config,
			IptInterface: iptInterface,
		}, nil
	}

	// TODO(vmarmol): Use container config for this.
	var oomAdjuster *oom.OOMAdjuster
	if config.OOMScoreAdj != 0 {
		oomAdjuster = oom.NewOOMAdjuster()
		if err := oomAdjuster.ApplyOOMScoreAdj(0, config.OOMScoreAdj); err != nil {
			glog.V(2).Info(err)
		}
	}

	if config.ResourceContainer != "" {
		// Run in its own container.
		if err := util.RunInResourceContainer(config.ResourceContainer); err != nil {
			glog.Warningf("Failed to start in resource-only container %q: %v", config.ResourceContainer, err)
		} else {
			glog.V(2).Infof("Running in resource-only container %q", config.ResourceContainer)
		}
	}

	// Create a Kube Client
	// define api config source
	if config.Kubeconfig == "" && config.Master == "" {
		glog.Warningf("Neither --kubeconfig nor --master was specified.  Using default API client.  This might not work.")
	}
	// This creates a client, first loading any specified kubeconfig
	// file, and then overriding the Master flag, if non-empty.
	kubeconfig, err := clientcmd.NewNonInteractiveDeferredLoadingClientConfig(
		&clientcmd.ClientConfigLoadingRules{ExplicitPath: config.Kubeconfig},
		&clientcmd.ConfigOverrides{ClusterInfo: clientcmdapi.Cluster{Server: config.Master}}).ClientConfig()
	if err != nil {
		return nil, err
	}

	// Override kubeconfig qps/burst settings from flags
	kubeconfig.QPS = config.KubeAPIQPS
	kubeconfig.Burst = config.KubeAPIBurst

	client, err := kubeclient.New(kubeconfig)
	if err != nil {
		glog.Fatalf("Invalid API configuration: %v", err)
	}

	// Create event recorder
	hostname := nodeutil.GetHostname(config.HostnameOverride)
	eventBroadcaster := record.NewBroadcaster()
	recorder := eventBroadcaster.NewRecorder(api.EventSource{Component: "kube-proxy", Host: hostname})

	var proxier proxy.ProxyProvider
	var endpointsHandler proxyconfig.EndpointsConfigHandler

	proxyMode := getProxyMode(config.ProxyMode, client.Nodes(), hostname, iptInterface)
	if proxyMode == proxyModeIptables {
		glog.V(2).Info("Using iptables Proxier.")
		proxierIptables, err := iptables.NewProxier(iptInterface, execer, config.IptablesSyncPeriod, config.MasqueradeAll)
		if err != nil {
			glog.Fatalf("Unable to create proxier: %v", err)
		}
		proxier = proxierIptables
		endpointsHandler = proxierIptables
		// No turning back. Remove artifacts that might still exist from the userspace Proxier.
		glog.V(2).Info("Tearing down userspace rules. Errors here are acceptable.")
		userspace.CleanupLeftovers(iptInterface)
	} else {
		glog.V(2).Info("Using userspace Proxier.")
		// This is a proxy.LoadBalancer which NewProxier needs but has methods we don't need for
		// our config.EndpointsConfigHandler.
		loadBalancer := userspace.NewLoadBalancerRR()
		// set EndpointsConfigHandler to our loadBalancer
		endpointsHandler = loadBalancer

		proxierUserspace, err := userspace.NewProxier(loadBalancer, config.BindAddress, iptInterface, config.PortRange, config.IptablesSyncPeriod, config.UDPIdleTimeout)
		if err != nil {
			glog.Fatalf("Unable to create proxier: %v", err)
		}
		proxier = proxierUserspace
		// Remove artifacts from the pure-iptables Proxier.
		glog.V(2).Info("Tearing down pure-iptables proxy rules. Errors here are acceptable.")
		iptables.CleanupLeftovers(iptInterface)
	}
	iptInterface.AddReloadFunc(proxier.Sync)

	// Create configs (i.e. Watches for Services and Endpoints)
	// Note: RegisterHandler() calls need to happen before creation of Sources because sources
	// only notify on changes, and the initial update (on process start) may be lost if no handlers
	// are registered yet.
	serviceConfig := proxyconfig.NewServiceConfig()
	serviceConfig.RegisterHandler(proxier)

	endpointsConfig := proxyconfig.NewEndpointsConfig()
	endpointsConfig.RegisterHandler(endpointsHandler)

	proxyconfig.NewSourceAPI(
		client,
		config.ConfigSyncPeriod,
		serviceConfig.Channel("api"),
		endpointsConfig.Channel("api"),
	)

	config.NodeRef = &api.ObjectReference{
		Kind:      "Node",
		Name:      hostname,
		UID:       types.UID(hostname),
		Namespace: "",
	}
	return NewProxyServer(client, config, iptInterface, proxier, eventBroadcaster, recorder)
}

// Run runs the specified ProxyServer.  This should never exit (unless CleanupAndExit is set).
func (s *ProxyServer) Run(_ []string) error {
	// remove iptables rules and exit
	if s.Config.CleanupAndExit {
		encounteredError := userspace.CleanupLeftovers(s.IptInterface)
		encounteredError = iptables.CleanupLeftovers(s.IptInterface) || encounteredError
		if encounteredError {
			return errors.New("Encountered an error while tearing down rules.")
		}
		return nil
	}

	s.Broadcaster.StartRecordingToSink(s.Client.Events(""))

	// Birth Cry after the birth is successful
	s.birthCry()

	// Start up Healthz service if requested
	if s.Config.HealthzPort > 0 {
		go util.Until(func() {
			err := http.ListenAndServe(s.Config.HealthzBindAddress.String()+":"+strconv.Itoa(s.Config.HealthzPort), nil)
			if err != nil {
				glog.Errorf("Starting health server failed: %v", err)
			}
		}, 5*time.Second, util.NeverStop)
	}

	// Just loop forever for now...
	s.Proxier.SyncLoop()
	return nil
}

type nodeGetter interface {
	Get(hostname string) (*api.Node, error)
}

func getProxyMode(proxyMode string, client nodeGetter, hostname string, iptver iptables.IptablesVersioner) string {
	if proxyMode == proxyModeUserspace {
		return proxyModeUserspace
	} else if proxyMode == proxyModeIptables {
		return tryIptablesProxy(iptver)
	} else if proxyMode != "" {
		glog.V(1).Infof("Flag proxy-mode=%q unknown, assuming iptables proxy", proxyMode)
		return tryIptablesProxy(iptver)
	}
	// proxyMode == "" - choose the best option.
	if client == nil {
		glog.Errorf("nodeGetter is nil: assuming iptables proxy")
		return tryIptablesProxy(iptver)
	}
	node, err := client.Get(hostname)
	if err != nil {
		glog.Errorf("Can't get Node %q, assuming iptables proxy: %v", hostname, err)
		return tryIptablesProxy(iptver)
	}
	if node == nil {
		glog.Errorf("Got nil Node %q, assuming iptables proxy: %v", hostname)
		return tryIptablesProxy(iptver)
	}
	proxyMode, found := node.Annotations[betaProxyModeAnnotation]
	if found {
		glog.V(1).Infof("Found beta annotation %q = %q", betaProxyModeAnnotation, proxyMode)
	} else {
		// We already published some information about this annotation with the "experimental" name, so we will respect it.
		proxyMode, found = node.Annotations[experimentalProxyModeAnnotation]
		if found {
			glog.V(1).Infof("Found experimental annotation %q = %q", experimentalProxyModeAnnotation, proxyMode)
		}
	}
	if proxyMode == proxyModeUserspace {
		glog.V(1).Infof("Annotation demands userspace proxy")
		return proxyModeUserspace
	}
	return tryIptablesProxy(iptver)
}

func tryIptablesProxy(iptver iptables.IptablesVersioner) string {
	var err error
	// guaranteed false on error, error only necessary for debugging
	useIptablesProxy, err := iptables.CanUseIptablesProxier(iptver)
	if err != nil {
		glog.Errorf("Can't determine whether to use iptables proxy, using userspace proxier: %v", err)
		return proxyModeUserspace
	}
	if useIptablesProxy {
		return proxyModeIptables
	}
	// Fallback.
	glog.V(1).Infof("Can't use iptables proxy, using userspace proxier: %v", err)
	return proxyModeUserspace
}

func (s *ProxyServer) birthCry() {
	s.Recorder.Eventf(s.Config.NodeRef, api.EventTypeNormal, "Starting", "Starting kube-proxy.")
}
