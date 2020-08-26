# Current version of OVS that this package requires
%define ovs_version 2.13

# Comma-separated (no spaces) e.g. 2.10,2.9 ... of prior fast-datapath
# openvswitch and ovn packages we need to obsolete
%define obsolete_ovs_versions 2.10,2.11,2.12

# Same as above, but enable ovs/ovn to be separate
%define ovn_version 2.13
%define obsolete_ovn_versions 2.10,2.11,2.12

# Lua macro to create a bunch of Obsoletes by splitting up the above
# definition and substituting where there's an asterisk
%{lua:
function rdo_obsoletes(package, ver, obsoletes)
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
  rdo_obsoletes(package, rpm.expand("%ovs_version"), rpm.expand("%obsolete_ovs_versions"))
end

function ovn_obsoletes(package)
  rdo_obsoletes(package, rpm.expand("%ovn_version"), rpm.expand("%obsolete_ovn_versions"))
end}

######## OPENVSWITCH PACKAGING ########

Name:           rdo-openvswitch
Epoch:          1
Version:        %{ovs_version}
Release:        0.2%{?dist}
Summary:        Wrapper rpm to allow installing OVS with new versioning schemes

Group:          System Environment/Daemons
License:        Public domain
URL:            http://www.openvswitch.org
BuildArch:      noarch

Requires:       openvswitch%{ovs_version}
Requires:       network-scripts-openvswitch%{ovs_version}
#Provides:       openvswitch = %{?epoch:%{epoch}:}%{ovs_version}
#Provides:       rhosp-openvswitch = %{?epoch:%{epoch}:}%{ovs_version}
Provides:       openvswitch = 1:%{ovs_version}
Provides:       rdo-openvswitch = 1:%{ovs_version}
Provides:       rhosp-openvswitch = 1:%{ovs_version}
%{lua:ovs_obsoletes("openvswitch*")}

%description
Wrapper rpm for the base openvswitch package

%package -n python3-rdo-openvswitch
Summary:    wrapper for python-openvswitch rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   python3-openvswitch%{ovs_version}
Provides:   python3-openvswitch = %{?epoch:%{epoch}:}%{ovs_version}
%{lua:ovs_obsoletes("python3-openvswitch*")}
%{lua:ovs_obsoletes("python2-openvswitch*")}
%{lua:ovs_obsoletes("python-openvswitch*")}

%description -n python3-rdo-openvswitch
Wrapper rpm for the base python3-openvswitch package

%package devel
Summary:    wrapper for openvswitch-devel rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovs_version}-devel
Provides:   openvswitch-devel = %{?epoch:%{epoch}:}%{ovs_version}
%{lua:ovs_obsoletes("openvswitch*-devel")}

%description devel
Wrapper rpm for the base openvswitch-devel package

%package test
Summary:    wrapper for openvswitch-test rpm
License:    Public domain
Requires:   python3-rdo-openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovs_version}-test
Provides:   openvswitch-test = %{?epoch:%{epoch}:}%{ovs_version}
%{lua:ovs_obsoletes("openvswitch*-test")}

%description test
Wrapper rpm for the base openvswitch-test package

######## OVN PACKAGING ########

%package -n rdo-ovn
Version:    %{ovn_version}
Summary:    wrapper for ovn rpm
License:    Public domain
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}
Provides:   ovn = %{?epoch:%{epoch}:}%{ovn_version}
Provides:   openvswitch-ovn-common = %{?epoch:%{epoch}:}%{ovn_version}
Provides:   %{name}-ovn-common = %{?epoch:%{epoch}:}%{version}
Obsoletes:  %{name}-ovn-common < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:   rdo-ovn-common = %{?epoch:%{epoch}:}%{version}
Obsoletes:  rdo-ovn-common < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  ovn < %{?epoch:%{epoch}:}%{version}-%{release}
# OVN packaging should do this, but doesn't?
# Obsoletes: openvswitch-ovn-common < ...
%{lua:ovn_obsoletes("ovn*")}

%description -n rdo-ovn
Wrapper rpm for the base ovn package

%package -n rdo-ovn-central
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-central rpm
License:    Public domain
Requires:   rdo-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}-central
Provides:   openvswitch-ovn-central = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  openvswitch-ovn-central < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   ovn-central = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  ovn-central < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   %{name}-ovn-central = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  %{name}-ovn-central < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  ovn-central < %{?epoch:%{epoch}:}%{version}-%{release}
# OVN packaging should do this, but doesn't?
%{lua:ovn_obsoletes("openvswitch*-ovn-central")}
%{lua:ovn_obsoletes("ovn*-central")}

%description -n rdo-ovn-central
Wrapper rpm for the base openvswitch-ovn-central package

%package -n rdo-ovn-host
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-host rpm
License:    Public domain
Requires:   rdo-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   openvswitch%{ovn_version}-ovn-host
Provides:   openvswitch-ovn-host = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  openvswitch-ovn-host < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   ovn-host = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  ovn-host < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   %{name}-ovn-host = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  %{name}-ovn-host < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  ovn-host < %{?epoch:%{epoch}:}%{version}-%{release}
%{lua:ovn_obsoletes("openvswitch*-ovn-host")}
%{lua:ovn_obsoletes("ovn*-host")}

%description -n rdo-ovn-host
Wrapper rpm for the base openvswitch-ovn-host package

%package -n rdo-ovn-vtep
Version:    %{ovn_version}
Summary:    wrapper for openvswitch-ovn-vtep rpm
License:    Public domain
Requires:   rdo-ovn = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   ovn%{ovn_version}-vtep
Provides:   openvswitch-ovn-vtep = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  openvswitch-ovn-vtep < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   ovn-vtep = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  ovn-vtep < %{?epoch:%{epoch}:}%{ovn_version}
Provides:   %{name}-ovn-vtep = %{?epoch:%{epoch}:}%{ovn_version}
Obsoletes:  %{name}-ovn-vtep < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:  ovn-vtep < %{?epoch:%{epoch}:}%{version}-%{release}
%{lua:ovn_obsoletes("openvswitch*-ovn-vtep")}
%{lua:ovn_obsoletes("ovn*-vtep")}

%description -n rdo-ovn-vtep
Wrapper rpm for the base ovn-vtep package

%setup -q

%build

%files -n rdo-openvswitch
%files -n python3-rdo-openvswitch
%files devel
%files test
%files -n rdo-ovn
%files -n rdo-ovn-central
%files -n rdo-ovn-host
%files -n rdo-ovn-vtep

%changelog
* Thu Aug 13 2020 Yatin Karel <ykarel@redhat.com> - 2.13-0.2
- RDO Wrapper

