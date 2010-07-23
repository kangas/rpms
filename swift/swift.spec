%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           swift
Version:        1.0.2
Release:        1%{?dist}
Summary:        OpenStack Object Storage (swift)

Group:          Development/Languages
License:        ASL 2.0
URL:            http://launchpad.net/swift
Source0:        http://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       python(abi) >= 2.6
Requires:       python-configobj
Requires:       python-eventlet >= 0.9.8
Requires:       python-greenlet >= 0.3.1
Requires:       python-simplejson
Requires:       python-webob
Requires:       pyxattr

%description
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.

%package        account
Summary:        A swift account server
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package        auth
Summary:        A swift auth server
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    auth
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} auth server.

%package        container
Summary:        A swift container server
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package        object
Summary:        A swift object server
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package        proxy
Summary:        A swift proxy server
Group:          Applications/System

Requires:       %{name} = %{version}-%{release}

%description    proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation

BuildRequires:  python-sphinx
# Required for genereating docs
BuildRequires:  python-eventlet
BuildRequires:  python-simplejson
BuildRequires:  python-webob
BuildRequires:  pyxattr

%description doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for the %{name}.

%prep
%setup -q
# Fix wrong-file-end-of-line-encoding warning
sed -i 's/\r//' LICENSE

%build
%{__python} setup.py build
# Build docs
pushd doc; make html; popd
# Fix hidden-file-or-dir warning 
rm doc/build/html/.buildinfo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%dir %{python_sitelib}/%{name}
%{_bindir}/st
%{_bindir}/swift-account-audit
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/common
%{python_sitelib}/%{name}-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{python_sitelib}/%{name}/account

%files auth
%defattr(-,root,root,-)
%doc etc/auth-server.conf-sample
%{_bindir}/swift-auth-create-account
%{_bindir}/swift-auth-recreate-accounts
%{_bindir}/swift-auth-server
%{python_sitelib}/%{name}/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-updater
%{python_sitelib}/%{name}/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%{_bindir}/swift-object-server
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-updater
%{_bindir}/swift-object-info
%{python_sitelib}/%{name}/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%{_bindir}/swift-proxy-server
%{python_sitelib}/%{name}/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
