Name:             redis
Version:          1.2.6
Release:          2%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://code.google.com/p/redis/
Source0:          http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
Source10:         %{name}-benchmark.1
Source11:         %{name}-cli.1
Source12:         %{name}-server.8
Source13:         %{name}-stat.1
Patch0:           %{name}-1.2.6.conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q
%patch0 -p1

%build
%{__make} %{?_smp_mflags}

%install
rm -fr %{buildroot}
# Install binaries
install -p -D -m 755 %{name}-benchmark %{buildroot}%{_bindir}/%{name}-benchmark
install -p -D -m 755 %{name}-cli %{buildroot}%{_bindir}/%{name}-cli
install -p -D -m 755 %{name}-stat %{buildroot}%{_bindir}/%{name}-stat
install -p -D -m 755 %{name}-server %{buildroot}%{_sbindir}/%{name}-server
# Install man pages
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_mandir}/man1/%{name}-benchmark.1
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_mandir}/man1/%{name}-cli.1
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_mandir}/man8/%{name}-server.8
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_mandir}/man1/%{name}-stat.1
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add redis

%pre
getent group redis >/dev/null || groupadd -r redis
getent passwd redis >/dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin \
-c 'Redis Server' redis
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis
fi

%files
%defattr(-,root,root,-)
%doc COPYING README doc/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%{_initrddir}/%{name}
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man8/%{name}*.8*
%{_sbindir}/%{name}-*

%changelog
* Mon Aug 16 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-2
- Don't compress man pages
- Use patch to fix redis.conf

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
