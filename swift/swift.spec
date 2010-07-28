%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             swift
Version:          1.0.2
Release:          2%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz
Source1:          swift-functions
Source2:          swift-account.init
Source3:          swift-auth.init
Source4:          swift-container.init
Source5:          swift-object.init
Source6:          swift-proxy.init
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
# Init helper functions
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/functions
# Init scripts
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-account
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-auth
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-container
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-object
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/%{name}-proxy
# Install man stubs
for name in $( ls ./man ); do
    mkdir -p "%{buildroot}%{_mandir}/$name"
    cp "./man/$name/"*.gz "%{buildroot}%{_mandir}/$name"
done
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/auth-server
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/container-server
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/object-server
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/proxy-server
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}/account-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}/auth-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}/container-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}/object-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}/proxy-server

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
%dir %{_datarootdir}/%{name}/functions
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{python_sitelib}/%{name}
%{_bindir}/st
%{_bindir}/%{name}-account-audit
%{_bindir}/%{name}-drive-audit
%{_bindir}/%{name}-get-nodes
%{_bindir}/%{name}-init
%{_bindir}/%{name}-ring-builder
%{_bindir}/%{name}-stats-populate
%{_bindir}/%{name}-stats-report
%{_mandir}/man8/st.8.gz
%{_mandir}/man8/%{name}-account-audit.8.gz
%{_mandir}/man8/%{name}-drive-audit.8.gz
%{_mandir}/man8/%{name}-get-nodes.8.gz
%{_mandir}/man8/%{name}-init.8.gz
%{_mandir}/man8/%{name}-ring-builder.8.gz
%{_mandir}/man8/%{name}-stats-populate.8.gz
%{_mandir}/man8/%{name}-stats-report.8.gz
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/common
%{python_sitelib}/%{name}-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_initrddir}/%{name}-account
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}/account-server
%dir %{_sysconfdir}/%{name}/account-server
%{_bindir}/%{name}-account-auditor
%{_bindir}/%{name}-account-reaper
%{_bindir}/%{name}-account-replicator
%{_bindir}/%{name}-account-server
%{_mandir}/man8/%{name}-account-auditor.8.gz
%{_mandir}/man8/%{name}-account-reaper.8.gz
%{_mandir}/man8/%{name}-account-replicator.8.gz
%{_mandir}/man8/%{name}-account-server.8.gz
%{python_sitelib}/%{name}/account

%files auth
%defattr(-,root,root,-)
%doc etc/auth-server.conf-sample
%dir %{_initrddir}/%{name}-auth
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}/auth-server
%dir %{_sysconfdir}/%{name}/auth-server
%{_bindir}/%{name}-auth-create-account
%{_bindir}/%{name}-auth-recreate-accounts
%{_bindir}/%{name}-auth-server
%{_mandir}/man8/%{name}-auth-create-account.8.gz
%{_mandir}/man8/%{name}-auth-recreate-accounts.8.gz
%{_mandir}/man8/%{name}-auth-server.8.gz
%{python_sitelib}/%{name}/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_initrddir}/%{name}-container
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}/container-server
%dir %{_sysconfdir}/%{name}/container-server
%{_bindir}/%{name}-container-auditor
%{_bindir}/%{name}-container-server
%{_bindir}/%{name}-container-replicator
%{_bindir}/%{name}-container-updater
%{_mandir}/man8/%{name}-container-auditor.8.gz
%{_mandir}/man8/%{name}-container-server.8.gz
%{_mandir}/man8/%{name}-container-replicator.8.gz
%{_mandir}/man8/%{name}-container-updater.8.gz
%{python_sitelib}/%{name}/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%dir %{_initrddir}/%{name}-object
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}/object-server
%dir %{_sysconfdir}/%{name}/object-server
%{_bindir}/%{name}-object-auditor
%{_bindir}/%{name}-object-info
%{_bindir}/%{name}-object-replicator
%{_bindir}/%{name}-object-server
%{_bindir}/%{name}-object-updater
%{_mandir}/man8/%{name}-object-auditor.8.gz
%{_mandir}/man8/%{name}-object-info.8.gz
%{_mandir}/man8/%{name}-object-replicator.8.gz
%{_mandir}/man8/%{name}-object-server.8.gz
%{_mandir}/man8/%{name}-object-updater.8.gz
%{python_sitelib}/%{name}/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%dir %{_initrddir}/%{name}-proxy
%dir %attr(0755, swift, root) %{_localstatedir}/run/%{name}/proxy-server
%dir %{_sysconfdir}/%{name}/proxy-server
%{_bindir}/%{name}-proxy-server
%{_mandir}/man8/%{name}-proxy-server.8.gz
%{python_sitelib}/%{name}/proxy

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Tue Jul 27 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-2
- Add swift user
- Update init scripts

* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
