#
# This is an OpenShift node image with integrated OpenvSwitch SDN
# If you do not require OVS SDN you should just use the origin image
#
# The standard name for this image is openshift/node
#

FROM openshift3/origin

# Based on work by: Peter Schiffer <pschiffe@redhat.com>
MAINTAINER Devan Goodwin <dgoodwin@redhat.com>

COPY scripts/* /usr/local/bin/

RUN yum-config-manager --enable rhel-7-server-ose-3.5-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-fast-datapath-rpms && \
    INSTALL_PKGS="origin-sdn-ovs libmnl libnetfilter_conntrack conntrack-tools openvswitch \
      libnfnetlink iptables iproute bridge-utils procps-ng ethtool socat openssl \
      binutils xz kmod-libs kmod sysvinit-tools device-mapper-libs dbus \
      iscsi-initiator-utils" && \
    yum install -y $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all && \
    mkdir -p /usr/lib/systemd/system/origin-node.service.d /usr/lib/systemd/system/docker.service.d && \
    chmod +x /usr/local/bin/* /usr/bin/openshift-* /opt/cni/bin/*

LABEL io.k8s.display-name="OpenShift Node" \
      io.k8s.description="This is a component of OpenShift and contains the software for individual nodes when using SDN." \
      io.openshift.tags="openshift,node"
VOLUME /etc/origin/node
ENV KUBECONFIG=/etc/origin/node/node.kubeconfig

# files required to run as a system container
COPY system-container/system-container-wrapper.sh /usr/local/bin/
COPY system-container/config.json.template system-container/service.template system-container/tmpfiles.template /exports/

ENTRYPOINT [ "/usr/local/bin/origin-node-run.sh" ]
