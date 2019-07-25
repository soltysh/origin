#debuginfo not supported with Go
%global debug_package %{nil}
# modifying the Go binaries breaks the DWARF debugging
%global __os_install_post %{_rpmconfigdir}/brp-compress

%global gopath      %{_datadir}/gocode
%global import_path github.com/openshift/origin

%global golang_version 1.12
# %commit and %os_git_vars are intended to be set by tito custom builders provided
# in the .tito/lib directory. The values in this spec file will not be kept up to date.
%{!?commit:
%global commit 79cc5bc6cbb6a86dced3c2d9fac9cc8390c8020c
}
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# os_git_vars needed to run hack scripts during rpm builds
%{!?os_git_vars:
%global os_git_vars OS_GIT_MINOR=2+ OS_GIT_MAJOR=4 OS_GIT_VERSION=v4.2.0 OS_GIT_TREE_STATE=clean OS_BUILD_LDFLAGS_DEFAULT_IMAGE_STREAMS=rhel7 KUBE_GIT_VERSION=v1.14.0+79cc5bc6c OS_GIT_PATCH=0 KUBE_GIT_COMMIT=e8fcd6a KUBE_GIT_MINOR=14+ OS_GIT_COMMIT=79cc5bc6c KUBE_GIT_MAJOR=1 OS_IMAGE_PREFIX=registry.redhat.io/openshift3/ose ETCD_GIT_VERSION=v3.3.10 ETCD_GIT_COMMIT=27fc7e2
}

%if 0%{?skip_build}
%global do_build 0
%else
%global do_build 1
%endif
%if 0%{?skip_prep}
%global do_prep 0
%else
%global do_prep 1
%endif
%if 0%{?skip_dist}
%global package_dist %{nil}
%else
%global package_dist %{dist}
%endif

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
%global package_name openshift
%global product_name OpenShift
%else
%global package_name openshift
%global product_name OpenShift
%endif

%{!?version: %global version 0.0.1}
%{!?release: %global release 1}

Name:           %{package_name}
Version:        4.2.0
Release:        201907250619%{?dist}
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
BuildRequires:  goversioninfo
BuildRequires:  systemd
BuildRequires:  bsdtar
BuildRequires:  golang >= %{golang_version}
BuildRequires:  krb5-devel
BuildRequires:  rsync
Requires:       %{name}-clients = %{version}-%{release}

#
# The following Bundled Provides entries are populated automatically by the
# OpenShift tito custom builder found here:
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

%package hyperkube
Summary:        %{product_name} Kubernetes server commands
Requires:       util-linux
Requires:       socat
Requires:       iptables
Provides:       hyperkube
Provides:       atomic-openshift-hyperkube
Provides:       atomic-openshift-node

%description hyperkube
%{summary}

%package clients
Summary:        %{product_name} Client binaries for Linux
Provides:       atomic-openshift-clients
Obsoletes:      atomic-openshift-clients
Requires:       bash-completion

%description clients
%{summary}

%if 0%{?make_redistributable}
%package clients-redistributable
Summary:        %{product_name} Client binaries for Linux, Mac OSX, and Windows
Provides:       atomic-openshift-clients-redistributable
Obsoletes:      atomic-openshift-clients-redistributable
BuildRequires:  goversioninfo

%description clients-redistributable
%{summary}
%endif

%prep
%if 0%{do_prep}
%setup -q
%endif

%build
%if 0%{do_build}
%if 0%{make_redistributable}
# Create Binaries for all supported arches
%{os_git_vars} OS_BUILD_RELEASE_ARCHIVES=n make build-cross
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
OS_ONLY_BUILD_PLATFORMS="${BUILD_PLATFORM}" %{os_git_vars} OS_BUILD_RELEASE_ARCHIVES=n make build-cross
%endif

# Generate man pages
%{os_git_vars} make build-docs
%endif

%install

PLATFORM="$(go env GOHOSTOS)/$(go env GOHOSTARCH)"
install -d %{buildroot}%{_bindir}

# Install linux components
for bin in oc hyperkube
do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 _output/local/bin/${PLATFORM}/${bin} %{buildroot}%{_bindir}/${bin}
done

%if 0%{?make_redistributable}
# Install client executable for windows and mac
install -d %{buildroot}%{_datadir}/%{name}/{linux,macosx,windows}
install -p -m 755 _output/local/bin/linux/amd64/oc %{buildroot}%{_datadir}/%{name}/linux/oc
install -p -m 755 _output/local/bin/linux/amd64/kubectl %{buildroot}%{_datadir}/%{name}/linux/kubectl
install -p -m 755 _output/local/bin/darwin/amd64/oc %{buildroot}/%{_datadir}/%{name}/macosx/oc
install -p -m 755 _output/local/bin/darwin/amd64/kubectl %{buildroot}/%{_datadir}/%{name}/macosx/kubectl
install -p -m 755 _output/local/bin/windows/amd64/oc.exe %{buildroot}/%{_datadir}/%{name}/windows/oc.exe
install -p -m 755 _output/local/bin/windows/amd64/kubectl.exe %{buildroot}/%{_datadir}/%{name}/windows/kubectl.exe
%endif

for cmd in \
    kubectl
do
    ln -s oc %{buildroot}%{_bindir}/$cmd
done

# Install man1 man pages
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -m 0644 docs/man/man1/* %{buildroot}%{_mandir}/man1/

# Install bash completions
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d/
for bin in oc kubectl
do
  echo "+++ INSTALLING BASH COMPLETIONS FOR ${bin} "
  %{buildroot}%{_bindir}/${bin} completion bash > %{buildroot}%{_sysconfdir}/bash_completion.d/${bin}
  chmod 644 %{buildroot}%{_sysconfdir}/bash_completion.d/${bin}
done

%files hyperkube
%license LICENSE
%{_bindir}/hyperkube
%defattr(-,root,root,0700)

%files clients
%license LICENSE
%{_bindir}/oc
%{_bindir}/kubectl
%{_sysconfdir}/bash_completion.d/oc
%{_sysconfdir}/bash_completion.d/kubectl
%{_mandir}/man1/oc*

%if 0%{?make_redistributable}
%files clients-redistributable
%license LICENSE
%dir %{_datadir}/%{name}/linux/
%dir %{_datadir}/%{name}/macosx/
%dir %{_datadir}/%{name}/windows/
%{_datadir}/%{name}/linux/oc
%{_datadir}/%{name}/linux/kubectl
%{_datadir}/%{name}/macosx/oc
%{_datadir}/%{name}/macosx/kubectl
%{_datadir}/%{name}/windows/oc.exe
%{_datadir}/%{name}/windows/kubectl.exe
%endif

%changelog
