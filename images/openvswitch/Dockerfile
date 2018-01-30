#
# This is an openvswitch image meant to enable OpenShift OVS based SDN
#
# The standard name for this image is openshift/openvswitch
#

FROM openshift3/origin-base

MAINTAINER Scott Dodson <sdodson@redhat.com>

COPY scripts/* /usr/local/bin/

RUN yum-config-manager --enable rhel-7-fast-datapath-rpms && \
    INSTALL_PKGS="openvswitch" && \
    yum install -y $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all && \
    chmod +x /usr/local/bin/*

LABEL io.k8s.display-name="OpenShift OpenVSwitch Daemon" \
      io.k8s.description="This is a component of OpenShift and runs an OpenVSwitch daemon process." \
      io.openshift.tags="openshift,openvswitch"
VOLUME /etc/openswitch
ENV HOME /root

# files required to run as a system container
COPY system-container/system-container-wrapper.sh /usr/local/bin/
COPY system-container/config.json.template system-container/service.template /exports/

ENTRYPOINT ["/usr/local/bin/ovs-run.sh"]
