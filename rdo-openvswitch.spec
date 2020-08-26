# Current version of OVS that this package requires
%define ovs_version 2.13

# Comma-separated (no spaces) e.g. 2.10,2.9 ... of prior fast-datapath
# openvswitch and ovn packages we need to obsolete
%define obsolete_ovs_versions 2.10,2.11,2.12

# Same as above, but enable ovs/ovn to be separate
%define ovn_version 2.13
%define obsolete_ovn_versions 2.10,2.11,2.12

%if 0%{?rhel} > 7
%define pyprefix python3
%else
%define pyprefix python
%endif

# Lua macro to create a bunch of Obsoletes by splitting up the above
# definition and substituting where there's an asterisk
%{lua:
function rhosp_obsoletes(package, ver, obsoletes)
  local s
  local pkg
  pkg = string.gsub(package, "*", "")
  print("Obsoletes: "..pkg.." < "..ver.."\n")
  for s in string.gmatch(obsoletes, "[^,]+") do
    pkg = string.gsub(package, "*", s)
    print("Obsoletes: "..pkg.." < "..ver.."\n")
  end
end

function ovs_obsoletes(package)
  rhosp_obsoletes(package, rpm.expand("%ovs_version"), rpm.expand("%obsolete_ovs_versions"))
end

function ovn_obsoletes(package)
  rhosp_obsoletes(package, rpm.expand("%ovn_version"), rpm.expand("%obsolete_ovn_versions"))
end}

######## OPENVSWITCH PACKAGING ########

Name:           rhosp-openvswitch
Version:        %{ovs_version}
Release:        8%{?dist}
Summary:        Wrapper rpm to allow installing OVS with new versioning schemes

Group:          System Environment/Daemons
License:        Public domain
URL:            http://www.openvswitch.org
BuildArch:      noarch

Requires:       openvswitch%{ovs_version}
%if 0%{?rhel} == 8
# RHEL8 still has network-scripts, but they are deprecated;
# RHEL>8 is unlikely to have them.
Requires:       network-scripts-openvswitch%{ovs_version}
%endif
Provides:       openvswitch = %{ovs_version}
%{lua:ovs_obsoletes("openvswitch*")}

%description
Wrapper rpm for the base openvswitch package

%package -n %{pyprefix}-rhosp-openvswitch
Summary:    wrapper for python-openvswitch rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   %{pyprefix}-openvswitch%{ovs_version}
Provides:   %{pyprefix}-openvswitch = %{ovs_version}
%if 0%{?rhel} > 7
%{lua:ovs_obsoletes("python3-openvswitch*")}
# Just in case / being pedantic ...
%{lua:ovs_obsoletes("python2-openvswitch*")}
%endif
# RHEL7 builds didn't have python2-openvswitch
%{lua:ovs_obsoletes("python-openvswitch*")}

%description -n %{pyprefix}-rhosp-openvswitch
Wrapper rpm for the base %{pyprefix}-openvswitch package

%package devel
Summary:    wrapper for openvswitch-devel rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovs_version}-devel
Provides:   openvswitch-devel = %{ovs_version}
%{lua:ovs_obsoletes("openvswitch*-devel")}

%description devel
Wrapper rpm for the base openvswitch-devel package

%package test
Summary:    wrapper for openvswitch-test rpm
License:    Public domain
Requires:   %{pyprefix}-rhosp-openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovs_version}-test
Provides:   openvswitch-test = %{ovs_version}
%{lua:ovs_obsoletes("openvswitch*-test")}

%description test
Wrapper rpm for the base openvswitch-test package

######## OVN PACKAGING ########

%package -n rhosp-ovn
Version:    %{ovn_version}
Summary:    wrapper for ovn rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}
Provides:   ovn = %{ovn_version}
Provides:   openvswitch-ovn-common = %{ovn_version}
Provides:   %{name}-ovn-common = %{version}
Obsoletes:  %{name}-ovn-common < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   rhosp-ovn-common = %{version}
Obsoletes:  rhosp-ovn-common < %{?epoch:%{epoch}:}%{version}-%{release}
# OVN packaging should do this, but doesn't?
# Obsoletes: openvswitch-ovn-common < ...
%{lua:ovn_obsoletes("ovn*")}

