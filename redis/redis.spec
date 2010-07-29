Name:             redis
Version:          1.2.6
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://code.google.com/p/redis/
Source0:          http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:          redis.logrotate
Source2:          redis.init
Source3:          redis.conf
Source10:         redis-benchmark.1
Source11:         redis-cli.1
Source12:         redis-server.8
Source13:         redis-stat.1
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

%build
%{__make} %{?_smp_mflags}
# Build man pages
mkdir man; pushd man
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .
cp %{SOURCE13} .
gzip *.{1,8}
popd

%install
%{__rm} -fr %{buildroot}
# Install binaries
install -p -D -m 755 redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
install -p -D -m 755 redis-cli %{buildroot}%{_bindir}/redis-cli
install -p -D -m 755 redis-stat %{buildroot}%{_bindir}/redis-stat
install -p -D -m 755 redis-server %{buildroot}%{_sbindir}/redis-server
# Install man pages
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}%{_mandir}/man8
cp -p man/*.1.gz %{buildroot}%{_mandir}/man1
cp -p man/*.8.gz %{buildroot}%{_mandir}/man8
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/redis
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/redis
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/redis.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/redis
install -d -m 755 %{buildroot}%{_localstatedir}/log/redis
install -d -m 755 %{buildroot}%{_localstatedir}/run/redis

%clean
%{__rm} -fr %{buildroot}

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
%config(noreplace) %{_sysconfdir}/logrotate.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/redis
%dir %attr(0755, redis, root) %{_localstatedir}/log/redis
%dir %attr(0755, redis, root) %{_localstatedir}/run/redis
%{_bindir}/redis-*
%{_initrddir}/redis
%{_mandir}/man1/redis*.1.gz
%{_mandir}/man8/redis*.8.gz
%{_sbindir}/redis-*

%changelog
* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
