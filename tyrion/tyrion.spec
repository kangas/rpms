Name:             tyrion
Version:          0.1.0
Release:          1%{?dist}
Summary:          A daemon that allows for the asynchronous running of remote processes
Group:            System Environment/Daemons
License:          BSD
URL:              http://www.tidg.org/tyrion
Source0:          http://github.com/downloads/tidg/tyrion/tyrion-%{version}.tar.bz2
Source1:          tyrion.logrotate
Source2:          tyrion.init
Source3:          tyrion.acl
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    bc
BuildRequires:    gtest-devel
BuildRequires:    txmpp-devel
BuildRequires:    scons

Requires:         %{name}-libs = %{version}-%{release}

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig

Provides:         tyrion-node = %{version}
Obsoletes:        tyrion-node < 0.1.0

Provides:         tyrion-libs = %{version}
Obsoletes:        tyrion-libs < 0.1.0

%description
Tyrion is a lightweight daemon that allows for the asynchronous running of
remote processes. It provides basic access controls, process timeouts and a
communication protocol (XMPP) that integrates nicely into both corporate and
cloud environments.

%package          service-perl
Summary:          A Tyrion Perl service
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         perl

%description      service-perl
Tyrion is a lightweight daemon that allows for the asynchronous running of
remote processes.

The %{name}-service-perl package contains a service that allows for the
running of arbitrary Perl code.

%package          service-python
Summary:          A Tyrion Python service
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         python

Provides:         tyrion-node-service-python = %{version}
Obsoletes:        tyrion-node-service-python < 0.1.0

%description      service-python
Tyrion is a lightweight daemon that allows for the asynchronous running of
remote processes.

The %{name}-service-python package contains a service that allows for the
running of arbitrary Python code.

%package          service-ruby
Summary:          A Tyrion Ruby service
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         ruby

Provides:         tyrion-node-service-ruby = %{version}
Obsoletes:        tyrion-node-service-ruby < 0.1.0

%description      service-ruby
Tyrion is a lightweight daemon that allows for the asynchronous running of
remote processes.

The %{name}-service-ruby package contains a service that allows for the
running of arbitrary Ruby code.

%prep
%setup -q

%build
scons %{?_smp_mflags} --flags="%{optflags}"

%check
./test

%install
rm -rf %{buildroot}
scons %{?_smp_mflags} --flags="%{optflags}" --install \
    --sbindir=%{buildroot}/%{_sbindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
cp -rp service %{buildroot}%{_datadir}/%{name}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
install -p -D -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/acl.conf
install -p -D -m 600 config/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -p -D -m 644 doc/%{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS LICENSE NOTICE README.md config/acl.conf config/tyrion.conf
%config(noreplace) %{_sysconfdir}/%{name}/acl.conf
%config(noreplace) %{_sysconfdir}/%{name}/tyrion.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/log/%{name}
%{_datadir}/%{name}/service/org.tyrion.service.bash
%{_initddir}/%{name}
%{_mandir}/man8/tyrion.8.*
%{_sbindir}/tyrion

%files service-perl
%defattr(-,root,root,-)
%{_datadir}/%{name}/service/org.tyrion.service.perl

%files service-python
%defattr(-,root,root,-)
%{_datadir}/%{name}/service/org.tyrion.service.python

%files service-ruby
%defattr(-,root,root,-)
%{_datadir}/%{name}/service/org.tyrion.service.ruby

%changelog
* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Remove Tyrion client
- Obsolete node packages
- Add check section

* Thu Aug 12 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-2
- Don't gzip man pages
- Remove useless documentation from node-service subpackages

* Thu Jul 29 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
