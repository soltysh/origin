// +build !ignore_autogenerated_openshift

// This file was autogenerated by conversion-gen. Do not edit it manually!

package v1

import (
	network "github.com/openshift/origin/pkg/network/apis/network"
	conversion "k8s.io/apimachinery/pkg/conversion"
	runtime "k8s.io/apimachinery/pkg/runtime"
	unsafe "unsafe"
)

func init() {
	localSchemeBuilder.Register(RegisterConversions)
}

// RegisterConversions adds conversion functions to the given scheme.
// Public to allow building arbitrary schemes.
func RegisterConversions(scheme *runtime.Scheme) error {
	return scheme.AddGeneratedConversionFuncs(
		Convert_v1_ClusterNetwork_To_network_ClusterNetwork,
		Convert_network_ClusterNetwork_To_v1_ClusterNetwork,
		Convert_v1_ClusterNetworkEntry_To_network_ClusterNetworkEntry,
		Convert_network_ClusterNetworkEntry_To_v1_ClusterNetworkEntry,
		Convert_v1_ClusterNetworkList_To_network_ClusterNetworkList,
		Convert_network_ClusterNetworkList_To_v1_ClusterNetworkList,
		Convert_v1_EgressNetworkPolicy_To_network_EgressNetworkPolicy,
		Convert_network_EgressNetworkPolicy_To_v1_EgressNetworkPolicy,
		Convert_v1_EgressNetworkPolicyList_To_network_EgressNetworkPolicyList,
		Convert_network_EgressNetworkPolicyList_To_v1_EgressNetworkPolicyList,
		Convert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer,
		Convert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer,
		Convert_v1_EgressNetworkPolicyRule_To_network_EgressNetworkPolicyRule,
		Convert_network_EgressNetworkPolicyRule_To_v1_EgressNetworkPolicyRule,
		Convert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec,
		Convert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec,
		Convert_v1_HostSubnet_To_network_HostSubnet,
		Convert_network_HostSubnet_To_v1_HostSubnet,
		Convert_v1_HostSubnetList_To_network_HostSubnetList,
		Convert_network_HostSubnetList_To_v1_HostSubnetList,
		Convert_v1_NetNamespace_To_network_NetNamespace,
		Convert_network_NetNamespace_To_v1_NetNamespace,
		Convert_v1_NetNamespaceList_To_network_NetNamespaceList,
		Convert_network_NetNamespaceList_To_v1_NetNamespaceList,
	)
}

func autoConvert_v1_ClusterNetwork_To_network_ClusterNetwork(in *ClusterNetwork, out *network.ClusterNetwork, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.Network = in.Network
	out.HostSubnetLength = in.HostSubnetLength
	out.ServiceNetwork = in.ServiceNetwork
	out.PluginName = in.PluginName
	out.ClusterNetworks = *(*[]network.ClusterNetworkEntry)(unsafe.Pointer(&in.ClusterNetworks))
	return nil
}

// Convert_v1_ClusterNetwork_To_network_ClusterNetwork is an autogenerated conversion function.
func Convert_v1_ClusterNetwork_To_network_ClusterNetwork(in *ClusterNetwork, out *network.ClusterNetwork, s conversion.Scope) error {
	return autoConvert_v1_ClusterNetwork_To_network_ClusterNetwork(in, out, s)
}

func autoConvert_network_ClusterNetwork_To_v1_ClusterNetwork(in *network.ClusterNetwork, out *ClusterNetwork, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.ClusterNetworks = *(*[]ClusterNetworkEntry)(unsafe.Pointer(&in.ClusterNetworks))
	out.Network = in.Network
	out.HostSubnetLength = in.HostSubnetLength
	out.ServiceNetwork = in.ServiceNetwork
	out.PluginName = in.PluginName
	return nil
}

// Convert_network_ClusterNetwork_To_v1_ClusterNetwork is an autogenerated conversion function.
func Convert_network_ClusterNetwork_To_v1_ClusterNetwork(in *network.ClusterNetwork, out *ClusterNetwork, s conversion.Scope) error {
	return autoConvert_network_ClusterNetwork_To_v1_ClusterNetwork(in, out, s)
}

func autoConvert_v1_ClusterNetworkEntry_To_network_ClusterNetworkEntry(in *ClusterNetworkEntry, out *network.ClusterNetworkEntry, s conversion.Scope) error {
	out.CIDR = in.CIDR
	out.HostSubnetLength = in.HostSubnetLength
	return nil
}

// Convert_v1_ClusterNetworkEntry_To_network_ClusterNetworkEntry is an autogenerated conversion function.
func Convert_v1_ClusterNetworkEntry_To_network_ClusterNetworkEntry(in *ClusterNetworkEntry, out *network.ClusterNetworkEntry, s conversion.Scope) error {
	return autoConvert_v1_ClusterNetworkEntry_To_network_ClusterNetworkEntry(in, out, s)
}

