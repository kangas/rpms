Name:             tyrion
Version:          0.0.1
Release:          1%{?dist}
Summary:          A systems automation framework
Group:            Applications/System
License:          GPLv2
URL:              http://www.tyrion.org
Source0:          %{name}-%{version}.tar.gz
Source1:          tyrion.logrotate
Source2:          tyrion-node.init
Source3:          tyrion-node.acl.conf
Source4:          tyrion-node.node.conf
Source5:          tyrion-node-wrapper
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    gloox-devel
BuildRequires:    scons

Requires:         %{name}-libs = %{version}-%{release}

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig

%description
Tyrion is a systems automation framework.

This package contains the client application for interacting with a Tyrion
node.

%package          libs
Summary:          Runtime library files for %{name}
Group:            System Environment/Libraries

%description      libs
Tyrion is a systems automation framework.

The %{name}-libs package contains libraries for running %{name} applications.

%package          node
Summary:          The Tyrion node daemon
Group:            Applications/System

Requires:         %{name}-libs = %{version}-%{release}

%description      node
Tyrion is a systems automation framework.

The %{name}-node package contains the daemon for running a Tyrion node.

%prep
%setup -q

%build
scons %{?_smp_mflags} --flags="%{optflags}"

%install
rm -rf %{buildroot}
scons %{?_smp_mflags} --flags="%{optflags}" install \
  --prefix=%{buildroot} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --sbindir=%{_sbindir}
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}
%{__cp} -rp service %{buildroot}%{_sharedstatedir}/%{name}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-node
install -p -D -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/acl.conf
install -p -D -m 600 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/node.conf
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_sbindir}/tyrion-node-wrapper

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post node
/sbin/chkconfig --add %{name}-node

%preun node
if [ $1 = 0 ] ; then
    /sbin/service %{name}-node stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-node
fi

%postun node
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-node condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md client.conf.sample
%{_bindir}/tyrion

%files libs
%defattr(-,root,root,-)
%doc README.md
%{_libdir}/*.so

%files node
%defattr(-,root,root,-)
%doc README.md acl.conf.sample node.conf.sample
%config(noreplace) %{_sysconfdir}/%{name}/acl.conf
%config(noreplace) %{_sysconfdir}/%{name}/node.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_localstatedir}/log/%{name}
%{_initrddir}/%{name}-node
%{_sbindir}/tyrion-node
%{_sbindir}/tyrion-node-wrapper
%{_localstatedir}/lib/%{name}

%changelog
* Wed Jun 02 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
