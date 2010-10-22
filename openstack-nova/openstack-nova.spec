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
BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools

%description
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

Nova is intended to be easy to extend, and adapt. For example, it currently
uses an LDAP server for users and groups, but also includes a fake LDAP server,
that stores data in Redis. It has extensive test coverage, and uses the Sphinx
toolkit (the same as Python itself) for code and user documentation.

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

%package          tests
Summary:          A nova test suite
Group:            Development/Languages

Requires:         %{name} = %{version}-%{release}

%description      tests
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} test suite.

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

# Setup configuration files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.qemu.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.qemu.xml.template
install -p -D -m 644 nova/virt/libvirt.uml.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.uml.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template

# TODO debian/nova_sudoers

# Clean CA directory
find %{_sharedstatedir}/swift/CA -name .gitignore -or -name .placeholder -delete

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%files
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info
%{python_sitelib}/nova/*.py*
%{_bindir}/nova-manage
%{_sysconfdir}/swift
# %{_sysconfdir}/nova/nova-manage.conf

## TODO: confirm location
%{python_sitelib}/nova/auth
%{python_sitelib}/nova/cloudpipe
%{python_sitelib}/nova/db
%{python_sitelib}/nova/image
%{python_sitelib}/nova/virt
## TODO: confirm location

# Common directories
%{_sysconfdir}/nova
%{_sharedstatedir}/nova
%{_sharedstatedir}/nova/images
%{_sharedstatedir}/nova/instances
%{_sharedstatedir}/nova/keys
%{_sharedstatedir}/nova/networks
%{_sharedstatedir}/nova/tmp
%{_localstatedir}/log/nova

%files api
%defattr(-,root,root,-)
%{python_sitelib}/nova/api
%{_bindir}/nova-api

%files compute
%defattr(-,root,root,-)
%{python_sitelib}/nova/compute
%{_bindir}/nova-compute
# %{_sysconfdir}/nova/nova-compute.conf

%files instancemonitor
%defattr(-,root,root,-)
%{_bindir}/nova-instancemonitor

%files network
%defattr(-,root,root,-)
%{python_sitelib}/nova/network
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
# %{_sysconfdir}/nova/nova-network.conf
# %{_sysconfdir}/nova/nova-dhcpbridge.conf

%files objectstore
%defattr(-,root,root,-)
%{python_sitelib}/nova/objectstore
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
# %{_sysconfdir}/nova/nova-objectstore.conf

%files tests
%{python_sitelib}/nova/tests

%files scheduler
%defattr(-,root,root,-)
%{python_sitelib}/nova/scheduler
%{_bindir}/nova-scheduler
# %{_sysconfdir}/nova/nova-scheduler.conf

%files volume
%defattr(-,root,root,-)
%{python_sitelib}/nova/volume
%{_bindir}/nova-volume
# %{_sysconfdir}/nova/nova-volume.conf

%changelog
* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 2010.1-1
- Initial build
