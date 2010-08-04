Name:             tyrion
Version:          0.0.1
Release:          1%{?dist}
Summary:          A framework for systems automation
Group:            Applications/System
License:          BSD
URL:              http://www.tidg.org/tyrion
Source0:          http://github.com/downloads/tidg/tyrion/tyrion-%{version}.tar.bz2
Source1:          tyrion-node.logrotate
Source2:          tyrion-node.init
Source3:          tyrion-node.acl
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    txmpp-devel
BuildRequires:    scons

Requires:         %{name}-libs = %{version}-%{release}

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig

%description
Tyrion is a framework for systems automation.

This package contains the client application for interacting with a Tyrion
node.

%package          libs
Summary:          Run-time library files for %{name}
Group:            System Environment/Libraries

%description      libs
Tyrion is a framework for systems automation.

The %{name}-libs package contains libraries for running %{name} applications.

%package          node
Summary:          A Tyrion node daemon
Group:            Applications/System

Requires:         %{name}-libs = %{version}-%{release}

%description      node
Tyrion is a framework for systems automation.

The %{name}-node package contains the daemon for running a Tyrion node.

%package          node-service-python
Summary:          A Tyrion node Python service
Group:            Applications/System

Requires:         %{name}-node = %{version}-%{release}
Requires:         python

%description      node-service-python
Tyrion is a framework for systems automation.

The %{name}-node-service-python package contains the node Python service.

%package          node-service-ruby
Summary:          A Tyrion node Ruby service
Group:            Applications/System

Requires:         %{name}-node = %{version}-%{release}
Requires:         ruby

%description      node-service-ruby
Tyrion is a framework for systems automation.

The %{name}-node-service-ruby package contains the node Ruby service.

%prep
%setup -q

%build
scons %{?_smp_mflags} --flags="%{optflags}"
# Build man pages
pushd doc; gzip *; popd

%install
rm -rf %{buildroot}
scons %{?_smp_mflags} --flags="%{optflags}" --install \
  --bindir=%{buildroot}/%{_bindir} \
  --libdir=%{buildroot}/%{_libdir} \
  --sbindir=%{buildroot}/%{_sbindir}
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}-node
%{__mkdir} -p %{buildroot}%{_datarootdir}/%{name}
%{__cp} -rp service %{buildroot}%{_datarootdir}/%{name}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-node
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-node
install -p -D -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/acl.conf
install -p -D -m 600 config/node.conf %{buildroot}%{_sysconfdir}/%{name}/node.conf
install -p -D -m 644 doc/tyrion.1.gz %{buildroot}%{_mandir}/man1/tyrion.1.gz
install -p -D -m 644 doc/tyrion-node.8.gz %{buildroot}%{_mandir}/man8/tyrion-node.8.gz

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
%doc config/client.conf
%{_bindir}/tyrion
%{_mandir}/man1/tyrion.1.gz

%files libs
%defattr(-,root,root,-)
%doc CONTRIBUTORS LICENSE NOTICE README.md
%{_libdir}/libtyrion.so.*

%files node
%defattr(-,root,root,-)
%doc config/acl.conf config/node.conf
%config(noreplace) %{_sysconfdir}/%{name}/acl.conf
%config(noreplace) %{_sysconfdir}/%{name}/node.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-node
%dir %{_localstatedir}/log/%{name}-node
%dir %{_datarootdir}/%{name}
%{_datarootdir}/%{name}/service/org.tyrion.service.bash
%{_initrddir}/%{name}-node
%{_mandir}/man8/tyrion-node.8.gz
%{_sbindir}/tyrion-node

%files node-service-python
%defattr(-,root,root,-)
%doc README.md
%{_datarootdir}/%{name}/service/org.tyrion.service.python

%files node-service-ruby
%defattr(-,root,root,-)
%doc README.md
%{_datarootdir}/%{name}/service/org.tyrion.service.ruby

%changelog
* Thu Jul 29 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
