#debuginfo not supported with Go
%global debug_package %{nil}
# modifying the Go binaries breaks the DWARF debugging
%global __os_install_post %{_rpmconfigdir}/brp-compress

%global gopath      %{_datadir}/gocode
%global import_path github.com/openshift/origin
# The following should only be used for cleanup of sdn-ovs upgrades
%global kube_plugin_path /usr/libexec/kubernetes/kubelet-plugins/net/exec/redhat~openshift-ovs-subnet

# docker_version is the version of docker requires by packages
%global docker_version 1.9.1
# tuned_version is the version of tuned requires by packages
%global tuned_version  2.3
# openvswitch_version is the version of openvswitch requires by packages
%global openvswitch_version 2.3.1
# this is the version we obsolete up to. The packaging changed for Origin
# 1.0.6 and OSE 3.1 such that 'openshift' package names were no longer used.
%global package_refector_version 3.0.2.900
%global golang_version 1.6.2
# %commit and %os_git_vars are intended to be set by tito custom builders provided
# in the .tito/lib directory. The values in this spec file will not be kept up to date.
%{!?commit:
%global commit f10b6aa21a9d3c93b9f6f1db493a8587a3fcd970
}
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# os_git_vars needed to run hack scripts during rpm builds
%{!?os_git_vars:
%global os_git_vars OS_GIT_MINOR=5+ OS_GIT_MAJOR=3 OS_GIT_VERSION=v3.5.5.31.95 OS_GIT_TREE_STATE=clean OS_BUILD_LDFLAGS_DEFAULT_IMAGE_STREAMS=rhel7 OS_IMAGE_PREFIX=registry.access.redhat.com/openshift3/ose OS_GIT_COMMIT=f10b6aa21a
}

%if 0%{?fedora} || 0%{?epel}
%global need_redistributable_set 0
%else
# Due to library availability, redistributable builds only work on x86_64
%ifarch x86_64
%global need_redistributable_set 1
%else
%global need_redistributable_set 0
%endif
%endif
%{!?make_redistributable: %global make_redistributable %{need_redistributable_set}}

%if "%{dist}" == ".el7aos"
%global package_name atomic-openshift
%global product_name Atomic OpenShift
%else
%global package_name origin
%global product_name Origin
%endif

Name:           atomic-openshift
# Version is not kept up to date and is intended to be set by tito custom
# builders provided in the .tito/lib directory of this project
Version:        3.5.5.31.96
Release:        1%{?dist}
Summary:        Open Source Container Management by Red Hat
License:        ASL 2.0
URL:            https://%{import_path}

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif

Source0:        https://%{import_path}/archive/%{commit}/%{name}-%{version}.tar.gz
BuildRequires:  systemd
BuildRequires:  bsdtar
BuildRequires:  golang >= %{golang_version}
BuildRequires:  krb5-devel
BuildRequires:  rsync
Requires:       %{name}-clients = %{version}-%{release}
Requires:       iptables
Obsoletes:      openshift < %{package_refector_version}

#
# The following Bundled Provides entries are populated automatically by the
# OpenShift Origin tito custom builder found here:
#   https://github.com/openshift/origin/blob/master/.tito/lib/origin/builder/
#
# These are defined as per:
# https://fedoraproject.org/wiki/Packaging:Guidelines#Bundling_and_Duplication_of_system_libraries
#
### AUTO-BUNDLED-GEN-ENTRY-POINT

%description
OpenShift is a distribution of Kubernetes optimized for enterprise application
development and deployment. OpenShift adds developer and operational centric
tools on top of Kubernetes to enable rapid application development, easy
deployment and scaling, and long-term lifecycle maintenance for small and large
teams and applications. It provides a secure and multi-tenant configuration for
Kubernetes allowing you to safely host many different applications and workloads
on a unified cluster.

%package master
Summary:        %{product_name} Master
Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Obsoletes:      openshift-master < %{package_refector_version}

%description master
%{summary}

%package tests
Summary: %{product_name} Test Suite
Requires:       %{name} = %{version}-%{release}

%description tests
%{summary}

%package node
Summary:        %{product_name} Node
Requires:       %{name} = %{version}-%{release}
Requires:       docker >= %{docker_version}
Requires:       tuned-profiles-%{name}-node = %{version}-%{release}
Requires:       util-linux
Requires:       socat
Requires:       nfs-utils
Requires:       ethtool
Requires:       device-mapper-persistent-data >= 0.6.2
Requires:       conntrack-tools
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Obsoletes:      openshift-node < %{package_refector_version}

%description node
%{summary}

%package -n tuned-profiles-%{name}-node
Summary:        Tuned profiles for %{product_name} Node hosts
Requires:       tuned >= %{tuned_version}
Obsoletes:      tuned-profiles-openshift-node < %{package_refector_version}

%description -n tuned-profiles-%{name}-node
%{summary}

%package clients
Summary:        %{product_name} Client binaries for Linux
Obsoletes:      openshift-clients < %{package_refector_version}
Requires:       git

%description clients
%{summary}

%if 0%{?make_redistributable}
%package clients-redistributable
Summary:        %{product_name} Client binaries for Linux, Mac OSX, and Windows
Obsoletes:      openshift-clients-redistributable < %{package_refector_version}

%description clients-redistributable
%{summary}
%endif

%package dockerregistry
Summary:        Docker Registry v2 for %{product_name}
Requires:       %{name} = %{version}-%{release}

%description dockerregistry
%{summary}

%package pod
Summary:        %{product_name} Pod

%description pod
%{summary}

%package sdn-ovs
Summary:          %{product_name} SDN Plugin for Open vSwitch
Requires:         openvswitch >= %{openvswitch_version}
Requires:         %{name}-node = %{version}-%{release}
Requires:         bridge-utils
Requires:         ethtool
Requires:         procps-ng
Requires:         iproute
Obsoletes:        openshift-sdn-ovs < %{package_refector_version}

%description sdn-ovs
%{summary}

%package excluder
Summary:   Exclude openshift packages from updates
BuildArch: noarch

%description excluder
Many times admins do not want openshift updated when doing
normal system updates.

%{name}-excluder exclude - No openshift packages can be updated
%{name}-excluder unexclude - Openshift packages can be updated

%package docker-excluder
Summary:   Exclude docker packages from updates
BuildArch: noarch

%description docker-excluder
Certain versions of OpenShift will not work with newer versions
of docker.  Exclude those versions of docker.

%{name}-docker-excluder exclude - No major docker updates
%{name}-docker-excluder unexclude - docker packages can be updated

%prep
%setup -q

%build
%if 0%{make_redistributable}
# Create Binaries for all supported arches
%{os_git_vars} hack/build-cross.sh
%else
# Create Binaries only for building arch
%ifarch x86_64
  BUILD_PLATFORM="linux/amd64"
%endif
%ifarch %{ix86}
  BUILD_PLATFORM="linux/386"
%endif
%ifarch ppc64le
  BUILD_PLATFORM="linux/ppc64le"
%endif
%ifarch %{arm} aarch64
  BUILD_PLATFORM="linux/arm64"
%endif
%ifarch s390x
  BUILD_PLATFORM="linux/s390x"
%endif
OS_ONLY_BUILD_PLATFORMS="${BUILD_PLATFORM}" %{os_git_vars} hack/build-cross.sh
%endif

# Generate man pages
%{os_git_vars} hack/generate-docs.sh

%install

PLATFORM="$(go env GOHOSTOS)/$(go env GOHOSTARCH)"
install -d %{buildroot}%{_bindir}

# Install linux components
for bin in oc openshift dockerregistry
do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 _output/local/bin/${PLATFORM}/${bin} %{buildroot}%{_bindir}/${bin}
done
install -d %{buildroot}%{_libexecdir}/%{name}
install -p -m 755 _output/local/bin/${PLATFORM}/extended.test %{buildroot}%{_libexecdir}/%{name}/

%if 0%{?make_redistributable}
# Install client executable for windows and mac
install -d %{buildroot}%{_datadir}/%{name}/{linux,macosx,windows}
install -p -m 755 _output/local/bin/linux/amd64/oc %{buildroot}%{_datadir}/%{name}/linux/oc
install -p -m 755 _output/local/bin/darwin/amd64/oc %{buildroot}/%{_datadir}/%{name}/macosx/oc
install -p -m 755 _output/local/bin/windows/amd64/oc.exe %{buildroot}/%{_datadir}/%{name}/windows/oc.exe
%endif

# Install pod
install -p -m 755 _output/local/bin/${PLATFORM}/pod %{buildroot}%{_bindir}/

install -d -m 0755 %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

for cmd in \
    kube-apiserver \
    kube-controller-manager \
    kube-proxy \
    kube-scheduler \
    kubelet \
    kubernetes \
    oadm \
    openshift-deploy \
    openshift-docker-build \
    openshift-f5-router \
    openshift-recycle \
    openshift-router \
    openshift-sti-build \
    origin
do
    ln -s openshift %{buildroot}%{_bindir}/$cmd
done

ln -s oc %{buildroot}%{_bindir}/kubectl

install -d -m 0755 %{buildroot}%{_sysconfdir}/origin/{master,node}

# different service for origin vs aos
install -m 0644 contrib/systemd/%{name}-master.service %{buildroot}%{_unitdir}/%{name}-master.service
install -m 0644 contrib/systemd/%{name}-node.service %{buildroot}%{_unitdir}/%{name}-node.service
# same sysconfig files for origin vs aos
install -m 0644 contrib/systemd/origin-master.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}-master
install -m 0644 contrib/systemd/origin-node.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}-node
install -d -m 0755 %{buildroot}%{_prefix}/lib/tuned/%{name}-node-{guest,host}
install -m 0644 contrib/tuned/origin-node-guest/tuned.conf %{buildroot}%{_prefix}/lib/tuned/%{name}-node-guest/tuned.conf
install -m 0644 contrib/tuned/origin-node-host/tuned.conf %{buildroot}%{_prefix}/lib/tuned/%{name}-node-host/tuned.conf

# Install man1 man pages
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -m 0644 docs/man/man1/* %{buildroot}%{_mandir}/man1/

# Patch and install the manpage for tuned profiles on aos
install -d -m 0755 %{buildroot}%{_mandir}/man7
%if "%{dist}" == ".el7aos"
%{__sed} -e 's|origin-node|atomic-openshift-node|g' \
 -e 's|ORIGIN_NODE|ATOMIC_OPENSHIFT_NODE|' \
 contrib/tuned/man/tuned-profiles-origin-node.7 > %{buildroot}%{_mandir}/man7/tuned-profiles-%{name}-node.7
%else
install -m 0644 contrib/tuned/man/tuned-profiles-origin-node.7 %{buildroot}%{_mandir}/man7/tuned-profiles-%{name}-node.7
%endif

mkdir -p %{buildroot}%{_sharedstatedir}/origin


# Install sdn scripts
install -d -m 0755 %{buildroot}%{_sysconfdir}/cni/net.d
pushd pkg/sdn/plugin/sdn-cni-plugin
   install -p -m 0644 80-openshift-sdn.conf %{buildroot}%{_sysconfdir}/cni/net.d
popd
pushd pkg/sdn/plugin/bin
   install -p -m 0755 openshift-sdn-ovs %{buildroot}%{_bindir}/openshift-sdn-ovs
popd
install -d -m 0755 %{buildroot}/opt/cni/bin
install -p -m 0755 _output/local/bin/${PLATFORM}/sdn-cni-plugin %{buildroot}/opt/cni/bin/openshift-sdn
install -p -m 0755 _output/local/bin/${PLATFORM}/host-local %{buildroot}/opt/cni/bin
install -p -m 0755 _output/local/bin/${PLATFORM}/loopback %{buildroot}/opt/cni/bin

install -d -m 0755 %{buildroot}%{_unitdir}/%{name}-node.service.d
install -p -m 0644 contrib/systemd/openshift-sdn-ovs.conf %{buildroot}%{_unitdir}/%{name}-node.service.d/openshift-sdn-ovs.conf

# Install bash completions
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d/
for bin in oadm oc openshift
do
  echo "+++ INSTALLING BASH COMPLETIONS FOR ${bin} "
  %{buildroot}%{_bindir}/${bin} completion bash > %{buildroot}%{_sysconfdir}/bash_completion.d/${bin}
  chmod 644 %{buildroot}%{_sysconfdir}/bash_completion.d/${bin}
done

# Install origin-accounting
install -d -m 755 %{buildroot}%{_sysconfdir}/systemd/system.conf.d/
install -p -m 644 contrib/systemd/origin-accounting.conf %{buildroot}%{_sysconfdir}/systemd/system.conf.d/

# Excluder variables
mkdir -p $RPM_BUILD_ROOT/usr/sbin
%if 0%{?fedora}
  OS_CONF_FILE="/etc/dnf.conf"
%else
  OS_CONF_FILE="/etc/yum.conf"
%endif

# Install openshift-excluder script
sed "s|@@CONF_FILE-VARIABLE@@|${OS_CONF_FILE}|" contrib/excluder/excluder-template > $RPM_BUILD_ROOT/usr/sbin/%{name}-excluder
sed -i "s|@@PACKAGE_LIST-VARIABLE@@|%{name} %{name}-clients %{name}-clients-redistributable %{name}-dockerregistry %{name}-master %{name}-node %{name}-pod %{name}-recycle %{name}-sdn-ovs %{name}-tests tuned-profiles-%{name}-node|" $RPM_BUILD_ROOT/usr/sbin/%{name}-excluder
chmod 0744 $RPM_BUILD_ROOT/usr/sbin/%{name}-excluder

# Install docker-excluder script
sed "s|@@CONF_FILE-VARIABLE@@|${OS_CONF_FILE}|" contrib/excluder/excluder-template > $RPM_BUILD_ROOT/usr/sbin/%{name}-docker-excluder
sed -i "s|@@PACKAGE_LIST-VARIABLE@@|docker*1.13* docker*1.14* docker*1.15* docker*1.16* docker*1.17* docker*1.18* docker*1.19* docker*1.20*|" $RPM_BUILD_ROOT/usr/sbin/%{name}-docker-excluder
chmod 0744 $RPM_BUILD_ROOT/usr/sbin/%{name}-docker-excluder


%files
%doc README.md
%license LICENSE
%{_bindir}/openshift
%{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kube-proxy
%{_bindir}/kube-scheduler
%{_bindir}/kubelet
%{_bindir}/kubernetes
%{_bindir}/oadm
%{_bindir}/openshift-deploy
%{_bindir}/openshift-docker-build
%{_bindir}/openshift-f5-router
%{_bindir}/openshift-recycle
%{_bindir}/openshift-router
%{_bindir}/openshift-sti-build
%{_bindir}/origin
%{_sharedstatedir}/origin
%{_sysconfdir}/bash_completion.d/oadm
%{_sysconfdir}/bash_completion.d/openshift
%defattr(-,root,root,0700)
%dir %config(noreplace) %{_sysconfdir}/origin
%ghost %dir %config(noreplace) %{_sysconfdir}/origin
%ghost %config(noreplace) %{_sysconfdir}/origin/.config_managed
%{_mandir}/man1/oadm*
%{_mandir}/man1/openshift*

%pre
# If /etc/openshift exists and /etc/origin doesn't, symlink it to /etc/origin
if [ -d "%{_sysconfdir}/openshift" ]; then
  if ! [ -d "%{_sysconfdir}/origin"  ]; then
    ln -s %{_sysconfdir}/openshift %{_sysconfdir}/origin
  fi
fi
if [ -d "%{_sharedstatedir}/openshift" ]; then
  if ! [ -d "%{_sharedstatedir}/origin"  ]; then
    ln -s %{_sharedstatedir}/openshift %{_sharedstatedir}/origin
  fi
fi

%files tests
%{_libexecdir}/%{name}
%{_libexecdir}/%{name}/extended.test

%files master
%{_unitdir}/%{name}-master.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-master
%defattr(-,root,root,0700)
%config(noreplace) %{_sysconfdir}/origin/master
%ghost %config(noreplace) %{_sysconfdir}/origin/admin.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/admin.key
%ghost %config(noreplace) %{_sysconfdir}/origin/admin.kubeconfig
%ghost %config(noreplace) %{_sysconfdir}/origin/ca.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/ca.key
%ghost %config(noreplace) %{_sysconfdir}/origin/ca.serial.txt
%ghost %config(noreplace) %{_sysconfdir}/origin/etcd.server.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/etcd.server.key
%ghost %config(noreplace) %{_sysconfdir}/origin/master-config.yaml
%ghost %config(noreplace) %{_sysconfdir}/origin/master.etcd-client.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/master.etcd-client.key
%ghost %config(noreplace) %{_sysconfdir}/origin/master.kubelet-client.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/master.kubelet-client.key
%ghost %config(noreplace) %{_sysconfdir}/origin/master.server.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/master.server.key
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-master.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-master.key
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-master.kubeconfig
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-registry.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-registry.key
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-registry.kubeconfig
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-router.crt
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-router.key
%ghost %config(noreplace) %{_sysconfdir}/origin/openshift-router.kubeconfig
%ghost %config(noreplace) %{_sysconfdir}/origin/policy.json
%ghost %config(noreplace) %{_sysconfdir}/origin/serviceaccounts.private.key
%ghost %config(noreplace) %{_sysconfdir}/origin/serviceaccounts.public.key
%ghost %config(noreplace) %{_sysconfdir}/origin/.config_managed

%post master
%systemd_post %{name}-master.service
# Create master config and certs if both do not exist
if [[ ! -e %{_sysconfdir}/origin/master/master-config.yaml &&
     ! -e %{_sysconfdir}/origin/master/ca.crt ]]; then
  %{_bindir}/openshift start master --write-config=%{_sysconfdir}/origin/master
  # Create node configs if they do not already exist
  if ! find %{_sysconfdir}/origin/ -type f -name "node-config.yaml" | grep -E "node-config.yaml"; then
    %{_bindir}/oadm create-node-config --node-dir=%{_sysconfdir}/origin/node/ --node=localhost --hostnames=localhost,127.0.0.1 --node-client-certificate-authority=%{_sysconfdir}/origin/master/ca.crt --signer-cert=%{_sysconfdir}/origin/master/ca.crt --signer-key=%{_sysconfdir}/origin/master/ca.key --signer-serial=%{_sysconfdir}/origin/master/ca.serial.txt --certificate-authority=%{_sysconfdir}/origin/master/ca.crt
  fi
  # Generate a marker file that indicates config and certs were RPM generated
  echo "# Config generated by RPM at "`date -u` > %{_sysconfdir}/origin/.config_managed
fi


%preun master
%systemd_preun %{name}-master.service

%postun master
%systemd_postun

%files node
%{_unitdir}/%{name}-node.service
%{_sysconfdir}/systemd/system.conf.d/origin-accounting.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-node
%defattr(-,root,root,0700)
%config(noreplace) %{_sysconfdir}/origin/node
%ghost %config(noreplace) %{_sysconfdir}/origin/node/node-config.yaml
%ghost %config(noreplace) %{_sysconfdir}/origin/.config_managed

%post node
%systemd_post %{name}-node.service
# If accounting is not currently enabled systemd reexec
if [[ `systemctl show docker %{name}-node | grep -q -e CPUAccounting=no -e MemoryAccounting=no; echo $?` == 0 ]]; then
  systemctl daemon-reexec
fi

%preun node
%systemd_preun %{name}-node.service

%postun node
%systemd_postun

%files sdn-ovs
%dir %{_unitdir}/%{name}-node.service.d/
%dir %{_sysconfdir}/cni/net.d
%dir /opt/cni/bin
%{_bindir}/openshift-sdn-ovs
%{_unitdir}/%{name}-node.service.d/openshift-sdn-ovs.conf
%{_sysconfdir}/cni/net.d/80-openshift-sdn.conf
/opt/cni/bin/*

%posttrans sdn-ovs
# This path was installed by older packages but the directory wasn't owned by
# RPM so we need to clean it up otherwise kubelet throws an error trying to
# load the directory as a plugin
if [ -d %{kube_plugin_path} ]; then
  rmdir %{kube_plugin_path}
fi

%files -n tuned-profiles-%{name}-node
%license LICENSE
%{_prefix}/lib/tuned/%{name}-node-host
%{_prefix}/lib/tuned/%{name}-node-guest
%{_mandir}/man7/tuned-profiles-%{name}-node.7*

%post -n tuned-profiles-%{name}-node
recommended=`/usr/sbin/tuned-adm recommend`
if [[ "${recommended}" =~ guest ]] ; then
  /usr/sbin/tuned-adm profile %{name}-node-guest > /dev/null 2>&1
else
  /usr/sbin/tuned-adm profile %{name}-node-host > /dev/null 2>&1
fi

%preun -n tuned-profiles-%{name}-node
# reset the tuned profile to the recommended profile
# $1 = 0 when we're being removed > 0 during upgrades
if [ "$1" = 0 ]; then
  recommended=`/usr/sbin/tuned-adm recommend`
  /usr/sbin/tuned-adm profile $recommended > /dev/null 2>&1
fi

%files clients
%license LICENSE
%{_bindir}/oc
%{_bindir}/kubectl
%{_sysconfdir}/bash_completion.d/oc
%{_mandir}/man1/oc*

%if 0%{?make_redistributable}
%files clients-redistributable
%dir %{_datadir}/%{name}/linux/
%dir %{_datadir}/%{name}/macosx/
%dir %{_datadir}/%{name}/windows/
%{_datadir}/%{name}/linux/oc
%{_datadir}/%{name}/macosx/oc
%{_datadir}/%{name}/windows/oc.exe
%endif

%files dockerregistry
%{_bindir}/dockerregistry

%files pod
%{_bindir}/pod

%files excluder
/usr/sbin/%{name}-excluder

%pretrans excluder
# we always want to clear this out using the last
#   versions script.  Otherwise excludes might get left in
if [ -s /usr/sbin/%{name}-excluder ] ; then
  /usr/sbin/%{name}-excluder unexclude
fi

%posttrans excluder
# we always want to run this after an install or update
/usr/sbin/%{name}-excluder exclude

%preun excluder
# If we are the last one, clean things up
if [ "$1" -eq 0 ] ; then
  /usr/sbin/%{name}-excluder unexclude
fi

%files docker-excluder
/usr/sbin/%{name}-docker-excluder

%pretrans docker-excluder
# we always want to clear this out using the last
#   versions script.  Otherwise excludes might get left in
if [ -s /usr/sbin/%{name}-docker-excluder ] ; then
  /usr/sbin/%{name}-docker-excluder unexclude
fi

%posttrans docker-excluder
# we always want to run this after an install or update
/usr/sbin/%{name}-docker-excluder exclude

%preun docker-excluder
# If we are the last one, clean things up
if [ "$1" -eq 0 ] ; then
  /usr/sbin/%{name}-docker-excluder unexclude
fi

%changelog
* Sun Mar 10 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.96-1
- 

* Sun Mar 03 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.95-1
- 

* Sun Feb 24 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.94-1
- 

* Sun Feb 17 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.93-1
- 

* Sun Feb 10 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.92-1
- 

* Sun Feb 03 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.91-1
- 

* Sun Jan 27 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.90-1
- 

* Sun Jan 20 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.89-1
- 

* Sun Jan 06 2019 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.88-1
- 

* Sun Dec 30 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.87-1
- 

* Sun Dec 23 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.86-1
- 

* Sun Dec 16 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.85-1
- 

* Sun Dec 09 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.84-1
- 

* Sun Dec 02 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.83-1
- UPSTREAM: 44962: Remove misleading error from CronJob controller when it
  can't find parent UID (maszulik@redhat.com)

* Sun Nov 25 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.82-1
- 

* Sun Nov 18 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.81-1
- Don't allow pods to send VXLAN packets out of the SDN (danw@redhat.com)

* Wed Nov 14 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.80-1
- UPSTREAM: 00000: Verify backend upgrade (deads@redhat.com)

* Sun Nov 11 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.79-1
- 

* Sun Nov 04 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.78-1
- 

* Sun Oct 28 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.77-1
- 

* Sun Oct 21 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.76-1
- 

* Sun Oct 14 2018 AOS Automation Release Team <aos-team-art@redhat.com> 3.5.5.31.75-1
- [3.5] bump(github.com/evanphx/json-patch):
  f195058310bd062ea7c754a834f0ff43b4b63afb (eparis@redhat.com)
- bump(github.com/evanphx/json-patch): 94e38aa1586e8a6c8a75770bddf5ff84c48a106b
  (eparis@redhat.com)

* Fri Jun 08 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.74-1
- 

* Thu Jun 07 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.73-1
- 

* Thu Jun 07 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.72-1
- 

* Thu Jun 07 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.71-1
- 

* Thu Jun 07 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.70-1
- [3.5] Prevent s2i build containers from running as root user
  (adam.kaplan@redhat.com)

* Thu May 10 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.69-1
- 

* Wed May 09 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.68-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 75e008b
  (jupierce@redhat.com)
- UPSTREAM: 61480: Fix mounting of unix sockets in subpaths
  (hekumar@redhat.com)

* Thu Apr 12 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.67-1
- UPSTREAM: <carry> prevent save-artifact tar extraction from overwriting files
  outside the working dir (bparees@redhat.com)

* Thu Mar 29 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.66-1
- 

* Wed Mar 28 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.65-1
- UPSTREAM: 00000: set IdleConnTimeout for etcd2 client (jliggitt@redhat.com)
- switch reversed old/new objects to validation (deads@redhat.com)
- image-strategy: unset image signature annotations (miminar@redhat.com)

* Wed Mar 21 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.64-1
- 

* Fri Mar 16 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.63-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 888ab08
  (jupierce@redhat.com)
- UPSTREAM: 58433: lstat with abs path of parent instead of '/..'
  (jsafrane@redhat.com)
- UPSTREAM: 61080: Detect backsteps correctly in base path detection
  (jsafrane@redhat.com)

* Sat Mar 10 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.62-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 7b466e9
  (jupierce@redhat.com)
- Make remoteBlobGetterService thread-safe (obulatov@redhat.com)
- UPSTREAM: 60342: Fix nested volume mounts for read-only API data volumes
  (joesmith@redhat.com)
- UPSTREAM: 58720: Ensure that the runtime mounts RO volumes read-only
  (joesmith@redhat.com)
- UPSTREAM: 57422: Rework method of updating atomic-updated data volumes
  (joesmith@redhat.com)
- UPSTREAM: carry: Lock subPath volumes (jsafrane@redhat.com)

* Fri Feb 16 2018 Justin Pierce <jupierce@redhat.com> 3.5.5.31.61-1
- Fixing bad Dockerfile reconcile (adammhaile@gmail.com)
- Better reconcile of Dockerfiles (adammhaile@gmail.com)

* Sun Jan 28 2018 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.60-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 51036f8
  (smunilla@redhat.com)

* Wed Jan 24 2018 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.59-1
- Adding pod Dockerfile.rhel7 to match old distgit (adammhaile@gmail.com)
- UPSTREAM: <carry>: Fix to avoid REST API calls at log level 2
  (sjenning@redhat.com)

* Thu Jan 04 2018 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.58-1
- 

* Wed Jan 03 2018 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.57-1
- 

* Thu Dec 28 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.56-1
- 

* Tue Dec 26 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.55-1
- 

* Thu Dec 21 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.54-1
- 

* Tue Dec 19 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.53-1
- 

* Thu Dec 14 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.52-1
- 

* Wed Dec 13 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.51-1
- 

* Thu Dec 07 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.50-1
- 

* Wed Dec 06 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.49-1
- 

* Mon Dec 04 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.48-1
- UPSTREAM: 56503: MustRunAsNonRoot should reject a pod if it has non-numeric
  USER (vsemushi@redhat.com)
- Version prefix matters when sorting tags names (miminar@redhat.com)
- Fix prioritizing of semver equal tags (obulatov@redhat.com)
- Fixed conversion of ImageStreamStatus.Tags (miminar@redhat.com)
- BACKPORT PR13897 Sanitize certificates from routes in the router
  (jtanenba@redhat.com)

* Thu Nov 09 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.47-1
- 

* Thu Nov 09 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.46-1
- 

* Thu Nov 09 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.45-1
- 

* Wed Nov 08 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.44-1
- 

* Tue Nov 07 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.43-1
- 

* Thu Nov 02 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.42-1
- 

* Tue Oct 31 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.41-1
- 

* Thu Oct 26 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.40-1
- 

* Tue Oct 24 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.39-1
- UPSTREAM: 44781: Ensure desired state of world populator runs before volume
  reconstructor (mawong@redhat.com)

* Thu Oct 19 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.38-1
- UPSTREAM: 48613: proxy/userspace: honor listen IP address as host IP if given
  (jtanenba@redhat.com)
- Print more details when network diagnostics test setup fails
  (rpenta@redhat.com)
- Bug 1481147 - Fix default pod image for network diagnostics
  (rpenta@redhat.com)
- UPSTREAM: <carry>: fix 45352 backport (ravisantoshgudimetla@gmail.com)

* Tue Oct 17 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.37-1
- UPSTREAM: 38691: Only create the symlink when container log path exists
  (sjenning@redhat.com)

* Thu Oct 12 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.36-1
- Retry image stream updates when pruning images (maszulik@redhat.com)

* Tue Oct 10 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.35-1
- UPSTREAM: 53135: Fixed counting of unbound PVCs towards limit of attached
  volumes. (jsafrane@redhat.com)

* Fri Oct 06 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.34-1
- 

* Thu Oct 05 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.33-1
- 

* Thu Oct 05 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.32-1
- Test for bug 1487408 (obulatov@redhat.com)
- Pruning should take all the images into account (agladkov@redhat.com)
- Fix tests (obulatov@redhat.com)
- UPSTREAM: <carry>: fix udp service blackhole problem when number of backends
  changes from 0 to non-0 (danw@redhat.com)
- UPSTREAM: docker/distribution: 2219: Fix forwarded logic (miminar@redhat.com)
- Require conntrack-tools in node package (danw@redhat.com)
- UPSTREAM: 48613: proxy/userspace: honor listen IP address as host IP if given
  (dcbw@redhat.com)

* Tue Oct 03 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.31-1
- Prevent panic when proxy is disabled in node start (amcdermo@redhat.com)
- UPSTREAM: 45352: Pod (Anti)affinity shouldn't be respected across namespaces.
  (ravisantoshgudimetla@gmail.com)

* Thu Sep 28 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.30-1
- Allow no-op pod updates (jliggitt@redhat.com)

* Tue Sep 26 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.29-1
- UPSTREAM: google/cadvisor: 1700: Reduce log spam when unable to get network
  stats (sjenning@redhat.com)

* Tue Sep 26 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.28-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 4fc84fc
  (smunilla@redhat.com)
- UPSTREAM: coreos/etcd: 8519: Fix for etcd client oneshot cluster member
  cycling (rrati@redhat.com)
- UPSTREAM: 52675: Fix FC WaitForAttach not mounting a volume
  (hchen@redhat.com)
- UPSTREAM: 52687: Refactoring and improvements for iSCSI and FC storage
  plugins (hchen@redhat.com)
- UPSTREAM: 52691: FC plugin: Return target wwn + lun at GetVolumeName()
  (hchen@redhat.com)
- updated generated completions (miminar@redhat.com)
- Image pruner: Determine protocol just once (miminar@redhat.com)
- Bug 1450291 - Improve logs in image pruning (maszulik@redhat.com)
- Prefer secure connection during image pruning (miminar@redhat.com)
- proxy: honor BindAddress for the iptables proxy (dcbw@redhat.com)
- Bug 1421643 - Fix network diagnostics timeouts (rpenta@redhat.com)

* Tue Sep 05 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.27-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 8e62f9a
  (smunilla@redhat.com)
- UPSTREAM: 49640: Run mount in its own systemd scope (jsafrane@redhat.com)

* Thu Aug 31 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.26-1
- 

* Tue Aug 29 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.25-1
- 

* Thu Aug 24 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.24-1
- NetworkCheck diagnostic: create projects with empty nodeselector
  (lmeyer@redhat.com)

* Tue Aug 22 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.23-1
- UPSTREAM: 45601: util/iptables: fix cross-build failures due to
  syscall.Flock() (dcbw@redhat.com)
- UPSTREAM: 44895: util/iptables: grab iptables locks if iptables-restore
  doesn't support --wait (dcbw@redhat.com)
- UPSTREAM: 43575: util/iptables: check for and use new iptables-restore 'wait'
  argument (dcbw@redhat.com)

* Thu Aug 17 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.22-1
- 

* Tue Aug 15 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.21-1
- 

* Thu Aug 10 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.20-1
- 

* Tue Aug 08 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.19-1
- 

* Tue Aug 08 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.18-1
- 

* Tue Aug 08 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.17-1
- 

* Mon Aug 07 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.16-1
- 

* Fri Aug 04 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.15-1
- 

* Fri Aug 04 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.14-1
- 

* Fri Aug 04 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.13-1
- 

* Thu Aug 03 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.12-1
- Fix panic when tag is nil when creating istag (maszulik@redhat.com)

* Thu Aug 03 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.11-1
- UPSTREAM : 45346: Don't try to attach volumes which are already attached to
  other nodes (hchen@redhat.com)
- UPSTREAM : 48940: support fc volume attach and detach (hchen@redhat.com)

* Wed Aug 02 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.10-1
- Backport of 3.6 container networking test (cewong@redhat.com)

* Tue Aug 01 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.9-1
- 

* Thu Jul 27 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.8-1
- UPSTREAM: 49420: Fix c-m crash while verifying attached volumes
  (hekumar@redhat.com)

* Tue Jul 25 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.7-1
- Update lastTriggeredImage if not set when instantiating DCs
  (mkargaki@redhat.com)
- Extended test for registry garbage collector (miminar@redhat.com)
- Exit normally if registry's storage is empty (miminar@redhat.com)
- Add -prune option to dockerregistry (obulatov@redhat.com)
- UPSTREAM: docker/distribution: 2299: Fix signalling Wait in regulator.enter
  (obulatov@redhat.com)

* Tue Jul 18 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.6-1
- UPSTREAM: 38865: Change mkfs arguments (hekumar@redhat.com)

* Thu Jul 13 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.5-1
- 

* Tue Jul 11 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.4-1
- UPSTREAM: 48733: Never prevent deletion of resources as part of namespace
  lifecycle (jliggitt@redhat.com)

* Thu Jul 06 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.3-1
- 

* Tue Jul 04 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.2-1
- 

* Fri Jun 30 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.1-1
- 

* Thu Jun 29 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31.0-1
- 

* Tue Jun 27 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.31-1
- Don't allow deleted routes in resync list (pcameron@redhat.com)
- Add then resync then Delete cause Pop() panic (pcameron@redhat.com)
- bump(github.com/openshift/source-to-image):
  84c6a2de2a672571fd690d4f4857e6f41ea8d9d3 (cewong@redhat.com)

* Fri Jun 23 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.30-1
- 

* Thu Jun 22 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.29-1
- 

* Tue Jun 20 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.28-1
- Change the MAC addresses to be generated based on IP (dcbw@redhat.com)
- UPSTREAM: <carry>: Add auto_unmount mount option for glusterfs fuse mount
  (hchiramm@redhat.com)
- UPSTREAM: 47516: Fix getInstancesByNodeNames for AWS (hekumar@redhat.com)
- Use GC rather than refcounting for VNID policy rules (danw@redhat.com)
- ovs: split out flow parsing code, expose API, and parse actions
  (dcbw@redhat.com)
- UPSTREAM: 42949: recycle pod can't get the event since channel closed
  (mawong@redhat.com)
- Bug 1454535 - Use created project name over namespace name in project
  template (mfojtik@redhat.com)
- UPSTREAM: 42275: discovery restmapping should always prefer /v1
  (mfojtik@redhat.com)

* Thu Jun 15 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.27-1
- UPSTREAM: 43878: Delete EmptyDir volume directly instead of renaming the
  directory (hchen@redhat.com)

* Tue Jun 13 2017 Jenkins CD Merge Bot <smunilla@redhat.com> 3.5.5.26-1
- Auto generated: bash completions for network diagnostics (rpenta@redhat.com)
- Provide better error message when network diags test pod fails
  (rpenta@redhat.com)
- Bug 1417641 - Make network diagnostic test pod image/protocol/port
  configurable (rpenta@redhat.com)
- Bug 1439142 - Use openshift/origin-deployer image instead of openshift/hello-
  openshift as network diagnostic test pod. (rpenta@redhat.com)
- UPSTREAM: 46371: reset resultRun on pod restart (sjenning@redhat.com)

* Thu Jun 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.25-1
- 

* Tue Jun 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.24-1
- Set layer size whether it found in cache or not (obulatov@redhat.com)
- UPSTREAM: 44439: controller: fix saturation check in Deployments
  (mkargaki@redhat.com)
- policy urls should support partitions (rchopra@redhat.com)
- Fix go tests; policy requests now include the partition paths
  (rchopra@redhat.com)
- F5 router partition path changes:   o Use fully qualified names so that there
  is no defaulting to /Common     and need to have all the referenced objects
  in the same partition,     otherwise F5 has reference errors across
  partitions.   o Fix policy partition path + rework and ensure we check the
  vserver     which is inside the partition we are configured in.   o Comment
  re: delete errors.   o Bug fixes.   o F5 unit test changes for supporting
  partition paths. (smitram@gmail.com)

* Fri Jun 02 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.23-1
- Use base64url to decode id_token (jliggitt@redhat.com)

* Thu Jun 01 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.22-1
- UPSTREAM: 46463: AWS: consider instances of all states in DisksAreAttached,
  not just "running" (mawong@redhat.com)
- UPSTREAM: 44295: Azure disk: dealing with missing disk probe
  (hchen@redhat.com)

* Tue May 30 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.21-1
- [3.5] Shuffle endpoints function for the router template : bz1447115
  (rchopra@redhat.com)

* Thu May 25 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.20-1
- [3.5] back-port: Set the log level for iptables rule dump to 5
  (bbennett@redhat.com)

* Tue May 23 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.19-1
- Change default arp cache size on nodes (pcameron@redhat.com)
- UPSTREAM: 45623: Don't attempt to make and chmod subPath if it already exists
  (mawong@redhat.com)
- generated code (hchen@redhat.com)
- UPSTREAM: 39928: Add portals field to iscsi volume source to achieve
  multipathing. (hchen@redhat.com)

* Thu May 18 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.18-1
- 

* Thu May 18 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.17-1
- [Backport to 3.5] Fix for bz1438402 (rchopra@redhat.com)
- [Upstream Backport][3.5] For the auto generated kube api-server service, the
  service spec re-uses the service port itself. The endpoint is created
  correctly using public port. Fix the service also because there are some
  plugin controllers that react to service spec itself. Upstream commit id:
  440dcd3675989fe91263d48ef6b4a2b3db6753d2 Upstream PR:
  https://github.com/kubernetes/kubernetes/pull/41115 (rchopra@redhat.com)

* Tue May 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.16-1
- UPSTREAM: 45286: detach the volume when pod is terminated
  (hekumar@redhat.com)
- Add backward compatibility for the old EgressNetworkPolicy "0.0.0.0/32" bug
  (danw@redhat.com)
- Use docker image reference from ImageStream (obulatov@redhat.com)
- Remove GetFake*Handler (obulatov@redhat.com)
- Replace io.ReadSeeker by simple []byte buffer (obulatov@redhat.com)
- Add tests for ManifestService (obulatov@redhat.com)
- Remove global DefaultRegistryClient (obulatov@redhat.com)
- Add stateful reactors for fake client (obulatov@redhat.com)
- Add function newTestRepository (obulatov@redhat.com)

* Thu May 11 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.15-1
- UPSTREAM: 41626: kubelet volume cleanup does not distinguish error
  (decarr@redhat.com)

* Tue May 09 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.14-1
- Fix NATting of external traffic with ovs-networkpolicy (danw@redhat.com)

* Thu May 04 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.13-1
- UPSTREAM: 37698: Make kubelet never delete files on mounted filesystems
  (hchen@redhat.com)
- UPSTREAM: 44462: 44489: fix selfLink for cluster-scoped resources
  (andy.goldstein@gmail.com)

* Tue May 02 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.12-1
- 

* Mon May 01 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.11-1
- Match subpaths correctly when path contains trailing slash
  (jliggitt@redhat.com)

* Wed Apr 26 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.10-1
- proxy/hybrid: add locking around userspace map (dcbw@redhat.com)
- UPSTREAM: 43375: Set permission for volume subPaths (pmorie@redhat.com)
- sdn: fix initialization order to prevent crash on node startup
  (dcbw@redhat.com)
- Fix service IP validation to handle "ClusterIP: None" (danw@redhat.com)
- sdn: fix single-node-cluster local multicast delivery (dcbw@redhat.com)
- Pullthrough broken registry server (agladkov@redhat.com)

* Mon Apr 24 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.9-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 7029ade
  (tdawson@redhat.com)
- UPSTREAM: 39732: Attach/detach should recover from a crash
  (tsmetana@redhat.com)
- UPSTREAM: 44452: Implement LRU for AWS device allocator (jsafrane@redhat.com)
- UPSTREAM: 42033: reconcile attach/detach state of world with missing pods
  periodically (jsafrane@redhat.com)
- UPSTREAM: 44566: WaitForCacheSync before running attachdetach controller
  (mawong@redhat.com)

* Thu Apr 20 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.8-1
- Increase max request size for HAProxy to be comparable to cloud LBs
  (ccoleman@redhat.com)
- [3.5] Add web diag endpoint to the F5 and haproxy routers
  (bbennett@redhat.com)
- UPSTREAM: 41306: Impement bulk polling of volumes (jsafrane@redhat.com)

* Tue Apr 18 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.7-1
- Prevent the router from deadlocking itself when calling Commit()
  (bbennett@redhat.com)
- Specify the default registry for the OSE images (skuznets@redhat.com)
- Cherry-pick: Fix namespace sync (marun@redhat.com)

* Thu Apr 13 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.6-1
- ensure the next build is kicked off when a build completes
  (bparees@redhat.com)
- Restrict packages from CentOS to OVS only (skuznets@redhat.com)
- Install OpenVSwitch from the CentOS PaaS SIG Repos (skuznets@redhat.com)
- Prevent new project creation with openshift/kubernetes/kube prefixes
  (jliggitt@redhat.com)

* Sat Apr 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.5-1
- Fix image pruning with both strong & weak refs (maszulik@redhat.com)

* Fri Apr 07 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.4-1
- Fix race between ovsdb-server.service and node service (sdodson@redhat.com)

* Thu Apr 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.3-1
- RestrictUsersAdmission: allow SA with implicit NS (miciah.masters@gmail.com)

* Wed Apr 05 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5.2-1
- Add architecture type to the os::build::rpm::format_nvr function
  (jhadvig@redhat.com)
- Let the name of the RPM package being built vary (skuznets@redhat.com)
- Break out RPM version logic from RPM build script (skuznets@redhat.com)
- enable release repo (jhadvig@redhat.com)
- Update namespace finalizer to delete RoleBindingRestrictions
  (mkhan@redhat.com)

* Wed Apr 05 2017 Troy Dawson <tdawson@redhat.com> 3.5.5.1-1
- Update OAuth grant flow tests (jliggitt@redhat.com)
- Redirect to relative subpath for approval, relative parent path on success
  (jliggitt@redhat.com)
- Update namespace finalizer to delete RoleBindingRestrictions
  (mkhan@redhat.com)
- BACKPORT PR13494 change the router eventqueue key function
  (jtanenba@redhat.com)

* Thu Mar 23 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.5-1
- 

* Thu Mar 23 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.4-1
- 

* Thu Mar 23 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.3-1
- 

* Wed Mar 22 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.2-1
- Gather all rpms for the repo creation (sdodson@redhat.com)

* Mon Mar 20 2017 Troy Dawson <tdawson@redhat.com> 3.5.1-1
- Changing versioning scheme for Openshift Online

* Fri Mar 17 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.55-1
- Remove the excluders origin-excluder (sdodson@redhat.com)

* Thu Mar 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.54-1
- Remove need for docker in build-images, use multi-tag (ccoleman@redhat.com)
- Fail if an image fails the build (ccoleman@redhat.com)
- [1.5] Exclude list cleans up properly (#1430929) (tdawson@redhat.com)
- UPSTREAM: 40417: Always detach volumes in operator executor
  (hekumar@redhat.com)

* Wed Mar 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.53-1
- UPSTREAM: 41436: Fix bug in status manager TerminatePod (decarr@redhat.com)

* Tue Mar 14 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.52-1
- 

* Mon Mar 13 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.51-1
- UPSTREAM: 42973: Fix selinux support in vsphere (gethemant@gmail.com)
- Accept the `$JUNIT_REPORT` flag in networking tests (skuznets@redhat.com)
- Use a very high patch number on RPM release builds (skuznets@redhat.com)
- Generate jUnit XML reports from hack/test-end-to-end.sh (skuznets@redhat.com)
- DRY out `os::cmd` jUnit generation, improve logic (skuznets@redhat.com)
- Disable local fsgroup quota test when not using XFS (skuznets@redhat.com)
- Reorder extended startup to yield jUnit with TEST_ONLY (skuznets@redhat.com)
- Always run extended tests with `-v -noColor` (skuznets@redhat.com)
- When no jUnit suites are requested, don't merge them (skuznets@redhat.com)
- Revert "Fix of BUG 1405440" (pcameron@redhat.com)
- Test fixes to the haproxy container on overlayfs (ccoleman@redhat.com)
- Fix a bug in the origin/node image with trailing slash (ccoleman@redhat.com)
- CGO_ENABLED prevents build cache reuse (ccoleman@redhat.com)
- UPSTREAM: 41226: Fix for detach volume when node is not present/ powered off
  (eboyd@redhat.com)
- UPSTREAM: 41217: Fix wrong VM name is retrieved by the vSphere Cloud Provider
  (eboyd@redhat.com)
- UPSTREAM: 40693: fix for vSphere DeleteVolume (eboyd@redhat.com)
- UPSTREAM: 39757: Fix space in volumePath in vSphere (eboyd@redhat.com)
- UPSTREAM: 39754: Fix fsGroup to vSphere (eboyd@redhat.com)
- UPSTREAM: 39752: Fix panic in vSphere cloud provider (eboyd@redhat.com)
- UPSTREAM: 39751: Changed default scsi controller type (eboyd@redhat.com)
- Insecure istag allows for insecure transport (miminar@redhat.com)
- Improve error message in image api helper (miminar@redhat.com)
- Do the manifest verification just once (miminar@redhat.com)
- Allow remote blob access checks only for manifest PUT (miminar@redhat.com)
- Cache imagestream and images during a handling of a single request
  (miminar@redhat.com)
- UPSTREAM: 42622: Preserve custom etcd prefix compatibility for etcd3
  (mkhan@redhat.com)

* Thu Mar 09 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.50-1
- 

* Wed Mar 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.49-1
- 

* Wed Mar 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.48-1
- 

* Wed Mar 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.47-1
- 

* Wed Mar 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.46-1
- Fix of BUG 1405440 (yhlou@travelsky.com)

* Tue Mar 07 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.45-1
- Allow control over TLS version and ciphers for docker-registry
  (jliggitt@redhat.com)

* Mon Mar 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.44-1
- Fix cookies for reencrypt routes with InsecureEdgeTerminationPolicy "Allow"
  (jtanenba@redhat.com)

* Mon Mar 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.43-1
- 

* Mon Mar 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.42-1
- 

* Mon Mar 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.41-1
- 

* Mon Mar 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.40-1
- node/sdn: make /var/lib/cni persistent to ensure IPAM allocations stick
  around across node restart (dcbw@redhat.com)
- make ciphers/tls version configurable (jliggitt@redhat.com)
- Work around docker race condition when running build post commit hooks.
  (jminter@redhat.com)
- UPSTREAM: 42337: Plumb cipher/tls version serving options
  (jliggitt@redhat.com)

* Fri Mar 03 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.39-1
- 

* Fri Mar 03 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.38-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 0c5b53c
  (tdawson@redhat.com)
- No failure reason displayed when build failed using invalid contextDir
  (cdaley@redhat.com)
- cluster up: warn on error parsing Docker version (cewong@redhat.com)
- Update Vagrantfile (dmcphers@redhat.com)
- Update Vagrantfile (dmcphers@redhat.com)
- Output VXLAN multicast flow in sorted order (danw@redhat.com)
- Retry OVS flow checks a few times if they fail (danw@redhat.com)
- Add stateful sets permissions to disruption controller (jliggitt@redhat.com)
- bump(github.com/openshift/source-to-image):
  431c81eac49eb43df80e629a511d80d6eca5bf13 (bparees@redhat.com)
- UPSTREAM: 42294: fix rsListerSynced and podListerSynced for
  DeploymentController (maszulik@redhat.com)
- Change logging deployer image name from 'logging-deployment' to 'logging-
  deployer' (cewong@redhat.com)
- Use posttrans for docker-excluder (#1404193) (tdawson@redhat.com)
- UPSTREAM: 41864: Allow 'kubectl drain --force' to remove orphaned pods
  (marun@redhat.com)

* Wed Mar 01 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.37-1
- 

* Wed Mar 01 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.36-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 79636c1
  (tdawson@redhat.com)
- provider recorder to attach detach controller (hchen@redhat.com)
- Necessary origin updates (maszulik@redhat.com)
- UPSTREAM: 40301: present request header cert CA (maszulik@redhat.com)
- UPSTREAM: revert: 15aaac7f8391a1e0514f80e6450f4bf12c0db191: <drop>: add
  ExtraClientCACerts to SecureServingInfo" (maszulik@redhat.com)
- Do not exclude the excluder for atomic-openshift (tdawson@redhat.com)
- UPSTREAM: 39825: Make PDBs represent percentage in StatefulSet
  (mfojtik@redhat.com)
- Update the reconciler sync period in master_config_test (mfojtik@redhat.com)
- UPSTREAM: 40903: Set docker opt separator correctly for SELinux options
  (maszulik@redhat.com)
- UPSTREAM: revert: 9f81f6f: <carry>: Change docker security opt separator to
  be compatible with 1.11+ (maszulik@redhat.com)
- UPSTREAM: 42097: Enqueue controllers after minreadyseconds when all pods are
  ready (maszulik@redhat.com)
- UPSTREAM: 40625: controller: old pods should block deployment completeness
  (mfojtik@redhat.com)
- UPSTREAM: 37093: Endpoints with TolerateUnready annotation, should list Pods
  in state terminating (maszulik@redhat.com)
- UPSTREAM: 41366: Change default reconciler sync period to 1 minute
  (mfojtik@redhat.com)
- UPSTREAM: 41455: Fix AWS device allocator to only use valid device names
  (mfojtik@redhat.com)
- UPSTREAM: 38818: Add sequential allocator for device names in AWS
  (mfojtik@redhat.com)
- UPSTREAM: 42178: stop spamming logs on restart of server (decarr@redhat.com)
- backup and remove keys during migration (sjenning@redhat.com)
- add migration script to fix etcd paths (sjenning@redhat.com)
- UPSTREAM: 40553: Adjust global log limit to 1ms (pweil@redhat.com)
- UPSTREAM: 40497: Make HandleError prevent hot-loops (pweil@redhat.com)
- UPSTREAM: 40935: Plumb subresource through subjectaccessreview
  (pweil@redhat.com)
- UPSTREAM: 38855: Fix variable shadowing in exponential backoff when deleting
  volumes (pweil@redhat.com)
- UPSTREAM: 38909: Add path exist check in getPodVolumePathListFromDisk
  (pweil@redhat.com)
- UPSTREAM: 38746: recognize eu-west-2 region (pweil@redhat.com)

* Mon Feb 27 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.35-1
- Use DefaultImagePrefix instead of hardcoded 'openshift/origin' for network
  diagnostic image. (rpenta@redhat.com)
- Auto generated: docs/bash completions for network diagnostic pod image option
  (rpenta@redhat.com)
- Make network diagnostic pod image configurable (rpenta@redhat.com)
- Bug 1421643 - Use existing openshift/origin image instead of new openshift
  /diagnostics-deployer (rpenta@redhat.com)
- Sync etcd endpoints during lease acquistion (agoldste@redhat.com)
- update guest profile with new arp tuning missed in
  https://github.com/openshift/origin/pull/13034 (jeder@redhat.com)
- Verify manifest with remote layers (agladkov@redhat.com)
- Don't overwrite /usr/local/bin with a file (sdodson@redhat.com)
- tito: generate man pages (mkargaki@redhat.com)
- Remove redundant docs (mkargaki@redhat.com)
- Check out generated docs (mkargaki@redhat.com)
- Stop checking in generated docs (mkargaki@redhat.com)

* Fri Feb 24 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.34-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 740f6e4
  (tdawson@redhat.com)
- Bug 1422376: Fix resolving ImageStreamImage latest tag (mfojtik@redhat.com)
- prevent build updates from reverting the build phase (bparees@redhat.com)
- Bug 1425706 - protect from nil tlsConfig. (maszulik@redhat.com)
- to fix bugzilla 1424946 (maszulik@redhat.com)
- SCC review client: generated code (salvatore-dario.minonne@amadeus.com)
- SCC review client: fix bugzilla 1424946 (salvatore-dario.minonne@amadeus.com)
- fix bugzilla 1421616 and 1421570 (salvatore-dario.minonne@amadeus.com)
- PSP reviews: client (salvatore-dario.minonne@amadeus.com)

* Thu Feb 23 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.33-1
- new package built with tito

* Mon Feb 20 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.32-1
- UPSTREAM: 41658: Fix cronjob controller panic on status update failure
  (maszulik@redhat.com)
- add oc expose -h explanation on generator (jvallejo@redhat.com)
- Have make_redistributable changable via the command line.
  (tdawson@redhat.com)
- improve flag description; add warning msg (jvallejo@redhat.com)
- generated: CLI docs and completions (ccoleman@redhat.com)
- Support local template transformation in process (ccoleman@redhat.com)
- Ensure RPMs are only build from clean git trees (skuznets@redhat.com)
- Add logging to bluegreen-pipeline.yaml to help diagnose flake Rewrite blue-
  green pipeline extended test to avoid hang on error (jminter@redhat.com)
- add service catalog metadata to templates (bparees@redhat.com)
- add closure that guarantees mutex unlock in loop (jvallejo@redhat.com)
- (WIP) Fixing build reason getting wiped out by race condition
  (cdaley@redhat.com)
- allow namespace specification via parameter in templates (bparees@redhat.com)
- UPSTREAM: 39998: Cinder volume attacher: use instanceID instead of NodeID
  when verifying attachment (jsafrane@redhat.com)
- Change all aarch64 references to arm64 (tdawson@redhat.com)
- inform that port is required as part of set-probe error when port missing
  (jvallejo@redhat.com)

* Fri Feb 17 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.31-1
- do not remove non-existent packages (bparees@redhat.com)
- Dump router logs for debugging purposes in the scoped and weighted extended
  tests. (smitram@gmail.com)

* Thu Feb 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.30-1
- Fix NetworkPolicies allowing from all to *some* (not all) (danw@redhat.com)

* Thu Feb 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.29-1
- 

* Thu Feb 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.28-1
- 

* Thu Feb 16 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.27-1
- deployment: add unit test to exercise the watch restart (mfojtik@redhat.com)
- deployment: retry failed watch when observed controller has old resource
  version (mfojtik@redhat.com)
- Add TestEtcdStoragePath (mkhan@redhat.com)
- UPSTREAM: <carry>: Change docker security opt separator to be compatible with
  1.11+ (pmorie@redhat.com)
- Revert "e2e test: remove PodCheckDns flake" (maszulik@redhat.com)
- Add replace patch strategy for DockerImageMetadata and cmd tests for oc edit
  istag (maszulik@redhat.com)
- UPSTREAM: 41043: allow setting replace patchStrategy for structs
  (maszulik@redhat.com)

* Wed Feb 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.26-1
- improve output of `oc idle` (jvallejo@redhat.com)

* Wed Feb 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.25-1
- 

* Wed Feb 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.24-1
- improve scale,process,get help output handle multi-line strings in
  describe/newapp output (jvallejo@redhat.com)

* Wed Feb 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.23-1
- 

* Wed Feb 15 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.22-1
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 04d7652
  (tdawson@redhat.com)
- dind: upgrade to fedora 25 (marun@redhat.com)

* Wed Feb 15 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.21-1
- Fix make_redistributionable logic (tdawson@redhat.com)
- Add new cross.sh command line options (tdawson@redhat.com)
- change the parameter names in the route generation function to match the oc
  expose flag name (jtanenba@redhat.com)
- in clear-route-status.sh alert users if 'jq' tool is not installed
  (jtanenba@redhat.com)
- a split on string can give empty elements - fix bz1421572
  (rchopra@redhat.com)
- UPSTREAM: 41329: stop senseless negotiation (deads@redhat.com)
- Handle RPM output paths better in RPM build (skuznets@redhat.com)
- Provide canonical version and release to `tito` (skuznets@redhat.com)
- router: Fix ingress handling of nil rule value (marun@redhat.com)
- Bumped minimum acceptable tito version (skuznets@redhat.com)
- Refactored custom `tito` tagger and builder (skuznets@redhat.com)
- openvswitch: add wrapper to read configuration from env files
  (gscrivan@redhat.com)
- origin: add wrapper to read configuration from env files
  (gscrivan@redhat.com)
- node: add wrapper to read configuration from env files (gscrivan@redhat.com)
- add better logging for new-app argument processing (bparees@redhat.com)
- add generated docs (jvallejo@redhat.com)
- add add-cluster-role-to-user support for -z (jvallejo@redhat.com)
- Fix test hosts to be unique (different). (smitram@gmail.com)
- add sample using openshift-client-plugin syntax; add ext test
  (gmontero@redhat.com)

* Mon Feb 13 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.20
- set php latest to v7 (bparees@redhat.com)
- Enforce authz(n) on controller (ccoleman@redhat.com)
- Add Path and IsNonResourceURL to SAR (like upstream) (ccoleman@redhat.com)
- Move quasi-generic handlers out so controller can reuse them
  (ccoleman@redhat.com)
- don't include the project name in the new-app validation check
  (bparees@redhat.com)
- Change how the router was logging (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  35f07305cdd184856a5a953215e2a350adbe8c26 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  8d3d3c618780c9b4885dee91c362835140269b53 (dmcphers+openshiftbot@redhat.com)
- Perform a mv instead of cp during RPM release (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  95fab83b258d25272bbbbb1fc9c5d81c666d7e30 (dmcphers+openshiftbot@redhat.com)
- remove mongo clustered test: replaced by statefulset example and test
  (jminter@redhat.com)
- Remove special handling of --token and --context for whoami
  (jliggitt@redhat.com)
- Add a dnsBindAddress configuration to the node (ccoleman@redhat.com)
- Swagger generation uses a hardcoded directory (ccoleman@redhat.com)
- master: allow to specify command (gscrivan@redhat.com)
- Take more care in handling statefulset pods in mongodb test
  (jminter@redhat.com)
- node: install conntrack-tools in the node image (gscrivan@redhat.com)
- node: fix typo in the system container image (gscrivan@redhat.com)
- build extended tests: don't use large Jenkins image unnecessarily
  (jminter@redhat.com)
- Remove legacy kube test runner (marun@redhat.com)
- Add a status function to excluder (sdodson@redhat.com)

* Fri Feb 10 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.19
- Dump router pod logs on e2e failures (ccoleman@redhat.com)
- Wait for the `kubernetes` service on server start (skuznets@redhat.com)
- Revert "Revert "Revert "Refactored custom `tito` tagger and builder"""
  (skuznets@redhat.com)
- use src distinct directory for context-dir builds (bparees@redhat.com)
- return partial matches when default latest tag is unavailable
  (bparees@redhat.com)
- Add a new cluster-debugger role and enable debugging on masters
  (ccoleman@redhat.com)
- Revert "install ceph-common pkg on origin to support rbd provisioning"
  (ccoleman@redhat.com)
- deploy: bump number of retries in trigger integration test
  (mfojtik@redhat.com)
- Fix wrong type for printf (song.ruixia@zte.com.cn)
- Sort `List` for Project virtual storage (mkhan@redhat.com)
- Sort `List` for RoleBinding virtual storage (mkhan@redhat.com)
- Sort `List` for Role virtual storage (mkhan@redhat.com)
- fix typo (noblea1117@gmail.com)
- generated: bootstrap bindata (ccoleman@redhat.com)
- Include prometheus and heapster in bootstrap bindata (ccoleman@redhat.com)
- Update heapster and prometheus examples for consistent ports
  (ccoleman@redhat.com)
- Build rpms on aarch64, ppc64le and s390x (tdawson@redhat.com)
- install the types for the ingress admission controller (jtanenba@redhat.com)
- UPSTREAM: 41147: Add debug logging to eviction manager (decarr@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3f779bc6a5c8b1529c16a6c6bd16aad9ab85691a (dmcphers+openshiftbot@redhat.com)
- Bug 1393716 - Fix network diagnostics on containerized openshift install
  (rpenta@redhat.com)
- minor doc correction (pweil@redhat.com)
- Deprecate User.groups field (jliggitt@redhat.com)
- update generated completetion and docs (mfojtik@redhat.com)
- image: add --reference-policy to oc tag (mfojtik@redhat.com)
- add test for resolving images with reference policy (mfojtik@redhat.com)
- 503 page does not show guide detail as expected. (pcameron@redhat.com)
- bug 1419472 print master config error if it exists (jvallejo@redhat.com)
- router: fix ingress compatibility with f5 (marun@redhat.com)
- Changed the router default to roundrobin if non-zero weights are used
  (bbennett@redhat.com)
- Revert "Install tito from source in `openshift/origin-release`"
  (skuznets@redhat.com)
- Revert "Revert "Refactored custom `tito` tagger and builder""
  (skuznets@redhat.com)
- add ceph-common (hchen@redhat.com)
- image(router): Add logging facility to router tmpl (sjr@redhat.com)
- use ImageStreamImport for container command lookup in oc debug
  (jminter@redhat.com)
- install ceph-common pkg on origin to support rbd provisioning
  (hchen@redhat.com)

* Wed Feb 08 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.18
- bump(github.com/openshift/origin-web-console):
  be73cc17031099e9eb4947a6d1ce9024d774910f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3d2855d6c1920345a14b3bad4e91839d5080fd2d (dmcphers+openshiftbot@redhat.com)
- recreate generated service cert secret when deleted (mfojtik@redhat.com)
- UPSTREAM: 41089: Use privileged containers for statefulset e2e tests
  (skuznets@redhat.com)
- only run handleBuildCompletion on completed builds (bparees@redhat.com)
- Fixed the multicast CIDR (was 224.0.0.0/3 not /4) (bbennett@redhat.com)
- treat fatal errors as actually fatal (bparees@redhat.com)
- Allow users to parameterize the image prefix (skuznets@redhat.com)
- add newline to login output (deads@redhat.com)
- Add multicast test to extended networking test (danw@redhat.com)
- change argument --wildcardpolicy to --wildcard-policy in 'oc expose'
  (jtanenba@redhat.com)
- added clear-route-status.sh script to images/router/ (root@wsfd-
  netdev29.ntdv.lab.eng.bos.redhat.com)
- Refactor release packaging to be DRYer (skuznets@redhat.com)
- deploy: rework extended test to use rollout latest and increase timeout for
  getting logs (mfojtik@redhat.com)
- build: take referencePolicy into account when resolving istag
  (mfojtik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  fbc282d0f3f136c9d7eb6b72d89afa3db7b16feb (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  68c65908b68c559777cc46a1e8a501f992859469 (dmcphers+openshiftbot@redhat.com)
- Allow multicast for VNID 0 (danw@redhat.com)
- report a useful error when wide mode is used with new-app/new-build
  (bparees@redhat.com)
- Fix OVS connection tracking in networkpolicy plugin (danw@redhat.com)
- UPSTREAM :41034: use instance's Name to attach gce disk (hchen@redhat.com)
- 1408172 - ipfailover - `Permission denied for check and notify scripts
  (pcameron@redhat.com)
- cluster up: add brew install instructions (cewong@redhat.com)
- cluster up: add registry instructions (cewong@redhat.com)
- Make haproxy maxconn configurable (pcameron@redhat.com)
- Fix cluster up documentation of Linux firewalld instructions
  (cewong@redhat.com)
- Expose product-specific string literals as ldflags (skuznets@redhat.com)
- UPSTREAM: google/cadvisor: 1588: disable thin_ls due to excessive iops
  (decarr@redhat.com)
- Add `$GOPATH/bin` to `$PATH` only when `$GOPATH` is set (skuznets@redhat.com)
- Replace our Validator interface with upstream one (maszulik@redhat.com)
- node: add files for running as a system container (gscrivan@redhat.com)
- Correct the way that haproxy uses the secure cookie attribute
  (jtanenba@redhat.com)
- Fix type %%s to %%d for int type (song.ruixia@zte.com.cn)
- perform both http and https checks for monitoring f5 pools
  (rchopra@redhat.com)
- UPSTREAM: 39842: Remove duplicate calls to DescribeInstance during volume
  operations (hekumar@redhat.com)
- origin: add files for running as a system container (gscrivan@redhat.com)
- openvswitch: add files for running as a system container
  (gscrivan@redhat.com)

* Mon Feb 06 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.17
- Add standalone heapster as an example (ccoleman@redhat.com)
- Provide an all in one prometheus template example (ccoleman@redhat.com)
- use oc logs to get log (li.guangxu@zte.com.cn)
- bump(github.com/openshift/origin-web-console):
  aac7d52b246630d467ea19881b724a34d1ed08e2 (dmcphers+openshiftbot@redhat.com)
- updated man page (jtanenba@redhat.com)
- Used `os::log` functions better in protobuf script (skuznets@redhat.com)
- UPSTREAM: 40859: PV binding: send an event when there are no PVs to bind
  (jsafrane@redhat.com)
- Fix matchPattern log level to be like debug messages - otherwise all the
  other messages logged at loglevel 4 get overwhelmed. (smitram@gmail.com)
- Disable the admission plugin LimitPodHardAntiAffinityTopology by default.
  (avagarwa@redhat.com)
- Attempt at resolving
  github.com/openshift/origin/pkg/cmd/server/origin.TestAdmissionPluginNames
  github.com/openshift/origin/pkg/cmd/server/start.TestAdmissionOnOffCoverage
  (jtanenba@redhat.com)
- Changed using a map to k8s.io/apimachinery/pkg/utils/sets and added a test
  for adding a hostname (jtanenba@redhat.com)
- addresses Ben's initial comments (jtanenba@redhat.com)
- took out the decription in api/v1/types.go because govet.sh complained
  (jtanenba@redhat.com)
- added swagger docs and verified the gofmt (jtanenba@redhat.com)
- updated generated docs (jtanenba@redhat.com)
- add admission controller to restrict updates to ingresss objects hostname
  field. (jtanenba@redhat.com)
- changes to the cli for creating routes (jtanenba@redhat.com)
- router: provide better indication of failure in ingress test
  (marun@redhat.com)
- update docs/tests (sjenning@redhat.com)
- adding option '--insecure-policy' for passthrough and reencrypt route for CLI
  (jtanenba@redhat.com)
- Changed the router to default to roundrobin with multiple services
  (bbennett@redhat.com)
- UPSTREAM: <carry>: kubelet: change image-gc-high-threshold below docker
  dm.min_free_space (sjenning@redhat.com)

* Fri Feb 03 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.16
- Revert "Merge pull request #12751 from stevekuznetsov/skuznets/path-updates"
  (tdawson@redhat.com)
- Router tests should check for curl errors (ccoleman@redhat.com)
- Add DisableAttachDetachReconcilerSync new flag to master_config_test
  (maszulik@redhat.com)

* Fri Feb 03 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.15
- Merge remote-tracking branch enterprise-3.5, bump origin-web-console 7d868ff
  (tdawson@redhat.com)
- Use watch.Deleted event on the endpoints to ensure we do a valid transition
  Deleted -> Added instead of Modified -> Added. Otherwise the event queue code
  panics and kills the cache reflector goroutine which causes events to never
  be delivered to the test router process. fixes #12736 (smitram@gmail.com)
- Make sure to honor address binding request for all services
  (jonh.wendell@redhat.com)
- UPSTREAM: 38527: Fail kubelet if runtime is unresponsive for 30 seconds
  (decarr@redhat.com)
- Increased the time the proxy will hold connections when unidling
  (bbennett@redhat.com)
- bump(github.com/openshift/origin-web-console):
  16ebed8ff9127d6316caa01888935dc48ec69838 (dmcphers+openshiftbot@redhat.com)
- use secrets in sample templates (bparees@redhat.com)
- No one needs this info (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  774a733104caa86180127ea8cf5d05639a76e8fb (dmcphers+openshiftbot@redhat.com)
- Search for `goimports` in `$GOPATH`, not `$PATH` (skuznets@redhat.com)
- Update `$PATH` to include `$GOPATH/bin` by default (skuznets@redhat.com)
- increase mongodb test image pull timeout (jminter@redhat.com)
- Preserve file and directory validation errors (mkhan@redhat.com)
- UPSTREAM: 40763: reduce log noise when aws cannot find public-ip4 metadata
  (decarr@redhat.com)
- only set CGO_ENABLED=0 for tests (jminter@redhat.com)
- enable Azure disk provisioner (hchen@redhat.com)
- bump(github.com/openshift/origin-web-console):
  936eff71a6d7bc105b642642c8698d42f1474865 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4eaf2880b0992378b873ab223237110d1408a0bf (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  52f496aef9bd29703bf878b68f1d3bdafe05d205 (dmcphers+openshiftbot@redhat.com)
- include thin_ls package in base image (sjenning@redhat.com)
- generated-protobuf is using the wrong method (ccoleman@redhat.com)
- Adding wildcardpolicy flag to `oc create route` and a column for the
  wildcardpolicy to `oc get route' (jtanenba@redhat.com)
- Add check for empty directory to recycler (jsafrane@redhat.com)

* Wed Feb 01 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.14
- bump(github.com/openshift/origin-web-console):
  7b83464ba2c7fbc936d40ed1ed5f4f4a93d180a3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5fe0d17f41073fdd3e271cb8f8a746ce762cc66c (dmcphers+openshiftbot@redhat.com)
- Pick a smaller image for idling unit tests (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  63ae71a1ec299c1d0198bdfa518c25aab36b8c41 (dmcphers+openshiftbot@redhat.com)
- cluster up: remove hard-coded docker root mount (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  285733b9e8b762b06a301ca4d67e4f8fe870aee9 (dmcphers+openshiftbot@redhat.com)
- cluster up: fix port checking, Mac startup (cewong@redhat.com)
- Change MEMORY LIMIT parameter to be required one for multiple DBs
  (vdinh@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e14b670c7a12564723b573bf9e98af431df270e6 (dmcphers+openshiftbot@redhat.com)
- Replace find with grep -rl in update scripts (agoldste@redhat.com)
- treat binary buildconfig instantiate requests as long running
  (bparees@redhat.com)
- Remove List and ListOptions from non-round-trippable types in serialization
  test (mfojtik@redhat.com)
- deploy: add support for dc --dry-run to rollout undo (mfojtik@redhat.com)
- Short-circuit path shortening logic when possible (skuznets@redhat.com)
- Use `os::log` better in `os::util::ensure` functions (skuznets@redhat.com)
- Use `exit` instead of `return` in `os::log::fatal` (skuznets@redhat.com)

* Tue Jan 31 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.13
- Use a greedy match instead of a lazy one for versions (skuznets@redhat.com)
- make sure all projects are deleted on test start (jvallejo@redhat.com)
- Revert "Merge pull request #12671 from openshift/revert-12328-jvallejo
  /update-oc-status-warning" (jvallejo@redhat.com)

* Tue Jan 31 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.12
- Revert "Refactored custom `tito` tagger and builder" (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  46c6d8bc6c881c6ed4e520a62e8c2398ae464d9d (dmcphers+openshiftbot@redhat.com)
- Revert the creation of `images/ose` symlink (skuznets@redhat.com)
- Revert URL updates in source code and READMEs (skuznets@redhat.com)
- Fix stub interface so Mac compilations work (bbennett@redhat.com)
- Added an option to `hack/env` to use a new volume (skuznets@redhat.com)
- Bumped minimum acceptable tito version (skuznets@redhat.com)
- Refactored custom `tito` tagger and builder (skuznets@redhat.com)
- Don't give up copying from `hack/env` on failure (skuznets@redhat.com)

* Mon Jan 30 2017 Jenkins CD Merge Bot <tdawson@redhat.com> 3.5.0.11
- Merge remote-tracking branch upstream/master, bump origin-web-console 9989eef
  (tdawson@redhat.com)
- genman: error message update (mkargaki@redhat.com)
- Update README.md (ccoleman@redhat.com)
- Update README (ccoleman@redhat.com)
- setup watches before creating the buildconfig (bparees@redhat.com)
- Filter disallowed outbound multicast (danw@redhat.com)
- Add an annotation for enabling multicast on a namespace (danw@redhat.com)
- podManager simplification (danw@redhat.com)
- Change how multicast rule updates on VNID change work (danw@redhat.com)
- Update comments on multicast flow rules, simplify vxlan multicast rule
  (danw@redhat.com)
- Fix pod multicast route (danw@redhat.com)
- Allow `os::log` functions to print multi-line messages (skuznets@redhat.com)
- start the next serial build immediately after a build is canceled
  (bparees@redhat.com)
- Refactor logic for OSX etcd cURL statement (skuznets@redhat.com)
- Break out `os::cmd` framework tests from `hack/test-cmd.sh`
  (skuznets@redhat.com)
- Make use of `os::util::absolute_path` over `realpath` (skuznets@redhat.com)
- Update completions (jvallejo@redhat.com)
- improve bash completions for namespace flags (jvallejo@redhat.com)
- fix jenkins blue-green ext test so it does not block forever on build/deploy
  error (gmontero@redhat.com)
- Update version regex to handle longer dot-versions (skuznets@redhat.com)
- Update version regex to handle longer dot-versions (skuznets@redhat.com)
- regen origin docs/completions/openapi (sjenning@redhat.com)
- UPSTREAM: 37228: kubelet: storage: teardown terminated pod volumes
  (sjenning@redhat.com)
- add persistent examples to quickstarts (bparees@redhat.com)
- Fix messages, so that the ui tooltips don't have unicode characters.
  (smitram@gmail.com)
- Allow multiple ipfailover configs on same node (pcameron@redhat.com)
- Increase test coverage (agladkov@redhat.com)
- Restore `hack/common.sh` to the version in Origin (skuznets@redhat.com)
- Remove back-ported container manifests from dist-git (skuznets@redhat.com)

* Fri Jan 27 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.10
- bump(github.com/openshift/origin-web-console):
  9989eefc00d8379246015350374f4cdfcdc89933 (dmcphers+openshiftbot@redhat.com)
- backup and remove keys during migration (sjenning@redhat.com)
- bump(github.com/openshift/origin-web-console):
  960a94b5e2a1416e26fbb16f3d13eda3c45f4f77 (dmcphers+openshiftbot@redhat.com)
- Update clusterup documentation (persistence, proxy) (cewong@redhat.com)
- tweak pipeline build background monitor and ginkgo integration
  (gmontero@redhat.com)
- Router sets its dns name in admitted routes test (pcameron@redhat.com)
- Fix http status for error and remove dead code (agladkov@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ad2fdea2b7ac03e14942f96c7447ad0bdbfed8fe (dmcphers+openshiftbot@redhat.com)
- Minor fixes for dockerregistry/server tests (dmage@yandex-team.ru)
- Revert "Update "no projects" warning in `oc status`" (ccoleman@redhat.com)
- add migration script to fix etcd paths (sjenning@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f517fe8456628870ad7dfdac6e247abf385b43a2 (dmcphers+openshiftbot@redhat.com)
- Upgrade hack/env to support shell, env vars (ccoleman@redhat.com)
- leave oauth on jenkins extended test, use token for http-level access
  (gmontero@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e202d9ff4575f32427d39ac3b2e0cf21a7a9ff60 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a506596e52864fbfbc8d3cafa40a83156164f4ca (dmcphers+openshiftbot@redhat.com)
- Add audit log (agladkov@redhat.com)
- Update extended tests to run StatefulSet tests (maszulik@redhat.com)
- Rename PetSet to StatefulSet (maszulik@redhat.com)
- Install tito from source in `openshift/origin-release` (skuznets@redhat.com)
- Configure global git options in the release images (skuznets@redhat.com)
- use correct context dir during s2i build (bparees@redhat.com)
- Fix connection URL in postgresql examples (mmilata@redhat.com)
- Existing images are tagged with correct reference on push
  (miminar@redhat.com)
- Stop generating router/registry client certs (jliggitt@redhat.com)
- Remove deprecated credentials flag (jliggitt@redhat.com)
- bump(github.com/openshift/source-to-image):
  72d1d47c7c9e543320db4f2622a152cd6a12fcb3 (bparees@redhat.com)
- prevent Normalize from running twice on oadm drain (jvallejo@redhat.com)
- UPSTREAM: <drop>: request logs when attaching to a container
  (agoldste@redhat.com)
- UPSTREAM: docker/engine-api: 26718: Add Logs to ContainerAttachOptions
  (agoldste@redhat.com)
- Add comment pointing out incorrect SDN annotation naming (danw@redhat.com)
- UPSTREAM: 37846: error in setNodeStatus func should not abort node status
  update (sjenning@redhat.com)

* Wed Jan 25 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.9
- bump(github.com/openshift/origin-web-console):
  c9474fc80ed7b5174e97ff168531384dccb049ba (dmcphers+openshiftbot@redhat.com)
- Replace utilruntime.HandleError with glog (cdaley@redhat.com)
- Add a changelog generator for GitHub releases (ccoleman@redhat.com)
- avoid to return erroneous sa (salvatore-dario.minonne@amadeus.com)
- prevent ctx-switching from failing on server err (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2e4f477035b5cf5ce480d5aa2bbfe3ae0bf046a8 (dmcphers+openshiftbot@redhat.com)
- Update "no projects" warning in `oc status` (jvallejo@redhat.com)
- Add `os::log::debug` and add statements to `hack/env` (skuznets@redhat.com)
- normalize server url before writing to config (jvallejo@redhat.com)
- Make the OS_RELEASE=n ./hack/build-images.sh work again (miminar@redhat.com)
-  modified the comment format (luo.yin@zte.com.cn)
- Use - instead of + in tar filenames because GitHub changes them
  (ccoleman@redhat.com)
- generated: docs (ccoleman@redhat.com)
- Add the certificate command into admin (ccoleman@redhat.com)
- Blacklist pkg/bootstrap/run from govet (ccoleman@redhat.com)
- Add a simple bootstrap mode that waits for a secret (ccoleman@redhat.com)
- Add `oc cluster join` (ccoleman@redhat.com)
- Fix build controller performance issues (cewong@redhat.com)
- Test flakes? Just wait longer in more places (ccoleman@redhat.com)
- Switch empty extension files to return 200 with Content-Length zero
  (jforrest@redhat.com)
- cancel binary builds if they hang (bparees@redhat.com)
- Fix test-go.sh for directories with "-" in their names (danw@redhat.com)
- Generated changes (maszulik@redhat.com)
- Remove copyright from our source code (maszulik@redhat.com)
- UPSTREAM: 40023: Allow setting copyright header file for generated
  completions (maszulik@redhat.com)
- Bug 1415440: Check image history for zero size (mfojtik@redhat.com)
- Router improvement (yhlou@travelsky.com)
- update issue template from oadm (surajssd009005@gmail.com)

* Mon Jan 23 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.8
- Merge remote-tracking branch upstream/master, bump origin-web-console 8e6fe69
  (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  32319869d5fdfc8a184dacca6e2be489d4898e04 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e3d3db7a2dc0ac26a515d6c11ef052062d903488 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5d5983c3ee7842cbd2ee38345192b87178d4c1e4 (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: <carry>: Retry resource quota lookup until count stabilizes
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7f971336337ad19f87b8cae4586f589dfab3f294 (dmcphers+openshiftbot@redhat.com)
- Restore custom etcd prefixes (jliggitt@redhat.com)
- Check for 'in-cluster configuration' in both oc logs and output from oc run
  (maszulik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  880fcfc5ca7bf2a26191412f4f6ed824179d0e1f (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: 39831: Check if error is Status in result.Stream()
  (mfojtik@redhat.com)
- bump(github.com/coreos/etcd):v3.1.0 (ccoleman@redhat.com)
- Origin does not compile on Macs (ccoleman@redhat.com)
- UPSTREAM: coreos/rkt: <drop>: Workaround etcd310 / grpc incompat
  (ccoleman@redhat.com)
- UPSTREAM: <drop>: Workaround etcd310 / gprc version conflict with CRI
  (ccoleman@redhat.com)
- modify comments  t2T in ut file (bai.miaomiao@zte.com.cn)
- modify Run function comment (xu.zhanwei@zte.com.cn)
- bump(github.com/openshift/source-to-image):
  e01e9b7cdd51bda33dcefa1f28ffa5ddc50e06d7 (bparees@redhat.com)
- UPSTREAM: <carry>: Wait longer for pods to stop (ccoleman@redhat.com)
- Fix expected error message on new test (danw@redhat.com)
- sdn: add multicast support (dcbw@redhat.com)
- util/ovs: add GetOFPort() (dcbw@redhat.com)
- sdn: track running pod VNIDs too (dcbw@redhat.com)
- Router sets its host name in admitted routes (pcameron@redhat.com)
- record build durations properly on build completion (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  448422b31bd1d74cb2f02977e13418ddf20bc181 (dmcphers+openshiftbot@redhat.com)
- Use a differently-named DC in test/cmd/idle.sh (sross@redhat.com)
- Fixes as per @danwinship review comments. (smitram@gmail.com)
- bump(github.com/openshift/origin-web-console):
  e50c0c24b878e52eccf1c08b153973ca42211934 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  857a4e66423f7ef2ef325e119f7d7f0625225b32 (dmcphers+openshiftbot@redhat.com)
- improve extended test documentation (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4690daf1c8f5db5524c1bd10fa9bfdf46a07e10a (dmcphers+openshiftbot@redhat.com)
- Store Jobs under batch/v1 instead of deprecated extensions/v1beta1
  (maszulik@redhat.com)
- Wait for the token to be added to serviceaccount before running command
  (maszulik@redhat.com)
- Implement NetworkPolicies with PodSelectors (danw@redhat.com)
- Implement NetworkPolicies with NamespaceSelectors (danw@redhat.com)
- Implement NetworkPolicies with ports (danw@redhat.com)
- Add initial implementation of NetworkPolicy-based SDN plugin
  (danw@redhat.com)
- Allow requiring a minimum OVS version (danw@redhat.com)
- Migrate build constants from `hack/common.sh` (skuznets@redhat.com)
- registry: refactor verification to share common helper (mfojtik@redhat.com)
- Store built image digest in the build status (mmilata@redhat.com)
- Make the router handle ports properly (don't strip them). (smitram@gmail.com)
- UPSTREAM: <carry>: Increase pod deletion test timeout (ccoleman@redhat.com)
- UPSTREAM: 35436: Add a package for handling version numbers (including non-
  semvers) (danw@redhat.com)
- registry: add image signature endpoint (mfojtik@redhat.com)
- Remove erroneous instance of `${OS_IMAGE_COMPILE_GOFLAGS}`
  (skuznets@redhat.com)

* Fri Jan 20 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.7
- bump(github.com/openshift/origin-web-console):
  5ca208d4d341c22752a25127dcd08450ccd27e76 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  036bca26763207ec4014eb6e8a993c0c0bad2e12 (dmcphers+openshiftbot@redhat.com)
- Wait for the token to be added to serviceaccount before running command
  (maszulik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4d03d9894e749c30524b1b07b85f44de5d915553 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ce46f5a444df26078d048ee19b7b064e725638e9 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5371b156fbb324d5700562772215a1c4fefa485a (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c298116958c86d3dc27e3a3e31df3fff2a5dfd6b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0c6f32f9c822af3a7710e8a7f4ad53c4f3c7930e (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4b8b74b74af7b99de3dd8fdf1b7f12e3aae32e0b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c8051e9b45848184b98ce0b79a98f953d7bfb4ca (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f8380670ab9bee828a7dc01382b627b2618384ef (dmcphers+openshiftbot@redhat.com)
- router: validate ingress compatibility with namespace filtering
  (marun@redhat.com)
- router: add support for configuration by ingress (marun@redhat.com)
- bump(github.com/openshift/origin-web-console):
  37d4d789e90d78264c5b1e77127188320a0a111e (dmcphers+openshiftbot@redhat.com)
- Prune manifest config of schema 2 images (miminar@redhat.com)
- UPSTREAM: 39844: fix bug not using volumetype config in create volume
  (hchiramm@redhat.com)
- bump(github.com/openshift/origin-web-console):
  487f7df29c1b7167c35da40f11f4c8cec657be00 (dmcphers+openshiftbot@redhat.com)
- Update quota test to better express intent (skuznets@redhat.com)
- Add `os::cmd::try_until_not_text` utility function (skuznets@redhat.com)
- Update `os::cmd` error messages to be more correct (skuznets@redhat.com)
- Run output tests only on the last attempt for `os::cmd` (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  32bbb0ff1f294cfdc8eb81118c8717fba185fc0e (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  01a4bedf245788cbca27c893c87a99f00547bdc8 (dmcphers+openshiftbot@redhat.com)
- Re-enable etcd3 mode and proto storage (ccoleman@redhat.com)
- Refactor `os::cmd` result printer (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  709cca2cbb68cb840a747aeb012dcc9a46aee198 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  dee65074bb6243f3a284eff2e546fea12f9647a2 (dmcphers+openshiftbot@redhat.com)
- Fixed attempt marking code for try_until stderr (skuznets@redhat.com)
- Updating external examples (cdaley@redhat.com)
- bump(github.com/openshift/origin-web-console):
  61b0d0fa14b68177c16cbc5b9fa2140988fe0324 (dmcphers+openshiftbot@redhat.com)
- Remove unused make target (maszulik@redhat.com)
- cluster up: mount host /dev into origin container (cewong@redhat.com)
- UPSTREAM: 38579: Let admin configure the volume type and parameters for
  gluster DP volumes (hchiramm@redhat.com)
- UPSTREAM: 38378: glusterfs: properly check gidMin and gidMax values from SC
  individually (hchiramm@redhat.com)
- UPSTREAM: 37986: Add `clusterid`, an optional parameter to storageclass.
  (hchiramm@redhat.com)
- Bump to golang-1.8rc1 (ccoleman@redhat.com)
- Add ut test for the function getContainerNameOrID (meng.hao1@zte.com.cn)
- bump(github.com/openshift/origin-web-console):
  5cb015108589cb3e9bbabe953ce86275c5a3a082 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f6709f685529329139b6b61aaf538dbcaf2d85f3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2cb38e1044b8ac640b464f48765d9d7ba22c250f (dmcphers+openshiftbot@redhat.com)
- Add headers that provide extra security protection in browsers
  (jforrest@redhat.com)
- bump(github.com/openshift/origin-web-console):
  04dcf30d6be1481cbb8a51967039015a4741864d (dmcphers+openshiftbot@redhat.com)
- Add annotations to roles. (mkhan@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f3d64d5d546617b431ee4f5a20803c6bba4111c2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2d9fec830c03c77a877d8afc63832dea206ad72e (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3c430699d21d47007b3fafdb6736881974c8bfa1 (dmcphers+openshiftbot@redhat.com)
- kubelet must have rw to cgroups for pod/qos cgroups to function
  (decarr@redhat.com)
- bump(github.com/openshift/origin-web-console):
  832cec030ff015081965dd6675e5b0fe98ec02c2 (dmcphers+openshiftbot@redhat.com)
- cluster up: add proxy support (cewong@redhat.com)
- update to compile against bumped glog godep (jminter@redhat.com)
- bump(github.com/golang/glog) 44145f04b68cf362d9c4df2182967c2275eaefed
  (jminter@redhat.com)
- fix broken "failing postCommit default entrypoint" test and reformat for
  clarity (jminter@redhat.com)
- ipfailover - user check script overrides default (pcameron@redhat.com)
- Update help text as per @knobunc review comments and regenerate the docs. Fix
  failing integration test. (smitram@gmail.com)
- Add support to disable the namespace ownership checks. This allows routes to
  claim non-overlapping hosts (+ paths) and wildcards across namespace
  boundaries. Update generated docs and completions. (smitram@gmail.com)

* Wed Jan 18 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.6
- bump(github.com/openshift/origin-web-console):
  c42118856232d57d410b17ca20d8a193cd22995b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  695c74dc0fac848444c79c555fb689c4d8431973 (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: <carry>: Pod deletion can be contended, causing test failure
  (ccoleman@redhat.com)
- Better haproxy 503 page (ffranz@redhat.com)
- bump external template examples (bparees@redhat.com)
- Build extended.test in build-cross (ccoleman@redhat.com)
- cluster up: add persistent volumes on startup (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  738a098ce3e0e1ab13b788e812eaba08f90f1146 (dmcphers+openshiftbot@redhat.com)
- Increase deployment test timeout (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  dda5f7ab8684393e6f376ae249f20a8a7d77c137 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b1dcc6f8daa1426f2bcdbcd36878b343ff6c69b9 (dmcphers+openshiftbot@redhat.com)
- Generated changes (maszulik@redhat.com)
- UPSTREAM: 39997: Fix ScheduledJob -> CronJob rename leftovers
  (maszulik@redhat.com)
- Add service UID as x509 extension to service server certs
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: Increase service endpoint test timeout
  (ccoleman@redhat.com)
- only set term if rsh is running /bin/sh (bparees@redhat.com)
- Adding a test for not having a route added if the gateway and the destination
  addresses are the same (fgiloux@redhat.com)
- bump(github.com/openshift/origin-web-console):
  15e4baa64a7d1a39771c32e67753edd0a0ee7cf5 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a3da0eff67c443ed5b5a0465913c3a3cf6e93839 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e9ab6af6f5520780c28da2294965c72f57e6d2f4 (dmcphers+openshiftbot@redhat.com)
- add swaggerapi to discovery rules (deads@redhat.com)
- add a test for fetchruntimeartifacts failure (ipalade@redhat.com)
- UPSTREAM: <carry>: Double container probe timeout (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0102c49ad4d39d9bd74d96fd85222e95b3c69743 (dmcphers+openshiftbot@redhat.com)
- Hide DockerImageConfig as well as DockerImageManifest (agladkov@redhat.com)
- Modify comment for pkg/controller/scheduler.go (song.ruixia@zte.com.cn)
- Adding --build-env and --build-env-file to oc new-app (cdaley@redhat.com)
- Uses patch instead of update to mark nodes (un)schedulable
  (ffranz@redhat.com)
- add affirmative output to oc policy / oadm policy (jvallejo@redhat.com)
- Remove vestiges of atomic-enterprise in the codebase (ccoleman@redhat.com)
- Do not reuse pkgdir across architectures (ccoleman@redhat.com)
- UPSTREAM: docker/distribution: 2140: Add 'ca-central-1' region for registry
  S3 storage driver (mfojtik@redhat.com)
- Links to docker and openshift docs updated (mupakoz@gmail.com)
- add log arguments (wang.xiaogang2@zte.com.cn)

* Mon Jan 16 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.5
- bump(github.com/openshift/origin-web-console):
  fa6f2af00717135ec5c8352daf73a3db2a4f4255 (dmcphers+openshiftbot@redhat.com)
- Increase timeout of deployment test (ccoleman@redhat.com)
- Networking tests must be able to schedule on all nodes (ccoleman@redhat.com)
- Generated changes (maszulik@redhat.com)
- Necessary k8s 1.5.2 updates (maszulik@redhat.com)
- UPSTREAM: 39886: Only set empty list for list types (maszulik@redhat.com)
- UPSTREAM: 39834: Ensure empty lists don't return nil items fields
  (maszulik@redhat.com)
- UPSTREAM: 39496: Use privileged containers for host path e2e tests
  (skuznets@redhat.com)
- UPSTREAM: 39059: Don't evict static pods - revert (maszulik@redhat.com)
- UPSTREAM: 38836: Admit critical pods in the kubelet - revert
  (maszulik@redhat.com)
- UPSTREAM: 39114: assign -998 as the oom_score_adj for critical pods (e.g.
  kube-proxy) - revert (maszulik@redhat.com)
- bump(k8s.io/kubernetes): 43a9be421799afb8a9c02d3541212a6e623c9053
  (maszulik@redhat.com)
- UPSTREAM: revert: eb8415dffd1db720429f8ea363defb981d0d9ebe: 39496: Use
  privileged containers for host path e2e tests (maszulik@redhat.com)
- UPSTREAM: revert: c610047330c232d7550ec17d2cfd687a295a5d54: <drop>: Disable
  memcfg notifications until softlockup fixed (maszulik@redhat.com)
- Registry manifest extended test is local only (ccoleman@redhat.com)
- UPSTREAM: <drop>: Disable memcfg notifications until softlockup fixed
  (ccoleman@redhat.com)
- Move kubelet e2e test to serial suite because it saturates nodes
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d8331ea4e4910a556771ae1e5416e389ab8a3fa5 (dmcphers+openshiftbot@redhat.com)
- Add golang source detector for new-app (cdaley@redhat.com)
- bump(github.com/docker/go-units): e30f1e79f3cd72542f2026ceec18d3bd67ab859c
  (ffranz@redhat.com)
- bump(github.com/openshift/origin-web-console):
  865b35e623a66e43acae810a03de9b5b1a94f694 (dmcphers+openshiftbot@redhat.com)
- Switch image quota to user shared informers (maszulik@redhat.com)
- Allow to use selector when listing clusterroles and rolebindings
  (mfojtik@redhat.com)
- return value all use observed (xu.zhanwei@zte.com.cn)
- Fix /.well-known/oauth-authorization-server panic and add test
  (stefan.schimanski@gmail.com)
- remove old version check for sup group test (pweil@redhat.com)
- update generated content (mfojtik@redhat.com)
- Remove pullthrough request from cross-repo mount test (agladkov@redhat.com)
- dind: Ensure help text documents the order of command and options
  (marun@redhat.com)
- dind: Switch OPENSHIFT_SKIP_BUILD to treat non-empty as true
  (marun@redhat.com)
- deploy: add ready replicas to DeploymentConfig (mfojtik@redhat.com)

* Fri Jan 13 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.4
- Merge remote-tracking branch upstream/master, bump origin-web-console 865715f
  (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  865715f679a193b659083a2f239a4cabb1a10937 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  bff896f04a4ece555229734e481d0c5de954b6a0 (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: 39496: Use privileged containers for host path e2e tests
  (skuznets@redhat.com)
- allow proxy values to be specified with non-http git uris
  (bparees@redhat.com)
- umount openshift local volumes in clean up script (li.guangxu@zte.com.cn)
- bump(github.com/openshift/origin-web-console):
  7e591430787f0a150b62e6fb0a533956235e72fe (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ba28a7432c175c0600330819e303ba4a07638a93 (dmcphers+openshiftbot@redhat.com)
- cluster up: use serverIP on Mac when public host is not specified
  (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  007f1d33fc639a1a99ade6e83ae81e1acf4ccb6a (dmcphers+openshiftbot@redhat.com)
- Add a nil check to Container.SecurityContext (bbennett@redhat.com)
- Add some optimization between command new-app and new-build
  (li.guangxu@zte.com.cn)
- Updating oc cluster up command to include a --image-streams flag
  (cdaley@redhat.com)
- ipfailover keepalived split brain (pcameron@redhat.com)
- Check and notify scripts are not executable (pcameron@redhat.com)
- UPSTREAM: 39493: kubelet: fix nil deref in volume type check
  (sjenning@redhat.com)
- Add a short explination of Subdomain wildcard policy (jtanenba@redhat.com)
- added wildcardpolicy flag to 'oc expose' (jtanenba@redhat.com)

* Wed Jan 11 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.3
- Merge remote-tracking branch upstream/master, bump origin-web-console 65ebe13
  (tdawson@redhat.com)
- Increase time 'oc cluster up' waits for dns to be available
  (agoldste@redhat.com)
- Only call UnrefVNID if the pod's netns is still valid (agoldste@redhat.com)
- bump(github.com/openshift/origin-web-console):
  65ebe1391f7798fdea1f93ce29eb45b932548859 (dmcphers+openshiftbot@redhat.com)
- Update import docker-compose test expectations (agoldste@redhat.com)
- Make test/extended/alternate_launches.sh pass (agoldste@redhat.com)
- Pushing busybox no longer necessary now that we have pull-through
  (agoldste@redhat.com)
- Add missing junit suite declarations (agoldste@redhat.com)
- Disable kube-proxy urls test for now (agoldste@redhat.com)
- Remove unnecessary line (agoldste@redhat.com)
- Set required ReferencePolicy field so tests pass (agoldste@redhat.com)
- Fix extended tests (maszulik@redhat.com)
- Fix hack/test-cmd.sh (maszulik@redhat.com)
- Switch tooling to go 1.7 (maszulik@redhat.com)
- Remove kube .proto files for api groups that no longer exist
  (agoldste@redhat.com)
- Fix defaults test expectations (agoldste@redhat.com)
- Match upstream client changes (agoldste@redhat.com)
- skip DNS config map e2e test (agoldste@redhat.com)
- Make test-end-to-end work (agoldste@redhat.com)
- Fix jenkins admission plugin (maszulik@redhat.com)
- Remove omitEmpty from DeploymentConfigStatus int fields so it will emit them
  even if 0 (agoldste@redhat.com)
- Update User-Agent test expectations (agoldste@redhat.com)
- Fix test-cmd.sh (agoldste@redhat.com)
- Image streams: move BeforeCreate/BeforeUpdate <carry> logic to
  Validate/ValidateUpdate (agoldste@redhat.com)
- Wrap checking for deleted routes in wait.Poll in TestRouterReloadCoalesce
  (agoldste@redhat.com)
- Set PreferredAddressTypes when we create the KubeletClientConfig
  (agoldste@redhat.com)
- Make jobClient use batch/v2alpha1 to support cronjobs (agoldste@redhat.com)
- policy: allow GCController to list/watch nodes (agoldste@redhat.com)
- policy: allow statefulsetcontroller access to statefulsets
  (agoldste@redhat.com)
- SA controller Run() is now blocking; call via goroutine (agoldste@redhat.com)
- Add DestroyFunc to ApplyOptions and tests (maszulik@redhat.com)
- Start kube shared informer factory (agoldste@redhat.com)
- Add support for kube admission plugin initializers (agoldste@redhat.com)
- Enable PodNodeSelector admission plugin (agoldste@redhat.com)
- Use kube's SA cache store/lister (agoldste@redhat.com)
- Use kube serviceaccounts shared informer (agoldste@redhat.com)
- Added certificate to ignored kube commands in tests (maszulik@redhat.com)
- Update bootstrap policy (maszulik@redhat.com)
- Update expected kube api group versions (agoldste@redhat.com)
- Add new arg for iptables min sync duration when creating proxiers
  (agoldste@redhat.com)
- Update master setup to match kube 1.5 changes (agoldste@redhat.com)
- Apply defaults the new way now that conversion and defaulting are separate
  (agoldste@redhat.com)
- Fixes based on updated generated code (agoldste@redhat.com)
- Use generated defaulters (agoldste@redhat.com)
- Regenerate generated files (agoldste@redhat.com)
- Add defaulter-gen comments (agoldste@redhat.com)
- Match clientcmd Factory changes from upstream (agoldste@redhat.com)
- Match upstream change for --allow-missing-template-keys (agoldste@redhat.com)
- UPSTREAM: 39486: Allow missing keys in templates by default
  (agoldste@redhat.com)
- UPSTREAM: <drop>: add origin resource shortcuts to kube shortcut restmapper
  (agoldste@redhat.com)
- UPSTREAM: 38647: make kubectl factory composeable (maszulik@redhat.com)
- Replace legacy kube informers with actual upstream kube informers
  (agoldste@redhat.com)
- Switch deployment controller/utils to use []*RC instead of []RC
  (agoldste@redhat.com)
- Pass sharedInformerFactory through to quota registry (agoldste@redhat.com)
- Fix Rollback signature (agoldste@redhat.com)
- Boring: match upstream moves/refactors/renames (agoldste@redhat.com)
- Implement CanMount() for emptyDirQuotaMounter (agoldste@redhat.com)
- PetSet -> StatefulSet (agoldste@redhat.com)
- ScheduledJob -> CronJob (agoldste@redhat.com)
- Boring: match upstream renames/moves (agoldste@redhat.com)
- Correct Godeps.json (agoldste@redhat.com)
- UPSTREAM: 38908: Remove two zany unit tests (agoldste@redhat.com)
- UPSTREAM: opencontainers/runc: 1216: Fix thread safety of SelinuxEnabled and
  getSelinuxMountPoint (pmorie@redhat.com)
- UPSTREAM: 38339: Exponential back off when volume delete fails
  (agoldste@redhat.com)
- UPSTREAM: 37009: fix permissions when using fsGroup (agoldste@redhat.com)
- UPSTREAM: 38137: glusterfs: Fix all gid types to int to prevent failures on
  32bit systems (agoldste@redhat.com)
- UPSTREAM: 37886: glusterfs: implement GID security in the dynamic provisioner
  (agoldste@redhat.com)
- UPSTREAM: 36437: glusterfs: Add `clusterid`, an optional parameter to
  storageclass. (agoldste@redhat.com)
- UPSTREAM: 38196: fix mesos unit tests (agoldste@redhat.com)
- UPSTREAM: 37721: Fix logic error in graceful deletion (agoldste@redhat.com)
- UPSTREAM: 37649: Fix top node (agoldste@redhat.com)
- bump(golang.org/x/sys) 8d1157a435470616f975ff9bb013bea8d0962067
  (jminter@redhat.com)
- bump(k8s.io/gengo): 6a1c24d7f08e671c244023ca9367d2dfbfaf57fc
  (agoldste@redhat.com)
- Fix imports for genconversion/gendeepcopy to use k8s.io/gengo
  (agoldste@redhat.com)
- bump(google.golang.org/grpc): b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
  (agoldste@redhat.com)
- bump(github.com/onsi/gomega): d59fa0ac68bb5dd932ee8d24eed631cdd519efc3
  (agoldste@redhat.com)
- UPSTREAM: 38603: Re-add /healthz/ping handler in genericapiserver
  (stefan.schimanski@gmail.com)
- UPSTREAM: 38690: unify swagger and openapi in config
  (stefan.schimanski@gmail.com)
- UPSTREAM: <drop>: add ExtraClientCACerts to SecureServingInfo
  (stefan.schimanski@gmail.com)
- UPSTREAM: <drop>: add missing index to limit range lister
  (agoldste@redhat.com)
- Match upstream singular -> singleItemImplied rename (agoldste@redhat.com)
- UPSTREAM: 39038: Fix kubectl get -f <file> -o <nondefault printer> so it
  prints all items in the file (agoldste@redhat.com)
- UPSTREAM: 38986: Fix DaemonSet cache mutation (agoldste@redhat.com)
- UPSTREAM: 38631: fix build tags for !cgo in kubelet cadvisor
  (agoldste@redhat.com)
- UPSTREAM: 38630: Fix threshold notifier build tags (agoldste@redhat.com)
- UPSTREAM: coreos/go-systemd: 190: util: conditionally build CGO functions
  (agoldste@redhat.com)
- bump(github.com/onsi/ginkgo/ginkgo): 74c678d97c305753605c338c6c78c49ec104b5e7
  (agoldste@redhat.com)
- bump(k8s.io/client-go): ecd05810bd98f1ccb9a4558871cb0de3aefd50b4
  (agoldste@redhat.com)
- bump(github.com/juju/ratelimit): 77ed1c8a01217656d2080ad51981f6e99adaa177
  (agoldste@redhat.com)
- UPSTREAM: 38294: Re-use tested ratelimiter (agoldste@redhat.com)
- bump(k8s.io/kubernetes): 225eecce40065518f2eabc3b52020365db012384
  (agoldste@redhat.com)
- Update copy-kube-artifacts to current k8s (maszulik@redhat.com)
- Update group versions in genprotobuf (agoldste@redhat.com)
- Add generators for defaulters, openapi, listers (agoldste@redhat.com)
- bump(github.com/rackspace/gophercloud):
  e00690e87603abe613e9f02c816c7c4bef82e063 (agoldste@redhat.com)
- bump(github.com/onsi/gomega): d59fa0ac68bb5dd932ee8d24eed631cdd519efc3
  (agoldste@redhat.com)
- bump(github.com/jteeuwen/go-bindata):
  a0ff2567cfb70903282db057e799fd826784d41d (agoldste@redhat.com)
- bump(github.com/fsnotify/fsnotify): f12c6236fe7b5cf6bcf30e5935d08cb079d78334
  (agoldste@redhat.com)
- Add extra required dependencies to hack/godep-save.sh (agoldste@redhat.com)
- godepchecker: add option to compare forks (agoldste@redhat.com)
- Pin godep to v75 (agoldste@redhat.com)
- bump(golang.org/x/sys): revert: 264b1bec8780c764719c49a189286aabbeefc9c2:
  (bump to 8d1157a435470616f975ff9bb013bea8d0962067) (agoldste@redhat.com)
- UPSTREAM: revert: bedff43594597764076a13c17b30a5fa28c4ea76: docker/docker:
  <drop>: revert: 734a79b: docker/docker: <carry>: WORD/DWORD changed
  (agoldste@redhat.com)
- origin: revert: 5d5c0c90bea65fea41a2b72d6e28bf0800696f95: 37649: Fix top node
  (agoldste@redhat.com)
- UPSTREAM: revert: 5d5c0c90bea65fea41a2b72d6e28bf0800696f95: 37649: Fix top
  node (agoldste@redhat.com)
- UPSTREAM: revert: 372e9928f1ada5f49d4c44684f7151798bcca200: 37721: Fix logic
  error in graceful deletion (agoldste@redhat.com)
- UPSTREAM: revert: 74f64a736154ab6bcc508abaa6d045828b7eacd8: 38196: fix mesos
  unit tests (agoldste@redhat.com)
- bump(github.com/heketi/heketi): revert:
  7fd7ced6cb2d2eeaf66408bb7b2e4491f7036cbb (bump to
  28b5cc4cc6d2b9bdfa91ed1b93efaab4931aa697) (agoldste@redhat.com)
- UPSTREAM: revert: 9bffc75ed9a26d0cd226febc93cad61d0a500d77: 37886: glusterfs:
  implement GID security in the dynamic provisioner (agoldste@redhat.com)
- UPSTREAM: revert: 6974f328a5577926c8a62a4ed456ed388f9e477d: 38137: glusterfs:
  Fix all gid types to int to prevent failures on 32bit systems
  (agoldste@redhat.com)
- UPSTREAM: revert: 64982639ab1321fb1a1332dd78101a1ff5f8c59a: 37009: fix
  permissions when using fsGroup (agoldste@redhat.com)
- UPSTREAM: revert: b049251dc647418edf2b1a700d1a52ce85dc9696: 38339:
  Exponential back off when volume delete fails (agoldste@redhat.com)
- UPSTREAM: revert: 33ee3c4f6a4a3b07d9c758c0271a950b6a52d26a:
  opencontainers/runc: 1216: Fix thread safety of SelinuxEnabled and
  getSelinuxMountPoint (agoldste@redhat.com)
- UPSTREAM: revert: 8f14f3b701aa10757d1edad3a566672c72b7b55f: <drop>: Handle Go
  1.6/1.7 differences in upstream (agoldste@redhat.com)
- if2If at the begining of one line (lu.jianping2@zte.com.cn)
- cluster up: add pod networking check (cewong@redhat.com)
- Adding aos-3.5 tito build queue (tdawson@redhat.com)
- Update ose_images.sh - 2017-01-09 (tdawson@redhat.com)
- modify comment for CommandFor (xu.zhanwei@zte.com.cn)
- Add extended test for manifest migration (agladkov@redhat.com)
- Migrate manifest from Image when receiving get-request (agladkov@redhat.com)
- Add tests for pullthroughManifestService (agladkov@redhat.com)
- Save manifest in docker-registry and make pullthrough for manifests
  (agladkov@redhat.com)
- Move ManifestService to separate object (agladkov@redhat.com)

* Mon Jan 09 2017 Troy Dawson <tdawson@redhat.com> 3.5.0.2
- Merge remote-tracking branch upstream/master, bump origin-web-console 6f48eb0
  (tdawson@redhat.com)
- remove openshift.io/container.%%s.image.entrypoint annotation and clarify
  new-app maximum name length (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6f48eb058bdf5e1e8b0fe75f124530be44acd1aa (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  abdc02074315ba9b3a7e26c2ca081aacbfa9c173 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  1bea253df7f420ee7a27478e6c7f1b38bad4bf17 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6f0b723c2f9c6473dab380f8b77c93e80774660a (dmcphers+openshiftbot@redhat.com)
- Implement secret injector admission controller for buildconfigs
  (jminter@redhat.com)
- bump(github.com/openshift/source-to-image):
  8de9f04445c8a58f244df30f0798d1d1fdb3023a (ipalade@redhat.com)
- bump(github.com/openshift/origin-web-console):
  81127a4039a90ce5e790b3a12b602aaf6950de91 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3656be70e9d4c88a91818ca148ce3aa3cc000cbd (dmcphers+openshiftbot@redhat.com)
- always set the commitid env variable in the output image (bparees@redhat.com)
- cluster up: do not ignore public-hostname on Mac with Docker for Mac
  (cewong@redhat.com)
- ipfailover - fix typo in script (pcameron@redhat.com)
- Fix manifest verification if pullthrough enabled (agladkov@redhat.com)
- fix typo and  drop = nil drop []string (yu.peng36@zte.com.cn)
- bump(github.com/openshift/origin-web-console):
  f0e8144f93ef69e996933c572fc6ecee619d2ebe (dmcphers+openshiftbot@redhat.com)
- Add --default-mode flag to oc set volume (rymurphy@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b55a35d8f6f7aed63de5a2d6e19e52c9053e841e (dmcphers+openshiftbot@redhat.com)
- Ensure default ingress cidr is a private range (marun@redhat.com)
- Fix 404 error in Jenkins plugin extended tests (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  025ded5e81d0bba659e5b88ba1d458bc751808eb (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  76040f12bbb6849467bec657bdd1d9ab20835ffd (dmcphers+openshiftbot@redhat.com)
- Ensure an invalid bearer token returns an error (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ddceed94f956f73363f3113eaaa73341e6f40fa2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ac02e04d55d69d23c2f4b701bca729d00dd2dfd8 (dmcphers+openshiftbot@redhat.com)
- Bug 1348174 - error on non-existing tag when importing from
  .spec.dockerImageRepository (maszulik@redhat.com)
- enable hostpath provisioning (somalley@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0b1435e239c27e3c52ad745a76ea29b5f8ee1ffd (dmcphers+openshiftbot@redhat.com)
- reduce some empty line && code, add some TODO comments (shiywang@redhat.com)
- clarify unknown type log message (bparees@redhat.com)
- Fix printing args in image pruning (maszulik@redhat.com)
- Disable registry test that compares sha256 checksum of layers due to
  go1.6/1.7 incompatibility (mfojtik@redhat.com)
- Label idling tests [local] for now, add more tests to suite
  (ccoleman@redhat.com)
- Use [local] consistently (ccoleman@redhat.com)
- note about net.ipv4.ip_forward=1 (Oleksii.Prudkyi@gmail.com)
- Merge extended test suite JUnit files to avoid duplicate skips
  (ccoleman@redhat.com)
- Allow additional extended tests to be skipped with TEST_EXTENDED_SKIP
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  34536058a2d795587040db3a16505360b1e9eb1b (dmcphers+openshiftbot@redhat.com)
- adapt secret key names to new policy (raaflaub@puzzle.ch)
- These tests require local access (ccoleman@redhat.com)
- Router tests should not assume access to pod network (ccoleman@redhat.com)
- Scheduler predicates test should run without node constraints
  (ccoleman@redhat.com)
- Fixing typos (mmahut@redhat.com)
- Allow much higher extended test bursting by increasing retry
  (ccoleman@redhat.com)
- Disable color on extended test suite (ccoleman@redhat.com)
- UPSTREAM: onsi/ginkgo: 318: Capture test output (ccoleman@redhat.com)
- Disable pullthrough in test case (ccoleman@redhat.com)
- Remove backup files (maszulik@redhat.com)
- Apply defaulting in image stream import (ccoleman@redhat.com)
- generated: swagger (ccoleman@redhat.com)
- Add an extended test for deployment resolution (ccoleman@redhat.com)
- Add reference policy to describe output (ccoleman@redhat.com)
- Respect tag referencePolicy in builds and deployments (ccoleman@redhat.com)
- Enable pullthrough by default (ccoleman@redhat.com)
- generated: api changes (ccoleman@redhat.com)
- Support a new image stream tag reference policy (ccoleman@redhat.com)
- Add extended tests for pipeline examples (cewong@redhat.com)
- Do not print findmnt on startup (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6bd844376083142cc89c7ce64ef39d49a887a8d0 (dmcphers+openshiftbot@redhat.com)
- Pass no focus spec in `make test-extended` when unset (skuznets@redhat.com)
- update debugging doc and sample-app README (li.guangxu@zte.com.cn)
- Fix hard coded binary path (tdawson@redhat.com)

* Thu Dec 22 2016 Troy Dawson <tdawson@redhat.com> 3.5.0.1
- Update version to 3.5.0.0 (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ab61c6fca709340f431605e92cedfcac447d998b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4e95180904ce953eb73793a40476af51217ea01f (dmcphers+openshiftbot@redhat.com)
- redo forcepull test so localnode is not required (gmontero@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0279eece98b9c8a3338be0e32968bfb22329d2af (dmcphers+openshiftbot@redhat.com)
- deprecate images based on EOL SCL packages (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e66c5add6055e8e2c15e8d277df590692fae8c7b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ea2a5b6d21c5a720baabccf53f4e5117cc95219f (dmcphers+openshiftbot@redhat.com)
- Return non-error msg on `oc status` if no projects (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  171a0675e7924d835afed76c933215d142700c7f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  723de04d1e7707b6d9801816654b4a5efa9473b4 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  019df5167c23d499463e332992b85b1d0b5d58cc (dmcphers+openshiftbot@redhat.com)
- s2i_extended_build: update repo url. (vsemushi@redhat.com)
- router: Cleanup logging of routing state changes (marun@redhat.com)
- router: clean up service unit configuration (marun@redhat.com)
- router: Avoid reloads when route configuration hasn't changed
  (marun@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b3ce1b68237db08e69e823d00c608af213192a5e (dmcphers+openshiftbot@redhat.com)
- Add a golang-1.8 release image (ccoleman@redhat.com)
- Reuse test artifacts (ccoleman@redhat.com)
- Don't use findmnt if it isn't there (ccoleman@redhat.com)
- Create a package for non-Linux builds (ccoleman@redhat.com)
- Add RHSCL 2.3 docker images to image streams (hhorak@redhat.com)
- bump(github.com/openshift/origin-web-console):
  664a2473bd2b2155499d9210579713431f6a07b6 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6010439649cd7550ea95adef27e3698979ee24f4 (dmcphers+openshiftbot@redhat.com)
- Added manifest verification (miminar@redhat.com)
- Registry: moved manifest schema operations to new files (miminar@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7973c2b9c77a236f7ff9516467cb46ee25212624 (dmcphers+openshiftbot@redhat.com)
- add debug to failure reason extended tests (bparees@redhat.com)
- Fix group name in EgressNetworkPolicy-related rules (danw@redhat.com)
- bump(github.com/openshift/origin-web-console):
  960a01bc0bb5d9d2ee129885fbcc8683f99f1a61 (dmcphers+openshiftbot@redhat.com)
- do s2i git cloning up front, not in s2i itself (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  eb5c33657e1133bb1b5579405446cdad191ce3d6 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ef858d27b8ffb68e1d801f527363d4223608a8e7 (dmcphers+openshiftbot@redhat.com)
- add namespace selector field to crq describe output (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a20a6942d2fdbddb0f71070027c2116c80649313 (dmcphers+openshiftbot@redhat.com)
- Updating usage of the --metrics flag to create a job (cdaley@redhat.com)
- s2i bump related code changes (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  3931979363ccb57da0c66c8aa9bf1a1319e492e5 (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  32c3a25c06670b040d076eb1e5fd6cecf443378c (dmcphers+openshiftbot@redhat.com)
- deploy: generated changes for configurable activeDeadlineSeconds
  (mkargaki@redhat.com)
- deploy: make activeDeadlineSeconds configurable for deployer pods
  (mkargaki@redhat.com)
- HAProxy Router: Add option to use PROXY protocol (miciah.masters@gmail.com)
- Add wildfly image stream to maven pipeline example (cewong@redhat.com)
- Make the DIND image creation script executable (skuznets@redhat.com)
- Fix irrelevant error messages during dind setup (danw@redhat.com)
- bump(github.com/openshift/origin-web-console):
  232ddec5343216575c90a69452e167f51efe1bde (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d0e340c5a1144fc04b3cf2c15af7a8b12970e482 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  247492a613162b594d88664baab8ec0fe479912b (dmcphers+openshiftbot@redhat.com)
- Show only project name when using the short option (chmouel@chmouel.com)
- regenerate man page for rsh (mfojtik@redhat.com)
- enable deployments and replica sets in rsh (mfojtik@redhat.com)
- deployments: lowercase the progress messages for deployment configs to match
  upstream (mfojtik@redhat.com)
- Don't mention internal error when docker registry is unreachable
  (mmilata@redhat.com)
- Remove `$TERM` export from our Bash library (skuznets@redhat.com)
- Introduce RestrictUsersAdmission admission plugin (miciah.masters@gmail.com)
- bump(github.com/openshift/origin-web-console):
  8e405523fe7ca626000bbd6fbb69ad79c1fce453 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cfc61cde705639c0d7e23e92c9329e0176d17f65 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2446d7f3b0e38786bb912c0a6ea978eacffd16f3 (dmcphers+openshiftbot@redhat.com)
- Test{NewAppSourceAuthRequired,Dockerfile{Path,From}}: create temp dir at the
  right location. (vsemushi@redhat.com)
- Updated image stream templates and db-templates (rymurphy@redhat.com)
- bump(github.com/openshift/origin-web-console):
  076ed5a47ef7759362bd0418f291625689b1a68a (dmcphers+openshiftbot@redhat.com)
- rebase (li.guangxu@zte.com.cn)
- deploy: revert proportional recreate timeout and default to 10m
  (mfojtik@redhat.com)
- new-app/new-build/process: read envvars/params from file (mmilata@redhat.com)
- deploy: fix timeoutSeconds for initial rolling rollouts (mfojtik@redhat.com)
- bump(github.com/joho/godotenv): 4ed13390c0acd2ff4e371e64d8b97c8954138243
  (mmilata@redhat.com)
- deploy: make retryTimeout proportional to deployer Pod startTime
  (mfojtik@redhat.com)
- Add hack/build-dind-images.sh (marun@redhat.com)
- bump(github.com/openshift/origin-web-console):
  df2b5b3e01bd65d3ecfa805585ca4bffdf7ae4be (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2206b62d538a3afbfac07ed08d23cdf6fb270efe (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  43e511fc80cbf3a7b25dd112da0157d7943d88d6 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  848b7943baad8af222451bf2ff6c3f8100671e9f (dmcphers+openshiftbot@redhat.com)
- Run hack/update-generated-completions.sh and hack/update-generated-docs.sh
  (vsemushi@redhat.com)
- oadm ca, oadm create-node-config, oadm create-api-client-config, openshift
  start: add --expire-days and --signer-expire-days options.
  (vsemushi@redhat.com)
- Run all verification in Makefile rather than exiting early
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9ab85d93337833b591be71cc4b94aa8240436fbb (dmcphers+openshiftbot@redhat.com)
- Improve ipfailover configurability (pcameron@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2ab961f7c76e889a3239c3debfcb02477ff666e3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cbbfb2e773ba326043ab3ac06e7bca03be293522 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7243a21adfb252f2e0d401c9d25394067b72f3d7 (dmcphers+openshiftbot@redhat.com)
- oc process: fix go template output, add jsonpath (mmilata@redhat.com)
- router: Minimize reloads for removal and filtering (marun@redhat.com)
- Review feedback from builds (ccoleman@redhat.com)
- router: Fix detection of initial sync (marun@redhat.com)
- router: Ensure reload on initial sync (marun@redhat.com)
- bump(github.com/openshift/origin-web-console):
  998521beaf100476eaede2a9c1fbd37a65320735 (dmcphers+openshiftbot@redhat.com)
- router: bypass the rate limiter for the initial commit (marun@redhat.com)
- Fix broken router stress test (marun@redhat.com)
- Turn on jUnit output by default for `make` targets (skuznets@redhat.com)
- fix for bz1400609; if the node status flips on the order of ip addresses
  (when there are multiple NICs to report), do not let the SDN chase it
  (rchopra@redhat.com)
- generated: protobuf definition changes in go 1.7 due to tar changes
  (ccoleman@redhat.com)
- UPSTREAM: <drop>: Handle Go 1.6/1.7 differences in upstream
  (ccoleman@redhat.com)
- Make go 1.7 the default build tool for the release (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  617df3f22248be58636641dc4e7573c03e979b2e (dmcphers+openshiftbot@redhat.com)
- Update docs wrt multiple --env/--param arguments (mmilata@redhat.com)
- Suggest oadm drain instead of oadm manage-node drain (mfojtik@redhat.com)
- oc cluster up: work around docker attach race condition (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3e63c9c5cc314777ca9306b2396093acd9466746 (dmcphers+openshiftbot@redhat.com)
- Punctuation corrected (aktjha@gmail.com)
- Redo isolation OVS rules (danw@redhat.com)
- Split out multitenant-specific and single-tenant-specific SDN code
  (danw@redhat.com)
- Renumber OVS tables (danw@redhat.com)
- Remove useless OVS-related error returns (danw@redhat.com)
- Make the OVS flow tests more generic (danw@redhat.com)
- missed punctuation (aktjha@gmail.com)
- Use the new build logic in *-build-images (ccoleman@redhat.com)
- Add a common function for building images supporting imagebuilder
  (ccoleman@redhat.com)
- Update to Go 1.7.4 in the spec (ccoleman@redhat.com)
- Fix formatting (dmcphers@redhat.com)
- bump(github.com/openshift/origin-web-console):
  8f964a8d439d7a6fbecf10dd9d416e1a76a1684c (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3579a803486cd3d23e7559814d627e607ee28b62 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  50c1d5e4f657ec5b92c3f332788fac3101b3f1e6 (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: opencontainers/runc: 1216: Fix thread safety of SelinuxEnabled and
  getSelinuxMountPoint (pmorie@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a3a3d3925ad674948fdfb8b8c85a390c63d5062d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d7af2d96749fe46359b3d5f977131a408de8725d (dmcphers+openshiftbot@redhat.com)
- more debug for failing db queries (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9be69b89076bb4b44f88a89faecf7e65cadc8ca7 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  1265ebcb846113e5471da1149b69a4e9ff45f05e (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  1fb702b27ad4f2c47cbd791122555ed14afd7094 (dmcphers+openshiftbot@redhat.com)
- Add `test-extended` target to the Makefile (skuznets@redhat.com)
- Provide the directory for Ginkgo jUnit output explicitly
  (skuznets@redhat.com)
- Logs wait for first build from bc with ConfigChange trigger
  (jupierce@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d9143865d5db98b4031688692d19cc377db467f4 (dmcphers+openshiftbot@redhat.com)
- Fix excluder incorrectly creating exclude line. (tdawson@redhat.com)
- Add advanced pipeline examples (cewong@redhat.com)
- Fixed Bashisms and temporary directory use in kubeconfig tests
  (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  10c6ca8502411aaecd08360233749493c2915fc8 (dmcphers+openshiftbot@redhat.com)
- rework build list order for oc status (gmontero@redhat.com)
- generated man pages and completetion (mfojtik@redhat.com)
- update extended test and add test cmd for retry (mfojtik@redhat.com)
- deploy: add retry subcommand for rollout (mfojtik@redhat.com)
- deploy: update doc for maxUnavailable (mkargaki@redhat.com)
- Seed math/rand on start (jliggitt@redhat.com)
- UPSTREAM: 38339: Exponential back off when volume delete fails
  (gethemant@gmail.com)
- Add List to token client (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e06dfb55f9d0ee29f2da7db9243e695e4c759acd (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: 37009: fix permissions when using fsGroup (sjenning@redhat.com)
- bump(github.com/openshift/origin-web-console):
  eee4d13f8fca1f0777df49bf352047ebdfa45119 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d257d664947af519bcb0cbaf990ca304a2b4e432 (dmcphers+openshiftbot@redhat.com)
- new-app hidden imagestreams: fix behaviour when no tag is specified
  (jminter@redhat.com)
- add test for s2i source fetch failure (ipalade@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b959663a3ee4d00f16ca0ee7144f795356a09bf4 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e28544ec35bcf585416c1bfc92c74a6235aac2cb (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c9b7feb34a35f6ca88158ee381c6a5b991befb7f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  33553e5d5a87b324287aa68a681f3198d33b384a (dmcphers+openshiftbot@redhat.com)
- generate man and bash completion (mfojtik@redhat.com)
- deploy: use rollout cancel in extended test (mfojtik@redhat.com)
- deploy: deprecate --enable-triggers in favor of set triggers
  (mfojtik@redhat.com)
- deploy: add rollout cancel command and deprecate deploy --cancel
  (mfojtik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  8fd9c66ca45a40d134a941448b1718d80b998f3a (dmcphers+openshiftbot@redhat.com)
- Prevent jenkins from being killed prematurely (wtrocki@redhat.com)
- UPSTREAM: 38196: fix mesos unit tests (mkargaki@redhat.com)
- Review 1: Comments and bashisms (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a9f4523243228229790c7c39375c0a128d743cdc (dmcphers+openshiftbot@redhat.com)
- add plugin ext test for build clone; verify build triggeredBy; fix build
  clone endpoint setting of triggered by (gmontero@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d264ce48c34d113f5d774f32be52401ae7ad9418 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e024781eb6f4272e66ffc63561ca9c5d63b33027 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a8bd1148758925ca3b5bd366a92b82c0bc86fe73 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  8baf00b8624ff918a4c754f01c6fba48e6bc62a0 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f697f5017e25cf30e9d5d263568e21c060a6b981 (dmcphers+openshiftbot@redhat.com)
- Wait for old pods to terminate before proceeding to Recreate
  (mkargaki@redhat.com)
- bump(github.com/openshift/origin-web-console):
  99070c15973a5714a3b2826b612f20a462cca0e8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  35b232328cb1dc92fe16b74a4644ab5b495e029d (dmcphers+openshiftbot@redhat.com)
- fix typo (yu.peng36@zte.com.cn)
- UPSTREAM: 38137: glusterfs: Fix all gid types to int to prevent failures on
  32bit systems (obnox@samba.org)
- bump(github.com/openshift/origin-web-console):
  2117097e332b8dea4cd0507439dae217cf39f7d9 (dmcphers+openshiftbot@redhat.com)
- Use default cert dir for oc cluster up client if DOCKER_TLS_VERIFY is set
  (jimmidyson@gmail.com)
- openshift/origin-release: install openssl. (vsemushi@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4fd08fea26309fa05100480ce088ac11b5b54ea8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  aa5d310211320d1131ed12f5ad7f9b8e35b70871 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6cbd1a7796abc2ffb0008f6045dc70ca502d0e4a (dmcphers+openshiftbot@redhat.com)
- deploy: generated changes for lastUpdateTime (mkargaki@redhat.com)
- deploy: bring deployment config conditions on par with upstream
  (mkargaki@redhat.com)
- Increase timeouts for idling extended test (mfojtik@redhat.com)
- deploy: cleanup strategy code (mkargaki@redhat.com)
- make /sys/devices/virtual/net r/w for kubelet under oc cluster up
  (jminter@redhat.com)
- UPSTREAM: 37886: glusterfs: implement GID security in the dynamic provisioner
  (obnox@redhat.com)
- bump(github.com/heketi/heketi):28b5cc4cc6d2b9bdfa91ed1b93efaab4931aa697
  (hchiramm@redhat.com)
- Use upstream path segment name validation (jliggitt@redhat.com)
- Compare object DN to structured baseDN (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  8bca523d03e6434245744e16f08194f17baa70bd (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: 37721: Fix logic error in graceful deletion (decarr@redhat.com)
- UPSTREAM: 37649: Fix top node (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ac395f8a59a771f5c1cedaa3bed0ec97057bb996 (dmcphers+openshiftbot@redhat.com)
- Reconcile deleted namespaces out of cluster quota status
  (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  281de6b73177b588a76940f6c96acbb4d2313fce (dmcphers+openshiftbot@redhat.com)
- new-app: appropriately warn/error on circular builds (gmontero@redhat.com)
- generated: docs (ccoleman@redhat.com)
- Add `oc serviceaccounts create-kubeconfig` to simplify bootstrapping
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9e5a65b9d95a76f10abebc9a59a4d355b4e24641 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  964762894db8c9cc9e4d94856f4e1c31b08d62ea (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  642c6f354adaeaea8651db8e9c798b2b07ca4ae7 (dmcphers+openshiftbot@redhat.com)
- build gitserver image FROM origin, not origin-base (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4aaf5da4600881a7d63ef8ce7a519c73d04bd118 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/docker/distribution): Add oss storage driver
  (agladkov@redhat.com)
- Enable oss storage driver (agladkov@redhat.com)
- oc new-app support for "hidden" tag in imagestreams (jminter@redhat.com)
- generated: docs (ccoleman@redhat.com)
- Mirror blobs to the local registry on pullthrough (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6aabd724a1069c5b95a301db5eede6c7171549d0 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e5dcaf2e91b1d22e610a66cd63d546ca9c3448e1 (dmcphers+openshiftbot@redhat.com)
- bump(gopkg.in/ldap.v2): 8168ee085ee43257585e50c6441aadf54ecb2c9f
  (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6ea5608efac317565723c6ecf28030b3f0fec8b9 (dmcphers+openshiftbot@redhat.com)
- [BZ1394716] Report false diagnostic message for curator-ops DeploymentConfig
  (jcantril@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0eb6441b19746ea39df494bc8ad7220a473fa6df (dmcphers+openshiftbot@redhat.com)
- Changing quickstart credentials to secrets (jupierce@redhat.com)
- bump(github.com/openshift/origin-web-console):
  04f331e68ee15916b5f2281b55d892740074e141 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9737260a421e4c459e9f4b45042345a7468f4a4d (dmcphers+openshiftbot@redhat.com)
- added an enviroment variable for balance alg. and ability to disable route
  cookies (jtanenba@redhat.com)
- Removed reference to gssapi variable (rymurphy@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ab6c1a4d04e795ca7ce9fee10c054c497178e740 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c4192691030a79212258d7ff3436b7fba0f011fa (dmcphers+openshiftbot@redhat.com)
- Fix typo introduced in 4b54d01c (mmilata@redhat.com)
- Fail new builds that can't start build pod because it already exists
  (mmilata@redhat.com)
- Add missing arguments to glog.Infof (mmilata@redhat.com)
- bump(github.com/openshift/origin-web-console):
  26fea747e4dac8b25338c07c4c9c6acff9c1b82e (dmcphers+openshiftbot@redhat.com)
- add some optimiztion for new-build command (li.guangxu@zte.com.cn)
- Fix excluder usage bug (tdawson@redhat.com)
- set env vars on oc new-app of template (gmontero@redhat.com)
- UPSTREAM: revert: 734a79b: docker/docker: <carry>: WORD/DWORD changed
  (jminter@redhat.com)
- Implement inscureEdgeTermination options for reencrypt and pasthrough routes
  reencrypt routes work the same as edge routes with Allow, Redirect, and None
  (jtanenba@redhat.com)
- Consideration of imagePullPolicy on lifecycle hook execution
  (roy@fullsix.com)
- bump(github.com/openshift/origin-web-console):
  d4a5a52687e9324dc8c898967b4b133c5017259e (dmcphers+openshiftbot@redhat.com)
- bump(golang.org/x/sys) 8d1157a435470616f975ff9bb013bea8d0962067
  (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  eea002ef608401acc426406d835431e8dd30a527 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5a88c56d465a99b267c59f5c0f9879158f04e197 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b503ddd5e3531fc01d415a55d76980fbecf4ea86 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3e75b27f3c8defc1e22cfed22a7e8e642a24ee1b (dmcphers+openshiftbot@redhat.com)
- add failure reasons (ipalade@redhat.com)
- Remove github.com/RangelReale from preload-remote list (jliggitt@redhat.com)
- Test OAuth state encoding (jliggitt@redhat.com)
- bump(github.com/RangelReale/osin): 1c1a533224dd9c631fdd8df8851b167d24cabe96
  (jliggitt@redhat.com)
- Fix godoc comments and typo in command description. (vsemushi@redhat.com)
- Extend commitchecker to call hack/godep-restore.sh when needed
  (maszulik@redhat.com)
- Add preloading google.golang.org/cloud to godep-restore.sh
  (maszulik@redhat.com)
- bump(github.com/jteeuwen/go-bindata):
  bfe36d3254337b7cc18024805dfab2106613abdf (maszulik@redhat.com)
- bump(github.com/onsi/ginkgo): 74c678d97c305753605c338c6c78c49ec104b5e7
  (maszulik@redhat.com)
- bump(github.com/docker/docker): b9f10c951893f9a00865890a5232e85d770c1087
  (maszulik@redhat.com)
- bump(github.com/docker/distribution):
  12acdf0a6c1e56d965ac6eb395d2bce687bf22fc (maszulik@redhat.com)
- bump(github.com/openshift/source-to-image):
  5741384e376d9c61b5b36156003ede6698ca563b (maszulik@redhat.com)
- bump(github.com/containernetworking/cni):
  52e4358cbd540cc31f72ea5e0bd4762c98011b84 (maszulik@redhat.com)
- bump(k8s.io/kubernetes): a9e9cf3b407c1d315686c452bdb918c719c3ea6e
  (maszulik@redhat.com)
- bump(k8s.io/client-go): d72c0e162789e1bbb33c33cfa26858a1375efe01
  (maszulik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  14fe43790c0b1b3f45f03177ef49365d56062e29 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ec1d6de5eab9d5d5d1ab4fb7afb303b5c4e4bf7c (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4d79ddb41a7c4dd1deae999cce2cbb60595c4421 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cf4e10786748312a930219b8da77e24856685f5a (dmcphers+openshiftbot@redhat.com)
- add controller to regenerate service serving certs (deads@redhat.com)
- update canRequestProjects check to include list,create (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4cd45b9fdfd65daa561f672fe90bfd1c32ee3e45 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b94910ff08fdeac83f1eadb2649bfd68b17d9b74 (dmcphers+openshiftbot@redhat.com)
- Adding extended tests for buildconfig postCommit (jupierce@redhat.com)
- Better formatting for jenkinsfile example (dmcphers@redhat.com)
- Fix typos (rhcarvalho@gmail.com)
- deploy: drop unnecessary resource handlers to reduce dc requeues
  (mkargaki@redhat.com)
- Move verify-upstream-commits to a separate make target (maszulik@redhat.com)
- oc: show ready pods next to deployments (mkargaki@redhat.com)
- Fail hard when the commit checker finds no Git repo (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f892e0aa156399e563c9ff92ba43f87135afcd03 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b8f3206572b689e1c899c19e30dfba60d9e9d585 (dmcphers+openshiftbot@redhat.com)
- Copy creationTimestamp from the image (mfojtik@redhat.com)
- Include createrepo in release images (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  151dc5f077ce608cf0239a94ca1adf6d7aac0689 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9061893ef691e6ca2ae13383f1eb71a74442d662 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  66ae612a7b33a79b2e537eff1d2ac1ddf602086f (dmcphers+openshiftbot@redhat.com)
- Fix a multiple-pointers-to-single-loop-variable bug in EgressNetworkPolicy
  (danw@redhat.com)
- Added logic to save JUNIT log with ENV vars (rymurphy@redhat.com)
- bump(github.com/Microsoft/go-winio) 24a3e3d3fc7451805e09d11e11e95d9a0a4f205e
  (jminter@redhat.com)
- Update ose_images.sh - 2016-11-28 (tdawson@redhat.com)
- Regen swagger spec (agoldste@redhat.com)
- UPSTREAM: <carry>: Remove DeprecatedDownwardAPIVolumeSource from protobuf
  (agoldste@redhat.com)
- bump(github.com/openshift/origin-web-console):
  75f0b8d879fac596173dd3735e4ee96e16c9feb2 (dmcphers+openshiftbot@redhat.com)
- added block arguments to remove jenkins deprecation warnings
  (matthias.luebken@gmail.com)
- add *.csproj support to examples/gitserver/hooks/detect-language
  (jminter@redhat.com)
- bump(github.com/Azure/go-ansiterm) 7e0a0b69f76673d5d2f451ee59d9d02cfa006527
  (backwards) (jminter@redhat.com)
- fix the mistake link type (yu.peng36@zte.com.cn)
- Use responsive writer only in help (ffranz@redhat.com)
- Switch to internalclientset - interesting changes (maszulik@redhat.com)
- Switch to internalclientset - boring changes (maszulik@redhat.com)
- rebase and add some change as specified (li.guangxu@zte.com.cn)
- rename jenkins extended test file (bparees@redhat.com)
- Move test suite extended/cmd/oc-on-kube into extended/cmd.
  (vsemushi@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d5fa2bbc04c34b74fcd95c8b8c8e3335e13fada8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  46dd41331363efaf22714b1d6af6c533db31d111 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  339a32eff93ba3a1298717fe2e9f82f55ea0d884 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2889c1d747406b85291102cdbf33faa0f3b4fbd9 (dmcphers+openshiftbot@redhat.com)
- Migrate build environment utilities from `common.sh` (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2a982a15c90a7b5da47aaab58fb50a952124a82e (dmcphers+openshiftbot@redhat.com)
- Deprecate process -v/--value in favor of -p/--param (jupierce@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b0c62bb12e51bb660bc68cbcee5b6c15eebd3dc4 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  95b0902ecb3627301fedf2a0a6855cbd5e8c39a2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  bc496f8b3e52ad0e6ea5f1e0caaccbd0e60e6850 (dmcphers+openshiftbot@redhat.com)
- make login, project, and discovery work against kube with RBAC enabled
  (deads@redhat.com)
- UPSTREAM: 37296: Fix skipping - protobuf fields (agoldste@redhat.com)
- bump(github.com/openshift/origin-web-console):
  da4a37d40751c459a7d0fad33ab92006efc14f78 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  72e0f59571cef3b9af904088bdbc4e2154d6c6d3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7389ce5638dfe4078a7ac24f6e2fd8e976e5c819 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  23682f14ee9a19931c72c106ed9c6a781b1bfcab (dmcphers+openshiftbot@redhat.com)
- Redirect to server root if login flow is started with no destination
  (jliggitt@redhat.com)
- fix image input extended test (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a60cd15356e51166f4e7a8d5b06760b003edcbd5 (dmcphers+openshiftbot@redhat.com)
- dind: Remove mention of br_netfilter from docs (marun@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cd4bfdc1870fc1edbce797833d7c231c7e9b3bfd (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  843d4aee83dc149fe9271f2cb403512c85bbe5c8 (dmcphers+openshiftbot@redhat.com)
- add jenkins plugin create/delete obj test; allow for jenkins mem mon disable
  (gmontero@redhat.com)
- bump(github.com/openshift/origin-web-console):
  82519db788b66218445f600dd50f22d5e8dec98f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  00e62d07a86341f986d36a3fda9effb89bbdd4f5 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  07653ad748a18fd5e55a10c94f7201916cda9a9f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  be993532e28dae2843df42ac5a5c234c05533ea1 (dmcphers+openshiftbot@redhat.com)
- Bug 1339754 - Fix tag sorting according to semantic versioning rules
  (maszulik@redhat.com)
- Remove references to clientset 1_3 (ccoleman@redhat.com)
- Remove generated v1_3 and v1_4 clients (ccoleman@redhat.com)
- generated: clients for release 1.5 (ccoleman@redhat.com)
- new-app: fix priority of Jenkinsfile, Dockerfile, source when strategy
  unspecified (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9686826940b7a6b7f996fefa5e80ed7ceb611fd1 (dmcphers+openshiftbot@redhat.com)
- prevent test/cmd/config.sh from writing config to working dir
  (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  68cce31e00c7fc8ea315ab0903fddecfd6fb0caf (dmcphers+openshiftbot@redhat.com)
- Migrated tests for login from hack/test-cmd.sh preamble (skuznets@redhat.com)
- Support HTTP URLs in oc start-build --from-file (mmilata@redhat.com)
- Support csproj files for identifying .NET Core projects (jminter@redhat.com)
- bump(github.com/openshift/origin-web-console):
  402dd2272fbd495b5e4cc54212671d605a51fbc7 (dmcphers+openshiftbot@redhat.com)
- create printMarkerSuggestions func (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6b5b66af4653f75de791c4a50107b63bc18992d0 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  0824fe472aafc97455b7e12f617e1dff09721a4f (dmcphers+openshiftbot@redhat.com)
- Updated DIND scripts to use the new `os::util::find` methods
  (skuznets@redhat.com)
- Updated `hack/update-generated-docs.sh` to use new util functions
  (skuznets@redhat.com)
- Moved documentation generation functions from common.sh (skuznets@redhat.com)
- Refactored to use the `os::util::find` methods where necessary
  (skuznets@redhat.com)
- Declared the need for `sudo` and use it correctly in extended tests
  (skuznets@redhat.com)
- Refactored scripts to use new methods for $GOPATH binaries
  (skuznets@redhat.com)
- Refactored scripts to use `os::util::ensure::iptables_privileges_exist`
  (skuznets@redhat.com)
- Refactored to use `os::util::ensure::system_binary_exists`
  (skuznets@redhat.com)
- Refactored scripts to use binaries directly now that they're in PATH
  (skuznets@redhat.com)
- Updated scripts to use `os::util::ensure::built_binary_exists`
  (skuznets@redhat.com)
- Implemented Bash methods to search for binaries and ensure they exist
  (skuznets@redhat.com)
- Removed old methods used for finding binaries, etc (skuznets@redhat.com)
- Added PATH change to hack/lib/init.sh so all scripts have it
  (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7e9009da2339e5745fc7f6419edb0ed15d406b71 (dmcphers+openshiftbot@redhat.com)
- sdn: garbage-collect dead containers to recover IPAM leases (dcbw@redhat.com)
- sdn: clean up pod IPAM allocation even if we don't have a netns
  (dcbw@redhat.com)
- update missing probe severity to info (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  29241d57543c32458776e376175c9abc119e34c3 (dmcphers+openshiftbot@redhat.com)
- patch dcs and rcs instead of update (jvallejo@redhat.com)
- filter secret mount check if secret cannot be listed (jvallejo@redhat.com)
- Add security response info (sdodson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ca4be237df6935819e795eeb2962e985230876e1 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f43ec95079a848d38637f40f6784f0d58cb4f952 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  98bd4719ec7eccc390cacce9defbffc231d0ccf6 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5e199bb407bb409d6ad063a6d8075567e714bcb3 (dmcphers+openshiftbot@redhat.com)
- Adding extended tests for Jenkins freestyle exec (jupierce@redhat.com)
- bump(github.com/openshift/origin-web-console):
  589a660321721216d285beb350165df9b7a61655 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cf48ed9137425ab9fe49fede1726937a92b86ea5 (dmcphers+openshiftbot@redhat.com)
- bump(k8s.io/kubernetes): a9e9cf3b407c1d315686c452bdb918c719c3ea6e
  (agoldste@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c21f7f6a483dc1396e0dc2d578253194bbdfa4a3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  faa5ed6218cd0062692139901b1e88594c1273e9 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  26e4d1f374d4f03d524212dcff8b4d3f6aa43551 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  28c791a33969bac880c3680767d8057d364956fc (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9f649e9c36bece2f9b73b49a98b208c3f94c4426 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  f839c85b5306ff210d6d7bd6e8c344b4a0bfd146 (dmcphers+openshiftbot@redhat.com)
- Fix issues with Godeps.json (agoldste@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9b21516783e1ca59e72d3b2cad66fdf915fa91b8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b446eb8f12af505b2c52fbad5925ca9e2c8c7d66 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ddad4dd4e800dcfbf80178af2dc9129e48dabdd4 (dmcphers+openshiftbot@redhat.com)
- straight move (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e94bc6c50d52fa4e697a0b63d3c2539b38197ce0 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d0a5912a82684aaa78d6759186444f3305582694 (dmcphers+openshiftbot@redhat.com)
- mark nodejs 0.10 image as deprecated (bparees@redhat.com)
- Fix bad format in README.md (zhao.xiangpeng@zte.com.cn)
- Memory monitoring for jenkins during extended tests (jupierce@redhat.com)
- Add OVS tests to exclusion list (agoldste@redhat.com)
- Expand scope of skipping kube federation tests (agoldste@redhat.com)
- Disable kube garbage collector tests (agoldste@redhat.com)
- Allow deployment controller to update pods (agoldste@redhat.com)
- Added a check to prevent pulling scratch (rymurphy@redhat.com)
- Add support for github teams (jliggitt@redhat.com)
- Allow all users to exec protoc in release images (ccoleman@redhat.com)
- Fixes bug 1395545 [link](https://bugzilla.redhat.com/show_bug.cgi?id=1395545)
  empty the pool, or delete the pool when endpoints are deleted
  (rchopra@redhat.com)
- UPSTREAM: 36779: fix leaking memory backed volumes of terminated pods
  (sjenning@redhat.com)
- Fix the command to restart docker on 1.3->1.4 upgrade (danw@redhat.com)
- Reap OAuthClientAuthorizations (jliggitt@redhat.com)
- Remove camel-casing on oauth client API calls (jliggitt@redhat.com)
- Reconfigured test-cmd to continue on failure (skuznets@redhat.com)
- Validate if the openshift master is running with mutitenant network plugin
  (zhao.xiangpeng@zte.com.cn)
- bump(*):remove unused _test.go files (ipalade@redhat.com)
- New-app/new-build support for pipeline buildconfigs (jminter@redhat.com)
- newapp: do not fail when file exists with same name as image
  (mmilata@redhat.com)
- Added error check for naming collisions with build (rymurphy@redhat.com)
- Fixed the SYN eater tests so they have enough privilege (bbennett@redhat.com)
- jenkins master/slave cleanup; fix job xml now that ict is auto==false
  (gmontero@redhat.com)
- Allow to unlink deleted secrets from a service account (mfojtik@redhat.com)
- Add router option to bind ports only when ready (marun@redhat.com)
- UPSTREAM: docker/distribution: 2008: Honor X-Forwarded-Port and Forwarded
  headers (miminar@redhat.com)
- diagnostics: add shell prompt to commands in msgs (lmeyer@redhat.com)
- diagnostics: make cluster role warning info, modify text (lmeyer@redhat.com)
- diagnostics: clarify when logging not configured (lmeyer@redhat.com)
- Added a mention of TEST_ONLY to extended test doc (rymurphy@redhat.com)
- pkg/quota/controller: Fix typo in file name (rhcarvalho@gmail.com)
- test: retry rollout latest on update conflicts (mkargaki@redhat.com)
- default resources for the build (haowang@redhat.com)
- Squash to a single commit (zhao.sijun@zte.com.cn)
- Drop the merge commits and update this (zhao.sijun@zte.com.cn)
- The func 'RequestForConfig' isn't used in the project
  (miao.yanqiang@zte.com.cn)
- Add a missing import to origin custom tito tagger. (dgoodwin@redhat.com)

* Mon Nov 28 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.30
- Update ose_images.sh - 2016-11-23 (tdawson@redhat.com)
- UPSTREAM: 36444: Read all resources for finalization and gc, not just
  preferred (maszulik@redhat.com)

* Wed Nov 23 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.29
- Merge remote-tracking branch upstream/master, bump origin-web-console 35b920b
  (tdawson@redhat.com)
- sdn: garbage-collect dead containers to recover IPAM leases (dcbw@redhat.com)
- sdn: clean up pod IPAM allocation even if we don't have a netns
  (dcbw@redhat.com)
- Update ose_images.sh - 2016-11-18 (tdawson@redhat.com)

* Fri Nov 18 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.28
- bump(k8s.io/kubernetes): a9e9cf3b407c1d315686c452bdb918c719c3ea6e
  (agoldste@redhat.com)
- Fix issues with Godeps.json (agoldste@redhat.com)
- Cherry-pick of https://github.com/openshift/origin/pull/11940 by @rajatchopra
  (commit a631fd33a4b6d079cd76951ea5fa082f3960c90c) (bbennett@redhat.com)
- Fix the command to restart docker on 1.3->1.4 upgrade (danw@redhat.com)
- Update ose_images.sh - 2016-11-16 (tdawson@redhat.com)
- Add OVS tests to exclusion list (agoldste@redhat.com)
- Expand scope of skipping kube federation tests (agoldste@redhat.com)
- Disable kube garbage collector tests (agoldste@redhat.com)
- Allow deployment controller to update pods (agoldste@redhat.com)

* Wed Nov 16 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.27
- oc convert tests (ffranz@redhat.com)
- Fix SDN startup ordering (again) (danw@redhat.com)
- UPSTREAM: 36603: fixes handling lists in convert (ffranz@redhat.com)
- Do not use whoami inside of start scripts (ccoleman@redhat.com)
- We should not be able to create a route when the host is not specified and
  wildcardpolicy is enabled. Fixes bug 1392862 -
  https://bugzilla.redhat.com/show_bug.cgi?id=1392862 Rework as per @liggitt
  review comments. Fix govet issue. (smitram@gmail.com)
- Accept docker0 traffic regardless of firewall (danw@redhat.com)
- updating (cdaley@redhat.com)
- Force image in test-end-to-end-docker.sh for ose (tdawson@redhat.com)
- Warn on login when user cannot request projects (jvallejo@redhat.com)
- Rescue panic (jliggitt@redhat.com)
- Update ose_images.sh - 2016-11-14 (tdawson@redhat.com)
- Wait for remote API response before return in UploadFileToContainer
  (jminter@redhat.com)
- f5 poolname fix (rchopra@redhat.com)
- Increase retained CI log size to 100M (agoldste@redhat.com)
- Fix SRV record lookup for ExternalName service (yhlou@travelsky.com)

* Mon Nov 14 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.26
- bump(github.com/openshift/origin-web-console):
  3d8c136b9089d687db197eb6c80daf243076c06a (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  44484b3fa93991a6b9d5f4121eda94600ef55628 (dmcphers+openshiftbot@redhat.com)
- Update the TTY detection logic in Bash text utils (skuznets@redhat.com)
- oc get templates: print only first description line (mmilata@redhat.com)

* Fri Nov 11 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.25
- bump(github.com/openshift/origin-web-console):
  d5d4a253ad5c6e1be4bb06ccdcb255feb7b41bb2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cc2bd92ae1cb470a5d09121b0bbf92f5e52fb619 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a8c369b3f0a87ca757f179d13ae7e48cce0f9c86 (dmcphers+openshiftbot@redhat.com)
- List events for unidling controller (jliggitt@redhat.com)
- Change default to etcd2 (jliggitt@redhat.com)
- bump(github.com/openshift/origin-web-console):
  bb443db5dae2de44042f8cafb0c0b01000f1d1d1 (dmcphers+openshiftbot@redhat.com)
- set automatic to false for the dev DC deployment (bparees@redhat.com)
- Move test case TestGenerateGateway to common_test.go
  (zhao.xiangpeng@zte.com.cn)
- add general build trigger msg and add some other optimizition
  (li.guangxu@zte.com.cn)
- Fix for bugz https://bugzilla.redhat.com/show_bug.cgi?id=1392862 - don't
  allow wildcard policy if host is not specified. (smitram@gmail.com)
- Fix for bugz 1393262 - serve certs for wildcard hosts. (smitram@gmail.com)
- Add missing permission when running 'oc cluster up --metrics'
  (mwringe@redhat.com)
- add test/cmd test (jvallejo@redhat.com)
- UPSTREAM: 36541: Remove duplicate describer errs (jvallejo@redhat.com)
- Fix for bugz 1391878 and 1391338 - for multiple wildcard routes asking for
  the same subdomain and in the same namespace, reject newer routes with
  'HostAlreadyClaimed' if paths are different + address @liggitt review
  comments. (smitram@gmail.com)
- fixup man and test for default seccomp directory (sjenning@redhat.com)
- UPSTREAM: 36375: Fix default Seccomp profile directory (sjenning@redhat.com)
- Fix launching number of pods for testing network diagnostics
  (rpenta@redhat.com)
- Fix ordering of SDN startup threads (danw@redhat.com)
- deployments: stop using --follow to verify the env var in test
  (mfojtik@redhat.com)
- Migrated router and registry startup utilities from util.sh
  (skuznets@redhat.com)
- resolve logic errors introduced in #11077 and return 40x errors instead of
  500 errors where possible (jminter@redhat.com)
- deployments: oc rollout latest should not rollout on paused config
  (mfojtik@redhat.com)
- Allow to use star as repository name in imagestreamimport
  (agladkov@redhat.com)
- UPSTREAM: 36386: Avoid setting S_ISGID on files in volumes
  (sjenning@redhat.com)
- Migrated misc method and removed unused method from util.sh
  (skuznets@redhat.com)

* Wed Nov 09 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.24
- require builder image for source-type binary build creation
  (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  abcecfac2a615383455af9441b65aeca2961c7b5 (dmcphers+openshiftbot@redhat.com)
-  fix readme link for extended tests (ipalade@redhat.com)
- Fix for bugz #1389165 - extended route validation breaks included templates.
  Plus fixes as per @liggitt review comments:   o Clean up errors to not leak
  cert/key data.   o Relax checks on certs which have expired or valid in the
  future for     backward compatibility.   o Add tests for expired, future
  valid and valid certs with intermediate     CAs and pass intermediate chains
  to the x509 verifier.   o Improve readability of test config (certs, keys
  etc).   o Fixup error messages to include underlying certificate parse
  errors.   o Add comment and remove currenttime hack. (smitram@gmail.com)
- allow special hostsubnets to force a vnid on egress packets
  (rchopra@redhat.com)
- Bug 1388026 - Fix network diagnostics cleanup when test setup fails
  (rpenta@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2684d16e5b68700f70c4fb3c8ee21e2cc34e3a0d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e93ae824f55ea789a60b0b393affb44d309e187e (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  582f844d34935d922cf6af60b5bafccbe32e305b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  61b1b3f78dc744ff2d5c8e303a5071cb3073a8ff (dmcphers+openshiftbot@redhat.com)
- clarify start-build --from-webhook only meant to work with generic webhook
  (jminter@redhat.com)
- bump(github.com/docker/docker/cliconfig):b9f10c951893f9a00865890a5232e85d770c
  1087 (ipalade@redhat.com)
- bump(github.com/openshift/source-to-image):
  5741384e376d9c61b5b36156003ede6698ca563b (ipalade@redhat.com)
- Fix bugz 1392395 - make regexp match more precise with ^$.
  (smitram@gmail.com)
- Update image-stream warning notices (andrew@andrewklau.com)
- bump(github.com/openshift/origin-web-console):
  35eab4849c4243041a53a5c5803bc30d6b96d4f8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  26ed3049f6169971ab109627d0f56e48e0a347ea (dmcphers+openshiftbot@redhat.com)
- sdn: update for bumped CNI (dcbw@redhat.com)
- bump(github.com/containernetworking/cni):
  52e4358cbd540cc31f72ea5e0bd4762c98011b84 (dcbw@redhat.com)
- sdn/eventqueue: handle DeletedFinalStateUnknown delta objects
  (dcbw@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c6dbf16e5584671d4d8c84343e890c5f3a9327cf (dmcphers+openshiftbot@redhat.com)
- Warn about the right thing on double-pod-teardown (danw@redhat.com)
- Update ose_images.sh - 2016-11-07 (tdawson@redhat.com)
- Migrate scripts to use `os::log::info` (skuznets@redhat.com)
- Migrated SELinux utility functions to the networking suite
  (skuznets@redhat.com)
- fix --host-config-dir, don't download host path from docker container
  (jminter@redhat.com)
- UPSTREAM: 33014: Kubelet: Use RepoDigest for ImageID when available
  (sross@redhat.com)
- UPSTREAM: 33014: Add method to inspect Docker images by ID (sross@redhat.com)
- UPSTREAM: 36248: Fix possible race in operationNotSupportedCache
  (agoldste@redhat.com)
- UPSTREAM: 36249: fix version detection in openstack lbaas
  (sjenning@redhat.com)
- fix extended argument parsing to config building for etcd (deads@redhat.com)
- Remove uninterpreted newline literal from logging functions
  (skuznets@redhat.com)
- update sourceURI used in BuildConfig (li.guangxu@zte.com.cn)
- Fix ip range check condition (zhao.xiangpeng@zte.com.cn)
- UPSTREAM: 34831: cloudprovider/gce: canonicalize instance name when returning
  instance array (dcbw@redhat.com)
- Tolerate being unable to access OpenShift resources in status
  (ccoleman@redhat.com)

* Mon Nov 07 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.23
- bump(github.com/openshift/origin-web-console):
  22cbe94128168282f06b4e52766f05170a77df92 (dmcphers+openshiftbot@redhat.com)
- Deprecated evacuate in favor of drain node (mfojtik@redhat.com)
- Handle services of type ExternalName by returning a CNAME
  (ccoleman@redhat.com)
- fixes extended test issues caused by #11411 (cdaley@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6304150c9696dc4d6cb02e67d1ac42ec39ba4ee8 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6759555895af3481dbda7b92009015e0cdca3b35 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  42d3d3b85544a85b9c9d6fe7e60c09f1ae95173d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a6e3bf3a68da0b710b97d6312752faf5e7267fe2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  62f53fe551ded617e07b7eb9059b7b587e2f36a5 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2896e83370336132433ebb7aa99642dd922b84a0 (dmcphers+openshiftbot@redhat.com)
- avoid repetitive erros on adding fdb entries if it already exists
  (rchopra@redhat.com)
- bump(github.com/openshift/origin-web-console):
  06723a7cec861573be7a0b96c08bc55bdaecd7d4 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4d5a78494e2618f1e5a0da0d7b61922497e1be10 (dmcphers+openshiftbot@redhat.com)
- Refactor uses of `wait_for_command` to use `os::cmd::try_until*`
  (skuznets@redhat.com)
- Migrate scripts to use `os::log::warn` (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  13e9d02b809914e507721d7ea62ec3ce6b9bce48 (dmcphers+openshiftbot@redhat.com)
- Migrate utilities specific to test/cmd/secrets.sh into the test script
  (skuznets@redhat.com)
- Replace old build utility functions with `os::cmd::try_until_text`
  (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  53904fdf20c0b8e188ba56be1a2639952066d20b (dmcphers+openshiftbot@redhat.com)
- Update ose_images.sh - 2016-11-04 (tdawson@redhat.com)
- Allow getting images from registries over untrusted connection
  (agladkov@redhat.com)
- oc start-build --from-repo now uses clone+checkout (rymurphy@redhat.com)
- Added a test for doTestConnection functionality (rymurphy@redhat.com)
- remove set resources from the list of exceptions to the --local flag
  (jtanenba@redhat.com)
- UPSTREAM: 36174: Implemented both the dry run and local flags.
  (jtanenba@redhat.com)
- UPSTREAM: 36174: fixed some issues with kubectl set resources
  (jtanenba@redhat.com)
- UPSTREAM: 36161: Fix how we iterate over active jobs when removing them for
  Replace policy (maszulik@redhat.com)
- integration: rewrite etcd dumper to use new client (mfojtik@redhat.com)
- remove unused go-etcd helper (mfojtik@redhat.com)
- bump(coreos/go-etcd): remove (mfojtik@redhat.com)
- Auto generated docs for NetworkDiagDefaultLogDir description change
  (rpenta@redhat.com)
- Bug 1388025 - Update NetworkDiagDefaultLogDir description (rpenta@redhat.com)
- Correcting log follow user guidance in new-build (jupierce@redhat.com)
- Fix an error variable reuse (miao.yanqiang@zte.com.cn)
- Clarify how we handle compression as a router env (bbennett@redhat.com)
- sdn: don't error deleting QoS if kubelet tears down networking a second time
  (dcbw@redhat.com)

* Fri Nov 04 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.22
- Restore use of oc ex dockerbuild (ccoleman@redhat.com)
- UPSTREAM: openshift/imagebuilder: <drop>: Handle Docker 1.12
  (ccoleman@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6da9b9c706b9bf3b00774835ee8cc4e05dd7ef65 (dmcphers+openshiftbot@redhat.com)
- Fix bugz 1391382 - allow http for edge teminated routes with wildcard policy.
  (smitram@gmail.com)
- bump(github.com/openshift/origin-web-console):
  8aa417ed6584042f46a519be8f688d69cdc45a33 (dmcphers+openshiftbot@redhat.com)
- Placed RPM release in a distinct directory and generated a repository
  (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7a4bd4638a7220d8479f892138ce1973f6803721 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  5f9ad0d846412cf8ae0d51e354248aa776b87f14 (dmcphers+openshiftbot@redhat.com)
- sdn: remove need for locking in pod tests (dcbw@redhat.com)
- bump(github.com/openshift/origin-web-console):
  75f6fe4de4ef6aedbce70280083c79b85b4bd765 (dmcphers+openshiftbot@redhat.com)
- MongoDB replica petset test: increase time of waiting for pods.
  (vsemushi@redhat.com)
- update default subcommand run func (jvallejo@redhat.com)
- UPSTREAM: 35206: update default subcommand run func (jvallejo@redhat.com)
- Test editing lists in oc (mkargaki@redhat.com)
- UPSTREAM: 36148: make edit work with lists (mkargaki@redhat.com)
- Align with other cli descriptions (yu.peng36@zte.com.cn)
- UPSTREAM: 34763: log info on invalid --output-version (jvallejo@redhat.com)
- CleanupHostPathVolumes(): fetch meta info before removing PV.
  (vsemushi@redhat.com)
- Extended deployment timeout (maszulik@redhat.com)
- Cleaned up Bash logging functions (skuznets@redhat.com)
- UPSTREAM: 35285: Remove stale volumes if endpoint/svc creation fails
  (hchiramm@redhat.com)
- Bug 1388026 - Ensure deletion of namespaces created by network diagnostics
  command (rpenta@redhat.com)
- Add new unit tests to cover valid cases where output length is different from
  input length. (avagarwa@redhat.com)
- Fix wrapped word writer for cases where length of output bytes is not equal
  to length of input bytes. (avagarwa@redhat.com)
- Fix to restore os.Stdout. (avagarwa@redhat.com)
- UPSTREAM: 35978: allow PATCH in an API CORS setup (ffranz@redhat.com)
- Add openshift-excluder to origin (tdawson@redhat.com)
- UPSTREAM: 35608: Update PodAntiAffinity to ignore calls to subresources
  (maszulik@redhat.com)
- UPSTREAM: 35675: Require PV provisioner secrets to match type
  (jsafrane@redhat.com)
- Remove redundant constant definition (danw@redhat.com)
- Add permissions to get secrets to pv-controller. (jsafrane@redhat.com)

* Thu Nov 03 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.21
- Bump the version

* Thu Nov 03 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.20
- minor cleanup (rpenta@redhat.com)
- Bug 1390173 - Test more pod to pod connectivity test combinations
  (rpenta@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a51c2d0576902147ba30ad93e4498233d04a36a2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  668739b535bcd16bca6ba7b181939c8f25be6872 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  989f3952453cae0bd25d2f2e2f7337c16fdf7459 (dmcphers+openshiftbot@redhat.com)
- f5 node watch fix - needs a cache to process 'MODIFY' events
  (rchopra@redhat.com)
- bump(github.com/openshift/origin-web-console):
  109b88081b48b1f5f70b7386ff3a8a40e5129ce7 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7862d494be717042245e49b8047b12cb8b5839f0 (dmcphers+openshiftbot@redhat.com)
- Update router debugging instructions (jawnsy@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d7146b50996a5d5e95220613a884fa30a1fb4f65 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  42f3dc01d752b49dfa02389e8f231ee7b6220304 (dmcphers+openshiftbot@redhat.com)
- tests: wait_for_registry: use oc rollout status (mmilata@redhat.com)
- bump(github.com/openshift/origin-web-console):
  00eb12fca5c8009191fecbb4093b969c35886142 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d4bfaeec71e263087e817d61b274f94d0227fd45 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6ab1616d931e6ea0d9fbb0239f728139d3a0ec86 (dmcphers+openshiftbot@redhat.com)
- Allow pv controller to recycle pvs, watch recycler pod events
  (mawong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  71202680a49368e6a72bdfe52f5cb558cb4d60f5 (dmcphers+openshiftbot@redhat.com)
- bump build pod admission test timeout (bparees@redhat.com)
- Update ose_images.sh - 2016-11-02 (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  a0c089fff75cfee4a223497d9114eee2f35db6c3 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  40f7e508b443b64307c068335c5a55faaaa32d5c (dmcphers+openshiftbot@redhat.com)
- Fix creation of macvlan interfaces (danw@redhat.com)
- Update Swagger documentation generator script name (skuznets@redhat.com)
- test: wait for frontend rollout before getting app logs (mkargaki@redhat.com)
- deploy: default maxSurge/maxUnavailable when one is set to zero
  (mkargaki@redhat.com)
- fix error - cannot list all services in the cluster (rchopra@redhat.com)
- dind: make /run a shared mount (dcbw@redhat.com)
- Drop unused add_macvlan code from openshift-sdn-ovs (danw@redhat.com)
- Merging jenkins plugin test templates into one (jupierce@redhat.com)
- Use existing kube method to fetch the container ID (rpenta@redhat.com)
- Bug 1389213 - Fix join/isolate project network (rpenta@redhat.com)
- provide vxlan integration options to the router cmd line (rchopra@redhat.com)
- sdn: fix network-already-set-up detection (dcbw@redhat.com)
- sdn: run pod manager server forever (dcbw@redhat.com)
- oc: update short desc for rollout (mkargaki@redhat.com)
- fix bz1389267 - release subnet leases upon hostsubnet delete
  (rchopra@redhat.com)
- sdn: wait for kubelet network plugin init before processing pods
  (dcbw@redhat.com)
- sdn: start pod manager before trying to update if VNIDs have changed
  (dcbw@redhat.com)
- Fix a bug in the egress router README (danw@redhat.com)
- Check port range for IP Failover configuration (zhao.xiangpeng@zte.com.cn)

* Wed Nov 02 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.19
- Merge remote-tracking branch upstream/master, bump origin-web-console b476d31
  (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  3d0d7c23d3eb7a858daad9f6995e71326ce2be4b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c971f7568a31038543a4ec3f26188ca563e6e714 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d08915b806cd94bda01941e9589d2f98f39adc3d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2478dab5f3396516a008761df66d71663d80c81d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d62161e496bf902a3c8c30d7b79a7bbb0605df0c (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: 35082: Wait for all pods to be running before checking PDB status
  (maszulik@redhat.com)
- bump(github.com/openshift/origin-web-console):
  7928c08da8959bd851013a9b61c8569c9c7e85a7 (dmcphers+openshiftbot@redhat.com)
- UPSTREAM: <drop>: add Timeout to client-go Config (agoldste@redhat.com)
- Removed `--force` flag from `docker tag` invocations (skuznets@redhat.com)
- Fix the failing serialization test - need a custom fuzzer to default the
  wildcard policy. (smitram@gmail.com)
- Fixes oc help global options hint (ffranz@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ed5d1ccb56350d4e3c72c27f7923d778907a44d5 (dmcphers+openshiftbot@redhat.com)
- Refactor scripts to use `oc get --raw` when possible (skuznets@redhat.com)
- bump(github.com/openshift/origin-web-console):
  4e66d443ec2918e6cba6256c4bfea1c0a8397b68 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  45e492f2f140fa3742895d10d0b379440cf2d06d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2701326256a43fda48739b211b1e88df570a8f88 (dmcphers+openshiftbot@redhat.com)
- Use custom transport for gitlab communication (jliggitt@redhat.com)
- fix oc whoami --show-server output (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  9c9f464e58da31df472fab9edef1502dfb6e2b2a (dmcphers+openshiftbot@redhat.com)
- Fixes bug 1380462 - https://bugzilla.redhat.com/show_bug.cgi?id=1380462
  (cdaley@redhat.com)
- update extended tests to work with non-empty output (jvallejo@redhat.com)
- update e2e test to work with non-emtpy output (jvallejo@redhat.com)
- UPSTREAM: 32722: warn on empty oc get output (jvallejo@redhat.com)
- UPSTREAM: 34434: Print valid json/yaml output (jvallejo@redhat.com)
- print valid json/yaml output (jvallejo@redhat.com)
- bump(github.com/openshift/origin-web-console):
  15caab12bc98d8be9decbcdf41fbbdd572118ff5 (dmcphers+openshiftbot@redhat.com)
- new-app: validate that Dockerfile from the repository has numeric EXPOSE
  directive (when strategy wasn't specified). (vsemushi@redhat.com)
- bump(github.com/openshift/origin-web-console):
  904eaca0a5e0ed5e1562a172ce064d125dec8e31 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  41d96f74bd672d4a4a67ff75796b1819c5d7f6d0 (dmcphers+openshiftbot@redhat.com)
- Generated clientset (maszulik@redhat.com)
- bump(k8s.io/client-go): d72c0e162789e1bbb33c33cfa26858a1375efe01
  (maszulik@redhat.com)
- Add cloud.google.com to supported hosts (maszulik@redhat.com)
- UPSTREAM: <drop>: Continue to carry the cAdvisor patch - revert
  (maszulik@redhat.com)
- UPSTREAM: 33806: Update cAdvisor godeps for v1.4.1 (maszulik@redhat.com)
- bump(github.com/google/cadvisor): ef63d70156d509efbbacfc3e86ed120228fab914
  (maszulik@redhat.com)
- bump(github.com/openshift/source-to-image):
  2dffea37104471547b865307415876cba2bdf1fc - revert (maszulik@redhat.com)
- UPSTREAM: 34368: Node status updater should SetNodeStatusUpdateNeeded if it
  fails to (maszulik@redhat.com)
- UPSTREAM: 35273: Fixed mutation warning in Attach/Detach controller
  (maszulik@redhat.com)
- UPSTREAM: 35071: Change merge key for VolumeMount to mountPath
  (maszulik@redhat.com)
- UPSTREAM: 34955: HPA: fixed wrong count for target replicas calculations
  (maszulik@redhat.com)
- UPSTREAM: 34895: Fix non-starting node controller in 1.4 branch
  (maszulik@redhat.com)
- UPSTREAM: 34851: Only wait for cache syncs once in NodeController
  (maszulik@redhat.com)
- UPSTREAM: 34251: Fix nil pointer issue when getting metrics from volume
  mounter (maszulik@redhat.com)
- UPSTREAM: 34809: NodeController waits for informer sync before doing anything
  (maszulik@redhat.com)
- UPSTREAM: 34694: Handle DeletedFinalStateUnknown in NodeController
  (maszulik@redhat.com)
- UPSTREAM: 34076: Remove headers that are unnecessary for proxy target
  (maszulik@redhat.com)
- UPSTREAM: 33968: scheduler: initialize podsWithAffinity (maszulik@redhat.com)
- UPSTREAM: 33735: Fixes in HPA: consider only running pods; proper denominator
  in avg (maszulik@redhat.com)
- UPSTREAM: 33796: Fix issue in updating device path when volume is attached
  multiple times (maszulik@redhat.com)
- UPSTREAM: 32914: Limit the number of names per image reported in the node
  status (maszulik@redhat.com)
- UPSTREAM: 32807: Fix race condition in setting node statusUpdateNeeded flag
  (maszulik@redhat.com)
- UPSTREAM: 33346: disallow user to update loadbalancerSourceRanges
  (maszulik@redhat.com)
- UPSTREAM: 33170: Remove closing audit log file and add error check when
  writing to audit (maszulik@redhat.com)
- UPSTREAM: 33086: Fix possible panic in PodAffinityChecker
  (maszulik@redhat.com)
- bump(github.com/google/cadvisor): 0cdf4912793fac9990de3790c273342ec31817fb
  (maszulik@redhat.com)
- Fix oauth redirect ref in jenkins service account (cewong@redhat.com)
- Fixing kubernetes_plugin extended test failure
  (root@dhcp137-43.rdu.redhat.com)
- UPSTREAM: 33014: Kubelet: Use RepoDigest for ImageID when available
  (sross@redhat.com)
- Fix EgressNetworkPolicy match-all-IPs special case (danw@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d3402a50e89c5d476f9a41f6e4ac964eaeceddd0 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  05de64a8417d48ef33ba4474c15aa271010895ab (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  1029c81d8cfd04534683ebd87b28ca3bad99b339 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d4becd8aedc3f39efdb1272a1cd66ff1212c9e7c (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  6631cc234d01243f12a594b949dad5b60a0211fd (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cd29ae2a7530f67924f5ea6ee26ff8afc9394602 (dmcphers+openshiftbot@redhat.com)
- provide the ability to modify the prefix of error reporting and ignore some
  errors in cmd operations (pweil@redhat.com)
- Jenkins imagestream scm extended tests (cewong@redhat.com)
- bump(github.com/openshift/origin-web-console):
  cb2212c6008c41196a78c43a4b3dd1de4ba8248f (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  b0ce978d52143e0f3d9d4ecc36f40a905d4f31f4 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  78a74f7768b05f2a73508e0d2e9a9b33bbecb7b3 (dmcphers+openshiftbot@redhat.com)
- deploy: correct updating lastTransitionTime in deployment conditions
  (mkargaki@redhat.com)
- bump(github.com/openshift/origin-web-console):
  693c33e8a5724f6b3d7d659411f3eeeea0aad78a (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e5b9d0fbfd2b3cceb0f9674d2361af0960861bb2 (dmcphers+openshiftbot@redhat.com)
- Update ose_images.sh - 2016-10-31 (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d1d6113a8d3dc6f2654d02d33332c110009ff4d0 (dmcphers+openshiftbot@redhat.com)
- Initialize cloud provider in node (jsafrane@redhat.com)
- deploy: drop paused conditions (mkargaki@redhat.com)
- Update rules for upstream deployment rollbacks (mkargaki@redhat.com)
- cli: remove support for comma-separated template values (mmilata@redhat.com)
- Fix as per @liggitt review comments - write wildcard spec as is in the
  rejection. (smitram@gmail.com)
- Fixes as per @liggitt review comments:   o Fix generated route protobuf file
  o Default Route.Spec.WildcardPolicy to None   o Add WildcardPolicy to
  RouteIngress in RouteStatus (defaulting to None)   o Record admitted wildcard
  policy when recording route status   o Reject wildcard routes when wildcards
  are disabled   o Change admission functions to just return errors (no bool)
  and update     checks for policy to use a switch in lieu of a if statement
  o Simpilify RouteLessThan api helper function   o Make
  Route.Spec.WildcardPolicy immutable (in update validation)   o Log details
  about conflicting routes, but don't leak info to the user   o Change error to
  "HostAlreadyClaimed"   o Add checks for defaults on Spec and Ingress
  WildcardPolicy in conversion tests. (smitram@gmail.com)
- Test run with --dry-run and attachable containers (ffranz@redhat.com)
- UPSTREAM: 35732: validate run with --dry-run and attachable containers
  (ffranz@redhat.com)
- UPSTREAM: 34298: Fix potential panic in namespace controller
  (decarr@redhat.com)
- to fix service account informer to podsecuritypolicyreview (salvatore-
  dario.minonne@amadeus.com)
- bump(github.com/spf13/pflag): 5ccb023bc27df288a957c5e994cd44fd19619465
  (mmilata@redhat.com)
- Align with other cli descriptions (yu.peng36@zte.com.cn)
- UPSTREAM: 30836:  fix Dynamic provisioning for vSphere (gethemant@gmail.com)
- Change to use helper function and fix up helper function expectations and
  tests and add missing generated files. (smitram@gmail.com)
- Data structure rework (jliggitt@redhat.com)
-    o Split out cert list and use commit from PR 11217    o Allow wildcard
  (currently only *.) routes to be created and add tests.    o Add a host
  admission controller and allow/deny list of domains and control      the
  admission/blockage of wildcard routes.    o Fix test cases and expection.
  o Add helper to generate valid wildcard regular expressions.    o Add
  wildcard domain map + regex based rules and use the rules for wildcard
  routes.    o Bug fixes and add tests.    o Add generated completions and
  docs.    o Changes as per @marun, @rajatchopra, @smarterclayton review
  comments    o Rework as per api changes to use wildcard policy with routes
  o Add defaults and update generated files. (smitram@gmail.com)
- Fix an issue with route ordering: it was possible for a newer route to be
  reported as the older route based on name/namespace checks. Ensure that we
  have a stable ordering based on the age of a route. (smitram@gmail.com)
- UPSTREAM: 35420: Remove Job also from .status.active for Replace strategy
  (maszulik@redhat.com)
- Fix for bugz https://bugzilla.redhat.com/show_bug.cgi?id=1337322 Add
  Spec.Host validation for dns labels and subdomain at runtime - this is not
  enabled in the API validation checks on route creation. And fixes as per
  @smarterclayton review comments. (smitram@gmail.com)

* Mon Oct 31 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.18
- Merge remote-tracking branch upstream/master, bump origin-web-console 9f1003a
  (tdawson@redhat.com)
- bump(github.com/openshift/origin-web-console):
  e30aa32263beacd860469cc1bd825a16fe41060b (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  12e11b40cc788780f93bde167ce0a7ff04b02d2d (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d8dad85ae673fe5d7be2f5a393f2f67594ea0ad2 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  2ad1f38354a58596a048ebd8a369fd733b165126 (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  d618617a596a4cac65ca6781f7422aa138659d0e (dmcphers+openshiftbot@redhat.com)
- reorder sample pipeline parameters for priority/importance
  (bparees@redhat.com)
- bump(github.com/openshift/origin-web-console):
  c3e34937c3e516d785299571ec20aa1afb3472df (dmcphers+openshiftbot@redhat.com)
- bump(github.com/openshift/origin-web-console):
  1ec5a2a739138f31d5a3f2e3cf9401e07f8cc3e1 (dmcphers+openshiftbot@redhat.com)
- make service controller failure non-fatal (sjenning@redhat.com)
- bump(github.com/openshift/origin-web-console):
  ea5fc5ee0f064cb717bfc93e6adbafa1833a4e13 (dmcphers+openshiftbot@redhat.com)
- Give the release images a fake golang provides (ccoleman@redhat.com)
- Update cluster up documentation (cewong@redhat.com)
- Skip retrieving logs if journalctl is not available (maszulik@redhat.com)
- Revert "Getting docker logs always to debug issue 8399" (maszulik@redhat.com)
- Replace uses of `validate_reponse` with `os::cmd::try_until_text`
  (skuznets@redhat.com)
- UPSTREAM: 33024: Add "PrintErrorWithCauses" kcmdutil helper
  (jvallejo@redhat.com)
- Make status errors with  multiple causes cleaner (jvallejo@redhat.com)
- Update ose_images.sh - 2016-10-28 (tdawson@redhat.com)
- HACKING.md fix format (jay@apache.org)
- Adds display name to image streams, updates PostgreSQL link
  (jacoblucky@gmail.com)
- Add some details to cherry picking for newcomers (jay@apache.org)
- Expose test build option for RPM `make` targets (skuznets@redhat.com)
- Add godoc to justify use of developmentRedirectURI (jvallejo@redhat.com)

* Fri Oct 28 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.17
- Merge remote-tracking branch upstream/master, bump origin-web-console df20542
  (tdawson@redhat.com)
- Fix failing deployment hook fixture (ironcladlou@gmail.com)
- Move namespace lifecycle plugin to the front of the admission chain
  (jliggitt@redhat.com)
- Only pay attention to origin types in project lifecycle admission
  (jliggitt@redhat.com)
- bump(origin-web-console): de8aca535f2762214184cd6bbc28d9948aac3a14
  (noreply@redhat.com)
- Fix deep copy for api.ResourceQuotasStatusByNamespace (jliggitt@redhat.com)
- Fix mutation in OrderedKeys getter (jliggitt@redhat.com)
- fix nil printer panic in oc set sub-cmds (jvallejo@redhat.com)
- add jenkins v2 imagestreams (bparees@redhat.com)
- Added comment to clarify that oc cluster did not work on releases before that
  1.3 (jparrill@redhat.com)
- Adding warning about port 8443 potentially being blocked by firewall rules on
  oc cluster up Fixes issue #10807 (cdaley@redhat.com)
- Replace uses of `wait_for_url_timed` with `os::cmd::try_until_success`
  (skuznets@redhat.com)
- Remove `reset_tmp_dir` function from Bash library (skuznets@redhat.com)
- new-app: validate that Dockerfile from the repository has numeric EXPOSE
  directive. (vsemushi@redhat.com)
- deploy: set condition reason correctly for new RCs (mkargaki@redhat.com)
- Use global LRU cache for layer sizes (agladkov@redhat.com)
- UPSTREAM: 27714: Send recycle events from pod to pv. (jsafrane@redhat.com)
- remove redundant variable 'retryCount' (miao.yanqiang@zte.com.cn)
- ie. is not the correct abbreviation for ID EST (yu.peng36@zte.com.cn)
- Display warning instead of error if ports 80/443 in use (cdaley@redhat.com)
- bump(github.com/openshift/source-to-image):
  2dffea37104471547b865307415876cba2bdf1fc (ipalade@redhat.com)
- test/integration: pass HostConfig at image creation time for router tests
  (dcbw@redhat.com)
- sdn: no longer kill docker0 (dcbw@redhat.com)
- add `oc status` warning for missing liveness probe (jvallejo@redhat.com)
- sdn: fix single-tenant pod setup (dcbw@redhat.com)
- Update ose_images.sh - 2016-10-26 (tdawson@redhat.com)
- Remove usage of deprecated utilities for starting a server
  (skuznets@redhat.com)
- Use `oc get --raw` instead of `curl` in Swagger verification/update scripts
  (skuznets@redhat.com)
- include timestamps in extended test build logs (bparees@redhat.com)
- UPSTREAM: 34997: Fix kube vsphere.kerneltime (gethemant@gmail.com)
- Quota test case is inaccurate (ccoleman@redhat.com)
- fix broken sample pipeline job (bparees@redhat.com)
- Allow users to pass in `make_redistributable` to the Origin spec file
  (skuznets@redhat.com)
- Make extended test build optional in origin.spec (skuznets@redhat.com)
- Fix regression from #9481 about defaulting prune images arguments
  (maszulik@redhat.com)
- Remove node access from the system:router roles (ccoleman@redhat.com)

* Wed Oct 26 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.16
- Merge remote-tracking branch upstream/master, bump origin-web-console c0704ca
  (tdawson@redhat.com)
- Migrated miscellaneous Bash utilities into the `hack/lib` library
  (skuznets@redhat.com)
- removing unused default variables (cdaley@redhat.com)
- Removing ImageChangeControllerFatalError and it's associated references as it
  is no longer used. (cdaley@redhat.com)
- Switch back to using docker build with docker 1.12 (dmcphers@redhat.com)
- deployments: set ActiveDeadlineSeconds in deployer hook pods correctly
  (mfojtik@redhat.com)
- Correctly report the size of overlarge log files (skuznets@redhat.com)
- Updates template and image stream metadata (jacoblucky@gmail.com)
- really re-enable jenkins autoprovisioning (bparees@redhat.com)
- Start-build/env, exec, and multitag jenkins plugin tests
  (jupierce@redhat.com)
- oc: fix export for deployment configs (mkargaki@redhat.com)
- WIP Fix bug 1373330 Invalid formatted generic webhook can trigger new-build
  without warning (jminter@redhat.com)
- serviceaccount: add secret informer to create_dockercfg_secret
  (mfojtik@redhat.com)
- Improve exec/attach error message (jliggitt@redhat.com)
- Create storage-admin role (screeley@redhat.com)
- support non-string template parameter substitution (bparees@redhat.com)
- move jenkins related ext tests to image_ecosystem (gmontero@redhat.com)
- Update ose_images.sh - 2016-10-24 (tdawson@redhat.com)
- Remove `get_object_assert` utility from our Bash libraries
  (skuznets@redhat.com)
- specfile: fix specfile issues after openshift-sdn CNI plugin merge
  (dcbw@redhat.com)
- Removed the `tryuntil` utility from our Bash libraries (skuznets@redhat.com)
- Update man pages (ffranz@redhat.com)
- UPSTREAM: 35427: kubectl commands must not use the factory out of Run
  (ffranz@redhat.com)
- Fix OS_RELEASE=n for build-images.sh (ccoleman@redhat.com)
- generated: resources (ccoleman@redhat.com)
- UPSTREAM: <carry>: Revert extra pod resources change (ccoleman@redhat.com)
- Add additional utilities used during test-cmd (ccoleman@redhat.com)
- Disable test for unwritable config file (ccoleman@redhat.com)
- deploy: tweak enqueueing in the trigger controller (mkargaki@redhat.com)
- extended: use timestamps in deployer logs (mkargaki@redhat.com)
- add nodeselector and annotation build pod overrides and defaulters
  (bparees@redhat.com)
- deploy: cleanup dc controller (mkargaki@redhat.com)
- Created a script to run tito builds and upack leftover artifacts
  (skuznets@redhat.com)
- Tests: don't clone openshift/origin where possible (mmilata@redhat.com)
- bump(github.com/coreos/etcd):v3.1.0-rc.0 (ccoleman@redhat.com)
- bump(google.golang.org/grpc):v1.0.2 (ccoleman@redhat.com)
- Switch to using protobuf and etcd3 storage (ccoleman@redhat.com)
- Fixes bug 1380555 - https://bugzilla.redhat.com/show_bug.cgi?id=1380555 Uses
  registry.access.redhat.com/openshift3/ose as the default for ose builds
  (cdaley@redhat.com)
- Remove -a flag from `os::build::build_static_binaries` (mkhan@redhat.com)
- Remove -a flag from hack/test-integration.sh (mkhan@redhat.com)
- add integration that create project using 1.3 clientset (mfojtik@redhat.com)
- regenerate clientsets for v1_3 (mfojtik@redhat.com)
- make projects non-namespaced (mfojtik@redhat.com)
- improve the client set generator script (mfojtik@redhat.com)
- set the --clientset-api-path=/oapi for origin clients (mfojtik@redhat.com)
- UPSTREAM: 32769: clientgen: allow to pass custom apiPath when generating
  client sets (mfojtik@redhat.com)

* Mon Oct 24 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.15
- Merge remote-tracking branch upstream/master, bump origin-web-console 9a90917
  (tdawson@redhat.com)
- PodDisruptionBudget - generated changes (maszulik@redhat.com)
- Enable PodDistruptionbudget e2e tests in conformance (maszulik@redhat.com)
- UPSTREAM: 35287: Add resource printer and describer for PodDisruptionBudget
  (maszulik@redhat.com)
- UPSTREAM: 35274: Fix PDB e2e test, off-by-one (maszulik@redhat.com)
- Correcting wording of error message (cdaley@redhat.com)
- Added cccp.yml file to build container on CentOS Container Pipeline.
  (mohammed.zee1000@gmail.com)
- sdn: re-add missing NAT for pods that docker used to do (dcbw@redhat.com)
- sdn: convert pod network setup to a CNI plugin (dcbw@redhat.com)
- sdn: use CNI for IPAM instead of docker (dcbw@redhat.com)
- Drop pkg/sdn/plugin/api, add stuff to pkg/sdn/api (danw@redhat.com)
- bump(github.com/containernetworking/cni):
  b8e92ed030588120f9fda47dd359e17a3234142d (dcbw@redhat.com)
- Remove the func 'parseRepositoryTag' (miao.yanqiang@zte.com.cn)
- f5 vxlan integration with sdn (rchopra@redhat.com)
- test-cmd fails when the user is root (ccoleman@redhat.com)
- for now disable jenkins oauth for ext tests (gmontero@redhat.com)
- re-enable jenkins autoprovisioning (bparees@redhat.com)
- Use actual semantic versioning for Git tags (ccoleman@redhat.com)
- hack/env upgrades - use rsync for sync (ccoleman@redhat.com)
- UPSTREAM: 32593: Audit test fails to take into account timezone
  (ccoleman@redhat.com)
- client: fix instantiate call to handle 204 (mkargaki@redhat.com)
- doc and template updates for jenkins openshift oauth plugin
  (gmontero@redhat.com)
- Revert "Add router support for wildcard domains (*.foo.com)"
  (ccoleman@redhat.com)
- Bump origin-web-console (7c57218) (spadgett@redhat.com)
- Bump to tls1.2 (jliggitt@redhat.com)
- Add `bc` to the release Docker image specs for test-cmd (skuznets@redhat.com)
- Generated: docs/bash completions for network diagnostics (rpenta@redhat.com)
- Added network diagnostic validation test (rpenta@redhat.com)
- Expose network diagnostics via 'oadm diagnostics NetworkCheck'
  (rpenta@redhat.com)
- Make network diagnostics log directory configurable (rpenta@redhat.com)
- Added support for Network diagnostics (rpenta@redhat.com)
- Collect and consolidate remote network diagnostic logs (rpenta@redhat.com)
- Create test environment for network diagnostics (rpenta@redhat.com)
- Custom pod/service objects for network diagnostics (rpenta@redhat.com)
- Added support for openshift infra network-diagnostic-pod (rpenta@redhat.com)
- Diagnostics: Collect network debug logs on the node (rpenta@redhat.com)
- Helper methods to capture master/node logs (rpenta@redhat.com)
- Diagnostics: Added service connectivity checks (rpenta@redhat.com)
- Diagnostics: Added external connectivity checks (rpenta@redhat.com)
- Diagnostics: Added pod network checks (rpenta@redhat.com)
- Modify GetHostIPNetworks() to also return host IPs (rpenta@redhat.com)
- Diagnostics: Added node network checks (rpenta@redhat.com)
- Added diagnostics util functions (rpenta@redhat.com)
- adding oc set resources as a wrapper for an upstream commit
  (jtanenba@redhat.com)
- UPSTREAM: 27206: Add kubectl set resources (jtanenba@redhat.com)
- fix annotations test flake (jvallejo@redhat.com)
- Change pipeline sample to use Node.js+MongoDB sample and also "nodejs"
  Jenkins slave. (sspeiche@redhat.com)
- CleanupHostPathVolumes(): remove also directories from the filesystem.
  (vsemushi@redhat.com)
- Update ose_images.sh - 2016-10-21 (tdawson@redhat.com)
- Update shell completions with oc describe storageclass (jsafrane@redhat.com)
- atomic registry systemd install bugfixes (aweiteka@redhat.com)
- UPSTREAM: 34638: Storage class updates in oc output (jsafrane@redhat.com)
- Implement route based annotations for service accounts (mkhan@redhat.com)
- UPSTREAM: 31607: Add kubectl describe storageclass (jsafrane@redhat.com)
- Bug 1386018: use deployment conditions when creating a rc
  (mkargaki@redhat.com)
-    o Split out cert list and use commit from PR 11217    o Allow wildcard
  (currently only *.) routes to be created and add tests.    o Add a host
  admission controller and allow/deny list of domains and control      the
  admission/blockage of wildcard routes.    o Fix test cases and expection.
  o Add helper to generate valid wildcard regular expressions.    o Add
  wildcard domain map + regex based rules and use the rules for wildcard
  routes.    o Bug fixes and add tests.    o Add generated completions and
  docs.    o Changes as per @marun, @rajatchopra, @smarterclayton review
  comments (smitram@gmail.com)
- Fix an issue with route ordering: it was possible for a newer route to be
  reported as the older route based on name/namespace checks. Ensure that we
  have a stable ordering based on the age of a route. (smitram@gmail.com)
- Cleanup: Use wait.ExponentialBackoff instead of retry loop
  (rpenta@redhat.com)
- Continue project cache evaluation in the presence of evaluation errors
  (jliggitt@redhat.com)
- group podLists into single list (jvallejo@redhat.com)
- update generated docs (jvallejo@redhat.com)
- Update oc create success message when using --dry-run (jvallejo@redhat.com)
- UPSTREAM: 31276: Update oc create success message when using --dry-run
  (jvallejo@redhat.com)
- Update completions and man pages for volume cmd (gethemant@gmail.com)
- Add AuditConfig validation and backwards compatibility if no AuditFilePath is
  provided (maszulik@redhat.com)
- Support specifying StorageClass while creating volumes (gethemant@gmail.com)
- Check if hostBits equals zero and add some test cases
  (zhao.xiangpeng@zte.com.cn)
- update oc env, return resources in list (jvallejo@redhat.com)
- Switch to use upstream audit handler - generated changes
  (maszulik@redhat.com)
- Switch to use upstream audit handler (maszulik@redhat.com)
- UPSTREAM: 33934: Add asgroups to audit log (maszulik@redhat.com)
- dind: bump deployment timeout to 120s (marun@redhat.com)
- dind: wait-for-condition forever by default (marun@redhat.com)
- UPSTREAM: 30145: Add PVC storage to Limit Range (mturansk@redhat.com)

* Fri Oct 21 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.14
- Merge remote-tracking branch upstream/master, bump origin-web-console 5e10797
  (tdawson@redhat.com)
- Implement cluster status command (jminter@redhat.com)
- Enable Gluster and RBD provisioners (jsafrane@redhat.com)
- Add compression to haproxy v2 (cw-aleks@users.noreply.github.com)
- Add extended test for PetSet based MongoDB replica set. (vsemushi@redhat.com)
- Enable PV controller to provisiong Gluster volumes (jsafrane@redhat.com)
- UPSTREAM: 34705: Make use of PVC namespace when provisioning gluster volumes
  (jsafrane@redhat.com)
- UPSTREAM: 35141: remove pv annotation from rbd volume (jsafrane@redhat.com)
- Update role binding docs (mkhan@redhat.com)
- Do not use "*" as DockerImageReference.Name for ImageStreamImport
  (agladkov@redhat.com)
- oc new-app --search: don't require docker hub access (mmilata@redhat.com)
- UPSTREAM: 35022: Remove PV annotations for Gluster provisioner
  (hchen@redhat.com)
- add extened test for pipeline build (haowang@redhat.com)
- Work around broken run --attach for now (agoldste@redhat.com)
- Fixes issue #10108 Adds os::build::setup_env to hack/update-generated-
  bootstrap-bindata.sh which ensures that the GOPATH env variable is set and
  not empty (cdaley@redhat.com)
- Update ose_images.sh - 2016-10-19 (tdawson@redhat.com)
- Fixes bug 1345773 - https://bugzilla.redhat.com/show_bug.cgi?id=1345773
  (cdaley@redhat.com)
- change gitserver template strategy to Recrate
  (shiywang@dhcp-140-35.nay.redhat.com)
- Bug 1386054: enqueue in the trigger controller only when really needed
  (mkargaki@redhat.com)
- keepalived vip (vrrp) requires 224.0.0.18/32 (pcameron@redhat.com)
- update build status reasons to StatusReason type (jvallejo@redhat.com)
- IngressIP controller: Fix Service update in an exponential backoff manner
  (rpenta@redhat.com)
- update generated docs (jvallejo@redhat.com)
- bump(k8s.io/client-go): add Timeout field to 1.4 restclient
  (jvallejo@redhat.com)
- rename global flag to --request-timeout (jvallejo@redhat.com)
- UPSTREAM: 33958: update --request-timeout flag to string value
  (jvallejo@redhat.com)
- UPSTREAM: 33958: add global timeout flag (jvallejo@redhat.com)
- Update the cli hacking guide (ffranz@redhat.com)
- Help templates which allow reordering of sections (ffranz@redhat.com)
- Update generated docs (ffranz@redhat.com)
- Tools for checking CLI conventions (ffranz@redhat.com)
- Normalize CLI examples and long descriptions (ffranz@redhat.com)
- Markdown rendering engine (ffranz@redhat.com)
- Commands must always use the provided err output (ffranz@redhat.com)
- Add writers capable of adjusting to terminal sizes (ffranz@redhat.com)
- bump(github.com/mitchellh/go-wordwrap):
  ad45545899c7b13c020ea92b2072220eefad42b8 (ffranz@redhat.com)
- Minor fixups after s2i bump (jminter@redhat.com)
- bump(github.com/openshift/source-to-image):
  5009651d01b7f96b5373979317f4d4f32415f32b (jminter@redhat.com)
- React to new --revision flag in rollout status (mkargaki@redhat.com)
- enable and test owner reference protection (deads@redhat.com)
- UPSTREAM: 34443: kubectl: add --revision flag in rollout status
  (mkargaki@redhat.com)
- oc: add -o revision in rollout latest (mkargaki@redhat.com)
- Reject Builds with unresolved image references (mmilata@redhat.com)
- Allow running extended test without specifying namespace
  (maszulik@redhat.com)
- Fix validation messages for PodSecurityPolicy*Review objects
  (maszulik@redhat.com)
- Add a missing err return (miao.yanqiang@zte.com.cn)
- Fix an imperfect if statement (miao.yanqiang@zte.com.cn)
- To add Informer for ServiceAccount (salvatore-dario.minonne@amadeus.com)
- dind: deploy multitenant plugin by default (marun@redhat.com)
- dind: stop truncating systemd logs (marun@redhat.com)
- Bump origin-web-console (d5318f2) (jforrest@redhat.com)
- Cleaned up the system logging Bash library (skuznets@redhat.com)
- update docs (jvallejo@redhat.com)
- UPSTREAM: 32555: WantsAuthorizer admission plugin support (deads@redhat.com)
- use cmdutil DryRun flag helper (jvallejo@redhat.com)
- UPSTREAM: 34028: add --dry-run option to apply kube cmd (jvallejo@redhat.com)
- UPSTREAM: 34028: add --dry-run option to create root cmd
  (jvallejo@redhat.com)
- Add --dry-run option to create sub-commands (jvallejo@redhat.com)
- UPSTREAM: 34829: add ownerref permission checks (deads@redhat.com)
- Make OAuth provider discoverable from within a Pod (mkhan@redhat.com)
- remove ruby, mysql tags from pipeline sample template (bparees@redhat.com)
- UPSTREAM: 32662: Change the default volume type of GlusterFS provisioner
  (jsafrane@redhat.com)
- spell jenkins correctly (jminter@redhat.com)
- cluster up: add option to install logging components (cewong@redhat.com)
- Remove -f flag from docker tag (gethemant@gmail.com)
- Remove signature store from registry (agladkov@redhat.com)
- UPSTREAM: docker/distribution: 1857: Provide stat descriptor for Create
  method during cross-repo mount (jliggitt@redhat.com)
- UPSTREAM: docker/distribution: 1757: Export storage.CreateOptions in top-
  level package (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: custom routes/auth
  (agoldste@redhat.com)
- UPSTREAM: docker/distribution: <carry>: Update dependencies
  (agladkov@redhat.com)
- bump(github.com/docker/distribution):
  12acdf0a6c1e56d965ac6eb395d2bce687bf22fc (agladkov@redhat.com)
- Enable exec/http proxy e2e test (agoldste@redhat.com)
- refactor install to support configuration, plus help manpage
  (aweiteka@redhat.com)

* Wed Oct 19 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.13
- Update ose_images.sh - 2016-10-17 (tdawson@redhat.com)
- Remove dependence on external mysql image tag order (jliggitt@redhat.com)
- Set test/extended/networking-minimal.sh +x (marun@redhat.com)
- UPSTREAM: 32084: Do not allow creation of GCE PDs in unmanaged zones
  (jsafrane@redhat.com)
- UPSTREAM: 32077: Do not report warning event when an unknown provisioner is
  requested (jsafrane@redhat.com)
- Clarify new-app messages (jminter@redhat.com)
- allow review endpoints on missing namespaces (deads@redhat.com)
- UPSTREAM: <carry>: update namespace lifecycle to allow review APIs
  (deads@redhat.com)
- Correct secret type in oc secrets new-{basic,ssh}auth (jminter@redhat.com)
- add cmd test (jvallejo@redhat.com)
- oc: generated code for switching from --latest to --again
  (mkargaki@redhat.com)
- oc: deprecate 'deploy --latest' in favor of 'rollout latest --again'
  (mkargaki@redhat.com)
- UPSTREAM: 34010: Match GroupVersionKind against specific version
  (maszulik@redhat.com)
- deploy: generated code for api refactoring (mkargaki@redhat.com)
- deploy: api types refactoring (mkargaki@redhat.com)
- make function addDefaultEnvVar cleaner (li.guangxu@zte.com.cn)
- add client config invalid flags error handling test (jvallejo@redhat.com)
- UPSTREAM: 29236: handle invalid client config option errors
  (jvallejo@redhat.com)
- UPSTREAM: 34020: Allow empty annotation values Annotations with empty values
  can be used, for example, in diagnostics logging. This patch removes the
  client-side check for empty values in an annotation key-value pair.
  (jvallejo@redhat.com)
- Add logging to project request failures (jliggitt@redhat.com)
- Allow cluster up and rsync when no ipv6 on container host
  (jminter@redhat.com)
- UPSTREAM: <carry>: sysctls SCC strategy (agoldste@redhat.com)
- Fix a typo of logging code in pkg/router/template/router.go
  (yhlou@travelsky.com)
- Add wildcard entry to cluster up router cert (ironcladlou@gmail.com)
- Update cluster_up_down.md (chris-milsted@users.noreply.github.com)

* Mon Oct 17 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.12
- Merge remote-tracking branch upstream/master, bump origin-web-console d5318f2
  (tdawson@redhat.com)
- fix oc describe suggestion in oc rsh output (jvallejo@redhat.com)
- add pod bash completion `oc exec` (jvallejo@redhat.com)
- Enable minimization of net e2e runtime (marun@redhat.com)
- ParseDockerImageReference use docker/distribution reference parser
  (agladkov@redhat.com)
- Delete a redundant arg and optimize some codes in the
  (miao.yanqiang@zte.com.cn)
- remove the tmp secret data (li.guangxu@zte.com.cn)
- remove old atomic doc (pweil@redhat.com)
- move images extended tests to new tag and directory (bparees@redhat.com)
- dind: Ensure unique node config and fix perms (marun@redhat.com)
- dind: ensure node certs are generated serially (marun@redhat.com)
- integration: retry instantiate on conflict (mkargaki@redhat.com)
- CLI: add a set build-secret command (cewong@redhat.com)
- Bug 1383138: suggest 'rollout latest' if 'deploy --latest' returns a bad
  request (mkargaki@redhat.com)
- UPSTREAM: 34524: Test x509 intermediates correctly (jliggitt@redhat.com)
- Test x509 intermediates correctly (jliggitt@redhat.com)
- Fixing validation msg (jhadvig@redhat.com)
- Change haproxy router to use a certificate list/map file. (smitram@gmail.com)
- Note the commit for the release packaged by hack/build-cross.sh
  (skuznets@redhat.com)
- new-app: warn when source credentials are needed (cewong@redhat.com)

* Fri Oct 14 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.11
- Merge remote-tracking branch upstream/master, bump origin-web-console b7fa730
  (tdawson@redhat.com)
- increase default vagrant volume size to 25gigs (bparees@redhat.com)
- Update ose_images.sh - 2016-10-12 (tdawson@redhat.com)
- the parameter no need set again (li.guangxu@zte.com.cn)
- Add a `make` target to vendor the web console (skuznets@redhat.com)
- Make evacuate aware of replica set and daemon set (mfojtik@redhat.com)
- Rename Kclient to KubeClient (mfojtik@redhat.com)
- add some optimizations to build code (li.guangxu@zte.com.cn)
- get password from dc; add more diag (gmontero@redhat.com)
- oc: update valid arguments for upstream commands (mkargaki@redhat.com)
- UPSTREAM: <drop>: rollout status should return appropriate exit codes
  (mkargaki@redhat.com)
- Tests for deployment conditions and oc rollout status (mkargaki@redhat.com)
- Extend Builds with list of labels applied to image (mmilata@redhat.com)
- bump(github.com/openshift/source-to-image):
  2a7f4c43b68c0f7a69de1d59040544619b03a21a (mmilata@redhat.com)
- Move "oadm pod-network" tests from extended to integration and cmd
  (danw@redhat.com)
- test/cmd/sdn.sh improvements (danw@redhat.com)
- oc: generated code for rollout status (mkargaki@redhat.com)
- oc: add rollout status (mkargaki@redhat.com)
- deploy: use Conditions in the deploymentconfig controller
  (mkargaki@redhat.com)
- Remove the unuse parameter in function ActiveDeployment
  (wang.yuexiao@zte.com.cn)
- neaten portforward code now that readyChan is accepted in New()
  (jminter@redhat.com)
- Enable extended validation check on all routes admitted in by the router.
  Update generated docs/manpage (smitram@gmail.com)
- One can now allocate hostsubnets for hosts that are not part of the cluster.
  This is useful when a host wants to be part of the SDN, but not part of the
  cluster (e.g. F5) (rchopra@redhat.com)
- bump(github.com/RangelReale/osincli):
  fababb0555f21315d1a34af6615a16eaab44396b (mkhan@redhat.com)

* Wed Oct 12 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.10
- Merge remote-tracking branch upstream/master, bump origin-web-console b60172f
  (tdawson@redhat.com)
- Update ose_images.sh - 2016-10-10 (tdawson@redhat.com)
- deployments: use centos:centos7 instead of deployment-example image
  (mfojtik@redhat.com)
- Warn if no login idps are present (jliggitt@redhat.com)
- Updated sysctl usage for cpu (johannes.scheuermann@inovex.de)

* Mon Oct 10 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.9
- Merge remote-tracking branch upstream/master, bump origin-web-console 6a78401
  (tdawson@redhat.com)
- Test case must handle caches now (ccoleman@redhat.com)
- Avoid doing a naive DeepEquals on all PolicyRules (ccoleman@redhat.com)
- Try a cached RuleResolver prior to the underlying in a few cases
  (ccoleman@redhat.com)
- Collapse local and cluster PolicyRule retrieval (ccoleman@redhat.com)
- Upgrade note and swagger for restoring automatic=false behavior in 1.4
  (mkargaki@redhat.com)
- Update ose_images.sh - 2016-10-07 (tdawson@redhat.com)
- Use utilwait.ExponentialBackoff instead of looping (danw@redhat.com)
- Split out SDN setup code from HostSubnet-monitoring code (danw@redhat.com)
- Split out EgressNetworkPolicy-monitoring code into its own file
  (danw@redhat.com)
- Tests for namespaced pruning and necessary refactor (maszulik@redhat.com)
- Suppress node configuration details during tests (mkhan@redhat.com)
- Bug 1371511 - add namespace awareness to oadm prune commands
  (maszulik@redhat.com)
- add tests, updated docs (jvallejo@redhat.com)
- UPSTREAM: 33319: Add option to set a nodeport (jvallejo@redhat.com)
- oc: generated code for 'rollout latest' (mkargaki@redhat.com)
- oc: add rollout latest (mkargaki@redhat.com)
- Correctly parse git versions with longer short hashes (danw@redhat.com)
- Change default node permission check to <apiVerb> nodes/proxy
  (jliggitt@redhat.com)
- Add support for using PATCH when add/remove vol (gethemant@gmail.com)
- fix to unaddressed nits in #10964 for AGL diagnostics (jcantril@redhat.com)
- extended: move conformance tag in top level test describers
  (mkargaki@redhat.com)
- extended: deployment with multiple containers using a single ICT
  (mkargaki@redhat.com)
- deploy: generated code for deployment conditions (mkargaki@redhat.com)
- deploy: api for deploymentconfig Conditions (mkargaki@redhat.com)
- dind: install 'less' to ease debugging (marun@redhat.com)
- dind: slim down base image size (marun@redhat.com)
- dind: update warning of system modification (marun@redhat.com)
- dind: enable ssh access to cluster (marun@redhat.com)
- Refactor dind (marun@redhat.com)

* Fri Oct 07 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.8
- Merge remote-tracking branch upstream/master, bump origin-web-console 2f78dcc
  (tdawson@redhat.com)
- Update ose_images.sh - 2016-10-05 (tdawson@redhat.com)
- Updated link to host subnet routing documentation. (pep@redhat.com)
- Allow multiple segments in DockerImageReference (agladkov@redhat.com)
- Updates `oc run` examples (jtslear@gmail.com)
- Introduce targets for building RPMs to the Makefile (skuznets@redhat.com)
- fix error messages for clusterrolebinding (jtanenba@redhat.com)
- Fixup tito tagger and builder libs (tdawson@redhat.com)
- Remove manpage generation from Tito build (skuznets@redhat.com)
- Update ovs.AddPort()/DeletePort() semantics (danw@redhat.com)
- Add a "global" type to pkg/util/ovs (danw@redhat.com)
- Make pkg/util/ovs and pkg/util/ipcmd tests check the passed-in command line
  (danw@redhat.com)

* Wed Oct 05 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.7
- Merge remote-tracking branch upstream/master, bump origin-web-console 02b3c89
  (tdawson@redhat.com)
- extended: move deployment fixtures in separate directory
  (mkargaki@redhat.com)
- UPSTREAM: 33677: add linebreak between resource groups (jvallejo@redhat.com)
- [origin-aggregated-logging 207] Add diagnostics for aggregated logging
  (jcantril@redhat.com)
- extended: bump image tagging timeout (mkargaki@redhat.com)
- encode/decode nested objects in SubjectRulesReviewStatus (mfojtik@redhat.com)
- generate protobuf (mfojtik@redhat.com)
- add validation (mfojtik@redhat.com)
- add user options to can-i (deads@redhat.com)
- add other user rules review (deads@redhat.com)
- add option to `oc whoami` that prints server url (jvallejo@redhat.com)
- Update ose_images.sh - 2016-10-03 (tdawson@redhat.com)
- Network plugin dir default removed (ccoleman@redhat.com)
- generated: docs (ccoleman@redhat.com)
- Client defaulting changed in Kube v1.4.0 (ccoleman@redhat.com)
- UPSTREAM: <drop>: Continue to carry the cAdvisor patch (ccoleman@redhat.com)
- bump(k8s.io/kubernetes):v1.4.0 (ccoleman@redhat.com)
- Disable cgo when building extended.test (marun@redhat.com)
- Fix dlv invocation in networking.sh (marun@redhat.com)
- More generated code (mkargaki@redhat.com)
- deploy: generated protobuf for instantiate (mkargaki@redhat.com)
- deploy: update generated code for instantiate (mkargaki@redhat.com)
- Make automatic=false work again as it should (mkargaki@redhat.com)
- Run admission for /instantiate (mkargaki@redhat.com)
- oc: switch deploy --latest to use new instantiate endpoint
  (mkargaki@redhat.com)
- deploy: remove imagechange controller (mkargaki@redhat.com)
- deploy: instantiate deploymentconfigs (mkargaki@redhat.com)
- e2e: schema2 config test amendments (miminar@redhat.com)
- line continue should be instead by break (li.guangxu@zte.com.cn)
- ppc64le platform support for build-cross.sh script (mkumatag@in.ibm.com)

* Mon Oct 03 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.6
- suggest use of `oc explain` in oc get output (jvallejo@redhat.com)
- UPSTREAM: 31818: suggest use of `oc explain` in oc get output
  (jvallejo@redhat.com)
- Fix unclosed tag in OpenAPI spec (ccoleman@redhat.com)
- Enable pods-per-core by default, and increase max pods (decarr@redhat.com)
- fix bug 1371047 When JenkinsPipeline build in New status, should not display
  its stages info (jminter@redhat.com)
- introduce no proxy setting for git cloning, with defaulter
  (bparees@redhat.com)
- relabel build compatibility test (cewong@redhat.com)
- fix fake_buildconfigs methods (guilhermebr@gmail.com)
- Re-enable the networking tests. (marun@redhat.com)
- generated swagger spec (salvatore-dario.minonne@amadeus.com)
- SCC check API: REST (salvatore-dario.minonne@amadeus.com)

* Fri Sep 30 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.5
- Merge remote-tracking branch upstream/master, bump origin-web-console 42e31a5
  (tdawson@redhat.com)
- Login must ignore some SSL cert errors when --insecure (ffranz@redhat.com)
- make oc project work with kube (deads@redhat.com)
- Fix proto generation and swagger generation (ccoleman@redhat.com)
- Master broken due to simultaneous merges around OpenAPI (ccoleman@redhat.com)
- make oc login tolerate kube with --token (deads@redhat.com)
- Add a simple test pod for running a kube-apiserver and etcd
  (ccoleman@redhat.com)
- cluster up: do not re-initialize a cluster that already has been initialized
  (cewong@redhat.com)
- cluster up remove temporary files, fixes #9385 (jminter@redhat.com)
- Bug 1312230 - fix image import command to reflect the actual status
  (maszulik@redhat.com)
- Generate and write an OpenAPI spec and copy protos (ccoleman@redhat.com)
- UPSTREAM: 33337: Order swagger docs properly (ccoleman@redhat.com)
- UPSTREAM: 33007: Register versioned.Event instead of *versioned.Event
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: Stably sort openapi request parameters
  (ccoleman@redhat.com)
- Update descriptions on all resources and remove definitions
  (ccoleman@redhat.com)
- Favor --show-token over --token for whoami (jliggitt@redhat.com)
- bump(github.com/openshift/source-to-image):
  785cfb47dab175271d96de9b6e7007ce5a3b811c (bparees@redhat.com)
- convert between s2i authconfig and fsouza authconfig types
  (bparees@redhat.com)
- deploy: generated code for updatePercent removal (mkargaki@redhat.com)
- Remove deprecated updatePercent field from deployment configs
  (mkargaki@redhat.com)
- A few test/cmd/sdn.sh fixups (danw@redhat.com)
- use field.Required for required username (pweil@redhat.com)
- Add details for field.Required (sgallagh@redhat.com)
- fix tito builder now that provides exceeds argument restriction on subprocess
  (maxamillion@fedoraproject.org)
- Revert "Allow startup to continue even if nodes don't have
  EgressNetworkPolicy list permission" (danw@redhat.com)
- add option to set host for profile endpoint (pweil@redhat.com)
- Bind socat to 127.0.0.1 when using it on OS X (cewong@redhat.com)
- lookup buildconfigs in shared indexed cache instead of listing
  (bparees@redhat.com)
- Add PKCE support (jliggitt@redhat.com)
- Adapt to ClientSecretMatches interface (jliggitt@redhat.com)
- bump(github.com/RangelReale/osin): 839b9f181ce80c6118c981a3f636927b3bb4f3a7
  (jliggitt@redhat.com)
- only set app label if it is not present on any object (bparees@redhat.com)
- master: check both places to fix bug 1372618 (lmeyer@redhat.com)
- sdn: set veth TX queue length to unblock QoS (dcbw@redhat.com)
- Allow job controller to get jobs (jliggitt@redhat.com)
- etcd install and version test is broken (ccoleman@redhat.com)
- Switch to using the new 'embed' package to launch etcd (ccoleman@redhat.com)
- UPSTREAM: coreos/etcd: 6463: Must explicitly enable http2 for Go 1.7 TLS
  (ccoleman@redhat.com)
- bump(github.com/coreos/etcd):v3.1.0-alpha.1 (ccoleman@redhat.com)
- Update to start-build --follow, somewhat contradicting #6268
  (jminter@redhat.com)
- Fix the documentation to show how to set a custom message
  (bbennett@redhat.com)
- Fix osadm manage-node --schedulable (marun@redhat.com)
- Extended previous version compatibility tests (cewong@redhat.com)
- function addDefaultEnvVar may have risk of nil pointer
  (li.guangxu@zte.com.cn)
- start-build from-webhook: use canonical hostport to compare with config
  (cewong@redhat.com)
- Explicit pull the docker base image for docker build (Haowang@redhat.com)
- Update preferred ciphers (jliggitt@redhat.com)

* Wed Sep 28 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.4
- Merge remote-tracking branch upstream/master, bump origin-web-console 068713d
  (tdawson@redhat.com)
- Fix a bug in text/extended/networking/ovs.go if a test fails
  (danw@redhat.com)
- Add test/cmd/sdn.sh (danw@redhat.com)
- Fix use of deprecated PodSpec field name (danw@redhat.com)
- Kill off SDN "Registry" type (danw@redhat.com)
- Make NetworkInfo just cache cluster/service CIDRs (danw@redhat.com)
- Move remaining NetworkInfo-related code out of registry.go (danw@redhat.com)
- Move NetworkInfo from Registry to OsdnNode/OsdnMaster/ovsProxyPlugin
  (danw@redhat.com)
- add test for mixed kinds output (jvallejo@redhat.com)
- UPSTREAM: 32222: ensure resource prefix on single type (jvallejo@redhat.com)
- oc: warn for rolling deployments with RWO volumes (mkargaki@redhat.com)
- The function 'NewPrintNameOrErrorAfter' is defined, but it's not used
  (miao.yanqiang@zte.com.cn)
- add hostmanager option to Vagrantfile (jminter@redhat.com)
- Fixed an error description of func, and deleted a redundant error check
  (miao.yanqiang@zte.com.cn)
- Update generated docs (ffranz@redhat.com)
- Fixes docs generation (ffranz@redhat.com)
- Update to released Go 1.7.1 (ffranz@redhat.com)
- add localhost:9000 as a default redirect URL (jvallejo@redhat.com)
- deployment: use event client to create events directly (mfojtik@redhat.com)
- deployment: use rc namespacer instead of function (mfojtik@redhat.com)
- deploy: forward warnings from deployer to deployment config
  (mfojtik@redhat.com)
- deploy: show replication controller warnings in deployer log
  (mfojtik@redhat.com)
- UPSTREAM: 33489: Log test error (jliggitt@redhat.com)
- Bump origin-web-console (fc61bfe) (jforrest@redhat.com)
- UPSTREAM: 33464: Fix cache expiration check (jliggitt@redhat.com)
- UPSTREAM: 33464: Allow testing LRUExpireCache with fake clock
  (jliggitt@redhat.com)
- extended: fix polling the status of a config that needs to be synced
  (mkargaki@redhat.com)
- Revert "Avoid using bsdtar for extraction during build" (bparees@redhat.com)
- Extract duplicate code (miao.yanqiang@zte.com.cn)
- UPSTREAM: 31163: add resource filter handling (jvallejo@redhat.com)
- refactor cli cmds: newapp, newbuild, logs, request_project and create unit
  tests (guilhermebr@gmail.com)
- Fix bug 1312278 Jenkins template has hardcoded SSL certificate.
  (jminter@redhat.com)
- Changed directory of slave image to /tmp (rymurphy@redhat.com)
- Refactor support for GitLab Push Event test case (admin@example.com)
- UPSTREAM: 32230: suggest-exposable resources in oc expose
  (jvallejo@redhat.com)
- suggest-exposable resources in oc expose (jvallejo@redhat.com)
- add --timeout flag to oc rsh (jvallejo@redhat.com)
- Add support for GitLab Push Event (admin@example.com)
- refactor the function 'getPlugin' in the
  'pkg/cmd/experimental/ipfailover/ipfailover.go' (miao.yanqiang@zte.com.cn)
- Ensure CLI and web console clients are public OAuth clients, pass token url
  to web console (jliggitt@redhat.com)
- suggest specifying flags before resource name (jvallejo@redhat.com)
- delete a unused function in the 'pkg/cmd/admin/policy/policy.go'
  (miao.yanqiang@zte.com.cn)

* Mon Sep 26 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.3
- The VS and dot is seprated (yu.peng36@zte.com.cn)
- add wildfly 10.1 spec (ch.raaflaub@gmail.com)
- fix deployment extended test condition (mfojtik@redhat.com)
- extended: Added new image pruning test (miminar@redhat.com)
- extended: Allow to re-deploy registry pod (miminar@redhat.com)
- Prune image configs of manifests V2 schema 2 (miminar@redhat.com)
- extended: Fix binary build helper (miminar@redhat.com)
- Renamed LayerDeleter to LayerLinkDeleter (miminar@redhat.com)
- fix panic when deployment is nil in describe (mfojtik@redhat.com)
- make oc set image resolve image stream images and tags using --source flag
  (mfojtik@redhat.com)
- UPSTREAM: 33083: Add ResolveImage function to CLI factory
  (mfojtik@redhat.com)
- add test case for function pushImage (li.guangxu@zte.com.cn)

* Fri Sep 23 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.2
- extended: fix latest deployment test flakes (mkargaki@redhat.com)
- verify and update protobufs in make verify/update (bparees@redhat.com)
- refactor cancelbuild cli cmd and add unit tests (guilhermebr@gmail.com)
- extract git revision condition (li.guangxu@zte.com.cn)
- The generated manpages were out of date. (bleanhar@redhat.com)
- Simplify binary build output in new-build #11000 (jminter@redhat.com)
- Fix NetNamespaces, which got accidentally broken in 58e8f93 (danw@redhat.com)
- Remove word additionaly (gethemant@gmail.com)
- UPSTREAM: 33141: don't mutate original client TLS config
  (jliggitt@redhat.com)
- Add bit about downloadable swagger-ui (gethemant@gmail.com)
- Update ose scripts to use 3.4 (tdawson@redhat.com)
- Error when test-cmd is given an invalid regex (mkhan@redhat.com)
- add /spec access for node (deads@redhat.com)
- Bump the timeout for deployment logs (mfojtik@redhat.com)
- Improve BuildConfig error reporting (mmilata@redhat.com)
- Changes the signature of CloneWithOptions function (rymurphy@redhat.com)
- fix noinput error msg in newbuild cli cmd (guilhermebr@gmail.com)
- Make links effective (zhao.sijun@zte.com.cn)
- return back the name you GETed for ISI (deads@redhat.com)
- Should hide the labels for route by oc get route (pcameron@redhat.com)
- Fix clusterresourcequota annotations validation (ffranz@redhat.com)
- extended test (mfojtik@redhat.com)
- Preserve valueFrom when merging envs in deployment strategy params
  (mfojtik@redhat.com)
- use a unique volume name for each input image secret (bparees@redhat.com)
- oc: generated code for 'set image' (mkargaki@redhat.com)
- oc: wire set image from kubectl (mkargaki@redhat.com)
- Remove terminating checks from origin namespace lifecycle admission
  (jliggitt@redhat.com)
- UPSTREAM: 32719: compensate for raft/cache delay in namespace admission
  (jliggitt@redhat.com)
- Made hello-openshift read the message from an environment variable
  (bbennett@redhat.com)
- modify the error info of test case (li.guangxu@zte.com.cn)
- remove call to compinit in zsh completion output (jvallejo@redhat.com)
- UPSTREAM: 32142: remove call to compinit in zsh completion output
  (jvallejo@redhat.com)
- SCC check API: refactor (salvatore-dario.minonne@amadeus.com)
- the open dockerfile need to be closed (li.guangxu@zte.com.cn)
- use const string for auth type if exist (li.guangxu@zte.com.cn)
- Use errors.New() instead of fmt.Errorf() where possible.
  (vsemushi@redhat.com)
- Allow users to choose database images version in the DB templates
  (vdinh@redhat.com)

* Tue Sep 20 2016 Troy Dawson <tdawson@redhat.com> 3.4.0.1
- Update tito to build for 3.4 (tdawson@redhat.com)
- Change spec file to the 3.4 branch (tdawson@redhat.com)
- Do not due bundled deps when building (tdawson@redhat.com)
- Enable defaults from upstream e2e framework, including logging
  (ccoleman@redhat.com)
- Suggest `oc get dc` in output of `oc deploy` (jvallejo@redhat.com)
- Add verbose output for `oadm groups new` (mkhan@redhat.com)
- Immediate exit if the return of  is (miao.yanqiang@zte.com.cn)
- Delete the extra dot (yu.peng36@zte.com.cn)
- Add bash symbol (yu.peng36@zte.com.cn)
- bump(github.com/coreos/etcd):v3.0.9 (ccoleman@redhat.com)
- Retry service account update correctly (jliggitt@redhat.com)
- Added necessary policies for running scheduled jobs (maszulik@redhat.com)
- Fix invalid hyperlink. (warmchang@outlook.com)
- Allow context to be provided to hack/env itself (ccoleman@redhat.com)
- UPSTREAM: docker/docker: <carry>: WORD/DWORD changed (ccoleman@redhat.com)
- Default qps/burst to historical values (jliggitt@redhat.com)
- Ensure system:master has full permissions on non-resource-urls
  (jliggitt@redhat.com)
- Disable go 1.6 in travis - it can't compile in under 10 minutes
  (ccoleman@redhat.com)
- Disable networking until it has been fixed (ccoleman@redhat.com)
- UPSTREAM: google/cadvisor: <drop>: Hack around cgroup load
  (ccoleman@redhat.com)
- generated: proto (ccoleman@redhat.com)
- generated: docs, swagger, and completions (ccoleman@redhat.com)
- Protobuf stringers disabled for OptionalNames (ccoleman@redhat.com)
- Debug: use master IP instead of localhost in nodeips (ccoleman@redhat.com)
- ImageStream tests now require user on context (ccoleman@redhat.com)
- Router event sends ADDED twice in violation of EventQueue semantics
  (ccoleman@redhat.com)
- Extended tests that are not yet ready for origin (ccoleman@redhat.com)
- Add the GC controller but default to off for now (ccoleman@redhat.com)
- Quota exceeded error message changed (ccoleman@redhat.com)
- test/cmd/migrate can race on image import under load (ccoleman@redhat.com)
- JSONPath output for nil changed slightly (ccoleman@redhat.com)
- Finalizers are reenabled temporarily (ccoleman@redhat.com)
- Describe should use imageapi.ParseImageStreamImageName (ccoleman@redhat.com)
- Check for GNU sed in os::util::sed (ccoleman@redhat.com)
- Add a simple prometheus config file (ccoleman@redhat.com)
- Error message from server has changed (ccoleman@redhat.com)
- Generators added scheduled jobs (ccoleman@redhat.com)
- Security admission now uses indexer and requires namespaces
  (ccoleman@redhat.com)
- Deployment related refactors (ccoleman@redhat.com)
- ImageStream limits should not start its own reflector (ccoleman@redhat.com)
- Wait for v2 registry test for server to come up (ccoleman@redhat.com)
- Update all permissions (ccoleman@redhat.com)
- Small refactors to tests to pass (ccoleman@redhat.com)
- Add DefaultStorageClass admission and disable by default ImagePolicyWebhook
  (ccoleman@redhat.com)
- Master configuration changes (ccoleman@redhat.com)
- Enable scheduled jobs controller and disruption budgets conditionally
  (ccoleman@redhat.com)
- Changes to util package reflected in tests (ccoleman@redhat.com)
- Add new top commands to 'oadm top' (ccoleman@redhat.com)
- Remove support for spec.portalIP (ccoleman@redhat.com)
- Dockerfile parser updates (ccoleman@redhat.com)
- Comment that SAR on namespace requires an upstream patch
  (ccoleman@redhat.com)
- DeepCopy requires pointer inputs now (ccoleman@redhat.com)
- Go 1.7 does not allow empty string req.URL.Path (ccoleman@redhat.com)
- Man page generation should skip hidden flags (ccoleman@redhat.com)
- LeaderLease off by one (ccoleman@redhat.com)
- Update integration tests with compilation changes (ccoleman@redhat.com)
- util.Clock moved to util/clock (ccoleman@redhat.com)
- Owner references are now required for kubernetes controllers
  (ccoleman@redhat.com)
- Update extended test code for 1.4 (ccoleman@redhat.com)
- Move the leaderlease package to the new etcd client (ccoleman@redhat.com)
- MasterLeaser was incorrect with new storage config (ccoleman@redhat.com)
- Use Quorum reads for OAuth and service account token reads
  (ccoleman@redhat.com)
- Support new Unstructured flows for get and create in factory
  (ccoleman@redhat.com)
- Add StorageClass access to the PV binder (ccoleman@redhat.com)
- Register Kubernetes log package early (ccoleman@redhat.com)
- Update Kubernetes node and controllers (ccoleman@redhat.com)
- Simple master signature changes (ccoleman@redhat.com)
- Refactor NewConfigGetter again to get closer to correct behavior
  (ccoleman@redhat.com)
- Switch to using storagebackend.Factory consistently (ccoleman@redhat.com)
- Use kubernetes Namespace informer, send Informers to admission
  (ccoleman@redhat.com)
- Accept cache.TriggerPublisher on ApplyOptions, use StorageFactory
  (ccoleman@redhat.com)
- Signature changes to CLI commands (ccoleman@redhat.com)
- Other kubectl and smaller moves (ccoleman@redhat.com)
- Printer takes options by value and GetPrinter takes noHeaders
  (ccoleman@redhat.com)
- Simplify AuthorizationAdapter now that upstream matches our signature
  (ccoleman@redhat.com)
- Deployment changes related to Scaler/Rollbacker/Client (ccoleman@redhat.com)
- Repair package changed (ccoleman@redhat.com)
- Validation constants are no longer public (ccoleman@redhat.com)
- Use go-dockerclient.ParseRepositoryTag() (ccoleman@redhat.com)
- Update to use generic.SelectionPredicate (ccoleman@redhat.com)
- Rename GV*.IsEmpty() to GV*.Empty() (ccoleman@redhat.com)
- Switch to new SchemeBuilder registration (ccoleman@redhat.com)
- Add kapi.Context to PrepareForCreate/PrepareForUpdate (ccoleman@redhat.com)
- Update API types with proper generator tags (ccoleman@redhat.com)
- Update gendeepcopy and genconversion (ccoleman@redhat.com)
- bump(k8s.io/kubernetes):d19513fe86f3e0769dd5c4674c093a88a5adb8b4
  (ccoleman@redhat.com)
- Enable temporary swap when on Linux and memory is low (ccoleman@redhat.com)
- Preserve Go build artifacts from test compilation (ccoleman@redhat.com)
- Update generated clientsets should use get_version_vars (ccoleman@redhat.com)
- Add cloudflare/cfssl as an upstream to restore Godeps from
  (ccoleman@redhat.com)
- The pod GC controller has been moved to a different package
  (ccoleman@redhat.com)
- Switch to github.com/docker/go-units (ccoleman@redhat.com)
- Net utilities have been moved, update imports (ccoleman@redhat.com)
- Strip removed deployment utility package (ccoleman@redhat.com)
- Refactor dockerfile code to latest Docker 1.12 (ccoleman@redhat.com)
- Magic Git tag transformations are awesome too (ccoleman@redhat.com)
- Release regex is awesome (ccoleman@redhat.com)
- remove the redundant spaces (haowang@redhat.com)
- Run zookeeper as non-root user. Fix zookeeper conf volumeMount.
  (ghyde@redhat.com)
- The promt is missed (yu.peng36@zte.com.cn)
- The 'eg' is should be 'e.g.', and 'for example' is better here
  (yu.peng36@zte.com.cn)
- use a post deploy hook that will pass, not fail (bparees@redhat.com)
- Allow annotation selector to match annotation values (jliggitt@redhat.com)
- Add service account for attach-detach controller (pmorie@redhat.com)
- Add logging to assist in determining openid claims (jliggitt@redhat.com)
- tolerate multiple =s in a parameter value (bparees@redhat.com)
- remove all tmp dir after test (li.guangxu@zte.com.cn)
- Fix issue#10853. Route cleanup does not need service key cleanup.
  (rchopra@redhat.com)
- sdn: convert from OpenShift client cache to k8s DeltaFIFO (dcbw@redhat.com)
- delete the unused function NameFromImageStream (li.guangxu@zte.com.cn)
- hack/release.sh should os::log::warn (ccoleman@redhat.com)
- Allow hack/env to reuse volumes (ccoleman@redhat.com)
-   Fix some typos for router_sharding.md (li.xiaobing1@zte.com.cn)
- Don't fail during negotiation when /oapi is missing (ccoleman@redhat.com)
- Make Kube version info best effort, and don't fail fast (ccoleman@redhat.com)
- JenkinsPipelineStrategy nil no need check again (li.guangxu@zte.com.cn)
- Added a mention of 'oc get' to 'oc get --help' (rymurphy@redhat.com)
- extended: add readiness test for initial deployments (mkargaki@redhat.com)
- deploy: deployment utilities and cmd fixes (mkargaki@redhat.com)
- extended: update polling for deployment tests (mkargaki@redhat.com)
- delete the redundant loop that save slice to map (li.guangxu@zte.com.cn)
- deploy: use upstream pod lister method (mkargaki@redhat.com)
- deploy: move cancellation event just after the deployment update
  (mkargaki@redhat.com)
- Fix a func name and return value in the comment of NewREST
  (wang.yuexiao@zte.com.cn)

* Tue Sep 06 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.30
- Fix wrong oadm document name in cli.md (li.xiaobing1@zte.com.cn)
- Image size needs to add a size of manifest config file (miminar@redhat.com)
- New e2e test: fetch manifest schema 2 with old client (miminar@redhat.com)
- Pullthrough blobs using Get() as well (miminar@redhat.com)
- Remember image with matching config reference (miminar@redhat.com)
- website changed for openshift and can be accessed directly
  (li.xiaobing1@zte.com.cn)
- UPSTREAM: <carry>: Tolerate node ExternalID changes with no cloud provider
  (pmorie@redhat.com)
- UPSTREAM: 32000: Update node status instead of node in kubelet
  (pmorie@redhat.com)
- Release should pass OS_GIT_COMMIT as a commit, not a tag
  (ccoleman@redhat.com)
- Reconcile non-resource-urls (jliggitt@redhat.com)
- UPSTREAM: 31627: make deep copy of quota objects before mutations
  (deads@redhat.com)

* Fri Sep 02 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.29
- The etc and dot is seprated (yu.peng36@zte.com.cn)
- Add a Docker image that will be built separately to run observe
  (ccoleman@redhat.com)
- generated: Completions and doc (ccoleman@redhat.com)
- Add an experimental observe command to handle changes to objects
  (ccoleman@redhat.com)
- UPSTREAM: 31714: Allow missing keys in jsonpath (ccoleman@redhat.com)
- UPSTREAM: <carry>: Tolerate node ExternalID changes with no cloud provider
  (pmorie@redhat.com)
- UPSTREAM: 31730: Make it possible to enable controller-managed attach-detach
  on existing nodes (pmorie@redhat.com)
- UPSTREAM: 31531: Add log message in Kuelet when controller attach/detach is
  enabled (pmorie@redhat.com)
- UPSTREAM: revert: 88abe47b9a963b41acd0c4f0fd18827192648468: <carry>: Tolerate
  node ExternalID changes with no cloud provider (pmorie@redhat.com)
- Bump origin-web-console (7d59453) (jforrest@redhat.com)
- deploy: don't requeue configs on stream updates yet (mkargaki@redhat.com)
- eg. should be e.g. (yu.peng36@zte.com.cn)
- bump(k8s.io/kubernetes):52492b4bff99ef3b8ca617d385a3ff0612f9402d
  (ccoleman@redhat.com)
- Make the router data structures remove duplicates cleanly
  (bbennett@redhat.com)
- Generated man/docs for reverting plugin auto detection (rpenta@redhat.com)
- Revert openshift sdn plugin auto detection on the node (rpenta@redhat.com)
- Compare additionally generation when comparing ImageStreamTag status with
  spec (maszulik@redhat.com)
- extended: bump deployment timeout for test about tagging
  (mkargaki@redhat.com)
- suggest use of `oc get bc` on `oc start-build` error output
  (jvallejo@redhat.com)
- extended: require old deployments to be equal to the expected amount
  (mkargaki@redhat.com)
- delete unused function panicIfStopped (li.guangxu@zte.com.cn)

* Wed Aug 31 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.28
- remove unnecessary service account edit step (bparees@redhat.com)
- Bump origin-web-console (39ffada) (jforrest@redhat.com)
- add test case for function GetDockerAuth (li.guangxu@zte.com.cn)
- add permissions for jenkins (deads@redhat.com)
- Make build spec file platform independent (mkumatag@in.ibm.com)
- Switch deployment utils to loop by index (zhao.sijun@zte.com.cn)
- Retry on registry client connect on tag unset (miminar@redhat.com)
- be tolerant of quota reconciler resetting to old values (deads@redhat.com)
- Return the exit code of the hack/env container (ccoleman@redhat.com)
- update the README outputs of the sample (li.guangxu@zte.com.cn)
- fix protobuff generation for the sdn (ipalade@redhat.com)

* Mon Aug 29 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.27
- Merge remote-tracking branch upstream/master, bump origin-web-console 3ef22d6
  (tdawson@redhat.com)
- Scale helpers: always fetch scale object for DCs (sross@redhat.com)
- Regenerate proxy iptables rules on EgressNetworkPolicy change
  (danw@redhat.com)
- Idle command: make sure to always print errors (sross@redhat.com)
- Restores the service proxier when unidling is disabled (bbennett@redhat.com)
- Automatically check and update docker-registry configuration
  (agladkov@redhat.com)
- Bump origin-web-console (b0cc495) (jforrest@redhat.com)
- UPSTREAM: openshift/source-to-image: 576: increase default docker timeout
  (gmontero@redhat.com)
- fix `oc set env` key-value pair matching (jvallejo@redhat.com)
- extended: debug failed tag update (mkargaki@redhat.com)
- Unidling Controller: Deal with tombstones in cache (sross@redhat.com)
- SCC API check: move (salvatore-dario.minonne@amadeus.com)

* Fri Aug 26 2016 Scott Dodson <sdodson@redhat.com> 3.3.0.26
- [RPMs] tito builds are always clean (sdodson@redhat.com)
- UPSTREAM: 31463: Add a line break when no events in describe
  (ffranz@redhat.com)
- Bump origin-web-console (98cd97c) (jforrest@redhat.com)
- UPSTREAM: 31446: Do initial 0-byte write to stdout when streaming container
  logs (jliggitt@redhat.com)
- UPSTREAM: 31446: Make limitWriter respect 0-byte writes until limit is
  reached (jliggitt@redhat.com)
- UPSTREAM: 31446: Send ping frame using specified encoding
  (jliggitt@redhat.com)
- UPSTREAM: 31396: Fixed integer overflow bug in rate limiter
  (deads@redhat.com)
- UPSTREAM: docker/distribution: 1703: GCS: FileWriter.Size: include number of
  buffered bytes if the FileWriter is not closed (mfojtik@redhat.com)
- Remove NotV2Registry check from redhat registry import test
  (mfojtik@redhat.com)
- fix autoprovision enabled field name (bparees@redhat.com)
- UPSTREAM: 31353: add unit test for duplicate error check
  (jvallejo@redhat.com)
- Bump origin-web-console (18a0d95) (jforrest@redhat.com)
- update invalid oc extract usage flag to "keys" (jvallejo@redhat.com)
- UPSTREAM: 31353: fix duplicate validation/field/errors (jvallejo@redhat.com)
- deploy: do not retry when deployer pod fail to start (mfojtik@redhat.com)
- Revert "add test to exercise deployment logs for multi-container pods"
  (mfojtik@redhat.com)
- Revert "Pass the container name to deployment config log options"
  (mfojtik@redhat.com)
- fix 'oadm policy' description error (miao.yanqiang@zte.com.cn)
- cluster up: use rslave propagation mode with nsenter mounter
  (cewong@redhat.com)
- when sercret was found need break the loop (li.guangxu@zte.com.cn)
- Add OVS rule creation/cleanup tests to extended networking test
  (danw@redhat.com)

* Wed Aug 24 2016 Scott Dodson <sdodson@redhat.com> 3.3.0.25
- Emit event when cancelling a deployment (mfojtik@redhat.com)
- deployments: make retries faster on update conflicts (mfojtik@redhat.com)
- UPSTREAM: 30896: Add Get() to ReplicationController lister
  (mfojtik@redhat.com)
- Bump origin-web-console (d24e068) (jforrest@redhat.com)
- Removing the VOLUME directive in the ose image (abhgupta@redhat.com)
- HAProxy Router: Invert health-check idled check (sross@redhat.com)
- note the change to oc tag -d (deads@redhat.com)
- Improve oc new-app examples. (vsemushi@redhat.com)
- sdn: clear kubelet-created initial NetworkUnavailable condition on GCE
  (dcbw@redhat.com)
- add test for non-duplicate error outputs (jvallejo@redhat.com)
- increase jenkins readiness timeout (bparees@redhat.com)
- An independent branch dealing with errors (root@master0.cloud.com.novalocal)
- private function mergeWithoutDuplicates no longer in use
  (li.guangxu@zte.com.cn)
- Clean up requested project if there are errors creating template items
  (jliggitt@redhat.com)
- retrieve keys from cache.Delta objects properly (bparees@redhat.com)
- Bump origin-web-console (0ab36ca) (jforrest@redhat.com)
- Fix gitserver bc search (cewong@redhat.com)
- Support init containers in 'oc debug' (agoldste@redhat.com)
- UPSTREAM: 31150: Check init containers in PodContainerRunning
  (agoldste@redhat.com)
- update swagger dev README with updated script name (aweiteka@redhat.com)
- fix pre-deploy hook args on cakephp example (bparees@redhat.com)
- Enable secure cookie for secure-only edge routes (marun@redhat.com)
- Usability improvements to failures in oc login (ffranz@redhat.com)
- fix json serialization in admissionConfig (deads@redhat.com)
- Re-setup SDN on startup if ClusterNetworkCIDR changes (danw@redhat.com)
- UPSTREAM: 30313: add unit test for duplicate errors (jvallejo@redhat.com)
- UPSTREAM: 30313: remove duplicate errors from aggregate error outputs
  (jvallejo@redhat.com)
- add suggestion to use `describe` to obtain container names
  (jvallejo@redhat.com)
- test: move e2e deployment test in extended suite (mkargaki@redhat.com)
- It is better to add "\n" in printf (yu.peng36@zte.com.cn)
- UPSTREAM: 30717: add suggestion to use `describe` to obtain container names
  (jvallejo@redhat.com)
- Fix typo in gen_man.go (mkumatag@in.ibm.com)
- Run updated docs (mdame@redhat.com)
- UPSTREAM: 28234: Make sure --record=false is acknowledged when passed to
  commands (mdame@redhat.com)
- Fix somee mistakes in script as follow: (wang.yuexiao@zte.com.cn)
- deploy: remove top level generator pkg (mkargaki@redhat.com)
- deploy: update validation for deploymentconfigs (mkargaki@redhat.com)
- Regenerate swagger docs (danw@redhat.com)
- Improve the SDN API docs a little bit (danw@redhat.com)
- Regenerate oc completions (danw@redhat.com)
- Add "oc describe" support for sdn types (danw@redhat.com)

* Mon Aug 22 2016 Scott Dodson <sdodson@redhat.com> 3.3.0.24
- generated: Docs and examples (ccoleman@redhat.com)
- Implement oc set route-backend and A/B to describers / printers
  (ccoleman@redhat.com)
- UPSTREAM: 31047: Close websocket stream when client closes
  (jliggitt@redhat.com)
- Bump origin-web-console (3fb0c3e) (jforrest@redhat.com)
- set image ref namespace when src project not specified (jvallejo@redhat.com)
- Improve the image stream describer (ccoleman@redhat.com)
- test-cmd updates for --raw (deads@redhat.com)
- UPSTREAM: 30445: add --raw for kubectl get (deads@redhat.com)
- Use non-secure cookie when tls and non-tls enabled (marun@redhat.com)
- Add a default ingress ip range (marun@redhat.com)
- UPSTREAM: 25308: fix rollout nil panic issue (agoldste@redhat.com)
- re-enable the build defaulter plugin by default (bparees@redhat.com)
- UPSTREAM: <carry>: JitterUntil should defer to utilruntime.HandleCrash on
  panic (decarr@redhat.com)
- BuildRequire golang greater than or equal to golang_version
  (tdawson@redhat.com)
- -pkgdir should not be root of project (ccoleman@redhat.com)
- add test to exercise deployment logs for multi-container pods
  (mfojtik@redhat.com)
- better debugging info for deployment flakes (mfojtik@redhat.com)
- BZ 1368050: add ability to change connection limits for reencrypt and
  passthrough routes (jtanenba@redhat.com)
- Highlight only active deployment in describer (mfojtik@redhat.com)
- Pass the container name to deployment config log options (mfojtik@redhat.com)
- Retry updating deployment config instead of creating new one in test
  (mfojtik@redhat.com)
- merge duplicate code (li.guangxu@zte.com.cn)
- UPSTREAM: 26680: Don't panic in NodeController if pod update fails
  (agoldste@redhat.com)
- UPSTREAM: 28697: Prevent kube-proxy from panicing when sysfs is mounted as
  read-only. (agoldste@redhat.com)
- UPSTREAM: 28744: Allow a FIFO client to requeue under lock
  (agoldste@redhat.com)
- UPSTREAM: 29581: Kubelet: Fail kubelet if cadvisor is not started.
  (agoldste@redhat.com)
- UPSTREAM: 29672: Add handling empty index key that may cause panic issue
  (agoldste@redhat.com)
- UPSTREAM: 29531: fix kubectl rolling update empty file cause panic issue
  (agoldste@redhat.com)
- UPSTREAM: 29743: Fix race condition found in JitterUntil
  (agoldste@redhat.com)
- UPSTREAM: 30291: Prevent panic in 'kubectl exec' when redirecting stdout
  (agoldste@redhat.com)
- UPSTREAM: 29594: apiserver: fix timeout handler (agoldste@redhat.com)
- disable jenkins auto-deployment (bparees@redhat.com)
- Remove VOLUME from Origin image (ccoleman@redhat.com)
- UPSTREAM: 30690: Don't bind pre-bound pvc & pv if size request not satisfied
  and continue searching on bad size and add tests for bad size&mode.
  (avesh.ncsu@gmail.com)
- update image policy API for first class resolution (deads@redhat.com)
- Router provides an invalid, expired certificate (pcameron@redhat.com)
- clarify idle error and usage output (jvallejo@redhat.com)
- Fixed extended unilding tests (sross@redhat.com)
- HAProxy Router: Don't health-check idled services (sross@redhat.com)
- Fix for BZ#1367937 which prevents CEPH RBD from working on atomic host.
  (bchilds@redhat.com)
- Now check for length on error array (rymurphy@redhat.com)
- UPSTREAM: 30579: Remove trailing newlines on describe (ccoleman@redhat.com)
- To break the for loop when found = true (li.xiaobing1@zte.com.cn)

* Fri Aug 19 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.23
- BuildRequires bsdtar, for hack scripts (tdawson@redhat.com)
- Disable ingress ip when cloud provider enabled (marun@redhat.com)
- Bump origin-web-console (4d411df) (jforrest@redhat.com)
- Fix oc project|projects when in cluster config (ffranz@redhat.com)
- move unrelated extended tests out of images (ipalade@redhat.com)
- bump(k8s.io/kubernetes): 447cecf8b808caa00756880f2537b2bafbfcd267
  (deads@redhat.com)
- UPSTREAM: 29093: Fix panic race in scheduler cache from 28886
  (ccoleman@redhat.com)
- calculate usage on istag creates (deads@redhat.com)
- compute image stream usage properly on istag touches (deads@redhat.com)
- UPSTREAM: 30907: only compute delta on non-creating updates
  (deads@redhat.com)
- UPSTREAM: google/cadvisor: 1359: Make ThinPoolWatcher loglevel consistent
  (agoldste@redhat.com)
- bump(google/cadvisor): 956e595d948ce8690296d297ba265d5e8649a088
  (agoldste@redhat.com)
- Allowed 'true' for the DROP_SYN_DURING_RESTART variable (bbennett@redhat.com)
- Randomize delay in router stress test. (marun@redhat.com)
- Add previous-scale annotation for idled resources (sross@redhat.com)
- Fixed the comment about the different backends we make (bbennett@redhat.com)
- block setting ownerReferences and finalizers (deads@redhat.com)
- UPSTREAM: 30839: queueActionLocked requires write lock (deads@redhat.com)
- UPSTREAM: 30624: Node controller deletePod return true if there are pods
  pending deletion (agoldste@redhat.com)
- UPSTREAM: 30277: Avoid computing DeepEqual in controllers all the time
  (agoldste@redhat.com)
- fix a logical error of the function 'RunCmdRouter' in the , the same as the
  funtion 'RunCmdRegistry' in the (miao.yanqiang@zte.com.cn)
- generate_vrrp_sync_groups calls expand_ip_ranges on an already expanded
  ranges (cameron@braid.com.au)
- Bump origin-web-console (8c03ff4) (jforrest@redhat.com)
- UPSTREAM: 29639: <drop>: Fix default resource limits (node allocatable) for
  downward api volumes and env vars. (avesh.ncsu@gmail.com)
- Fix validation of pkg/sdn/api object updates (danw@redhat.com)
- UPSTREAM: 30731: Always return command output for exec probes and kubelet
  RunInContainer (agoldste@redhat.com)
- UPSTREAM: 30796: Quota usage checking ignores unrelated resources
  (decarr@redhat.com)
- regen protos (bparees@redhat.com)
- Make it easier to extract content from hack/env (ccoleman@redhat.com)
- UPSTREAM: 27541: Attach should work for init containers (ccoleman@redhat.com)
- UPSTREAM: 30736: Close websocket watch when client closes
  (jliggitt@redhat.com)
- Added Git logging to build output (rymurphy@redhat.com)
- deploy: reconcile streams on config creation/updates (mkargaki@redhat.com)
- Bug 1366936: fix ICT matching in the trigger controller (mkargaki@redhat.com)
- Variable definition is not used (li.guangxu@zte.com.cn)
- add test cases for `oc set env` (jvallejo@redhat.com)
- return error when no env args are given (jvallejo@redhat.com)
- check CustomStrategy validation at begin (li.guangxu@zte.com.cn)
- force all plugins to either default off or default on (deads@redhat.com)
- integration: fix imagestream admission flake (miminar@redhat.com)
- Improve tests for extended build. (vsemushi@redhat.com)
- Revert "test: extend timeout in ICT tests to the IC controller resync
  interval" (mkargaki@redhat.com)
- Return original error on on limit error (miminar@redhat.com)
- Fix haproxy config bug. (smitram@gmail.com)
- Fix somee mistakes in script as follow: (wang.yuexiao@zte.com.cn)
- UPSTREAM: 30533: Validate involvedObject.Namespace matches event.Namespace
  (jliggitt@redhat.com)
- support for zero weighted services in a route (rchopra@redhat.com)
- UPSTREAM: 30713: Empty resource type means no defaulting
  (ccoleman@redhat.com)
- Extract should default to current directory (ccoleman@redhat.com)
- deprecate --list option from `volumes` cmd (jvallejo@redhat.com)
- Bug 1330201 - Periodically sync k8s iptables rules (rpenta@redhat.com)
- call out config validation warnings more clearly (deads@redhat.com)
- Show restart count warnings only for latest deployment (mfojtik@redhat.com)
- Fix scrub pod container command (mawong@redhat.com)
- Updated auto generated doc for pod-network CLI commands (rpenta@redhat.com)
- Updated auto generated bash completions for pod-network CLI commands
  (rpenta@redhat.com)
- Added test cases for 'oadm pod-network isolate-projects' (rpenta@redhat.com)
- CLI changes to support project network isolation (rpenta@redhat.com)
- Make pod-network cli command to use ChangePodNetworkAnnotation instead of
  updating VNID directly (rpenta@redhat.com)
- Remove old SDN netid allocator (rpenta@redhat.com)
- Test cases for assign/update/revoke VNIDs (rpenta@redhat.com)
- Handling VNID manipulations (rpenta@redhat.com)
- Test cases for network ID allocator interface (rpenta@redhat.com)
- Added network ID allocator interface (rpenta@redhat.com)
- Test cases for network ID range interface (rpenta@redhat.com)
- Added network ID range interface (rpenta@redhat.com)
- Accessor methods for ChangePodNetworkAnnotation on NetNamespace
  (rpenta@redhat.com)
- have origin.spec use hack scripts to build (tdawson@redhat.com)
- Allow startup to continue even if nodes don't have EgressNetworkPolicy list
  permission (danw@redhat.com)
- add a validateServiceAccount to the creation of ipfailover pods
  (jtanenba@redhat.com)

* Wed Aug 17 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.22
- Return directly if no pods found when evacuating (zhao.xiangpeng@zte.com.cn)
- Bump origin-web-console (5fa2bd9) (jforrest@redhat.com)
- add new-app support for detecting .net apps (bparees@redhat.com)
- Use scheme/host from request for token redirect (jliggitt@redhat.com)
- Modify a error variable (miao.yanqiang@zte.com.cn)
- Revert "add suggestion to use `describe` to obtain container names"
  (ccoleman@redhat.com)
- allow SA oauth clients to list projects (deads@redhat.com)
- namespace scope all our new admission plugins (deads@redhat.com)
- Update to released Go 1.7 (ccoleman@redhat.com)
- Allow registry-admin and registry-editor create serviceaccounts
  (agladkov@redhat.com)
- fail server on bad admission (deads@redhat.com)
- extended: retry on update conflicts in deployment tests (mkargaki@redhat.com)
- test: extend timeout in ICT tests to the IC controller resync interval
  (mkargaki@redhat.com)
- The first letter should be capitalized (yu.peng36@zte.com.cn)
- func getCredentials no longer in use (li.guangxu@zte.com.cn)
- Bug 1365450 - Fix SDN plugin name change (rpenta@redhat.com)
- Bump origin-web-console (bc567c7) (jforrest@redhat.com)
- add suggestion to use `describe` to obtain container names
  (jvallejo@redhat.com)
- bump(github.com/openshift/source-to-image):
  89b96680e451c0fa438446043f967b5660942974 (bparees@redhat.com)
- Moving from enviornment variables to annotaions for healthcheck interval
  (erich@redhat.com)
- record quota errors on image import conditions (pweil@redhat.com)
- oc start-build: display an error when git is not available and --from-repo is
  requested (cewong@redhat.com)
- Adding ENV's for Default Router timeout settings, and adding validation
  (erich@redhat.com)
- UPSTREAM: 30510: Endpoint controller logs errors during normal cluster
  behavior (decarr@redhat.com)
- Improve grant page appearance, allow partial scope grants
  (jliggitt@redhat.com)
- UPSTREAM: 30626: prevent RC hotloop on denied pods (deads@redhat.com)
- remove redundant comment in build-base-images.sh (wang.yuexiao@zte.com.cn)
- if err is nil return nil directly (li.guangxu@zte.com.cn)
- Fix pullthrough serve blob (miminar@redhat.com)
- Ignore negative value of grace-period and add more evacuate examples
  (zhao.xiangpeng@zte.com.cn)
- Pullthrough logging improvements (miminar@redhat.com)
- Allow to pull from insecure registries for unit tests (miminar@redhat.com)
- add func to instead of lengthiness parameters (wang.yuexiao@zte.com.cn)
- Stop using node selector as ipfailover label (marun@redhat.com)
- Changes createLocalGitDirecory to s2i version (rymurphy@redhat.com)
- fix up image policy admission plugin (deads@redhat.com)
- bump(github.com/openshift/source-to-image):
  2878c1ab41784dab0a467e12a200659506174e68 (jupierce@redhat.com)
- Set xff headers for reencrypt[ed] routes. (smitram@gmail.com)
- Delete EgressNetworkPolicy objects on namespace deletion (danw@redhat.com)
- UPSTREAM: 29982: Fix PVC.Status.Capacity and AccessModes after binding
  (jsafrane@redhat.com)

* Mon Aug 15 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.21
- Need to set OS_ROOT for tito (tdawson@redhat.com)
- The first letter should be capitalized (yu.peng36@zte.com.cn)
- bump(github.com/AaronO/go-git-http) 34209cf6cd947cfa52063bcb0f6d43cfa50c5566
  (cewong@redhat.com)
- don't do pod deletion management for pipeline builds (bparees@redhat.com)
- Bump origin-web-console (1e55231) (jforrest@redhat.com)
- Updated bash preamble in test/cmd/run.sh (skuznets@redhat.com)
- Update generated docs and completions (ffranz@redhat.com)
- Fixes required by latest version of Cobra (ffranz@redhat.com)
- bump(github.com/spf13/cobra): f62e98d28ab7ad31d707ba837a966378465c7b57
  (ffranz@redhat.com)
- bump(github.com/spf13/pflag): 1560c1005499d61b80f865c04d39ca7505bf7f0b
  (ffranz@redhat.com)
- Avoid using bsdtar for extraction during build (joesmith@redhat.com)
- Removed executable check from test-cmd test filter (skuznets@redhat.com)
- Remain in the current project at login if possible (jliggitt@redhat.com)
- Moved shared init code into hack/lib/init.sh (skuznets@redhat.com)
- respect scopes in list/watch projects (deads@redhat.com)
- Add zsh compatibility note to `completion` help (jvallejo@redhat.com)
- UPSTREAM: 30460: Add zsh compatibility note `completion` cmd help
  (jvallejo@redhat.com)

* Mon Aug 15 2016 Troy Dawson <tdawson@redhat.com>
- Need to set OS_ROOT for tito (tdawson@redhat.com)
- The first letter should be capitalized (yu.peng36@zte.com.cn)
- bump(github.com/AaronO/go-git-http) 34209cf6cd947cfa52063bcb0f6d43cfa50c5566
  (cewong@redhat.com)
- don't do pod deletion management for pipeline builds (bparees@redhat.com)
- Bump origin-web-console (1e55231) (jforrest@redhat.com)
- Updated bash preamble in test/cmd/run.sh (skuznets@redhat.com)
- Update generated docs and completions (ffranz@redhat.com)
- Fixes required by latest version of Cobra (ffranz@redhat.com)
- bump(github.com/spf13/cobra): f62e98d28ab7ad31d707ba837a966378465c7b57
  (ffranz@redhat.com)
- bump(github.com/spf13/pflag): 1560c1005499d61b80f865c04d39ca7505bf7f0b
  (ffranz@redhat.com)
- Avoid using bsdtar for extraction during build (joesmith@redhat.com)
- Removed executable check from test-cmd test filter (skuznets@redhat.com)
- Remain in the current project at login if possible (jliggitt@redhat.com)
- Moved shared init code into hack/lib/init.sh (skuznets@redhat.com)
- respect scopes in list/watch projects (deads@redhat.com)
- Add zsh compatibility note to `completion` help (jvallejo@redhat.com)
- UPSTREAM: 30460: Add zsh compatibility note `completion` cmd help
  (jvallejo@redhat.com)

* Fri Aug 12 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.19
- Merge remote-tracking branch upstream/master, bump origin-web-console 01e7f6b
  (tdawson@redhat.com)
- mark extended builds experimental (bparees@redhat.com)
- the tmpfile may be not closed when function DownloadFromContainer returns err
  (li.guangxu@zte.com.cn)
- Improving circular dependency checking for new-build (jupierce@redhat.com)
- Adding -o=name to start-build (jupierce@redhat.com)
- add tests; mv printer tests to separate file (jvallejo@redhat.com)
- Add the default image policy to bootstrap bindata (ccoleman@redhat.com)
- Make hack commands more consistent and add policy to bindata
  (ccoleman@redhat.com)
- Enable a simple image policy admission controller (ccoleman@redhat.com)
- Make DefaultRegistryFunc and PodSpec extraction generic (ccoleman@redhat.com)
- Fix govet complains (maszulik@redhat.com)
- Change go version detection logic (maszulik@redhat.com)
- Bump origin-web-console (233c7f3) (jforrest@redhat.com)
- Bug 1363630 - Print shortened parent ID in oadm top images
  (maszulik@redhat.com)
- Revert "Bug 1281735 - remove the internal docker registry information from
  imagestream" (ccoleman@redhat.com)
- fix broken paths and redirects for s2i containers (ipalade@redhat.com)
- show namespace for custom strategy bc (jvallejo@redhat.com)
- remove redundant example from `oc projects` (jvallejo@redhat.com)
- SourceStrategy: assign PullSecret when only RuntimeImage needs it.
  (vsemushi@redhat.com)
- Fix `oc idle` help text (sross@redhat.com)
- Ensure only endpoints are specified in `oc idle` (sross@redhat.com)
- add unit tests for s2iProxyConfig and buildEnvVars (ipalade@redhat.com)
- add test case (jvallejo@redhat.com)
- UPSTREAM: 30162: return err on oc run --image with invalid value
  (jvallejo@redhat.com)
- show project labels (deads@redhat.com)
- add metrics to clusterquota controllers (deads@redhat.com)
- UPSTREAM: 30296: add metrics for workqueues (deads@redhat.com)
- Mark ingress as tech-preview in README (mfojtik@redhat.com)
- go-binddata can not found when GOPATH is a list of directories
  (li.guangxu@zte.com.cn)
- refactor function parameters (li.guangxu@zte.com.cn)
- Addressing the issues identified in BZ 1341312 (erich@redhat.com)
- diagnostics: fix bug 1359771 (lmeyer@redhat.com)
- make db user/password parameter description clearer (bparees@redhat.com)
- Use default scrub pod template for NFS recycler (mawong@redhat.com)
- move cmd tools to common build cmd package (bparees@redhat.com)
- fix some bugs with ROUTER_SLOW_LORIS_TIMEOUT (jtanenba@redhat.com)

* Wed Aug 10 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.18
- Merge remote-tracking branch upstream/master, bump origin-web-console 4a118e0
  (tdawson@redhat.com)
- Fix test compile error (jliggitt@redhat.com)
- Add scope representing full user permissions, default token requests with
  unspecified scope (jliggitt@redhat.com)
- make build API validation compile (deads@redhat.com)
- Fix openshift/origin-release:golang-1.4 image (agoldste@redhat.com)
- Clean up test etcd data in test loops (jliggitt@redhat.com)
- UPSTREAM: 29212: hpa: ignore scale targets whose replica count is 0
  (sross@redhat.com)
- Make HAProxy Router Aware of Idled Services (sross@redhat.com)
- Introduce the Unidler Socket (sross@redhat.com)
- Add the `oc idle` command (sross@redhat.com)
- Introduce Unidling Controller (sross@redhat.com)
- Introduce the Hybrid Proxy (sross@redhat.com)
- Changed the userspace proxy to remove conntrack entries (bbennett@redhat.com)
- Fork Kubernetes Userspace Proxy (sross@redhat.com)
- Recognize gzipped empty layer when marking parents in oadm top images
  (maszulik@redhat.com)
- fix typo in deployment (wang.yuexiao@zte.com.cn)
- Add link for details on controlling Docker options with systemd
  (vichoudh@redhat.com)
- Support network ingress on arbitrary ports (marun@redhat.com)
- Use a consistent process for the official release (ccoleman@redhat.com)
- Add MongoDB connection URL to template message (spadgett@redhat.com)
- The docker-builder url is not found (yu.peng36@zte.com.cn)
- fix rpm spec file to properly build man pages dynamically
  (tdawson@redhat.com)
- Make import image more efficient (miminar@redhat.com)
- Remove allocated IPs from app-scenarios test data (jliggitt@redhat.com)
- Isolate graph test data (jliggitt@redhat.com)
- Bug 1281735 - remove the internal docker registry information from
  imagestream (maszulik@redhat.com)
- Add more info for test case (zhao.xiangpeng@zte.com.cn)
- change "timeout server" to "timeout tunnel" for pass through routes
  (jtanenba@redhat.com)
- Drop the SDN endpoint filter pod watch (danw@redhat.com)
- support for defaulting s2i incremental field at the cluster level
  (bparees@redhat.com)
- display build config dependencies more explicitly in oc status; also note
  input images have scheduled imports (gmontero@redhat.com)

* Mon Aug 08 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.17
- Bump origin-web-console (5ae75bb) (jforrest@redhat.com)
- update help and option suggestions on cmds acting as root cmd
  (jvallejo@redhat.com)
- UPSTREAM: google/cadvisor: 1359: Make ThinPoolWatcher loglevel consistent
  (agoldste@redhat.com)
- UPSTREAM: 29961: Allow PVs to specify supplemental GIDs (agoldste@redhat.com)
- UPSTREAM: 29576: Retry assigning CIDRs in case of failure
  (agoldste@redhat.com)
- UPSTREAM: 29246: Kubelet: Set PruneChildren when removing image
  (agoldste@redhat.com)
- UPSTREAM: 29063: Automated cherry pick of #28604 #29062 (agoldste@redhat.com)
- Update RunNodeController to match upstream change (agoldste@redhat.com)
- UPSTREAM: 28886: Add ForgetPod to SchedulerCache (agoldste@redhat.com)
- UPSTREAM: 28294: kubectl: don't display empty list when trying to get a
  single resource that isn't found (agoldste@redhat.com)
- vendor console script says what commit its vendoring in the output
  (jforrest@redhat.com)
- switch postgres template to latest (9.5) version (bparees@redhat.com)
- new-app: display warning if git not installed (cewong@redhat.com)
- Create petset last in testdata (jliggitt@redhat.com)
- Added unit tests for repository and blobdescriptorservice
  (miminar@redhat.com)
- Allow to mock default registry client (miminar@redhat.com)
- e2e: added tests for cross-repo mounting (miminar@redhat.com)
- e2e: speed-up docker repository pull tests (miminar@redhat.com)
- Configurable blobrepositorycachettl value (miminar@redhat.com)
- Cache blob <-> repository entries in registry with TTL (miminar@redhat.com)
- Fixes docker call in CONTRIBUTING documentation (rymurphy@redhat.com)
- Check for blob existence before serving (miminar@redhat.com)
- Store media type in image (miminar@redhat.com)
- UPSTREAM: docker/distribution: 1857: Provide stat descriptor for Create
  method during cross-repo mount (jliggitt@redhat.com)
- UPSTREAM: docker/distribution: 1757: Export storage.CreateOptions in top-
  level package (miminar@redhat.com)
- Preventing build from inheriting master log level (jupierce@redhat.com)
- Update README URLs based on HTTP redirects (frankensteinbot@gmail.com)
- update the output of quota example (li.guangxu@zte.com.cn)

* Fri Aug 05 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.16
- Buildrequires rsync - due to hack scripts (tdawson@redhat.com)

* Fri Aug 05 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.15
- Use hack/update-generated-docs.sh to update man pages in origin.spec
  (tdawson@redhat.com)
- Set OS_GIT_VERSION in spec file (tdawson@redhat.com)
- UPSTREAM: google/cadvisor: 1411: Ensure minimum kernel version for thin_ls
  (agoldste@redhat.com)
- Remove unsupported DNS calls from tests (ccoleman@redhat.com)
- UPSTREAM: 29655: No PetSet client (ccoleman@redhat.com)
- Show PetSets in oc status (ccoleman@redhat.com)
- DNS should support hostname annotations (ccoleman@redhat.com)
- generate: debug command (ccoleman@redhat.com)
- Debug should be able to skip init containers (ccoleman@redhat.com)
- PetSet examples (ccoleman@redhat.com)
- Enable petsets (ccoleman@redhat.com)
- Bump origin-web-console (ef9f1a1) (jforrest@redhat.com)
- Refactored the dependency between images and images-old-policy
  (skuznets@redhat.com)
- fix s2i config validation (ipalade@redhat.com)
- regen docs and completions (sjenning@redhat.com)
- follow reference values in 'oc env --list' (sjenning@redhat.com)
- Update ose_iamges.sh script to work with 3.3 (tdawson@redhat.com)
- UPSTREAM: 27392: allow watching old resources with kubectl
  (sjenning@redhat.com)
- Dockerfile builder moved to github.com/openshift/imagebuilder
  (ccoleman@redhat.com)
- bump(github.com/openshift/imagebuilder):5a8e7d9be33db899875d7c9effb8c60276188
  67a (ccoleman@redhat.com)
- Switch to depend on docker imagebuilder (ccoleman@redhat.com)
- Copy more kube artifacts (ccoleman@redhat.com)
- bump(kubernetes):507d3a7b242634b131710cfdfd55e3a1531ffb1b
  (ccoleman@redhat.com)
- add istag create (deads@redhat.com)
- Support image forcePull policy for runtime image when do extended build
  (haowang@redhat.com)
- UPSTREAM: 30021: add asserts for RecognizingDecoder and update protobuf
  serializer to implement interface (pweil@redhat.com)
- Print warning next to deployment with restarting pods (mfojtik@redhat.com)
- Fix panic caused by invalid ip range (zhao.xiangpeng@zte.com.cn)
- create app label based on template name, not buildconfig name
  (bparees@redhat.com)
- Added wait for project cache sync before test-cmd buckets start
  (skuznets@redhat.com)
- cluster up: use shared volumes in mac and windows (cewong@redhat.com)
- Avoid test flakes when creating new projects (mkhan@redhat.com)
- UPSTREAM: 29847: Race condition in scheduler predicates test
  (ccoleman@redhat.com)
- update config for unauth pull (aweiteka@redhat.com)
- Bump origin-web-console (781f34f) (jforrest@redhat.com)
- check for correct exiterr type on oc exec failures (bparees@redhat.com)
- UPSTREAM: 29182: Use library code for scheduler predicates test
  (ccoleman@redhat.com)
- Upstream packages for Go 1.4 have been dropped (ccoleman@redhat.com)
- switch to generated password for jenkins service (bparees@redhat.com)
- Always output existing credentials message when reusing credentials on login
  (jliggitt@redhat.com)
- Fix debugging pods with multiple containers (ffranz@redhat.com)
- UPSTREAM: 29952: handle container terminated but pod still running in
  conditions (ffranz@redhat.com)
- properly check for running app pod (bparees@redhat.com)
- handle forbidden server errs on older server version (jvallejo@redhat.com)
- Reorganize directories, test and Makefile (aweiteka@redhat.com)
- add link to Manageing Security Context Contraints (li.guangxu@zte.com.cn)
- Fix BZ1361024 (jtanenba@redhat.com)
- Generate man pages and bash completion during rpm build (tdawson@redhat.com)
- [RPMS] Require device-mapper-persistent-data >= 0.6.2 (sdodson@redhat.com)
- UPSTREAM: 28539: Fix httpclient setup for gcp (decarr@redhat.com)
- UPSTREAM: 28871: Do not use metadata server to know if on GCE
  (decarr@redhat.com)
- Removed namespace assumptions from test-cmd test cases (skuznets@redhat.com)
- deploy: deep-copy only when mutating in the controllers (mkargaki@redhat.com)
- deploy: remove redundant test deployment checks (mkargaki@redhat.com)
- improve checking if systemd needs to be reexec'd (sdodson@redhat.com)
- regen swagger spec (sjenning@redhat.com)
- UPSTREAM: 28263: Allow specifying secret data using strings
  (sjenning@redhat.com)
- [RPMS] Enable CPU and Memory during node installation (sdodson@redhat.com)

* Wed Aug 03 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.14
- Fix doc link (wang.yuexiao@zte.com.cn)
- Bump origin-web-console (b0dc7d5) (jforrest@redhat.com)
- Adds a flag to allow skipping config writes when creating a project
  (ffranz@redhat.com)
- add back missing integration tests (deads@redhat.com)
- clusterquota: prove image stream work with cluster quota (mfojtik@redhat.com)
- add back missing integration tests (deads@redhat.com)
- cluster up: suggest 'cluster down' message (cewong@redhat.com)
- add extended builds functionality (ipalade@redhat.com)
- Display original cmd and stderr in extended test (mfojtik@redhat.com)
- Improve bootstrap policy overwrite error handling (jliggitt@redhat.com)
- Aggregate reconcile errors (jliggitt@redhat.com)
- Make AddRole tolerate races on role additions (jliggitt@redhat.com)
- Improve role/rolebinding virtual storage (jliggitt@redhat.com)
- Fix panic in rolebinding reconcile error message (jliggitt@redhat.com)
- generated code (pweil@redhat.com)
- SCC seccomp admission (pweil@redhat.com)
- UPSTREAM: <carry>: SCC seccomp support (pweil@redhat.com)
- using a unused parameter (Yanqiang Miao)
- Add paused field in deployment config describer (mfojtik@redhat.com)
- mv oc projects tests to separate file (jvallejo@redhat.com)
- Bump origin-web-console (d68bf15) (jforrest@redhat.com)
- new-app: accept template on stdin (cewong@redhat.com)
- UPSTREAM: 29588: Properly apply quota for init containers
  (ccoleman@redhat.com)
- oc rsync: allow multiple include or exclude patterns (cewong@redhat.com)
- Change package names for upstream volume controllers in master.go
  (pmorie@gmail.com)
- UPSTREAM: 29673: Fix mount collision timeout issue (pmorie@gmail.com)
- UPSTREAM: 29641: Fix wrapped volume race (pmorie@gmail.com)
- UPSTREAM: 28939: Allow mounts to run in parallel for non-attachable volumes
  (pmorie@gmail.com)
- UPSTREAM: 28409: Reorganize volume controllers and manager (pmorie@gmail.com)
- UPSTREAM: 28153: Fixed goroutinemap race on Wait() (pmorie@gmail.com)
- UPSTREAM: 24797: add enhanced volume and mount logging for block devices
  (pmorie@gmail.com)
- UPSTREAM: 28584: Add spec.Name to the configmap GetVolumeName
  (pmorie@gmail.com)
- remove accidentally checked in openshift.local.config (bparees@redhat.com)
- UPSTREAM: 29171: Fix order of determineContainerIP args (pmorie@gmail.com)
- handle nil reference to o.Attach.Err (jvallejo@redhat.com)
- UPSTREAM: 29485: Assume volume detached if node doesn't exist
  (pmorie@gmail.com)
- UPSTREAM: 24385: golint fixes for aws cloudprovider (pmorie@gmail.com)
- UPSTREAM: 29240: Pass nodeName to VolumeManager instead of hostName
  (pmorie@gmail.com)
- UPSTREAM: 29031: Wait for PD detach on PD E2E to prevent kernel err
  (pmorie@gmail.com)
- UPSTREAM: 28404: Move ungraceful PD tests out of flaky (pmorie@gmail.com)
- UPSTREAM: 28181: Add two pd tests with default grace period
  (pmorie@gmail.com)
- UPSTREAM: 28090: Mark "RW PD, remove it, then schedule" test flaky
  (pmorie@gmail.com)
- UPSTREAM: 28048: disable flaky PD test (pmorie@gmail.com)
- UPSTREAM: 29077: Fix "PVC Volume not detached if pod deleted via namespace
  deletion" issue (pmorie@gmail.com)
- enable deployments (deads@redhat.com)
- cluster up: fix incorrect directory permissions (cewong@redhat.com)
- Handle local source as binary when git is not available (cewong@redhat.com)
- enable replicasets (deads@redhat.com)
- Move image administrative commands tests to admin.sh (maszulik@redhat.com)
- oadm top command generated changes (maszulik@redhat.com)
- Add oadm top command for analyzing image and imagestream usage
  (maszulik@redhat.com)
- remove unnecessary export (deads@redhat.com)
- Bug 1325069 - Sort status tags according to semver (maszulik@redhat.com)
- Support scheduler config options so custom schedulers can be used
  (ccoleman@redhat.com)
- Check pull access when tagging imagestreams (jliggitt@redhat.com)
- to remove singleton and to fix
  TestSimpleImageChangeBuildTriggerFromImageStreamTagSTI (salvatore-
  dario.minonne@amadeus.com)
- update the URL of git server (li.guangxu@zte.com.cn)
- Kerberos Extended Test Improvements (mkhan@redhat.com)
- update hardcoded "oc" cmd suggestion in cmd output (jvallejo@redhat.com)
- check that dest exists before attempting to extract (jvallejo@redhat.com)
- Support EgressNetworkPolicy in SDN plugin (danw@redhat.com)
- Make SDN plugin track vnid->Namespaces mapping (in addition to the reverse)
  (danw@redhat.com)
- Update generated code (danw@redhat.com)
- Add EgressNetworkPolicy (danw@redhat.com)
- Always set pod name annotation on build (cewong@redhat.com)
- SCC admission with sharedIndexInformer (salvatore-dario.minonne@amadeus.com)
- use legacy restmapper against undiscoverable servers (deads@redhat.com)
- fix bz1355721 (bmeng@redhat.com)
- `env_file` option of docker-compose support (surajssd009005@gmail.com)
- testing (bparees@redhat.com)
- Changing defaultExporter to be public (DefaultExporter) (mdame@redhat.com)
- Don't use "kexec" as both a package name and a variable name
  (danw@redhat.com)
- Use randomness for REGISTRY_HTTP_SECRET in projectatomic/atomic-registry-
  install (schmidt.simon@gmail.com)

* Mon Aug 01 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.13
- rsh: Insert a TERM variable into the command to be run
  (jonh.wendell@redhat.com)
- e2e test: remove PodCheckDns flake (lmeyer@redhat.com)
- oc secrets: rename `add` to `link` and add `unlink` (sgallagh@redhat.com)
- Return nil directly instead of err when err is nil
  (zhao.xiangpeng@zte.com.cn)
- Extended tests for kerberos (mkhan@redhat.com)
- UPSTREAM: 29134: Improve quota controller performance (decarr@redhat.com)

* Fri Jul 29 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.12
- Avoid to create an API client if not needed (ffranz@redhat.com)
- bump(github.com/openshift/source-to-image):
  724c0ddaacec2fad31a05ac2d2175cd9ad7136c6 (bparees@redhat.com)
- UPSTREAM: 29457: Quota was not counting services with multiple nodeports
  properly (agoldste@redhat.com)
- Improved Bash idioms in test/cmd/images.sh (skuznets@redhat.com)
- Improved Bash idioms in test/cmd/builds.sh (skuznets@redhat.com)
- Improved Bash idioms in test/cmd/basicresources.sh (skuznets@redhat.com)
- Ensured that all indentation in hack/lib/cmd.sh used tabs
  (skuznets@redhat.com)
- Use anonyous FIFO instead of pipe in os::cmd output test
  (skuznets@redhat.com)
- Handled working dir changes in Bash relative path util (skuznets@redhat.com)
- Colocated config validation with other diagnostics tests
  (skuznets@redhat.com)
- example: add pulling origin-pod (li.guangxu@zte.com.cn)
- Update generated files (stefan.schimanski@gmail.com)
- UPSTREAM: 28351: Add support for kubectl create quota command
  (stefan.schimanski@gmail.com)
- generated: cmd changes (ccoleman@redhat.com)
- Add a migration framework for mutable resources (ccoleman@redhat.com)
- make oc login kubeconfig permission error clearer (jvallejo@redhat.com)
- Update branding of templates to use OpenShift Platform Container
  (sgoodwin@redhat.com)
- update oc version to display client and server versions (jvallejo@redhat.com)
- Set default image version for 'oc cluster up' (cewong@redhat.com)
- make clusterquota/status endpoint (deads@redhat.com)
- update PSP review APIS (deads@redhat.com)
- handle authorization evaluation error for SAR (deads@redhat.com)
- BuildSource: mark secrets field as omitempty. (vsemushi@redhat.com)
- Moved completions tests from hack/test-cmd.sh into test/cmd/completions.sh
  (skuznets@redhat.com)
- Removed spam from hack/test-cmd.sh output on test success
  (skuznets@redhat.com)
- update the output of Deploying a private docker registry
  (li.guangxu@zte.com.cn)
- document NetworkPolicy status (danw@redhat.com)
- UPSTREAM: 29291: Cherry-picked (jimmidyson@gmail.com)
- Description of (run the unit tests) is incorrect in README.md
  (li.guangxu@zte.com.cn)
- dockerbuild pull on Docker 1.9 is broken (ccoleman@redhat.com)
- Add Dockerfiles.centos7 and job-id files for CentOS image building
  (tdawson@redhat.com)
- Add V(5) logging back to pkg/util/ovs and pkg/util/ipcmd (danw@redhat.com)
- update FAQ in README.md (li.guangxu@zte.com.cn)
- dind: enable overlay storage (marun@redhat.com)
- dind: remove wrapper script (marun@redhat.com)
- Make /var/lib/origin mounted rslave for containerized systemd units
  (sdodson@redhat.com)

* Wed Jul 27 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.11
- README.md: Updates to "What can I run on Origin?" section (jawnsy@redhat.com)
- Return instead of exit on argument mismatch in os::cmd (skuznets@redhat.com)
- Allows filtering templates by namespace in new-app (ffranz@redhat.com)
- tolerate yaml payloads for generic webhooks (bparees@redhat.com)
- Use client interface for DCReaper (matthieu.dalstein@amadeus.com)
- Clarify major Origin features (jawnsy@redhat.com)
- bump(github.com/openshift/source-to-image):
  3632461ab64707aad489203b99889650cdf02647 (jupierce@redhat.com)
- Update Origin admission controllers to handle init containers
  (ccoleman@redhat.com)
- UPSTREAM: 29356: Container limits are not applied to InitContainers
  (ccoleman@redhat.com)
- UPSTREAM: 29356: InitContainers are not checked for hostPort ranges
  (ccoleman@redhat.com)
- InitContainer admission (ccoleman@redhat.com)
- update docs (jvallejo@redhat.com)
- make cli command root dynamic in cmd output (jvallejo@redhat.com)
- Ensure build pod name annotation is set (cewong@redhat.com)
- Secrets: work around race in `oc extract` test (sgallagh@redhat.com)
- Fix test registry client with images of different versions
  (agladkov@redhat.com)
- Parse v2 schema manifest (agladkov@redhat.com)
- add master-config validation that complains about using troublesome admission
  chains (deads@redhat.com)
- Use image.DockerImageLayers for pruning (maszulik@redhat.com)
- implement basic DDOS protections in the HAProxy template router
  (jtanenba@redhat.com)
- generated: For proto and authorization changes (ccoleman@redhat.com)
- Enable protobuf for new configurations, json for old (ccoleman@redhat.com)
- bump(github.com/openshift/source-to-image):
  49dac82c5f1521e95980c71ff0e092b991fc1b09 (bparees@redhat.com)
- Make authorization conversions efficient (ccoleman@redhat.com)
- Rename AuthorizationAttributes -> Action (ccoleman@redhat.com)
- Fix issues running protobuf from clients (ccoleman@redhat.com)
- Verify protobuf during runs (ccoleman@redhat.com)
- Templates should use NestedObject* with Unstructured scheme
  (ccoleman@redhat.com)
- UPSTREAM: 28931: genconversion=false should skip fields during conversion
  generation (ccoleman@redhat.com)
- UPSTREAM: 28934: Unable to have optional message slice (ccoleman@redhat.com)
- UPSTREAM: <drop>: Drop LegacyCodec in unversioned client
  (ccoleman@redhat.com)
- UPSTREAM: 28932: Fail correctly in go-to-protobuf (ccoleman@redhat.com)
- UPSTREAM: 28933: Handle server errors more precisely (ccoleman@redhat.com)
- extended: set failure traps in all deployment tests (mkargaki@redhat.com)
- Adding template instructional message to new-app output (jupierce@redhat.com)
- Override port forwarding if using docker machine (cewong@redhat.com)
- Bump origin-web-console (50d02f7) (jforrest@redhat.com)
- support -f flag for --follow in start-build (bparees@redhat.com)
- Enforce --tty=false flag for 'oc debug' (mdame@localhost.localdomain)

* Mon Jul 25 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.10
- Skip the '-' character in scratch builds for Docker 1.9.1
  (ccoleman@redhat.com)
- Added REST storage for imagesignatures resource (miminar@redhat.com)
- List enabled/disabled features in readme. (ccoleman@redhat.com)
- Match upstream exec API refactoring (agoldste@redhat.com)
- UPSTREAM: 29237: Fix Windows terminal handling (agoldste@redhat.com)
- Example description incorrect (li.guangxu@zte.com.cn)
- add oc annotate --single-resource flag tests (jvallejo@redhat.com)
- UPSTREAM: 29319: update rsrc amnt check to allow use of --resource-version
  flag with single rsrc (jvallejo@redhat.com)
- deploy: validate minReadySeconds against default deployment timeout
  (mkargaki@redhat.com)
- make node auth use tokenreview API (deads@redhat.com)
- UPSTREAM: 28788: add tokenreviews endpoint to implement webhook
  (deads@redhat.com)
- UPSTREAM: 28852: authorize based on user.Info (deads@redhat.com)
- deploy: stop defaulting to ImageStreamTag unconditionally
  (mkargaki@redhat.com)
- deploy: enqueue configs on pod events (mkargaki@redhat.com)
- validate imagestreamtag names in build definitions (bparees@redhat.com)
- dump etcd on test integration failures (deads@redhat.com)
- oc: enable following deployment logs in deploy (mkargaki@redhat.com)
- deploy: update the log registry to poll on notfound deployments
  (mkargaki@redhat.com)
- UPSTREAM: 28964: Reexport term.IsTerminal (agoldste@redhat.com)
- UPSTREAM: <carry>: support pointing oc portforward to old openshift server
  (agoldste@redhat.com)
- UPSTREAM: <carry>: support pointing oc exec to old openshift server
  (agoldste@redhat.com)
- UPSTREAM: 25273: Support terminal resizing for exec/attach/run
  (agoldste@redhat.com)
- UPSTREAM: <carry>: REVERT support pointing oc exec to old openshift server
  (agoldste@redhat.com)
- Implement an `oc extract` command to make it easy to use secrets
  (ccoleman@redhat.com)

* Fri Jul 22 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.9
- Clean up Origin and OSE differences (tdawson@redhat.com)
- Abort deployment when the from version is higher than to version
  (mfojtik@redhat.com)
- run all parallel builds when a serial build finishes (bparees@redhat.com)
- Image progress: recognize additional already pushed status
  (cewong@redhat.com)
- Accept OS_BUILD_IMAGE_ARGS in our image build scripts (ccoleman@redhat.com)
- clean up jenkins master/slave example (bparees@redhat.com)
- add mariadb template and use specific imagestream tag versions, not latest
  (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  9350cd1ef8afc9c91dcdc96e1d972cbcc6f36181 (vsemushi@redhat.com)
- Add an experimental --mount flag to oc ex dockerbuild (ccoleman@redhat.com)
- Inherit all our images from our base (ccoleman@redhat.com)
- add default resource requests to registry creation (agladkov@redhat.com)
- Pause the deployment config before deleting (mfojtik@redhat.com)
- Debug should not have 15s timeout (ccoleman@redhat.com)
- Start rsync daemon in the foreground to prevent zombie processes
  (cewong@redhat.com)
- Bump origin-web-console (bad6254) (jforrest@redhat.com)
- Enabling multiline parameter injection for templates (jupierce@redhat.com)
- allow for configurable server side timeouts on routes (jtanenba@redhat.com)
- UPSTREAM: 29133: use a separate queue for initial quota calculation
  (deads@redhat.com)
- Cherry-pick scripts create a .make directory that we should ignore
  (decarr@redhat.com)
- Fix ClusterResourceOverride test that has been broken for a while
  (ccoleman@redhat.com)
- Bump size of file allowed to be uploaded (ccoleman@redhat.com)
- Test must set RequireEtcd (ccoleman@redhat.com)
- Strip build tags from integration, they are not needed (ccoleman@redhat.com)
- update generated docs (jvallejo@redhat.com)
- UPSTREAM: 0000: update timeout flag help to contain correct duration format
  (jvallejo@redhat.com)
- Avoid allocations while checking role bindings (ccoleman@redhat.com)
- Fixed a bug in jUnit output from os::cmd::try_until_text
  (skuznets@redhat.com)
- use pod name instead of id in oc delete example (jvallejo@redhat.com)
- deploy: add source for hook events (mkargaki@redhat.com)
- Added checks in build path for docker-compose import
  (surajssd009005@gmail.com)

* Wed Jul 20 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.8
- Add support for anonymous registry requests (jliggitt@redhat.com)
- Allow anonymous users to check their access (jliggitt@redhat.com)
- gather dump before you kill the process (deads@redhat.com)
- Bug 1357668: update error message on invalid tags in ICTs
  (mkargaki@redhat.com)
- Add goimports to the release image (ccoleman@redhat.com)
- generate: Protobuf types and updates (ccoleman@redhat.com)
- Handle content type correctly in extensions (ccoleman@redhat.com)
- Generator for protobuf (ccoleman@redhat.com)
- Give build fields proto safe names (ccoleman@redhat.com)
- UPSTREAM: 28935: don't double encode runtime.Unknown (ccoleman@redhat.com)
- UPSTREAM: 26044: Additional fixes to protobuf versioning
  (ccoleman@redhat.com)
- UPSTREAM: 28810: Honor protobuf name tag (ccoleman@redhat.com)
- bump(k8s.io/kubernetes/third_party/protobuf):v1.3.0 (ccoleman@redhat.com)
- Enable protoc in the release images (ccoleman@redhat.com)
- Bump origin-web-console (15dc649) (jforrest@redhat.com)
- Copy GSSAPI errors to prevent use-after-free bugs (mkhan@redhat.com)
- oc new-app: add missing single quote. (vsemushi@redhat.com)
- UPSTREAM: 27263: Cherry-picked (stefan.schimanski@gmail.com)
- Remove deployment trigger warning (jhadvig@redhat.com)
- deploy: add minReadySeconds for deploymentconfigs (mkargaki@redhat.com)
- deploy: generated code for minReadySeconds (mkargaki@redhat.com)
- UPSTREAM: 28111: Add MinReadySeconds to rolling updater (mkargaki@redhat.com)
- UPSTREAM: 28966: Describe container volume mounts (mfojtik@redhat.com)
- oc: add --insecure-policy for creating edge routes (mkargaki@redhat.com)
- Bug 1356530: handle 403 in oc rollback (mkargaki@redhat.com)
- Allow Docker for Mac beta to work by using port forwarding
  (cewong@redhat.com)
- expose evaluation errors for RAR (deads@redhat.com)
- allow git_ssl_no_verify env variable in build pods (bparees@redhat.com)
- deploy: move cli-related packages in cmd (mkargaki@redhat.com)

* Mon Jul 18 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.7
- deploy: update revisionHistoryLimit to int32 (mkargaki@redhat.com)
- Added a check for empty template in DeployConfig (rymurphy@redhat.com)
- restore resyncing ability for fifo based controllers (deads@redhat.com)
- UPSTREAM: <carry>: fix fifo resync, remove after FIFO is dead
  (deads@redhat.com)
- Dump deployment logs in case of test failure (nagy.martin@gmail.com)
- Test gssapi library load when selecting available challenge handlers
  (jliggitt@redhat.com)

* Fri Jul 15 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.6
- Cleanup OSE directories no longer in origin, or used (tdawson@redhat.com)
- Add jobs to conformance run (maszulik@redhat.com)
- deploy: set gracePeriod on deployer creation rather than on deletion
  (mkargaki@redhat.com)
- UPSTREAM: 28966: Fix watch cache filtering (jliggitt@redhat.com)
- Fully specify DeleteHostSubnet() rules (danw@redhat.com)
- Ensure the test deployment invariant is maintained (ccoleman@redhat.com)
- Bump origin-web-console (38099da) (jforrest@redhat.com)
- Added debugging information to os::cmd output content test
  (skuznets@redhat.com)
- Fix SA OAuth test flake (jliggitt@redhat.com)
- Load versioned gssapi libs (jliggitt@redhat.com)
- Re-enable new-app integration tests (cewong@redhat.com)
- treat notfound and badrequest instantiate errors as fatal
  (bparees@redhat.com)
- docs: remove openshift_model.md (lmeyer@redhat.com)
- add nodejs 4 imagestream and bump templates to use latest imagestreams
  (bparees@redhat.com)
- Update CONTRIBUTING.adoc (jminter@redhat.com)
- Enable PersistentVolumeLabel admission plugin (agoldste@redhat.com)
- add etcd dump for integration test (deads@redhat.com)
- UPSTREAM: 28626: update resource builder error message to be more clear
  (jvallejo@redhat.com)
- display resource type as part of its name (jvallejo@redhat.com)
- UPSTREAM: 28509: Update HumanResourcePrinter signature w single PrintOptions
  param (jvallejo@redhat.com)
- extended: update deployment test timeout (mkargaki@redhat.com)
- deploy: set gracePeriodSeconds on deployer deletion (mkargaki@redhat.com)
- integration: add multiple ict deployment test (mkargaki@redhat.com)
- Added a clean-up policy for deployments (skuznets@redhat.com)
- add project annotation selectors to cluster quota (deads@redhat.com)
- Refactor stable layer count unit test (cewong@redhat.com)
- Add test for image import and conversion v2 schema to v1 schema
  (agladkov@redhat.com)
- UPSTREAM: 27379: display resouce type as part of resource name
  (jvallejo@redhat.com)
- Added tests for pod-network CLI command (rpenta@redhat.com)
- Some reorg/cleanup for enabling pod-network cli tests (rpenta@redhat.com)
- use maven image for slave pods in sample pipeline (bparees@redhat.com)
- Revert "Allow size of image to be zero when schema1 from Hub"
  (legion@altlinux.org)
- Fix image size calculation in importer (agladkov@redhat.com)

* Wed Jul 13 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.5
- Add an admission controller to block illegal service endpoints
  (danw@redhat.com)
- Limit the amount of output of a faulty new-build (rymurphy@redhat.com)
- Parameter validation for new-app strategy (jupierce@redhat.com)
- Add option to handle OAuth grants at a per-client granularity
  (sgallagh@redhat.com)
- Add mirror env var options and fix required parameters to templates
  (vdinh@redhat.com)
- Add a service account for the endpoints controller (danw@redhat.com)
- Remove unused code (li.guangxu@zte.com.cn)
- no need to build networking pkg in build-tests session
  (li.guangxu@zte.com.cn)
- SDN types should used fixed width integers (ccoleman@redhat.com)
- reject build requests for binary builds if not providing binary inputs
  (bparees@redhat.com)
- dind: update to f24 (and go 1.6) (marun@redhat.com)
- Bump origin-web-console (563e73a) (jforrest@redhat.com)
- return notfound errors w/o wrappering them (bparees@redhat.com)
- No info about deployer pods logged (ccoleman@redhat.com)
- Update godep-restore (ccoleman@redhat.com)
- Adding a field to templates to allow them to deliver a user message with
  parameters substituted (jupierce@redhat.com)
- UPSTREAM: 28500: don't migrate files you can't access (deads@redhat.com)
- Update comment (rhcarvalho@gmail.com)
- Refactored test/cmd/authentication.sh to use proper strings and literals
  (skuznets@redhat.com)

* Mon Jul 11 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.4
- OSE Fix: Revert OS_GIT_VERSION regex back (tdawson@redhat.com)
- Fix a DNS flake by watching for pod succeeded (ccoleman@redhat.com)
- Avoid mutating the cached deployment config in image change controller
  (ccoleman@redhat.com)
- combine quota registries (deads@redhat.com)
- UPSTREAM: 28611: add union registry for quota (deads@redhat.com)
- UPSTREAM: <carry>: make namespace lifecycle access review aware
  (deads@redhat.com)
- collapse admission chains (deads@redhat.com)
- lock clusterquota admission to avoid conflicts (deads@redhat.com)
- add clusterquota admission (deads@redhat.com)
- UPSTREAM: 28504: shared informer cleanup (deads@redhat.com)
- Remove all checkErr() flags and retry conflict on BuildController
  (ccoleman@redhat.com)
- test-local-registry.sh works on *nix as well (miminar@redhat.com)
- deploy: pin retries to a const and forget correctly in the dc loop
  (mkargaki@redhat.com)
- deploy: remove deployer pod controller (mkargaki@redhat.com)
- deploy: collapse deployer into deployments controller (mkargaki@redhat.com)
- Add gssapi build flags (jliggitt@redhat.com)
- Limit gssapi auth to specified principal (jliggitt@redhat.com)
- Add gssapi negotiate support (jliggitt@redhat.com)
- bump(github.com/apcera/gssapi): b28cfdd5220f7ebe15d8372ac81a7f41cc35ab32
  (jliggitt@redhat.com)
- Use recycler service account for the recycler pod (ccoleman@redhat.com)
- modify example in Makefile (li.guangxu@zte.com.cn)
- Failing to update deployment config should requeue on image change
  (ccoleman@redhat.com)
- Print more info in router tests (ccoleman@redhat.com)
- generated: API, completions, man pages, conversion, copy
  (ccoleman@redhat.com)
- Deployment test does not round trip (ccoleman@redhat.com)
- Disable extended tests that won't work on OpenShift (ccoleman@redhat.com)
- Update master startup and admission to reflect changes in upstream
  (ccoleman@redhat.com)
- Alter generation to properly reuse upstream types (ccoleman@redhat.com)
- Make conversion and encoding handle nested runtime.Objects
  (ccoleman@redhat.com)
- Refactors from upstream Kube changes (ccoleman@redhat.com)
- Revert "react to 27341: this does not fix races in our code"
  (ccoleman@redhat.com)
- UPSTREAM: docker/distribution: <carry>: Distribution dependencies
  (ccoleman@redhat.com)
- bump(k8s.io/kubernetes):v1.3.0+ (ccoleman@redhat.com)
- bump(*): rename Godeps/_workspace/src -> vendor/ (ccoleman@redhat.com)
- Track upstream versions more precisely (ccoleman@redhat.com)
- Use vendor instead of Godeps/_workspace in builds (ccoleman@redhat.com)
- Update commit checker to handle vendor (ccoleman@redhat.com)
- Remove v1beta3 (ccoleman@redhat.com)
- bump registry xfs quota; re-enable disk usage diag; add docker info
  (gmontero@redhat.com)
- make sure the db has an endpoint before testing the app (bparees@redhat.com)
- Adding dumplogs pattern to extended build tests (jupierce@redhat.com)
- allow cni as one of the plugins (rchopra@redhat.com)
- fix bz1353489 (rchopra@redhat.com)
- Fix incorrect master leases ttl setting (agoldste@redhat.com)
- Fix race in imageprogress test (cewong@redhat.com)

* Fri Jul 08 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.3
- Bump origin-web-console (e29729b) (jforrest@redhat.com)
- Ensure binary is built before completions are updated (jvallejo@redhat.com)
- Added tagged pull e2e tests (maszulik@redhat.com)
- Ensure client can delete a buildconfig with no associated builds, even if
  user lacks build strategy permission (jupierce@redhat.com)
- Fixes oc convert examples (ffranz@redhat.com)
- Remove v1beta3 from end-to-end tests (maszulik@redhat.com)
- cache: return api errors on not found imagestreams/deploymentconfigs
  (mkargaki@redhat.com)
- add clusterquota reconciliation controller (deads@redhat.com)
- Bump origin-web-console (ccd995f) (jforrest@redhat.com)
- Remove global flags from 'openshift start kubernetes *' (ffranz@redhat.com)
- allow roundrobin algorithm as a choice in passthrough/reencrypt
  (rchopra@redhat.com)
- Fixes oc convert examples (ffranz@redhat.com)
- Add krb5-devel to build environments (jliggitt@redhat.com)
-  Backporting dist-git Dockerfile to Dockerfile.product (tdawson@redhat.com)
- Issue 9702 - consider schema v2 layers when pruning (maszulik@redhat.com)
- UPSTREAM: 28353: refactor quota calculation for re-use (deads@redhat.com)
- extended: refactor deployment test to be more debuggable
  (mkargaki@redhat.com)
- track updated manpages (jvallejo@redhat.com)
- update manpage list parsing (jvallejo@redhat.com)
- Cleaned up test/end-to-end/core script (skuznets@redhat.com)
- Add debug logging to ldap search bind errors (jliggitt@redhat.com)
- align s2i and docker push image error messages (bparees@redhat.com)
- Removed environment variable substitution step from stacktrace
  (skuznets@redhat.com)
- Make former openshift-sdn code pass govet (danw@redhat.com)
- Update for import/reorg of openshift-sdn code (danw@redhat.com)
- Drop imported openshift-sdn code (danw@redhat.com)
- handle multiple names for docker registry (deads@redhat.com)
- UPSTREAM: 28379: allow handler to join after the informer has started
  (deads@redhat.com)
- Generated changes for oadm prune images --prune-over-size-limit
  (maszulik@redhat.com)
- Add --prune-over-size-limit flag for pruning images (maszulik@redhat.com)
- Move files to the right places for the origin tree (danw@redhat.com)
- Drop pkg/exec, port pkg/ipcmd and pkg/ovs to kexec (danw@redhat.com)
- Refactor pruning images to follow one common flow with other pruners
  (maszulik@redhat.com)
- Refactor pruning deployment to follow one common flow with other pruners
  (maszulik@redhat.com)
- Refactor pruning builds to follow one common flow with other pruners
  (maszulik@redhat.com)
- haproxy-router delete service endpoint problem (pcameron@redhat.com)
- Remove build files, Godeps, docs, etc (danw@redhat.com)
- Oops, branch got broken by a last-minute change (danw@redhat.com)
- Unexport names that don't need to be exported. (danw@redhat.com)
- Reorganize and split out node API (danw@redhat.com)
- Simplify and split out master API (danw@redhat.com)
- Split OsdnController into OsdnMaster and OsdnNode (danw@redhat.com)
- Add vnidMap type (danw@redhat.com)
- Merge ovsPlugin into OsdnController (danw@redhat.com)
- Merge plugins/osdn/factory into plugins/odsn (danw@redhat.com)
- Merge plugins/osdn/ovs into plugins/osdn (danw@redhat.com)
- Updated `os::cmd' internals to reflect new script location
  (skuznets@redhat.com)
- Migrated `os::text' utilities into `hack/lib/util' (skuznets@redhat.com)
- Migrated `os::cmd' utilities into `hack/lib' (skuznets@redhat.com)
- Adjust types for rebase, add stub Status method (jliggitt@redhat.com)
- we are already production ready (akostadi@redhat.com)
- Use osapi.ClusterNetworkDefault instead of hard coding to 'default'
  (rpenta@redhat.com)
- Added IsOpenShiftNetworkPlugin and IsOpenShiftMultitenantNetworkPlugin
  methods (rpenta@redhat.com)
- Log created/updated ClusterNetwork resource (rpenta@redhat.com)
- Persist network plugin name as part of cluster network creation
  (rpenta@redhat.com)
- Simplify caching and fetching network information (rpenta@redhat.com)
- debug.sh: Fix fetching config file for service (rpenta@redhat.com)
- Force a rebuild after ./hack/sync-to-origin.sh (danw@redhat.com)
- Fix naming typo in sync-to-origin.sh (danw@redhat.com)
- debug: log master config and master api/controllers journal and service
  (dcbw@redhat.com)
- Enable SDN StartNode() to call node iptables setup (rpenta@redhat.com)
- Periodically sync openshift node iptables rules (rpenta@redhat.com)
- Fail more cleanly on script errors (danw@redhat.com)
- Add logging for SDN watch events (rpenta@redhat.com)
- Update subnet when host IP changes instead of delete-old + create-new subnet.
  (rpenta@redhat.com)
- Remove prompts from commented examples (rhcarvalho@gmail.com)
- Add tc state to the debug tar (bbennett@redhat.com)
- Split plugin creation into NewMasterPlugin and NewNodePlugin
  (dcbw@redhat.com)
- Split proxy endpoint filtering out into separate object (dcbw@redhat.com)
- Ignore malformed IP in Node object (danw@redhat.com)
- SDN watch will try to fix transient errors (rpenta@redhat.com)
- Return errors from plugin hooks (rpenta@redhat.com)
- Run Watch resources forever! (rpenta@redhat.com)
- Simplify Watch resource in SDN (rpenta@redhat.com)
- Refer resource names by constants (rpenta@redhat.com)
- Refer SDN plugin names and annotations by constants (rpenta@redhat.com)
- Update for origin kubernetes rebase (dcbw@redhat.com)
- Add more HostSubnet logging (dcbw@redhat.com)
- Synchronize access to vnid map (rpenta@redhat.com)
- Controlled access to vnid map (rpenta@redhat.com)
- Delete NetID from VNID map before deleting NetNamespace object
  (rpenta@redhat.com)
- Fix updating VNID map (rpenta@redhat.com)
- debug.sh: don't do DNS check if node "name" is an IP address
  (danw@redhat.com)
- debug.sh: fix incoming remote test packet traces (danw@redhat.com)
- debug.sh: comment fix (danw@redhat.com)
- debug.sh: check for systemd unit files in /etc too (danw@redhat.com)
- Return better errors from SetUpPod/TearDownPod (danw@redhat.com)
- Fix AddHostSubnetRules() and DeleteHostSubnetRules() (rpenta@redhat.com)
- Removed the cookies from the remote node rules. (bbennett@redhat.com)
- Add a mutex to registry.podsByIP (danw@redhat.com)
- Prepopulate pod info map so that proxy can filter endpoints
  (rpenta@redhat.com)
- Remove unused GetServicesNetwork() and GetHostSubnetLength()
  (rpenta@redhat.com)
- Existing items in the event queue will be reported as Modified event, so
  handle approriately during watching resources(services,namespaces,etc.)
  (rpenta@redhat.com)
- OsdnController.services is only needed in watch services, make it local
  (rpenta@redhat.com)
- Minor cleanup in watchServices() (rpenta@redhat.com)
- Prepopulate VNIDMap for VnidStartMaster/VnidStartNode methods
  (rpenta@redhat.com)
- Do not need to pre-populate nodeAddressMap in WatchNodes (rpenta@redhat.com)
- Don't return resource version for methods GetSubnets, GetNetNamespaces and
  GetServices. No longer needed. (rpenta@redhat.com)
- Remove unused stop channels in sdn (rpenta@redhat.com)
- Remove Get and Watch resource behavior in sdn (rpenta@redhat.com)
- Don't resync/repopulate the event queue for sdn events (rpenta@redhat.com)
- Use NewListWatchFromClient() instead of ListFunc/WatchFunc
  (rpenta@redhat.com)
- Add more logging, to help debug problems (danw@redhat.com)
- Fixes the ip address to namespace cache when pods reuse addresses
  (bbennett@redhat.com)
- Changed the debug script to capture the arp cache (bbennett@redhat.com)
- Added 'docker ps -a' to the node debug items (bbennett@redhat.com)
- Do not throw spurious error msgs in watch network namespaces
  (rpenta@redhat.com)
- Fix watch services for multitenant plugin (rpenta@redhat.com)
- Fix broken VnidStartMaster() (rpenta@redhat.com)
- Fix watch services for multitenant plugin (rpenta@redhat.com)
- Implement "pod.network.openshift.io/assign-macvlan" annotation
  (danw@redhat.com)
- Fix network pod teardown (rpenta@redhat.com)
- Added endpoints to the list of things we add to the debug tar.
  (bbennett@redhat.com)
- Make plugin event-handling methods take objects rather than multiple args
  (danw@redhat.com)
- Move remaining internal-only types from osdn/api to osdn (danw@redhat.com)
- Drop kubernetes/OpenShift wrapper types (danw@redhat.com)
- Merge FlowController into PluginHooks (danw@redhat.com)
- Rename OvsController to OsdnController (danw@redhat.com)
- Fix qos check in del_ovs_flows() (rpenta@redhat.com)
- Improved the debug script to grab the docker unit file. (bbennett@redhat.com)
- Remove unused MTU stuff from bandwidth code (danw@redhat.com)
- Implement better OVS flow rule versioning (dcbw@redhat.com)
- Enforce ingress/egress bandwidth limits (dcbw@redhat.com)
- Validate cluster/service network only when there is a config change
  (rpenta@redhat.com)
- Add pod annotations to osdn Pod API object (dcbw@redhat.com)
- Ensure NodeIP doesn't overlap with the cluster network (dcbw@redhat.com)
- Simplify passing ClusterNetwork through master start functions
  (dcbw@redhat.com)
- Consolidate cluster network validation (dcbw@redhat.com)
- Cache ClusterNetwork details in the Registry (dcbw@redhat.com)
- Fixes to danwinship/arp-fixes (danw@redhat.com)
- Add explicit "actions=drop" OVS rules (danw@redhat.com)
- Add some more OVS anti-spoofing checks (danw@redhat.com)
- Redo OVS rules to avoid ARP caching problems (danw@redhat.com)
- Re-fix reconnect-pods-on-restart code (danw@redhat.com)
- Sync more rebase-related changes back from origin (danw@redhat.com)
- Set the right MTU on tun0 too (dcbw@redhat.com)
- debug.sh: fix typo that messed up our journal output (danw@redhat.com)
- debug.sh: make this work even if renamed (danw@redhat.com)
- Only UpdatePod on startup if the network actually changed (danw@redhat.com)
- Call UpdatePod on all running pods at startup (danw@redhat.com)
- Make "openshift-sdn-ovs update" fix up network connectivity (danw@redhat.com)
- openshift-sdn-ovs: reorganize, deduplicate (danw@redhat.com)
- openshift-sdn-ovs: remove unused Init and Status methods (danw@redhat.com)
- Set MTU on vovsbr/vlinuxbr (danw@redhat.com)
- Resync from origin for kubernetes rebase (danw@redhat.com)
- If NodeIP and NodeName are unsuitable, fallback to default interface IP
  address (dcbw@redhat.com)
- Update to new ListOptions client APIs - missing piece of puzzle
  (maszulik@redhat.com)
- Update to new ListOptions client APIs (jliggitt@redhat.com)
- Minor update to previous commit; use log.Fatalf() (danw@redhat.com)
- Put the network-already-set-up check in the right place (danw@redhat.com)
- Don't set registry.clusterNetwork/.serviceNetwork until needed
  (danw@redhat.com)
- Revert "Fail early on a node if we can't fetch the ClusterNetwork record"
  (danw@redhat.com)
- Fix alreadySetUp() check by using correct address string (dcbw@redhat.com)
- Add setup debug log output (dcbw@redhat.com)
- Fail early on a node if we can't fetch the ClusterNetwork record
  (danw@redhat.com)
- Revert "Don't crash on endpoints with invalid/empty IP addresses"
  (danw@redhat.com)
- Don't crash on endpoints with invalid/empty IP addresses (danw@redhat.com)
- debug.sh: add "sysctl -a" output (danw@redhat.com)
- debug.sh: don't try to run "oc" on the nodes (danw@redhat.com)
- debug.sh: fix up master-as-node case (danw@redhat.com)
- debug.sh: bail out correctly if "run_self_via_ssh --master" fails
  (danw@redhat.com)
- debug.sh: remove some unused code (danw@redhat.com)
- debug.sh: belatedly update for merged OVS rules (danw@redhat.com)
- debug.sh: belatedly update environment filtering for json->yaml change
  (danw@redhat.com)
- fix connectivity from docker containers (me@ibotty.net)
- Add a missing 'ovs-ofctl del-flows' on pod teardown (danw@redhat.com)
- Add a route to fix up service IP usage from the node. (danw@redhat.com)
- Fix a bug with services in multitenant (danw@redhat.com)
- Make pkg/ipcmd and pkg/ovs not panic if their binaries are missing
  (danw@redhat.com)
- Tweak SubnetAllocator behavior when hostBits%%8 != 0 (danw@redhat.com)
- Add some caching to SubnetAllocator (danw@redhat.com)
- Extend TestAllocateReleaseSubnet() to test subnet exhaustion
  (danw@redhat.com)
- Improve subnet_allocator_test debugging (danw@redhat.com)
- trivial: rename SubnetAllocator.capacity to .hostBits (danw@redhat.com)
- Minor: move 'ovsPluginName' to project_options.go, used by join-projects
  /isolate-projects/make-projects-global        rename adminVNID to globalVNID
  (rpenta@redhat.com)
- Admin commands should not depend on OVS code (ccoleman@redhat.com)
- Update kube and multitenant to use pkg/ovs and pkg/ipcmp (danw@redhat.com)
- Move config.env handling to go and rename the file (danw@redhat.com)
- Port setup_required check to go (danw@redhat.com)
- Move docker network configuration into its own setup script (danw@redhat.com)
- Move setup sysctl calls to controller.go (danw@redhat.com)
- Remove locking from openshift-sdn-ovs-setup.sh (danw@redhat.com)
- Add pkg/ipcmd, a wrapper for /sbin/ip (danw@redhat.com)
- Add pkg/ovs, a wrapper for ovs-ofctl and ovs-vsctl (danw@redhat.com)
- Bump node subnet wait to 30 seconds (from 10) (dcbw@redhat.com)
- Add an os.exec wrapper that can be used for test programs (danw@redhat.com)
- Don't redundantly validate the ClusterNetwork (danw@redhat.com)
- Move FilteringEndpointsConfigHandler into openshift-sdn (dcbw@redhat.com)
- Remove unused openshift-sdn-ovs script parameters (dcbw@redhat.com)
- Consolidate pod setup/teardown and update operations (dcbw@redhat.com)
- Log message when pod is waiting for sdn initialization (rpenta@redhat.com)
- Move pod network readiness check to pod setup instead of network plugin init
  (rpenta@redhat.com)
- Filter VXLAN packets from outside the cluster (danw@redhat.com)
- trivial: renumber ovs tables (danw@redhat.com)
- Use the multitenant OVS flows even for the single tenant case
  (danw@redhat.com)
- Properly prioritize all multitenant openflow rules (danw@redhat.com)
- Fix sdn GetHostIPNetworks() and GetNodeIP() (rpenta@redhat.com)
- Make kubelet to block on network plugin initialization until OpenShift is
  done with it's SDN setup. (rpenta@redhat.com)
- Recognize go v1.5 in hack/verify-gofmt.sh (dcbw@redhat.com)
- Merge flatsdn and multitenant plugins (danw@redhat.com)
- Make openshift-ovs-subnet and openshift-ovs-multitenant identical
  (danw@redhat.com)
- Make openshift-sdn-kube-subnet-setup.sh and openshift-sdn-multitenant-
  setup.sh identical (danw@redhat.com)
- Move kube controller base OVS flow setup into setup.sh (danw@redhat.com)
- osdn: Fix out of range panic (mkargaki@redhat.com)
- Trivial build fix (dcbw@redhat.com)
- Don't return an error if the plugin is unknown (dcbw@redhat.com)
- Remove unused/stale files from sdn repo (rpenta@redhat.com)
- Allowing running single tests via "WHAT=pkg/foo ./hack/test.sh"
  (danw@redhat.com)
- Shuffle things around in node start to fix a hang (danw@redhat.com)
- Simplify Origin/openshift-sdn interfaces (dcbw@redhat.com)
- Export oc.Registry for plugins (dcbw@redhat.com)
- Consolidate plugins/osdn and pkg/ovssubnet (dcbw@redhat.com)
- Split subnet-specific startup into separate file (dcbw@redhat.com)
- Split multitenant-specific startup into separate file (dcbw@redhat.com)
- Genericize watchAndGetResource() (dcbw@redhat.com)
- Consolidate hostname lookup (dcbw@redhat.com)
- Trivial multitenant cleanups (dcbw@redhat.com)
- Drop the SubnetRegistry type (danw@redhat.com)
- Move GetNodeIP() to netutils (danw@redhat.com)
- Rename osdn.go to registry.go, OsdnRegistryInterface to Registry
  (danw@redhat.com)
- Remove unused lookup of VNID for TearDownPod (dcbw@redhat.com)
- Fixed comment typo (bbennett@redhat.com)
- Updated with the review comments:  - Fixed stupid errors  - Moved the ssh
  options into the ssh function  - Changed the nsenter commands to make them
  use -- before the subsidiary command  - Changed the output format to yaml
  (bbennett@redhat.com)
- Copy in kubernetes/pkg/util/errors for netutils tests (danw@redhat.com)
- Detect host network conflict with sdn cluster/service network
  (rpenta@redhat.com)
- Made a few small changes:  - Got the 'oc routes' output  - Supressed the host
  check in ssh  - Unified common code between host and node  - Cleaned up the
  formatting to make the commands being run a little more obvious
  (bbennett@redhat.com)
- Tolerate missing routes for lbr0 too (sdodson@redhat.com)
- Isolate restarting docker (sdodson@redhat.com)
- Fix for go-fmt (danw@redhat.com)
- Don't loop forever if subnet not found for the node (rpenta@redhat.com)
- Track Service modifications and update OVS rules (danw@redhat.com)
- Change representation of multi-port services (danw@redhat.com)
- Fix a few log.Error()s that should have been log.Errorf() (danw@redhat.com)
- debug.sh: skip ready=false pods, which won't have podIP set (danw@redhat.com)
- debug.sh: protect a bit against unexpected command output (danw@redhat.com)
- debug.sh: fix a hack (danw@redhat.com)
- Rename pod-network subcommand unisolate-projects to make-projects-global
  (rpenta@redhat.com)
- Allow traffic from VNID 0 pods to all services (danw@redhat.com)
- Tolerate error for tun0 redundant route but not for lbr0 route
  (rpenta@redhat.com)
- Remove support for supervisord-managed docker (marun@redhat.com)
- debug.sh: comment and error message fixes (danw@redhat.com)
- debug.sh: filter out some potentially-sensitive data (danw@redhat.com)
- debug.sh: ignore --net=host containers (danw@redhat.com)
- debug.sh: try to find node config file from 'ps' output (danw@redhat.com)
- debug.sh: include resolv.conf in output (danw@redhat.com)
- debug.sh: explicitly run remote script via bash (danw@redhat.com)
- Validate SDN cluster/service network (rpenta@redhat.com)
- Fix GetClusterNetworkCIDR() (rpenta@redhat.com)
- Minor nit: change valid service IP check to use kapi.IsServiceIPSet
  (rpenta@redhat.com)
- Remove redundant tun0 route (rpenta@redhat.com)
- Fix multitenant flow cleanup again (danw@redhat.com)
- Fix cleanup of service OpenFlow rules (danw@redhat.com)
- Unconditionally use kubernetes iptables pkg to add iptables rules
  (danw@redhat.com)
- Backport changes from origin for kubernetes rebase (danw@redhat.com)
- Clean up stale OVS flows correctly / don't error out of TearDown early
  (danw@redhat.com)
- Fix non-multitenant pod routing (danw@redhat.com)
- Misc debug.sh fixes (danw@redhat.com)
- Detect SDN setup requirement when user switches between flat and multitenant
  plugins (rpenta@redhat.com)
- Minor: pod-network CLI examples to use # for comments (rpenta@redhat.com)
- Track PodIP->Namespace mappings, implement endpoint filtering
  (danw@redhat.com)
- Make plugins take osdn.OsdnRegistryInterface rather than creating it
  themselves (danw@redhat.com)
- Admin command to manage project network (rpenta@redhat.com)
- Fix SDN GetServices() (rpenta@redhat.com)
- Fix SDN status hook (rpenta@redhat.com)
- Use kubernetes/pkg/util/iptables for iptables manipulation (danw@redhat.com)
- Move firewall/iptables setup to common.go (danw@redhat.com)
- Updated debug.sh to handle origin vs OSE vs atomic naming conventions
  (danw@redhat.com)
- Change deprecated "oc get -t" to "oc get --template" in debug.sh
  (danw@redhat.com)
- Indicate if debug.sh fails because KUBECONFIG isn't set. (danw@redhat.com)
- Simplify service tracking by using kapi.NamespaceAll (danw@redhat.com)
- let Status call not do docker inspect, as an empty output defaults to that
  only within kubelet (rajatchopra@gmail.com)
- Replace hostname -f with unmae -n (nakayamakenjiro@gmail.com)
- Remove unused import/method (rpenta@redhat.com)
- plugins: Update Kube client imports (mkargaki@redhat.com)
- More code cleanup (no new changes) (rpenta@redhat.com)
- Fix gofmt in previous commit (rpenta@redhat.com)
- Fix imports in openshift-sdn plugins (rpenta@redhat.com)
- Sync openshift-sdn/plugins to origin/Godeps/.../openshift-sdn/plugins
  (rpenta@redhat.com)
- IP/network-related variable naming consistency/clarify (danw@redhat.com)
- Fix up setup.sh args (danw@redhat.com)
- Remove dead code from kube plugin (that was already removed from multitenant)
  (danw@redhat.com)
- Update setup_required to do the correct check for docker-in-docker
  (danw@redhat.com)
- Fix hack/test.sh (rpenta@redhat.com)
- Remove hack/build.sh from travis.yml (rpenta@redhat.com)
- Update README.md (rpenta@redhat.com)
- sync-to-origin.sh - Program to sync openshift-sdn changes to origin
  repository (rpenta@redhat.com)
- Remove Makefile (rpenta@redhat.com)
- Flat and Multitenant plugins for openshift sdn (rpenta@redhat.com)
- Move ovssubnet to pkg dir (rpenta@redhat.com)
- Remove standalone openshift-sdn binary (rpenta@redhat.com)
- Remove etcd registry (rpenta@redhat.com)
- cleanup lbr (rpenta@redhat.com)
- debug.sh: improve progress output a bit (danw@redhat.com)
- debug.sh: test services (danw@redhat.com)
- debug.sh: test default namespace in connectivity check (danw@redhat.com)
- Move vovsbr to br0 port 3 rather than 9 (danw@redhat.com)
- debug.sh: add some missing quotes (danw@redhat.com)
- Add a tool for gathering data to debug networking problems (danw@redhat.com)
- Cleanup docker0 interface before restarting docker, since it won't do so
  itself. (eric.mountain@amadeus.com)
- Fix SDN race conditions during master/node setup (rpenta@redhat.com)
- Use firewalld D-Bus API to configure firewall rules (danw@redhat.com)
- Add godbus dep (danw@redhat.com)
- Fix race condition in pkg/netutils/server/server_test.go (danw@redhat.com)
- Fix error messages in server_test.go (danw@redhat.com)
- Status hook for multitenant plugin (rpenta@redhat.com)
- Remove some testing cruft from the multitenant plugin (danw@redhat.com)
- Implement kubernetes status hook in kube plugin (danw@redhat.com)
- Update README.md (ccoleman@redhat.com)
- Make SDN MTU configurable (rpenta@redhat.com)
- Expose method for getting node IP in osdn api (rpenta@redhat.com)
- Revoke VNID for admin namespaces (rpenta@redhat.com)
- For multitenant plugin, handle both existing and admin namespaces
  (rpenta@redhat.com)
- Add GOPATH setup to hack/test.sh (danw@redhat.com)
- Improve error messages in pkg/netutils/server/server_test (danw@redhat.com)
- Make Get/Watch interfaces for nodes/subnets/namespaces consistent
  (rpenta@redhat.com)
- Consistent error logging in standalone registry/IP allocator
  (rpenta@redhat.com)
- Multi-tenant service isolation (danw@redhat.com)
- Get node IP from GetNodes() instead of net.Lookup() (rpenta@redhat.com)
- Renamed some field names to remove confusion (rpenta@redhat.com)
- VNID fixes (rpenta@redhat.com)
- Revert "Merge pull request #115 from danwinship/service-isolation"
  (danw@redhat.com)
- Add support for dind in multitenant plugin (marun@redhat.com)
- Fix veth host discovery for multitenant plugin (marun@redhat.com)
- In openshift-sdn standalone mode, trigger node event when node ip changes
  (rpenta@redhat.com)
- Pass updated node IP in the NodeEvent to avoid cache/stale lookup by
  net.LookupIP() (rpenta@redhat.com)
- Replace 'minion' with 'node' or 'nodeIP' based on context (rpenta@redhat.com)
- Update subnet openflow rules in case of host ip change (rpenta@redhat.com)
- Add install-dev target to makefile. (marun@redhat.com)
- Add support for docker-in-docker deployment (marun@redhat.com)
- Enable IP forwarding during openshift sdn setup (rpenta@redhat.com)
- Fix veth lookup for kernels with interface suffix (marun@redhat.com)
- service isolation support (danw@redhat.com)
- Add basic plugin migration script (dcbw@redhat.com)
- Remove some dead code (dcbw@redhat.com)
- Add some documentation about our isolation implementation (dcbw@redhat.com)
- add a few more comments to the multitenant OVS setup (danw@redhat.com)
- simplify the incoming-from-docker-bridge rule (danw@redhat.com)
- drop an unnecessary multitenant ovs rule (danw@redhat.com)
- fix a comment in openshift-sdn-multitenant-setup.sh (danw@redhat.com)
- make cross node services work (make the gateway a special exit); add priority
  to overlapping rules (rchopra@redhat.com)
- Let docker-only container global traffic through the vSwitch to tun0
  (dcbw@redhat.com)
- Allow vnid=x to send to vnid=0 on the same host (dcbw@redhat.com)
- distribute vnids from 10 (rchopra@redhat.com)
- Initialise VnidMap (rchopra@redhat.com)
- Don't install multitenant plugin for now (dcbw@redhat.com)
- Fix shell syntax error in openshift-ovs-multitenant (dcbw@redhat.com)
- Make the multitenant controller work (danw@redhat.com)
- multitenancy: logic to create and manage netIds for new namespaces
  (rchopra@redhat.com)
- multitenant mode call from 'main'; its just a copy of the kube functionality
  - no real multitenancy feature added (rchopra@redhat.com)
- move api,types,bin files to respective controllers (rchopra@redhat.com)
- fix error in bash script (rchopra@redhat.com)
- ignore the SDN setup/teardown if the NetworkMode of the container is 'host'
  (rchopra@redhat.com)
- fix issue#88 - generate unique cookie based on vtep (rchopra@redhat.com)
- install docker systemd conf file (rchopra@redhat.com)
- sdn should not re-configure docker/ovs if it appears to be a harmless restart
  (rchopra@redhat.com)
- Make docker-network configuration only happen when sdn is running
  (sdodson@redhat.com)
- Signal when the SDN is ready (ccoleman@redhat.com)
- Fix origin issue#2834; submit existing subnets as in-use (rchopra@redhat.com)
- doc: fix spelling error in example (thaller@redhat.com)
- kube-subnet-setup: fix setup iptables FORWARD rule (thaller@redhat.com)
- add sysctl flag to kube-setup (rchopra@redhat.com)
- Update the comments that go into /etc/sysconfig/docker-network
  (sdodson@redhat.com)
- lockwrap shell utils; add support for internet connectivity to containers
  spun directly through docker (rchopra@redhat.com)
- Forward packages to/from cluster_network (sdodson@redhat.com)
- Update /etc/sysconfig/docker-network rather than /etc/sysconfig/docker
  (sdodson@redhat.com)
- disallow 127.0.0.1 as vtep resolution (rchopra@redhat.com)
- state file no more with docker 1.6, use ethtool instead. Credit: Dan Winship
  (rchopra@redhat.com)
- fixed the default to kubernetes minion path (rchopra@redhat.com)
- Install files under %%{_buildroot}, fixes rpm build (sdodson@redhat.com)
- add option for etcd path to watched for minions (rajatchopra@gmail.com)
- remove revision arg from api as it is an etcd abstraction
  (rchopra@redhat.com)
- first set of reorg for api-fication of openshift-sdn (rchopra@redhat.com)
- fix bz1215107. Use the lbr gateway as the tun device address.
  (rchopra@redhat.com)
- kube plugin (rchopra@redhat.com)
- Adds network diagram. (mrunalp@gmail.com)
- Set DOCKER_NETWORK_OPTIONS via /etc/sysconfig/docker-network
  (sdodson@redhat.com)
- Add ip route description. (mrunal@me.com)
- Add router instructions. (mrunal@me.com)
- Add node instructions (mrunal@me.com)
- Add introduction (mrunal@me.com)
- Add README for native container networking. (mrunalp@gmail.com)
- Add SyslogIdentifier=openshift-sdn-{master,node} respectively
  (sdodson@redhat.com)
- add error checking to netutils/server; move ipam interface up
  (rchopra@redhat.com)
- netutils server (rchopra@redhat.com)
- Add service dependency triggering on enablement (sdodson@redhat.com)
- Adds a test for IP release. (mrunalp@gmail.com)
- Fix typo. (mrunalp@gmail.com)
- Add tests for IP Allocator. (mrunalp@gmail.com)
- Add IP Allocator. (mrunalp@gmail.com)
- Make SDN service dependencies more strict (sdodson@redhat.com)
- Document -container-network & -container-subnet-length in master sysconfig
  (sdodson@redhat.com)
- return if error is a stop by user event (rchopra@redhat.com)
- error handling, cleanup, formatting and bugfix in generating default gateway
  for a subnet (rchopra@redhat.com)
- store network config in etcd (rchopra@redhat.com)
- Makes subnets configurable. (mrunalp@gmail.com)
- Improve output formatting (miciah.masters@gmail.com)
- remove unnecessary for loop and handle client create error
  (rchopra@redhat.com)
- Add Restart=on-failure to unit files (miciah.masters@gmail.com)
- Remove unncessary print (nakayamakenjiro@gmail.com)
- Fixed error handling to catch error from newNetworkManager
  (nakayamakenjiro@gmail.com)
- WatchMinions: Correctly handle errors (miciah.masters@gmail.com)
- Add travis build file. (mrunalp@gmail.com)
- Add gofmt verifier script from Openshift. (mrunalp@gmail.com)
- Add starter test script. (mrunalp@gmail.com)
- Revert to hostname -f as go builtin doesn't return FQDN. (mrunalp@gmail.com)
- Always treat -etcd-path as a directory (miciah.masters@gmail.com)
- openshift-sdn-master does not require openvswitch or bridge-utils
  (sdodson@redhat.com)
- Update commit to a commit that exists upstream (sdodson@redhat.com)
- Require systemd in subpackages, update setup for tarball format
  (sdodson@redhat.com)
- Remove DOCKER_OPTIONS references from master sysconfig (sdodson@redhat.com)
- Push packaging work into the upstream repo (sdodson@redhat.com)
- Fix comment. (mrunalp@gmail.com)
- Rename refactor in the controller. (mrunalp@gmail.com)
- Use library function to get hostname. (mrunalp@gmail.com)
- Add a LICENSE file. (mrunalp@gmail.com)
- Just use Error when no formatting is needed (rchopra@redhat.com)
- fix issue#12. Give some slack for etcd to come alive. (rchopra@redhat.com)
- fix iptables rules for traffic from docker (rchopra@redhat.com)
- Fixed misspellings in output (jolamb@redhat.com)
- Update README.md (rchopra@redhat.com)
- Document DOCKER_OPTIONS variable (jolamb@redhat.com)
- Add helpful comment at start of docker sysconfig (jolamb@redhat.com)
- Use $DOCKER_OPTIONS env var for docker settings if present
  (jolamb@redhat.com)
- iptables modifications for vxlan (rchopra@redhat.com)
- non-permanence for linux bridge, so that we do not need restart network
  service (rchopra@redhat.com)
- init minion registry for sync mode, updated README for sync mode
  (rchopra@redhat.com)
- Sync mode for running independently of PaaS to register nodes
  (rchopra@redhat.com)
- burnish that spot (rchopra@redhat.com)
- README enhancements, specified requirements (rchopra@redhat.com)
- GetMinions fix on key (rchopra@redhat.com)
- gofmt fixes. (mrunalp@gmail.com)
- Update README.md (rchopra@redhat.com)
- initial commit (rchopra@redhat.com)

* Tue Jul 05 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.2
- clarify makefile (li.guangxu@zte.com.cn)
- Remove deprecated man pages (ffranz@redhat.com)
- Fixes usage for oc set probe and oc debug (ffranz@redhat.com)
- Add test for DockerImageConfig parsing and counting size of image layers
  (agladkov@redhat.com)
- Fix parsing DockerImageConfig (agladkov@redhat.com)
- disable stack tracing logic for curl operations, it breaks them.
  (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  ebd41a8b24bd95716b90a05fe0fda540c69fc119 (bparees@redhat.com)
- better warning for users when the buildconfig is of type binary
  (bparees@redhat.com)
- sort projects alphabetically (jvallejo@redhat.com)
- UPSTREAM: 28179: dedup workqueue requeing (deads@redhat.com)
- Add test for invalid client cert (jliggitt@redhat.com)
- add clusterquota projection for associated projects (deads@redhat.com)
- integration: wait for synced config before testing autoscaling
  (mkargaki@redhat.com)
- Unify counting of image layers in our helper and registry
  (agladkov@redhat.com)
- extended: test for iterative deployments (mkargaki@redhat.com)
- Limit the number of events and deployments displayed in dc describer
  (mfojtik@redhat.com)
- remove extra deploy invocation for sample repos tests (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  ec23cd36484d1c32d3cfdbbc160d30d06bac9db4 (jupierce@redhat.com)
- Clean up references to NETWORKING_DEBUG (marun@redhat.com)
- Bump vagrant memory to allow go builds (marun@redhat.com)
- UPSTREAM: 27435: Fix bugs in DeltaFIFO (deads@redhat.com)
- update completion help example (jvallejo@redhat.com)
- update generated docs (jvallejo@redhat.com)
- update completion help to use root command in examples (jvallejo@redhat.com)
- set env from secrets and configmaps (sjenning@redhat.com)
- Note that --env flag doesn't apply to templates (rhcarvalho@gmail.com)
- Simplify calls to FixturePath (rhcarvalho@gmail.com)
- oc: support rollout undo (mkargaki@redhat.com)
- oc: tests for rollout {pause,resume,history} (mkargaki@redhat.com)
- oc: support rollout history (mkargaki@redhat.com)
- UPSTREAM: 27267: kubectl: refactor rollout history (mkargaki@redhat.com)
- oc: support rollout {pause,resume} (mkargaki@redhat.com)
- oc: generated completions/docs for rollout (mkargaki@redhat.com)
- oc: make route utility reusable across packages (mkargaki@redhat.com)
- oc: port rollout command from kubectl (mkargaki@redhat.com)
- add new SCL version imagestreams (bparees@redhat.com)
- remove source repo from pipeline buildconfig (bparees@redhat.com)
- deploy: update tests in the deployment controller (mkargaki@redhat.com)
- deploy: use shared caches in the deployment controller (mkargaki@redhat.com)
- Fix --show-events=false for build configs and deployment configs
  (mfojtik@redhat.com)
- Update for openshift-sdn changes (danw@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  e2106a29fc38f962af64332e6e1d9f94e421c7aa (danw@redhat.com)
- Add 'MissingSecret' reason for pending builds (mfojtik@redhat.com)
- Don't fallback to cert when given invalid token (mkhan@redhat.com)
- commonize bc input across strategies; better insure bc ouput is set
  (gmontero@redhat.com)
- Do not hard code build name (rhcarvalho@gmail.com)
- e2e: honor $USE_IMAGES during registry's deployment (miminar@redhat.com)

* Thu Jun 30 2016 Troy Dawson <tdawson@redhat.com> 3.3.0.1
- add OSE 3.3 build target (tdawson@redhat.com)
- add oc create clusterquota (deads@redhat.com)
- Enable certain test debug with delve using DLV_DEBUG envvar.
  (maszulik@redhat.com)
- Registry auth cleanup (jliggitt@redhat.com)
- dind: avoid being targeted by oci-systemd-hooks (marun@redhat.com)
- dind: minor cleanup in systemd masking (marun@redhat.com)
- dind: stop systemd containers with RTMIN+3 (marun@redhat.com)
- Update hack/ose_image build scripts (tdawson@redhat.com)
- add clusterresourcequota/namespace reverse index (deads@redhat.com)
- Add master lease endpoint reconciler (agoldste@redhat.com)
- Send lifecycle hook status events from deployer pod (mfojtik@redhat.com)
- remove underscores from function names (deads@redhat.com)
- ab testing (rchopra@redhat.com)
- react to 27341: this does not fix races in our code (deads@redhat.com)
- UPSTREAM: 27341: Fix race in informer (deads@redhat.com)
- UPSTREAM: 28025: Add EndpointReconciler to master Config
  (agoldste@redhat.com)
- UPSTREAM: 26915: Extract interface for master endpoints reconciler
  (agoldste@redhat.com)

* Tue Jun 28 2016 Scott Dodson <sdodson@redhat.com> 3.3.0.0
- Godeps did not properly remove old registry godeps (ccoleman@redhat.com)
- track generated manpages (jvallejo@redhat.com)
- add manpage generation utils (jvallejo@redhat.com)
- UPSTREAM: 6744: add upstream genutils helpers (jvallejo@redhat.com)
- Fix sti build e2e test (miminar@redhat.com)
- ignore build version on bc update if version is older than existing value
  (bparees@redhat.com)
- force a db deployment in extended template tests (bparees@redhat.com)
- use an image with a valid docker1.9 manifest (bparees@redhat.com)
- Use docker/distribution v2.4.0+ (agladkov@redhat.com)
- Fixes oc set env --overwrite=false with multiple resources
  (ffranz@redhat.com)
- Changing logging statments to Clayton's spec (jupierce@redhat.com)
- oc: cleanup expose; make --port configurable for routes (mkargaki@redhat.com)
- add configchange trigger so deploy happens on imagechange
  (bparees@redhat.com)
- restructure run policy test and add logging (bparees@redhat.com)
- controller: move shared informers in separate package (mkargaki@redhat.com)
- deploy: fix initial image change deployments (mkargaki@redhat.com)
- oc: restore legacy behavior for deploy --latest (mkargaki@redhat.com)
- use valid commit for binary build test (bparees@redhat.com)
- Revert "use cache for referential integrity and escalation checks"
  (deads@redhat.com)
- tweak sample pipeline template and add to oc cluster up (bparees@redhat.com)
- cache: add an image stream lister and a reference index (mkargaki@redhat.com)
- deploy: add shared caches in the trigger controller (mkargaki@redhat.com)
- move _tools to _output/tools (sjenning@redhat.com)
- godep scripts (sjenning@redhat.com)
- Add a simple script for starting a local docker registry
  (ccoleman@redhat.com)
- UPSTREAM: 25913: daemonset handle DeletedFinalStateUnknown (deads@redhat.com)
- use cache for referential integrity and escalation checks (deads@redhat.com)
- add cluster quota APIs (deads@redhat.com)
- oc set env must respect --overwrite=false (ffranz@redhat.com)
- display cache mutation errors in stdout (deads@redhat.com)
- dc controller was mutating cache objects (deads@redhat.com)
- increase watch timeout for build controller test (bparees@redhat.com)
- use shared informer for authorization (deads@redhat.com)
- UPSTREAM: 27784: add optional mutation checks for shared informer cache
  (deads@redhat.com)
- UPSTREAM: 27786: add lastsyncresourceversion to sharedinformer
  (deads@redhat.com)
- deploy: enhance status for deploymentconfigs (mkargaki@redhat.com)
- deploy: generated code for deploymentconfig status enhancements
  (mkargaki@redhat.com)
- extended: test deploymentconfig rollback (mkargaki@redhat.com)
- oc: make rollback use both paths for rolling back (mkargaki@redhat.com)
- deploy: add new endpoint for rolling back deploymentconfigs
  (mkargaki@redhat.com)
- deploy: generated code for rollback (mkargaki@redhat.com)
- Add missed fast path conversions (will go upstream eventually)
  (ccoleman@redhat.com)
- Don't state crashlooping container when pod only has one container
  (mkhan@redhat.com)
- hide authorization resource groups to prevent further usage
  (deads@redhat.com)
- handle cyclic dependencies in build-chain (gmontero@redhat.com)
- highlight current project with asterisk (jvallejo@redhat.com)
- Fixes examples of oc proxy (ffranz@redhat.com)
- Delete obsolete Dockerfile (jawnsy@redhat.com)
- Expose a way for clients to discover OpenShift API resources
  (ccoleman@redhat.com)
- update cluster-reader tests to use discovery (deads@redhat.com)
- UPSTREAM: 26355: refactor quota evaluation to cleanly abstract the quota
  access (deads@redhat.com)
- Use include flags with build (agladkov@redhat.com)
- UPSTREAM: docker/distribution: <carry>: custom routes/auth
  (agoldste@redhat.com)
- bump(github.com/docker/distribution):
  596ca8b86acd3feebedae6bc08abf2a48d403a14 (agladkov@redhat.com)
- refactor openshift for quota changes (deads@redhat.com)
- UPSTREAM: 25091: reduce conflict retries (deads@redhat.com)
- UPSTREAM: 25414: Improve quota integration test to not use events
  (deads@redhat.com)
- deploy: reread hook logs on Retry (mkargaki@redhat.com)
- Unmarshal ports given in integer format (surajssd009005@gmail.com)
- Changing secrets.go to avoid unreliable docker build output capture. Also
  changing test cases so that BuildConfig resources are local to the tree and
  do not need to be current in origin/master HEAD. (jupierce@redhat.com)
- bump(github.com/openshift/source-to-image):
  69a0d96663b775c5e8fa942401c7bb9ca495e8f0 (bparees@redhat.com)
- add oc completion cmd wrapper (jvallejo@redhat.com)
- Modify oadm print statements to use stderr (mkhan@redhat.com)
- bump(coreos/etcd): fix etcd hash in Godeps.json (agoldste@redhat.com)
- add /version/openshift (deads@redhat.com)
- deploy: use shared caches in the dc controller (mkargaki@redhat.com)
- deploy: caches obsolete dc update in the deployerpod controller
  (mkargaki@redhat.com)
- cache: add a deploymentconfig lister (mkargaki@redhat.com)
- Revert "fixup coreos dep bump" (ccoleman@redhat.com)
- Made output of error more specific to bad parameter in a template file
  Updated tests for my change (rymurphy@redhat.com)
- Bump origin-web-console (cf5a74d) (jforrest@redhat.com)
- Bump origin-web-console (cf5a74d) (jforrest@redhat.com)
- bump(coreos/etcd):8b320e7c550067b1dfb37bd1682e8067023e0751 fixup coreos dep
  bump (sjenning@redhat.com)
- bump(github.com/AaronO/go-git-http/auth) but not really because mfojtik was
  just too tired to type those last 2 character (eparis@redhat.com)
- Clean up unused token secret (jliggitt@redhat.com)
- Update MySQL replication tests to reflect new template
  (nagy.martin@gmail.com)
- Add missing fuzzers for AnonymousConfig test (mfojtik@redhat.com)
- revise pipeline instructions for current sample state (bparees@redhat.com)
- Clean up unused token secret (jliggitt@redhat.com)
- Add a make perform-official-release target (ccoleman@redhat.com)
- Don't enforce quota in registry by default (miminar@redhat.com)
- oc describe for JenkinsBuildStrategy (gmontero@redhat.com)
- DSL openShift -> openshift in Jenkinsfile (gmontero@redhat.com)
- add mutation cache (deads@redhat.com)
- UPSTREAM: 25091: partial - reduce conflict retries (deads@redhat.com)
- convert dockercfg secret generator to a work queue (deads@redhat.com)
- return status error from build admission (deads@redhat.com)
- Fix docker tag command in hack/build-images.sh (mkumatag@in.ibm.com)
- Deleteing buildconfig with wildcard results in wrong output not related to
  action taken (skramaja@redhat.com)
- GIF version of asciicast (ccoleman@redhat.com)
- Ignore attempt to empty route spec.host field (jliggitt@redhat.com)
- Add screen cap of oc cluster up to README (ccoleman@redhat.com)
- Add error detection and UT to image progress (cewong@redhat.com)
- UPSTREAM: 27644: Use preferred group version when discovery fails due to 403
  (mkhan@redhat.com)
- Disable ResourceQuota while it is being investigated (ccoleman@redhat.com)
- UPSTREAM: <carry>: Limit affinity but handle error (ccoleman@redhat.com)
- UPSTREAM: <drop>: Remove string trimming (ccoleman@redhat.com)
- Reenable upstream e2e, disable PodAffinity (ccoleman@redhat.com)
- When updating policies and roles, only update last modified on change
  (ccoleman@redhat.com)
- DiscoveryRESTMapper was not caching the calculated mapper
  (ccoleman@redhat.com)
- UPSTREAM: 27243: Don't alter error type from server (ccoleman@redhat.com)
- UPSTREAM: 27242: Make discovery client parameterizable to legacy prefix
  (ccoleman@redhat.com)
- Fixes router printer line breaks (ffranz@redhat.com)
- Update test data to not reference v1beta3 (jforrest@redhat.com)
- cluster up: prevent start without a writeable KUBECONFIG (cewong@redhat.com)
- udpate jenkinsfile to use new DSL (gmontero@redhat.com)
- Added newline print to warning when individual rsync strategies fail Changed
  the return error to say that all strategies have failed, as opposed to just
  the final strategy error. (rymurphy@redhat.com)
- UPSTREAM: 23801: update Godeps completion support (jvallejo@redhat.com)
- Don't enforce quota in registry by default (miminar@redhat.com)
- deploy: deep-copy rcs before mutating them (mkargaki@redhat.com)
- UPSTREAM: <drop>: Disable timeouts on kubelet pull and logs
  (ccoleman@redhat.com)
- Add immutable updates on access and authorize tokens (ccoleman@redhat.com)
- Build LastVersion should be int64 (ccoleman@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  c3721f675f5474b717e6eb6aff9b837e095b6840 (rpenta@redhat.com)
- Auto generated conversions and swagger spec/descriptions for ClusterNetwork
  resource and node networkPluginName changes (rpenta@redhat.com)
- Make node to auto detect openshift network plugin from master
  (rpenta@redhat.com)
- Use ClusterNetworkDefault for referring to 'default' cluster network
  (rpenta@redhat.com)
- Added pluginName field to ClusterNetwork resource (rpenta@redhat.com)
- Fixes deprecated oc exec examples (ffranz@redhat.com)
- add clusterquota types (deads@redhat.com)
- React to int -> intXX changes in the code (ccoleman@redhat.com)
- start using shared informer (deads@redhat.com)
- UPSTREAM: 26276: make quota validation re-useable (deads@redhat.com)
- add cluster rules to namespace powers (deads@redhat.com)
- import docker-compose env var substitution (surajssd009005@gmail.com)
- oc: don't print anything specific on create yet (mkargaki@redhat.com)
- UPSTREAM: 26161: kubectl: move printObjectSpecificMessage in factory
  (mkargaki@redhat.com)
- deploy: use new sorting logic for deployment logs (mkargaki@redhat.com)
- UPSTREAM: 26771: kubectl: fix sort logic for logs (mkargaki@redhat.com)
- UPSTREAM: 27048: kubectl: return more meaningful timeout errors
  (mkargaki@redhat.com)
- UPSTREAM: 27048: kubectl: ignore only update conflicts in the scaler
  (mkargaki@redhat.com)
- Convert all int types to int32 or int64 (ccoleman@redhat.com)
- Add fast path conversions for Origin resources (ccoleman@redhat.com)
- Generated files (mfojtik@redhat.com)
- Interesting changes (mfojtik@redhat.com)
- defaulting changes (mfojtik@redhat.com)
- boring changes (mfojtik@redhat.com)
- UPSTREAM: 27412: Allow specifying base location for test etcd data
  (jliggitt@redhat.com)
- UPSTREAM: 26078: Fix panic when the namespace flag is not present
  (mfojtik@redhat.com)
- UPSTREAM: openshift/openshift-sdn: 321: Fix integers and add missing methods
  to OVS plugin (mfojtik@redhat.com)
- UPSTREAM: coreos/etcd: 5617: fileutil: avoid double preallocation
  (jliggitt@redhat.com)
- UPSTREAM: coreos/etcd: 5572: fall back to truncate() if fallocate is
  interrupted (mfojtik@redhat.com)
- UPSTREAM: skynetservices/skydns: <carry>: Allow listen only ipv4
  (ccoleman@redhat.com)
- UPSTREAM: skynetservices/skydns: <carry>: Disable systemd activation for DNS
  (ccoleman@redhat.com)
- UPSTREAM: google/cadvisor: <carry>: Disable container_hints flag that is set
  twice (mfojtik@redhat.com)
- UPSTREAM: emicklei/go-restful: <carry>: Add "Info" to go-restful ApiDecl
  (ccoleman@redhat.com)
- bump(denverdino/aliyungo): 554da7ebe31b6172a8f15a0b1cf8c628145bed6a
  (mfojtik@redhat.com)
- bump(github.com/docker/engine-api): 3d72d392d07bece8d7d7b2a3b6b2e57c2df376a2
  (mfojtik@redhat.com)
- bump(github.com/google/cadvisor): 750f18e5eac3f6193b354fc14c03d92d4318a0ec
  (mfojtik@redhat.com)
- bump(github.com/spf13/cobra): 4c05eb1145f16d0e6bb4a3e1b6d769f4713cb41f
  (mfojtik@redhat.com)
- bump(github.com/onsi/ginkgo): 2c2e9bb47b4e44067024f29339588cac8b34dd12
  (mfojtik@redhat.com)
- bump(github.com/coreos): 8b320e7c550067b1dfb37bd1682e8067023e0751
  (mfojtik@redhat.com)
- bump(github.com/emicklei/go-restful):
  496d495156da218b9912f03dfa7df7f80fbd8cc3 (mfojtik@redhat.com)
- bump(github.com/fsouza/go-dockerclient):
  bf97c77db7c945cbcdbf09d56c6f87a66f54537b (mfojtik@redhat.com)
- bump(github.com/onsi/gomega): 7ce781ea776b2fd506491011353bded2e40c8467
  (mfojtik@redhat.com)
- bump(github.com/skynetservices/skydns):
  1be70b5b8aa07acccd972146d84011b670af88b4 (mfojtik@redhat.com)
- bump(gopkg.in/yaml.v2) a83829b6f1293c91addabc89d0571c246397bbf4
  (mfojtik@redhat.com)
- bump(k8s.io/kubernetes): 686fe3889ed652b3907579c9e46f247484f52e8d
  (mfojtik@redhat.com)
- Refactored binary build shell invocation (skuznets@redhat.com)
- Refactored stacktrace implementation for bash scripts (skuznets@redhat.com)
- Failure in extended deployment test (ccoleman@redhat.com)
- Fixes examples of port-forward (ffranz@redhat.com)
- Added quote func to make all DOT ID valids (mkhan@redhat.com)
- Lock release build to specific versions (ccoleman@redhat.com)
- Bump origin-web-console (7840198) (jforrest@redhat.com)
- atomic-registry via systemd (aweiteka@redhat.com)
- Typo fix - oc dockerbuild example (mkumatag@in.ibm.com)
- cluster up: optionally install metrics components (cewong@redhat.com)
- refactor to Complete-Validate-Run (pweil@redhat.com)
- Bug 1343681 - Fix tagsChanged logic (maszulik@redhat.com)
- tolerate multiple bcs pointing to same istag for oc status
  (gmontero@redhat.com)
- use defined constant (pweil@redhat.com)
- deploy: switch config change to a generic trigger controller
  (mkargaki@redhat.com)
- deploy: move config change controller to new location (mkargaki@redhat.com)
- deploy: stop instantiating from the image change controller
  (mkargaki@redhat.com)
- Changed glog V(1) and V(2) to V(0) (jupierce@redhat.com)
- Add make to all release images and add a Golang 1.7 image
  (ccoleman@redhat.com)
- Refactored os::text library to use `[[' tests instead of `[' tests
  (skuznets@redhat.com)
- Implemented `os::text::clear_string' to remove a string from TTY output
  (skuznets@redhat.com)
- Escaped special characters in regex (skuznets@redhat.com)
- Refactored `source' statements that drifted since the original PR
  (skuznets@redhat.com)
- Added `findutils' dependency for DIND image (skuznets@redhat.com)
- Renamed $ORIGIN_ROOT to $OS_ROOT for consistency (skuznets@redhat.com)
- Revert "Revert "Implemented a single-directive library import for Origin Bash
  scripts"" (skuznets@redhat.com)
- Update pipeline templates (spadgett@redhat.com)
- update "oc projects" to display all projects (jvallejo@redhat.com)
- Cleanup some dead test code (ccoleman@redhat.com)
- Increase the lease renewal fraction to 1/3 interval (ccoleman@redhat.com)
- Return the error from losing a lease to log output (ccoleman@redhat.com)
- Prevent route theft by removing the ability to update spec.host
  (ccoleman@redhat.com)
- allow map keys to be templatized (deads@redhat.com)
- deploy: remove deployer pods on cancellation (mkargaki@redhat.com)
- bypass k8s container image validation when ict's defined (allow for empty
  string) (gmontero@redhat.com)
- Update CONTRIBUTING and HACKING docs (mkargaki@redhat.com)
- Bug 1327108 - Updated error information when trying to import ImageStream
  pointing to a different one (maszulik@redhat.com)
- Revert "remove lastModified from policy and policybinding"
  (deads2k@users.noreply.github.com)
- Check logs after we verify the deployment passed (ccoleman@redhat.com)
- When tagging an image across image streams, rewrite the tag ref
  (ccoleman@redhat.com)
- Bug in oc describe imagestream (ccoleman@redhat.com)
- ImageStreamMappings should default DockerImageReference (ccoleman@redhat.com)
- Allow mutation of image dockerImageReference (ccoleman@redhat.com)
- Add 'oc create imagestream' (ccoleman@redhat.com)
- Allow --reference to be passed to oc tag (ccoleman@redhat.com)
- remove lastModified from policy and policybinding (deads@redhat.com)
- setup_tmpdir_vars(): TPMDIR -> TMPDIR (miciah.masters@gmail.com)
- respect scopes for rules review (deads@redhat.com)
- Updated Dockerfiles (ccoleman@redhat.com)
- Move directories appropriately (ccoleman@redhat.com)
- Change code to use /testdata/ instead of /fixtures directories
  (ccoleman@redhat.com)
- dind: enable intra pod test (marun@redhat.com)
- dind: Fix EmptyDir support (marun@redhat.com)
- dind: rm docker volumes natively (added in 1.9) (marun@redhat.com)
- bump(github.com/evanphx/json-patch):465937c80b3c07a7c7ad20cc934898646a91c1de
  (jimmidyson@gmail.com)
- remove multiple template example, it's a lie (bparees@redhat.com)
- Move fixtures to testdata directories (ccoleman@redhat.com)
- New release images locked to Go versions (ccoleman@redhat.com)
- Be more selective about what we generate for build names
  (ccoleman@redhat.com)
- Add instructions for downloading oc and using hosted template
  (sspeiche@redhat.com)
- don't specify sync project (bparees@redhat.com)
- cluster up: print last 10 lines of logs on errors after container started
  (cewong@redhat.com)
- Command to set deployment hooks on deployment configs (cewong@redhat.com)
- integration: bump timeout for non-automatic test (mkargaki@redhat.com)
- builders: simplified image progress reporting (cewong@redhat.com)
- Update bindata (mkargaki@redhat.com)
- Retry service account update on conflict (jliggitt@redhat.com)
- fix django typo (bparees@users.noreply.github.com)
- Add liveness probe for the ipfailover dc. (smitram@gmail.com)
- Allow import all tags when .spec.tags are specified as well
  (maszulik@redhat.com)
- allocate route host on update if host is empty in spec (pweil@redhat.com)
- add service dependency and infrastructure annotations (bparees@redhat.com)
- Added Signatures field to Image object (miminar@redhat.com)
- fix some ineffassign issues (v.behar@free.fr)
- Trap sigterm and cleanup - remove any assigned VIPs. (smitram@gmail.com)
- Add a GCS test to verify it is compiled in (ccoleman@redhat.com)
- mark docker compose as experimental (bparees@redhat.com)
- Build dockerregistry with tag `include_gcs` (ccoleman@redhat.com)
- UPSTREAM: docker/distribution: <carry>: Distribution dependencies
  (ccoleman@redhat.com)
- debug / workarounds for image extended tests wrt current ICT based deploy
  behavior (gmontero@redhat.com)
- Update go version in contributing doc (jliggitt@redhat.com)
- Fix job e2e test (maszulik@redhat.com)
- make project watch work for namespace deletion (deads@redhat.com)
- set build-hook command (cewong@redhat.com)
- Guard against deleting entire filesystem in hack/test-go.sh
  (skuznets@redhat.com)
- Detect data races in `go test` log output (skuznets@redhat.com)
- Bug 1343426: list deployments correctly in oc deploy (mkargaki@redhat.com)
- auto-create a jenkins service account (bparees@redhat.com)
- Refactor image-import command into managable methods (maszulik@redhat.com)
- Increase the tests coverage for import-image command (maszulik@redhat.com)
- extended: refactor deployment tests (mkargaki@redhat.com)
- deploy: add pausing for deploymentconfigs (mkargaki@redhat.com)
- deploy: generated code for pause (mkargaki@redhat.com)
- bypass oc.Run() --follow --wait output flakes (gmontero@redhat.com)
- stop mutating cache (deads@redhat.com)
- add openshift ex config patch to modify master-config.yaml (deads@redhat.com)
- Improve escalation error message (jliggitt@redhat.com)
- prevent the build controller from escalating users (deads@redhat.com)
- Remove template fields with default values (rhcarvalho@gmail.com)
- fix scope character validation (jliggitt@redhat.com)
- UPSTREAM: 26554: kubectl: make --container-port actually work for expose
  (mkargaki@redhat.com)
- deploy: ignore set lastTriggeredImage on create (mkargaki@redhat.com)
- Fixes --show-labels when printing OpenShift resources (ffranz@redhat.com)
- UPSTREAM: 26793: expose printer utils (ffranz@redhat.com)
- Add the both ROUTER_SERVICE*SNI_PORT (cw-aleks@users.noreply.github.com)
- SCC check API: add addmission in podnodeconstraints (salvatore-
  dario.minonne@amadeus.com)
- Extended tests: added quota and limit range related tests
  (miminar@redhat.com)
- Cache limit range objects in registry (miminar@redhat.com)
- Allow to toggle quota enforcement in the registry (miminar@redhat.com)
- Limit imagestreamimages and imagestreamtags (miminar@redhat.com)
- Limit ImageStreams per project using quota (miminar@redhat.com)
- Use helpers to parse and make imagestream tag names (miminar@redhat.com)
- Image size admission with limitrange (pweil@redhat.com)
- Removed image quota evaluators (miminar@redhat.com)
- Serve DNS from the nodes (ccoleman@redhat.com)
- UPSTREAM: 24118: Proxy can be initialized directly (ccoleman@redhat.com)
- UPSTREAM: 24119: Use default in AddFlags (ccoleman@redhat.com)
- fix contextdir path (bparees@redhat.com)
- Improve validation message on build spec update (cewong@redhat.com)
- add service serving cert signer to token controller initialization
  (deads@redhat.com)
- UPSTREAM: <carry>: add service serving cert signer to token controller
  (deads@redhat.com)
- address typecast panic (gmontero@redhat.com)
- deflake second level timing issue in TestDescribeBuildDuration
  (gmontero@redhat.com)
- add validation to prevent filters on dn lookups (deads@redhat.com)
- BasicAuthIdentityProvider: Do not follow redirection (sgallagh@redhat.com)
- router: Add name and namespace templates params (miciah.masters@gmail.com)
- api: fix serialization test for deploymentconfigs (mkargaki@redhat.com)
- SCC check: API and validation (salvatore-dario.minonne@amadeus.com)
- builder: increase git check timeout exponentially (cewong@redhat.com)
- Add a test to validate ipfailover starts (ccoleman@redhat.com)
- oc set probe/triggers: set output version (cewong@redhat.com)
- Default container name on execPod lifecycle hooks (ccoleman@redhat.com)
- Add temporary HTTP failures to image retry (ccoleman@redhat.com)
- Import app.json to OpenShift applications (ccoleman@redhat.com)
- UPSTREAM: 25487: pod constraints func for quota validates resources
  (decarr@redhat.com)
- UPSTREAM: 24514: Quota ignores pod compute resources on updates
  (decarr@redhat.com)
- UPSTREAM: 25161: Sort resources in quota errors to avoid duplicate events
  (decarr@redhat.com)
- gitserver: allow anonymous access when using uid/pwd auth (cewong@redhat.com)
- Skip registry client v1 and v2 tests until we push with 1.10
  (ccoleman@redhat.com)
- deploy: restore ict behavior for deploymentconfig with no cc triggers
  (mkargaki@redhat.com)
- unbreak e2e after DNS and oc cluster up (deads@redhat.com)
- Update jenkins-master-template.json context (xiuwang)
- bump(github.com/openshift/source-to-image):
  2abf650e2e65008e5837266991ff4f2aed14bf39 (cewong@redhat.com)
- let builders create new imagestreams for pushes (deads@redhat.com)
- Allow size of image to be zero when schema1 from Hub (ccoleman@redhat.com)
- IPFailover was broken for alpha.1 (ccoleman@redhat.com)
- Add watch caching to origin types (jliggitt@redhat.com)
- test-integration etcd verbosity controlled by OSTEST_VERBOSE_ETCD
  (deads@redhat.com)
- fix oc describe panic (ipalade@redhat.com)
- Integration test for automatic=false ICTs (mkargaki@redhat.com)
- Bug 1340735: update dc image at most once on automatic=false
  (mkargaki@redhat.com)
- If --public-hostname is an IP, use it for server IP in cluster up
  (ccoleman@redhat.com)
- dockerbuild pulls all images rather than :latest (ccoleman@redhat.com)
- Bug 1340344 - Add additional interfaces implementation for handling watches,
  rsh, etc. (maszulik@redhat.com)
- Add test for suppression of router reload (marun@redhat.com)
- Printing duplicate messages during startbuild (ccoleman@redhat.com)
- Enable integration test debug with delve (marun@redhat.com)
- Optionally skip building integration test binary (marun@redhat.com)
- Fix verbose output for hack/test-integration.sh (marun@redhat.com)
- Avoid router reload during sync (marun@redhat.com)
- add impersonate-group (deads@redhat.com)
- Increased timeout in TestTimedCommand integration test (skuznets@redhat.com)
- add ROUTER_SLOWLORIS_TIMEOUT enviroment variable to default router image
  (jtanenba@redhat.com)
- Fix misspells reported by goreportcard.com (v.behar@free.fr)
- make the jenkins service last so that you can retry on failures
  (deads@redhat.com)
- cleanup bootstrap policy to allow future changes (deads@redhat.com)
- hack/util: wait for registry readiness (miminar@redhat.com)
- Updated auto generated docs for pod-network CLI cmd (rpenta@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  b74a40614df17a99b8f77ac0dbd9aaa3ffae3218 (rpenta@redhat.com)
- Pass iptablesSyncPeriod config to SDN node plugin (rpenta@redhat.com)
- Change default value of iptablesSyncPeriod from 5s to 30s (rpenta@redhat.com)
- Add goreportcard badge in README (mkargaki@redhat.com)
- add cli describer for oauthtokens (jvallejo@redhat.com)
- Document things, remove /usr/bin/docker mount from contrib systemd unit
  (sdodson@redhat.com)
- Fix git clone tests (jliggitt@redhat.com)
- chroot docker to the rootfs (sdodson@redhat.com)
- bump(github.com/openshift/source-to-image):
  6373e0ab0016dd013573f55eaa037c667f8e4a92 (vsemushi@redhat.com)
- UPSTREAM: 25907: Fix detection of docker cgroup on RHEL (agoldste@redhat.com)
- Updated allowed levels of `glog` info levels in CLI doc (skuznets@redhat.com)
- Tolerate partial successes on reconciling cluter role bindings
  (skuznets@redhat.com)
- add build trigger information and separate buildconfig data
  (ipalade@redhat.com)
- Warn if a docker compose service has no ports (ccoleman@redhat.com)
- bump(github.com/openshift/source-to-image):
  65db940221d282c2f7f1d21998bbd4af2f8a1c16 (gmontero@redhat.com)
- git server readme: fix references to gitserver (cewong@redhat.com)
- More pretty readme (ccoleman@redhat.com)
- gitserver: allow specifying build strategy (cewong@redhat.com)
- remove resource groups and divide by API group (deads@redhat.com)
- Truncate labels of builds generated from a BuildConfig (cewong@redhat.com)
- Refactored builder remote URI check to used timed ListRemote
  (skuznets@redhat.com)
- Added a timeout to `git ls-remote` invocation in `oc new-app`
  (skuznets@redhat.com)
- Refactored command functions not to accept a Writer (skuznets@redhat.com)
- make the pipeline readme pretty (bparees@redhat.com)
- Update egress-router package dependencies (danw@redhat.com)
- make the empty API groups to "" for policy rules standard (deads@redhat.com)
- Separated export from declaration for environment variables
  (skuznets@redhat.com)
- Added make update to simplify updating all generated artifacts.
  (maszulik@redhat.com)
- bump(github.com/Microsoft/go-winio):4f1a71750d95a5a8a46c40a67ffbed8129c2f138
  (sdodson@redhat.com)
- Service account token controller startup change (jliggitt@redhat.com)
- Disable sticky sessions for tcp routes based on env value. Updated to use env
  variable value directly as per @smarterclayton comments. (smitram@gmail.com)
- Update the jsonpath template link in oc get -h (ripcurld.github@gmail.com)
- UPSTREAM: 23858: Convert service account token controller to use a work queue
  (jliggitt@redhat.com)
- [RPMS] bump BuildRequires: golang to 1.6.2 (#19) (sdodson@redhat.com)
- cluster up: fix insecure registry argument message (cewong@redhat.com)
- add jenkins pipeline example files (bparees@redhat.com)
- UPSTREAM: 24537: Add locks in HPA test (deads@redhat.com)
- make admission plugins enablable or disabable based on config
  (deads@redhat.com)
- UPSTREAM: 25898: make admission plugins configurable based on external
  criteria (deads@redhat.com)
- respect scopes during authz delegation (deads@redhat.com)
- discovery rest mapper (deads@redhat.com)
- Update glogging to always set level, and to respect glog.level
  (ccoleman@redhat.com)
- Mount only host dir to copy files from (cewong@redhat.com)
- Enhance jenkins-persistent-template and jenkins-ephemeral-template
  (tnozicka@gmail.com)
- add scope options to oc policy can-i (deads@redhat.com)
- allow SAR to specify scopes (deads@redhat.com)
- cluster up: test bootstrap asset locations (cewong@redhat.com)
- Fix govet errors in oc cluster up for 1.6 (cewong@redhat.com)
- oc: inform about switch to the same project (mkargaki@redhat.com)
- Bug 1338679: emit events on failure to create a deployer pod
  (mkargaki@redhat.com)
- Drop Go 1.4 conditions, switch to 1.6 by default (ccoleman@redhat.com)
- Docker image cannot have - or _ in succession (ccoleman@redhat.com)
- Allow a user to specify --as-user or --as-root=false (ccoleman@redhat.com)
- Update extensionProperties to single array of structs (jforrest@redhat.com)
- eliminate need for SA token as client secret annotation (deads@redhat.com)
- Longer timeout on test fixture DC (ccoleman@redhat.com)
- Switch gitserver to use origin-base (cewong@redhat.com)
- Bump origin-web-console (5cfe43625c3885835f2b23b674e527ceabf17502)
  (jliggitt@redhat.com)
- policy unsafe proxy requests separately (jliggitt@redhat.com)
- Limit queryparam auth to websockets (jliggitt@redhat.com)
- cluster up: allow specifying a full image template (cewong@redhat.com)
- retry SA annotation updates in the test in case of conflicts or other
  weirdness (deads@redhat.com)
- bump(github.com/AaronO/go-git-http) 34209cf6cd947cfa52063bcb0f6d43cfa50c5566
  (cewong@redhat.com)
- deployapi: fix automatic description (mkargaki@redhat.com)
- Fix tests for the trigger controllers (mkargaki@redhat.com)
- Resolve image for all initial deployments (mkargaki@redhat.com)
- Deploymentconfig controller should update dc status on successful exit
  (mkargaki@redhat.com)
- Stop using the deploymentconfig generator (mkargaki@redhat.com)
- fix flaky configapi fuzzing for SA grant method (deads@redhat.com)
- Support arbitrary key:value properties for console extensions
  (jforrest@redhat.com)
- default to letting oauth clients request all scopes from users
  (deads@redhat.com)
- allow configuration of the SA oauth client grant flows (deads@redhat.com)
- cluster up: use alternate port for DNS when 53 is not available
  (cewong@redhat.com)
- use service account credentials as oauth token (deads@redhat.com)
- add AdditionalSecrets to oauthclients (deads@redhat.com)
- UPSTREAM: RangelReale/osin: <carry>: only request secret validation
  (deads@redhat.com)
- Update atomic registry quickstart artifacts (aweiteka@redhat.com)
- Restrict the scratch name to lowercase in the dockerbuilder
  (ccoleman@redhat.com)
- run registry as daemonset (pweil@redhat.com)
- cluster up: ensure you can login as administrator (cewong@redhat.com)
- F5: Cleanup mockF5.close() calls in tests (miciah.masters@gmail.com)
- add user:list-projects scope (deads@redhat.com)
- refactor whatcanido to can-i --list (deads@redhat.com)
- oc: separate test for the deploymentconfig describer (mkargaki@redhat.com)
- oc: enhance the deploymentconfig describer (mkargaki@redhat.com)
- print proper image name during root user warning (bparees@redhat.com)
- README for 'oc cluster up/down' (cewong@redhat.com)
- allow who-can to reference resource names (deads@redhat.com)
- extend timeout for SSCS tests running in parallel (deads@redhat.com)
- Allow update on hostsubnets (rpenta@redhat.com)
- Cleanup all asset related files in origin (jforrest@redhat.com)
- make scopes forbidden message friendlier to read (deads@redhat.com)
- Client command to start OpenShift with reasonable defaults
  (cewong@redhat.com)
- Include option in console vendoring script to generate the branch and commit
  automatically (jforrest@redhat.com)
- Bump origin-web-console (140a1f1) (jforrest@redhat.com)
- UPSTREAM: 25690: Fixes panic on round tripper when TLS under a proxy
  (ffranz@redhat.com)
- o Add locking around ops that change state. Its better to go   lockless
  eventually and use a "shadow" (cloned) copy of the   config when we do a
  reload. o Fixes as per @smarterclayton review comments. (smitram@gmail.com)
- create client code for oauth types and tests (deads@redhat.com)
- add scope restrictions to oauth clients (deads@redhat.com)
- container image field values irrelevant with ict's in automatic mode, don't
  have setting that confuses users; add updated quickstarts
  (gmontero@redhat.com)
- localsubjectaccessreview test-cmd demonstration with scoped token
  (deads@redhat.com)
-   o Add basic validation for route TLS configuration - checks that     input
  is "syntactically" valid.   o Checkpoint initial code.   o Add support for
  validating route tls config.   o Add option for validating route tls config.
  o Validation fixes.   o Check private key + cert mismatches.   o Add tests.
  o Record route rejection.   o Hook into add route processing + store invalid
  service alias configs     in another place - easy to check prior errors on
  readmission.   o Remove entry from invalid service alias configs upon route
  removal.   o Add generated completions.   o Bug fixes.   o Recording
  rejecting routes is not working completely.   o Fix status update problem -
  we should set the status to admitted     only if we had no errors handling a
  route.   o Rework to use a new controller - extended_validator as per
  @smarterclayton comments.   o Cleanup validation as per @liggitt comments.
  o Update bash completions.   o Fixup older validation unit tests.   o Changes
  as per @liggitt review comments + cleanup tests.   o Fix failing test.
  (smitram@gmail.com)
- Cleanup output to builds, force validation, better errors
  (ccoleman@redhat.com)
- Convert builder glog use to straight output (ccoleman@redhat.com)
- Add a simple glog replacement stub (ccoleman@redhat.com)
- Print hooks for custom deployments and multiline commands
  (ccoleman@redhat.com)
- Recreate deployment should always run the acceptor (ccoleman@redhat.com)
- Updated generated deepcopy/conversion (ccoleman@redhat.com)
- Enable custom deployments to have rolling/recreate as well
  (ccoleman@redhat.com)
- Add incremental conditional completion to deployments (ccoleman@redhat.com)
- UPSTREAM: 25617: Rolling updater should indicate progress
  (ccoleman@redhat.com)
- If desired conditions match, don't go into a wait loop (ccoleman@redhat.com)
- Add an annotation that skips creating deployer pods (ccoleman@redhat.com)
- Update deployment logs and surge on recreate (ccoleman@redhat.com)
- return status errors from build clone API (deads@redhat.com)
- Fix go vet errors (rhcarvalho@gmail.com)
- Ignore errors on debug when a template is returned (ccoleman@redhat.com)
- bump(github.com/openshift/source-to-image):
  64f909fd86e302e5e22a7dd2854278a97ed44cf4 (rhcarvalho@gmail.com)
- Deployment config pipeline must mark the pods it covers (ffranz@redhat.com)
- Revert "Revert "oc status must show monopods"" (ffranz@redhat.com)
- clarify 'oc delete' help info (somalley@redhat.com)
- Add script for vendoring the console repo into bindata.go files
  (jforrest@redhat.com)
- UPSTREAM: 25077: PLEG: reinspect pods that failed prior inspections
  (agoldste@redhat.com)
- Support schema2 of compose, set env vars properly (ccoleman@redhat.com)
- UPSTREAM: 25537: e2e make ForEach fail if filter is empty, fix no-op tests
  (decarr@redhat.com)
- add bash script demonstrating scoped tokens (deads@redhat.com)
- platformmanagement_public_704: Added basic auditing capabilities
  (maszulik@redhat.com)
- Remove dind hack from kubelet (marun@redhat.com)
- more spots to dump on error deployment logs in extended tests
  (gmontero@redhat.com)
- Truncate build pod label to allowed size (cewong@redhat.com)
- disable gitauth tests (gmontero@redhat.com)
- change BC ICT to automatic=true (more deterministic) (gmontero@redhat.com)
- Add NetworkManager dnsmasq configuration dispatcher (sdodson@redhat.com)
- Remove prompts from commented examples (rhcarvalho@gmail.com)
- db-templates: mongodb ephemeral dc should automatically resolve
  (mkargaki@redhat.com)
- UPSTREAM: 25501: SplitHostPort is needed since Request.RemoteAddr has the
  host:port format (maszulik@redhat.com)
- workaround to infinite wait on service in k8s utils; better deployment
  failure test diag (gmontero@redhat.com)
- provide a way to request escalating scopes (deads@redhat.com)
- prevent escalating resource access by default (deads@redhat.com)
- Fixing test flake for docker builds (bleanhar@redhat.com)
- Delete registry interfaces for clusternetwork/hostsubnet/netnamespace
  resources (rpenta@redhat.com)
- Refactored Bash scripts to use new preable for imports (skuznets@redhat.com)
- Declared all Bash library functions read-only. (skuznets@redhat.com)
- Implemented a single-directive library import for Origin Bash scripts
  (skuznets@redhat.com)
- Updated the function declaration syle in existing Bash libararies.
  (skuznets@redhat.com)
- migrate use of s.DefaultConvert to autoConvert (gmontero@redhat.com)
- UPSTREAM: 25472: tolerate nil error in HandleError (deads@redhat.com)
- Check for pod creation in scc exec admission (jliggitt@redhat.com)
- enforce scc during pod updates (deads@redhat.com)
- update jenkins example readme to leverage -z option on oc policy
  (gmontero@redhat.com)
- fix nil ImageChange conversion (gmontero@redhat.com)
- Interrupting a dockerbuild command should clean up leftovers
  (ccoleman@redhat.com)
- When building oc from build-*-images, use found path (ccoleman@redhat.com)
- Bug 1329138: stop emitting events on update conflicts (mkargaki@redhat.com)
- add istag to oc debug (deads@redhat.com)
- add scoped impersonation (deads@redhat.com)
- add service serving cert controller (deads@redhat.com)
- Show/Edit runPolicy (jhadvig@redhat.com)
- add descriptions for scopes (deads@redhat.com)
- add scope validation to tokens (deads@redhat.com)
- Pre-skip some GCE/AWS-only extended networking tests (danw@redhat.com)
- Reorganize extended network tests to save a bit of time (danw@redhat.com)
- bump(k8s.io/kubernetes): c2cc7fd2eafe14472098737b2c255ce4ca06d987
  (mfojtik@redhat.com)
- Add a Docker compose import and command (ccoleman@redhat.com)
- Ignore govet errors on ./third_party (ccoleman@redhat.com)
- UPSTREAM: 25018: Don't convert objects in the destination version
  (ccoleman@redhat.com)
- UPSTREAM: 24390: []byte conversion is not correct (ccoleman@redhat.com)
- bump(third_party/github.com/docker/libcompose):3ca15215f36154fbf64f15bfa305bf
  b0cebb6ca7 (ccoleman@redhat.com)
- bump(github.com/flynn/go-shlex):3f9db97f856818214da2e1057f8ad84803971cff
  (ccoleman@redhat.com)
- Add defensive if statements to valuesIn and valuesNotIn filters
  (admin@benjaminapetersen.me)
- UPSTREAM: 25369: Return 'too old' errors from watch cache via watch stream
  (jliggitt@redhat.com)
- add scope authorizer (deads@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  0fbae3c75c6802a5f5d7fe48d562856443457f6a (dcbw@redhat.com)
- Update for split-out openshift-sdn proxy plugin (dcbw@redhat.com)
- oc: update rollback example (mkargaki@redhat.com)
- Remove gaps from build chart for deleted builds (spadgett@redhat.com)
- Fix jshint warnings (spadgett@redhat.com)
- Changes to markup and the logo so that it isn't clipped at certain dimensions
  - Fixes bug 1328016 - CSS changes to enable logos of varing dimensions within
  the following sizes - Logo max width 230px / height 36px
  (sgoodwin@redhat.com)
- UPSTREAM: 23574: add user.Info.GetExtra (deads@redhat.com)
- Test path-based routing via HTTPS and WebSockets (elyscape@gmail.com)
- cluster quota options (deads@redhat.com)
- Include ext-searchbox.js for Ace editor search (spadgett@redhat.com)
- deployapi: add separate call for updating DC status (mkargaki@redhat.com)
- deployapi: add generation numbers (mkargaki@redhat.com)
- Bug 1333300 - add/update resource labels and annotations (jhadvig@redhat.com)
- Bug 1333669 - error msg when unknown apiVersion or kind (jhadvig@redhat.com)
- Calculate effective limit min in UI for request/limit ratio
  (spadgett@redhat.com)
- Bug 1333651 - set object group and version (jhadvig@redhat.com)
- haproxy Cookie id leaks information about software (pcameron@redhat.com)
- Project should not fetch client immediately (ccoleman@redhat.com)
- put new quota size in extended test (gmontero@redhat.com)
- Remove deployments resource from roles (jliggitt@redhat.com)
- dockerbuild: stop container before committing it (cewong@redhat.com)
- refactor webhook code (bparees@redhat.com)
- Add reconcile protection for roles (jliggitt@redhat.com)
- more catching of build errors, dump of logs, etc.; add registry pod disk
  usage analysis (gmontero@redhat.com)
- Remove sudo call from hack/test-cmd.sh (jliggitt@redhat.com)
- Omit needless reconciles (jliggitt@redhat.com)
- allow project request limits on system users and service accounts
  (deads@redhat.com)
- Allow pulling base image by default in dockerbuild (mfojtik@redhat.com)
- Store author when using MAINTAINER instruction (mfojtik@redhat.com)
- Show newlines and links in template descriptions (spadgett@redhat.com)
- Display FROM instruction (mfojtik@redhat.com)
- Disable UI scaling for in progress deployment (spadgett@redhat.com)
- Bug fix to remove empty <tbody> results in Firefox border rendering bug
  (rhamilto@redhat.com)
- refactor webhooks to account for multiple sources (ipalade@redhat.com)
- point users to the jenkins tutorial from the template (bparees@redhat.com)
- add oc create dc (deads@redhat.com)
- put the git ls-remote "--head" argument in the right order (before the url)
  (bparees@redhat.com)
- Exclude type fields from conversion (ccoleman@redhat.com)
- Regenerate image api deep copies (ccoleman@redhat.com)
- Don't use external types in our serialized structs (ccoleman@redhat.com)
- Regenerated copies and conversions (ccoleman@redhat.com)
- Switch to upstream generators (ccoleman@redhat.com)
- UPSTREAM: 25033: Make conversion gen downstream consumable
  (ccoleman@redhat.com)
- Add support for resource owner password grant (jliggitt@redhat.com)
- Fix timing issue scaling deployments (spadgett@redhat.com)
- UPSTREAM: 24924: fix PrepareForUpdate bug for HPA (jliggitt@redhat.com)
- UPSTREAM: 24924: fix PrepareForUpdate bug for PV and PVC
  (jliggitt@redhat.com)
- Use copy-to-clipboard for next steps webhook URL (spadgett@redhat.com)
- BZ 1332876 - Break long Git source URL (jhadvig@redhat.com)
- stop resending modifies with same project resourceversion for watch
  (deads@redhat.com)
- Allow network test runner to use kubeconfig (marun@redhat.com)
- Replace mongostat with mongo in mongodb example template (mfojtik@redhat.com)
- Fix a problem with ignored Dockerfiles in db conformance
  (ccoleman@redhat.com)
- Add tests and properly handle directory merging (ccoleman@redhat.com)
- Return error from exec (ccoleman@redhat.com)
- update to match s2i type renames (bparees@redhat.com)
- bump(github.com/RangelReale/osincli):
  05659f31e8b694f522f44226839a66bd8b7c08cct (jliggitt@redhat.com)
- support project watch resourceversion=0 (deads@redhat.com)
- bump(github.com/openshift/source-to-image):
  c99ef8b29e94bdaf62d5d5aefa74d12af6d37e3c (bparees@redhat.com)
- Increase initialDelay for Jenkins livenessprobe (mfojtik@redhat.com)
- add configmap to oc set volume (deads@redhat.com)
- Add extended network tests for default namespace non-isolation
  (danw@redhat.com)
- bump(github.com/openshift/source-to-image):
  528d0e97ac38354621520890878d7ea34451384b (bparees@redhat.com)
- Update data.js to support fieldSelector & labelSelector
  (admin@benjaminapetersen.me)
- BZ 1332787 Cannot create resources defined in List through From File option
  on create page (jhadvig@redhat.com)
- Skip pulp test in integration (ccoleman@redhat.com)
- Add output logging to docker build and correctly pull (ccoleman@redhat.com)
- Enable recursion by default for start commands (ccoleman@redhat.com)
- DNS resolution must return etcd name errors (ccoleman@redhat.com)
- Add DNS to the conformance suite (ccoleman@redhat.com)
- Add expanded DNS e2e tests for Origin (ccoleman@redhat.com)
- UPSTREAM: 24128: Allow cluster DNS verification to be overriden
  (ccoleman@redhat.com)
- Additional web console updates for JenkinsPipeline strategy
  (spadgett@redhat.com)
- Reverting mountPath validation for add to allow overwriting volume without
  specifying mountPath (ewolinet@redhat.com)
- Remove moment timezone (jliggitt@redhat.com)
- Add the ability to configure an HAPROXY router to send log messages to a
  syslog address (jtanenba@redhat.com)
- [RPMS] Improve default permissions (sdodson@redhat.com)
- show pod IP during debug (deads@redhat.com)
- Add the service load balancer controller to Origin (ccoleman@redhat.com)
- Add create helpers for users, identities, and mappings from the CLI
  (jliggitt@redhat.com)
- Update editor mode before checking error annotations (spadgett@redhat.com)
- default the volume type (deads@redhat.com)
- Accessibility: make enter key work when confirming project name
  (spadgett@redhat.com)
- let registry-admin delete his project (deads@redhat.com)
- Upload component during the create flow (jhadvig@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  c709df994a5bbecfa80fae62c20131cd25337b79 (rpenta@redhat.com)
- Improve oc cancel-build command (mfojtik@redhat.com)
- dind: stop attempting to cache images during build (marun@redhat.com)
- added oc status check for hpa missing cpu request (skuznets@redhat.com)
- Fix for issue 8578 involving non-breaking strings. (sgoodwin@redhat.com)
- Update yaml.js to latest, official version (spadgett@redhat.com)
- add what-can-i-do endpoint (deads@redhat.com)
- Allow to specify the run policy for builds (mfojtik@redhat.com)
- oc: remove dead factory code (mkargaki@redhat.com)
- oc: dont warn for missing istag in case of in-flight build
  (mkargaki@redhat.com)
- Fix openshift-start empty hostname error message (ripcurld.github@gmail.com)
- oc: support multiple resources in rsh (mkargaki@redhat.com)
- UPSTREAM: 23590: kubectl: more sophisticated pod selection for logs and
  attach (mkargaki@redhat.com)
- UPSTREAM: <drop>: watch-based wait utility (mkargaki@redhat.com)
- Fix broken tests, cleanup config (ccoleman@redhat.com)
- UPSTREAM: <carry>: force import ordering for stable codegen
  (deads@redhat.com)
- Instantiate Jenkins when pipeline strategy is created (jimmidyson@gmail.com)
- Add JenkinsPipeline build strategy (jimmidyson@gmail.com)
- Review 1 (ccoleman@redhat.com)
- Change hack to use direct docker build (ccoleman@redhat.com)
- Flexible dockerfile builder that uses client calls (ccoleman@redhat.com)
- Increase default web console line limit to 5000 (spadgett@redhat.com)
- Allow parameters on generic webhook build trigger call (gmontero@redhat.com)
- prevent s2i from running onbuild images (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  849ad2f6204f7bc0c3522fc59ec4d3c6d653db7c (bparees@redhat.com)
- Enable the gcs, oss, and inmemory storage drivers in registry
  (ccoleman@redhat.com)
- Fix bootstrap package name spelling (cewong@redhat.com)
- make project cache watchable (deads@redhat.com)
- setup default impersonation rules (deads@redhat.com)
- blacklist the ThirdPartyResource kind from other resources page
  (jforrest@redhat.com)
- Do not stop tests (agladkov@redhat.com)
- Generate bindata for bootstrap streams, templates and quickstarts
  (cewong@redhat.com)
- Template parameters broken in new-app (ccoleman@redhat.com)
- integration tests: wait for admission control cache to allow pod creation
  (cewong@redhat.com)
- [RPMS] Get rid of openshift-recycle subpackage (#18) (sdodson@redhat.com)
- [RPMS] Add openshift-recycle (#17) (sdodson@redhat.com)
- bump(k8s.io/kubernetes): 61d1935e4fbaf5b9dd43ebd491dd33fa0aeb48a0
  (deads@redhat.com)
- UPSTREAM: 24839: Validate deletion timestamp doesn't change on update
  (jliggitt@redhat.com)
- add acting-as request handling (deads@redhat.com)
- Handle null items array from bad api responses (jforrest@redhat.com)
- UPSTREAM: 23549: add act-as powers (deads@redhat.com)
- Use git shallow clone when not using ref (mfojtik@redhat.com)
- Correctly use netcat (ccoleman@redhat.com)
- Add lsof (ccoleman@redhat.com)
- Label and streamline the remaining images (ccoleman@redhat.com)
- Simplify the router and ipfailover images (ccoleman@redhat.com)
- Move recycler into origin binary (ccoleman@redhat.com)
- UPSTREAM: 24052: Rate limiting requeue (deads@redhat.com)
- UPSTREAM: 23444: add a delayed queueing option to the workqueue
  (deads@redhat.com)
- add default resource requests to router creation (jtanenba@redhat.com)
- bump(github.com/openshift/source-to-image):
  caa5fed4d6c38041ec1396661b66faff4eff358d (bparees@redhat.com)
- Increase deployment test fixture timeout (ironcladlou@gmail.com)
- remove admission plugins from chain when they have an nil config
  (deads@redhat.com)
- UPSTREAM: 24421: remove admission plugins from chain (deads@redhat.com)
- Refactors to generation in preparation for compose (ccoleman@redhat.com)
- Add openshift.io/deployer-pod.type label (agladkov@redhat.com)
- fix godeps (bparees@redhat.com)
- remove describe user function (ipalade@redhat.com)
- Update integration tests to confirm project name when deleting
  (spadgett@redhat.com)
- remove old double escape validation (pweil@redhat.com)
- Make --insecure flag take precedence over insecure annotation
  (maszulik@redhat.com)
- introduce --watch capability for oc rsync (bparees@redhat.com)
- bump(github.com/fsnotify/fsnotify): 3c39c22b2c7b0516d5f2553f1608e5d13cb19053
  (bparees@redhat.com)
- Read insecure annotation on an image stream when import-image is invoked.
  (maszulik@redhat.com)
- Remove port from request's Host header (elyscape@gmail.com)
- Fix failing application generator test (spadgett@redhat.com)
- warn if image is not a builder, even if it came from source detection
  (bparees@redhat.com)
- Bindata for the console 1.3 changes to date and fixes to spec tests
  (jforrest@redhat.com)
- Make bulk output more centralized (ccoleman@redhat.com)
- Refer SDN plugin names by constants (rpenta@redhat.com)
- fix bad tabbing in template (bparees@redhat.com)
- Fixes to bower after rebase (jforrest@redhat.com)
- Project list add user to role message shouldnt hardcode admin role
  (jforrest@redhat.com)
- Don't validate limit against request limit range default
  (spadgett@redhat.com)
- Trigger login flow if api discovery failed because of possible cert errors
  (jforrest@redhat.com)
- Changing notifications to alerts (rhamilto@redhat.com)
- Lock matchHeight and temporarily add resolution to fix jenkins issue
  (jforrest@redhat.com)
- Tolarate no input buildConfig in console (jhadvig@redhat.com)
- Web console support for JenkinsPipeline builds (spadgett@redhat.com)
- Enabling WebHooks from console will add Generic webhook (jhadvig@redhat.com)
- Add an 'Other resources' page to view, raw edit, and delete other stuff in
  your project (jforrest@redhat.com)
- Changing copy to clipboard button to an input + button (rhamilto@redhat.com)
- Confirm project delete by typing project name (spadgett@redhat.com)
- Update humanizeKind filter to use lowercase by default (spadgett@redhat.com)
- Edit routes in web console (spadgett@redhat.com)
- API discovery in the console (jforrest@redhat.com)
- Reintroduce :empty selector to hide online extensions but adds as a util
  class in _util.scss (admin@benjaminapetersen.me)
- Handle multiline command arguments in web console (spadgett@redhat.com)
- Update nav-mobile-dropdown to use new extension-point, eliminate hawtio-
  extension (admin@benjaminapetersen.me)
- Metrics updates (spadgett@redhat.com)
- Fix usage rate calculation for network metrics in pod page
  (ffranz@redhat.com)
- Fix httpGet path in pod template (spadgett@redhat.com)
- Warn users when navigating away with the terminal window open
  (spadgett@redhat.com)
- Add network metrics to pod page on console (ffranz@redhat.com)
- Fix UI e2e test failure (spadgett@redhat.com)
- Add _spacers.less to generate pad/mar utility classes
  (admin@benjaminapetersen.me)
- Add container entrypoint to debug dialog (spadgett@redhat.com)
- Web console: debug terminal for crashing pods (spadgett@redhat.com)
- Exclude google-code-prettify (spadgett@redhat.com)
- Left align tabs when they wrap to second line (spadgett@redhat.com)
- DataService._urlForResource should return a string (spadgett@redhat.com)
- Fix jshint warnings (spadgett@redhat.com)
- Update grunt-contrib-jshintrc to 1.0.0 (spadgett@redhat.com)
- Fix failing web console unit tests (spadgett@redhat.com)
- Web console support for health checks (spadgett@redhat.com)
- Update online extensions, avoid rendering emtpy DOM nodes
  (admin@benjaminapetersen.me)
- Use hawtioPluginLoader to load javaLinkExtension (admin@benjaminapetersen.me)
- Support autoscaling in the web console (spadgett@redhat.com)
- Update extension points from hawtio manager to angular-extension-registry
  (admin@benjaminapetersen.me)
- Don't enable editor save button until after a change (spadgett@redhat.com)
- Improving pod-template visualization (rhamilto@redhat.com)
- Use @dl-horizontal-breakpoint (spadgett@redhat.com)
- Update Patternfly utilization chart class name (spadgett@redhat.com)
- Updating PatternFly and Angular-PatternFly to v3.3.0 (rhamilto@redhat.com)
- Remove angular-patternfly utilization card dependency (spadgett@redhat.com)
- tests: Bind DNS only to API_HOST address (sgallagh@redhat.com)
- Add mount debug information for cpu quota test flake (mrunalp@gmail.com)
- Handle client-side errors on debug pod creation (ffranz@redhat.com)
- make new project wait for rolebinding cache before returning
  (deads@redhat.com)
- cite potential builds for oc status missing input streams
  (gmontero@redhat.com)
- allow for no build config source input (defer assemble script or custom
  builder) (gmontero@redhat.com)
- add oc create policybinding (deads@redhat.com)
- wait for authorization cache to update before pruning (deads@redhat.com)
- UPSTREAM: <carry>: add scc to pod describer (screeley@redhat.com)
- add option to reverse buildchains (deads@redhat.com)
- switch new project example repo to one that doesn't need a db
  (bparees@redhat.com)
- fully qualify admission attribute records (deads@redhat.com)
- UPSTREAM: 24601: fully qualify admission resources and kinds
  (deads@redhat.com)
- Update generated public functions (ccoleman@redhat.com)
- Make hand written conversions public (ccoleman@redhat.com)
- do not force drop KILL cap on anyuid SCC (pweil@redhat.com)
- UPSTREAM: 24382: RateLimitedQueue TestTryOrdering could fail under load
  (ccoleman@redhat.com)
- generated files (deads@redhat.com)
- important: etcd initialization change (deads@redhat.com)
- important: previously bugged: authorization adapter (deads@redhat.com)
- fix rebase of limitranger for clusterresourceoverride (lmeyer@redhat.com)
- important: resource enablement (deads@redhat.com)
- disabled kubectl features: third-party resources and recursive directories
  (deads@redhat.com)
- rebase interesting enough to keep diff-able (deads@redhat.com)
- <drop>: disable etcd3 unit tests (deads@redhat.com)
- boring changes (deads@redhat.com)
- UPSTREAM: <drop>: keep old deep copy generator for now (deads@redhat.com)
- UPSTREAM: 24208: Honor starting resourceVersion in watch cache
  (agoldste@redhat.com)
- UPSTREAM: 24153: make optional generic etcd fields optional
  (deads@redhat.com)
- UPSTREAM: 23894: Should not fail containers on OOM score adjust
  (ccoleman@redhat.com)
- UPSTREAM: 24048: Use correct defaults when binding apiserver flags
  (jliggitt@redhat.com)
- UPSTREAM: 24008: Make watch cache behave like uncached watch
  (jliggitt@redhat.com)
- UPSTREAM: openshift/openshift-sdn: <drop>: sig changes (deads@redhat.com)
- bump(hashicorp/golang-lru): a0d98a5f288019575c6d1f4bb1573fef2d1fcdc4
  (deads@redhat.com)
- bump(davecgh/go-spew): 5215b55f46b2b919f50a1df0eaa5886afe4e3b3d
  (deads@redhat.com)
- bump(rackspace/gophercloud): 8992d7483a06748dea706e4716d042a4a9e73918
  (deads@redhat.com)
- bump(coreos/etcd): 5e6eb7e19d6385adfabb1f1caea03e732f9348ad
  (deads@redhat.com)
- bump(k8s.io/kubernetes): 61d1935e4fbaf5b9dd43ebd491dd33fa0aeb48a0
  (deads@redhat.com)
- pass args to bump describer (deads@redhat.com)
- UPSTREAM: revert: 1f9b8e5: 24008: Make watch cache behave like uncached watch
  (deads@redhat.com)
- UPSTREAM: revert: c3d1d37: 24048: Use correct defaults when binding apiserver
  flags (deads@redhat.com)
- UPSTREAM: revert: 9ec799d: 23894: Should not fail containers on OOM score
  adjust (deads@redhat.com)
- UPSTREAM: revert: 66d1fdd: 24208: Honor starting resourceVersion in watch
  cache (deads@redhat.com)
- diagnostics: update cmd tests (lmeyer@redhat.com)
- Debug command should default to pods (ccoleman@redhat.com)
- Support --logspec (glog -vmodule) for finegrained logging
  (ccoleman@redhat.com)
- diagnostics: introduce cluster ServiceExternalIPs (lmeyer@redhat.com)
- diagnostics: introduce cluster MetricsApiProxy (lmeyer@redhat.com)
- Output logs on network e2e deployment failure (marun@redhat.com)
- Import from repository doesn't panic (miminar@redhat.com)
- Default role reconciliation to additive-only (jliggitt@redhat.com)
- made commitchecker error statements more verbose (skuznets@redhat.com)
- Remove deprecated --nodes flag (jliggitt@redhat.com)
- Improve logging of missing authorization codes (jliggitt@redhat.com)
- git server: automatically launch builds on push (cewong@redhat.com)
- fix typo in error message (pweil@redhat.com)
- update registry config with deprecated storage.cache.layerinfo, now
  blobdescriptor (aweiteka@redhat.com)
- implemented glog wrapper for use in delegated commands (skuznets@redhat.com)
- UPSTREAM: golang/glog: <carry>: add 'InfoDepth' to 'V' guard
  (skuznets@redhat.com)
- update failure conditions for oc process (skuznets@redhat.com)
- remove unused constant that has been migrated to bootstrappolicy
  (pweil@redhat.com)
- dind: output rc reminder if bin path is not set (marun@redhat.com)
- dind: clean up disabling of sdn node (marun@redhat.com)
- dind: ensure quoting of substitutions (marun@redhat.com)
- dind: use os::build funcs to find binary path (marun@redhat.com)
- dind: ensure all conditionals use [[ (marun@redhat.com)
- least change to stop starting reflector in clusterresourceoverride
  (deads@redhat.com)
- UPSTREAM: 24403: kubectl: use platform-agnostic helper in edit
  (mkargaki@redhat.com)
- Allow new-app params to be templatized (ccoleman@redhat.com)
- Change the context being used when Stat-ing remote registry
  (maszulik@redhat.com)
- Revert SDN bridge-nf-call-iptables=0 hack (dcbw@redhat.com)
- Update README.md (brian.christner@gmail.com)
- add labels and annotations from buildrequest to resulting build
  (bparees@redhat.com)
- Don't close the "lost" channel more than once (ccoleman@redhat.com)
- Expose Watch in the Users client API (v.behar@free.fr)
- Expose Watch in the Groups client API (v.behar@free.fr)
- oc: fix help message for deploy (mkargaki@redhat.com)
- Disable serial image pulls by default (avagarwa@redhat.com)
- docs: add irc badge (jsvgoncalves@gmail.com)
- improve systemd unit ordering (jdetiber@redhat.com)
- F5: handle HTML responses gracefully (miciah.masters@gmail.com)
- correct precision in the no config file message (jay@apache.org)

* Mon Jun 20 2016 Scott Dodson <sdodson@redhat.com> 3.2.1.3
- add mutation cache (deads@redhat.com)
- convert dockercfg secret generator to a work queue (deads@redhat.com)
- UPSTREAM: 25091: partial - reduce conflict retries (deads@redhat.com)
- Add bindata.go to pick up changes merged in
  https://github.com/openshift/ose/pull/213 which addressed bug 1328016.
  (sgoodwin@redhat.com)

* Tue Jun 14 2016 Scott Dodson <sdodson@redhat.com> 3.2.1.2
- UPSTREAM: 27227: Counting pod volume towards PV limit even if PV/PVC is
  missing (abhgupta@redhat.com)
- UPSTREAM 22568: Considering all nodes for the scheduler cache to allow
  lookups (abhgupta@redhat.com)
- Use our golang-1.4 build image in OSE (ccoleman@redhat.com)
- Add a GCS test to verify it is compiled in (ccoleman@redhat.com)
- Build dockerregistry with tag `include_gcs` (ccoleman@redhat.com)
- UPSTREAM: docker/distribution: <carry>: Distribution dependencies
  (ccoleman@redhat.com)
- Upstream PR8615 - haproxy Cookie id leaks info (pcameron@redhat.com)

* Sat Jun 04 2016 Scott Dodson <sdodson@redhat.com> 3.2.1.1
- UPSTREAM 8287 Suppress router reload during sync (marun@redhat.com)
- UPSTREAM 8893 Sync access to router state (smitram@gmail.com)
- UPSTREAM: 25487: pod constraints func for quota validates resources
  (decarr@redhat.com)
- UPSTREAM: 24514: Quota ignores pod compute resources on updates
  (decarr@redhat.com)
- Skip registry client v1 and v2 tests until we push with 1.10
  (ccoleman@redhat.com)
- Allow size of image to be zero when schema1 from Hub (ccoleman@redhat.com)
- UPSTREAM: 25161: Sort resources in quota errors to avoid duplicate events
  (decarr@redhat.com)
- Bug 1342091 - Add additional interfaces implementation for handling watches,
  rsh, etc. (maszulik@redhat.com)
- Add watch caching to origin types (jliggitt@redhat.com)
- Fix login redirect (spadgett@redhat.com)
- UPSTREAM: 24403: kubectl: use platform-agnostic helper in edit
  (mkargaki@redhat.com)
- Backport bug #1333118: adding labels and envs is tricky
  (admin@benjaminapetersen.me)
- Document things, remove /usr/bin/docker mount from contrib systemd unit
  (sdodson@redhat.com)
- chroot docker to the rootfs (sdodson@redhat.com)
- Truncate labels of builds generated from a BuildConfig (cewong@redhat.com)
- Truncate build pod label to allowed size (cewong@redhat.com)
- Service account token controller startup change (jliggitt@redhat.com)
- [RPMs] Refactor golang BuildRequires (sdodson@redhat.com)
- UPSTREAM: 23858: Convert service account token controller to use a work queue
  (jliggitt@redhat.com)
- UPSTREAM: 24052: add built-in ratelimiter to workqueue (deads@redhat.com)
- UPSTREAM: 23444: fake util.clock tick (jliggitt@redhat.com)
- UPSTREAM: 23444: make delayed workqueue use channels with single writer
  (jliggitt@redhat.com)
- UPSTREAM: 23444: add a delayed queueing option to the workqueue
  (deads@redhat.com)
- Fix extended validation test expected error count. Probably needs to do error
  check rather than exact error count match. (smitram@gmail.com)
-   o Add basic validation for route TLS configuration - checks that     input
  is "syntactically" valid.   o Checkpoint initial code.   o Add support for
  validating route tls config.   o Add option for validating route tls config.
  o Validation fixes.   o Check private key + cert mismatches.   o Add tests.
  o Record route rejection.   o Hook into add route processing + store invalid
  service alias configs     in another place - easy to check prior errors on
  readmission.   o Remove entry from invalid service alias configs upon route
  removal.   o Add generated completions.   o Bug fixes.   o Recording
  rejecting routes is not working completely.   o Fix status update problem -
  we should set the status to admitted     only if we had no errors handling a
  route.   o Rework to use a new controller - extended_validator as per
  @smarterclayton comments.   o Cleanup validation as per @liggitt comments.
  o Update bash completions.   o Fixup older validation unit tests.   o Changes
  as per @liggitt review comments + cleanup tests.   o Fix failing test.
  (smitram@gmail.com)
- Bug 1334485 - Empty overview page (jhadvig@redhat.com)
- UPSTREAM: 25907: Fix detection of docker cgroup on RHEL (agoldste@redhat.com)
- UPSTREAM: 25472: tolerate nil error in HandleError (deads@redhat.com)
- UPSTREAM: 25690: Fixes panic on round tripper when TLS under a proxy
  (ffranz@redhat.com)
- platformmanagement_public_704: Added basic auditing (maszulik@redhat.com)
- Bug 1333118 - Make for CLI tools a standalone help page (jhadvig@redhat.com)
- allow project request limits on system users and service accounts
  (deads@redhat.com)
- Bug 1333172 - differ between route hostname and navigation within the console
  (jhadvig@redhat.com)
- Updating Help > Documentation links to use helpLink filter
  (rhamilto@redhat.com)
- UPSTREAM: 25501: SplitHostPort is needed since Request.RemoteAddr has the
  host:port format (maszulik@redhat.com)
- Remove gaps from build chart for deleted builds (spadgett@redhat.com)
- Check for pod creation in scc exec admission (jliggitt@redhat.com)
- Include ext-searchbox.js for Ace editor search (spadgett@redhat.com)
- UPSTREAM: 25369: Return 'too old' errors from watch cache via watch stream
  (jliggitt@redhat.com)
- Update logo and support css structure to enable a more flexible dimensions
  (sgoodwin@redhat.com)
- Calculate effective limit min in UI for request/limit ratio
  (spadgett@redhat.com)
- Disable UI scaling for in progress deployment (spadgett@redhat.com)
- Fix timing issue scaling deployments (spadgett@redhat.com)
- Show newlines and links in template descriptions (spadgett@redhat.com)
- UPSTREAM: 25077: PLEG: reinspect pods that failed prior inspections
  (agoldste@redhat.com)
- Update spec to 4.2.1 (tdawson@redhat.com)

* Thu May 05 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.42
- UPSTREAM: 24924: fix PrepareForUpdate bug for HPA (jliggitt@redhat.com)
- UPSTREAM: 24924: fix PrepareForUpdate bug for PV and PVC
  (jliggitt@redhat.com)
- enforce scc during pod updates (deads@redhat.com)
- bump(github.com/openshift/source-to-image):
  528d0e97ac38354621520890878d7ea34451384b (bparees@redhat.com)
- bump(github.com/openshift/source-to-image):
  849ad2f6204f7bc0c3522fc59ec4d3c6d653db7c (bparees@redhat.com)
- prevent s2i from running onbuild images (bparees@redhat.com)

* Tue May 03 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.41
- UPSTREAM: 24933: Validate deletion timestamp doesn't change on update
  (jliggitt@redhat.com)
- policy unsafe proxy requests separately (jliggitt@redhat.com)
- Add login csrf prompts (jliggitt@redhat.com)
- Enable the gcs, oss, and inmemory storage drivers in registry
  (ccoleman@redhat.com)
- Limit queryparam auth to websockets (jliggitt@redhat.com)
- Web console: don't validate limit against request default
  (spadgett@redhat.com)
- Bug 1330364 - add user to role message has 'admin' role hardcoded, should
  just have a placeholder (jforrest@redhat.com)

* Tue Apr 26 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.40
- Update version for first hotfix (tdawson@redhat.com)
- Merge pull request #184 from ironcladlou/deployment-quota-fix
   Prevent deployer pod creation conflicts

* Mon Apr 25 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.20
- bump(github.com/openshift/openshift-sdn)
  ba3087afd66cce7c7d918af10ad91197f8dfd74f (rpenta@redhat.com)
- Open() is called in the pullthrough code path and needs retry
  (ccoleman@redhat.com)
- Improve parsing of semantic version for git tag (ccoleman@redhat.com)
- Prevent deployer pod creation conflicts (ironcladlou@gmail.com)
- Wait until user has access to project in extended (ccoleman@redhat.com)
- Retry 401 unauthorized responses from registries within a window
  (ccoleman@redhat.com)

* Fri Apr 22 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.19
- Support extracting release binaries on other platforms (ccoleman@redhat.com)
- When Kube and Origin version are the same, skip test (ccoleman@redhat.com)
- All image references should be using full semantic version
  (ccoleman@redhat.com)
- Simplified and extended jobs tests (maszulik@redhat.com)
- debug for ext test failures on jenkins (gmontero@redhat.com)
- Fix branding in html title for oauth pages (jforrest@redhat.com)
- force pull fixes / debug (gmontero@redhat.com)
- Make /etc/origin /etc/origin/master /etc/origin/node 0700
  (sdodson@redhat.com)

* Wed Apr 20 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.18
- Revert "Retry import to the docker hub on 401" (ccoleman@redhat.com)
- debug for failures on jenkins (gmontero@redhat.com)
- Change the context being used when Stat-ing remote registry
  (maszulik@redhat.com)
- Update 1 - run to the entire interval (ccoleman@redhat.com)
- Retry 401 unauthorized responses from registries within a window
  (ccoleman@redhat.com)
- Exclude deployment tests and set a perf test to serial (ccoleman@redhat.com)
- Add client debugging for legacy dockerregistry code (ccoleman@redhat.com)
- moved jUnit report for test-cmd to be consistent (skuznets@redhat.com)
- remove trailing = from set trigger example (bparees@redhat.com)
- haproxy obfuscated internal IP in routing cookie (pcameron@redhat.com)
- Example CLI command (ccoleman@redhat.com)
- Add summary status message to network test runner (marun@redhat.com)
- dind: Clean up check for ready nodes (marun@redhat.com)
- Fix precision of cpu to millicore and memory to bytes (decarr@redhat.com)
- UPSTREAM: 23435: Fixed mounting with containerized kubelet
  (jsafrane@redhat.com)

* Mon Apr 18 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.17
- Revert "oc status must show monopods" (ccoleman@redhat.com)
- Refactor build strategy permissions into distinct roles (jliggitt@redhat.com)
- Cleanup network test runner's use of conditionals (marun@redhat.com)
- Copy config to dev cluster master's local storage (marun@redhat.com)
- Cleanup network test runner error handling (marun@redhat.com)
- Minimize image builds by the network test runner (marun@redhat.com)
- Improve network test runner error handling (marun@redhat.com)
- Reduce log verbosity of network test runner (marun@redhat.com)
- Remove redundant extended networking sanity tests (marun@redhat.com)
- [RPMS] Switch requires from docker-io to docker (sdodson@redhat.com)
- extended: Allow to focus on particular tests (miminar@redhat.com)
- Ensure stable route admission (marun@redhat.com)
- Added provisioning flag and refactored VolumeConfig struct names
  (mturansk@redhat.com)
- UPSTREAM: 23793: Make ConfigMap volume readable as non-root
  (pmorie@gmail.com)
- added jUnit XML publishing step to exit trap (skuznets@redhat.com)
- added support for os::cmd parsing to junitreport (skuznets@redhat.com)
- refactored nested suites builder (skuznets@redhat.com)
- configure test-cmd to emit parsable output for jUnit (skuznets@redhat.com)

* Fri Apr 15 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.16
- UPSTREAM: 24208: Honor starting resourceVersion in watch cache
  (agoldste@redhat.com)
- Abuse deployments with extended test (ccoleman@redhat.com)
- dind: only wait for Ready non-sdn nodes (marun@redhat.com)
- UPSTREAM: 23769: Ensure volume GetCloudProvider code uses cloud config
  (jliggitt@redhat.com)
- UPSTREAM: 21140: e2e test for dynamic provisioning. (jliggitt@redhat.com)
- UPSTREAM: 23463: add an event for when a daemonset can't place a pod due to
  insufficent resource or port conflict (jliggitt@redhat.com)
- UPSTREAM: 23929: only include running and pending pods in daemonset should
  place calculation (jliggitt@redhat.com)
- Update font-awesome bower dependency (spadgett@redhat.com)
- Fix unit tests (ironcladlou@gmail.com)
- Prevent concurrent deployer pod creation (ironcladlou@gmail.com)
- Enforce overview scaling rules for deployments without a service
  (spadgett@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  9f1f60258fcef6f0ef647a75a8754bc80779c065 (rpenta@redhat.com)

* Wed Apr 13 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.15
- Update atomic registry quickstart artifacts (aweiteka@redhat.com)
- UPSTREAM: 23746: A pod never terminated if a container image registry was
  unavailable (agoldste@redhat.com)
- fix push path in log message (bparees@redhat.com)
- Bump fontawesome to 4.6.1 (jforrest@redhat.com)
- Fix bindata diff for new font-awesome release (spadgett@redhat.com)
- Fix e2e scc race (agoldste@redhat.com)
- UPSTREAM: 23894: Should not fail containers on OOM score adjust
  (ccoleman@redhat.com)
- Add ability to specify allowed CNs for RequestHeader proxy client cert
  (jliggitt@redhat.com)
- bump(k8s.io/kubernetes): 114a51dfbc43a8bcf07db1774a20e05d560e34b0
  (deads@redhat.com)
- Update ose image build scripts (tdawson@redhat.com)
- Modify pullthrough import-image use case to use our cli framework
  (maszulik@redhat.com)
- add system:image-auditor (deads@redhat.com)
- Improve wording in sample-app README (rhcarvalho@gmail.com)
- Wrap login requests to clear in-memory session (jliggitt@redhat.com)
- Grant use of the NFS plugin in hostmount-anyuid SCC, to enable NFS recycler
  pods to run (pmorie@gmail.com)
- made hack/test-go handle compilation errors better (skuznets@redhat.com)
- Enable etcd cache for k8s resources (jliggitt@redhat.com)
- UPSTREAM: 24048: Use correct defaults when binding apiserver flags
  (jliggitt@redhat.com)
- UPSTREAM: 24008: Make watch cache behave like uncached watch
  (jliggitt@redhat.com)

* Mon Apr 11 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.14
- deployer controller: ensure phase direction (mkargaki@redhat.com)
- Getting docker logs always to debug issue 8399 (maszulik@redhat.com)
- deployment controller: cancel deployers on new cancelled deployments
  (mkargaki@redhat.com)
- Bug 1324437: show cancel as subordinate to non-terminating phases
  (mkargaki@redhat.com)

* Fri Apr 08 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.13
- Travis can't install go vet anymore (ccoleman@redhat.com)
- Add debugs for CPU Quota flake (mrunalp@gmail.com)
- Getting docker logs always to debug issue 8399 (maszulik@redhat.com)
- ProjectRequestLimit plugin: ignore projects in terminating state
  (cewong@redhat.com)
- Support focus arguments on both conformance and core (ccoleman@redhat.com)
- BZ_1324273: Make BC edit form dirty when deleting Key-Value pair
  (jhadvig@redhat.com)
- Add a conformance test for extended (ccoleman@redhat.com)
- Always set the Cmd for source Docker image (mfojtik@redhat.com)
- stylistic/refactoring changes for test/extended/cmd to use os::cmd
  (skuznets@redhat.com)
- UPSTREAM: 23445: Update port forward e2e for go 1.6 (agoldste@redhat.com)
- Naming inconsistancy fix (jhadvig@redhat.com)
- install iproute since the origin-base image dose not contain ip command
  (bmeng@redhat.com)
- Change RunOnce duration plugin to act as a limit instead of override
  (cewong@redhat.com)
- Error on node startup using perFSGroup quota, but fs mounted with noquota.
  (dgoodwin@redhat.com)
- remove running containers in case of a sigterm (bparees@redhat.com)
- Add mounting volumes to privileged pods template (jcope@redhat.com)
- oc describe build: improve output. (vsemushi@redhat.com)

* Wed Apr 06 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.12
- Make infra and shared resource namespaces immortal (jliggitt@redhat.com)
- UPSTREAM: 23883: Externalize immortal namespaces (jliggitt@redhat.com)
- add conformance tag to some extended build tests (bparees@redhat.com)
- add slow tag to jenkins plugin extended test (gmontero@redhat.com)
- Bug 1323710: fix deploy --cancel message on subsequent calls
  (mkargaki@redhat.com)
- UPSTREAM: 23548: Check claimRef UID when processing a recycled PV, take 2
  (swagiaal@redhat.com)
- Updates to the 503 application unavailable page. (sgoodwin@redhat.com)
- Improve display of logs in web console (spadgett@redhat.com)
- bump(github.com/openshift/source-to-image):
  641b22d0a5e7a77f7dab2b1e75f563ba59a4ec96 (rhcarvalho@gmail.com)
- elevate privilegs when removing etcd binary store (skuznets@redhat.com)
- UPSTREAM: 23078: Check claimRef UID when processing a recycled PV
  (swagiaal@redhat.com)

* Mon Apr 04 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.11
- Show pulling / terminated status in pods donut (spadgett@redhat.com)
- Update the postCommit hook godoc to reflect API (ccoleman@redhat.com)
- do not error on adding app label to objects if it exists (bparees@redhat.com)
- Add the openshift/origin-egress-router image (danw@redhat.com)
- remove credentials arg (aweiteka@redhat.com)
- remove atomic registry quickstart from images dir, also hack test script
  (aweiteka@redhat.com)
- Retry when receiving an imagestreamtag not found error (ccoleman@redhat.com)

* Fri Apr 01 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.10
- Allow multiple routers to update route status (sross@redhat.com)
- change default volume size (gmontero@redhat.com)
- Bug 1322587 - NotFound error (404) when deleting layers is logged but we'll
  be continuing the execution. (maszulik@redhat.com)
- Separate out new-app code for reuse (ccoleman@redhat.com)
- Refactor new app and new build to use options struct (ccoleman@redhat.com)
- use restart sec to avoid default rate limit (pweil@redhat.com)
- Refactor start-build to use options style (ccoleman@redhat.com)
- Tolerate local Git repositories without an origin set (ccoleman@redhat.com)
- Add unique suffix to build post-hook containers (rhcarvalho@gmail.com)
- The router command should keep support for hostPort (ccoleman@redhat.com)
- UPSTREAM: 23586: don't sync deployment when pod selector is empty
  (jliggitt@redhat.com)
- UPSTREAM: 23586: validate that daemonsets don't have empty selectors on
  creation (jliggitt@redhat.com)
- no commit id in img name and add openshift org to image name for openshift-
  pipeline plugin extended test (gmontero@redhat.com)
- Set service account correctly in oadm registry, deprecate --credentials
  (jliggitt@redhat.com)
- Add tests for multiple IDPs (sgallagh@redhat.com)
- Encode provider name when redirecting to login page (jliggitt@redhat.com)
- Allow multiple web login methods (sgallagh@redhat.com)
- allow pvc by default (pweil@redhat.com)
- UPSTREAM: 23007: Kubectl shouldn't print throttling debug output
  (jliggitt@redhat.com)
- Resolve api groups in resolveresource (jliggitt@redhat.com)
- Improve provider selection page (jliggitt@redhat.com)
- fix a forgotten modification : 'sti->s2i' (qilin.wang@huawei.com)
- sort volumes for reconciliation (pweil@redhat.com)
- Set charset with content type (jliggitt@redhat.com)
- Bug 1318920: emit events for failed cancellations (mkargaki@redhat.com)
- UPSTREAM: 22525: Add e2e for remaining quota resources (decarr@redhat.com)
- remove test file cruft (skuznets@redhat.com)

* Wed Mar 30 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.9
- Fixed string formatting for glog.Infof in image prunning
  (maszulik@redhat.com)
- bump(github.com/openshift/source-to-image):
  48e62fd57bebba14e1d0f7a40a15b65dafa5458c (cewong@redhat.com)
- Fix 8162: project settings layout issues (admin@benjaminapetersen.me)
- UPSTREAM: 23456: don't sync daemonsets or controllers with selectors that
  match all pods (jliggitt@redhat.com)
- UPSTREAM: 23457: Do not track resource usage for host path volumes. They can
  contain loops. (jliggitt@redhat.com)
- UPSTREAM: 23325: Fix hairpin mode (jliggitt@redhat.com)
- UPSTREAM: 23019: Add a rate limiter to the GCE cloudprovider
  (jliggitt@redhat.com)
- UPSTREAM: 23141: kubelet: send all recevied pods in one update
  (jliggitt@redhat.com)
- UPSTREAM: 23143: Make kubelet default to 10ms for CPU quota if limit < 10m
  (jliggitt@redhat.com)
- UPSTREAM: 23034: Fix controller-manager race condition issue which cause
  endpoints flush during restart (jliggitt@redhat.com)
- bump inotify watches (jeder@redhat.com)
- Use scale subresource for DC scaling in web console (spadgett@redhat.com)
- Fixing typos (dmcphers@redhat.com)
- Disambiguate origin generators (jliggitt@redhat.com)
- Add explicit emptyDir volumes where possible (ironcladlou@gmail.com)
- Resource discovery integration test (jliggitt@redhat.com)
- UPSTREAM: <carry>: v1beta3: ensure only v1 appears in discovery for legacy
  API group (jliggitt@redhat.com)
- Use strategy proxy setting for script download (cewong@redhat.com)
- bump(github.com/openshift/source-to-image):
  2c0fc8ae6150b27396dc00907cac128eeda99b09 (cewong@redhat.com)
- Deployment tests should really be disabled in e2e (ccoleman@redhat.com)
- fix useragent for SA (deads@redhat.com)
- Fix e2e test's check for determining that the router is up - wait for the
  healthz port to respond with success - HTTP status code 200. Still need to
  check for router pod to be born. (smitram@gmail.com)
- tweak jenkins job to test unrelased versions of the plugin
  (gmontero@redhat.com)
- Fix oadm diagnostic (master-node check for ovs plugin) to retrieve the list
  of nodes running on the same machine as master. (avagarwa@redhat.com)
- scc volumes support (pweil@redhat.com)
- UPSTREAM: <carry>: scc volumes support (pweil@redhat.com)
- UPSTREAM: <carry>: v1beta3 scc volumes support (pweil@redhat.com)
- add volume prereq to db template descriptions (bparees@redhat.com)
- Fix typo (tdawson@redhat.com)
- Verify yum installed rpms (tdawson@redhat.com)

* Mon Mar 28 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.8
- E2e deployments filter is incorrect (ccoleman@redhat.com)
- Reorder the debug pod name (ccoleman@redhat.com)
- use a first class field definition to identify scratch images
  (bparees@redhat.com)
- Remove project admin/edit ability to create daemonsets (jliggitt@redhat.com)
- Bug 1314270: force dc reconcilation on canceled deployments
  (mkargaki@redhat.com)
- controller: refactor deployer controller interfaces (mkargaki@redhat.com)
- cli: oc process should print errors to stderr (stefw@redhat.com)
- use emptydir for sample-app volumes (bparees@redhat.com)
- fix extended cmd.sh to handle faster importer (deads@redhat.com)
- #7976 : Initialize Binary source to an empty default state if type but no
  value set (for API v1) (roland@jolokia.org)
- Atomic registry quickstart image (aweiteka@redhat.com)
- Fix bug where router reload fails to run lsof - insufficient permissions with
  the hostnetwork scc. Reduce the lsof requirement since we now check for error
  codes [non zero means bind errors] and have a healthz check as a sanity
  check. Plus fixes as per @smarterclayton review comments. (smitram@gmail.com)
- Include branded header within <noscript> message. (sgoodwin@redhat.com)
- Better error message when JavaScript is disabled (jawnsy@redhat.com)
- Simplify synthetic skips so that no special chars are needed Isolate the
  package skipping into a single function. (jay@apache.org)
- Fix new-app template search with multiple matches (cewong@redhat.com)
- UPSTREAM: <carry>: Suppress aggressive output of warning
  (ccoleman@redhat.com)
- hardcode build name to expect instead of getting it from start-build output
  (bparees@redhat.com)
- New skips in extended tests (ccoleman@redhat.com)
- removed binary etcd store from test-cmd artfacts (skuznets@redhat.com)
- Fix resolver used for --image-stream param, annotation searcher output
  (cewong@redhat.com)
- UPSTREAM: 23065: Remove gce provider requirements from garbage collector test
  (tiwillia@redhat.com)
- Bindata change for error with quotes on project 404 (jforrest@redhat.com)
- Fixed error with quotes (jlam@snaplogic.com)
- Escape ANSI color codes in web console logs (spadgett@redhat.com)
- refactor to not use dot imports for heredoc (skuznets@redhat.com)
- Bug 1320335: Fix quoting for mysql probes (mfojtik@redhat.com)
- Add client utilities for iSCSI and Ceph. (jsafrane@redhat.com)
- loosen exec to allow SA checks for privileges (deads@redhat.com)
- Allow perFSGroup local quota in config on first node start.
  (dgoodwin@redhat.com)
- use a max value of 92233720368547 for cgroup values (bparees@redhat.com)
- Revert "temporarily disable cgroup limits on builds" (bparees@redhat.com)
- update generated code and docs (pweil@redhat.com)
- UPSTREAM: 22857: partial - ensure DetermineEffectiveSC retains the container
  setting for readonlyrootfs (pweil@redhat.com)
- UPSTREAM: <carry>: v1beta3 scc - read only root file system support
  (pweil@redhat.com)
- UPSTREAM: <carry>: scc - read only root file system support
  (pweil@redhat.com)
- UPSTREAM: 23279: kubectl: enhance podtemplate describer (mkargaki@redhat.com)
- oc: add volume info on the dc describer (mkargaki@redhat.com)
- remove dead cancel code (bparees@redhat.com)
- Enable the pod garbage collector (tiwillia@redhat.com)
- pkg: cmd: cli: cmd: startbuild: close response body (runcom@redhat.com)

* Wed Mar 23 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.7
- Ensure ingress host matches route host (marun@redhat.com)
- Enable extensions storage for batch/autoscaling (jliggitt@redhat.com)
- Add navbar-utility-mobile to error.html Fixes
  https://github.com/openshift/origin/issues/8198 (sgoodwin@redhat.com)
- Add /dev to node volumes (sdodson@redhat.com)
- Install e2fsprogs and xfsprogs into base image (sdodson@redhat.com)
- oc debug is not defaulting to TTY (ccoleman@redhat.com)
- UPSTREAM: revert: d54ed4e: 21373: kubelet: reading cloudinfo from cadvisor
  (deads@redhat.com)
- temporarily disable cgroup limits on builds (bparees@redhat.com)
- test/extended/images/mongodb_replica: add tests for mongodb replication
  (vsemushi@redhat.com)
- oc status must show monopods (ffranz@redhat.com)
- Integration tests should use docker.ClientFromEnv() (ccoleman@redhat.com)
- Move upstream (ccoleman@redhat.com)
- hack/test-cmd.sh races against deployment controller (ccoleman@redhat.com)
- make who-can use resource arg format (deads@redhat.com)
- Bug in Kube API version group ordering (ccoleman@redhat.com)
- Fix precision displaying percentages in quota chart tooltip
  (spadgett@redhat.com)
- updated artifacts to contain docker log and exlucde etcd data dir
  (skuznets@redhat.com)
- Mount /var/log into node container (sdodson@redhat.com)
- Hide extra close buttons for task lists (spadgett@redhat.com)
- Test refactor (ccoleman@redhat.com)
- Disable failing upstream test (ccoleman@redhat.com)
- In the release target, only build linux/amd64 (ccoleman@redhat.com)
- Pod diagnostic check is not correct in go 1.6 (ccoleman@redhat.com)
- Update Dockerfile for origin-release to use Go 1.6 (ccoleman@redhat.com)
- Update build-go.sh to deal with Go 1.6 (ccoleman@redhat.com)
- Suppress Go 1.6 error on -X flag (ccoleman@redhat.com)
- Add RunOnceDuration and ProjectRequestLimit plugins to default plugin chains
  (cewong@redhat.com)
- Add kube component config tests, disable /logs on master, update kube-proxy
  init (jliggitt@redhat.com)
- Adjust -webkit-scrollbar width and log-scroll-top affixed position. Fixes
  https://github.com/openshift/origin/issues/7963 (sgoodwin@redhat.com)

* Mon Mar 21 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.6
- Bug 1318537 - Add warning when trying to import non-existing tag
  (maszulik@redhat.com)
- Bug 1310062 - Fallback to http if status code is not 2xx/3xx when deleting
  layers. (maszulik@redhat.com)
- Log the reload output for admins in the router logs (ccoleman@redhat.com)
- Set terminal max-width to 100%% for mobile (spadgett@redhat.com)
- Hide the java link if the container is not ready (slewis@fusesource.com)
- Support limit quotas and scopes in UI (spadgett@redhat.com)
- Add test for patch+conflicts (jliggitt@redhat.com)
- Removed the stray line that unconditionally forced on the SYN eater.
  (bbennett@redhat.com)
- Remove large, unnecessary margin from bottom of create forms
  (spadgett@redhat.com)
- Use smaller log font size for mobile (spadgett@redhat.com)
- UPSTREAM: 23145: Use versioned object when computing patch
  (jliggitt@redhat.com)
- Handle new volume source types on web console (ffranz@redhat.com)
- Show consistent pod status in web console as CLI (spadgett@redhat.com)
- PVCs should not be editable once bound (ffranz@redhat.com)
- bump(github.com/openshift/source-to-image):
  625b58aa422549df9338fdaced1b9444d2313a15 (rhcarvalho@gmail.com)
- bump(github.com/openshift/openshift-sdn):
  72d9ab84f4bf650d1922174e6a90bd06018003b4 (dcbw@redhat.com)
- Reworked image quota (miminar@redhat.com)
- Fix certificate display on mobile (spadgett@redhat.com)
- Include container ID in glog message (rhcarvalho@gmail.com)
- Ignore default security context constraints when running on kube
  (decarr@redhat.com)
- use transport defaults (deads@redhat.com)
- UPSTREAM: 23003: support CIDRs in NO_PROXY (deads@redhat.com)
- UPSTREAM: 22852: Set a missing namespace on objects to admit
  (miminar@redhat.com)
- Handle fallback to docker.io for 1.9 docker, which uses docker.io in
  .docker/config.json (maszulik@redhat.com)
- Revert "platformmanagement_public_425 - add quota information to oc describe
  is" (miminar@redhat.com)

* Fri Mar 18 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.5
- Don't show chromeless log link if log not available (spadgett@redhat.com)
- UPSTREAM: 21373: kubelet: reading cloudinfo from cadvisor (deads@redhat.com)
- fix typo in db template readme (bparees@redhat.com)
- oc: more status fixes (mkargaki@redhat.com)
- Don't autofocus catalog filter input (spadgett@redhat.com)
- Add e2fsprogs to base image (sdodson@redhat.com)
- Bump kubernetes-container-terminal to 0.0.11 (spadgett@redhat.com)
- oc: plumb error writer in oc edit (mkargaki@redhat.com)
- UPSTREAM: 22634: kubectl: print errors that wont be reloaded in the editor
  (mkargaki@redhat.com)
- Include all extended tests in a single binary (marun@redhat.com)
- Update swagger spec (jliggitt@redhat.com)
- bump(k8s.io/kubernetes): 4a3f9c5b19c7ff804cbc1bf37a15c044ca5d2353
  (jliggitt@redhat.com)
- bump(github.com/google/cadvisor): 546a3771589bdb356777c646c6eca24914fdd48b
  (jliggitt@redhat.com)
- add debug when extended build tests fail (bparees@redhat.com)
- clean up jenkins master/slave parameters (bparees@redhat.com)
- Web console: fix problem balancing create flow columns (spadgett@redhat.com)
- Tooltip for multiple ImageSources in BC editor (jhadvig@redhat.com)
- fix two broken extended tests (bparees@redhat.com)
- Bug fix so that table-mobile will word-wrap: break-word (rhamilto@redhat.com)
- Add preliminary quota support for emptyDir volumes on XFS.
  (dgoodwin@redhat.com)
- Bump unit test timeout (jliggitt@redhat.com)
- updated tmpdir for e2e-docker (skuznets@redhat.com)
- Load environment files in containerized systemd units (sdodson@redhat.com)
- Interesting changes for rebase (jliggitt@redhat.com)
- Extended test namespace creation fixes (jliggitt@redhat.com)
- Mechanical changes for rebase (jliggitt@redhat.com)
- fix credential lookup for authenticated image stream import
  (jliggitt@redhat.com)
- Generated docs, conversions, copies, completions (jliggitt@redhat.com)
- UPSTREAM: <carry>: Allow overriding default generators for run
  (jliggitt@redhat.com)
- UPSTREAM: 22921: Fix job selector validation and tests (jliggitt@redhat.com)
- UPSTREAM: 22919: Allow starting test etcd with http (jliggitt@redhat.com)
- Stack definition lists only at narrower widths (spadgett@redhat.com)
- Disable externalIP by default (ccoleman@redhat.com)
- oc: warn about missing stream when deleting a tag (mkargaki@redhat.com)
- implemented miscellaneous iprovements for test-cmd (skuznets@redhat.com)
- Handle env vars that use valueFrom (jhadvig@redhat.com)
- UPSTREAM: 22917: Decrease verbosity of namespace controller trace logging
  (jliggitt@redhat.com)
- UPSTREAM: 22916: Correctly identify namespace subresources in GetRequestInfo
  (jliggitt@redhat.com)
- UPSTREAM: 22914: Move TestRuntimeCache into runtime_cache.go file
  (jliggitt@redhat.com)
- UPSTREAM: 22913: register internal types with scheme for reference unit test
  (jliggitt@redhat.com)
- UPSTREAM: 22910: Decrease parallelism in deletecollection test, lengthen test
  etcd certs (jliggitt@redhat.com)
- UPSTREAM: 22875: Tolerate multiple registered versions in a single group
  (jliggitt@redhat.com)
- UPSTREAM: 22877: mark filename flags for completions (ffranz@redhat.com)
- UPSTREAM: 22929: Test relative timestamps using UTC (jliggitt@redhat.com)
- UPSTREAM: 22746: add user-agent defaulting for discovery (deads@redhat.com)
- bump(github.com/Sirupsen/logrus): aaf92c95712104318fc35409745f1533aa5ff327
  (jliggitt@redhat.com)
- bump(github.com/hashicorp/golang-lru):
  a0d98a5f288019575c6d1f4bb1573fef2d1fcdc4 (jliggitt@redhat.com)
- bump(bitbucket.org/ww/goautoneg): 75cd24fc2f2c2a2088577d12123ddee5f54e0675
  (jliggitt@redhat.com)
- bump(k8s.io/kubernetes): 148dd34ab0e7daeb82582d6ea8e840c15a24e745
  (jliggitt@redhat.com)
- Update copy-kube-artifacts script (jliggitt@redhat.com)
- Allow recursive unit testing packages under godeps (jliggitt@redhat.com)
- Update godepchecker to print commit dates, allow checking out commits
  (jliggitt@redhat.com)
- Ensure errors are reported back in the container logs. (smitram@gmail.com)
- UPSTREAM: 22999: Display a better login message (ccoleman@redhat.com)
- oc: better new-app suggestions (mkargaki@redhat.com)
- parameterize IS namespace (gmontero@redhat.com)
- place tmp secret files in tmpdir (skuznets@redhat.com)

* Wed Mar 16 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.4
- Update ose build scripts (tdawson@redhat.com)
- move-upstream should use UPSTREAM_REPO_LOCATION like cherry-pick
  (ccoleman@redhat.com)
- Update javaLink extension (admin@benjaminapetersen.me)
- add parameter to start OS server with latest images (skuznets@redhat.com)
- added test to decode and validate ldap sync config fixtures
  (skuznets@redhat.com)
- Bug 1317783: avoid shadowing errors in the deployment controller
  (mkargaki@redhat.com)
- Add a test of services/service isolation to tests/e2e/networking/
  (danw@redhat.com)
- Run the isolation extended networking tests under both plugins
  (danw@redhat.com)
- Make sanity and isolation network tests pass in a single-node environment
  (danw@redhat.com)
- Update extended networking tests to use k8s e2e utilities (danw@redhat.com)
- UPSTREAM: 22303: Make net e2e helpers public for 3rd party reuse
  (danw@gnome.org)
- Handle parametrized content types for build triggers (jimmidyson@gmail.com)
- Fix for bugz https://bugzilla.redhat.com/show_bug.cgi?id=1316698 and issue
  #7444   o Fixes as per @pweil- and @marun review comments.   o Fixes as per
  @smarterclayton review comments. (smitram@gmail.com)
- Ensure we are clean to docker.io/* images during hack/release.sh
  (ccoleman@redhat.com)
- make userAgentMatching take a set of required and deny regexes
  (deads@redhat.com)
- UPSTREAM: 22746: add user-agent defaulting for discovery (deads@redhat.com)
- fine tune which template parameter error types are returned
  (gmontero@redhat.com)
- Add ConfigMap permissions (pmorie@gmail.com)
- Slim down issue template appearance (jliggitt@redhat.com)
- Bug 1316749: prompt warning when scaling test deployments
  (mkargaki@redhat.com)
- Remove description field from types (mfojtik@redhat.com)
- [RPMS] Add extended.test to /usr/libexec/origin/extended.test
  (sdodson@redhat.com)
- made edge language less ambiguous (skuznets@redhat.com)
- Move hack/test-cmd_util.sh to test-util.sh, messing with script-fu
  (ccoleman@redhat.com)

* Mon Mar 14 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.3
- UPSTREAM: 22929: Test relative timestamps using UTC (jliggitt@redhat.com)
- DETECT_RACES doesn't work (ccoleman@redhat.com)
- Add policy constraints for node targeting (jolamb@redhat.com)
- Mark filename flags for completions (ffranz@redhat.com)
- UPSTREAM: 22877: mark filename flags for completions (ffranz@redhat.com)
- Send graceful shutdown signal to all haproxy processes + wait for process to
  start listening, fixes as per @smarterclayton review comments and for
  integration tests. (smitram@gmail.com)
- always flush glog before returning from build logic (bparees@redhat.com)
- Improving markup semantics and appearance of display of Volumes data
  (rhamilto@redhat.com)
- Bumping openshift-object-describer to v1.1.2 (rhamilto@redhat.com)
- Bump grunt-contrib-uglify to 0.6.0 (spadgett@redhat.com)
- Export OS_OUTPUT_GOPATH=1 in Makefile (stefw@redhat.com)
- Bug fix for long, unbroken words that don't wrap in pod template
  (rhamilto@redhat.com)
- Fix test with build reference cycle (rhcarvalho@gmail.com)
- updated issue template (skuznets@redhat.com)
- Rename misleading util function (rhcarvalho@gmail.com)
- Only check circular references for oc new-build (rhcarvalho@gmail.com)
- Extract TestBuildOutputCycleDetection (rhcarvalho@gmail.com)
- Fixes rsh usage (ffranz@redhat.com)
- Increase sdn node provisioning timeout (marun@redhat.com)
- Set default template router reload interval to 5 seconds. (smitram@gmail.com)
- Update and additions to web console screenshots (sgoodwin@redhat.com)

* Fri Mar 11 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.2
- Remove left over after move to test/integration (rhcarvalho@gmail.com)
- Improved next steps pages for bcs using sample repos (ffranz@redhat.com)
- Remove dead code (rhcarvalho@gmail.com)
- oc new-app/new-build: handle the case when an imagestream matches but has no
  tags (cewong@redhat.com)
- Add the ability to install iptables rules to eat SYN packets targeted to
  haproxy while the haproxy reload happens.  This prevents traffic to haproxy
  getting dropped if it connects while the reload is in progess.
  (bbennett@redhat.com)
- sample-app: update docs (mkargaki@redhat.com)
- bump(github.com/openshift/source-to-image):
  fb7794026064c5a7b83905674a5244916a07fef9 (rhcarvalho@gmail.com)
- Fixing BZ1291521 where long project name spills out of modal
  (rhamilto@redhat.com)
- Moving overflow:hidden to specifically target  long replication controller or
  deployment name instead of deployment-block when caused another issue.  -
  Fixes https://github.com/openshift/origin/issues/7887 (sgoodwin@redhat.com)
- changed find behavior for OSX compatibility (skuznets@redhat.com)
- add debug statements for test-go (skuznets@redhat.com)
- Improve log text highlighting in Firefox (spadgett@redhat.com)
- Fixes [options] in usage (ffranz@redhat.com)
- Prevent last catalog tile from stretching to 100%% width
  (spadgett@redhat.com)
- Fix default cert for edge route not being used - fixes #7904
  (smitram@gmail.com)
- Initial addition of issue template (mfojtik@redhat.com)
- Fix deployment page layout problems (spadgett@redhat.com)
- allow different cert serial number generators (deads@redhat.com)
- Enabling LessCSS source maps for development (rhamilto@redhat.com)
- Prevent fieldset from expanding due to content (jawnsy@redhat.com)
- Add placement and container to popover and tooltip into popover.js so that
  messages aren't hidden when spanning multiple scrollable areas.  - Fixes
  https://github.com/openshift/origin/issues/7723 (sgoodwin@redhat.com)
- bump(k8s.io/kubernetes): 91d3e753a4eca4e87462b7c9e5391ec94bb792d9
  (jliggitt@redhat.com)
- Add liveness and readiness probe for Jenkins (mfojtik@redhat.com)
- Fix word-break in Firefox (spadgett@redhat.com)
- Add table-bordered styles to service port table (spadgett@redhat.com)
- nocache should be noCache (haowang@redhat.com)
- Drop capabilities when running s2i build container (cewong@redhat.com)
- bump(github.com/openshift/source-to-image)
  0278ed91e641158fbbf1de08808a12d5719322d8 (cewong@redhat.com)
- Fixed races in ratelimiter tests on go1.5 (maszulik@redhat.com)

* Wed Mar 09 2016 Troy Dawson <tdawson@redhat.com> 3.2.0.1
- Change version numbering from 3.1.1.9xx to 3.2.0.x to avoid confusion.
  (tdawson@redhat.com)
- oc: update route warnings for oc status (mkargaki@redhat.com)
- Allow extra trusted bundles when generating master certs, node config, or
  kubeconfig (jliggitt@redhat.com)
- Update README.md (ccoleman@redhat.com)
- Update README.md (ccoleman@redhat.com)
- Update README (ccoleman@redhat.com)
- Break words when wrapping values in environment table (spadgett@redhat.com)
- Improve deployment name wrapping on overview page (spadgett@redhat.com)
- Bug 1315595: Use in-container env vars for liveness/readiness probes
  (mfojtik@redhat.com)
- deploy: more informative cancellation event on dc (mkargaki@redhat.com)
- Fixing typo (jhadvig@redhat.com)
- Show kind in editor modal (spadgett@redhat.com)
- rsync must validate if pod exists (ffranz@redhat.com)
- Minor fixes to Jenkins kubernetes readme (mfojtik@redhat.com)
- Breadcrumbs unification (jhadvig@redhat.com)
- test-cmd: mktemp --suffix is not supported in Mac (mkargaki@redhat.com)
- Fix hardcoded f5 username (admin). (smitram@gmail.com)
- Add "quickstart" to web console browse menu (spadgett@redhat.com)
- Add active deadline to browse pod page (spadgett@redhat.com)
- Unconfuse web console about resource and kind (spadgett@redhat.com)
- Fix role addition for kube e2e tests (marun@redhat.com)
- UPSTREAM: 22516: kubectl: set maxUnavailable to 1 if both fenceposts resolve
  to zero (mkargaki@redhat.com)
- Add pods donut to deployment page (spadgett@redhat.com)
- deploy: emit events on the dc instead of its rcs (mkargaki@redhat.com)
- prevent skewed client updates (deads@redhat.com)
- oc new-build: add --image-stream flag (cewong@redhat.com)
- UPSTREAM: 22526: kubectl: bring the rolling updater on par with the
  deployments (mkargaki@redhat.com)
- Set source of incremental build artifacts (rhcarvalho@gmail.com)
- bump(github.com/openshift/source-to-image):
  2e889d092f8f3fd0266610fa6b4d92db999ef68f (rhcarvalho@gmail.com)
- Use conventional profiler setup code (dmace@redhat.com)
- Support HTTP pprof server in registry (dmace@redhat.com)
- Bump docker minimum version to 1.9.1 in preparation for v1.2
  (sdodson@redhat.com)
- shorten dc caused by annotations (deads@redhat.com)

* Mon Mar 07 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.911
- add oc status warnings for missing is/istag/dockref/isimg for bc
  (gmontero@redhat.com)
- Update skip tags for gluster and ceph. (jay@apache.org)
- Skip quota check when cluster roles are outdated (miminar@redhat.com)
- Put dev cluster unit files in /etc/systemd/system (marun@redhat.com)
- dind: skip building etcd (marun@redhat.com)
- dind: disable sdn node at the end of provisioning (marun@redhat.com)
- Simplify vagrant/dind host provisioning (marun@redhat.com)
- Remove / fix dead code (ccoleman@redhat.com)
- UPSTREAM: <carry>: fix casting errors in case of obj nil
  (jawed.khelil@amadeus.com)
- Show log output in conversion generation (ccoleman@redhat.com)
- Support in-cluster-config for registry (ccoleman@redhat.com)
- Upgrade the registry to create secrets and service accounts
  (ccoleman@redhat.com)
- Support overriding the hostname in the router (ccoleman@redhat.com)
- Remove invisible browse option from web console catalog (spadgett@redhat.com)
- fixes bug 1312218 (bugzilla), fixes #7646 (github)
  (admin@benjaminapetersen.me)
- add discovery cache (deads@redhat.com)
- Making margin consistent around alerts inside.modal-resource-edit
  (rhamilto@redhat.com)
- platformmanagement_public_425 - add quota information to oc describe is
  (maszulik@redhat.com)
- oc: hide markers from different projects on oc status (mkargaki@redhat.com)
- Removing .page-header from About as the visuals aren't "right" for the page
  (rhamilto@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  58baf17e027bc1fd913cddd55c5eed4782400c60 (danw@redhat.com)
- UPSTREAM: revert: 902e416: <carry>: v1beta3 scc (dgoodwin@redhat.com)
- UPSTREAM: revert: 7d1b481: <carry>: scc (dgoodwin@redhat.com)
- Dashboard extended test should not be run (ccoleman@redhat.com)
- make all alias correctly (deads@redhat.com)
- Bug 1310616: Validate absolute dir in build secret for docker strategy in oc
  new-build (mfojtik@redhat.com)
- Remove unnecessary word from oc volume command (nakayamakenjiro@gmail.com)
- Revert "Updates to use the SCC allowEmptyDirVolumePlugin setting."
  (dgoodwin@redhat.com)
- UPSTREAM: <carry>: Increase test etcd request timeout to 30s
  (ccoleman@redhat.com)
- Fix services e2e tests for dev clusters (marun@redhat.com)
- tweak registry roles (deads@redhat.com)
- export OS_OUTPUT_GOPATH for target build (jawed.khelil@amadeus.com)
- Fix intra-pod kube e2e test (marun@redhat.com)
- WIP: Enable FSGroup in restricted and hostNS SCCs (pmorie@gmail.com)
- Change default ClusterNetworkCIDR and HostSubnetLength (danw@redhat.com)
- Remove downward api call for Jenkins kubernetes example (mfojtik@redhat.com)

* Fri Mar 04 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.910
- Resolving visual defect on Storage .page-header (rhamilto@redhat.com)
- Cleaning up random drop shadow and rounded corners on messenger messages
  (rhamilto@redhat.com)
- Correcting colspan value to resolve cosmetic bug with missing right border on
  <thead> (rhamilto@redhat.com)
- ignore unrelated build+pod events during tests (bparees@redhat.com)
- Adjust kube-topology so that it doesn't extend off of iOS viewport. Move
  bottom spacing from container-fluid to tab-content. (sgoodwin@redhat.com)
- Make mktmp call in common.sh compatible with OS X (cewong@redhat.com)
- Update external examples to include readiness/liveness probes
  (mfojtik@redhat.com)
- Fix build link in alert message (spadgett@redhat.com)
- Make "other routes" link go to browse routes page (spadgett@redhat.com)
- Skip hostPath test for upstream conformance test. (jay@apache.org)
- oc rsync: do not set owner when extracting with the tar strategy
  (cewong@redhat.com)
- removed SAR logfile from artifacts (skuznets@redhat.com)
- integration: Retry import from external registries when not reachable
  (miminar@redhat.com)
- Prevent log line number selection in Chrome (spadgett@redhat.com)
- Add create route button padding on mobile (jhadvig@redhat.com)
- test-cmd: ensure oc apply works with lists (mkargaki@redhat.com)
- UPSTREAM: 20948: Fix reference to versioned object in kubectl apply
  (mkargaki@redhat.com)
- Web console: fix problems with display route and route warnings
  (spadgett@redhat.com)
- Restrict events filter to certain fields in web console (spadgett@redhat.com)
- configchange: correlate triggers with the generated cause
  (mkargaki@redhat.com)
- Bug fix for negative reload intervals - bugz 1311459. (smitram@gmail.com)
- Fill image's metadata in the registry (miminar@redhat.com)
- Added additional quota check for layer upload in a registry
  (miminar@redhat.com)
- Resource quota for images and image streams (miminar@redhat.com)
- Add support for build config into oc set env (mfojtik@redhat.com)
- UPSTREAM: docker/distribution: 1474: Defined ErrAccessDenied error
  (miminar@redhat.com)
- UPSTREAM: docker/distribution: 1473: Commit uploaded blob with size
  (miminar@redhat.com)
- UPSTREAM: 20446: New features in ResourceQuota (miminar@redhat.com)

* Wed Mar 02 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.909
- Added more cmd tests for import-image to cover main branches
  (maszulik@redhat.com)
- Support API group and version in SAR/RAR (jliggitt@redhat.com)
- Pick correct strategy for binary builds (cewong@redhat.com)
- Metrics: show missing data as gaps in the chart (spadgett@redhat.com)
- Issue 7555 - fixed importimage which was picking wrong docker pull spec for
  images that failed previous import. (maszulik@redhat.com)
- Refactor import-image to Complete-Validate-Run scheme. Additionally split the
  code so it's testable + added tests. (maszulik@redhat.com)
- Adds completion for oc rsh command (akram@free.fr)
- Fix swagger description generation (jliggitt@redhat.com)
- Allow externalizing/encrypting config values (jliggitt@redhat.com)
- Add encrypt/decrypt helper commands (jliggitt@redhat.com)
- bump all template mem limits to 512 Mi (gmontero@redhat.com)
- Fixes as per @smarterclayton's review comments. (smitram@gmail.com)
- Use http[s] ports for environment values. Allows router ports to be overriden
  + multiple instances to run with host networking. (smitram@gmail.com)
- Switch from margin to padding and move it to the container-fluid div so gray
  bg extends length of page and maintains bottom spacing across pages Include
  fix to prevent filter appended button from wrapping in Safari
  (sgoodwin@redhat.com)
- check covers for role changes (deads@redhat.com)
- favicon.ico not copied during asset build (jforrest@redhat.com)
- Added liveness and readiness probes to database templates
  (mfojtik@redhat.com)
- Create policy for image registry users (agladkov@redhat.com)

* Mon Feb 29 2016 Scott Dodson <sdodson@redhat.com> 3.1.1.908
- enabled junitreport tool to stream output (skuznets@redhat.com)
- BZ_1312819: Can not add Environment Variables on buildconfig edit page
  (jhadvig@redhat.com)
- rewrite hack/test-go.sh (skuznets@redhat.com)
- UPSTREAM: <drop>: patch for 16146: Fix validate event for non-namespaced
  kinds (deads@redhat.com)
- added commands to manage serviceaccounts (skuznets@redhat.com)
- configchange: proceed with deployment with non-automatic ICTs
  (mkargaki@redhat.com)
- Allow use S2I builder with non-s2i build strategies (mfojtik@redhat.com)
- Verify the integration test build early (ccoleman@redhat.com)
- Support building from dirs symlinked from GOPATH (pmorie@gmail.com)
- remove openshift ex tokens (deads@redhat.com)
- Improve Dockerfile keyword highlighting in web console (spadgett@redhat.com)
- Don't shutdown etcd in integration tests (ccoleman@redhat.com)
- Fix OSE branding on web console (#1309205) (tdawson@redhat.com)
- hack/update-swagger-spec times out in integration (ccoleman@redhat.com)
- Dump debug info from etcd during integration tests (ccoleman@redhat.com)
- Upgrade dind image to fedora23 (marun@redhat.com)
- Add header back to logging in page (spadgett@redhat.com)
- UPSTREAM: 21265: added 'kubectl create sa' to create serviceaccounts
  (skuznets@redhat.com)
- Updated copy-kube-artifacts to current k8s (maszulik@redhat.com)

* Fri Feb 26 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.907
- Fix OSE branding on web console (#1309205) (tdawson@redhat.com)
- Add ability to push to image build script (tdawson@redhat.com)
- Change button label from "Cancel" to "Cancel Build" (spadgett@redhat.com)
- Filter and sort web console events table (spadgett@redhat.com)
- Fix timing problem enabling start build button (spadgett@redhat.com)
- Add Patternfly button styles to catalog browse button (spadgett@redhat.com)
- Bump Vagrant machine RAM requirement (dcbw@redhat.com)
- Remove json files added accidentally (rhcarvalho@gmail.com)
- Submit forms on enter (jhadvig@redhat.com)
- Set triggers via the CLI (ccoleman@redhat.com)
- UPSTREAM: <drop>: utility for the rolling updater (mkargaki@redhat.com)
- UPSTREAM: 21872: kubectl: preserve availability when maxUnavailability is not
  100%% (mkargaki@redhat.com)
- Including css declarations of flex specific prefixes for IE10 to position
  correctly (sgoodwin@redhat.com)
- Adjustments to the css controlling the filter widget so that it addresses
  some overlapping issues. Also, subtle changes to the project nav menu
  scrollbar so that it's more noticable. (sgoodwin@redhat.com)
- Only show builds bar chart when at least 4 builds (spadgett@redhat.com)
- Disable failing extended tests. (ccoleman@redhat.com)
- Remove v(4) logging of build admission startup (cewong@redhat.com)
- Include build hook in describer (rhcarvalho@gmail.com)
- Update hack/update-external-examples.sh (rhcarvalho@gmail.com)
- Update external examples (rhcarvalho@gmail.com)
- Add shasums to release build output (ccoleman@redhat.com)
- diagnostics: promote from openshift ex to oadm (lmeyer@redhat.com)
- Integrate etcd into the test cases themselves (ccoleman@redhat.com)
- Web console: improve repeated events message (spadgett@redhat.com)
- Improve web console metrics error message (spadgett@redhat.com)
- added generated swagger descriptions for v1 api (skuznets@redhat.com)
- Fix css compilation issues that affect IE, particularly flexbox
  (jforrest@redhat.com)
- pruned govet whitelist (skuznets@redhat.com)
- Use args flavor sample-app build hooks (rhcarvalho@gmail.com)
- added automatic swagger doc generator (skuznets@redhat.com)
- disabling start build/rebuild button when bc is deleted (jhadvig@redhat.com)
- UPSTREAM: <carry>: change BeforeEach to JustBeforeEach to ensure SA is
  granted to anyuid SCC (pweil@redhat.com)
- Fix reuse of release build on nfs mount (marun@redhat.com)
- Force dind deployment to build binaries by default (marun@redhat.com)
- Symlink repo mount to /origin for convenience (marun@redhat.com)
- Fix vagrant vm cluster and dind deployment (marun@redhat.com)
- Fix dind go build (marun@redhat.com)

* Wed Feb 24 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.906
- Fix cli download link (#1311396) (tdawson@redhat.com)
- Fix bindata diff (spadgett@redhat.com)
- Add `oc debug` to make it easy to launch a test pod (ccoleman@redhat.com)
- Hide hidden flags in help output (ccoleman@redhat.com)
- React to changes in upstream term (ccoleman@redhat.com)
- UPSTREAM: 21624: improve terminal reuse and attach (ccoleman@redhat.com)
- Add 'oc set probe' for setting readiness and liveness (ccoleman@redhat.com)
- Remove npm shrinkwrap by bumping html-min deps (jforrest@redhat.com)
- Fix router e2e validation for docker 1.9 (marun@redhat.com)
- Cache projects outside of projectHeader link fn (admin@benjaminapetersen.me)
- Use $scope.$emit to notify projectHeader when project settings change
  (admin@benjaminapetersen.me)
- fix builder version typo (bparees@redhat.com)
- Update swagger description (jliggitt@redhat.com)
- add hostnetwork scc (pweil@redhat.com)
- UPSTREAM: 21680: Restore service port validation compatibility with 1.0/1.1
  (jliggitt@redhat.com)
- Read extended user attributes from auth proxy (jliggitt@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  08a79d5adc8af21b14adcc0b9650df2d5fccf2f0 (danw@redhat.com)
- Display better route info in status (ccoleman@redhat.com)
- Ensure log run vars are set in GET and WATCH on build, pod & deployment
  (admin@benjaminapetersen.me)
- Contextualize errors from GetCGroupLimits (rhcarvalho@gmail.com)
- Fix extended tests and up default pod limit. (ccoleman@redhat.com)
- configchange: abort update once an image change is detected
  (mkargaki@redhat.com)
- UPSTREAM: 21671: kubectl: add container ports in pod description
  (mkargaki@redhat.com)
- Js error on overview for route warnings (jforrest@redhat.com)
- UPSTREAM: 21706: Ensure created service account tokens are available to the
  token controller (jliggitt@redhat.com)
- use imageid from trigger for imagesource inputs, instead of resolving them
  (bparees@redhat.com)
- increase binary build timeout to 5 minutes (bparees@redhat.com)
- Add status icon for ContainerCreating reason (spadgett@redhat.com)
- integration test for newapp dockerimagelookup (bparees@redhat.com)
- pod diagnostics: fix panic in bz 1302649, prettify (lmeyer@redhat.com)
- Fix log follow link on initial page load, add loading ellipsis while
  logViewer is pending (admin@benjaminapetersen.me)
- Don't show "Deployed" for plain RCs in web console (spadgett@redhat.com)
- Run post build hook with `/bin/sh -ic` (rhcarvalho@gmail.com)
- origin-pod rpm does not require the base rpm (sdodson@redhat.com)
- Mobile table headers missing on browse image page (jforrest@redhat.com)
- Suppress escape sequences at end of hack/test-assets.sh (ccoleman@redhat.com)
- Replace /bin/bash in oc rsh with /bin/sh (mfojtik@redhat.com)
- UPSTREAM: 19868: Fixed persistent volume claim controllers processing an old
  claim (jsafrane@redhat.com)
- Display additional tags after import (ccoleman@redhat.com)
- UPSTREAM: 21268: Delete provisioned volumes without claim.
  (jsafrane@redhat.com)
- UPSTREAM: 21273: kubectl: scale down based on ready during rolling updates
  (mkargaki@redhat.com)
- UPSTREAM: 20213: Fixed persistent volume claim controllers processing an old
  volume (jsafrane@redhat.com)

* Mon Feb 22 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.905
- Display better information when running 'oc' (ccoleman@redhat.com)
- Update completions to be cross platform (ccoleman@redhat.com)
- Add events tab to plain RCs in web console (spadgett@redhat.com)
- new-app broken when docker not installed (ccoleman@redhat.com)
- UPSTREAM: 21628: Reduce node controller debug logging (ccoleman@redhat.com)
- Drop 1.4 and add 1.6 to travis Go matrix (ccoleman@redhat.com)
- Add --since-time logs test (jliggitt@redhat.com)
- UPSTREAM: 21398: Fix sinceTime pod log options (jliggitt@redhat.com)
- Show project display name in breadcrumbs (spadgett@redhat.com)
- Hide copy to clipboard button on iOS (spadgett@redhat.com)
- Validate master/publicMaster args to create-master-certs
  (jliggitt@redhat.com)
- Update completions (ffranz@redhat.com)
- UPSTREAM: 21593: split adding global and external flags (ffranz@redhat.com)
- clean up wording of oc status build/deployment descriptions
  (bparees@redhat.com)
- iOS: prevent select from zooming page (spadgett@redhat.com)
- Restoring fix for route names overflowing .componet in Safari for iOS
  (rhamilto@redhat.com)
- On node startup, perform more checks of known requirements
  (ccoleman@redhat.com)
- Bug 1309195 - Return ErrNotV2Registry when falling back to http backend
  (maszulik@redhat.com)
- Set OS_OUTPUT_GOPATH=1 to build in a local GOPATH (ccoleman@redhat.com)
- Add back the filter bar to the bc and dc pages (jforrest@redhat.com)
- Router should tolerate not having permission to write status
  (ccoleman@redhat.com)
- Env vars with leading slashes cause major js errors in console create from
  image flow (jforrest@redhat.com)
- Refactor WaitForADeployment (rhcarvalho@gmail.com)
- bump(github.com/elazarl/goproxy): 07b16b6e30fcac0ad8c0435548e743bcf2ca7e92
  (ffranz@redhat.com)
- UPSTREAM: 21409: SPDY roundtripper support to proxy with Basic auth
  (ffranz@redhat.com)
- UPSTREAM: 21185: SPDY roundtripper must respect InsecureSkipVerify
  (ffranz@redhat.com)
- Use route ingress status in console (jforrest@redhat.com)
- correct cluster resource override tests (deads@redhat.com)
- UPSTREAM: 21341: Add a liveness and readiness describer to pods
  (mkargaki@redhat.com)
- oc: enhance deploymentconfig description (mkargaki@redhat.com)
- Fix commit checker to find commits with upstream changes
  (jliggitt@redhat.com)
- Verify extended tests build (jliggitt@redhat.com)
- Normalize usernames for AllowAllPasswordIdentityProvider
  (jliggitt@redhat.com)
- Add auth logging to login page, basic auth, and OAuth paths
  (jliggitt@redhat.com)
- Use "install" to install SDN script to make sure they get exec permission
  (danw@redhat.com)
- tar extract cannot hard link on vboxfs filesystem (horatiu@vlad.eu)
- Use pkg/util/homedir from upstream to detect home directory
  (ffranz@redhat.com)
- UPSTREAM: 17590: use correct home directory on Windows (ffranz@redhat.com)
- Web console: add "Completed" to status-icon directive (spadgett@redhat.com)
- Adjust empty state margin for pages with tabs (spadgett@redhat.com)
- Limit route.spec.to to kind/name (jliggitt@redhat.com)
- Add cross project promotion example (mfojtik@redhat.com)

* Fri Feb 19 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.904
- Updated URLs fo OpenShift Enterprise (tdawson@redhat.com)
- Fix extended build compile error (jliggitt@redhat.com)
- refactored test-end-to-end/core to use os::cmd functions
  (skuznets@redhat.com)
- update completions (pweil@redhat.com)
- UPSTREAM: <carry>: add scc describer (pweil@redhat.com)
- Allow subdomain flag to create router (ccoleman@redhat.com)
- add gutter class to annotations directive to provide margin
  (admin@benjaminapetersen.me)
- vendor quickstart templates into origin (bparees@redhat.com)
- Add attach storage and create route to the actions dropdown
  (spadgett@redhat.com)
- properly check for nil docker client value (bparees@redhat.com)
- Web console: show more detailed pod status (spadgett@redhat.com)
- always pull the previous image for s2i builds (bparees@redhat.com)
- Improve log error messages (admin@benjaminapetersen.me)
- add DB icons and also add annotations to the 'latest' imagestream tags
  (bparees@redhat.com)
- Add Jenkins with kubernetes plugin example (mfojtik@redhat.com)
- UPSTREAM: 21470: fix limitranger to handle latent caches without live lookups
  every time (deads@redhat.com)
- react to limitrange update (deads@redhat.com)
- Handle multiple imageChange triggers in BC edit page (jhadvig@redhat.com)
- Resolving a couple cosmetic issues with navbar at mobile resolutions
  (rhamilto@redhat.com)
- Refactoring .component to prevent weird wrapping issues (rhamilto@redhat.com)
- UPSTREAM: 21335: make kubectl logs work for replication controllers
  (deads@redhat.com)
- make sure that logs for rc work correctly (deads@redhat.com)
- Use in-cluster-config without setting POD_NAMESPACE (jliggitt@redhat.com)
- UPSTREAM: 21095: Provide current namespace to InClusterConfig
  (jliggitt@redhat.com)
- Get rid of the plugins/ dir (ccoleman@redhat.com)
- Route ordering is unstable, and writes must be ignored (ccoleman@redhat.com)
- Replace kebab with actions button on browse pages (spadgett@redhat.com)
- Fixes for unnecessary scrollbars in certain areas and situations
  (sgoodwin@redhat.com)
- Fix asset build so that it leaves the dev environment in place without having
  to re-launch grunt serve (jforrest@redhat.com)
- addition of memory limits with online beta in mind (gmontero@redhat.com)
- make hello-openshift print to stdout when serving a request
  (bparees@redhat.com)
- Run-once pod duration: remove flag from plugin config (cewong@redhat.com)
- Add deletecollection verb to admin/edit roles (jliggitt@redhat.com)
- UPSTREAM: 21005: Use a different verb for delete collection
  (jliggitt@redhat.com)
- Validate wildcard certs against non-wildcard namedCertificate names
  (jliggitt@redhat.com)
- Image building resets the global script time (ccoleman@redhat.com)
- remove volumes when removing containers (skuznets@redhat.com)
- UPSTREAM: 21089: Default lockfile to empty string while alpha
  (pweil@redhat.com)
- UPSTREAM: 21340: Tolerate individual NotFound errors in DeleteCollection
  (pweil@redhat.com)
- UPSTREAM: 21318: kubectl: use the factory properly for recording commands
  (pweil@redhat.com)
- refactor api interface to allow returning an error (pweil@redhat.com)
- fixing tests (pweil@redhat.com)
- proxy config refactor (pweil@redhat.com)
- boring refactors (pweil@redhat.com)
- UPSTREAM: <carry>: update generated client code for SCC (pweil@redhat.com)
- UPSTREAM: 21278: include discovery client in adaptor (pweil@redhat.com)
- bump(k8s.io/kubernetes): bc4550d9e93d04e391b9e33fc85a679a0ca879e9
  (pweil@redhat.com)
- UPSTREAM: openshift/openshift-sdn: <drop>: openshift-sdn refactoring
  (pweil@redhat.com)
- bump(github.com/stretchr/testify): e3a8ff8ce36581f87a15341206f205b1da467059
  (pweil@redhat.com)
- bump(github.com/onsi/ginkgo): 07d85e6b10c4289c7d612f9b13f45ba36f66d55b
  (pweil@redhat.com)
- bump(github.com/fsouza/go-dockerclient):
  0099401a7342ad77e71ca9f9a57c5e72fb80f6b2 (pweil@redhat.com)
- UPSTREAM: coreos/etcd: 4503: expose error details for normal stringify
  (deads@redhat.com)
- bump(github.com/coreos/etcd): bc9ddf260115d2680191c46977ae72b837785472
  (pweil@redhat.com)
- godeps: fix broken hash before restore (pweil@redhat.com)
- The Host value should be written to all rejected routes (ccoleman@redhat.com)
- fix jenkins testjob xml; fix jenkins ext test deployment error handling
  (gmontero@redhat.com)
- Web console: honor cluster-resource-override-enabled (spadgett@redhat.com)
- bump(github.com/openshift/source-to-image):
  41947800efb9fb7f5c3a13e977d26ac0815fa4fb (maszulik@redhat.com)
- UPSTREAM: 21266: only load kubeconfig files one time (deads@redhat.com)
- Fix admission attribute comparison (agladkov@redhat.com)
- Suppress conflict error printout (ccoleman@redhat.com)

* Wed Feb 17 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.903
- Change web console to display OpenShift Enterprise logo and urls
  (tdawson@redhat.com)
- remove testing symlink (deads@redhat.com)
- Add pathseg polyfill to fix c3 bar chart runtime error (spadgett@redhat.com)
- Size build chart correctly in Firefox (spadgett@redhat.com)
- dump build logs when build test fails (bparees@redhat.com)
- fix circular input/output detection (bparees@redhat.com)
- do not tag for pushing if there is no output target (bparees@redhat.com)
- admission: cluster req/limit override plugin (lmeyer@redhat.com)
- ignore events from previous builds (bparees@redhat.com)
- Changes and additions to enable text truncation of the project menu and
  username at primary media query breakpoints (sgoodwin@redhat.com)
- Addition of top-header variables for mobile and desktop to set height and
  control offset of fixed header height.         This will ensure the proper
  bottom offset so that the flex containers extend to the bottom correctly.
  Switch margin-bottom to padding-bottom so that background color is maintained
  (sgoodwin@redhat.com)
- Set a timeout on integration tests of 4m (ccoleman@redhat.com)
- added support for paged queries in ldap sync (skuznets@redhat.com)
- bump(gopkg.in/ldap.v2): 07a7330929b9ee80495c88a4439657d89c7dbd87
  (skuznets@redhat.com)
- Resource specific events on browse pages (jhadvig@redhat.com)
- added Godoc to api types where Godoc was missing (skuznets@redhat.com)
- updated commitchecker regex to work for ldap package (skuznets@redhat.com)
- Fix layout in osc-key-value directive (admin@benjaminapetersen.me)
- bump(github.com/openshift/openshift-sdn):
  5cf5cd2666604324c3bd42f5c12774cfaf1a3439 (danw@redhat.com)
- Add docker-registry image store on glusterfs volume example
  (jcope@redhat.com)
- Bump travis to go1.5.3 (jliggitt@redhat.com)
- Provide a way in console to access orphaned builds / deployments
  (jforrest@redhat.com)
- Revising sidebar to better align with PatternFly standard
  (rhamilto@redhat.com)
- refactor docker image searching (bparees@redhat.com)
- Remove EtcdClient from MasterConfig (agladkov@redhat.com)
- Move 'adm' function into 'oc' as 'oc adm' (ccoleman@redhat.com)
- Break compile time dependency on etcd for clients (ccoleman@redhat.com)

* Mon Feb 15 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.902
-  Backporting dist-git Dockerfile to Dockerfile.product (tdawson@redhat.com)
- added infra namespace to PV recycler (mturansk@redhat.com)
- Run user-provided command as part of build flow (rhcarvalho@gmail.com)
- Fix deployment log var (admin@benjaminapetersen.me)
- Add direnv .envrc to gitignore (pmorie@gmail.com)
- Use normal GOPATH for build (ccoleman@redhat.com)
- DeploymentConfig hooks did not have round trip defaulting
  (ccoleman@redhat.com)
- Fix pod warnings popup (spadgett@redhat.com)
- Move slow newapp tests to integration (ccoleman@redhat.com)
- filter events being tested (bparees@redhat.com)
- Improve performance of overview page with many deployments
  (spadgett@redhat.com)
- mark slow extended build/image tests (bparees@redhat.com)
- Tweak LDAP sync config error flags (jliggitt@redhat.com)
- Add extension points to the nav menus and add sample extensions for online
  (jforrest@redhat.com)
- UPSTREAM: coreos/etcd: 4503: expose error details for normal stringify
  (deads@redhat.com)
- suppress query scope issue on member extraction (skuznets@redhat.com)
- use correct fixture path (bparees@redhat.com)
- Add a TagImages hook type to lifecycle hooks (ccoleman@redhat.com)
- Support create on update of imagestreamtags (ccoleman@redhat.com)
- Many anyuid programs fail due to SETGID/SETUID caps (ccoleman@redhat.com)
- Exclude failing tests, add [Kubernetes] and [Origin] skip targets
  (ccoleman@redhat.com)
- Scheduler has an official default name (ccoleman@redhat.com)
- Disable extended networking testing of services (marun@redhat.com)
- Fix filename of network test entry point (marun@redhat.com)
- Make sure extended networking isolation test doesn't run for subnet plugin
  (dcbw@redhat.com)
- Ensure more code uses the default transport settings (ccoleman@redhat.com)
- read docker pull secret from correct path (bparees@redhat.com)
- Ignore .vscode (ccoleman@redhat.com)
- Have routers take ownership of routes (ccoleman@redhat.com)
- Fix web console dev env certificate problems for OS X Chrome
  (spadgett@redhat.com)
- Update build info in web console pod template (spadgett@redhat.com)
- Changing .ace_editor to .ace_editor-bordered so the border around .ace_editor
  is optional (rhamilto@redhat.com)
- Web console: Warn about problems with routes (spadgett@redhat.com)
- fix variable shadowing complained about by govet for 1.4 (bparees@redhat.com)
- added LDIF for suppression testing (skuznets@redhat.com)
- launch integration tests using only the API server when possible
  (deads@redhat.com)
- bump(k8s.io/kubernetes): f0cd09aabeeeab1780911c8023203993fd421946
  (pweil@redhat.com)
- Create oscUnique directive to provide unique-in-list validation on DOM nodes
  with ng-model attribute (admin@benjaminapetersen.me)
- Support modifiable pprof web port (nakayamakenjiro@gmail.com)
- Add additional docker volume (dmcphers@redhat.com)
- Web console: Use service port name for route targetPort (spadgett@redhat.com)
- Correcting reference to another step (rhamilto@redhat.com)
- fix jobs package import naming (bparees@redhat.com)
- fix ldap sync decode codec (deads@redhat.com)
- Fix attachScrollEvents on window.resize causing affixed follow links in
  logViewer to behave inconsistently (admin@benjaminapetersen.me)
- Use SA config when creating clients (ironcladlou@gmail.com)
- fix up client code to use the RESTMapper functions they mean
  (deads@redhat.com)
- fix ShortcutRESTMapper and prevent it from ever silently failing again
  (deads@redhat.com)
- UPSTREAM: 20968: make partial resource detection work for singular matches
  (deads@redhat.com)
- UPSTREAM: 20829: Union rest mapper (deads@redhat.com)
- validate default imagechange triggers (bparees@redhat.com)
- ignore .vscode settings (jliggitt@redhat.com)
- handle additional cgroup file locations (bparees@redhat.com)
- Fix web console type error when image has no env (spadgett@redhat.com)
- Fixing livereload so that it works with https (rhamilto@redhat.com)
- Display source downloading in build logs by default (mfojtik@redhat.com)
- Clean up test scripts (jliggitt@redhat.com)
- Forging consistency among empty tables at xs screen size #7163
  (rhamilto@redhat.com)
- UPSTREAM: 20814: type RESTMapper errors to better handle MultiRESTMapper
  errors (deads@redhat.com)
- Renamed extended tests files by removing directory name from certain files
  (maszulik@redhat.com)
- oc: enable autoscale for dcs (mkargaki@redhat.com)
- add fuzzer tests for config scheme (deads@redhat.com)
- Updates to use the SCC allowEmptyDirVolumePlugin setting.
  (dgoodwin@redhat.com)
- UPSTREAM: <carry>: scc (dgoodwin@redhat.com)
- UPSTREAM: <carry>: v1beta3 scc (dgoodwin@redhat.com)
- kebab case urls (and matching view templates), add legacy redirects
  (admin@benjaminapetersen.me)
- Add tests for explain (ccoleman@redhat.com)
- Bug fix where table border on right side of thead was disappearing at sm and
  md sizes (rhamilto@redhat.com)
- Cherrypick should force delete branch (ccoleman@redhat.com)
- Support block profile by pprof webserver (nakayamakenjiro@gmail.com)
- Allow recursive DNS to be enabled (ccoleman@redhat.com)
- Prevent dev cluster deploy from using stale config (marun@redhat.com)
- remove grep -P usage (skuznets@redhat.com)
- Support debugging networking tests with delve (marun@redhat.com)

* Tue Feb 09 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.901
- Add organization restriction to github IDP (jliggitt@redhat.com)
- UPSTREAM: 20827: Backwards compat for old Docker versions
  (ccoleman@redhat.com)
- Handle cert-writing error (jliggitt@redhat.com)
- image scripts updated to work with dependents. (tdawson@redhat.com)
- Add aos-3.2 (tdawson@redhat.com)
- Web console: only show "no services" message if overview empty
  (spadgett@redhat.com)
- Remove custom SIGQUIT handler (rhcarvalho@gmail.com)
- Use the vendored KUBE_REPO_ROOT (ccoleman@redhat.com)
- Include Kube examples, needed for extended tests (rhcarvalho@gmail.com)
- Update copy-kube-artifacts.sh (rhcarvalho@gmail.com)
- Return the Origin schema for explain (ccoleman@redhat.com)
- Regenerate conversions with stable order (ccoleman@redhat.com)
- UPSTREAM: 20847: Force a dependency order between extensions and api
  (ccoleman@redhat.com)
- UPSTREAM: 20858: Ensure public conversion name packages are imported
  (ccoleman@redhat.com)
- UPSTREAM: 20775: Set kube-proxy arg default values (jliggitt@redhat.com)
- Add kube-proxy config, match upstream proxy startup (jliggitt@redhat.com)
- allow either iptables-based or userspace-based proxy (danw@redhat.com)
- UPSTREAM: 20846: fix group mapping and encoding order: (deads@redhat.com)
- UPSTREAM: 20481: kubectl: a couple of edit fixes (deads@redhat.com)
- mark tests that access the host system as LocalNode (bparees@redhat.com)
- Build secrets isn't using fixture path (ccoleman@redhat.com)
- Test extended in parallel by default (ccoleman@redhat.com)
- UPSTREAM: 20796: SecurityContext tests wrong volume dir (ccoleman@redhat.com)
- UPSTREAM: 19947: Cluster DNS test is wrong (ccoleman@redhat.com)
- Replacing zeroclipboard with clipboard.js #5115 (rhamilto@redhat.com)
- import the AlwaysPull admission controller (pweil@redhat.com)
- GitLab IDP tweaks (jliggitt@redhat.com)
- BuildConfig editor fix (jhadvig@redhat.com)
- Tiny update in HACKING.md (nakayamakenjiro@gmail.com)
- Document requirements on kubernetes clone for cherry-picking.
  (jsafrane@redhat.com)
- Update recycler controller initialization. (jsafrane@redhat.com)
- Removing copyright leftovers (maszulik@redhat.com)
- UPSTREAM: 19365: Retry recycle or delete operation on failure
  (jsafrane@redhat.com)
- UPSTREAM: 19707: Fix race condition in cinder attach/detach
  (jsafrane@redhat.com)
- UPSTREAM: 19600: Fixed cleanup of persistent volumes. (jsafrane@redhat.com)
- example_test can fail due to validations (ccoleman@redhat.com)
- Add option and support for router id offset - this enables multiple
  ipfailover router installations to run within the same cluster. Rebased and
  changes as per @marun and @smarterclayton review comments.
  (smitram@gmail.com)
- Test extended did not compile (ccoleman@redhat.com)
- Unique host check should not delete when route is same (ccoleman@redhat.com)
- UPSTREAM: 20779: Take GVK in SwaggerSchema() (ccoleman@redhat.com)
- sanitize/consistentize how env variables are added to build pods
  (bparees@redhat.com)
- Update tag for Origin Kube (ccoleman@redhat.com)
- Fix typo (rhcarvalho@gmail.com)
- Add custom auth error template (jliggitt@redhat.com)
- fix multiple component error handling (bparees@redhat.com)
- Template test is not reentrant (ccoleman@redhat.com)
- Fix log viewer urls (jliggitt@redhat.com)
- make unit tests work (deads@redhat.com)
- make unit tests work (maszulik@redhat.com)
- eliminate v1beta3 round trip in the fuzzer.  We don't have to go out from
  there, only in (deads@redhat.com)
- move configapi back into its own scheme until we split the group
  (deads@redhat.com)
- refactor admission plugin types to avoid cycles and keep api types consistent
  (deads@redhat.com)
- update code generators (deads@redhat.com)
- make docker registry image auto-provisioning work with new status details
  (deads@redhat.com)
- add CLI helpers to convert lists before display since encoding no longer does
  it (deads@redhat.com)
- remove most of the latest package; it should go away completely
  (deads@redhat.com)
- template encoding/decoding no longer works like it used to (deads@redhat.com)
- add runtime.Object conversion method that works for now, but doesn't span
  groups or versions (deads@redhat.com)
- api type installation (deads@redhat.com)
- openshift launch sequence changed for rebase (deads@redhat.com)
- replacement etcd client (deads@redhat.com)
- oc behavior change by limiting generator scope (deads@redhat.com)
- runtime.EmbeddedObject removed (deads@redhat.com)
- scheme/codec changes (deads@redhat.com)
- API registration changes (deads@redhat.com)
- boring refactors for rebase (deads@redhat.com)
- UPSTREAM: 20736: clear env var check for unit test (deads@redhat.com)
- UPSTREAM: <drop>: make etcd error determination support old client until we
  drop it (deads@redhat.com)
- UPSTREAM: 20730: add restmapper String methods for debugging
  (deads@redhat.com)
- UPSTREAM: <drop>: disable kubelet image GC unit test (deads@redhat.com)
- UPSTREAM: 20648: fix validation error path for namespace (deads@redhat.com)
- UPSTREAM: <carry>: horrible hack for intstr types (deads@redhat.com)
- UPSTREAM: 20706: register internal types with scheme for reference unit test
  (deads@redhat.com)
- UPSTREAM: 20226:
  Godeps/_workspace/src/k8s.io/kubernetes/pkg/conversion/error.go
  (deads@redhat.com)
- UPSTREAM: 20511: let singularization handle non-conflicting ambiguity
  (deads@redhat.com)
- UPSTREAM: 20487: expose unstructured scheme as codec (deads@redhat.com)
- UPSTREAM: 20431: tighten api server installation for bad groups
  (deads@redhat.com)
- UPSTREAM: <drop>: patch for 16146: Fix validate event for non-namespaced
  kinds (deads@redhat.com)
- UPSTREAM: <drop>: merge multiple registrations for the same group
  (deads@redhat.com)
- UPSTREAM: emicklei/go-restful: <carry>: Add "Info" to go-restful ApiDecl
  (ccoleman@redhat.com)
- UPSTREAM: openshift/openshift-sdn: <drop>: minor updates for kube rebase
  (deads@redhat.com)
- UPSTREAM: docker/distribution: <carry>: remove parents on delete
  (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: export app.Namespace
  (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: custom routes/auth
  (agoldste@redhat.com)
- UPSTREAM: docker/distribution: 1050: Exported API functions needed for
  pruning (miminar@redhat.com)
- bump(k8s.io/kubernetes): 9da202e242d8ceedb549332fb31bf1a933a6c6b6
  (deads@redhat.com)
- bump(github.com/docker/docker): 0f5c9d301b9b1cca66b3ea0f9dec3b5317d3686d
  (deads@redhat.com)
- bump(github.com/coreos/go-systemd): b4a58d95188dd092ae20072bac14cece0e67c388
  (deads@redhat.com)
- bump(github.com/coreos/etcd): e0c7768f94cdc268b2fce31ada1dea823f11f505
  (deads@redhat.com)
- describe transitivity of bump commits (deads@redhat.com)
- clean godeps.json (deads@redhat.com)
- transitive bump checker (jliggitt@redhat.com)
- Clarify how to enable coverage report (rhcarvalho@gmail.com)
- Include offset of JSON syntax error (rhcarvalho@gmail.com)
- Move env and volume to a new 'oc set' subcommand (ccoleman@redhat.com)
- Make clean up before test runs more consistent (rhcarvalho@gmail.com)
- Prevent header and toolbar flicker for empty project (spadgett@redhat.com)
- Add GitLab OAuth identity provider (fabio@fh1.ch)
- release notes: incorrect field names will be rejected (pweil@redhat.com)
- Rename system:humans group to system:authenticated:oauth
  (jliggitt@redhat.com)
- Check index.docker.io/v1 when auth.docker.io/token has no auth
  (ccoleman@redhat.com)
- Update markup in chromeless templates to fix log scrolling issues
  (admin@benjaminapetersen.me)
- Adding missing bindata.go (rhamilto@redhat.com)
- Missing loading message on browse pages, only show tables on details tabs
  (jforrest@redhat.com)
- Set up API service and resourceGroupVersion helpers (jliggitt@redhat.com)
- Removing the transition on .sidebar-left for cleaner rendering on resize
  (rhamilto@redhat.com)
- Fix of project name alignment in IE, fixes bug 1304228 (sgoodwin@redhat.com)
- Test insecure TLS without CA for import (ccoleman@redhat.com)
- Admission control plugin to override run-once pod ActiveDeadlineSeconds
  (cewong@redhat.com)
- Fix problem with iOS zoom using the YAML editor (spadgett@redhat.com)
- Web console: editing compute resources limits (spadgett@redhat.com)
- Align edit build config styles with other edit pages (spadgett@redhat.com)
- Move build "rebuild" button to primary actions (spadgett@redhat.com)
- UPSTREAM: 16146: Fix validate event for non-namespaced kinds
  (deads@redhat.com)
- Bug 1304635: fix termination type for oc create route reencrypt
  (mkargaki@redhat.com)
- Bug 1304604: add missing route generator param for path (mkargaki@redhat.com)
- Support readiness checking on recreate strategy (ccoleman@redhat.com)
- Allow values as arguments in oc process (ffranz@redhat.com)
- Implement a mid hook for recreate deployments (ccoleman@redhat.com)
- Allow new-app to create test deployments (ccoleman@redhat.com)
- Force mount path to word break so it works at mobile (jforrest@redhat.com)
- Bug fix:  adding Go installation step, formatting fix (rhamilto@redhat.com)
- Modify buildConfig from web console (jhadvig@redhat.com)
- Bug fixes:  broken link, formatting fixes, addition of missing step
  (rhamilto@redhat.com)
- Preserve labels and annotations during reconcile scc (agladkov@redhat.com)
- Use tags consistently in top-level extended tests descriptions
  (mfojtik@redhat.com)
- Improve namer.GetName (rhcarvalho@gmail.com)
- Fix args check for role and scc modify (nakayamakenjiro@gmail.com)
- UPSTREAM: 19490: Don't print hairpin_mode error when not using Linux bridges
  (danw@gnome.org)
- added property deduping for junitreport (skuznets@redhat.com)
- Fixes #6797  - router flake due to some refactoring done. The probe needs an
  initial delay to allow the router to start up + harden the tests a lil' more
  by waiting for the router to come up and become available.
  (smitram@gmail.com)
- remove unused flag (pweil@redhat.com)
- reverted typo in extended cmd (skuznets@redhat.com)
- Fix kill_all_processes on OS X (cewong@redhat.com)
- declared variables better for RHEL (skuznets@redhat.com)

* Thu Feb 04 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.900
- made login fail with bad token (skuznets@redhat.com)
- Support test deployments (ccoleman@redhat.com)
- logs: return application logs for dcs (mkargaki@redhat.com)
- Constants in web console can be customized with JS extensions
  (ffranz@redhat.com)
- About page, configurable cli download links (ffranz@redhat.com)
- Preserve existing oauth client secrets on startup (jliggitt@redhat.com)
- Bug 1298750 - Force IE document mode to be edge (jforrest@redhat.com)
- Only pass --ginkgo.skip when focus is absent (ccoleman@redhat.com)
- Unify new-app Resolver and Searcher (ccoleman@redhat.com)
- UPSTREAM: 20053: Don't duplicate error prefix (ccoleman@redhat.com)
- new-app should chase a defaulted "latest" tag to the stable ref
  (ccoleman@redhat.com)
- Update web console tab style (spadgett@redhat.com)
- add list feature (tdawson@redhat.com)
- apply builder pod cgroup limits to launched containers (bparees@redhat.com)
- Remove transition, no longer needed, that causes Safari mobile menu flicker
  https://github.com/openshift/origin/issues/6958 Remove extra alert from
  builds page Make spacing consistent by moving <h1>, actions, and labels into
  middle-header Add missing btn default styling to copy-to-clipboard
  (sgoodwin@redhat.com)
- Document how to run test/cmd tests in development (rhcarvalho@gmail.com)
- Use an insecure TLS config for insecure: true during import
  (ccoleman@redhat.com)
- Only load secrets if import needs them (ccoleman@redhat.com)
- Fix both header dropdowns staying open (jforrest@redhat.com)
- script to check our images for security updates (tdawson@redhat.com)
- Add patching tests (jliggitt@redhat.com)
- Build defaults and build overrides admission plugins (cewong@redhat.com)
- Initial build http proxy admission control plugin (deads@redhat.com)
- Bug 1254431 - fix display of ICTs to handle the from subobject
  (jforrest@redhat.com)
- Bug 1275902 - fix help text for name field on create from image
  (jforrest@redhat.com)
- Fix display when build has not started, no startTimestamp exists
  (jforrest@redhat.com)
- Bug 1291535 - alignment of oc commands in next steps page is wrong
  (jforrest@redhat.com)
- UPSTREAM: ugorji/go: <carry>: Fix empty list/map decoding
  (jliggitt@redhat.com)
- Updates to console theme (sgoodwin@redhat.com)
- Bug 1293578 - The Router liveness/readiness probes should always use
  localhost (bleanhar@redhat.com)
- handle .dockercfg and .dockerconfigjson independently (bparees@redhat.com)
- ImageStreamImage returns incorrect image info (ccoleman@redhat.com)
- Replace NamedTagReference with TagReference (ccoleman@redhat.com)
- Don't fetch an is image if we are already in the process of fetching it
  (jforrest@redhat.com)
- Allow different version encoding for custom builds (nagy.martin@gmail.com)
- bump(github.com/openshift/source-to-image):
  f30208380974bdf302263c8a21b3e8a04f0bb909 (gmontero@redhat.com)
- Update java console to 1.0.42 (slewis@fusesource.com)
- UPSTREAM: 19366: Support rolling update to 0 desired replicas
  (dmace@redhat.com)
- Move graph helpers to deploy/api (ccoleman@redhat.com)
- oc: add `create route` subcommands (mkargaki@redhat.com)
- Allow images to be pulled through the Docker registry (ccoleman@redhat.com)
- Remove debug logging from project admission (ccoleman@redhat.com)
- Improve godoc and add validation tests (ccoleman@redhat.com)
- Review 1 - Added indenting and more log info (ccoleman@redhat.com)
- Watch "run" change as part of watchGroup in logViewer to ensure logs run when
  ready (admin@benjaminapetersen.me)
- bump(github.com/openshift/source-to-image):
  91769895109ea8f193f41bc0e2eb6ba83b30a894 (mfojtik@redhat.com)
- Add API Group to UI config (jliggitt@redhat.com)
- Add a customizable interstitial page to select login provider
  (jforrest@redhat.com)
- Update help for docker/config.json secrets (jliggitt@redhat.com)
- Bug 1303012 - Validate the build secret name in new-build
  (mfojtik@redhat.com)
- Add support for coalescing router reloads:   *  second implementation with a
  rate limiting function.   *  Fixes as per @eparis and @smarterclayton review
  comments.      Use duration instead of string/int values. This also updates
  the      usage to only allow values that time.ParseDuration accepts via
  either the infra router command line or via the RELOAD_INTERVAL
  environment variables. (smitram@gmail.com)
- bump(github.com/openshift/openshift-sdn):
  04aafc3712ec4d612f668113285370f58075e1e2 (maszulik@redhat.com)
- Update java console to 1.0.40 (slewis@fusesource.com)
- update kindToResource to match upstream (pweil@redhat.com)
- tweaks and explanation to use move-upstream.sh for rebase (deads@redhat.com)
- Delay fetching of logs on pod, build & deployment until logs are ready to run
  (admin@benjaminapetersen.me)
- bump(github.com/openshift/source-to-image):
  56dd02330716bd0ed94b87236a9989933b490237 (vsemushi@redhat.com)
- Fix js error in truncate directive (jforrest@redhat.com)
- make example imagesource path relative (bparees@redhat.com)
- Add a crashlooping error to oc status and a suggestion (ccoleman@redhat.com)
- Update the image import controller to schedule recurring import
  (ccoleman@redhat.com)
- oc: re-use edit from kubectl (mkargaki@redhat.com)
- oc: support `logs -p` for builds and deployments (mkargaki@redhat.com)
- api: enable serialization tests for Pod{Exec,Attach}Options
  (mkargaki@redhat.com)
- Project request quota admission control (cewong@redhat.com)
- Add environment to the relevant browse pages (jforrest@redhat.com)
- Make image stream import level driven (ccoleman@redhat.com)
- Add support to cli to set and display scheduled flag (ccoleman@redhat.com)
- Add a bucketed, rate-limited queue for periodic events (ccoleman@redhat.com)
- Allow admins to allow unlimited imported tags (ccoleman@redhat.com)
- Add server API config variables to control scheduling (ccoleman@redhat.com)
- API types for addition of scheduled to image streams (ccoleman@redhat.com)
- Update to fedora 23 (dmcphers@redhat.com)
- Edit project display name & description via settings page
  (admin@benjaminapetersen.me)
- UPSTREAM: <carry>: enable daemonsets by default (pweil@redhat.com)
- enable daemonset (pweil@redhat.com)
- oc: generate path-based routes in expose (mkargaki@redhat.com)
- Generated docs, swagger, completions, conversions (jliggitt@redhat.com)
- API group enablement for master/controllers (jliggitt@redhat.com)
- Explicit API version during login (jliggitt@redhat.com)
- API Group Version changes (maszulik@redhat.com)
- Make etcd registries consistent, updates for etcd test tooling changes
  (maszulik@redhat.com)
- API registration (maszulik@redhat.com)
- Change validation to use field.Path and field.ErrorList (maszulik@redhat.com)
- Determine PublicAddress automatically if masterIP is empty or loopback
  (jliggitt@redhat.com)
- Add origin client negotiation (jliggitt@redhat.com)
- Boring rebase changes (jliggitt@redhat.com)
- UPSTREAM: <drop>: Copy kube artifacts (jliggitt@redhat.com)
- UPSTREAM: 20157: Test specific generators for kubectl (jliggitt@redhat.com)
- UPSTREAM: <carry>: allow hostDNS to be included along with ClusterDNS setting
  (maszulik@redhat.com)
- UPSTREAM: 20093: Make annotate and label fall back to replace on patch
  compute failure (jliggitt@redhat.com)
- UPSTREAM: 19988: Fix kubectl annotate and label to use versioned objects when
  operating (maszulik@redhat.com)
- UPSTREAM: <carry>: Keep default generator for run 'run-pod/v1'
  (jliggitt@redhat.com)
- UPSTREAM: <drop>: stop registering versions in reverse order
  (jliggitt@redhat.com)
- UPSTREAM: 19892: Add WrappedRoundTripper methods to round trippers
  (jliggitt@redhat.com)
- UPSTREAM: 19887: Export transport constructors (jliggitt@redhat.com)
- UPSTREAM: 19866: Export PrintOptions struct (jliggitt@redhat.com)
- UPSTREAM: <carry>: remove types.generated.go (jliggitt@redhat.com)
- UPSTREAM: openshift/openshift-sdn: 253: update to latest client API
  (maszulik@redhat.com)
- UPSTREAM: emicklei/go-restful: <carry>: Add "Info" to go-restful ApiDecl
  (ccoleman@redhat.com)
- UPSTREAM: 17922: <partial>: Allow additional groupless versions
  (jliggitt@redhat.com)
- UPSTREAM: 20095: Restore LoadTLSFiles to client.Config (maszulik@redhat.com)
- UPSTREAM: 18653: Debugging round tripper should wrap CancelRequest
  (ccoleman@redhat.com)
- UPSTREAM: 18541: Allow node IP to be passed as optional config for kubelet
  (rpenta@redhat.com)
- UPSTREAM: <carry>: Tolerate node ExternalID changes with no cloud provider
  (sross@redhat.com)
- UPSTREAM: 19481: make patch call update admission chain after applying the
  patch (deads@redhat.com)
- UPSTREAM: revert: fa9f3ea88: coreos/etcd: <carry>: etcd is using different
  version of ugorji (jliggitt@redhat.com)
- UPSTREAM: 18083: Only attempt PV recycling/deleting once, else fail
  permanently (jliggitt@redhat.com)
- UPSTREAM: 19239: Added missing return statements (jliggitt@redhat.com)
- UPSTREAM: 18042: Add cast checks to controllers to prevent nil panics
  (jliggitt@redhat.com)
- UPSTREAM: 18165: fixes get --show-all (ffranz@redhat.com)
- UPSTREAM: 18621: Implement GCE PD dynamic provisioner. (jsafrane@redhat.com)
- UPSTREAM: 18607: Implement OpenStack Cinder dynamic provisioner.
  (jsafrane@redhat.com)
- UPSTREAM: 18601: Implement AWS EBS dynamic provisioner. (jsafrane@redhat.com)
- UPSTREAM: 18522: Close web socket watches correctly (jliggitt@redhat.com)
- UPSTREAM: 17590: correct homedir on windows (ffranz@redhat.com)
- UPSTREAM: 16964: Preserve int64 data when unmarshaling (jliggitt@redhat.com)
- UPSTREAM: <carry>: allow specific, skewed group/versions
  (jliggitt@redhat.com)
- UPSTREAM: 16667: Make HPA Controller use Namespacers (jliggitt@redhat.com)
- UPSTREAM: <carry>: OpenShift 3.0.2 nodes report v1.1.0-alpha
  (ccoleman@redhat.com)
- UPSTREAM: 16067: Provide a RetryOnConflict helper for client libraries
  (maszulik@redhat.com)
- UPSTREAM: 12221: Allow custom namespace creation in e2e framework
  (deads@redhat.com)
- UPSTREAM: 15451: <partial>: Add our types to kubectl get error
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: add kubelet timeouts (maszulik@redhat.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (maszulik@redhat.com)
- UPSTREAM: <carry>: tweak generator to handle conversions in other packages
  (deads@redhat.com)
- UPSTREAM: <carry>: Suppress aggressive output of warning
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: v1beta3 (deads@redhat.com)
- UPSTREAM: <carry>: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: <carry>: Back n forth downward/metadata conversions
  (deads@redhat.com)
- UPSTREAM: <carry>: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: <carry>: reallow the ability to post across namespaces in api
  (pweil@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: SCC (deads@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (deads@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  eda3808d8fe615229f168661fea021a074a34750 (jliggitt@redhat.com)
- bump(github.com/ugorji/go): f1f1a805ed361a0e078bb537e4ea78cd37dcf065
  (maszulik@redhat.com)
- bump(github.com/emicklei/go-restful):
  777bb3f19bcafe2575ffb2a3e46af92509ae9594 (maszulik@redhat.com)
- bump(github.com/coreos/go-systemd): 97e243d21a8e232e9d8af38ba2366dfcfceebeba
  (maszulik@redhat.com)
- bump(github.com/coreos/go-etcd): 003851be7bb0694fe3cc457a49529a19388ee7cf
  (maszulik@redhat.com)
- bump(k8s.io/kubernetes): 4a65fa1f35e98ae96785836d99bf4ec7712ab682
  (jliggitt@redhat.com)
- fix sample usage (bparees@redhat.com)
- Add needed features (tdawson@redhat.com)
- Disable replication testing for MySQL 5.5 (nagy.martin@gmail.com)
- Install iptables-services for dev & dind clusters (marun@redhat.com)
- Check for forbidden error on ImageStreamImport client (cewong@redhat.com)
- Sanitize S2IBuilder tests (rhcarvalho@gmail.com)
- Add container from annotations to options for build log to generate kibana
  url (admin@benjaminapetersen.me)
- status: Report path-based passthrough terminated routes (mkargaki@redhat.com)
- Add extended test for MongoDB. (vsemushi@redhat.com)
- Simplify Makefile for limited parallelization (ccoleman@redhat.com)
- If release binaries exist, extract them instead of building
  (ccoleman@redhat.com)
- Webhooks: use constant-time string secret comparison (elyscape@gmail.com)
- bump(github.com/openshift/source-to-image):
  78f4e4fe283bd9619804da9e929c61f655df6d06 (bparees@redhat.com)
- Send error output from verify-gofmt to stderr to allow piping to xargs to
  clean up (jliggitt@redhat.com)
- Implement submodule init/update in s2i (christian@paral.in)
- guard openshift resource dump (skuznets@redhat.com)
- Add endpoints to oc describe route (agladkov@redhat.com)
- Use docker registry contants (miminar@redhat.com)
- deployapi: remove obsolete templateRef reference (mkargaki@redhat.com)
- Do not remove image after Docker build (rhcarvalho@gmail.com)
- If Docker is installed, run the e2e/integ variant automatically
  (ccoleman@redhat.com)
- UPSTREAM: <drop>: (do not merge) Make upstream tests pass on Mac
  (ccoleman@redhat.com)
- test/cmd/basicresources.sh fails on macs (ccoleman@redhat.com)
- Remove Travis + assets workarounds (ccoleman@redhat.com)
- Implement authenticated image import (ccoleman@redhat.com)
- refactored test-cmd core to use os::cmd functions (skuznets@redhat.com)
- Move limit range help text outside of header on settings page
  (spadgett@redhat.com)
- hello-openshift example: make the ports configurable (v.behar@free.fr)
- new-build support for image source (cewong@redhat.com)
- bump(github.com/blang/semver):31b736133b98f26d5e078ec9eb591666edfd091f
  (ccoleman@redhat.com)
- Do not retry if the UID changes on import (ccoleman@redhat.com)
- Make import-image a bit more flexible (ccoleman@redhat.com)
- UPSTREAM: <drop>: Allow client transport wrappers to support CancelRequest
  (ccoleman@redhat.com)
-  bump(github.com/fsouza/go-dockerclient)
  25bc220b299845ae5489fd19bf89c5278864b050 (bparees@redhat.com)
- restrict project requests to human users: ones with oauth tokens
  (deads@redhat.com)
- Improve display of quota and limits in web console (spadgett@redhat.com)
- cmd tests: fix diagnostics tests (lmeyer@redhat.com)
- Allow --all-namespaces on status (ccoleman@redhat.com)
- don't fail for parsing error (pweil@redhat.com)
- accept diagnostics as args (deads@redhat.com)
- mark validation commands as deprecated (skuznets@redhat.com)
- fix template processing (deads@redhat.com)
- deployapi: make dc selector optional (mkargaki@redhat.com)
- Not every registry has library (miminar@redhat.com)
- Set REGISTRY_HTTP_SECRET (agladkov@redhat.com)
- homogenize tmpdirs (skuznets@redhat.com)
- Add support for --build-secret to oc new-build command (mfojtik@redhat.com)
- WIP: Add extended test for source build secrets (mfojtik@redhat.com)
- Allow to specify secrets used for the build in source (vsemushi@redhat.com)
- Fixed typo in junitreport properties (maszulik@redhat.com)
- Suppress tooltip when hovering over cut-line at top of pod donut
  (spadgett@redhat.com)
- Described oadm prune builds command. (vsemushi@redhat.com)
- Block build cloning when BC is paused (nagy.martin@gmail.com)
- cleanup of extended cleanup traps (deads@redhat.com)
- oadm: should have prune groups cmd (mkargaki@redhat.com)
- Improve message for deprecated build-logs option. (vsemushi@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  fccee2120e9e8662639df6b40f4e1adf07872105 (danw@redhat.com)
- Set REGISTRY_HTTP_ADDR to first specified port (agladkov@redhat.com)
- ignore ctags file (ian.miell@gmail.com)
- Initial addition of image promotion proposal (mfojtik@redhat.com)
- oadm: bump prune deployments description/examples (mkargaki@redhat.com)
- Add annotation information when describing new-app results
  (ccoleman@redhat.com)
- made system logger get real error code (skuznets@redhat.com)
- wire an etcd dump into an API server for debugging (deads@redhat.com)
- add extended all.sh to allow [extended:all] to run all buckets
  (deads@redhat.com)
- diagnostics: add diagnostics from pod perspective (lmeyer@redhat.com)
- Use interfaces to pass config data to admission plugins (cewong@redhat.com)
- Create registry dc with readiness probe (miminar@redhat.com)
- removed global project cache (skuznets@redhat.com)
- Improve data population (ccoleman@redhat.com)
- stop status from checking SA mountable secrets (deads@redhat.com)
- remove outdated validation (skuznets@redhat.com)
- return a error+recommendation to the user on multiple matches, prioritize
  imagestream matches over annotation matches (bparees@redhat.com)
- make test-integration use our etcd (deads@redhat.com)
- Updated troubleshooting guide with information about insecure-registry
  (maszulik@redhat.com)
- DuelingRepliationControllerWarning -> DuelingReplicationControllerWarning
  (ian.miell@gmail.com)
- Updated generated docs (miminar@redhat.com)
- Fix hack/test-go.sh testing packages recursively (jliggitt@redhat.com)
- Expose admission control plugins list and config in master configuration
  (cewong@redhat.com)
- put openshift-f5-router in origin.spec (tdawson@redhat.com)
- add etcdserver launch mechanism (deads@redhat.com)
- Update minimum Docker version (rhcarvalho@gmail.com)
- added system logging utility (skuznets@redhat.com)
- Described oadm prune images command (miminar@redhat.com)
- add caps defaulting (pweil@redhat.com)
- hack/move-upstream now supports extracting true commits (ccoleman@redhat.com)
- bump(github.com/openshift/source-to-image):
  8ec5b0f51f8baa30159c1d8cceb62126bba6f384 (mfojtik@redhat.com)
- bump(fsouza/go-dockerclient): 299d728486342c894e7fafd68e3a4b89623bef1d
  (mfojtik@redhat.com)
- Update lodash to v 3.10.1 (admin@benjaminapetersen.me)
- Implement BuildConfig reaper (nagy.martin@gmail.com)
- clarify build-started message based on buildconfig triggers
  (bparees@redhat.com)
- Lock bootstrap-hover-dropdown version to 2.1.3 (spadgett@redhat.com)
- Enable swift storage backend for the registry (miminar@redhat.com)
- bump(ncw/swift): c54732e87b0b283d1baf0a18db689d0aea460ba3
  (miminar@redhat.com)
- Enable cloudfront storage driver in dockerregistry (miminar@redhat.com)
- bump(AdRoll/goamz/cloudfront): aa6e716d710a0c7941cb2075cfbb9661f16d21f1
  (miminar@redhat.com)
- Use const values as string for defaultLDAP(S)Port (nakayamakenjiro@gmail.com)
- Replace --master option with --config (miminar@redhat.com)
- Enable Azure Blob Storage (spinolacastro@gmail.com)
- bump(Azure/azure-sdk-for-go/storage):
  97d9593768bbbbd316f9c055dfc5f780933cd7fc (spinolacastro@gmail.com)
- Simplify reading of random bytes (rhcarvalho@gmail.com)
- stop etcd from retrying failures (deads@redhat.com)
- created structure for whitelisting directories for govet shadow testing
  (skuznets@redhat.com)
- Adapt to etcd changes from v2.1.2 to v2.2.2 (ccoleman@redhat.com)
- UPSTREAM: coreos/etcd: <carry>: etcd is using different version of ugorji
  (ccoleman@redhat.com)
- bump(github.com/coreos/etcd):b4bddf685b26b4aa70e939445044bdeac822d042
  (ccoleman@redhat.com)
- bump(AdRoll/goamz): aa6e716d710a0c7941cb2075cfbb9661f16d21f1
  (miminar@redhat.com)
- Fix typo as per review comments from @Miciah (smitram@gmail.com)
- Fix old PR #4282 code and tests to use new layout (Spec.*) and fix gofmt
  errors. (smitram@gmail.com)
- Prohibit passthrough route with path (miciah.masters@gmail.com)
- Don't say "will retry in 5s seconds" in push failure message
  (danw@redhat.com)
- fix contrib doc (pweil@redhat.com)

* Mon Jan 18 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.5
- More fixes and tweeks (tdawson@redhat.com)
- Lock ace-builds version to 1.2.2 (spadgett@redhat.com)
- Do not check builds/details in build by strategy admission control
  (cewong@redhat.com)

* Sat Jan 16 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.4
- Fix up net.bridge.bridge-nf-call-iptables after kubernetes breaks it
  (danw@redhat.com)
- admission tests and swagger (pweil@redhat.com)
- UPSTREAM: <carry>: capability defaulting (pweil@redhat.com)
- Fix logic to add Dockerfile to BuildConfig (rhcarvalho@gmail.com)
- Add TIMES=N to rerun integration tests for flakes (ccoleman@redhat.com)
- Fix route serialization flake (mkargaki@redhat.com)
- STI -> S2I (dmcphers@redhat.com)
- Enable PostgreSQL replication tests for RHEL images (nagy.martin@gmail.com)

* Thu Jan 14 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.3
- Bug 1298457 - The link to pv doc is wrong (bleanhar@redhat.com)
- Fix typo in build generator (mfojtik@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  eda3808d8fe615229f168661fea021a074a34750 (dcbw@redhat.com)
- Auto generated bash completions for node-ip kubelet config option
  (rpenta@redhat.com)
- Use KubeletServer.NodeIP instead of KubeletServer.HostnameOverride to set
  node IP (rpenta@redhat.com)
- UPSTREAM: <carry>: Tolerate node ExternalID changes with no cloud provider
  (sross@redhat.com)
- Update certs for router tests (jliggitt@redhat.com)
- Retry adding roles to service accounts in conflict cases
  (jliggitt@redhat.com)
- Include update operation in build admission controller (cewong@redhat.com)
- UPSTREAM: 18541: Allow node IP to be passed as optional config for kubelet
  (rpenta@redhat.com)
- Fix test fixture fields (mkargaki@redhat.com)
- Make `oc cancel-build` to be suggested for `oc stop-build`.
  (vsemushi@redhat.com)
- The default codec should be v1.Codec, not v1beta3 (ccoleman@redhat.com)

* Wed Jan 13 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.2
- Wait for access tokens to be available in clustered etcd
  (jliggitt@redhat.com)
- Add a new image to be used for testing (ccoleman@redhat.com)
- Bug 1263609 - fix oc rsh usage (ffranz@redhat.com)
- Fix HPA default policy (jliggitt@redhat.com)
- oc rsync: expose additional rsync flags (cewong@redhat.com)
- Bug 1248463 - fixes exec help (ffranz@redhat.com)
- Bug 1273708 - mark --all in oc export deprecated in help (ffranz@redhat.com)
- Fix tests for route validation changes (mkargaki@redhat.com)
- Make new-build output BC with multiple sources (rhcarvalho@gmail.com)
- Remove code duplication (rhcarvalho@gmail.com)
- Require tls termination in route tls configuration (mkargaki@redhat.com)
- Fix nw extended test support for skipping build (marun@redhat.com)
- Fix broken switch in usageWithUnits filter (spadgett@redhat.com)
- UPSTREAM: 19481: make patch call update admission chain after applying the
  patch (deads@redhat.com)
- diagnostics: logs and units for origin (lmeyer@redhat.com)
- Update java console to 1.0.39 (slewis@fusesource.com)
- extended tests for jenkins openshift V3 plugin (gmontero@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  da8ad5dc5c94012eb222221d909b2b6fa678500f (dcbw@redhat.com)
- Update for openshift-sdn script installation changes (danw@redhat.com)
- use direct mount for etcd data (deads@redhat.com)
- mark image input source as experimental (bparees@redhat.com)
- made large file behavior smarter (skuznets@redhat.com)
- Revert "Allow parallel image stream importing" (jordan@liggitt.net)
- version now updates FROM (tdawson@redhat.com)
- Fix deployment CLI ops link and make all doc links https
  (jforrest@redhat.com)
- Fix detection of Python projects (rhcarvalho@gmail.com)
- add probe for mongodb template (haowang@redhat.com)
- deal with RawPath field added to url.URL in go1.5 (gmontero@redhat.com)
- Include kube e2e service tests in networking suite (marun@redhat.com)
- Fix replication controller usage in kube e2e tests (marun@redhat.com)
- Enable openshift-sdn sdn node by default (marun@redhat.com)
- Fix dind compatibility with centos/rhel (marun@redhat.com)
- Fix dind compatibility with centos/rhel (marun@redhat.com)
- added junitreport tool (skuznets@redhat.com)
- diagnostics: list diagnostic names in long desc (lmeyer@redhat.com)
- Increase web console e2e login timeout (spadgett@redhat.com)
- Persistent volume claims on the web console (ffranz@redhat.com)
- update extended test to point to correct version tool (skuznets@redhat.com)
- add warning about root user in images (bparees@redhat.com)
- allow parallel image streams (deads@redhat.com)
- Suppress conflict error logging when adding SA role bindings
  (jliggitt@redhat.com)
- BuildConfig envVars in wrong structure in sti build template
  (jhadvig@redhat.com)
- Remove unnecessary type conversions (rhcarvalho@gmail.com)

* Thu Jan 07 2016 Troy Dawson <tdawson@redhat.com> 3.1.1.1
- add option --insecure for oc import-image
  (haoran@dhcp-129-204.nay.redhat.com)
- new-app: search local docker daemon if registry search fails
  (cewong@redhat.com)
- Fix breadcrumb on next steps page (spadgett@redhat.com)
- Enable DWARF debuginfo (tdawson@redhat.com)
- update scripts to respect TMPDIR (deads@redhat.com)
- handle missing dockerfile with docker strategy (bparees@redhat.com)
- Bump kubernetes-topology-graph to 0.0.21 (spadgett@redhat.com)
- Print more enlightening string if test fails (rhcarvalho@gmail.com)
- Add to project catalog legend and accessibility fixes (spadgett@redhat.com)
- tolerate spurious failure during test setup (deads@redhat.com)
- fixed readiness endpoint route listing (skuznets@redhat.com)
- moved tools from cmd/ to tools/ (skuznets@redhat.com)
- Fix scale up button tooltip (spadgett@redhat.com)
- fix deploy test to use actual master (deads@redhat.com)
- Use angular-bootstrap dropdown for user menu (spadgett@redhat.com)
- added bash autocompletion for ldap sync config (skuznets@redhat.com)
- Don't allow clock icon to wrap in image tag table (spadgett@redhat.com)
- diagnostics: improve wording of notes (lmeyer@redhat.com)
- diagnostics: improve master/node config warnings (lmeyer@redhat.com)
- Show scalable deployments on web console overview even if not latest
  (spadgett@redhat.com)
- Use angular-bootstrap uib-prefixed components (spadgett@redhat.com)
- write output to file in e2e core (skuznets@redhat.com)
- Make web console alerts dismissable (spadgett@redhat.com)
- Reenabled original registry's /healthz route (miminar@redhat.com)
- fixed TestEditor output (skuznets@redhat.com)
- added readiness check to LDAP server pod (skuznets@redhat.com)
- diagnostics: avoid some redundancy (lmeyer@redhat.com)
- update auth tests to use actual master (deads@redhat.com)
- fix non-compliant build integration tests (deads@redhat.com)
- Wait until animation finishes to call chart.flush() (spadgett@redhat.com)
- oc: Add more doc and examples in oc get (mkargaki@redhat.com)
- Make KUBE_TIMEOUT take a duration (rhcarvalho@gmail.com)
- examples: Update resource quota README (mkargaki@redhat.com)
- promoted group prune and sync from experimental (skuznets@redhat.com)
- Various accessibility fixes, bumps angular-bootstrap version
  (jforrest@redhat.com)
- Avoid scrollbar flicker on build trends tooltip (spadgett@redhat.com)
- Show empty RCs in some cases on overview when no service
  (spadgett@redhat.com)
- make os::cmd::try_until* output smarter (skuznets@redhat.com)
- Fix tito ldflag manipulation at tag time (sdodson@redhat.com)
- graphapi: Remove dead code and add godoc (mkargaki@redhat.com)
- describe DockerBuildStrategy.DockerfilePath (v.behar@free.fr)
- integration-tests: retry get image on not found error (miminar@redhat.com)
- Wait for user permissions in test-cmd.sh (jliggitt@redhat.com)
- Wait for bootstrap policy on startup (jliggitt@redhat.com)
- Shorten image importer dialTimeout to 5 seconds (jliggitt@redhat.com)
- Increase specificity of CSS .yaml-mode .ace-numeric style
  (spadgett@redhat.com)
- Fix typo in example `oc run` command. (dusty@dustymabe.com)
- deployapi: Necessary refactoring after updating the internal objects
  (mkargaki@redhat.com)
- deployapi: Update generated conversions and deep copies (mkargaki@redhat.com)
- deployapi: Update manual conversions (mkargaki@redhat.com)
- deployapi: Refactor internal objects to match versioned (mkargaki@redhat.com)
- Allow using an image as source for a build (cewong@redhat.com)
- Updating after real world tests (tdawson@redhat.com)
- added os::cmd readme (skuznets@redhat.com)
- fixed caching bug in ldap sync (skuznets@redhat.com)
- update deltafifo usage to match upstream changes (bparees@redhat.com)
- UPSTREAM: 14881: fix delta fifo & various fakes for go1.5.1
  (maszulik@redhat.com)

* Sat Dec 19 2015 Scott Dodson <sdodson@redhat.com> 3.1.1.0
- Fix tito ldflag manipulation at tag time (sdodson@redhat.com)
- Fix oc status unit test (mkargaki@redhat.com)
- Improve web console scaling (spadgett@redhat.com)
- UPSTREAM: <drop>: fixup for 14537 (mturansk@redhat.com)
- Add bash auto-completion for oc, oadm, and openshift to the environments
  created by Vagrant. (bbennett@redhat.com)
- Fix github link when contextDir is set but not git ref (jforrest@redhat.com)
- install which in the base image (bparees@redhat.com)
- UPSTREAM: 18165: fixes get --show-all (ffranz@redhat.com)
- fix extra indentation for bare builds (deads@redhat.com)
- Edit resource YAML in the web console (spadgett@redhat.com)
- Use DeepEqual instead of field by field comparison (rhcarvalho@gmail.com)
- Fix regression: new-app with custom Git ref (rhcarvalho@gmail.com)
- Increase debug logging for image import controller (jliggitt@redhat.com)
- Gather logs for test-cmd (jliggitt@redhat.com)
- UPSTREAM: 18621: Implement GCE PD dynamic provisioner. (jsafrane@redhat.com)
- UPSTREAM: 17747: Implement GCE PD disk creation. (jsafrane@redhat.com)
- UPSTREAM: 18607: Implement OpenStack Cinder dynamic provisioner.
  (jsafrane@redhat.com)
- UPSTREAM: 18601: Implement AWS EBS dynamic provisioner. (jsafrane@redhat.com)
- Fix test-cmd.sh on OSX (jliggitt@redhat.com)
- Web console: Fix edge case scaling to 0 replicas (spadgett@redhat.com)
- correctly determine build pushability for status (deads@redhat.com)
- move imagestream creation to more sensible spot (bparees@redhat.com)
- Avoid generating tokens with leading dashes (jliggitt@redhat.com)
- Show 'none' when there is no builder image. (rhcarvalho@gmail.com)
- status: Add more details for a broken dc trigger (mkargaki@redhat.com)
- diagnose timeouts correctly in error message (skuznets@redhat.com)
- Fix up ClusterNetwork validation. (danw@redhat.com)
- Show warning when --env is used in start-build with binary source
  (mfojtik@redhat.com)
- Fix deployements/stragies anchor link (christophe@augello.be)
- don't output empty strings in logs (bparees@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  e7f0d8be285f73c896ff19455bd03d5189cbe5e6 (dcbw@redhat.com)
- Fix race between Kubelet initialization and plugin creation (dcbw@redhat.com)
- Output more helpful cancel message (jliggitt@redhat.com)
- Use the iptables-based proxier instead of the userland one (danw@redhat.com)
- Delete tag if its history is empty (miminar@redhat.com)
- Remove redundant admin routes (miminar@redhat.com)
- Reenabled registry dc's liveness probe (miminar@redhat.com)
- Refactor of OSO's code (miminar@redhat.com)
- Refactor dockerregistry: prevent a warning during startup
  (miminar@redhat.com)
- Refactor dockerregistry: unify logging style with upstream's codebase
  (miminar@redhat.com)
- Refactor dockerregistry: use registry's own health check (miminar@redhat.com)
- Refactor dockerregistry: adapt to upstream changes (miminar@redhat.com)
- Registry refactor: handle REGISTRY_CONFIGURATION_PATH (miminar@redhat.com)
- unbump(code.google.com/p/go-uuid/uuid): which is obsoleted
  (miminar@redhat.com)
- Always use port 53 as the dns service port. (abutcher@redhat.com)
- Fix service link on route page (spadgett@redhat.com)
- Increase contrast of web console log text (spadgett@redhat.com)
- custom Dockerfile path for the docker build (v.behar@free.fr)
- assets: Fix up the topology view icon colors and lines (stefw@redhat.com)
- Remove static nodes, deprecate --nodes (jliggitt@redhat.com)
- Add PV Provisioner Controller (mturansk@redhat.com)
- Fix for bugz https://bugzilla.redhat.com/show_bug.cgi?id=1290643   o Make
  Forwarded header value rfc7239 compliant.   o Set X-Forwarded-Proto for http
  (if insecure edge terminated routes     are allowed). (smitram@gmail.com)
- UPSTREAM: 14537: Add PersistentVolumeProvisionerController
  (mturansk@redhat.com)
- Fix test failures for scoped and host-overriden routers. (smitram@gmail.com)
- Unit test for hostname override (ccoleman@redhat.com)
- Routers should be able to override the host value on Routes
  (ccoleman@redhat.com)
- added support for recursive testing using test-go (skuznets@redhat.com)
- fixed group detection bug for LDAP prune (skuznets@redhat.com)
- removed tryuntil from test-cmd (skuznets@redhat.com)
- fixed LDAP test file extensions (skuznets@redhat.com)
- Allow image importing to work with proxy (jkhelil@gmail.com)
- oc: Use object name instead of provided arg in cancel-build
  (mkargaki@redhat.com)
- add step for getting the jenkins service ip (bparees@redhat.com)
- fix forcepull setup build config (gmontero@redhat.com)
- Add user/group reapers (jliggitt@redhat.com)
- Make project template use default rolebinding name (jliggitt@redhat.com)
- update missing imagestream message to warning (bparees@redhat.com)
- Temporary fix for systemd upgrade path issues (sdodson@redhat.com)
- Add logging for etcd integration tests (jliggitt@redhat.com)
- Fix the mysql replica extended test (mfojtik@redhat.com)
- Use service port name as route targetPort in 'oc expose service'
  (jliggitt@redhat.com)
- Refactor SCM auth and use of env vars in builders (cewong@redhat.com)
- oc: Cosmetic fixes in oc status (mkargaki@redhat.com)
- allow for test specification from command-line for test-cmd
  (skuznets@redhat.com)
- Change uuid imports to github.com/pborman/uuid (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: remove parents on delete
  (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: export app.Namespace
  (miminar@redhat.com)
- UPSTREAM: docker/distribution: <carry>: custom routes/auth
  (agoldste@redhat.com)
- UPSTREAM: docker/distribution: 1050: Exported API functions needed for
  pruning (miminar@redhat.com)
- bump(github.com/stevvooe/resumable): 51ad44105773cafcbe91927f70ac68e1bf78f8b4
  (miminar@redhat.com)
- bump(github.com/docker/distribution):
  e6c60e79c570f97ef36f280fcebed497682a5f37 (miminar@redhat.com)
- Give user suggestion about new-app on new-project (ccoleman@redhat.com)
- Controllers should always go async on start (ccoleman@redhat.com)
- Clean up docker-in-docker image (marun@redhat.com)
- doc: create glusterfs service to persist endpoints (hchen@redhat.com)
- [RPMs] Add requires on git (sdodson@redhat.com)
- added better output to test-end-to-end/core (skuznets@redhat.com)
- refactored scripts to use hack/text (skuznets@redhat.com)

* Mon Dec 14 2015 Troy Dawson <tdawson@redhat.com> 3.1.0.902
- Include LICENSE in client zips (ccoleman@redhat.com)
- Minor commit validation fixes (ironcladlou@gmail.com)
- remove build-related type fields from internal api (bparees@redhat.com)
- Add godeps commit verification (ironcladlou@gmail.com)
- Retry build logs in start build when waiting for build (mfojtik@redhat.com)
- Create proper client packages for mac and windows (ccoleman@redhat.com)
- update jenkins tutorial for using plugin (gmontero@redhat.com)
- Allow oc new-build to accept zero arguments (ccoleman@redhat.com)
- Fix fallback scaling behavior (ironcladlou@gmail.com)
- Fix deployment e2e flake (mkargaki@redhat.com)
- UPSTREAM: 18522: Close web socket watches correctly (jliggitt@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  8a7e17c0c3eea529955229dfd7b4baefad56633b (rpenta@redhat.com)
- Start SDN controller after running kubelet (rpenta@redhat.com)
- [RPMs] Cleanup kubeplugin path from old sdn-ovs installs (sdodson@redhat.com)
- Fix flakiness in builds extended tests (cewong@redhat.com)
- Add suggestions in oc status (mkargaki@redhat.com)
- status: Report tls routes with unspecified termination type
  (mkargaki@redhat.com)
- Use the dockerclient ClientFromEnv setup (ccoleman@redhat.com)
- Don't show build trends chart scrollbars if not needed (spadgett@redhat.com)
- Prevent y-axis label overlap when filtering build trends chart
  (spadgett@redhat.com)
- Packaging specfile clean up (admiller@redhat.com)
- added prune-groups; refactored rfc2307 ldapinterface (skuznets@redhat.com)
- only expand resources when strictly needed (deads@redhat.com)
- added logging of output for failed builds (ipalade@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  0f33df18b9747ebfe2c337f2bf4443b520a8f2ab (rpenta@redhat.com)
- UPSTREAM: revert: 97bd6c: <carry>: Allow pod start to be delayed in Kubelet
  (rpenta@redhat.com)
- Don't use KubeletConfig 'StartUpdates' channel for blocking kubelet
  (rpenta@redhat.com)
- after live test (tdawson@redhat.com)
- Unload filtered groups from build config chart (spadgett@redhat.com)
- Fix login tests for OSE variants (sdodson@redhat.com)
- Optionally skip builds for dev cluster provision (marun@redhat.com)
- Fix for bugz 1283952 and add a test. (smitram@gmail.com)
- more code (tdawson@redhat.com)
- more code (tdawson@redhat.com)
- Disable delete button for RCs with status replicas (spadgett@redhat.com)
- Web console support for deleting individual builds and deployments
  (spadgett@redhat.com)
- add new options (tdawson@redhat.com)
- UPSTREAM: 18065: Fixed forbidden window enforcement in horizontal pod
  autoscaler (sross@redhat.com)
- more updating of script (tdawson@redhat.com)
- first rough draft (tdawson@redhat.com)
- HACKING.md: clarify meaning and provide proper usage of OUTPUT_COVERAGE
  variable. (vsemushi@redhat.com)

* Tue Dec 08 2015 Scott Dodson <sdodson@redhat.com> 3.1.0.901
- Show build trends chart on build config page (spadgett@redhat.com)
- fix ruby-22 scl enablement (bparees@redhat.com)
- dump build logs on failure (bparees@redhat.com)
- make sure imagestreams are imported before using them with new-app
  (bparees@redhat.com)
- increase build timeout to 60mins (bparees@redhat.com)
- Update config of dind cluster image registry (marun@redhat.com)
- Allow junit output filename to be overridden (marun@redhat.com)
- improved os::cmd handling of test names, timing (skuznets@redhat.com)
- Improve deployment scaling behavior (ironcladlou@gmail.com)
- refactored test/cmd/admin to use wrapper functions (skuznets@redhat.com)
- Create sourcable bash env as part of dind cluster deploy (marun@redhat.com)

* Fri Dec 04 2015 Scott Dodson <sdodson@redhat.com> 3.1.0.900
- Update liveness/readiness probe to always use the /healthz endpoint (on the
  stats port or on port 1936 if the stats are disabled). (smitram@gmail.com)
- Fix incorrect status icon on pods page (spadgett@redhat.com)
- Update rest of controllers to use new ProjectsService controller, remove ng-
  controller directives in templates, all controllers defined in routes, minor
  update to tests (admin@benjaminapetersen.me)
- Remove the tooltip from the delete button (spadgett@redhat.com)
- Add success line to dry run (rhcarvalho@gmail.com)
- Add integration test for router healthz endpoint as per @smarterclayton
  review comments. (smitram@gmail.com)
- UPSTREAM: drop: part of upstream kube PR #15843. (avagarwa@redhat.com)
- UPSTREAM: drop: Fix kube e2e tests in origin. This commit is part of upstream
  kube PR 16360. (avagarwa@redhat.com)
- Bug 1285626 - need to handle IS tag with a from of kind DockerImage
  (jforrest@redhat.com)
- Fix for Bug 1285647 and issue 6025  - Border width will be expanded when long
  value added in Environment Variables for project  - Route link on overview is
  truncated even at wide browser widths (sgoodwin@redhat.com)
- Patch AOS tuned-profiles manpage during build (sdodson@redhat.com)
- Do not print steps for alternative output formats (rhcarvalho@gmail.com)
- UPSTREAM: 17920: Fix frequent kubernetes endpoint updates during cluster
  start (abutcher@redhat.com)
- Add additional route settings to UI (spadgett@redhat.com)
- switch hello-world tests to expect ruby-22 (bparees@redhat.com)
- Upstream: 16728: lengthened pv controller sync period to 10m
  (mturansk@redhat.com)
- Support deleting routes in web console (spadgett@redhat.com)
- oc rsync: pass-thru global command line options (cewong@redhat.com)
- Sync Dockerfile.product from dist-git (sdodson@redhat.com)
- add namespace to field selectors (pweil@redhat.com)
- Use minutes instead of seconds where possible. (vsemushi@redhat.com)
- added volume length check for overriden recycler (mturansk@redhat.com)
- make adding infrastructure SAs easier (deads@redhat.com)
- fixed origin recycler volume config w/ upstream cli flags
  (mturansk@redhat.com)
- oc: Make env use PATCH instead of PUT (mkargaki@redhat.com)
- Prompt before scaling deployments to 0 in UI (spadgett@redhat.com)
- UPSTREAM: 18000: Fix test failure due to days-in-month check. Issue #17998.
  (mkargaki@redhat.com)
- Update install for osdn plugin reorg (danw@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  0d3440e224aeb26a056c0c4c91c30fdbb59588f9 (danw@redhat.com)
- Update various templates to use status-icon (admin@benjaminapetersen.me)
- UPSTREAM: 17973: Validate pod spec.nodeName (jliggitt@redhat.com)
- Rename project service to ProjectsService, update all pre-existing occurances
  (admin@benjaminapetersen.me)
- Hide old deployments in the topology view (spadgett@redhat.com)
- refactored constructors to allow for better code resue with prune-groups
  (skuznets@redhat.com)
- Prevent identical input/output IST in oc new-build (rhcarvalho@gmail.com)
- Add aria-describedby attributes to template parameter inputs
  (spadgett@redhat.com)
- remove url workaround (now at correct s2i level) (gmontero@redhat.com)
- New flag to oc new-build to produce no output (rhcarvalho@gmail.com)
- Fix sr-only text for pod status chart (spadgett@redhat.com)
- Add README.md to examples/db-templates (rhcarvalho@gmail.com)
- Fix test registry resource location (ffranz@redhat.com)
- UPSTREAM: 17886: pod log location must validate container if provided
  (ffranz@redhat.com)
- Background the node service so we handle SIGTERM (sdodson@redhat.com)
- hack/util.sh(delete_large_and_empty_logs): optimize find usage.
  (vsemushi@redhat.com)
- Bug 1281928 - fix image stream tagging for DockerImage type images.
  (maszulik@redhat.com)
- Remove type conversion (rhcarvalho@gmail.com)
- Bug1277420 - show friendly prompt when cancelling a completed build
  (jhadvig@redhat.com)
- Add new-build flag to set output image reference (rhcarvalho@gmail.com)
- Output uppercase, hex, 2-character padded serial.txt (jliggitt@redhat.com)
- Fix test/cmd/admin.shwq (jliggitt@redhat.com)
- Fix template processing multiple values (jliggitt@redhat.com)
- CLI usability - proposed aliases (ffranz@redhat.com)
- overhaul imagestream definitions and update latest (bparees@redhat.com)
- refactored test/cmd/images to use wrapper methods (skuznets@redhat.com)
- added unit testing to existing LDAP sync code (skuznets@redhat.com)
- fix macro order for bundled listing in tito custom builder
  (admiller@redhat.com)
- refactor fedora packaging additions with tito custom builder updates
  (admiller@redhat.com)
- Fedora packaging: (admiller@redhat.com)
- Typo fixes (jhadvig@redhat.com)
- Update templates to use navigateResourceURL filter where appropriate
  (admin@benjaminapetersen.me)
- Update completions (ffranz@redhat.com)
- bump(github.com/spf13/pflag): 08b1a584251b5b62f458943640fc8ebd4d50aaa5
  (ffranz@redhat.com)
- bump(github.com/spf13/cobra): 1c44ec8d3f1552cac48999f9306da23c4d8a288b
  (ffranz@redhat.com)
- Adds .docker/config.json secret example (ffranz@redhat.com)
- refactored test/cmd/basicresources to use wrapper functions
  (skuznets@redhat.com)
- added os::cmd::try_until* (skuznets@redhat.com)
- no redistributable for either fedora or epel (tdawson@redhat.com)
- Skip Daemonset and DaemonRestart as these are not enabled yet and keep
  failing. (avagarwa@redhat.com)
- Retry failed attempts to talk to remote registry (miminar@redhat.com)
- Split UI tests into e2e vs rest_api integration suites (jforrest@redhat.com)
- refactored test/cmd/templates to use wrapper methods (skuznets@redhat.com)
- refactored test/cmd/policy to use wrapper methods (skuznets@redhat.com)
- refactored test/cmd/builds to use wrapper methods (skuznets@redhat.com)
- refactored test/cmd/newapp to use wrapper functions (skuznets@redhat.com)
- refactored test/cmd/help to use wrapper functions (skuznets@redhat.com)
- avoid: no such file error in test-cmd (deads@redhat.com)
- added ldap test client and query tests (skuznets@redhat.com)
- Link in the alert for the newly triggered build (jhadvig@redhat.com)
- reorganized ldaputil error and query code (skuznets@redhat.com)
- refactored test/cmd/export to use wrapper functions (skuznets@redhat.com)
- refactored test/cmd/deployments to use wrapper methods (skuznets@redhat.com)
- refactored test/cmd/volumes to use helper methods (skuznets@redhat.com)
- Update build revision information when building (cewong@redhat.com)
- Enable /healthz irrespective of stats port being enabled/disabled. /healthz
  is available on the stats port or the default stats port 1936 (if stats are
  turned off via --stats-port=0). (smitram@gmail.com)
- refactored test/cmd/secrets to use helper methods (skuznets@redhat.com)
- added cmd util function test to CI (skuznets@redhat.com)
- bump(gopkg.in/asn1-ber.v1): 4e86f4367175e39f69d9358a5f17b4dda270378d
  (jliggitt@redhat.com)
- bump(gopkg.in/ldap.v2): e9a325d64989e2844be629682cb085d2c58eef8d
  (jliggitt@redhat.com)
- Rename github.com/go-ldap/ldap to gopkg.in/ldap.v2 (jliggitt@redhat.com)
- bump(gopkg.in/ldap.v2): b4c9518ccf0d85087c925e4a3c9d5802c9bc7025 (package
  rename) (jliggitt@redhat.com)
- add role reaper (deads@redhat.com)
- Exposes the --token flag in login command help (ffranz@redhat.com)
- allow unknown secret types (deads@redhat.com)
- allow startup of API server only for integration tests (deads@redhat.com)
- bump(github.com/openshift/source-to-image)
  7597eaa168a670767bf2b271035d29b92ab13b5c (cewong@redhat.com)
- refactored hack/test to not use aliases, detect tty (skuznets@redhat.com)
- Refactor pkg/generate/app (rhcarvalho@gmail.com)
- add image-pusher role (deads@redhat.com)
- refactored test-cmd/edit to use new helper methods (skuznets@redhat.com)
- remove db tag from jenkins template (bparees@redhat.com)
- Change default instance size (dmcphers@redhat.com)
- bump the wait for images timeout (bparees@redhat.com)
- dump container logs when s2i incremental tests fail (bparees@redhat.com)
- test non-db sample templates also (bparees@redhat.com)
- Use correct homedir on Windows (ffranz@redhat.com)
- UPSTREAM: 17590: correct homedir on windows (ffranz@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  919e0142fe594ab5115ecf7fa3f7ad4f5810f009 (dcbw@redhat.com)
- Update to new osdn plugin API (dcbw@redhat.com)
- Accept CamelCase versions of TLS config (ccoleman@redhat.com)
- fix git-ls to leverage GIT_SSH for non-git, secret/token access
  (gmontero@redhat.com)
- Bug 1277046 - fixed tagging ImageStreamImage from the same ImageStream to
  point to original pull spec instead of the internal registry.
  (maszulik@redhat.com)
- Get rid of util.StringList (ffranz@redhat.com)
- UPSTREAM: revert: 199adb7: <drop>: add back flag types to reduce noise during
  this rebase (ffranz@redhat.com)
- added start-build parameters to cli.md (ipalade@redhat.com)
- UPSTREAM: 17567: handle the HEAD verb correctly for authorization
  (deads@redhat.com)
- examples/sample-app/README.md: fix commands to simplify user experience.
  (vsemushi@redhat.com)
- Add PostgreSQL replication tests (nagy.martin@gmail.com)
- Allow to override environment and build log level in oc start-build
  (mfojtik@redhat.com)
- Remove hook directory by default in gitserver example (cewong@redhat.com)
- wait for imagestream import before running a build in tests
  (bparees@redhat.com)
- extended tests for docker and sti bc with no outputname defined
  (ipalade@redhat.com)
- The git:// protocol with proxy is not allowed (mfojtik@redhat.com)
- Fix build controller integration test flake (cewong@redhat.com)
- add requester username to project template (deads@redhat.com)
- Fix extended test for start-build (mfojtik@redhat.com)
- prevent go panic when output not specified for build config
  (gmontero@redhat.com)
- fix start-build --from-webhook (cewong@redhat.com)
- SCMAuth: use local proxy when password length exceeds 255 chars
  (cewong@redhat.com)
- Use constants for defaults instead of strings (rhcarvalho@gmail.com)
- Add extended test for proxy (mfojtik@redhat.com)
- Cleanup extended test output some more (nagy.martin@gmail.com)
- Use router's /healtz route for health checks (miminar@redhat.com)
- Unflake MySQL extended test (nagy.martin@gmail.com)
- Add git ls-remote to validate the remote GIT repository (mfojtik@redhat.com)
- Handle openshift.io/build-config.name label as well as buildconfig.
  (vsemushi@redhat.com)
- update the readme (haoran@dhcp-129-204.nay.redhat.com)
- Completions for persistent flags (ffranz@redhat.com)
- UPSTREAM: spf13/cobra 180: fixes persistent flags completions
  (ffranz@redhat.com)
- Generated docs must use the short command name (ffranz@redhat.com)
- UPSTREAM: 17033: Fix default value for StreamingConnectionIdleTimeout
  (avagarwa@redhat.com)
- Fixes bug 1275518 https://bugzilla.redhat.com/show_bug.cgi?id=1275518
  (avagarwa@redhat.com)
- tito builder/tagger cleanup: (admiller@redhat.com)
- stop oc export from exporting SA secrets that aren't round-trippable
  (deads@redhat.com)
- accept new dockercfg format (deads@redhat.com)
- Fix alignment of icon on settings page by overriding patternfly rule
  (sgoodwin@redhat.com)
- spec: Use relative symlinks in bin/ (walters@verbum.org)
- Added readiness probe for Router (miminar@redhat.com)
- Add openshift/origin-gitserver to push-release.sh (cewong@redhat.com)
- To replace Func postfixed identifier with Fn postfixed in e2e extended
  (salvatore-dario.minonne@amadeus.com)
- to add a job test to extended test (salvatore-dario.minonne@amadeus.com)
- Allow kubelet to be configured for dind compat (marun@redhat.com)
- Force network tests to wait until cluster is ready (marun@redhat.com)
- Update dind docs to configure more vagrant memory (marun@redhat.com)
- Run networking sanity checks separately. (marun@redhat.com)
- Add 'redeploy' command to dind cluster script (marun@redhat.com)
- Fix networking extended test suite declaration (marun@redhat.com)
- Skip internet check in network extended test suite (marun@redhat.com)
- Skip sdn node during dev cluster deploy (marun@redhat.com)
- Fix handling of network plugin arg in deployment (marun@redhat.com)
- Ensure deltarpm is used for devcluster deployment. (marun@redhat.com)
- Rename OPENSHIFT_SDN env var (marun@redhat.com)
- Refactor extended networking test script (marun@redhat.com)
- Increase verbosity of networking test setup (marun@redhat.com)
- Deploy ssh by default on dind cluster nodes (marun@redhat.com)
- Fix numeric comparison bug in cluster provisioning (marun@redhat.com)
- Make provisioning output less noisy (marun@redhat.com)
- Retain systemd logs from extended networking tests (marun@redhat.com)
- Allow networking tests to target existing cluster (marun@redhat.com)
- Optionally skip builds during cluster provision (marun@redhat.com)
- Enable parallel dev cluster deployment (marun@redhat.com)
- Disable scheduling for sdn node when provisioning (marun@redhat.com)
- Rename bash functions used for provisioning (marun@redhat.com)
- Doc and env var cleanup for dind refactor (marun@redhat.com)
- Switch docker-in-docker to use systemd (marun@redhat.com)
- fix merge conflicts in filters/resources.js, update bindata
  (gabriel_ruiz@symantec.com)
- add tests for variable expansion (bparees@redhat.com)
- Use assets/config.local.js if present for development config
  (spadgett@redhat.com)
- Fix typos (dmcphers@redhat.com)
- Allow tag already exist when pushing a release (ccoleman@redhat.com)
- Fixes attach example (ffranz@redhat.com)
- UPSTREAM: 17239: debug filepath in config loader (ffranz@redhat.com)
- Allow setting build config environment variables, show env vars on build
  config page (jforrest@redhat.com)
- UPSTREAM: 17236: fixes attach example (ffranz@redhat.com)
- Remove failing Docker Registry client test (ccoleman@redhat.com)
- leverage new source-to-image API around git clone spec validation/correction
  (gmontero@redhat.com)
- Reload proxy rules on firewalld restart, etc (danw@redhat.com)
- Fix serviceaccount in gitserver example yaml (cewong@redhat.com)
- gitserver: return appropriate error when auth fails (cewong@redhat.com)
- provide validation for build source type (bparees@redhat.com)
- Show less output in test-cmd.sh (ccoleman@redhat.com)
- Change the image workdir to be /var/lib/origin (ccoleman@redhat.com)
- bump(github.com/openshift/source-to-image):
  c9985b5443c4a0a0ffb38b3478031dcc2dc8638d (gmontero@redhat.com)
- Add deployment logs to UI (spadgett@redhat.com)
- Push recycler image (jliggitt@redhat.com)
- Prevent sending username containing colon via basic auth
  (jliggitt@redhat.com)
- added test-cmd test wrapper functions and tests (skuznets@redhat.com)
- Dont loop over all the builds / deployments for the config when we get an
  update for one (jforrest@redhat.com)
- Avoid mobile Safari zoom on input focus (spadgett@redhat.com)
- add build pod name annotation to builds (bparees@redhat.com)
- Prevent autocorrect and autocapitilization for some inputs
  (spadgett@redhat.com)
- bump rails test retry timeout (bparees@redhat.com)
- Adding the recycle tool to the specfile (bleanhar@redhat.com)
- Prevent route from overflowing box in mobile Safari (spadgett@redhat.com)
- Update recycler image to use binary (jliggitt@redhat.com)
- bump(go-ldap/ldap): b4c9518ccf0d85087c925e4a3c9d5802c9bc7025
  (skuznets@redhat.com)
- status: Warn about transient deployment trigger errors (mkargaki@redhat.com)
- Updated pv recycler to work with uid:gid (mturansk@redhat.com)
- Set registry service's session affinity (miminar@redhat.com)
- Several auto-completion fixes (ffranz@redhat.com)
- Fixes auto-completion for build config names (ffranz@redhat.com)
- show warning when pod's containers are restarting (deads@redhat.com)
- Change how we store association between builds and ICTs on DCs for the
  console overview (jforrest@redhat.com)
- Point docs at docs.openshift.com/enterprise/latest (sdodson@redhat.com)
- eliminate double bc reporting in status (deads@redhat.com)
- Use a different donut color for pods not ready (spadgett@redhat.com)
- disable --validate flag by default (deads@redhat.com)
- Update CONTRIBUTING.adoc (bpeterse@redhat.com)
- Show deployment status on overview when failed or cancelled
  (spadgett@redhat.com)
- UPSTREAM: revert: 0048df4: <carry>: Disable --validate by default
  (deads@redhat.com)
- add reconcile-cluster-role arg for specifying specific roles
  (deads@redhat.com)
- Reduce number of tick labels in metrics sparkline (spadgett@redhat.com)
- fix openshift client cache for different versions (deads@redhat.com)
- UPSTREAM: 17058: fix client cache for different versions (deads@redhat.com)
- make export-all work in failures (deads@redhat.com)
- Fix build-waiting logic to use polling instead of watcher
  (nagy.martin@gmail.com)
- add APIGroup to role describer (deads@redhat.com)
- UPSTREAM: 17017: stop jsonpath panicing on bad array length
  (deads@redhat.com)
- don't update the build phase once it reaches a terminal state
  (bparees@redhat.com)
- Run registry as non-root user (ironcladlou@gmail.com)
- warn on missing log and metric URLs for console (deads@redhat.com)
- don't show context nicknames that users don't recognize (deads@redhat.com)
- Allow non-alphabetic characters in expression generator (mfojtik@redhat.com)
- WIP - try out upstream e2e (ccoleman@redhat.com)
- add a wordpress template (bparees@redhat.com)
- UPSTREAM: 16945: kubelet: Fallback to api server for pod status
  (mkargaki@redhat.com)
- Bug 1278007 - Use commit instead of HEAD when streaming in start-build
  (mfojtik@redhat.com)
- Move os::util:install-sdn to contrib/node/install-sdn.sh (sdodson@redhat.com)
- Drop selinux relabeling for volumes, add images to push-release
  (sdodson@redhat.com)
- Build controller - set build status only if pod creation succeeds
  (cewong@redhat.com)
- Let users to select log content without line numbers (spadgett@redhat.com)
- pre-set the SA namespaces (deads@redhat.com)
- Add labels and annotations to DeploymentStrategy. (roque@juniper.net)
- containerized-installs -> containerized (sdodson@redhat.com)
- Add example systemd units for running as container (sdodson@redhat.com)
- Add sdn ovs enabled node image (sdodson@redhat.com)
- fix case for events (deads@redhat.com)
- prune: Remove deployer pods when pruning failed deployments
  (mkargaki@redhat.com)
- reenable static building of hello pod (bparees@redhat.com)
- do not make redistributable in fedora (tdawson@redhat.com)
- Make building clients for other architectures optional (tdawson@redhat.com)

* Tue Nov 10 2015 Scott Dodson <sdodson@redhat.com> 3.1.0.4
- change OS bootstrap SCCs to use RunAsAny for fsgroup and sup groups
  (pweil@redhat.com)
- UPSTREAM:<carry>:v1beta3 default fsgroup/supgroup strategies to RunAsAny
  (pweil@redhat.com)
- UPSTREAM:<carry>:default fsgroup/supgroup strategies to RunAsAny
  (pweil@redhat.com)
- UPSTREAM: 17061: Unnecessary updates to ResourceQuota when doing UPDATE
  (decarr@redhat.com)
- Fix typo (dmcphers@redhat.com)
- Update HPA bootstrap policy (sross@redhat.com)
- Run deployer as non-root user (ironcladlou@gmail.com)
- UPSTREAM: 15537: openstack: cache InstanceID and use it for volume
  management. (jsafrane@redhat.com)

* Mon Nov 09 2015 Troy Dawson <tdawson@redhat.com> 3.1.0.3
- Add jenkins status to readme (dmcphers@redhat.com)
- cAdvisor needs access to dmsetup for devicemapper info (ccoleman@redhat.com)
- Make auth-in-container tests cause test failure again (ccoleman@redhat.com)
- UPSTREAM: 16969: nsenter file writer mangles newlines (ccoleman@redhat.com)
- Doc fixes (mkargaki@redhat.com)
- Doc fixes (dmcphers@redhat.com)
- Specify scheme/port for metrics client (jliggitt@redhat.com)
- UPSTREAM: 16926: Enable specifying scheme/port for metrics client
  (jliggitt@redhat.com)
- Test template preservation of integers (jliggitt@redhat.com)
- UPSTREAM: 16964: Preserve int64 data when unmarshaling (jliggitt@redhat.com)
- Given we don't restrict on Travis success.  Make what it does report be 100%%
  reliable and fast.  So when it does fail we know something is truly wrong.
  (dmcphers@redhat.com)
- back project cache with local authorizer (deads@redhat.com)

* Sat Nov 07 2015 Brenton Leanhardt <bleanhar@redhat.com> 3.1.0.2
- bump(github.com/openshift/openshift-sdn)
  d5965ee039bb85c5ec9ef7f455a8c03ac0ff0214 (dcbw@redhat.com)
- Identify the upstream Kube tag more clearly (ccoleman@redhat.com)
- Move etcd.log out of etcd dir (jliggitt@redhat.com)
- Conditionally run extensions controllers (jliggitt@redhat.com)
- Make namespace delete trigger exp resource delete (sross@redhat.com)

* Fri Nov 06 2015 Troy Dawson <tdawson@redhat.com> 3.1.0.1
- Allow in-cluster config for oc (ccoleman@redhat.com)
- deprecation for buildconfig label (bparees@redhat.com)
- Unable to submit subject rolebindings to a v1 server (ccoleman@redhat.com)
- Allow a service account installation (ccoleman@redhat.com)
- UPSTREAM: 16818: Namespace controller should always get latest state prior to
  deletion (decarr@redhat.com)
- UPSTREAM: 16859: Return a typed error for no-config (ccoleman@redhat.com)
- New-app: Set context directory and strategy on source repos specified with
  tilde(~) (cewong@redhat.com)
- update UPGRADE.md (pweil@redhat.com)

* Wed Nov 04 2015 Scott Dodson <sdodson@redhat.com> 3.1.0.0
- add reconcile-sccs command (pweil@redhat.com)
- Guard against servers that return non-json for the /v2/ check
  (ccoleman@redhat.com)
- Added PVController service account (mturansk@redhat.com)
- Disable deployment config detail message updates (ironcladlou@gmail.com)
- updates via github discussions (admin@benjaminapetersen.me)
- UPSTREAM: 16432: fixed pv binder race condition (mturansk@redhat.com)
- Fixes completions (ffranz@redhat.com)
- UPSTREAM: spf13/cobra: fixes filename completion (ffranz@redhat.com)
- Revert 7fc8ab5b2696b533e6ac5bea003e5a0622bdbf58 (jordan@liggitt.net)
- Automatic commit of package [atomic-openshift] release [3.0.2.906].
  (tdawson@redhat.com)
- UPSTREAM: 16384: Large memory allocation with key prefix generation
  (ccoleman@redhat.com)
- Update bash completions (decarr@redhat.com)
- UPSTREAM: 16749: Kubelet serialize image pulls had incorrect default
  (decarr@redhat.com)
- UPSTREAM: 15914: make kubelet images pulls serialized by default
  (decarr@redhat.com)
- New kibanna archive log link on log tab for build & pod
  (admin@benjaminapetersen.me)
- Transfer ImagePullSecrets to deployment hook pods (ironcladlou@gmail.com)
- Copy volume mounts to hook pods (ironcladlou@gmail.com)
- UPSTREAM: 16717: Ensure HPA has valid resource/name/subresource, validate
  path segments (jliggitt@redhat.com)
- Switch back to subnet (dmcphers@redhat.com)
- Inline deployer hook logs (ironcladlou@gmail.com)
- Remove default subnet (dmcphers@redhat.com)
- Disable quay.io test (ccoleman@redhat.com)
- UPSTREAM: 16032: revert origin 03e50db: check if /sbin/mount.nfs is present
  (mturansk@redhat.com)
- UPSTREAM: 16277: Fixed resetting last scale time in HPA status
  (sross@redhat.com)
- Change subnet default (dmcphers@redhat.com)
- Add default subnet back (dmcphers@redhat.com)
- Remove default subnet (dmcphers@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  cb0e352cd7591ace30d592d4f82685d2bcd38a04 (rpenta@redhat.com)
- Disable new-app Git tests in Vagrant (ccoleman@redhat.com)
- oc logs long description is wrong (ffranz@redhat.com)
- scc sort by priority (pweil@redhat.com)
- UPSTREAM:<carry>:v1beta3 scc priority field (pweil@redhat.com)
- UPSTREAM:<carry>:scc priority field (pweil@redhat.com)
- Bug and issue fixes (3) (sgoodwin@redhat.com)
- Fix deploy test conflict flake (ironcladlou@gmail.com)
- Prevent early exit on install-assets failure (jliggitt@redhat.com)
- UPSTREAM: 15997: Prevent NPE in resource printer on HPA (ccoleman@redhat.com)
- UPSTREAM: 16478: Daemon controller shouldn't place pods on not ready nodes
  (ccoleman@redhat.com)
- UPSTREAM: 16340: Kubelet pod status update is not correctly occuring
  (ccoleman@redhat.com)
- UPSTREAM: 16191: Mirror pods don't show logs (ccoleman@redhat.com)
- UPSTREAM: 14182: Distinguish image registry unavailable and pull failure
  (decarr@redhat.com)
- UPSTREAM: 16174: NPE when checking for mounting /etc/hosts
  (ccoleman@redhat.com)
-  Bug 1275537 - Fixed the way image import controller informs about errors
  from imports. (maszulik@redhat.com)
- UPSTREAM: 16052: Control /etc/hosts in the kubelet (ccoleman@redhat.com)
- UPSTREAM: 16044: Don't shadow error in cache.Store (ccoleman@redhat.com)
- UPSTREAM: 16025: Fix NPE in describe of HPA (ccoleman@redhat.com)
- UPSTREAM: 16668: Fix hpa escalation (deads@redhat.com)
- UPSTREAM: 15944: DaemonSet controller modifies the wrong fields
  (ccoleman@redhat.com)
- UPSTREAM: 15414: Annotations for kube-proxy move to beta
  (ccoleman@redhat.com)
- UPSTREAM: 15745: Endpoint timeouts in the proxy are bad (ccoleman@redhat.com)
- UPSTREAM: 15646: DaemonSet validation (ccoleman@redhat.com)
- UPSTREAM: 15574: Validation on resource quota (ccoleman@redhat.com)
- Calculate correct bottom scroll position (spadgett@redhat.com)
- oc tag should retry on conflict errors (ccoleman@redhat.com)
- Remove log arg for travis (jliggitt@redhat.com)
- hack/install-assets: fix nonstandard bash (lmeyer@redhat.com)
- extend role covers with groups (deads@redhat.com)
- Bug 1277021 - Fixed import-image help information. (maszulik@redhat.com)
- Deprecate build-logs in favor of logs (mkargaki@redhat.com)
- Build and deployment logs should check kubelet response (ccoleman@redhat.com)
- DNS services are not resolving properly (ccoleman@redhat.com)
- hack/test-end-to-end.sh won't start on IPv6 system (ccoleman@redhat.com)
- Wait longer for etcd startup in integration tests (ccoleman@redhat.com)
- Restore detailed checking for forbidden exec (jliggitt@redhat.com)
- UPSTREAM: 16711: Read error from failed upgrade attempts
  (jliggitt@redhat.com)
- Only show scroll links when log is offscreen (spadgett@redhat.com)
- Temporarily accept 'Forbidden' and 'forbidden' responses
  (jliggitt@redhat.com)
- Add HPA support for DeploymentConfig (sross@redhat.com)
- UPSTREAM: 16570: Fix GetRequestInfo subresource parsing for proxy/redirect
  verbs (sross@redhat.com)
- UPSTREAM: 16671: Customize HPA Heapster service namespace/name
  (sross@redhat.com)
- Add Scale Subresource to DeploymentConfigs (sross@redhat.com)
- bz 1276319 - Fix oc rsync deletion with tar strategy (cewong@redhat.com)
- UPSTREAM: <carry>: s/imagestraams/imagestreams/ in `oc get`
  (eparis@redhat.com)
- UPSTREAM(go-dockerclient): 408: fix stdin-only attach (agoldste@redhat.com)
- Add error clause to service/project.js (admin@benjaminapetersen.me)
- Switch to checking for CrashLoopBackOff to show the container looping message
  (jforrest@redhat.com)
- Fix namespace initialization (jliggitt@redhat.com)
- UPSTREAM: 16590: Create all streams before copying in exec/attach
  (agoldste@redhat.com)
- UPSTREAM: 16677: Add Validator for Scale Objects (sross@redhat.com)
- UPSTREAM: 16537: attach must only allow a tty when container supports it
  (ffranz@redhat.com)
- Bug 1276602 - fixes error when scaling dc with --timeout (ffranz@redhat.com)
- test/cmd/admin.sh isn't reentrant (ccoleman@redhat.com)
- add group/version serialization to master (deads@redhat.com)
- UPSTREAM: <drop>: allow specific, skewed group/versions (deads@redhat.com)
- UPSTREAM: 16667: Make Kubernetes HPA Controller use Namespacers
  (sross@redhat.com)
- rsync: output warnings to stdout instead of using glog (cewong@redhat.com)
- allow cluster-admin and cluster-reader to use different groups
  (deads@redhat.com)
- UPSTREAM: 16127: Bump cAdvisor (jimmidyson@gmail.com)
- UPSTREAM: 15612: Bump cadvisor (jimmidyson@gmail.com)
- rsync: output warnings to stdout instead of using glog (cewong@redhat.com)
- UPSTREAM: 16223: Concurrency fixes in kubelet status manager
  (ccoleman@redhat.com)
- UPSTREAM: 15275: Kubelet reacts much faster to unhealthy containers
  (ccoleman@redhat.com)
- UPSTREAM: 15706: HorizontalPodAutoscaler and Scale subresource APIs graduated
  to beta (sross@redhat.com)
- Fixed how tags are being printed when describing ImageStream. Previously the
  image.Spec.Tags was ignored, which resulted in not showing the tags for which
  there were errors during imports. (maszulik@redhat.com)

* Wed Nov 04 2015 Troy Dawson <tdawson@redhat.com> 3.0.2.906
- Copy volume mounts to hook pods (ironcladlou@gmail.com)
- UPSTREAM: 16717: Ensure HPA has valid resource/name/subresource, validate
  path segments (jliggitt@redhat.com)
- Switch back to subnet (dmcphers@redhat.com)
- Inline deployer hook logs (ironcladlou@gmail.com)
- Remove default subnet (dmcphers@redhat.com)
- Disable quay.io test (ccoleman@redhat.com)
- UPSTREAM: 16032: revert origin 03e50db: check if /sbin/mount.nfs is present
  (mturansk@redhat.com)
- UPSTREAM: 16277: Fixed resetting last scale time in HPA status
  (sross@redhat.com)
- Change subnet default (dmcphers@redhat.com)
- Add default subnet back (dmcphers@redhat.com)
- Remove default subnet (dmcphers@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  cb0e352cd7591ace30d592d4f82685d2bcd38a04 (rpenta@redhat.com)
- Disable new-app Git tests in Vagrant (ccoleman@redhat.com)
- oc logs long description is wrong (ffranz@redhat.com)
- scc sort by priority (pweil@redhat.com)
- UPSTREAM:<carry>:v1beta3 scc priority field (pweil@redhat.com)
- UPSTREAM:<carry>:scc priority field (pweil@redhat.com)
- Bug and issue fixes (3) (sgoodwin@redhat.com)
- Fix deploy test conflict flake (ironcladlou@gmail.com)
- Prevent early exit on install-assets failure (jliggitt@redhat.com)
- UPSTREAM: 15997: Prevent NPE in resource printer on HPA (ccoleman@redhat.com)
- UPSTREAM: 16478: Daemon controller shouldn't place pods on not ready nodes
  (ccoleman@redhat.com)
- UPSTREAM: 16340: Kubelet pod status update is not correctly occuring
  (ccoleman@redhat.com)
- UPSTREAM: 16191: Mirror pods don't show logs (ccoleman@redhat.com)
- UPSTREAM: 14182: Distinguish image registry unavailable and pull failure
  (decarr@redhat.com)
- UPSTREAM: 16174: NPE when checking for mounting /etc/hosts
  (ccoleman@redhat.com)
-  Bug 1275537 - Fixed the way image import controller informs about errors
  from imports. (maszulik@redhat.com)
- UPSTREAM: 16052: Control /etc/hosts in the kubelet (ccoleman@redhat.com)
- UPSTREAM: 16044: Don't shadow error in cache.Store (ccoleman@redhat.com)
- UPSTREAM: 16025: Fix NPE in describe of HPA (ccoleman@redhat.com)
- UPSTREAM: 16668: Fix hpa escalation (deads@redhat.com)
- UPSTREAM: 15944: DaemonSet controller modifies the wrong fields
  (ccoleman@redhat.com)
- UPSTREAM: 15414: Annotations for kube-proxy move to beta
  (ccoleman@redhat.com)
- UPSTREAM: 15745: Endpoint timeouts in the proxy are bad (ccoleman@redhat.com)
- UPSTREAM: 15646: DaemonSet validation (ccoleman@redhat.com)
- UPSTREAM: 15574: Validation on resource quota (ccoleman@redhat.com)
- Calculate correct bottom scroll position (spadgett@redhat.com)
- oc tag should retry on conflict errors (ccoleman@redhat.com)
- Remove log arg for travis (jliggitt@redhat.com)
- hack/install-assets: fix nonstandard bash (lmeyer@redhat.com)
- extend role covers with groups (deads@redhat.com)
- Bug 1277021 - Fixed import-image help information. (maszulik@redhat.com)
- Deprecate build-logs in favor of logs (mkargaki@redhat.com)
- Build and deployment logs should check kubelet response (ccoleman@redhat.com)
- DNS services are not resolving properly (ccoleman@redhat.com)
- hack/test-end-to-end.sh won't start on IPv6 system (ccoleman@redhat.com)
- Wait longer for etcd startup in integration tests (ccoleman@redhat.com)
- Restore detailed checking for forbidden exec (jliggitt@redhat.com)
- UPSTREAM: 16711: Read error from failed upgrade attempts
  (jliggitt@redhat.com)
- Only show scroll links when log is offscreen (spadgett@redhat.com)
- Temporarily accept 'Forbidden' and 'forbidden' responses
  (jliggitt@redhat.com)
- Add HPA support for DeploymentConfig (sross@redhat.com)
- UPSTREAM: 16570: Fix GetRequestInfo subresource parsing for proxy/redirect
  verbs (sross@redhat.com)
- UPSTREAM: 16671: Customize HPA Heapster service namespace/name
  (sross@redhat.com)
- Add Scale Subresource to DeploymentConfigs (sross@redhat.com)
- bz 1276319 - Fix oc rsync deletion with tar strategy (cewong@redhat.com)
- UPSTREAM: <carry>: s/imagestraams/imagestreams/ in `oc get`
  (eparis@redhat.com)
- UPSTREAM(go-dockerclient): 408: fix stdin-only attach (agoldste@redhat.com)
- Add error clause to service/project.js (admin@benjaminapetersen.me)
- Switch to checking for CrashLoopBackOff to show the container looping message
  (jforrest@redhat.com)
- Fix namespace initialization (jliggitt@redhat.com)
- UPSTREAM: 16590: Create all streams before copying in exec/attach
  (agoldste@redhat.com)
- UPSTREAM: 16677: Add Validator for Scale Objects (sross@redhat.com)
- UPSTREAM: 16537: attach must only allow a tty when container supports it
  (ffranz@redhat.com)
- Bug 1276602 - fixes error when scaling dc with --timeout (ffranz@redhat.com)
- test/cmd/admin.sh isn't reentrant (ccoleman@redhat.com)
- add group/version serialization to master (deads@redhat.com)
- UPSTREAM: <drop>: allow specific, skewed group/versions (deads@redhat.com)
- UPSTREAM: 16667: Make Kubernetes HPA Controller use Namespacers
  (sross@redhat.com)
- rsync: output warnings to stdout instead of using glog (cewong@redhat.com)
- Throttle log updates to avoid UI flicker (spadgett@redhat.com)
- allow cluster-admin and cluster-reader to use different groups
  (deads@redhat.com)
- UPSTREAM: 16127: Bump cAdvisor (jimmidyson@gmail.com)
- UPSTREAM: 15612: Bump cadvisor (jimmidyson@gmail.com)
- Bug 1277017 - Added checking if spec.DockerImageRepository and spec.Tags are
  not empty. (maszulik@redhat.com)
- rsync: output warnings to stdout instead of using glog (cewong@redhat.com)
- Bug 1276657 - Reuse --insecure-registry flag value when creating ImageStream
  from passed docker image. (maszulik@redhat.com)
- Use pficon-info on pod terminal tab (spadgett@redhat.com)
- Bug 1268000 - replace Image.DockerImageReference with value from status.
  (maszulik@redhat.com)
- UPSTREAM: 16223: Concurrency fixes in kubelet status manager
  (ccoleman@redhat.com)
- UPSTREAM: 15275: Kubelet reacts much faster to unhealthy containers
  (ccoleman@redhat.com)
- UPSTREAM: 16033: Mount returns verbose error (ccoleman@redhat.com)
- UPSTREAM: 16032: check if /sbin/mount.nfs is present (ccoleman@redhat.com)
- UPSTREAM: 15555: Use default port 3260 for iSCSI (ccoleman@redhat.com)
- UPSTREAM: 15562: iSCSI use global path to mount (ccoleman@redhat.com)
- UPSTREAM: 15236: Better error output from gluster (ccoleman@redhat.com)
- UPSTREAM: 15706: HorizontalPodAutoscaler and Scale subresource APIs graduated
  to beta (sross@redhat.com)
- Fixed how tags are being printed when describing ImageStream. Previously the
  image.Spec.Tags was ignored, which resulted in not showing the tags for which
  there were errors during imports. (maszulik@redhat.com)
- UPSTREAM: 15961: Add streaming subprotocol negotation (agoldste@redhat.com)
- Systemd throws an error on Restart=Always (sdodson@redhat.com)

* Sun Nov 01 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.905
- Add and test field label conversions (jliggitt@redhat.com)
- logs: View logs from older deployments/builds with --version
  (mkargaki@redhat.com)
- UPSTREAM: 15733: Disable keepalive on liveness probes (ccoleman@redhat.com)
- UPSTREAM: 15845: Add service locator in service rest storage
  (ccoleman@redhat.com)
- install-assets: retry bower update (lmeyer@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  1f449c7f0d3cd41314a895ef119f9d25a15b54de (rpenta@redhat.com)
- Improve UI performance when displaying large logs (spadgett@redhat.com)
- fixes as per @smarterclayton review comments. (smitram@gmail.com)
- new SCCs (pweil@redhat.com)
- UPSTREAM: 16068: Increase annotation size significantly (ccoleman@redhat.com)
- UPSTREAM(go-dockerclient): 408: fix stdin-only attach (agoldste@redhat.com)
- stop creating roles with resourcegroups (deads@redhat.com)
- Fixes as per @smarterclayton and @liggit review comments. (smitram@gmail.com)
- Various style/positioning fixes (sgoodwin@redhat.com)
- Add missing kube resources to bootstrap policy (jliggitt@redhat.com)
- UPSTREAM: <carry>: OpenShift 3.0.2 nodes report v1.1.0-alpha
  (ccoleman@redhat.com)
- UPSTREAM: 16137: Release node port correctly (ccoleman@redhat.com)
- Run serialization tests for upstream types (mkargaki@redhat.com)
- UPSTREAM: <carry>: Update v1beta3 (mkargaki@redhat.com)
- UPSTREAM: 15930: Deletion of pods managed by old kubelets
  (ccoleman@redhat.com)
- UPSTREAM: 15900: Delete succeeded and failed pods immediately
  (ccoleman@redhat.com)
- add istag list, update (deads@redhat.com)
- diagnostics: default server conf paths changed (lmeyer@redhat.com)
- diagnostics: systemd unit name changes (lmeyer@redhat.com)
- Handle passwords with colon in basic auth (pep@redhat.com)
- Bug 1275564 - Removed the requirement for spec.dockerImageRepository from
  import-image command. (maszulik@redhat.com)
- bump(github.com/openshift/source-to-image)
  65d46436ab599633b76e570311a05f46a818389b (mfojtik@redhat.com)
- Add openshift.io/build-config.name label to builds. (vsemushi@redhat.com)
- oc: Use default resources where it makes sense (mkargaki@redhat.com)
- logs: Support all flags for builds and deployments (mkargaki@redhat.com)
- UPSTREAM: <carry>: Update v1beta3 PodLogOptions (mkargaki@redhat.com)
- UPSTREAM: 16494: Remove dead pods upon stopping a job (maszulik@redhat.com)
- Add local IP addresses to node certificate (jliggitt@redhat.com)
- Rest validation of binary builds is more aggressive (ccoleman@redhat.com)
-   o Add support to expose/redirect/disable insecure schemes (http) for
  edge secured routes.   o Add changes to template, haproxy and f5 router
  implementations.   o Add generated* files. (smitram@gmail.com)
- removed unneeded squash and chown from nfs doc (mturansk@redhat.com)
- Only run pod nodeenv admission on create (agoldste@redhat.com)
- fix up latest tags and add new scl image versions (bparees@redhat.com)
- UPSTREAM: 16532: Allow log tail and log follow to be specified together
  (ccoleman@redhat.com)
- Need to be doing a bower update instead of install so dependencies will
  update without conflict (jforrest@redhat.com)
- Update swagger spec (pmorie@gmail.com)
- UPSTREAM: 15799: Fix PodPhase issue caused by backoff (mkargaki@redhat.com)
- watchObject in console triggers callbacks for events of items of the same
  kind (jforrest@redhat.com)
- status: Report routes that have no route port specified (mkargaki@redhat.com)
- Add special casing for v1beta3 DeploymentConfig in serialization_test
  (pmorie@gmail.com)
- UPSTREAM: <carry>: respect fuzzing defaults for v1beta3 SecurityContext
  (pmorie@gmail.com)
- OS integration for PSC (pweil@redhat.com)
- UPSTREAM: <carry>: v1beta3 scc integration for PSC (pweil@redhat.com)
- UPSTREAM: <carry>: scc integration for PSC (pweil@redhat.com)
- UPSTREAM: <carry>: Workaround for cadvisor/libcontainer config schema
  mismatch (pmorie@gmail.com)
- UPSTREAM: 15323: Support volume relabling for pods which specify an SELinux
  label (pmorie@gmail.com)
- Update completions (jimmidyson@gmail.com)
- Test scm password auth (jliggitt@redhat.com)
- Add prometheus exporter to haproxy router (jimmidyson@gmail.com)
- UPSTREAM: 16332: Remove invalid blank line when printing jobs
  (maszulik@redhat.com)
- UPSTREAM: 16234: Fix jobs unittest flakes (maszulik@redhat.com)
- UPSTREAM: 16196: Fix e2e test flakes (maszulik@redhat.com)
- UPSTREAM: 15791: Update master service ports and type via controller.
  (abutcher@redhat.com)
- Add dns ports to the master service (abutcher@redhat.com)
- UPSTREAM: 15352: FSGroup implementation (pmorie@gmail.com)
- UPSTREAM: 14705: Inline some SecurityContext fields into PodSecurityContext
  (pmorie@gmail.com)
- UPSTREAM: 14991: Add Support for supplemental groups (pmorie@gmail.com)
- Allow processing template from different namespace (mfojtik@redhat.com)
- changed build for sti and docker to use OutputDockerImageReference, fixed
  tests (ipalade@redhat.com)
- Bug 1270728 - username in the secret don't override the username in the
  source URL (jhadvig@redhat.com)
- UPSTREAM: 15520: Move job to generalized label selector (maszulik@redhat.com)
- Update openshift-object-describer to 1.1.1 (jforrest@redhat.com)

* Thu Oct 29 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.904
- Based on origin v1.0.7
- Provide informational output in new-app and new-build (ccoleman@redhat.com)
- Revert 'Retry ISM save upon conflicting IS error' commit upon retry mechanism
  introduced in ISM create method (maszulik@redhat.com)
- Bug 1275003: expose: Set route port based on service target port
  (mkargaki@redhat.com)
- Improve generation of name based on a git repo url to make it valid.
  (vsemushi@redhat.com)
- UPSTREAM: 16080: Convert from old mirror pods (1.0 to 1.1)
  (ccoleman@redhat.com)
- UPSTREAM: 15983: Store mirror pod hash in annotation (ccoleman@redhat.com)
- Slightly better output order in the CLI for login (ccoleman@redhat.com)
- Attempt to find merged parent (ccoleman@redhat.com)
- Fix extended tests for --from-* binary (ccoleman@redhat.com)
- Completions (ffranz@redhat.com)
- UPSTREAM: 16482: stdin is not a file extension for bash completions
  (ffranz@redhat.com)
- Bump angular-pattern to version 2.3.4 (spadgett@redhat.com)
- Use cmdutil.PrintSuccess to print objects (ffranz@redhat.com)
- Improve the error messages when something isn't found (ccoleman@redhat.com)
- UPSTREAM: 16445: Capitalize and expand UsageError message
  (ccoleman@redhat.com)
- Updates to address several issues (sgoodwin@redhat.com)
- Refactor to use ExponentialBackoff (ironcladlou@gmail.com)
- bump(github.com/openshift/openshift-sdn)
  c08ebda0774795eec624b5ce9063662b19959cf3 (rpenta@redhat.com)
- Auto-generated docs/bash-completions for 'oadm pod-network make-projects-
  global' (rpenta@redhat.com)
- Show empty deployments on overview if latest (spadgett@redhat.com)
- Support retrying mapping creation on conflict (ironcladlou@gmail.com)
- Support installation via containers in new-app (ccoleman@redhat.com)
- Disable create form inputs and submit button while the API request is
  happening (jforrest@redhat.com)
- fix project request with quota (deads@redhat.com)
- UPSTREAM: 16441: Pass runtime.Object to Helper.Create/Replace
  (deads@redhat.com)
- Slim down the extended tests (ccoleman@redhat.com)
- upper case first letter of status message (bparees@redhat.com)
- Rsync fixes (cewong@redhat.com)
- better error message for missing dockerfile (bparees@redhat.com)
- add verbose logging to new-app flake and remove extraneous tryuntil logging
  (bparees@redhat.com)
- Support --binary on new-build (ccoleman@redhat.com)
- Fix text-overflow issue on Safari (sgoodwin@redhat.com)
- bump(github.com/openshift/source-to-image)
  9728b53c11218598acb2cc1b9c8cc762c36f44bc (cewong@redhat.com)
- Include name of port in pod template, switch to port/protocol format
  (jforrest@redhat.com)
- Various logs fixes: (admin@benjaminapetersen.me)
- add --context-dir flag to new-build (bparees@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  22b9a4176435ac4453c30c53799338979ef79050 (rpenta@redhat.com)
- Adding border above builds without a service so that they look more
  connected. (sgoodwin@redhat.com)
- Updates to the log-view so that it's more inline with pod terminal. And
  switch to more subtle ellipsis loader. (sgoodwin@redhat.com)
- Expose all container ports creating from source in the UI
  (spadgett@redhat.com)
- Fail if timeout is reached (ccoleman@redhat.com)
- UPSTREAM: 15975: Validate names in BeforeCreate (jliggitt@redhat.com)
- Bug 1275234 - fixes --resource-version error in scale (ffranz@redhat.com)
- skip project validation when creating a new-project (deads@redhat.com)
- Show route target port in the routes table if its set (jforrest@redhat.com)
- Allow users to click monopod donut charts on overview (spadgett@redhat.com)
- Add verbose output to test execution (marun@redhat.com)
- Show warning popup when builds have a status message (jforrest@redhat.com)
- UPSTREAM: 16241: Deflake wsstream stream_test.go (ccoleman@redhat.com)
- Read kubernetes remote from git repository. (maszulik@redhat.com)
- Fix dind vagrant provisioning and test execution (marun@redhat.com)
- Bug 1261548 - oc run --attach support for DeploymentConfig
  (ffranz@redhat.com)
- Use server time for end time in metrics requests (spadgett@redhat.com)
- Fix typo (jliggitt@redhat.com)
- Update angular-patternfly to version 2.3.3 (spadgett@redhat.com)
- UPSTREAM: 16109: expose attachable pod discovery in factory
  (ffranz@redhat.com)
- libvirt use nfs for dev cluster synced folder (marun@redhat.com)
- report a warning and do not continue on a partial match (bparees@redhat.com)
- Move the cgroup regex to package level. (roque@juniper.net)
- UPSTREAM: 16286: Avoid CPU hotloop on client-closed websocket
  (jliggitt@redhat.com)
- Increase vagrant memory default by 512mb (marun@redhat.com)
- Source dind script from the docker repo (marun@redhat.com)
- dind: Fix disabling of sdn node scheduling (marun@redhat.com)
- Switch dind image to use fedora 21 (marun@redhat.com)
- Only run provision-full.sh for single-vm clusters (marun@redhat.com)
- Fix extended network test invocation (marun@redhat.com)
- Invoke docker with sudo when archiving test logs (marun@redhat.com)
- Enhance dind vagrant deployment (marun@redhat.com)
- Add dind detail to the contribution doc (marun@redhat.com)
- Enhance dind-cluster.sh documentation (marun@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  1e4edc9abb6bb8ac7e5cd946ddec4c10cc714d67 (danw@redhat.com)
- Add rsync daemon copy strategy for windows support (cewong@redhat.com)
- UPSTREAM: 11694: http proxy support for exec/pf (agoldste@redhat.com)
- hack/cherry-pick.sh: fix typo (agoldste@redhat.com)
- hack/cherry-pick.sh: support binary files in diffs (agoldste@redhat.com)
- Added job policy (maszulik@redhat.com)
- platformmanagement_public_514 - Allow importing tags from ImageStreams
  pointing to external registries. (maszulik@redhat.com)
- Minor fix for nfs readme (liangxia@users.noreply.github.com)
- delete: Remove both image stream spec and status tags (mkargaki@redhat.com)
- move newapp commands that need docker into extended tests
  (bparees@redhat.com)
- Only watch pod statuses for overview donut chart (spadgett@redhat.com)
- Vagrantfile should allow multiple sync folders (ccoleman@redhat.com)
- Fix context dir for STI (ccoleman@redhat.com)
- Fixing typos (dmcphers@redhat.com)
- Deflake test/cmd/newapp.sh (ccoleman@redhat.com)
- Review comments (ccoleman@redhat.com)
- Docs (ccoleman@redhat.com)
- Completions (ccoleman@redhat.com)
- Generated conversions (ccoleman@redhat.com)
- Docker and STI builder images support binary extraction (ccoleman@redhat.com)
- Enable binary build endpoint and CLI via start-build (ccoleman@redhat.com)
- UPSTREAM: 15053<carry>: Conversions for v1beta3 (ccoleman@redhat.com)
- UPSTREAM: 15053: Support stdinOnce and fix attach (ccoleman@redhat.com)
- Disable all e2e portforward tests (ccoleman@redhat.com)
- Fixes infinite loop on login and forces auth when password were provided
  (ffranz@redhat.com)
- increase timeout for helper pods (bparees@redhat.com)
- bump(github.com/openshift/source-to-image)
  84e4633329181926ec8d746e189769522b1ff6a7 (roque@juniper.net)
- When running as a pod, pass the network context to source-to-image.
  (roque@juniper.net)
- allow dockersearcher to be setup after config is parsed (bparees@redhat.com)
- UPSTREAM: <carry>: Back n forth downward/metadata conversions
  (maszulik@redhat.com)
- Ensure no overlap between SDN cluster network and service/portal network
  (rpenta@redhat.com)
- [RPMS] expand obsoletes to include OSE versions (sdodson@redhat.com)
- [RPMS] bump docker requirement to 1.8.2 (sdodson@redhat.com)
- UPSTREAM: 15194: Avoid spurious "Hairpin setup failed..." errors
  (danw@gnome.org)
- Change to healthz as per @liggit comments. (smitram@gmail.com)
- Add a monitoring uri to the stats port. This allows us to not affect hosted
  backends but rather use the listener on the stats port to service health
  check requests. Of course the side effect here is that if you turn off stats,
  then the monitoring uri will not be available. (smitram@gmail.com)

* Fri Oct 23 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.903
- Revert "bump(github.com/openshift/openshift-sdn):
  699716b85d1ac5b2f3e48969bbdbbb2a1266e9d0" (sdodson@redhat.com)
- More cleanup of the individual pages, use the extra space better
  (jforrest@redhat.com)
- don't attempt to call create on files that don't exist (bparees@redhat.com)
- Use remove() rather than html('') to empty SVG element (spadgett@redhat.com)
- enable storage interface functions (deads@redhat.com)
- Retry ISM save upon conflicting IS error (maszulik@redhat.com)
- assets: Update topology-graph widget (stefw@redhat.com)
- logs: Re-use from upstream (mkargaki@redhat.com)
- assets: Use $evalAsync when updating topology widget (stefw@redhat.com)
- Handle data gaps when calculating CPU usage in UI (spadgett@redhat.com)
- add SA and role for job and hpa controllers (deads@redhat.com)
- UPSTREAM: 16067: Provide a RetryOnConflict helper for client libraries
  (maszulik@redhat.com)
- UPSTREAM: 10707: logs: Use resource builder (mkargaki@redhat.com)
- Update pod status chart styles (spadgett@redhat.com)
- rework how allow-missing-images resolves (bparees@redhat.com)
- bump(github.com/docker/spdystream): 43bffc4 (agoldste@redhat.com)
- Remove unused godep (agoldste@redhat.com)
- Increase height of metrics utilization sparkline (spadgett@redhat.com)
- Disable a known broken test (ccoleman@redhat.com)
- UID repair should not fail when out of range allocation (ccoleman@redhat.com)
- Add v1beta3 removal notes to UPGRADE.md (ironcladlou@gmail.com)
- Add iptables to origin image (sdodson@redhat.com)
- policy changes for extensions (deads@redhat.com)
- enable extensions (deads@redhat.com)
- UPSTREAM: 7f6f85bd7b47db239868bcd868ae3472373a4f05: fixes attach broken
  during the refactor (ffranz@redhat.com)
- UPSTREAM: 16042: fix missing error handling (deads@redhat.com)
- UPSTREAM: 16084: Use NewFramework in all tests (ccoleman@redhat.com)
- e2e: Verify service account token and log cli errors (ccoleman@redhat.com)
- add commands for managing SCCs (deads@redhat.com)
- Allow patching events (jliggitt@redhat.com)
- Fix problems with overview donut chart on IE (spadgett@redhat.com)
- Bug 1274200: Prompt by default when deleting a non-existent tag
  (mkargaki@redhat.com)
- correct htpasswd error handling: (deads@redhat.com)
- Set build.status.reason on error (rhcarvalho@gmail.com)
- Fixes several issues with tabbed output (ffranz@redhat.com)
- Referenced tags should get updated on a direct tag (ccoleman@redhat.com)
- oc tag should take an explicit reference to ImageStreamImage
  (ccoleman@redhat.com)
- Add back a fix for the libvirt dev_cluster case (danw@redhat.com)
- Completions (ccoleman@redhat.com)
- Fixes 'oc edit' file blocking on windows (ffranz@redhat.com)
- On Windows, use CRLF line endings in oc edit (ccoleman@redhat.com)
- Add iptables requirement to openshift package (sdodson@redhat.com)
- Remove extra copy of main.css from bindata (jforrest@redhat.com)
- add grace period for evacuate (pweil@redhat.com)
- Remove "Pod" prefix from header on browse pod page (spadgett@redhat.com)
- Only try to update build if status message changed (rhcarvalho@gmail.com)
- Show status details for a DC in both the deployments table and DC pages
  (jforrest@redhat.com)
- Bug 1273787 - start deployment btn doesnt get enabled after dep finishes
  (jforrest@redhat.com)
- UPSTREAM: Proxy: do not send X-Forwarded-Host or X-Forwarded-Proto with an
  empty value (cewong@redhat.com)
- handle new non-resource urls (deads@redhat.com)
- UPSTREAM: 15958: add nonResourceURL detection (deads@redhat.com)
- expose: Set route port (mkargaki@redhat.com)
- UPSTREAM: 15461: expose: Enable exposing multiport objects
  (mkargaki@redhat.com)

* Wed Oct 21 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.902
- Revert "Support deleting image stream status tags" (ccoleman@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  699716b85d1ac5b2f3e48969bbdbbb2a1266e9d0 (danw@redhat.com)
- Adjust line-height of route link to avoid clipping (spadgett@redhat.com)
- Support deleting image stream status tags (kargakis@tuta.io)
- tag: Support deleting a tag with -d (mkargaki@redhat.com)
- Bump K8s label selector to next version (sgoodwin@redhat.com)
- Add a container terminal to the pod details page (stefw@redhat.com)
- Remove old labels rendering from individual pages since its duplicate info
  (jforrest@redhat.com)
- Remove duplicate bootstrap.js from dependencies (spadgett@redhat.com)
- updated LDIF and tests (skuznets@redhat.com)
- Bug 1273350 - make click open the secondary nav instead of navigating
  (jforrest@redhat.com)
- Update label key/value pairs truncate at <769. Fixes
  https://github.com/openshift/origin/issues/5181 (sgoodwin@redhat.com)
- remove the deprecated build label on pods (bparees@redhat.com)
- UPSTREAM: 15621: Correctly handle empty source (ccoleman@redhat.com)
- UPSTREAM: 15953: Return unmodified error from negotiate (ccoleman@redhat.com)
- Fix exposing deployment configs (mkargaki@redhat.com)
- Remove code duplication (rhcarvalho@gmail.com)
- Fix patternfly CSS ordering (spadgett@redhat.com)
- Initial impl of viewing logs in web console (admin@benjaminapetersen.me)
- This commit implements birthcry for openshift proxy. This also addresses
  rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1270474
  (avagarwa@redhat.com)
- Bug 1271989 - error when navigating to resources in diff projects
  (jforrest@redhat.com)
- fix --config flag (deads@redhat.com)
- client side changes for deployment logs (mkargaki@redhat.com)
- server side changes for deployment logs (mkargaki@redhat.com)
- api changes for deployment logs (mkargaki@redhat.com)
- Disable new upstream e2e tests (ccoleman@redhat.com)
- Remove authentication from import (ccoleman@redhat.com)
- Web console scaling (spadgett@redhat.com)
- Bug 1268891 - pods not always grouped when service selector should cover
  template of a dc/deployment (jforrest@redhat.com)
- ImageStream status.dockerImageRepository should always be local
  (ccoleman@redhat.com)
- remove kubectl apply from oc (deads@redhat.com)
- UPSTREAM: <drop>: disable kubectl apply until there's an impl
  (deads@redhat.com)
- Add ng-cloak to navbar to reduce flicker on load (spadgett@redhat.com)
- Disable v1beta3 in REST API (ironcladlou@gmail.com)
- help unit tests compile (maszulik@redhat.com)
- refactors (deads@redhat.com)
- UPSTREAM: openshift-sdn(TODO): update for iptables.New call
  (deads@redhat.com)
- UPSTREAM: openshift-sdn(TODO): handle boring upstream refactors
  (deads@redhat.com)
- UPSTREAM: 12221: Allow custom namespace creation in e2e framework
  (deads@redhat.com)
- UPSTREAM: 15807: Platform-specific setRLimit implementations
  (jliggitt@redhat.com)
- UPSTREAM: TODO: expose ResyncPeriod function (deads@redhat.com)
- UPSTREAM: 15451 <partial>: Add our types to kubectl get error
  (ccoleman@redhat.com)
- UPSTREAM: 14496: deep-copies: Structs cannot be nil (mkargaki@redhat.com)
- UPSTREAM: 11827: allow permissive SA secret ref limitting (deads@redhat.com)
- UPSTREAM: 12498: Re-add timeouts for kubelet which is not in the upstream PR.
  (deads@redhat.com)
- UPSTREAM: 15232: refactor logs to be composeable (deads@redhat.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (deads@redhat.com)
- UPSTREAM: <drop>: tweak generator to handle conversions in other packages
  (deads@redhat.com)
- UPSTREAM: <drop>: make test pass with old codec (deads@redhat.com)
- UPSTREAM: <drop>: add back flag types to reduce noise during this rebase
  (deads@redhat.com)
- UPSTREAM: <none>: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: <none>: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: <carry>: v1beta3 (deads@redhat.com)
- UPSTREAM: <carry>: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: <carry>: Back n forth downward/metadata conversions
  (deads@redhat.com)
- UPSTREAM: <carry>: Disable --validate by default (mkargaki@redhat.com)
- UPSTREAM: <carry>: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: <carry>: reallow the ability to post across namespaces in api
  (pweil@redhat.com)
- UPSTREAM: <carry>: helper methods paralleling old latest fields
  (deads@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: SCC (deads@redhat.com)
- UPSTREAM: <carry>: Allow pod start to be delayed in Kubelet
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (deads@redhat.com)
- bump(k8s.io/kubernetes): 4c8e6f47ec23f390978e651232b375f5f9cde3c7
  (deads@redhat.com)
- bump(github.com/coreos/go-etcd): de3514f25635bbfb024fdaf2a8d5f67378492675
  (deads@redhat.com)
- bump(github.com/ghodss/yaml): 73d445a93680fa1a78ae23a5839bad48f32ba1ee
  (deads@redhat.com)
- bump(github.com/fsouza/go-dockerclient):
  1399676f53e6ccf46e0bf00751b21bed329bc60e (deads@redhat.com)
- bump(github.com/prometheus/client_golang):
  3b78d7a77f51ccbc364d4bc170920153022cfd08 (deads@redhat.com)
- Change api version in example apps (jhadvig@redhat.com)
- Bug 1270185 - service link on route details page missing project name
  (jforrest@redhat.com)
- make cherry-pick.sh easier to work with (deads@redhat.com)
- Minor deployment describer formatting fix (ironcladlou@gmail.com)
- Fix deployment config minor ui changes. (sgoodwin@redhat.com)
- Several fixes to the pods page (jforrest@redhat.com)
- test/cmd/export.sh shouldn't dump everything to STDOUT (ccoleman@redhat.com)
- Use the privileged SCC for all kube e2e tests (ccoleman@redhat.com)
- Preserve case of subresources when normalizing URLs (jliggitt@redhat.com)
- Output less info on hack/test-cmd.sh failures (ccoleman@redhat.com)
- Disable potentially insecure TLS cipher suites by default
  (ccoleman@redhat.com)
- Raw sed should not be used in hack/* scripts for Macs (ccoleman@redhat.com)
- Show container metrics in UI (spadgett@redhat.com)
- Fix provisions to be overrides (dmcphers@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  62ec906f6563828364474ef117371ea2ad804dc8 (danw@redhat.com)
- UPSTREAM: Fix non-multitenant pod routing (sdodson@redhat.com)
- Make image trigger test more reliable (ironcladlou@gmail.com)
- [RPMS] atomic-openshift services use openshift bin (sdodson@redhat.com)
- [RPMS] fix rpm build related to sdn restructure (sdodson@redhat.com)
- Fix fuzzing versions in serialization tests (pmorie@gmail.com)
- Show labels on all individual pages. Add label filtering to build config and
  deployment config pages. (jforrest@redhat.com)
- Provide initialized cloud provider in Kubelet config. (jsafrane@redhat.com)
- Fixes to the warning returned by the dc controller (mkargaki@redhat.com)
- Fix govet error (jliggitt@redhat.com)
- adding keystone IdP (sseago@redhat.com)
- Bug 1259260 - when searching docker registry, should not exit in case of no
  matches (ffranz@redhat.com)
- Fix asset config warning (jliggitt@redhat.com)
- Configurable identity mapper strategies (jliggitt@redhat.com)
- Bump proxy resync from 30s to 10m (agoldste@redhat.com)
- Convert secondary nav to a hover menu (sgoodwin@redhat.com)
- remove useless ginkgo test for LDAP (skuznets@redhat.com)
- Sample app readme update (jhadvig@redhat.com)
- Fix s2i build with environment file extended test (mfojtik@redhat.com)
- Return error instead of generating arbitrary names (rhcarvalho@gmail.com)
- Replace local constant with constant from Kube (rhcarvalho@gmail.com)
- Godoc formatting (rhcarvalho@gmail.com)
- Print etcd version when calling openshift version (mfojtik@redhat.com)
- Use cmdutil.PrintSuccess() to display bulk output (ccoleman@redhat.com)
- Add SNI support (jliggitt@redhat.com)
- make ldap sync job accept group/foo whitelists (deads@redhat.com)
- move bash_completion.d/oc to clients package (tdawson@redhat.com)
- Add a cluster diagnostic to check if master is also running as a node.
  (dgoodwin@redhat.com)
- Update the hacking guide (mkargaki@redhat.com)
- add examples for rpm-based installs (jeder@redhat.com)
- Add fibre channel guide (hchen@redhat.com)
- Add Cinder Persistent Volume guide (jsafrane@redhat.com)
- Move NFS documentation to a subchapter. (jsafrane@redhat.com)
- Add environment values to oc new-app help for mysql
  (nakayamakenjiro@gmail.com)
- Update oadm router and registry help message (nakayamakenjiro@gmail.com)
- Enable cpu cfs quota by default (decarr@redhat.com)
- Gluster Docs (screeley@redhat.com)

* Wed Oct 14 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.901
- Build transport for etcd directly (jliggitt@redhat.com)
- Remove volume dir chcon from e2e-docker (agoldste@redhat.com)
- Always try to chcon the volume dir (agoldste@redhat.com)
- Filter service endpoints when using multitenant plugin (danw@redhat.com)
- Update for osdn plugin argument changes (danw@redhat.com)
- Updated generated docs for openshift-sdn changes (danw@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  5a41fee40db41b65578c07eff9fef35d183dce1c (danw@redhat.com)
- Generalize move-upstream.sh (ccoleman@redhat.com)
- Add links to things from the overview and pod template (jforrest@redhat.com)
- deconflict swagger ports (deads@redhat.com)
- Scan for selinux write error in registry diagnostic. (dgoodwin@redhat.com)
- Report transient deployment trigger errors via API field
  (mkargaki@redhat.com)
- Add build timeout, by setting ActiveDeadlineSeconds on a build pod
  (maszulik@redhat.com)
- Update completions (ffranz@redhat.com)
- Append missing flags to cobra flags (jchaloup@redhat.com)
- added an LDAP host label (skuznets@redhat.com)
- add openshift group mapping for ldap sync (deads@redhat.com)
- Convert tables to 2 column layout at mobile res. And fix incorrect url to js
  files. (sgoodwin@redhat.com)
- add ldapsync blacklisting (deads@redhat.com)
- Move to openshift-jvm 1.0.29 (slewis@fusesource.com)
- bump(github.com/openshift/openshift-sdn)
  12f0efeb113058e04e9d333b92bbdddcfc34a9b4 (rpenta@redhat.com)
- Auto generated bash completion and examples doc for oadm pod-network
  (rpenta@redhat.com)
- Remove duplicated helper (rhcarvalho@gmail.com)
- union group name mapper (deads@redhat.com)
- UPSTREAM: 14871: Additional service ports config for master service.
  (abutcher@redhat.com)
- Update completions for kubernetes-service-node-port (abutcher@redhat.com)
- UPSTREAM: 13978 <drop>: NodePort option: Allowing for apiservers behind load-
  balanced endpoint. (abutcher@redhat.com)
- Update image stream page to use a table for the tags (jforrest@redhat.com)
- tighten ldap sync query types (deads@redhat.com)
- refactor building the syncer (deads@redhat.com)
- enhanced active directory ldap sync (deads@redhat.com)
- Use only official Dockerfile parser (rhcarvalho@gmail.com)
- Support oadm pod-network cmd (rpenta@redhat.com)
- added extended tests for LDAP sync (skuznets@redhat.com)
- update ldif to work (deads@redhat.com)
- e2e util has unused import 'regexp' (ccoleman@redhat.com)
- add master API proxy client cert (jliggitt@redhat.com)
- Change CA lifetime defaults (jliggitt@redhat.com)
- UPSTREAM: 15224: Refactor SSH tunneling, fix proxy transport TLS/Dial
  extraction (jliggitt@redhat.com)
- UPSTREAM: 15224: Allow specifying scheme when proxying (jliggitt@redhat.com)
- UPSTREAM: 14889: Honor InsecureSkipVerify flag (jliggitt@redhat.com)
- UPSTREAM: 14967: Add util to set transport defaults (jliggitt@redhat.com)
- Fix for issue where pod template is clipped at mobile res.      - fix
  https://github.com/openshift/origin/issues/4489   - switch to pf-image icon
  - correct icon alignment in pod template        - align label and meta data
  on overview (sgoodwin@redhat.com)
- Fix issue where long text strings extend beyond pod template container at
  mobile res.  - remove flex and min/max width that are no longer needed
  (sgoodwin@redhat.com)
- OS support for host pid and ipc (pweil@redhat.com)
- UPSTREAM:<carry>:hostPid/hostIPC scc support (pweil@redhat.com)
- UPSTREAM:14279:IPC followup (pweil@redhat.com)
- UPSTREAM:<carry>:v1beta3 hostIPC (pweil@redhat.com)
- UPSTREAM:12470:Support containers with host ipc in a pod (pweil@redhat.com)
- UPSTREAM:<carry>:v1beta3 hostPID (pweil@redhat.com)
- UPSTREAM:13447:Allow sharing the host PID namespace (pweil@redhat.com)
- Specify scheme in the jolokia URL (slewis@fusesource.com)
- Fix tag and package name in new-build example (rhcarvalho@gmail.com)
- UPSTREAM: <drop>: disable oidc tests (jliggitt@redhat.com)
- Verify `oc get` returns OpenShift resources (ccoleman@redhat.com)
- UPSTREAM: 15451 <partial>: Add our types to kubectl get error
  (ccoleman@redhat.com)
- Add loading message to all individual pages (jforrest@redhat.com)
- Remove build history and deployment history from main tables
  (jforrest@redhat.com)
- status: Fix incorrect missing registry warning (mkargaki@redhat.com)
- Add configuration options for logging and metrics endpoints
  (spadgett@redhat.com)
- Fix masterCA conversion (jliggitt@redhat.com)
- Fix oc logs (jliggitt@redhat.com)
- Revert "Unique output image stream names in new-app" (ccoleman@redhat.com)
- Bug 1263562 - users without projects should get default ctx when logging in
  (ffranz@redhat.com)
- added LDAP entries for other schemas (skuznets@redhat.com)
- remove cruft from options (deads@redhat.com)
- provide feedback while the ldap group sync job is running (deads@redhat.com)
- Allow POST access to node stats for cluster-reader and system:node-reader
  (jliggitt@redhat.com)
- Update role bindings in compatibility test (jliggitt@redhat.com)
- Add cluster role bindings diagnostic (jliggitt@redhat.com)
- Fix template minification to keep line breaks, remove html files from bindata
  (jforrest@redhat.com)
- Post 4902 fixes (maszulik@redhat.com)
- Add oc rsync command (cewong@redhat.com)
- bump(github.com/openshift/source-to-image)
  1fd4429c584d688d83c1247c03fa2eeb0b083ccb (cewong@redhat.com)
- Fixing typos (dmcphers@redhat.com)
- allocate supplemental groups to namespace (pweil@redhat.com)
- Remove forgotten code no longer used (nagy.martin@gmail.com)
- assets: Fix null dereference in updateTopology() (stefw@redhat.com)
- make oc logs support builds and buildconfigs (deads@redhat.com)
- Wait until the slave pod is gone (nagy.martin@gmail.com)
- UPSTREAM: 14616: Controller framework test flake fix (mfojtik@redhat.com)
- Disable verbose extended run (mfojtik@redhat.com)
- Unique output image stream names in new-app (rhcarvalho@gmail.com)
- Fix start build extended test (mfojtik@redhat.com)
- Make cleanup less noisy (mfojtik@redhat.com)
- Replace default reporter in Ginkgo with SimpleReporter (mfojtik@redhat.com)
- Atomic feature flags followup (miminar@redhat.com)
- examples: Move hello-openshift example to API v1 (stefw@redhat.com)
- Fix Vagrant provisioning after move to contrib/vagrant (dcbw@redhat.com)
- Always bring up openshift's desired network configuration on Vagrant
  provision (dcbw@redhat.com)
- Add annotations to the individual pages (jforrest@redhat.com)
- OS swagger and descriptions (pweil@redhat.com)
- UPSTREAM:<carry>:introduce scc types for fsgroup and supplemental groups
  (pweil@redhat.com)
- ldap sync active directory (deads@redhat.com)
- Change connection-based kubelet auth to application-level authn/authz
  interfaces (jliggitt@redhat.com)
- UPSTREAM: 15232`: refactor logs to be composeable (deads@redhat.com)
- bump(github.com/hashicorp/golang-lru):
  7f9ef20a0256f494e24126014135cf893ab71e9e (jliggitt@redhat.com)
- UPSTREAM: 14700: Add authentication/authorization interfaces to kubelet,
  always include /metrics with /stats (jliggitt@redhat.com)
- UPSTREAM: 14134: sets.String#Intersection (jliggitt@redhat.com)
- UPSTREAM: 15101: Add bearer token support for kubelet client config
  (jliggitt@redhat.com)
- UPSTREAM: 14710: Add verb to authorizer attributes (jliggitt@redhat.com)
- UPSTREAM: 13885: Cherry pick base64 and websocket patches
  (ccoleman@redhat.com)
- Delete --all option for oc export in cli doc (nakayamakenjiro@gmail.com)
- Fix cadvisor in integration test (jliggitt@redhat.com)
- Disable --allow-missing-image test (cewong@redhat.com)
- Make kube-proxy iptables sync period configurable (mkargaki@redhat.com)
- Update to latest version of PatternFly 2.2.0 and Bootstrap  3.3.5
  (sgoodwin@redhat.com)
- PHP hot deploy extended test (jhadvig@redhat.com)
- Ruby hot deploy extended test (jhadvig@redhat.com)
- change show-all default to true (deads@redhat.com)
- Update post-creation messages for builds in CLI (rhcarvalho@gmail.com)
- [Bug 4959] sample-app/cleanup.sh: fix usage of not-installed killall command.
  (vsemushi@redhat.com)
- fix bad oadm line (max.andersen@gmail.com)
- Refactored Openshift Origin builder, decoupled from S2I builder, added mocks
  and testing (kirill.frolov@servian.com)
- Use correct master url for internal token request, set master CA correctly
  (jliggitt@redhat.com)
- fix non-default all-in-one ports for testing (deads@redhat.com)
- Add extended test for git authentication (cewong@redhat.com)
- reconcile-cluster-role-bindings command (jliggitt@redhat.com)
- Change validation timing on create from image page (spadgett@redhat.com)
- Issue 2378 - Show TLS information for routes, create routes and
  routes/routename pages (jforrest@redhat.com)
- Lowercase resource names (rhcarvalho@gmail.com)
- create local images as docker refs (bparees@redhat.com)
- Preserve deployment status sequence (mkargaki@redhat.com)
- Add tests for S2I Perl and Python images with Hot Deploy
  (nagy.martin@gmail.com)
- Test asset config (jliggitt@redhat.com)
- UPSTREAM: 14967: Add util to set transport defaults (jliggitt@redhat.com)
- UPSTREAM: 14246: Fix race in lifecycle admission test (mfojtik@redhat.com)
- Fix send to closed channel in waitForBuild (mfojtik@redhat.com)
- UPSTREAM: 13885: Update error message in wsstream for go 1.5
  (mfojtik@redhat.com)
- Fix go vet (jliggitt@redhat.com)
- Change to use a 503 error page to fully address #4215 This allows custom
  error pages to be layered on in custom haproxy images. (smitram@gmail.com)
- Reduce number of test cases and add cleanup - travis seems to be hitting
  memory errors with starting multiple haproxy routers. (smitram@gmail.com)
- Fixes as per @Miciah review comments. (smitram@gmail.com)
- Update generated completions. (smitram@gmail.com)
- Add/update f5 tests for partition path. (smitram@gmail.com)
- Add partition path support to the f5 router - this will also allows us to
  support sharded routers with f5 using different f5 partitions.
  (smitram@gmail.com)
- Fixes as per @smarterclayton & @pweil- review comments and add generated docs
  and bash completions. (smitram@gmail.com)
- Turn on haproxy statistics by default since its now on a protected page.
  (smitram@gmail.com)
- Bind to router stats options (fixes issue #4884) and add help text
  clarifications. (smitram@gmail.com)
- Add tabs to pod details page (spadgett@redhat.com)
- Bug 1268484 - Use build.metadata.uid to track dismissed builds in UI
  (spadgett@redhat.com)
- cleanup ldap sync validation (deads@redhat.com)
- update auth test to share long running setup (deads@redhat.com)
- make ldap sync-group work (deads@redhat.com)
- fix ldap sync types to be more understandable (deads@redhat.com)
- remove unused mapper (pweil@redhat.com)
- change from kind to resource (pweil@redhat.com)
- fix decoding to handle yaml (deads@redhat.com)
- UPSTREAM: go-ldap: add String for debugging (deads@redhat.com)
- UPSTREAM: 14451: Fix a race in pod backoff. (mfojtik@redhat.com)
- Fix unbound variable in hack/cherry-pick.sh (mfojtik@redhat.com)
- Cleanup godocs of build types (rhcarvalho@gmail.com)
- Update travis to go 1.5.1 (mfojtik@redhat.com)
- Enable Go 1.5 (ccoleman@redhat.com)
- UPSTREAM: Fix typo in e2e pods test (nagy.martin@gmail.com)
- rename allow-missing to allow-missing-images (bparees@redhat.com)
- prune images: Conform to the hacking guide (mkargaki@redhat.com)
- Drop imageStream.spec.dockerImageRepository tags/IDs during conversion
  (ccoleman@redhat.com)
- Add validation to prevent IS.spec.dockerImageRepository from having tags
  (ccoleman@redhat.com)
- Add a helper to move things upstream (ccoleman@redhat.com)
- Cherry-pick helper (ccoleman@redhat.com)
- Clean up root folder (ccoleman@redhat.com)
- UPSTREAM: 13885: Support websockets on exec and pod logs
  (ccoleman@redhat.com)
- add test for patching anonymous fields in structs (deads@redhat.com)
- UPSTREAM: 14985: fix patch for anonymous struct fields (deads@redhat.com)
- fix exec admission controller flake (deads@redhat.com)
- updated template use (skuznets@redhat.com)
- fixed go vet invocation and errors (skuznets@redhat.com)
- Add ethtool to base/Dockerfile.rhel7 too (sdodson@redhat.com)
- [RPMS] atomic-openshift services use openshift bin (sdodson@redhat.com)
- [RPMS] fix rpm build related to sdn restructure (sdodson@redhat.com)
- UPSTREAM: 14831: allow yaml as argument to patch (deads@redhat.com)
- Move host etc master/node directories to official locations.
  (dgoodwin@redhat.com)
- Wait for service account to be accessible (mfojtik@redhat.com)
- Wait for builder account (mfojtik@redhat.com)
- Pull RHEL7 images from internal CI registry (mfojtik@redhat.com)
- Initial addition of S2I SCL enablement extended tests (mfojtik@redhat.com)
- tolerate missing docker images (bparees@redhat.com)
- bump(github.com/spf13/cobra): d732ab3a34e6e9e6b5bdac80707c2b6bad852936
  (ffranz@redhat.com)
- Rename various openshift directories to origin. (dgoodwin@redhat.com)
- allow SAR requests in lifecycle admission (pweil@redhat.com)
- Issue 4001 - add requests and limits to resource limits on settings page
  (jforrest@redhat.com)
- prevent force pull set up from running in other focuses; add some debug clues
  in hack/util.sh; comments from Cesar, Ben; create new builder images so we
  run concurrent;  MIchal's comments; move to just one builder
  (gmontero@redhat.com)
- fix govet example error (skuznets@redhat.com)
- Add Restart=always to master service (sdodson@redhat.com)
- Issue 4867 - route links should open in a new window (jforrest@redhat.com)
- Fix output of git basic credentials in builder (cewong@redhat.com)
- Set build status message in case of error (rhcarvalho@gmail.com)
- Fix the reference of openshift command in Makefile (akira@tagoh.org)
- Issue 4632 - remove 'Project' from the project overview header
  (jforrest@redhat.com)
- Issue 4860 - missing no deployments msg when only have RCs
  (jforrest@redhat.com)
- Support deployment hook volume inheritance (ironcladlou@gmail.com)
- fix RAR test flake (deads@redhat.com)
- UPSTREAM: 14688: Deflake max in flight (deads@redhat.com)
- Fix vagrant provisioning (danw@redhat.com)
- setup makefile to be parallelizeable (deads@redhat.com)
- api group support for authorizer (deads@redhat.com)
- Apply OOMScoreAdjust and Restart policy to openshift node (decarr@redhat.com)
- Fix nit (dmcphers@redhat.com)
- Add ethtool to our deps (mkargaki@redhat.com)
- Issue 4855 - warning flickers about build config and deployment config not
  existing (jforrest@redhat.com)
- Add MySQL extended replication tests (nagy.martin@gmail.com)
- extended: Disable Daemon tests (mkargaki@redhat.com)
- Adds explicit suggestions for some cli commands (ffranz@redhat.com)
- bump(github.com/spf13/pflag): b084184666e02084b8ccb9b704bf0d79c466eb1d
  (ffranz@redhat.com)
- bump(github.com/cpf13/cobra): 046a67325286b5e4d7c95b1d501ea1cd5ba43600
  (ffranz@redhat.com)
- Don't show errors in name field until blurred (spadgett@redhat.com)
- Allow whitespace-only values in UI for required parameters
  (spadgett@redhat.com)
- make RAR allow evaluation errors (deads@redhat.com)
- Watch routes on individual service page (spadgett@redhat.com)
- bump(github.com/vjeantet/ldapserver) 19fbc46ed12348d5122812c8303fb82e49b6c25d
  (mkargaki@redhat.com)
- Bug 1266859: UPSTREAM: <drop>: expose: Truncate service names
  (mkargaki@redhat.com)
- Update docs regarding the rebase (mkargaki@redhat.com)
- add timing statements (deads@redhat.com)
- Routes should be able to specify which port they desire (ccoleman@redhat.com)
- Add dbus for the OVS setup required docker restart. (dgoodwin@redhat.com)
- Return to OSBS preferred labels. (dgoodwin@redhat.com)
- Source info should only be loaded when Git is used for builds
  (ccoleman@redhat.com)
- Rename ose3 node run script to match aos. (dgoodwin@redhat.com)
- Bump aos-master and aos-node to 3.0.2.100. (dgoodwin@redhat.com)
- Rename ose3 script to matching aos, standardize labels. (dgoodwin@redhat.com)
- Merge in latest work from oseonatomic repo. (dgoodwin@redhat.com)
- Expose version as prometheus metric (jimmidyson@gmail.com)
- Cleanup unused code and add proper labels. (dgoodwin@redhat.com)
- Update for AOS 3.1 version and a more consistent bz component name.
  (dgoodwin@redhat.com)
- Add missing Name label. (dgoodwin@redhat.com)
- Cleanup aos-master image for OSBS build. (dgoodwin@redhat.com)
- aos-node container building locally. (dgoodwin@redhat.com)
- Use Dockerfile.product for ose-master to future proof a bit.
  (dgoodwin@redhat.com)
- Move to Dockerfile.product for future upstream compatability.
  (dgoodwin@redhat.com)
- Initial draft of aos-master container. (dgoodwin@redhat.com)

* Tue Sep 29 2015 Scott Dodson <sdodson@redhat.com> 3.0.2.900
- OSE Docs URLs (sdodson@redhat.com)
- Do not treat directories named Dockerfile as file (rhcarvalho@gmail.com)
- Disable the pods per node test - it requires the kubelet stats
  (ccoleman@redhat.com)
- Set Build.Status.Pushspec to resolved pushspec (rhcarvalho@gmail.com)
- Bug: 1266442 1266447 (jhadvig@redhat.com)
- new-app: Better output in case of invalid Dockerfile (mkargaki@redhat.com)
- Compatibility test for Volume Source (mkargaki@redhat.com)
- Update UPGRADE.md about Metadata/Downward (mkargaki@redhat.com)
- get local IP like the server would and add retries to build test watch
  (pweil@redhat.com)
- Interesting refactoring (mkargaki@redhat.com)
- Fix verify-open-ports.sh to not fail on success (mkargaki@redhat.com)
- Boring refactoring; code generations (mkargaki@redhat.com)
- UPSTREAM: openshift-sdn: 167: plugins: Update Kube client imports
  (mkargaki@redhat.com)
- UPSTREAM: <carry>: Move to test pkg to avoid linking test flags in binaries
  (pweil@redhat.com)
- UPSTREAM: <carry>: Add etcd prefix (mkargaki@redhat.com)
- UPSTREAM: 14664: fix testclient prepend (deads@redhat.com)
- UPSTREAM: 14502: don't fatal on missing sorting flag (deads@redhat.com)
- UPSTREAM: <drop>: hack experimental versions and client creation
  (deads@redhat.com)
- UPSTREAM: 14496: deep-copies: Structs cannot be nil (mkargaki@redhat.com)
- UPSTREAM: <carry>: Back n forth downward/metadata conversions
  (mkargaki@redhat.com)
- UPSTREAM: 13728: Allow to replace os.Exit() with panic when CLI command fatal
  (mfojtik@redhat.com)
- UPSTREAM: 14291: add patch verb to APIRequestInfo (deads@redhat.com)
- UPSTREAM: 13910: Fix resourcVersion = 0 in cacher (mkargaki@redhat.com)
- UPSTREAM: 13864: Fix kubelet logs --follow bug (mkargaki@redhat.com)
- UPSTREAM: 14063: enable system CAs (mkargaki@redhat.com)
- UPSTREAM: 13756: expose: Avoid selector resolution if a selector is not
  needed (mkargaki@redhat.com)
- UPSTREAM: 13746: Fix field=metadata.name (ccoleman@redhat.com)
- UPSTREAM: 9870: Allow Volume Plugins to be configurable (deads@redhat.com)
- UPSTREAM: 11827: allow permissive SA secret ref limitting (deads@redhat.com)
- UPSTREAM: 12221: Allow custom namespace creation in e2e framework
  (mfojtik@redhat.com)
- UPSTREAM: 12498: Re-add timeouts for kubelet which is not in the upstream PR.
  (deads@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: 9844: EmptyDir volume SELinux support (deads@redhat.com)
- UPSTREAM: 7893: scc allocation interface methods (deads@redhat.com)
- UPSTREAM: 7893: scc (pweil@redhat.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (deads@redhat.com)
- UPSTREAM: <drop>: add back flag types to reduce noise during this rebase
  (deads@redhat.com)
- UPSTREAM: <none>: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: <none>: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable --validate by default (mkargaki@redhat.com)
- UPSTREAM: <carry>: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: <carry>: reallow the ability to post across namespaces in api
  (pweil@redhat.com)
- UPSTREAM: <carry>: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: Allow pod start to be delayed in Kubelet
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (deads@redhat.com)
- UPSTREAM: <carry>: v1beta3 (deads@redhat.com)
- bump(github.com/emicklei/go-restful) 1f9a0ee00ff93717a275e15b30cf7df356255877
  (mkargaki@redhat.com)
- bump(k8s.io/kubernetes) 86b4e777e1947c1bc00e422306a3ca74cbd54dbe
  (mkargaki@redhat.com)
- Update java console (slewis@fusesource.com)
- fix QueryForEntries API (deads@redhat.com)
- added sync-groups command basics (skuznets@redhat.com)
- add ldap groups sync (skuznets@redhat.com)
- Remove templates.js from bindata and fix HTML minification
  (spadgett@redhat.com)
- fedora 21 Vagrant provisioning fixes (dcbw@redhat.com)
- Issue 4795 - include ref and contextdir in github links (jforrest@redhat.com)
- new-app: Actually use the Docker parser (mkargaki@redhat.com)
- Update old references to _output/local/go/bin (rhcarvalho@gmail.com)
- improved robustness of recycler script (mturansk@redhat.com)
- Do not export test utility (rhcarvalho@gmail.com)
- Change build-go to generate binaries to _output/local/bin/${platform}
  (ccoleman@redhat.com)
- Make deployment trigger logging quieter (ironcladlou@gmail.com)
- bump(github.com/openshift/openshift-sdn)
  669deb4de23ab7f79341a132786b198c7f272082 (rpenta@redhat.com)
- Fix openshift-sdn imports in origin (rpenta@redhat.com)
- Move plugins/osdn to Godeps/workspace/src/github.com/openshift/openshift-
  sdn/plugins/osdn (rpenta@redhat.com)
- Move sdn ovssubnet to pkg/ovssubnet dir (rpenta@redhat.com)
- Reorganize web console create flow (spadgett@redhat.com)
- Fix handle on watchObject. Set deletionTimestamp instead of deleted.
  (jforrest@redhat.com)
- Use direct CLI invocations rather than embedding CLI (ccoleman@redhat.com)
- Next steps page (after creating stuff in console) (ffranz@redhat.com)
- Disable parallelism for now (ccoleman@redhat.com)
- Do not require the master components from test/util (ccoleman@redhat.com)
- [userinterface_public_538] Create individual pages for all resources With
  some changes from @sg00dwin and @spadgett (jforrest@redhat.com)
- Fix some of the govet issues (mfojtik@redhat.com)
- annotate builds on clone (bparees@redhat.com)
- Make network fixup during provision conditional (marun@redhat.com)
- Update roadmap url (dmcphers@redhat.com)
- better error message for immutable edits to builds (bparees@redhat.com)
- Default NetworkConfig.ServiceNetworkCIDR to
  KubernetesMasterConfig.ServicesSubnet (jliggitt@redhat.com)
- create SCCExecRestriction admission plugin (deads@redhat.com)
- added oadm commands to validate node and master config (skuznets@redhat.com)
- Add an e2e test for Dockerfile and review comments (ccoleman@redhat.com)
- Add extended tests for start-build (mfojtik@redhat.com)
- allow local access reviews while namespace is terminating (deads@redhat.com)
- build oc, move to clients, move alt clients to redistributable
  (tdawson@redhat.com)
- Add --kubeconfig support for compat with kubectl (ccoleman@redhat.com)
- assets: Filter topology correctly and refactor relations (stefw@redhat.com)
- allow self SARs using old policy: (deads@redhat.com)
- Capture panic in extended CLI and return them as Go errors
  (mfojtik@redhat.com)
- UPSTREAM: 13728: Allow to replace os.Exit() with panic when CLI command fatal
  (mfojtik@redhat.com)
- Take stdin on OpenShift CLI (ccoleman@redhat.com)
- add extended tests for example repos (bparees@redhat.com)
- added syntax highlighting to readme (skuznets@redhat.com)
- Retry finalizer on conflict error (decarr@redhat.com)
- Build from a Dockerfile directly (ccoleman@redhat.com)
- fix backwards poll args (bparees@redhat.com)
- Add missing rolling hook conversions (ironcladlou@gmail.com)
- Fix potential race conditions during SDN setup (rpenta@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  0f9e6558e8dceb8c8317e3587d9c9c94ae07ecb8 (rpenta@redhat.com)
- Add missing rolling hook conversions (ironcladlou@gmail.com)
- Make "default" an admin namespace in multitenant (danw@redhat.com)
- add patch to default roles (deads@redhat.com)
- Exclude a few more tests (ccoleman@redhat.com)
- Refactor setting and resetting HTTP proxies (rhcarvalho@gmail.com)
- UPSTREAM: 14291: add patch verb to APIRequestInfo (deads@redhat.com)
- Add --portal-net back to all-in-one args (danw@redhat.com)
- Bump kubernetes-ui-label-selector to v0.0.10 - fixes js error
  (jforrest@redhat.com)
- Fix broken link in readme (mtayer@redhat.com)
- add SA role bindings to auto-provisioned namespaces (deads@redhat.com)
- diagnostics: fail gracefully on broken kubeconfig (lmeyer@redhat.com)
- Improve systemd detection for diagnostics. (dgoodwin@redhat.com)
- Refactor pkg/build/builder (rhcarvalho@gmail.com)
- Set kubeconfig in extended tests (ccoleman@redhat.com)
- Extended failure (ccoleman@redhat.com)
- Only run k8s upstream tests that are passing (ccoleman@redhat.com)
- Add example env vars (rhcarvalho@gmail.com)
- Pass env vars defined in Docker build strategy (rhcarvalho@gmail.com)
- [RPMs] Ease the upgrade to v1.0.6 (sdodson@redhat.com)
- BZ1221441 - new filter that shows unique project name (rafabene@gmail.com)
- Push F5 image (ccoleman@redhat.com)
- Making the regex in ./test/cmd/admin.sh a little more flexible for downstream
  (bleanhar@redhat.com)
- Making the regex in ./test/cmd/admin.sh a little more flexible for downstream
  (bleanhar@redhat.com)
- Add generated-by annotation to CLI new-app and web console
  (mfojtik@redhat.com)
- disable go vet in make check-test (skuznets@redhat.com)
- more comments (pweil@redhat.com)
- add cluster roles to diagnostics (deads@redhat.com)
- UPSTREAM: 14063: enable system CAs (deads@redhat.com)
- Linux 386 cross compile (ccoleman@redhat.com)
- Add X-Forwarded-* headers and the new Forwarded header for rfc7239 so that
  the backend has info about the proxied request (and requestor).
  (smitram@gmail.com)
- switch to https for sample repo url (bparees@redhat.com)
- Add SA secret checking to SA readiness test in integration tests
  (cewong@redhat.com)
- Adding source secret (jhadvig@redhat.com)
- disable go vet in make check-test (skuznets@redhat.com)
- Update bash-completion (nakayamakenjiro@gmail.com)
- Allow metadata on images to be edited after creation (ccoleman@redhat.com)
- Enable linux-386 (ccoleman@redhat.com)
- .commit is a file, not a directory (ccoleman@redhat.com)
- Retry deployment resource updates (ironcladlou@gmail.com)
- Improve latest deployment output (ironcladlou@gmail.com)
- Make release extraction a separate step for builds (ccoleman@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  0f9e6558e8dceb8c8317e3587d9c9c94ae07ecb8 (rpenta@redhat.com)
- Fix potential race conditions during SDN setup (rpenta@redhat.com)
- Fix casing of output (ironcladlou@gmail.com)
- Adjust help templates to latest version of Cobra (ffranz@redhat.com)
- Update generated completions (ffranz@redhat.com)
- bump(github.com/spf13/cobra): 6d7031177028ad8c5b4b428ac9a2288fbc1c0649
  (ffranz@redhat.com)
- bump(github.com/spf13/pflag): 8e7dc108ab3a1ab6ce6d922bbaff5657b88e8e49
  (ffranz@redhat.com)
- Update to version 0.0.9 for kubernetes-label-selector. Fixes issue
  https://github.com/openshift/origin/issues/3180 (sgoodwin@redhat.com)
- UPSTREAM: 211: Allow listen only ipv4 (ccoleman@redhat.com)
- UPSTREAM: Disable systemd activation for DNS (ccoleman@redhat.com)
- bump(github.com/skynetservices/skydns):bb2ebadc9746f23e4a296e3cbdb8c01e956bae
  e1 (jimmidyson@gmail.com)
- Fixes #4494: Don't register skydns metrics on nodes (jimmidyson@gmail.com)
- Move positional parameters before package lists (nagy.martin@gmail.com)
- Simplify the readme to point to docs (ccoleman@redhat.com)
- Normalize extended tests into test/extended/*.sh (ccoleman@redhat.com)
- Improve deploy --cancel output (ironcladlou@gmail.com)
- Bump min Docker version in docs (agoldste@redhat.com)
- Normalize extended tests into test/extended/*.sh (ccoleman@redhat.com)
- Return empty Config field in FromName to avoid nil pointer error
  (nakayamakenjiro@gmail.com)
- docs: Fixed broken links in openshift_model.md. (stevem@gnulinux.net)
- Show corrent error message if passed json template is invalid
  (prukner.jan@seznam.cz)
- Clean up test directories (ccoleman@redhat.com)
- hack/build-images.sh fails on vboxfs due to hardlink (ccoleman@redhat.com)
- Fail with stack trace in test bash (ccoleman@redhat.com)
- Make oc rsh behave more like ssh (ccoleman@redhat.com)
- better error messages for parameter errors (bparees@redhat.com)
- Simplify the release output, create a zip (ccoleman@redhat.com)
- Cleaning useless colon (remy.binsztock@tech-angels.com)
- app: Implement initial topology-graph based view (stefw@redhat.com)
- app: Normalize kind property on retrieved items (stefw@redhat.com)
- app: Toggle overview modes between tiles and topology (stefw@redhat.com)
- Test for exposing external services (mkargaki@redhat.com)
- UPSTREAM: 13756: expose: Avoid selector resolution if a selector is not
  needed (mkargaki@redhat.com)
- Add helper script to run kube e2e tests (marun@redhat.com)
- Stop adding user to 'docker' group (marun@redhat.com)

* Fri Sep 18 2015 Scott Dodson <sdodson@redhat.com> 0.2-9
- Rename from openshift -> origin
- Symlink /var/lib/origin to /var/lib/openshift if /var/lib/openshift exists

* Wed Aug 12 2015 Steve Milner <smilner@redhat.com> 0.2-8
- Master configs will be generated if none are found when the master is installed.
- Node configs will be generated if none are found when the master is installed.
- Additional notice file added if config is generated by the RPM.
- All-In-One services removed.

* Wed Aug 12 2015 Steve Milner <smilner@redhat.com> 0.2-7
- Added new ovs script(s) to file lists.

* Wed Aug  5 2015 Steve Milner <smilner@redhat.com> 0.2-6
- Using _unitdir instead of _prefix for unit data

* Fri Jul 31 2015 Steve Milner <smilner@redhat.com> 0.2-5
- Configuration location now /etc/origin
- Default configs created upon installation

* Tue Jul 28 2015 Steve Milner <smilner@redhat.com> 0.2-4
- Added AEP packages

* Mon Jan 26 2015 Scott Dodson <sdodson@redhat.com> 0.2-3
- Update to 21fb40637c4e3507cca1fcab6c4d56b06950a149
- Split packaging of openshift-master and openshift-node

* Mon Jan 19 2015 Scott Dodson <sdodson@redhat.com> 0.2-2
- new package built with tito

* Fri Jan 09 2015 Adam Miller <admiller@redhat.com> - 0.2-2
- Add symlink for osc command line tooling (merged in from jhonce@redhat.com)

* Wed Jan 07 2015 Adam Miller <admiller@redhat.com> - 0.2-1
- Update to latest upstream release
- Restructured some of the golang deps  build setup for restructuring done
  upstream

* Thu Oct 23 2014 Adam Miller <admiller@redhat.com> - 0-0.0.9.git562842e
- Add new patches from jhonce for systemd units

* Mon Oct 20 2014 Adam Miller <admiller@redhat.com> - 0-0.0.8.git562842e
- Update to latest master snapshot

* Wed Oct 15 2014 Adam Miller <admiller@redhat.com> - 0-0.0.7.git7872f0f
- Update to latest master snapshot

* Fri Oct 03 2014 Adam Miller <admiller@redhat.com> - 0-0.0.6.gite4d4ecf
- Update to latest Alpha nightly build tag 20141003

* Wed Oct 01 2014 Adam Miller <admiller@redhat.com> - 0-0.0.5.git6d9f1a9
- Switch to consistent naming, patch by jhonce

* Tue Sep 30 2014 Adam Miller <admiller@redhat.com> - 0-0.0.4.git6d9f1a9
- Add systemd and sysconfig entries from jhonce

* Tue Sep 23 2014 Adam Miller <admiller@redhat.com> - 0-0.0.3.git6d9f1a9
- Update to latest upstream.

* Mon Sep 15 2014 Adam Miller <admiller@redhat.com> - 0-0.0.2.git2647df5
- Update to latest upstream.
