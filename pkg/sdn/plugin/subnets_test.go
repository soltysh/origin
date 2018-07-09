package plugin

import (
	"testing"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/aws"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/azure"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/gce"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/mesos"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/openstack"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/ovirt"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/photon"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/rackspace"
	"k8s.io/kubernetes/pkg/cloudprovider/providers/vsphere"
)

func testNodeCP(provider string) *kapi.Node {
	node := &kapi.Node{
		Spec: kapi.NodeSpec{
			ProviderID: provider + "://instanceID",
		},
		Status: kapi.NodeStatus{},
	}

	switch provider {
	case azure.CloudProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "azureNode",
			},
		}
	case aws.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeLegacyHostIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "172.10.15.2",
			},
			{
				Type:    kapi.NodeInternalDNS,
				Address: "NodeInternalDNS",
			},
			{
				Type:    kapi.NodeExternalDNS,
				Address: "NodeExternalDNS",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "awsNode",
			},
		}
	case gce.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "172.10.15.2",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "gceNode",
			},
		}
	case mesos.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeLegacyHostIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.6",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "mesosNode",
			},
		}
	case openstack.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.6",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "openstackNode",
			},
		}
	case ovirt.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeLegacyHostIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.6",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "ovirtNode",
			},
		}
	case photon.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "photonNode",
			},
		}
	case rackspace.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeLegacyHostIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.6",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "rackspaceNode",
			},
		}
	case vsphere.ProviderName:
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeInternalIP,
				Address: "10.1.1.4",
			},
			{
				Type:    kapi.NodeExternalIP,
				Address: "10.1.1.5",
			},
			{
				Type:    kapi.NodeHostName,
				Address: "vsphereNode",
			},
		}
	}

	return node
}

func swapAddresses(node *kapi.Node, i, j int) *kapi.Node {
	node.Status.Addresses[i], node.Status.Addresses[j] = node.Status.Addresses[j], node.Status.Addresses[i]
	return node
}

func changeAddressesType(node *kapi.Node, i int, addrType kapi.NodeAddressType) *kapi.Node {
	node.Status.Addresses[i].Type = addrType
	return node
}

func setHostnameAddressesType(node *kapi.Node, i int, hostname string) *kapi.Node {
	if len(node.Status.Addresses) > i {
		node.Status.Addresses[i] = kapi.NodeAddress{Type: kapi.NodeHostName, Address: hostname}
	} else {
		node.Status.Addresses = []kapi.NodeAddress{
			{
				Type:    kapi.NodeHostName,
				Address: hostname,
			},
		}
	}
	return node
}

func TestGetNodeIpFromNodeObject(t *testing.T) {
	// test various cloud providers
	// test with errors as well

	testCases := []struct {
		name       string
		node       *kapi.Node
		err        error
		expectedIP string
	}{
		{
			name:       "Get node IP, Azure cloud provided, no error",
			node:       testNodeCP(azure.CloudProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, Azure cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(azure.CloudProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, AWS cloud provided, no error",
			node:       testNodeCP(aws.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, AWS cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(aws.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, GCE cloud provided, no error",
			node:       testNodeCP(gce.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, GCE cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(gce.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "172.10.15.2",
		},
		{
			name:       "Get node IP, Mesos cloud provided, no error",
			node:       testNodeCP(mesos.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, Mesos cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(mesos.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, OpenStack cloud provided, first ExternalIP, no error",
			node:       testNodeCP(openstack.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, OpenStack cloud provided, first InternalIP, no error",
			node:       changeAddressesType(testNodeCP(openstack.ProviderName), 0, kapi.NodeInternalIP),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, OVirt cloud provided, no error",
			node:       testNodeCP(mesos.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, OVirt cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(mesos.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, Photon cloud provided, no error",
			node:       testNodeCP(photon.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, Photon cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(photon.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, Rackspace cloud provided, no error",
			node:       testNodeCP(rackspace.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, Rackspace cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(rackspace.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, VSphere cloud provided, no error",
			node:       testNodeCP(vsphere.ProviderName),
			err:        nil,
			expectedIP: "10.1.1.4",
		},
		{
			name:       "Get node IP, VSphere cloud provided, swapped node addresses, no error",
			node:       swapAddresses(testNodeCP(vsphere.ProviderName), 0, 1),
			err:        nil,
			expectedIP: "10.1.1.5",
		},
		{
			name:       "Get node IP, Unknown cloud provided, hostname, no error",
			node:       setHostnameAddressesType(testNodeCP(""), 0, "UnknownCloudProvider"),
			err:        nil,
			expectedIP: "UnknownCloudProvider",
		},
	}

	for _, test := range testCases {
		ip, err := getNodeIP(test.node)
		if err != test.err {
			t.Errorf("%q: Unexpected error %v, expected %v\n", test.name, err, test.err)
		}
		if ip != test.expectedIP {
			t.Errorf("%q: Unexpected IP address %v, expected %v\n", test.name, ip, test.expectedIP)
		}
	}
}