func autoConvert_network_ClusterNetworkEntry_To_v1_ClusterNetworkEntry(in *network.ClusterNetworkEntry, out *ClusterNetworkEntry, s conversion.Scope) error {
	out.CIDR = in.CIDR
	out.HostSubnetLength = in.HostSubnetLength
	return nil
}

// Convert_network_ClusterNetworkEntry_To_v1_ClusterNetworkEntry is an autogenerated conversion function.
func Convert_network_ClusterNetworkEntry_To_v1_ClusterNetworkEntry(in *network.ClusterNetworkEntry, out *ClusterNetworkEntry, s conversion.Scope) error {
	return autoConvert_network_ClusterNetworkEntry_To_v1_ClusterNetworkEntry(in, out, s)
}

func autoConvert_v1_ClusterNetworkList_To_network_ClusterNetworkList(in *ClusterNetworkList, out *network.ClusterNetworkList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]network.ClusterNetwork, len(*in))
		for i := range *in {
			if err := Convert_v1_ClusterNetwork_To_network_ClusterNetwork(&(*in)[i], &(*out)[i], s); err != nil {
				return err
			}
		}
	} else {
		out.Items = nil
	}
	return nil
}

// Convert_v1_ClusterNetworkList_To_network_ClusterNetworkList is an autogenerated conversion function.
func Convert_v1_ClusterNetworkList_To_network_ClusterNetworkList(in *ClusterNetworkList, out *network.ClusterNetworkList, s conversion.Scope) error {
	return autoConvert_v1_ClusterNetworkList_To_network_ClusterNetworkList(in, out, s)
}

func autoConvert_network_ClusterNetworkList_To_v1_ClusterNetworkList(in *network.ClusterNetworkList, out *ClusterNetworkList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]ClusterNetwork, len(*in))
		for i := range *in {
			if err := Convert_network_ClusterNetwork_To_v1_ClusterNetwork(&(*in)[i], &(*out)[i], s); err != nil {
				return err
			}
		}
	} else {
		out.Items = nil
	}
	return nil
}

// Convert_network_ClusterNetworkList_To_v1_ClusterNetworkList is an autogenerated conversion function.
func Convert_network_ClusterNetworkList_To_v1_ClusterNetworkList(in *network.ClusterNetworkList, out *ClusterNetworkList, s conversion.Scope) error {
	return autoConvert_network_ClusterNetworkList_To_v1_ClusterNetworkList(in, out, s)
}

func autoConvert_v1_EgressNetworkPolicy_To_network_EgressNetworkPolicy(in *EgressNetworkPolicy, out *network.EgressNetworkPolicy, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	if err := Convert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec(&in.Spec, &out.Spec, s); err != nil {
		return err
	}
	return nil
}

// Convert_v1_EgressNetworkPolicy_To_network_EgressNetworkPolicy is an autogenerated conversion function.
func Convert_v1_EgressNetworkPolicy_To_network_EgressNetworkPolicy(in *EgressNetworkPolicy, out *network.EgressNetworkPolicy, s conversion.Scope) error {
	return autoConvert_v1_EgressNetworkPolicy_To_network_EgressNetworkPolicy(in, out, s)
}

func autoConvert_network_EgressNetworkPolicy_To_v1_EgressNetworkPolicy(in *network.EgressNetworkPolicy, out *EgressNetworkPolicy, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	if err := Convert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec(&in.Spec, &out.Spec, s); err != nil {
		return err
	}
	return nil
}

// Convert_network_EgressNetworkPolicy_To_v1_EgressNetworkPolicy is an autogenerated conversion function.
func Convert_network_EgressNetworkPolicy_To_v1_EgressNetworkPolicy(in *network.EgressNetworkPolicy, out *EgressNetworkPolicy, s conversion.Scope) error {
	return autoConvert_network_EgressNetworkPolicy_To_v1_EgressNetworkPolicy(in, out, s)
}

func autoConvert_v1_EgressNetworkPolicyList_To_network_EgressNetworkPolicyList(in *EgressNetworkPolicyList, out *network.EgressNetworkPolicyList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]network.EgressNetworkPolicy)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_EgressNetworkPolicyList_To_network_EgressNetworkPolicyList is an autogenerated conversion function.
func Convert_v1_EgressNetworkPolicyList_To_network_EgressNetworkPolicyList(in *EgressNetworkPolicyList, out *network.EgressNetworkPolicyList, s conversion.Scope) error {
	return autoConvert_v1_EgressNetworkPolicyList_To_network_EgressNetworkPolicyList(in, out, s)
}

