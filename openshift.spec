#debuginfo not supported with Go
%global debug_package %{nil}
%global gopath      %{_datadir}/gocode
%global import_path github.com/openshift/origin
%global kube_plugin_path /usr/libexec/kubernetes/kubelet-plugins/net/exec/redhat~openshift-ovs-subnet
%global sdn_import_path github.com/openshift/openshift-sdn

# %commit and %ldflags are intended to be set by tito custom builders provided
# in the rel-eng directory. The values in this spec file will not be kept up to date.
%{!?commit:
%global commit a5a90a1b7ca71bb250b91322c8d0669b7f8316a6
}
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# OpenShift specific ldflags from hack/common.sh os::build:ldflags
%{!?ldflags:
%global ldflags -X github.com/openshift/origin/pkg/version.majorFromGit 3 -X github.com/openshift/origin/pkg/version.minorFromGit 0+ -X github.com/openshift/origin/pkg/version.versionFromGit v3.0.1.0-1-640-ga5a90a1 -X github.com/openshift/origin/pkg/version.commitFromGit a5a90a1 -X k8s.io/kubernetes/pkg/version.gitCommit 44c91b1 -X k8s.io/kubernetes/pkg/version.gitVersion v1.1.0-alpha.0-1605-g44c91b1
}

Name:           openshift
# Version is not kept up to date and is intended to be set by tito custom
# builders provided in the rel-eng directory of this project
Version:        3.0.1.900
Release:        0%{?dist}
Summary:        Open Source Platform as a Service by Red Hat
License:        ASL 2.0
URL:            https://%{import_path}
ExclusiveArch:  x86_64
Source0:        https://%{import_path}/archive/%{commit}/%{name}-%{version}.tar.gz

BuildRequires:  systemd
BuildRequires:  golang >= 1.4


%description
%{summary}

%package master
Summary:        OpenShift Master
Requires:       %{name} = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description master
%{summary}

%package node
Summary:        OpenShift Node
Requires:       %{name} = %{version}-%{release}
Requires:       docker-io >= 1.6.2
Requires:       tuned-profiles-openshift-node
Requires:       util-linux
Requires:       socat
Requires:       nfs-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description node
%{summary}

%package -n tuned-profiles-openshift-node
Summary:        Tuned profiles for OpenShift Node hosts
Requires:       tuned >= 2.3
Requires:       %{name} = %{version}-%{release}

%description -n tuned-profiles-openshift-node
%{summary}

%package clients
Summary:      Openshift Client binaries for Linux, Mac OSX, and Windows
BuildRequires: golang-pkg-darwin-amd64
BuildRequires: golang-pkg-windows-386

%description clients
%{summary}

%package dockerregistry
Summary:        Docker Registry v2 for OpenShift
Requires:       %{name} = %{version}-%{release}

%description dockerregistry
%{summary}

%package pod
Summary:        OpenShift Pod
Requires:       %{name} = %{version}-%{release}

%description pod
%{summary}

%package sdn-ovs
Summary:          OpenShift SDN Plugin for Open vSwitch
Requires:         openvswitch >= 2.3.1
Requires:         %{name}-node = %{version}-%{release}
Requires:         bridge-utils
Requires:         ethtool

%description sdn-ovs
%{summary}

%prep
%setup -q

%build

# Don't judge me for this ... it's so bad.
mkdir _build

# Horrid hack because golang loves to just bundle everything
pushd _build
    mkdir -p src/github.com/openshift
    ln -s $(dirs +1 -l) src/%{import_path}
popd


# Gaming the GOPATH to include the third party bundled libs at build
# time. This is bad and I feel bad.
mkdir _thirdpartyhacks
pushd _thirdpartyhacks
    ln -s \
        $(dirs +1 -l)/Godeps/_workspace/src/ \
            src
popd
export GOPATH=$(pwd)/_build:$(pwd)/_thirdpartyhacks:%{buildroot}%{gopath}:%{gopath}
# Build all linux components we care about
for cmd in openshift dockerregistry
do
        go install -ldflags "%{ldflags}" %{import_path}/cmd/${cmd}
done

# Build only 'openshift' for other platforms
GOOS=windows GOARCH=386 go install -ldflags "%{ldflags}" %{import_path}/cmd/openshift
GOOS=darwin GOARCH=amd64 go install -ldflags "%{ldflags}" %{import_path}/cmd/openshift

#Build our pod
pushd images/pod/
    go build -ldflags "%{ldflags}" pod.go
popd

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}/{linux,macosx,windows}

# Install linux components
for bin in openshift dockerregistry
do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 _build/bin/${bin} %{buildroot}%{_bindir}/${bin}
done
# Install 'openshift' as client executable for windows and mac
install -p -m 755 _build/bin/openshift %{buildroot}%{_datadir}/%{name}/linux/oc
install -p -m 755 _build/bin/darwin_amd64/openshift %{buildroot}%{_datadir}/%{name}/macosx/oc
install -p -m 755 _build/bin/windows_386/openshift.exe %{buildroot}%{_datadir}/%{name}/windows/oc.exe
#Install openshift pod
install -p -m 755 images/pod/pod %{buildroot}%{_bindir}/

install -d -m 0755 %{buildroot}/etc/%{name}/{master,node}
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} rel-eng/openshift-master.service
install -m 0644 -t %{buildroot}%{_unitdir} rel-eng/openshift-node.service

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 rel-eng/openshift-master.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/openshift-master
install -m 0644 rel-eng/openshift-node.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/openshift-node

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

ln -s %{_bindir}/openshift %{buildroot}%{_bindir}/oc
ln -s %{_bindir}/openshift %{buildroot}%{_bindir}/oadm
ln -s %{_bindir}/openshift %{buildroot}%{_bindir}/kubectl

install -d -m 0755 %{buildroot}%{_prefix}/lib/tuned/openshift-node-{guest,host}
install -m 0644 tuned/openshift-node-guest/tuned.conf %{buildroot}%{_prefix}/lib/tuned/openshift-node-guest/
install -m 0644 tuned/openshift-node-host/tuned.conf %{buildroot}%{_prefix}/lib/tuned/openshift-node-host/
install -d -m 0755 %{buildroot}%{_mandir}/man7
install -m 0644 tuned/man/tuned-profiles-openshift-node.7 %{buildroot}%{_mandir}/man7/tuned-profiles-openshift-node.7

# Install sdn scripts
install -d -m 0755 %{buildroot}%{kube_plugin_path}
pushd _thirdpartyhacks/src/%{sdn_import_path}/ovssubnet/controller/kube/bin
   install -p -m 755 %{name}-ovs-subnet %{buildroot}%{kube_plugin_path}/openshift-ovs-subnet
   install -p -m 755 %{name}-sdn-kube-subnet-setup.sh %{buildroot}%{_bindir}/openshift-sdn-kube-subnet-setup.sh
popd
pushd _thirdpartyhacks/src/%{sdn_import_path}/ovssubnet/controller/multitenant/bin
   install -p -m 755 %{name}-ovs-multitenant %{buildroot}%{_bindir}/openshift-ovs-multitenant
   install -p -m 755 %{name}-sdn-multitenant-setup.sh %{buildroot}%{_bindir}/openshift-sdn-multitenant-setup.sh
popd
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system/docker.service.d
install -p -m 0644 rel-eng/docker-sdn-ovs.conf %{buildroot}%{_prefix}/lib/systemd/system/docker.service.d/
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system/openshift-node.service.d
install -p -m 0644 rel-eng/openshift-sdn-ovs.conf %{buildroot}%{_prefix}/lib/systemd/system/openshift-node.service.d/


