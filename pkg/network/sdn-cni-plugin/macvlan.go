// +build linux

package main

import (
	"fmt"
	"net"
	"os"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/plugins/pkg/ns"

	"github.com/vishvananda/netlink"
)

func (p *cniPlugin) maybeSetupMacvlan(args *skel.CmdArgs) error {
	netns, ok := os.LookupEnv("CNI_NETNS")
	if !ok {
		// should have caused an error already?
		return nil
	}

	err := ns.WithNetNSPath(netns, func(hostNS ns.NetNS) error {
		macvlan0, err := netlink.LinkByName("macvlan0")
		if err != nil {
			// no macvlan0, so nothing to do
			return nil
		}

		var dsts []*net.IPNet
		err = hostNS.Do(func(ns.NetNS) error {
			// find IPs of the macvlan's parent interface
			parent, err := netlink.LinkByIndex(macvlan0.Attrs().ParentIndex)
			if err != nil {
				return err
			}
			addrs, err := netlink.AddrList(parent, netlink.FAMILY_V4)
			if err != nil {
				return err
			}

			for _, addr := range addrs {
				dsts = append(dsts, &net.IPNet{IP: addr.IP, Mask: net.CIDRMask(32, 32)})
			}

			// find the service CIDR
			tun0, err := netlink.LinkByName("tun0")
			if err != nil {
				return err
			}
			routes, err := netlink.RouteList(tun0, netlink.FAMILY_V4)
			if err != nil {
				return err
			}
			for _, route := range routes {
				// Only grab the serviceCIDR route, not the SCOPE_LINK clusterCIDR route
				if route.Scope != netlink.SCOPE_LINK {
					dsts = append(dsts, route.Dst)
					break
				}
			}

			return nil
		})
		if err != nil {
			return fmt.Errorf("could not determine node routes: %v", err)
		}

		eth0, err := netlink.LinkByName("eth0")
		if err != nil {
			return fmt.Errorf("could not find pod network interface: %v", err)
		}
		routes, err := netlink.RouteList(eth0, netlink.FAMILY_V4)
		if err != nil {
			return err
		}
		var defaultGW net.IP
		for _, route := range routes {
			if route.Dst == nil {
				defaultGW = route.Gw
				break
			}
		}
		if defaultGW == nil {
			return fmt.Errorf("could not find default route")
		}

		for _, dst := range dsts {
			route := &netlink.Route{
				LinkIndex: eth0.Attrs().Index,
				Dst:       dst,
				Gw:        defaultGW,
			}
			if err := netlink.RouteAdd(route); err != nil && !os.IsExist(err) {
				return fmt.Errorf("failed to add route to dst %q via SDN: %v", dst.String(), err)
			}
		}

		return nil
	})
	if err != nil {
		return fmt.Errorf("error setting up macvlan: %v", err)
	} else {
		return nil
	}
}