%description -n rhosp-ovn
Wrapper rpm for the base ovn package

%package -n rhosp-ovn-central
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-central rpm
License:    Public domain
Requires:   rhosp-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}-central
Provides:   openvswitch-ovn-central = %{ovn_version}
Obsoletes:  openvswitch-ovn-central < %{ovn_version}
Provides:   ovn-central = %{ovn_version}
Obsoletes:  ovn-central < %{ovn_version}
Provides:   %{name}-ovn-central = %{ovn_version}
Obsoletes:  %{name}-ovn-central < %{?epoch:%{epoch}:}%{version}-%{release}
%{lua:ovn_obsoletes("openvswitch*-ovn-central")}
%{lua:ovn_obsoletes("ovn*-central")}

%description -n rhosp-ovn-central
Wrapper rpm for the base openvswitch-ovn-central package

%package -n rhosp-ovn-host
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-host rpm
License:    Public domain
Requires:   rhosp-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovn_version}-ovn-host
Provides:   openvswitch-ovn-host = %{ovn_version}
Obsoletes:  openvswitch-ovn-host < %{ovn_version}
Provides:   ovn-host = %{ovn_version}
Obsoletes:  ovn-host < %{ovn_version}
Provides:   %{name}-ovn-host = %{ovn_version}
Obsoletes:  %{name}-ovn-host < %{?epoch:%{epoch}:}%{version}-%{release}
%{lua:ovn_obsoletes("openvswitch*-ovn-host")}
%{lua:ovn_obsoletes("ovn*-host")}

%description -n rhosp-ovn-host
Wrapper rpm for the base openvswitch-ovn-host package

%package -n rhosp-ovn-vtep
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-vtep rpm
License:    Public domain
Requires:   rhosp-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}-vtep
Provides:   openvswitch-ovn-vtep = %{ovn_version}
Obsoletes:  openvswitch-ovn-vtep < %{ovn_version}
Provides:   ovn-vtep = %{ovn_version}
Obsoletes:  ovn-vtep < %{ovn_version}
Provides:   %{name}-ovn-vtep = %{ovn_version}
Obsoletes:  %{name}-ovn-vtep < %{?epoch:%{epoch}:}%{version}-%{release}
%{lua:ovn_obsoletes("openvswitch*-ovn-vtep")}
%{lua:ovn_obsoletes("ovn*-vtep")}

%description -n rhosp-ovn-vtep
Wrapper rpm for the base ovn-vtep package

%setup -q

%build

%files
%files -n %{pyprefix}-rhosp-openvswitch
%files devel
%files test
%files -n rhosp-ovn
%files -n rhosp-ovn-central
%files -n rhosp-ovn-host
%files -n rhosp-ovn-vtep

%changelog
* Mon Apr 20 2020 Lon Hohberger <lon@redhat.com> 2.13-8
- Allow OVS and OVN versions to diverge
- Fix requirements / obsoletes / provides preventing certain upgrades from 2.11-0.6

* Thu Mar 19 2020 Lon Hohberger <lon@redhat.com> 2.13-3
- Fix OVN wrappers

* Wed Mar 18 2020 Lon Hohberger <lon@redhat.com> 2.13-2
- Mirror openvswitch2.13 internal dependencies in wrappers

* Mon Mar 16 2020 Thierry Vignaud <tvignaud@redhat.com> 2.13-1
- rebase to OVS 2.13

* Tue Jul 30 2019 Lon Hohberger <lon@redhat.com> - 2.11-0.6
- Use Obsoletes: lua macro so we can add/remove versions to Obsoletes
  without rewriting the spec file each time

* Tue Jun 11 2019 Thierry Vignaud <tvignaud@redhat.com> 2.11-0.1.fc29
- Update for OVS 2.11

* Wed Jul 11 2018 Mike Burns <mburns@redhat.com> - 2.10-0.1
- initial spec for RHOSP openvswitch wrapper RPMs
