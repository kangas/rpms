%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:          2010.1
Release:          1%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/nova
Source0:          http://launchpad.net/nova/austin/%{version}/+download/nova-%{version}.tar.gz
Source1:          %{name}-api.conf
Source2:          %{name}-api.init
Source3:          %{name}-compute.conf
Source4:          %{name}-compute.init
Source5:          %{name}-dhcpbridge.conf
Source6:          %{name}.logrotate
Source7:          %{name}-manage.conf
Source8:          %{name}-network.conf
Source9:          %{name}-network.init
Source10:         %{name}-objectstore.conf
Source11:         %{name}-objectstore.init
Source12:         %{name}-scheduler.conf
Source13:         %{name}-scheduler.init
Source14:         %{name}-volume.conf
Source15:         %{name}-volume.init
BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python-nova = %{version}-%{release}

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

%description
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

Nova is intended to be easy to extend, and adapt. For example, it currently
uses an LDAP server for users and groups, but also includes a fake LDAP server,
that stores data in Redis. It has extensive test coverage, and uses the Sphinx
toolkit (the same as Python itself) for code and user documentation.

%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         PyXML
Requires:         m2crypto
Requires:         python-IPy
Requires:         python-boto
Requires:         python-carrot
Requires:         python-daemon
Requires:         python-eventlet
Requires:         python-gflags
Requires:         python-mox
Requires:         python-redis
Requires:         python-routes
Requires:         python-sqlalchemy
Requires:         python-tornado
Requires:         python-twisted-core
Requires:         python-twisted-web
Requires:         python-webob
Requires:         python-webob

%description -n   python-nova
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Python library.

%package          api
Summary:          A nova api server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      api
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} api server.

%package          compute
Summary:          A nova compute server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      compute
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} compute server.

%package          instancemonitor
Summary:          A nova instancemonitor server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      instancemonitor
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} instance monitor.

%package          network
Summary:          A nova network server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      network
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} network server.

%package          objectstore
Summary:          A nova objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      objectstore
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} object store server.

%package          scheduler
Summary:          A nova scheduler server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      scheduler
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} scheduler server.

%package          volume
Summary:          A nova volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      volume
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} volume server.

%prep
%setup -q -n nova-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
cp -rp CA %{buildroot}%{_sharedstatedir}/nova

# Install init files
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE9} %{buildroot}%{_initrddir}/%{name}-network
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-objectstore
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-scheduler
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-volume

# Install logrotate
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install config files
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/nova/nova-api.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/nova/nova-compute.conf
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/nova/nova-dhcpbridge.conf
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/nova/nova-manage.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/nova/nova-network.conf
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/nova/nova-objectstore.conf
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/nova/nova-scheduler.conf
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/nova/nova-volume.conf

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.qemu.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.qemu.xml.template
install -p -D -m 644 nova/virt/libvirt.uml.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.uml.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template

# TODO debian/nova_sudoers

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/nova/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/nova/CA -name .placeholder -delete

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post api
/sbin/chkconfig --add nova-api

%preun api
if [ $1 = 0 ] ; then
    /sbin/service nova-api stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-api
fi

%post compute
/sbin/chkconfig --add nova-compute

%preun compute
if [ $1 = 0 ] ; then
    /sbin/service nova-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-compute
fi

%post network
/sbin/chkconfig --add nova-network

%preun network
if [ $1 = 0 ] ; then
    /sbin/service nova-network stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-network
fi

%post objectstore
/sbin/chkconfig --add nova-objectstore

%preun objectstore
if [ $1 = 0 ] ; then
    /sbin/service nova-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-objectstore
fi

%post scheduler
/sbin/chkconfig --add nova-scheduler

%preun scheduler
if [ $1 = 0 ] ; then
    /sbin/service nova-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-scheduler
fi

%post volume
/sbin/chkconfig --add nova-volume

%preun volume
if [ $1 = 0 ] ; then
    /sbin/service nova-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-volume
fi

%files
%defattr(-,root,root,-)
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/nova/nova-manage.conf
%dir %{_sysconfdir}/nova
%{_bindir}/nova-manage
%{_datarootdir}/nova
%{_localstatedir}/log/nova
%{_sharedstatedir}/nova

%files -n python-nova
%defattr(-,root,root,-)
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%files api
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-api.conf
%{_initrddir}/%{name}-api
%{_bindir}/nova-api

%files compute
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-compute.conf
%{_bindir}/nova-compute
%{_initrddir}/%{name}-compute

%files instancemonitor
%defattr(-,root,root,-)
%{_bindir}/nova-instancemonitor

%files network
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-network.conf
%config(noreplace) %{_sysconfdir}/nova/nova-dhcpbridge.conf
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{name}-network

%files objectstore
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-objectstore.conf
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{name}-objectstore

%files scheduler
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-scheduler.conf
%{_bindir}/nova-scheduler
%{_initrddir}/%{name}-scheduler

%files volume
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-volume.conf
%{_bindir}/nova-volume
%{_initrddir}/%{name}-volume

%changelog
* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 2010.1-1
- Initial build