func autoConvert_network_EgressNetworkPolicyList_To_v1_EgressNetworkPolicyList(in *network.EgressNetworkPolicyList, out *EgressNetworkPolicyList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]EgressNetworkPolicy)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_network_EgressNetworkPolicyList_To_v1_EgressNetworkPolicyList is an autogenerated conversion function.
func Convert_network_EgressNetworkPolicyList_To_v1_EgressNetworkPolicyList(in *network.EgressNetworkPolicyList, out *EgressNetworkPolicyList, s conversion.Scope) error {
	return autoConvert_network_EgressNetworkPolicyList_To_v1_EgressNetworkPolicyList(in, out, s)
}

func autoConvert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer(in *EgressNetworkPolicyPeer, out *network.EgressNetworkPolicyPeer, s conversion.Scope) error {
	out.CIDRSelector = in.CIDRSelector
	out.DNSName = in.DNSName
	return nil
}

// Convert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer is an autogenerated conversion function.
func Convert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer(in *EgressNetworkPolicyPeer, out *network.EgressNetworkPolicyPeer, s conversion.Scope) error {
	return autoConvert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer(in, out, s)
}

func autoConvert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer(in *network.EgressNetworkPolicyPeer, out *EgressNetworkPolicyPeer, s conversion.Scope) error {
	out.CIDRSelector = in.CIDRSelector
	out.DNSName = in.DNSName
	return nil
}

// Convert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer is an autogenerated conversion function.
func Convert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer(in *network.EgressNetworkPolicyPeer, out *EgressNetworkPolicyPeer, s conversion.Scope) error {
	return autoConvert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer(in, out, s)
}

func autoConvert_v1_EgressNetworkPolicyRule_To_network_EgressNetworkPolicyRule(in *EgressNetworkPolicyRule, out *network.EgressNetworkPolicyRule, s conversion.Scope) error {
	out.Type = network.EgressNetworkPolicyRuleType(in.Type)
	if err := Convert_v1_EgressNetworkPolicyPeer_To_network_EgressNetworkPolicyPeer(&in.To, &out.To, s); err != nil {
		return err
	}
	return nil
}

// Convert_v1_EgressNetworkPolicyRule_To_network_EgressNetworkPolicyRule is an autogenerated conversion function.
func Convert_v1_EgressNetworkPolicyRule_To_network_EgressNetworkPolicyRule(in *EgressNetworkPolicyRule, out *network.EgressNetworkPolicyRule, s conversion.Scope) error {
	return autoConvert_v1_EgressNetworkPolicyRule_To_network_EgressNetworkPolicyRule(in, out, s)
}

func autoConvert_network_EgressNetworkPolicyRule_To_v1_EgressNetworkPolicyRule(in *network.EgressNetworkPolicyRule, out *EgressNetworkPolicyRule, s conversion.Scope) error {
	out.Type = EgressNetworkPolicyRuleType(in.Type)
	if err := Convert_network_EgressNetworkPolicyPeer_To_v1_EgressNetworkPolicyPeer(&in.To, &out.To, s); err != nil {
		return err
	}
	return nil
}

// Convert_network_EgressNetworkPolicyRule_To_v1_EgressNetworkPolicyRule is an autogenerated conversion function.
func Convert_network_EgressNetworkPolicyRule_To_v1_EgressNetworkPolicyRule(in *network.EgressNetworkPolicyRule, out *EgressNetworkPolicyRule, s conversion.Scope) error {
	return autoConvert_network_EgressNetworkPolicyRule_To_v1_EgressNetworkPolicyRule(in, out, s)
}

func autoConvert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec(in *EgressNetworkPolicySpec, out *network.EgressNetworkPolicySpec, s conversion.Scope) error {
	out.Egress = *(*[]network.EgressNetworkPolicyRule)(unsafe.Pointer(&in.Egress))
	return nil
}

// Convert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec is an autogenerated conversion function.
func Convert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec(in *EgressNetworkPolicySpec, out *network.EgressNetworkPolicySpec, s conversion.Scope) error {
	return autoConvert_v1_EgressNetworkPolicySpec_To_network_EgressNetworkPolicySpec(in, out, s)
}

func autoConvert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec(in *network.EgressNetworkPolicySpec, out *EgressNetworkPolicySpec, s conversion.Scope) error {
	out.Egress = *(*[]EgressNetworkPolicyRule)(unsafe.Pointer(&in.Egress))
	return nil
}

// Convert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec is an autogenerated conversion function.
func Convert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec(in *network.EgressNetworkPolicySpec, out *EgressNetworkPolicySpec, s conversion.Scope) error {
	return autoConvert_network_EgressNetworkPolicySpec_To_v1_EgressNetworkPolicySpec(in, out, s)
}

