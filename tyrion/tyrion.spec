Name:             tyrion
Version:          0.0.1
Release:          1%{?dist}
Summary:          A systems automation framework
Group:            Applications/System
License:          BSD
URL:              http://www.tyrion.org
Source0:          http://github.com/downloads/tidg/tyrion/%{name}-%{version}.tar.gz
Source1:          tyrion.logrotate
Source2:          tyrion-node.init
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    txmpp-devel
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
Summary:          Run-time library files for %{name}
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
scons %{?_smp_mflags} --flags="%{optflags}" --install \
  --bindir=%{buildroot}/%{_bindir} \
  --libdir=%{buildroot}/%{_libdir} \
  --sbindir=%{buildroot}/%{_sbindir}
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}
%{__cp} -rp service %{buildroot}%{_sharedstatedir}/%{name}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-node
install -p -D -m 600 config/acl.conf %{buildroot}%{_sysconfdir}/%{name}/acl.conf
install -p -D -m 600 config/node.conf %{buildroot}%{_sysconfdir}/%{name}/node.conf

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
%doc AUTHORS LICENSE NOTICE README.md config/client.conf
%{_bindir}/tyrion

%files libs
%defattr(-,root,root,-)
%doc README.md
%{_libdir}/libtyrion.so

%files node
%defattr(-,root,root,-)
%doc README.md config/acl.conf config/node.conf
%config(noreplace) %{_sysconfdir}/%{name}/acl.conf
%config(noreplace) %{_sysconfdir}/%{name}/node.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_localstatedir}/log/%{name}
%{_initrddir}/%{name}-node
%{_sbindir}/tyrion-node
%{_localstatedir}/lib/%{name}

%changelog
* Wed Jun 02 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