# Install bash completions
install -d -m 755 %{buildroot}/etc/bash_completion.d/
install -p -m 644 rel-eng/completions/bash/* %{buildroot}/etc/bash_completion.d/

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/openshift
%{_bindir}/oc
%{_bindir}/oadm
%{_bindir}/kubectl
%{_sharedstatedir}/%{name}
/etc/bash_completion.d/*

%files master
%defattr(-,root,root,-)
%{_unitdir}/openshift-master.service
%config(noreplace) %{_sysconfdir}/sysconfig/openshift-master
%config(noreplace) /etc/%{name}/master

%post master
%systemd_post %{basename:openshift-master.service}

%preun master
%systemd_preun %{basename:openshift-master.service}

%postun master
%systemd_postun


%files node
%defattr(-,root,root,-)
%{_unitdir}/openshift-node.service
%config(noreplace) %{_sysconfdir}/sysconfig/openshift-node
%config(noreplace) /etc/%{name}/node

%post node
%systemd_post %{basename:openshift-node.service}

%preun node
%systemd_preun %{basename:openshift-node.service}

%postun node
%systemd_postun

%files sdn-ovs
%defattr(-,root,root,-)
%{_bindir}/openshift-sdn-kube-subnet-setup.sh
%{_bindir}/%{name}-ovs-multitenant
%{_bindir}/%{name}-sdn-multitenant-setup.sh
%{kube_plugin_path}/openshift-ovs-subnet
%{_prefix}/lib/systemd/system/openshift-node.service.d/openshift-sdn-ovs.conf
%{_prefix}/lib/systemd/system/docker.service.d/docker-sdn-ovs.conf

%files -n tuned-profiles-openshift-node
%defattr(-,root,root,-)
%{_prefix}/lib/tuned/openshift-node-host
%{_prefix}/lib/tuned/openshift-node-guest
%{_mandir}/man7/tuned-profiles-openshift-node.7*

%post -n tuned-profiles-openshift-node
recommended=`/usr/sbin/tuned-adm recommend`
if [[ "${recommended}" =~ guest ]] ; then
  /usr/sbin/tuned-adm profile openshift-node-guest > /dev/null 2>&1
else
  /usr/sbin/tuned-adm profile openshift-node-host > /dev/null 2>&1
fi

%preun -n tuned-profiles-openshift-node
# reset the tuned profile to the recommended profile
# $1 = 0 when we're being removed > 0 during upgrades
if [ "$1" = 0 ]; then
  recommended=`/usr/sbin/tuned-adm recommend`
  /usr/sbin/tuned-adm profile $recommended > /dev/null 2>&1
fi

%files clients
%{_datadir}/%{name}/linux/oc
%{_datadir}/%{name}/macosx/oc
%{_datadir}/%{name}/windows/oc.exe

%files dockerregistry
%defattr(-,root,root,-)
%{_bindir}/dockerregistry

%files pod
%defattr(-,root,root,-)
%{_bindir}/pod

%changelog
* Mon Aug 31 2015 Scott Dodson <sdodson@redhat.com> 3.0.1.900
- Revert "rpm: Now building AEP packages." (sdodson@redhat.com)
- Revert "rpm: Config location now /etc/origin/" (sdodson@redhat.com)
- Revert "rpm: atomic-enterprise bash completion now generated."
  (sdodson@redhat.com)
- Revert "rpm: Using _unitdir instead of _prefix and path."
  (sdodson@redhat.com)
- Revert "rpm: Link /etc/openshift to /etc/origin if it exists."
  (sdodson@redhat.com)
- Revert "Change /etc to %%{_sysconfdir}." (sdodson@redhat.com)
- Revert "rpm: Packages now generate configs when possible."
  (sdodson@redhat.com)
- Revert "Rename openshift.spec origin.spec" (sdodson@redhat.com)
- Revert "Origin and Atomic OpenShift package refactoring" (sdodson@redhat.com)
- Re-enable complex console integration tests (ffranz@redhat.com)
- ux for deleting a project, no api call implemented yet (gabe@ggruiz.me)
- Workaround slow ECDHE in F5 router tests (miciah.masters@gmail.com)
- fix typo in docker_version definition, handle origin pre-existing symlink
  (admiller@redhat.com)
- Convert zookeeper template to v1 (mfojtik@redhat.com)
- Fix bugz 1243529 - HAProxy template is overwritten by incoming changes.
  (smitram@gmail.com)
- Revert previous Vagrantfile cleanup (rpenta@redhat.com)
- Add empty state help for projects page (spadgett@redhat.com)
- F5 router implementation (miciah.masters@gmail.com)
- Use os::build::setup_env when building extended test package
  (mfojtik@redhat.com)
- buildchain: Fix resource shortcut (mkargaki@redhat.com)
- oc new-app with no arguments will suggest --search and --list
  (jhadvig@redhat.com)
- bump(github.com/openshift/openshift-sdn)
  5a5c409df14c066f564b6015d474d1bf88da2424 (rpenta@redhat.com)
- Return node IPs in GetNodes() SDN interface (rpenta@redhat.com)
- bump(github.com/openshift/source-to-image)
  00d1cb3cb9224bb59c0a37bb2bdd0100e20e1982 (cewong@redhat.com)
- document why namespaces are stripped (bparees@redhat.com)
- Cleanup Vagrantfile (rpenta@redhat.com)
- add extended test for s2i incremental builds using docker auth credentials to
  push and pull (bparees@redhat.com)
- plugins/osdn: multitenant service isolation support (danw@redhat.com)
- Add ServiceNetwork field to ClusterNetwork struct (danw@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  9d342eb61cfdcb1d77045ba69b27745f600385e3 (danw@redhat.com)
- Allow to override the default Jenkins image in example (mfojtik@redhat.com)
- Add support for dind image caching (marun@redhat.com)
- Improve graceful shutdown of dind daemon (marun@redhat.com)
- fix wf81 imagestream (bparees@redhat.com)
- Change default instance type (dmcphers@redhat.com)
- Fixup router test hostnames - good catch @Miciah (smitram@gmail.com)
- Restructure of nav layout and presentation at mobile resolutions to address
  https://github.com/openshift/origin/issues/3149 (sgoodwin@redhat.com)
- Add support for docker-in-docker dev cluster (marun@redhat.com)
- Prevent panic in import-image (ccoleman@redhat.com)
- Remove flakiness in webhook test (cewong@redhat.com)
- Add SOURCE_REF variable to builder container (mfojtik@redhat.com)
- change OpenShift references to Origin (pweil@redhat.com)
- Move documentation to test/extended/README.md (mfojtik@redhat.com)
- ext-tests: CLI interface docs (jhadvig@redhat.com)
- Initial docs about writing extended test (mfojtik@redhat.com)
- Remove sti-image-builder from our build-images flow (mfojtik@redhat.com)
- Add 'displayName' to Template (mfojtik@redhat.com)
- Fix 'pods "hello-openshift" cannot be updated' flake (jliggitt@redhat.com)
- make service targetPort consistent with container port (tangbixuan@gmail.com)
- Refactor vagrant provision scripts for reuse (marun@redhat.com)
- UPSTREAM: 13107: Fix portforward test flake with GOMAXPROCS > 1
  (jliggitt@redhat.com)
- UPSTREAM: 12162: Correctly error when all port forward binds fail
  (jliggitt@redhat.com)
- Minor cleanup (ironcladlou@gmail.com)
- Support prefixed deploymentConfig name (ironcladlou@gmail.com)
- Add vpc option to vagrantfile (dmcphers@redhat.com)
- Wait for the builder service account to get registry secrets in extended
  tests (mfojtik@redhat.com)
- Removing unused conversion tool, which was replaced with
  cmd/genconversion/conversion.go some time ago, already. (maszulik@redhat.com)
- Update k8s repository links and fix docs links (maszulik@redhat.com)
- Fix permission issues in zookeeper example (mfojtik@redhat.com)
- Make output directory symlinks relative links (stefw@redhat.com)
- Cleanup etcd install (ccoleman@redhat.com)
- Make config change triggers a default (ccoleman@redhat.com)
- Support generating DeploymentConfigs from run (ccoleman@redhat.com)
- UPSTREAM: 13011: Make run support other types (ccoleman@redhat.com)
- Add attach, run, and annotate to cli (ccoleman@redhat.com)
- Allow listen address to be overriden on api start (ccoleman@redhat.com)
- Completion generation can't run on Mac (ccoleman@redhat.com)
- Govet doesn't run on Mac (ccoleman@redhat.com)
- Split verify step into its own make task (ccoleman@redhat.com)
- Don't use _tmp or cp -u (ccoleman@redhat.com)
- Don't need to test same stuff twice (ccoleman@redhat.com)
- extended tests for setting forcePull in the 3 strategies; changes stemming
  from Ben's comments; some debug improvements; Michal's comments; address
  merge conflicts; adjust to extended test refactor (gmontero@redhat.com)
- Print line of error (ccoleman@redhat.com)
- Add stack dump to log on sigquit of sti builder (bparees@redhat.com)
- Overwriting a volume claim with --claim-name not working
  (ccoleman@redhat.com)
- change internal representation of rolebindings to use subjects
  (deads@redhat.com)
- remove export --all (deads@redhat.com)
- Tests failing at login, fix name of screenshots to be useful Remove the
  backporting of selenium since we no longer use phantom Remove phantomjs
  protractor config (jforrest@redhat.com)
- Remove double-enabled build controllers (jliggitt@redhat.com)
- add --all-namespaces to export (deads@redhat.com)
- fix --all (bparees@redhat.com)
- dump the namespaces at the end of e2e (bparees@redhat.com)
- Completion (ccoleman@redhat.com)
- OpenShift master setup example (ccoleman@redhat.com)
- Allow master-ip to set when running the IP directly (ccoleman@redhat.com)
- UPSTREAM: 12595 <drop>: Support status.podIP (ccoleman@redhat.com)
- Watch from the latest valid index for leader lease (ccoleman@redhat.com)
- add namespace to cluster SAR (deads@redhat.com)
- rpm: Added simple test case script for rpm builds. (smilner@redhat.com)
- Adding more retriable error types for push retry logic (jhadvig@redhat.com)
- Origin and Atomic OpenShift package refactoring (sdodson@redhat.com)
- Rename openshift.spec origin.spec (sdodson@redhat.com)
- update master for new recycler (mturansk@redhat.com)
- UPSTREAM: 5093+12603: adapt downward api volume to volume changes
  (deads@redhat.com)
- UPSTREAM: 6093+12603: adapt cephfs to volume changes (deads@redhat.com)
- UPSTREAM: 9870: configurable pv recyclers (deads@redhat.com)
- UPSTREAM: 12603: Expanded volume.Spec to full Volume and PV
  (deads@redhat.com)
- UPSTREAM: revert faab6cb: 9870: Allow Recyclers to be configurable
  (deads@redhat.com)
- disable SA secret ref limitting per SA (deads@redhat.com)
- Adding extended-tests for build-label (jhadvig@redhat.com)
- Add Docker labels (jhadvig@redhat.com)
- bump(openshift/source-to-image) a737bdd101de4a013758ad01f4bdd1c8d2f912b3
  (jhadvig@redhat.com)
- Extended test fixtures (jhadvig@redhat.com)
- Fix for issue #4035 - internally generated router keys are not unique.
  (smitram@gmail.com)
- Fix failing integration test expectation - we now return a service
  unavailable error rather than connect to 127.0.0.1:8080 (smitram@gmail.com)
- Include namespace in determining new-app dup objects (cewong@redhat.com)
- Use instance_type param (dmcphers@redhat.com)
- Remove default backend from the mix. In the first case, it returns incorrect
  info if something is serving on port 8080. The second bit is if nothing is
  running on port 8080, the cost to return a 503 is high. If someone wants
  custom 503 messages, they can always add a custom backend or use the
  errorfile 503 /path/to/page directive in a custom template.
  (smitram@gmail.com)
- UPSTREAM: 11827: allow permissive SA secret ref limitting (deads@redhat.com)
- Make the docker registry client loggable (ccoleman@redhat.com)
- bump(github.com/openshift/openshift-sdn):
  9dd0b510146571d42c5c9371b4054eae2dc5f82c (rpenta@redhat.com)
- Rename VindMap to VNIDMap (rpenta@redhat.com)
- Fixing the retry logic (jhadvig@redhat.com)
- Add standard vars to hook pod environment (ironcladlou@gmail.com)
- Make push retries more intelligent (jhadvig@redhat.com)
- Run e2e UI test in chrome (jliggitt@redhat.com)
- Remove dot imports from extended tests (mfojtik@redhat.com)
- display the host in 'oc status' (v.behar@free.fr)
- Typo in https proxy debug output (swapdisk@users.noreply.github.com)
- use push auth creds to pull previous image for incremental build
  (bparees@redhat.com)
- Fix sdn api field names to match openshift-sdn repo (rpenta@redhat.com)
- fixed -buildtags errors (skuznets@redhat.com)
- fixed -composites errors (skuznets@redhat.com)
- fixed -printf errors (skuznets@redhat.com)
- made verify-govet functional (skuznets@redhat.com)
- Bug 1247680 and 1251601 - new-app must validate --name instead of silently
  truncating and changing case (ffranz@redhat.com)
- Revert "Bug 1247680 - must not truncate svc names in the cli, rely on API
  validation" (ffranz@redhat.com)
- show build context in oc status (deads@redhat.com)
- make oc status build output consistent with deployments (deads@redhat.com)
- prevent kubectl/oc command drift (deads@redhat.com)
- Bug 1250676 - fixes --all-namespaces printer (ffranz@redhat.com)
- fixed printf errors (skuznets@redhat.com)
- enabled go tool -printf (skuznets@redhat.com)
- Add the DenyExecOnPrivileged admission control plugin to origin
  (cewong@redhat.com)
- Add namespace flag to trigger enable instructions (ironcladlou@gmail.com)
- Add the DenyExecOnPrivileged admission control plugin to origin
  (cewong@redhat.com)
- make readme instructions work (deads@redhat.com)
- fixed method error (skuznets@redhat.com)
- added go tool vet -methods (skuznets@redhat.com)
- Move extended tests to separate Go packages (mfojtik@redhat.com)
- Replace FatalErr with ginkgos Fail (jhadvig@redhat.com)
- add jenkins to imagestream definitions (bparees@redhat.com)
- Reuse the previously evaulated 'sni' acl. (smitram@gmail.com)
- Add path based reencrypt routes - makes the map files sorting generic, was
  missing os_tcp_be.map and fixes a bug with wrong map used for reencrypt
  traffic and add integration tests. (smitram@gmail.com)
- Show last three builds by default in the UI (spadgett@redhat.com)
- Bug 1251845 - app name validation should require first char is a letter
  (jforrest@redhat.com)
- bump(go-ldap/ldap): c265aaa27b1c60c66f6d4695c6f33eb8b28989ad
  (jliggitt@redhat.com)
- Make UI treat bearer token type case-insensitively (jliggitt@redhat.com)
- Add persistent storage jenkins template (bparees@redhat.com)
- Set +e when removing (jhadvig@redhat.com)
- Bug 1250153 - console doesnt accept git ref in create from source URL
  (jforrest@redhat.com)
- Use ginkgo to run extended tests and use -focus to select which tests to run
  (mfojtik@redhat.com)
- UPSTREAM: 12221: Allow custom namespace creation in e2e framework
  (mfojtik@redhat.com)
- fix help typo (deads@redhat.com)
- bump(openshift/source-to-image) 2e52377338d425a290e74192ba8d53bb22965b0d
  (bparees@redhat.com)
- Add build number annotation and update UI pod template (spadgett@redhat.com)
- kill all child processes (jhadvig@redhat.com)
- Review feedback (ccoleman@redhat.com)
- Bug 1248464 - fixes message about builds created by new-app
  (ffranz@redhat.com)
- Bug 1247680 - must not truncate svc names in the cli, rely on API validation
  (ffranz@redhat.com)
- Add SCC checking to Source build controller strategy (cewong@redhat.com)
- Remove omitempty from server types (ccoleman@redhat.com)
- Refactor master start to split responsibilities (ccoleman@redhat.com)
- Support election of controllers (ccoleman@redhat.com)
- fix integration tests (deads@redhat.com)
- Bug 1253538 - webhook URLs should have a lower case type
  (jforrest@redhat.com)
- Leader lease utility (ccoleman@redhat.com)
- Add simple hello-world template to validate deployment of routes to pods
  (jcantril@redhat.com)
- bump(fsouza/go-dockerclient): 42d06e2b125654477366c320dcea99107a86e9c2
  (bparees@redhat.com)
- fixed composites errors (skuznets@redhat.com)
- added go tools vet -composites (skuznets@redhat.com)
- added openldap image artifacts (skuznets@redhat.com)
- do not register build storage if disabled (pweil@redhat.com)
- UPSTREAM:12675: don't swallow bad request errors (pweil@redhat.com)
- Ensure CLI OAuth client always has a single redirect_uri
  (jliggitt@redhat.com)
- bump(github.com/RangelReale/osin): c07b3bd1ee57089f63e6325c0ea035ceed2e905c
  (jliggitt@redhat.com)
- UPSTREAM: vjeantet/ldapserver: 15: fix ldapserver test panic
  (jliggitt@redhat.com)
- Disable CAdvisor insecure port (jliggitt@redhat.com)
- fix BuildConfign typo (bparees@users.noreply.github.com)
- changed integration test build tags (skuznets@redhat.com)
- enabled go tool vet -buildtags (skuznets@redhat.com)
- fixed unusedresult errors (skuznets@redhat.com)
- added go tool vet -unusedresult (skuznets@redhat.com)
- fixed structtags errors (skuznets@redhat.com)
- enabled go tool vet -structtags (skuznets@redhat.com)
- fixred unreachable errors (skuznets@redhat.com)
- added go tool vet -unreachable (skuznets@redhat.com)
- Allow API or controllers to start independently (ccoleman@redhat.com)
- Disable starting builds of a particular type when you don't have access
  (cewong@redhat.com)
- Add BuildConfig change trigger for initial build trigger (cewong@redhat.com)
- UPSTREAM: 12544: Re-add ServiceSpreadingPriority priority algorithm
  (jliggitt@redhat.com)
- Remove metadata from bindata assets (jliggitt@redhat.com)
- bump(jteeuwen/go-bindata): bfe36d3254337b7cc18024805dfab2106613abdf
  (jliggitt@redhat.com)
- Fix apiVersion in UI calls, re-enable project creation test
  (jliggitt@redhat.com)
- fix the preferred API order (deads@redhat.com)
- kube test artifact updates (deads@redhat.com)
- update to new testclient (deads@redhat.com)
- boring refactors (deads@redhat.com)
- UPSTREAM: 12669: make printer tolerate missing template flag
  (deads@redhat.com)
- UPSTREAM: 12498: Re-add timeouts for kubelet which is not in the upstream PR.
  (deads@redhat.com)
- UPSTREAM: 12602: expose e2e methods for downstream use (deads@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: 12552: only return name field (deads@redhat.com)
- UPSTREAM: 5093: adding downward api volume plugin (deads@redhat.com)
- UPSTREAM: 9844: EmptyDir volume SELinux support (deads@redhat.com)
- UPSTREAM: 9870: Allow Recyclers to be configurable (deads@redhat.com)
- UPSTREAM: 7893: scc allocation interface methods (deads@redhat.com)
- UPSTREAM: 6649: Add CephFS volume plugin (deads@redhat.com)
- UPSTREAM: 7893: scc (pweil@redhat.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (deads@redhat.com)
- UPSTREAM: <to-fix>: bind variable to flags, not just flagnames
  (deads@redhat.com)
- UPSTREAM: <drop>: add back flag types to reduce noise during this rebase
  (deads@redhat.com)
- UPSTREAM: <none>: search for mount binary in hostfs (ccoleman@redhat.com)
- UPSTREAM: <none>: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: <none>: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: <carry>: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: <carry>: kube dep for tests (deads@redhat.com)
- UPSTREAM: <carry>: reallow the ability to post across namespaces in api
  (pweil@redhat.com)
- UPSTREAM: <carry>: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: Allow pod start to be delayed in Kubelet
  (ccoleman@redhat.com)
- UPSTREAM: <carry>: Enable LimitSecretReferences in service account
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: implement a generic webhook storage (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (deads@redhat.com)
- UPSTREAM: <carry>: v1beta3 (deads@redhat.com)
- bump(github.com/prometheus/client_golang)
  692492e54b553a81013254cc1fba4b6dd76fad30 (deads@redhat.com)
- bump(github.com/spf13/cobra) 385fc87e4343efec233811d3d933509e8975d11a
  (deads@redhat.com)
- bump(github.com/fsouza/go-dockerclient)
  933433faa3e1c0bbc825b251143f8e77affbf797 (deads@redhat.com)
- bump(google.golang.org/api) 0c2979aeaa5b573e60d3ddffe5ce8dca8df309bd
  (deads@redhat.com)
- bump(k8s.io/kubernetes) 44c91b1a397e0580d403eb9e9cecd1dac3da0b25
  (deads@redhat.com)
- Disable create project in console integration tests (ffranz@redhat.com)
- Upgrade tag and import-image to be easier (ccoleman@redhat.com)
- Disable complex web console test scenarios until we can have clear runs
  (ffranz@redhat.com)
- added go vet to travis (skuznets@redhat.com)
- added go vet verification script (skuznets@redhat.com)
- Import and pull from v2 registries (ccoleman@redhat.com)
- accept --sa as argument for rolebinding (deads@redhat.com)
- add required value to parameter describer (bparees@redhat.com)
- allow regex test identifiers for docker int tests (skuznets@redhat.com)
- Rebuild assets (jliggitt@redhat.com)
- bump(github.com/jteeuwen/go-bindata):
  dce55d09e24ac40a6e725c8420902b86554f8046 (jliggitt@redhat.com)
- Refactor sorting by CreationTimestamp (rhcarvalho@gmail.com)
- do not remove output image when doing s2i build (bparees@redhat.com)
- Improve help on volumes and allow claim creation (ccoleman@redhat.com)
- Web console integration tests (contact@fabianofranz.com)
- rpm: Packages now generate configs when possible. (smilner@redhat.com)
- Trigger SDN node event when node ip changes (rpenta@redhat.com)
- bump openshift-sdn/ovssubnet(b4d90f205160ccf4a6e9c662f1b4568a6ac243f5)
  (rpenta@redhat.com)
- Prevent ipv6 bind for unsupported endpoints (ccoleman@redhat.com)
- Adapt flagtypes.Addr to support ipv6 hosts (ccoleman@redhat.com)
- Allow the bind address to be configured (ccoleman@redhat.com)
- add required field to sample templates (bparees@redhat.com)
- UPSTREAM: 211: Allow listen only ipv4 (ccoleman@redhat.com)
- rpm: added new bin files to ovs sections. (smilner@redhat.com)
- bump(github.com/openshift/source-to-image)
  c33ec325ac5b136e02cb999893aae0bdec4292ac (cewong@redhat.com)
- Add fake factory (mkargaki@redhat.com)
- Extended tested endpoints (miminar@redhat.com)
- refactored test to use upstream method (skuznets@redhat.com)
- fix package names for conversion generators (deads@redhat.com)
- UPSTREAM: <drop>: handle kube package refactor (deads@redhat.com)
- handle kube package refactors (deads@redhat.com)
- Add port table to browse services page (spadgett@redhat.com)
- More polishment for integration test (miminar@redhat.com)
- Inline test cases (miminar@redhat.com)
- Godoced exported method (miminar@redhat.com)
- Test improvements (miminar@redhat.com)
- fix remove-users help (deads@redhat.com)
- Added integration test for disabling web console (miminar@redhat.com)
- add layout.attrs to web console (admin@benjaminapetersen.me)
- update comments to accurately reflect validation (pweil@redhat.com)
- UPSTREAM: 12498: Re-add timeouts for kubelet which is not in the upstream PR.
  (pweil@redhat.com)
- Use skydns metrics (ccoleman@redhat.com)
- UPSTREAM: 219: External metrics registration (ccoleman@redhat.com)
- Gitserver should use DNS name for connecting to master (ccoleman@redhat.com)
- Change /etc to %%{_sysconfdir}. (avagarwa@redhat.com)
- update HACKING.md (skuznets@redhat.com)
- Change router to use host networking - adds a new --host-network option (the
  default). Setting it to false makes it use the container network stack.
  (smitram@gmail.com)
- output external serialization for router/registry (deads@redhat.com)
- Deny access to Web Console (miminar@redhat.com)
- UPSTREAM: search for mount binary in hostfs (ccoleman@redhat.com)
- refactors for review (pweil@redhat.com)
- non-interesting refactors (pweil@redhat.com)
- add group commands (deads@redhat.com)
- Add commas between pod template ports in UI (spadgett@redhat.com)
- Support auth in the gitserver (ccoleman@redhat.com)
- UPSTREAM:<carry>:kube dep for tests (pweil@redhat.com)
- UPSTREAM:<carry>:reallow the ability to post across namespaces in api
  installer (pweil@redhat.com)
- UPSTREAM:12271:expose codec in storage (pweil@redhat.com)
- UPSTREAM: 10636: Split kubelet server initialization for easier reuse
  (pweil@redhat.com)
- UPSTREAM: 9844: EmptyDir volume SELinux support (pmorie@gmail.com)
- UPSTREAM: carry: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: 5093: adding downward api volume plugin (salvatore-
  dario.minonne@amadeus.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (abhgupta@redhat.com)
- UPSTREAM: 6649: Add CephFS volume plugin (deads@redhat.com)
- UPSTREAM: <carry>: Enable LimitSecretReferences in service account admission
  (jliggitt@redhat.com)
- UPSTREAM: <none>: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: <none>: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (ccoleman@redhat.com)
- UPSTREAM: 9321: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: <carry>: Allow pod start to be delayed in Kubelet
  (ccoleman@redhat.com)
- UPSTREAM: 9870: Allow Recyclers to be configurable (deads@redhat.com)
- UPSTREAM: 7893: scc allocation interface methods (deads@redhat.com)
- UPSTREAM: <carry>: implement a generic webhook storage (ccoleman@redhat.com)
- UPSTREAM: 8607: service account groups (deads@redhat.com)
- UPSTREAM: 9472: expose name validation method (deads@redhat.com)
- UPSTREAM:<carry>: v1beta3 (pweil@redhat.com)
- UPSTREAM:7893: scc (pweil@redhat.com)
- bump(github.com/GoogleCloudPlatform/kubernetes):b73c53c37d06bc246eb862a83df51
  c8fd75994f8 (pweil@redhat.com)
- Allow subjectaccessreview to be invoked for a token (ccoleman@redhat.com)
- Newlines should be between warnings and output (ccoleman@redhat.com)
- Split hack/test-cmd.sh into individual tests (ccoleman@redhat.com)
- Add completions (ccoleman@redhat.com)
- Add a -q option for project to print the name (ccoleman@redhat.com)
- readlink -f doesn't work on Mac, fix tests (ccoleman@redhat.com)
- Remove unused constant variables (nakayamakenjiro@gmail.com)
- Fix silly error in example in test-integration.sh (pmorie@gmail.com)
- Update UI to oapi/v1 (spadgett@redhat.com)
- Update UI to k8s API version v1 (spadgett@redhat.com)
- Simplify error message improving responsiveness (rhcarvalho@gmail.com)
- Tweak test-integration.sh pipeline and add examples (pmorie@gmail.com)
- Extended MasterConfig for feature flags (miminar@redhat.com)
- Recognize atomic-enterprise binary namu (miminar@redhat.com)
- Make /token/display less like an API, send CLI redirect to informational page
  (jliggitt@redhat.com)
- Update documentation for new --host-network option. (smitram@gmail.com)
- Update build-chain examples to match product docs (adellape@redhat.com)
- LDAP group sync proposal (skuznets@redhat.com)
- descriptions for netnamespace objects (rchopra@redhat.com)
- multitenant sdn support; bump openshift-
  sdn/ovssubnet(74738c359b670c6e12435c1af10ee2802a4b0b64) vagrant instance
  updated to consume 2G (rchopra@redhat.com)
- add entrypoint for extended test (deads@redhat.com)
- Revert hack/test-cmd.sh changes from #3732 (ccoleman@redhat.com)
- Remove unnecessary godep requirement in extended tests
  (nagy.martin@gmail.com)
- Update hello-openshift example's README (nakayamakenjiro@gmail.com)
- remove 'experimental' from v1 log output (deads@redhat.com)
- support update on project (deads@redhat.com)
- rpm: Link /etc/openshift to /etc/origin if it exists. (smilner@redhat.com)
- Fix integration tests (mfojtik@redhat.com)
- Making test DRYer (jhadvig@redhat.com)
- Allow empty template parameters that can be generated (spadgett@redhat.com)
- sort edge map file (pweil@redhat.com)
- rpm: Using _unitdir instead of _prefix and path. (smilner@redhat.com)
- rpm: atomic-enterprise bash completion now generated. (smilner@redhat.com)
- rpm: Config location now /etc/origin/ (smilner@redhat.com)
- rpm: Now building AEP packages. (smilner@redhat.com)
- Refactor hack/test-extended to allow grouping (mfojtik@redhat.com)
- Refactor extended tests to use upstream e2e framework (mfojtik@redhat.com)
- Add openshift CLI testing framework (mfojtik@redhat.com)
- UPSTREAM: 12221: Allow custom namespace creation in e2e framework
  (mfojtik@redhat.com)
- bump(github.com/GoogleCloudPlatform/kubernetes/test/e2e)
  cd821444dcf3e1e237b5f3579721440624c9c4fa (mfojtik@redhat.com)
- bump(github.com/onsi/ginkgo) d981d36e9884231afa909627b9c275e4ba678f90
  (mfojtik@redhat.com)
- Fix 'oc' command to allow redirection of stdout (mfojtik@redhat.com)
- Enforce required on template parameters in UI (spadgett@redhat.com)
- prevent nil panic (deads@redhat.com)
- honor new group resources in authorizer (deads@redhat.com)
- handle cache.Index updates (deads@redhat.com)
- UPSTREAM: 11925: support multiple index values for a single object
  (deads@redhat.com)
- UPSTREAM: 11171: Added ability to list index keys (deads@redhat.com)
- merge AE docs work to OS (pweil@redhat.com)
- Allow additional image stream build triggers on BuildConfig
  (cewong@redhat.com)
- Add dns prefixes to default cert (jliggitt@redhat.com)
- Sort printed builds according to creation timestamp (nagy.martin@gmail.com)
- add required field to parameters (bparees@redhat.com)
- Generate the same labels in the UI as the CLI (spadgett@redhat.com)
- update to allow /api and /api/ for negotiation (deads@redhat.com)
- minor doc updates trying to run through README; comments from Ben
  (gmontero@redhat.com)
- routing.md update for router service account (pweil@redhat.com)
- return if SCCs can't be listed (pweil@redhat.com)
- add router service account requirements (pweil@redhat.com)
- bump(github.com/openshift/source-to-image)
  cfd95f2873bf687fbd2a4f32721462200d1b704a (bparees@redhat.com)
- Minor fixes (dmcphers@redhat.com)
- Minor tweak to hack/install-assets.sh for the RHEL AMI (bleanhar@redhat.com)
- shorted SAR response (deads@redhat.com)
- oc new-app --list (contact@fabianofranz.com)
- Add rolling update strategy for router with -10%% update percentage - fixes
  issue #3861 (smitram@gmail.com)
- Add rolling update strategy for router with -10%% update percentage - fixes
  issue #3861 (smitram@gmail.com)
- customForcePull:  update swagger spec (gmontero@redhat.com)
- changes from update-generated-deep-copies.sh (gmontero@redhat.com)
- customForcePull:  changes to allow force pull of customer build strategy,
  including updates based on review with Ben; address gofmt issues
  (gmontero@redhat.com)
- Special case upstream kubernetes api package unit tests (pmorie@gmail.com)
- fix gendocs (deads@redhat.com)
- Added verification script for Swagger API object descriptions
  (skuznets@redhat.com)
- fail a build if there are no container statuses in the build pod
  (bparees@redhat.com)
- Add TLS support to docker client (cewong@redhat.com)
- Sync with master (sdodson@redhat.com)
- Add mode http - fixes issue #3926. Add similar checks to the sni code path
  for specific path based lookups before using the host header lookup (in
  os_edge_http_be.map). (smitram@gmail.com)
- UPSTREAM: 9844: EmptyDir volume SELinux support (pmorie@gmail.com)
- UPSTREAM: 9384: Make emptyDir volumes work for non-root UIDs
  (pmorie@gmail.com)
- UPSTREAM: 9844: revert origin e53e78f: Support emptyDir volumes for
  containers running as uid != 0 (pmorie@gmail.com)
- UPSTREAM: 9384: revert origin 4e5cebd: EmptyDir volumes for non-root 2/2
  (pmorie@gmail.com)
- UPSTREAM: 9384: revert origin b92d1c7: Handle SecurityContext correctly for
  emptyDir volumes (pmorie@gmail.com)
- UPSTREAM: 9844: revert origin 73b2454: fix emptyDir idempotency bug
  (pmorie@gmail.com)
- UPSTREAM: 9384: revert origin 2d83001: Make emptyDir work when SELinux is
  disabled (pmorie@gmail.com)
- UPSTREAM: 9384: revert origin ac5f35b: Increase clarity in empty_dir volume
  plugin (pmorie@gmail.com)
- UPSTREAM: 9384: revert origin 6e57b2d: Make empty_dir unit tests work with
  SELinux disabled (pmorie@gmail.com)
- export: Initialize map for image stream tags
  (kargakis@users.noreply.github.com)
- add Group kind (deads@redhat.com)
- add cli display coverage tests (deads@redhat.com)
- issue3894: update vagrant sections of contributing and readme doc to account
  for recent tweaks in runtime (gmontero@redhat.com)
- test-cmd.sh broken on Mac (ccoleman@redhat.com)
- Generated docs (ccoleman@redhat.com)
- Make naming less specific to OpenShift (ccoleman@redhat.com)
- buildchain: Refactor to use the graph library
  (kargakis@users.noreply.github.com)
- Updated update scripts to allow for a settable output directory
  (skuznets@redhat.com)
- Newapp: fix image stream name used in deployment trigger (cewong@redhat.com)
- Cleanup deployment describe slightly (ccoleman@redhat.com)
- Add app=<name> label to new-app groups (ccoleman@redhat.com)
- Release tar should contain smaller oc (ccoleman@redhat.com)
- UPSTREAM: 11766: make kubelet prefer ipv4 address if available
  (deads@redhat.com)
- Remove gographviz (kargakis@users.noreply.github.com)
- UPSTREAM: 9384: Make empty_dir unit tests work with SELinux disabled
  (pmorie@gmail.com)
- render graph using DOT (deads@redhat.com)
- Include list of recent builds in error message (rhcarvalho@gmail.com)
- clean up handling of no output builds (bparees@redhat.com)
- UPSTREAM: 11303: Add CA data to service account tokens if missing or
  different (jliggitt@redhat.com)
- Make 'make check' run the kubernetes unit tests (pmorie@gmail.com)
- Add information about copying kubernetes artifacts in to HACKING.md
  (pmorie@gmail.com)
- UPSTREAM: add dependencies for packages missing for upstream unit tests
  (pmorie@gmail.com)
- Add third party deps stub (pmorie@gmail.com)
- UPSTREAM: 11147: Fix TestRunExposeService (pmorie@gmail.com)
- Add upstream examples, README files, etc (pmorie@gmail.com)
- Add copy-kube-artifacts.sh script (pmorie@gmail.com)
- WIP: make hack/test-go.sh run upstream unit tests (pmorie@gmail.com)
- UPSTREAM: 11698: Make copy_test.go failures easier to debug
  (pmorie@gmail.com)
- Newapp: Use labels for deployment config and service selectors
  (cewong@redhat.com)
- reintroduce missing conversions for imagestream kind and lowercase build
  trigger types (bparees@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: revert da0a3d: 9009: Retry service account update when adding token
  reference (deads@redhat.com)
- Generated docs (ccoleman@redhat.com)
- update swagger spec to match (deads@redhat.com)
- Add Cache-Control header (spadgett@redhat.com)
- Update swagger spec (spadgett@redhat.com)
- fix colliding serial numbers in certs (deads@redhat.com)
- Update object-describer to v1.0.2 (jforrest@redhat.com)
- Move Build cancellation and Pod deletion logic to HandleBuild
  (nagy.martin@gmail.com)
- bump(github.com/openshift/source-to-image)
  587d0f0a63589436322ac2ba6e01abb2f98a8dae (cewong@redhat.com)
- Updated Swagger spec, added Swagger spec verification (skuznets@redhat.com)
- Add a 'rsh' command for simpler remote access (ccoleman@redhat.com)
- Fix incorrect ENV["VAGRANT_LIBVIRT_URI"] if statement which causes "Missing
  required arguments: libvirt_uri (ArgumentError)" (takayoshi@gmail.com)
- UPSTREAM: 11729: Make exec reusable (ccoleman@redhat.com)
- Print consistent output for oadm manage-node --list-pods (rpenta@redhat.com)
- oc volume will allow changing volume type in case of unabiguous mount-path
  (rpenta@redhat.com)
- UPSTREAM: <carry>: Correct v1 deep_copy_generated.go (pmorie@gmail.com)
- Fix for tito 0.6.0 (sdodson@redhat.com)
- add reconcile-cluster-roles command (deads@redhat.com)
- Customize the events table layout and styles for better readability on mobile
  devices. (sgoodwin@redhat.com)
- UPSTREAM: 11669: add non root marker to sc types (pweil@redhat.com)
- OS: validation of host network and host ports in the SCC. (pweil@redhat.com)
- handle kube resources in project request template (deads@redhat.com)
- Bug 1245455 - fixes duplicated search results with openshift namespace
  (contact@fabianofranz.com)
- Bug 1245447 - fixes template search (contact@fabianofranz.com)
- use env var for config arg value (pweil@redhat.com)
- Rolling updater enhancements (ironcladlou@gmail.com)
- output invalid config field name (deads@redhat.com)
- Bump release for brew rebuild (sdodson@redhat.com)
- UPSTREAM: 7893: validation of host network and host ports in the SCC.
  (pweil@redhat.com)
- New-app: set name of image stream with --name argument (cewong@redhat.com)
- don't fail status on forbidden lists (deads@redhat.com)
- update forbidden error to include structured kind (deads@redhat.com)
- Adding kubectl symlink for atomic host compatibility (bleanhar@redhat.com)
- Diff whole template for deployment config changes (ironcladlou@gmail.com)
- add tls termination type to printer and describer (pweil@redhat.com)
- Add "Show older builds" link to browse builds (spadgett@redhat.com)
- new-app search/list (contact@fabianofranz.com)
- make oc status output describeable (deads@redhat.com)
- Vagrant: Allow override of IP addresses (marun@redhat.com)
- Allow registry client to work with registries that don't implement
  repo/tag/[tag] (cewong@redhat.com)
- do not use vagrant shared dir for volumes (pweil@redhat.com)
- do not use vagrant shared dir for volumes (pweil@redhat.com)
- Don't handle errors for dcs on retry failures
  (kargakis@users.noreply.github.com)
- add revision info to build descriptions (bparees@redhat.com)
- make fake client thread-safe (deads@redhat.com)
- UPSTREAM: 11597: make fake client thread-safe (deads@redhat.com)
- Refine canary text a bit more (ccoleman@redhat.com)
- Line up breadcrumbs and content on create from template page
  (spadgett@redhat.com)
- UPSTREAM: 10062: Rolling updater enhancements (ironcladlou@gmail.com)
- UPSTREAM: 10062: revert origin 316c2e84783fdb93450865eb8801f9d4dbe1f79c:
  support acceptance check in rolling updater (ironcladlou@gmail.com)
- Defer to Kubernetes factory where appropriate
  (kargakis@users.noreply.github.com)
- add dueling rc warning (deads@redhat.com)
- add graph markers (deads@redhat.com)
- OSE: Set defaultImageFormat to openshift3/ose-${component}:${version}
  (sdodson@redhat.com)
- Show more detail on browse image streams page (spadgett@redhat.com)
- expose: Default to the service generator when not exposing services
  (kargakis@users.noreply.github.com)
- Minor fixes to deployment README (rhcarvalho@gmail.com)
- Add canary doc (ccoleman@redhat.com)
- Deployment examples (ccoleman@redhat.com)
- Route should default to name, not serviceName (ccoleman@redhat.com)
- Fix nodeSelector enforcement by the kubelet (jliggitt@redhat.com)
- Fix errors creating from source in UI (spadgett@redhat.com)
- UPSTREAM: 10647 (carry until 10656): increase Kubelet timeouts to 1 hour
  (agoldste@redhat.com)
- Remove generated name from container ports (jliggitt@redhat.com)
- status: Warn for circular deps in buildConfigs
  (kargakis@users.noreply.github.com)
- cluster groups proposal (deads@redhat.com)
- Handle unrecognized types in DataService.createList() (spadgett@redhat.com)
- Default DNS name should change (ccoleman@redhat.com)
- Remove 12MB from the oc binary (ccoleman@redhat.com)
- react to gonum/graph rebase (deads@redhat.com)
- bump(github.com/gonum/graph)bde6d0fbd9dec5a997e906611fe0364001364c41
  (deads@redhat.com)
- remove auto build triggering and make jenkins auto deploy work
  (bparees@redhat.com)
- always show markers is oc status (deads@redhat.com)
- oc exec upgrade.md (deads@redhat.com)
- examples/sample-app: Use the registry kubeconfig, not master
  (walters@verbum.org)
- Test resource builder file extensions (jliggitt@redhat.com)
- Duplicate serials were being handed out because objects were copied
  (ccoleman@redhat.com)
- Move NoNamespaceKeyFunc into origin (jliggitt@redhat.com)
- UPSTREAM: revert 6cc0c51: Ensure no namespace on create/update root scope
  types (jliggitt@redhat.com)
- Describe security in readme (ccoleman@redhat.com)
- UPSTREAM: carry: support pointing oc exec to old openshift server
  (deads@redhat.com)
- UPSTREAM: 11333: pass along status errors for upgrades (deads@redhat.com)
- Update oc logs examples and docs (kargakis@users.noreply.github.com)
- make claim name parameterized (bparees@redhat.com)
- UPSTREAM: 10866: don't check extension for single files (jliggitt@redhat.com)
- fix racy SAR test (deads@redhat.com)
- clean up jenkins example (bparees@redhat.com)
- Web Console: Handle docker and custom builder strategy in templates
  (spadgett@redhat.com)
- update policy for pods/exec (deads@redhat.com)
- allow multiple edges of different kinds between nodes (deads@redhat.com)
- [docs] group cli commands; add missing ones (tnguyen@redhat.com)
- Output emptyDir notice to standard error (nagy.martin@gmail.com)
- Fix command descriptions and alignment (ccoleman@redhat.com)
- Run hack/test-assets first and fail if error (ccoleman@redhat.com)
- Completion and doc updates (ccoleman@redhat.com)
- Refactor for printer/namespace changes (ccoleman@redhat.com)
- Update completions (ccoleman@redhat.com)
- Don't print subcommands info (ccoleman@redhat.com)
- Print the version of the master and node on start (ccoleman@redhat.com)
- Provide a way to get the exact IP used by the master (ccoleman@redhat.com)
- Use containerized builds (ccoleman@redhat.com)
- UPSTREAM: <carry>: Leave v1beta3 enabled for now (ccoleman@redhat.com)
- UPSTREAM: 10024: add originator to reflector logging (deads@redhat.com)
- UPSTREAM: 9384: Increase clarity in empty_dir volume plugin
  (pmorie@gmail.com)
- UPSTREAM: 9384: Fixes for empty_dir merge problem (pmorie@gmail.com)
- UPSTREAM: 10841: Default --ignore-not-found to true for delete --all
  (jliggitt@redhat.com)
- UPSTREAM: <carry>: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- UPSTREAM: 9971: add imports for map conversion types (bparees@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: 5093: adding downward api volume plugin (salvatore-
  dario.minonne@amadeus.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (abhgupta@redhat.com)
- UPSTREAM: 6649: Add CephFS volume plugin (deads@redhat.com)
- UPSTREAM: 9976: search for mount binary in hostfs (ccoleman@redhat.com)
- UPSTREAM: 9976: nsenter path should be relative (ccoleman@redhat.com)
- UPSTREAM: 8530: GCEPD mounting on Atomic (deads@redhat.com)
- UPSTREAM: <carry>: Enable LimitSecretReferences in service account admission
  (jliggitt@redhat.com)
- UPSTREAM: <none>: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: <none>: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: <carry>: Disable UIs for Kubernetes and etcd (ccoleman@redhat.com)
- UPSTREAM: 9844: fix emptyDir idempotency bug (deads@redhat.com)
- UPSTREAM: 9384: Handle SecurityContext correctly for emptyDir volumes
  (pmorie@gmail.com)
- UPSTREAM: 9384: Make emptyDir work when SELinux is disabled
  (pmorie@gmail.com)
- UPSTREAM: 9384: EmptyDir volumes for non-root 2/2 (deads@redhat.com)
- UPSTREAM: 9844: Support emptyDir volumes for containers running as uid != 0
  (deads@redhat.com)
- UPSTREAM: 9321: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: 9971: generated conversion updates (deads@redhat.com)
- UPSTREAM: 10636(extra): patch to fix kubelet startup (deads@redhat.com)
- UPSTREAM: <carry>: Allow pod start to be delayed in Kubelet
  (ccoleman@redhat.com)
- UPSTREAM: 10636: Split kubelet server initialization for easier reuse
  (deads@redhat.com)
- UPSTREAM: 10635: Cloud provider should return an error (deads@redhat.com)
- UPSTREAM: 9870: Allow Recyclers to be configurable (deads@redhat.com)
- UPSTREAM: 7893: scc allocation interface methods (deads@redhat.com)
- UPSTREAM: 10062: support acceptance check in rolling updater
  (deads@redhat.com)
- UPSTREAM: <carry>: implement a generic webhook storage (ccoleman@redhat.com)
- UPSTREAM: <carry>: Ensure no namespace on create/update root scope types
  (jliggitt@redhat.com)
- UPSTREAM: 8607: service account groups (deads@redhat.com)
- UPSTREAM: 9472: expose name validation method (deads@redhat.com)
- UPSTREAM: 7893: scc (deads@redhat.com)
- bump(github.com/GoogleCloudPlatform/kubernetes):v1.0.0 (ccoleman@redhat.com)
- issue2740: updates to debugging doc for SELinux intermittent label issue
  (gmontero@redhat.com)
- status to indicate resources with broken secret/SA refs (deads@redhat.com)
- add graph analysis helpers (deads@redhat.com)
- issue1875: make the force pull option configurable in the sti build strategy
  definition; various upstream documentation clarifications / enhancements;
  comments around reqs for coding/testing changes that run in the builder pod;
  fixes after merging (changes lost); incorporate comments from Ben
  (gmontero@redhat.com)
- display standalone rcs (deads@redhat.com)
- Split oc and gitserver into their own binaries (ccoleman@redhat.com)
- Fix help message for client-certificate (chmouel@redhat.com)
- show standalone pods that back services (deads@redhat.com)
- suggest oc status from new-app (deads@redhat.com)
- Group commands in oadm for ease of use (rpenta@redhat.com)
- fix mutex for projectstatus (deads@redhat.com)
- README for hacking CLI commands (contact@fabianofranz.com)
- Show command to load templates on "Add to Project" page (spadgett@redhat.com)
- deploy: --enable-triggers should be used alone
  (kargakis@users.noreply.github.com)
- Clarify policy command on all projects page (spadgett@redhat.com)
- Added test for external kube proxied watches (skuznets@redhat.com)
- Issue 3502 - removing label propagation to build pods in build controller.
  (maszulik@redhat.com)
- LDAP password authenticator (jliggitt@redhat.com)
- Add scala source detector (jatescher@gmail.com)
- show RCs for services in oc status (deads@redhat.com)
- bump(github.com/openshift/source-to-image)
  72ed2c7edc4c4e03d490716404a25a6b7a15c890 (cewong@redhat.com)
- Handle "" for service.spec.portalIP on overview page (spadgett@redhat.com)
- return api error for privilege escalation attempt (deads@redhat.com)
- parallel resource lists for status (deads@redhat.com)
- Defer closing resp.Body after issuing an HTTP request
  (kargakis@users.noreply.github.com)
- UPSTREAM: 10024: add originator to reflector logging (deads@redhat.com)
- bump(github.com/vjeantet/asn1-ber): 85041cd0f4769ebf4a5ae600b1e921e630d6aff0
  (jliggitt@redhat.com)
- bump(github.com/vjeantet/ldapserver):
  5700661e721f508db936af42597a254c4ea6aea4 (jliggitt@redhat.com)
- bump(gopkg.in/asn1-ber.v1): 9eae18c3681ae3d3c677ac2b80a8fe57de45fc09
  (jliggitt@redhat.com)
- bump(github.com/go-ldap/ldap): 83e65426fd1c06626e88aa8a085e5bfed0208e29
  (jliggitt@redhat.com)
- Simplify rollback arguments (ironcladlou@gmail.com)
- Added test cases for HandleBuildPodDeletion and HandleBuildDeletion methods
  in build controller. (maszulik@redhat.com)
- refactor internal build api to match v1 (bparees@redhat.com)
- Docker registry client: handle [registry]/[name] specs (cewong@redhat.com)
- scaler: Sync with upstream behavior (kargakis@users.noreply.github.com)
- add masterCA to SA token controller (deads@redhat.com)
- Update headers and breadcrumbs to match button text (spadgett@redhat.com)
- Set expanded property on ng-repeat child scope for tasks
  (spadgett@redhat.com)
- Expose oapi (jliggitt@redhat.com)
- Vagrantfile: enable running on remote libvirtd (lmeyer@redhat.com)
- Bug 1232177 - handle mutually exclusive flags on oc process
  (contact@fabianofranz.com)
- add kubectl patch (deads@redhat.com)
- Sync .jshint options between root .jshintrc & test/.jshintrc, then fix
  outstanding errors (admin@benjaminapetersen.me)
- indicate builds that can't push (deads@redhat.com)
- UPSTREAM: 9384: Increase clarity in empty_dir volume plugin
  (pmorie@gmail.com)
- Awkward text wrapping on overview page (jhadvig@redhat.com)
- UPSTREAM: 9384: Fixes for empty_dir merge problem (pmorie@gmail.com)
- Add link to dismiss builds from overview (spadgett@redhat.com)
- UPSTREAM: 10841: Default --ignore-not-found to true for delete --all
  (jliggitt@redhat.com)
- [RPMs] Add nfs-utils to openshift-node requires (sdodson@redhat.com)
- Add 1.0.0 k8s v1 compatibility test (jliggitt@redhat.com)
- UPSTREAM: Carry: Add deprecated fields to migrate 1.0.0 k8s v1 data
  (jliggitt@redhat.com)
- Fix confusing output when cancelling deployments (ironcladlou@gmail.com)
- Remove unused function in CatalogImagesController (spadgett@redhat.com)
- Remove selection highlighting when sidebar hidden (spadgett@redhat.com)
- Remove "There is no service" message from overview (spadgett@redhat.com)
- Updating sti-image-builder with latest s2i (maszulik@redhat.com)
- run e2e cleanup as system:admin (deads@redhat.com)
- bump(github.com/openshift/source-to-
  image):e28fc867a72a6f2d1cb9898e0ce47c70e26909eb (maszulik@redhat.com)
- Clean-up desired replicas annotation for a complete deployment
  (kargakis@users.noreply.github.com)
- UPSTREAM: 9971: add imports for map conversion types (bparees@redhat.com)
- UPSTREAM: 9009: Retry service account update when adding token reference
  (deads@redhat.com)
- UPSTREAM: 5093: adding downward api volume plugin (salvatore-
  dario.minonne@amadeus.com)
- UPSTREAM: 8890: Allowing ActiveDeadlineSeconds to be updated for a pod
  (abhgupta@redhat.com)
- Avoid flicker on overview page when scaling (spadgett@redhat.com)
- Cleaned CONTRIBUTING.adoc and added information about problems with vagrant's
  synced folders. (maszulik@redhat.com)
- Image pruning improvements (agoldste@redhat.com)
- make imagestreamtag usage consistent (deads@redhat.com)
- prevent skydns metrics panic (deads@redhat.com)
- DeepCopy in Scheme (deads@redhat.com)
- update conversion/deep-copy generator (deads@redhat.com)
- NewProxier port range (deads@redhat.com)
- swagger API changes (deads@redhat.com)
- boring refactors (deads@redhat.com)
- UPSTREAM: 6649: Add CephFS volume plugin (deads@redhat.com)
- UPSTREAM: search for mount binary in hostfs (ccoleman@redhat.com)
- UPSTREAM: nsenter path should be relative (ccoleman@redhat.com)
- UPSTREAM: Run had invalid arguments (ccoleman@redhat.com)
- UPSTREAM: 8530: GCEPD mounting on Atomic (deads@redhat.com)
- UPSTREAM: 10169: Work around for PDs stop mounting after a few hours issue
  (deads@redhat.com)
- UPSTREAM: Enable LimitSecretReferences in service account admission
  (jliggitt@redhat.com)
- UPSTREAM: Hack date-time format on *util.Time (ccoleman@redhat.com)
- UPSTREAM: Suppress aggressive output of warning (ccoleman@redhat.com)
- UPSTREAM: Disable UIs for Kubernetes and etcd (ccoleman@redhat.com)
- UPSTREAM: 9844: fix emptyDir idempotency bug (deads@redhat.com)
- UPSTREAM: MISSING PULL: Handle SecurityContext correctly for emptyDir volumes
  (pmorie@gmail.com)
- UPSTREAM: MISSING PULL: Make emptyDir work when SELinux is disabled
  (pmorie@gmail.com)
- UPSTREAM: 9384: EmptyDir volumes for non-root 2/2 (deads@redhat.com)
- UPSTREAM: 9844: Support emptyDir volumes for containers running as uid != 0
  (deads@redhat.com)
- UPSTREAM: kube: update describer for dockercfg secrets (deads@redhat.com)
- UPSTREAM: 9971: generated conversion updates (deads@redhat.com)
- UPSTREAM: patch to fix kubelet startup (deads@redhat.com)
- UPSTREAM: fix SCC printers (deads@redhat.com)
- UPSTREAM: Allow pod start to be delayed in Kubelet (ccoleman@redhat.com)
- UPSTREAM: 10636: Split kubelet server initialization for easier reuse
  (deads@redhat.com)
- UPSTREAM: 10635 Cloud provider should return an error (deads@redhat.com)
- UPSTREAM: 9870 Allow Recyclers to be configurable (deads@redhat.com)
- UPSTREAM: scc allocation interface methods (deads@redhat.com)
- UPSTREAM: 10062 support acceptance check in rolling updater
  (deads@redhat.com)
- UPSTREAM: implement a generic webhook storage (ccoleman@redhat.com)
- UPSTREAM: Ensure no namespace on create/update root scope types
  (jliggitt@redhat.com)
- UPSTREAM: 8607 service account groups (deads@redhat.com)
- UPSTREAM: kube: expose name validation method (deads@redhat.com)
- UPSTREAM: Make util.Empty public (ccoleman@redhat.com)
- UPSTREAM: 7893 scc (deads@redhat.com)
- UPSTREAM: 7893 scc design (deads@redhat.com)
- UPSTREAM: Add "Info" to go-restful ApiDecl (ccoleman@redhat.com)
- UPSTREAM: Handle missing resolv.conf (ccoleman@redhat.com)
- UPSTREAM: Disable systemd activation for DNS (ccoleman@redhat.com)
- bump(github.com/elazarl/go-bindata-
  assetfs):3dcc96556217539f50599357fb481ac0dc7439b9 (deads@redhat.com)
- bump(github.com/syndtr/gocapability/capability):8e4cdcb3c22b40d5e330ade0b68cb
  2e2a3cf6f98 (deads@redhat.com)
- bump(github.com/miekg/dns):c13058f493c3756207ced654dce2986e812f2bcf
  (deads@redhat.com)
- bump(github.com/spf13/pflag): 381cb823881391d5673cf2fc41e38feba8a8e49a
  (jliggitt@redhat.com)
- bump(github.com/spf13/cobra): a8f7f3dc25e03593330100563f6c392224221899
  (jliggitt@redhat.com)
- bump(github.com/GoogleCloudPlatform/kubernetes):96828f203c8d960bb7a5ad649d1f3
  8f77ae8910f (deads@redhat.com)
- Move origin/scripts to ose/scripts (sdodson@redhat.com)
- edit: Default to notepad for Windows and env renaming
  (kargakis@users.noreply.github.com)
- describe: Use spec.replicas when describing a deployment
  (kargakis@users.noreply.github.com)
- oc volume fixes (rpenta@redhat.com)
- Clean up to status output for ports and messages (ccoleman@redhat.com)
- Fix database service name copy&paste mistake (nagy.martin@gmail.com)
- Change our example templates to use ReadWriteOnce access modes
  (nagy.martin@gmail.com)
- Update readme to indicate docker 1.7 is broken (ccoleman@redhat.com)
- Restore failed initial deployment events (ironcladlou@gmail.com)
- Give cap_sys_net_bind to openshift binary (ccoleman@redhat.com)
- Support quay.io by allowing cookies on connect (ccoleman@redhat.com)
- further doc corrections/clarifications based on exercising *-ex; update
  .gitignore for .project; incorporate Ben's suggestions and Clayton's
  clarifications; general minor cleanup; fix typo (gmontero@redhat.com)
- Stop defaulting to Recreate deployment strategy (jliggitt@redhat.com)
- Add EXPOSE to our public Dockerfile (ccoleman@redhat.com)
- Refactored the use of restful.Container.Handle() method (skuznets@redhat.com)
- Stop creating deployments with recreate strategy (jliggitt@redhat.com)
- sample that uses direct docker pullspec for builder image
  (bparees@redhat.com)
- Don't produce events when initial deployment fails (ironcladlou@gmail.com)
- refactor graph veneers (deads@redhat.com)
- Added healthz endpoint to OpenShift (steve.kuznetsov@gmail.com)
- deploy: Remove extra newline when describing deployments
  (kargakis@users.noreply.github.com)
- deploy: Better message (kargakis@users.noreply.github.com)
- Making build logs error msgs more clear (j.hadvig@gmail.com)
- sample-app: Show real output from oadm registry
  (kargakis@users.noreply.github.com)
- Fix for https://github.com/openshift/origin/issues/3446 (sgoodwin@redhat.com)
- Look for deployer label when filtering pods on overview page
  (spadgett@redhat.com)
- Remove ellipses from links and buttons (spadgett@redhat.com)
- Correct registry auth for pruning (agoldste@redhat.com)
- Add image pruning e2e test (agoldste@redhat.com)
- Wrapped tile content on builds and pods pages into 2 column layout for better
  presentation by using available space Update UI screenshots for browse builds
  and pods pages (sgoodwin@redhat.com)
- allow http proxy env variables to be set in privileged sti container
  (bparees@redhat.com)
- update host name section (pweil@redhat.com)
- add graph testing helpers (deads@redhat.com)
- Fix the example command to list the projects (misc@redhat.com)
- MySQL/Wordpress on NFS PVs (mturansk@redhat.com)
- Automatic commit of package [openshift] release [3.0.0.1].
  (bleanhar@redhat.com)
- update prune error message to mention --confirm (chmouel@enovance.com)
- Add control/flow diagram for new-app (cewong@redhat.com)
- Remove duplicated template (rhcarvalho@gmail.com)
- Fix README.md markdown formatting (rhcarvalho@gmail.com)
- Make ose/scripts a symlink to origin/scripts (sdodson@redhat.com)
- fixed bash error (mturansk@redhat.com)
- fixed typo in script name (mturansk@redhat.com)
- fixed plugin init (mturansk@redhat.com)
- Copy recycler script to ose image (sdodson@redhat.com)
- Automatic commit of package [openshift] release [3.0.0.0].
  (sdodson@redhat.com)
- Ensure we're importing everything necessary for fallback codepaths too
  (sdodson@redhat.com)
- Add tooltips to values we elide in the Web Console (spadgett@redhat.com)

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

* Thu Aug 14 2014 Adam Miller <admiller@redhat.com> - 0-0.0.1.gitc3839b8
- First package