func autoConvert_v1_HostSubnet_To_network_HostSubnet(in *HostSubnet, out *network.HostSubnet, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.Host = in.Host
	out.HostIP = in.HostIP
	out.Subnet = in.Subnet
	out.EgressIPs = *(*[]string)(unsafe.Pointer(&in.EgressIPs))
	return nil
}

// Convert_v1_HostSubnet_To_network_HostSubnet is an autogenerated conversion function.
func Convert_v1_HostSubnet_To_network_HostSubnet(in *HostSubnet, out *network.HostSubnet, s conversion.Scope) error {
	return autoConvert_v1_HostSubnet_To_network_HostSubnet(in, out, s)
}

func autoConvert_network_HostSubnet_To_v1_HostSubnet(in *network.HostSubnet, out *HostSubnet, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.Host = in.Host
	out.HostIP = in.HostIP
	out.Subnet = in.Subnet
	out.EgressIPs = *(*[]string)(unsafe.Pointer(&in.EgressIPs))
	return nil
}

// Convert_network_HostSubnet_To_v1_HostSubnet is an autogenerated conversion function.
func Convert_network_HostSubnet_To_v1_HostSubnet(in *network.HostSubnet, out *HostSubnet, s conversion.Scope) error {
	return autoConvert_network_HostSubnet_To_v1_HostSubnet(in, out, s)
}

func autoConvert_v1_HostSubnetList_To_network_HostSubnetList(in *HostSubnetList, out *network.HostSubnetList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]network.HostSubnet)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_HostSubnetList_To_network_HostSubnetList is an autogenerated conversion function.
func Convert_v1_HostSubnetList_To_network_HostSubnetList(in *HostSubnetList, out *network.HostSubnetList, s conversion.Scope) error {
	return autoConvert_v1_HostSubnetList_To_network_HostSubnetList(in, out, s)
}

func autoConvert_network_HostSubnetList_To_v1_HostSubnetList(in *network.HostSubnetList, out *HostSubnetList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]HostSubnet)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_network_HostSubnetList_To_v1_HostSubnetList is an autogenerated conversion function.
func Convert_network_HostSubnetList_To_v1_HostSubnetList(in *network.HostSubnetList, out *HostSubnetList, s conversion.Scope) error {
	return autoConvert_network_HostSubnetList_To_v1_HostSubnetList(in, out, s)
}

func autoConvert_v1_NetNamespace_To_network_NetNamespace(in *NetNamespace, out *network.NetNamespace, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.NetName = in.NetName
	out.NetID = in.NetID
	out.EgressIPs = *(*[]string)(unsafe.Pointer(&in.EgressIPs))
	return nil
}

// Convert_v1_NetNamespace_To_network_NetNamespace is an autogenerated conversion function.
func Convert_v1_NetNamespace_To_network_NetNamespace(in *NetNamespace, out *network.NetNamespace, s conversion.Scope) error {
	return autoConvert_v1_NetNamespace_To_network_NetNamespace(in, out, s)
}

func autoConvert_network_NetNamespace_To_v1_NetNamespace(in *network.NetNamespace, out *NetNamespace, s conversion.Scope) error {
	out.ObjectMeta = in.ObjectMeta
	out.NetName = in.NetName
	out.NetID = in.NetID
	out.EgressIPs = *(*[]string)(unsafe.Pointer(&in.EgressIPs))
	return nil
}

// Convert_network_NetNamespace_To_v1_NetNamespace is an autogenerated conversion function.
func Convert_network_NetNamespace_To_v1_NetNamespace(in *network.NetNamespace, out *NetNamespace, s conversion.Scope) error {
	return autoConvert_network_NetNamespace_To_v1_NetNamespace(in, out, s)
}

func autoConvert_v1_NetNamespaceList_To_network_NetNamespaceList(in *NetNamespaceList, out *network.NetNamespaceList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]network.NetNamespace)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_v1_NetNamespaceList_To_network_NetNamespaceList is an autogenerated conversion function.
func Convert_v1_NetNamespaceList_To_network_NetNamespaceList(in *NetNamespaceList, out *network.NetNamespaceList, s conversion.Scope) error {
	return autoConvert_v1_NetNamespaceList_To_network_NetNamespaceList(in, out, s)
}

func autoConvert_network_NetNamespaceList_To_v1_NetNamespaceList(in *network.NetNamespaceList, out *NetNamespaceList, s conversion.Scope) error {
	out.ListMeta = in.ListMeta
	out.Items = *(*[]NetNamespace)(unsafe.Pointer(&in.Items))
	return nil
}

// Convert_network_NetNamespaceList_To_v1_NetNamespaceList is an autogenerated conversion function.
func Convert_network_NetNamespaceList_To_v1_NetNamespaceList(in *network.NetNamespaceList, out *NetNamespaceList, s conversion.Scope) error {
	return autoConvert_network_NetNamespaceList_To_v1_NetNamespaceList(in, out, s)
}
