%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             swift
Version:          1.0.2
Release:          1%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz
Source1:          swift-account.init
Source2:          swift-auth.init
Source3:          swift-container.init
Source4:          swift-object.init
Source5:          swift-proxy.init
Source20:         swift-create-man-stubs.py
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python(abi) >= 2.6
Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-simplejson
Requires:         python-webob
Requires:         pyxattr

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

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

%package          account
Summary:          A swift account server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package          auth
Summary:          A swift auth server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      auth
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} auth server.

%package          container
Summary:          A swift container server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package          object
Summary:          A swift object server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package          proxy
Summary:          A swift proxy server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%package doc
Summary:          Documentation for %{name}
Group:            Documentation

BuildRequires:    python-sphinx
# Required for genereating docs
BuildRequires:    python-eventlet
BuildRequires:    python-simplejson
BuildRequires:    python-webob
BuildRequires:    pyxattr

%description      doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}.

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
# Build man stubs
%{__python} %{SOURCE20} --mandir=./man

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Init scripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-account
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-auth
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-container
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-object
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-proxy
# Install man stubs
for name in $( ls ./man ); do
  mkdir -p "%{buildroot}%{_mandir}/$name"
  cp "./man/$name/"*.gz "%{buildroot}%{_mandir}/$name"
done
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
mkdir -p %{buildroot}/%{_localstatedir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/account-server
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/auth-server
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/container-server
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/object-server
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/proxy-server

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c "Swift Daemons" %{name}
exit 0

%post account
/sbin/chkconfig --add %{name}-account

%preun account
if [ $1 = 0 ] ; then
    /sbin/service %{name}-account stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-account
fi

%postun account
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-account condrestart >/dev/null 2>&1 || :
fi

%post auth
/sbin/chkconfig --add %{name}-auth

%preun auth
if [ $1 = 0 ] ; then
    /sbin/service %{name}-auth stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-auth
fi

%postun auth
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-auth condrestart >/dev/null 2>&1 || :
fi

%post container
/sbin/chkconfig --add %{name}-container

%preun container
if [ $1 = 0 ] ; then
    /sbin/service %{name}-container stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-container
fi

%postun container
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-container condrestart >/dev/null 2>&1 || :
fi

%post object
/sbin/chkconfig --add %{name}-object

%preun object
if [ $1 = 0 ] ; then
    /sbin/service %{name}-object stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-object
fi

%postun object
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-object condrestart >/dev/null 2>&1 || :
fi

%post proxy
/sbin/chkconfig --add %{name}-proxy

%preun proxy
if [ $1 = 0 ] ; then
    /sbin/service %{name}-proxy stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-proxy
fi

%postun proxy
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-proxy condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%dir %{_sysconfdir}/%{name}
%dir %{python_sitelib}/%{name}
%{_bindir}/st
%{_bindir}/swift-account-audit
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
%{_mandir}/man8/st.8.gz
%{_mandir}/man8/swift-account-audit.8.gz
%{_mandir}/man8/swift-drive-audit.8.gz
%{_mandir}/man8/swift-get-nodes.8.gz
%{_mandir}/man8/swift-init.8.gz
%{_mandir}/man8/swift-ring-builder.8.gz
%{_mandir}/man8/swift-stats-populate.8.gz
%{_mandir}/man8/swift-stats-report.8.gz
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/common
%{python_sitelib}/%{name}-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_sysconfdir}/%{name}/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{_initrddir}/%{name}-account
%{_mandir}/man8/swift-account-auditor.8.gz
%{_mandir}/man8/swift-account-reaper.8.gz
%{_mandir}/man8/swift-account-replicator.8.gz
%{_mandir}/man8/swift-account-server.8.gz
%{python_sitelib}/%{name}/account

%files auth
%defattr(-,root,root,-)
%doc etc/auth-server.conf-sample
%dir %{_sysconfdir}/%{name}/auth-server
%{_bindir}/swift-auth-create-account
%{_bindir}/swift-auth-recreate-accounts
%{_bindir}/swift-auth-server
%{_initrddir}/%{name}-auth
%{_mandir}/man8/swift-auth-create-account.8.gz
%{_mandir}/man8/swift-auth-recreate-accounts.8.gz
%{_mandir}/man8/swift-auth-server.8.gz
%{python_sitelib}/%{name}/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_sysconfdir}/%{name}/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_initrddir}/%{name}-container
%{_mandir}/man8/swift-container-auditor.8.gz
%{_mandir}/man8/swift-container-server.8.gz
%{_mandir}/man8/swift-container-replicator.8.gz
%{_mandir}/man8/swift-container-updater.8.gz
%{python_sitelib}/%{name}/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%dir %{_sysconfdir}/%{name}/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{_initrddir}/%{name}-object
%{_mandir}/man8/swift-object-auditor.8.gz
%{_mandir}/man8/swift-object-info.8.gz
%{_mandir}/man8/swift-object-replicator.8.gz
%{_mandir}/man8/swift-object-server.8.gz
%{_mandir}/man8/swift-object-updater.8.gz
%{python_sitelib}/%{name}/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%dir %{_sysconfdir}/%{name}/proxy-server
%{_bindir}/swift-proxy-server
%{_initrddir}/%{name}-proxy
%{_mandir}/man8/swift-proxy-server.8.gz
%{python_sitelib}/%{name}/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
