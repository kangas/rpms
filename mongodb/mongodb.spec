Name:             mongodb
Version:          1.4.1
Release:          1%{?dist}
Summary:          High-performance, schema-free document-oriented database
Group:            Applications/Databases
License:          AGPLv3
URL:              http://www.mongodb.org
Source0:          http://downloads.mongodb.org/src/mongodb-src-r%{version}.tar.gz
Source1:          mongodb.init
Source2:          mongodb.logrotate
Patch0:           mongodb-1.0.1.SConstruct.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    python-devel >= 2.6
BuildRequires:    scons
BuildRequires:    boost-devel
BuildRequires:    pcre-devel
BuildRequires:    js-devel
BuildRequires:    readline-devel
BuildRequires:    libpcap-devel
BuildRequires:    unittest

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

%description
MongoDB (from "humongous") is a scalable, high-performance, open source,
schema-free, document-oriented database. Written in C++, MongoDB features:

 * Document-oriented storage (the simplicity and power of JSON-like data schemas)
 * Dynamic queries
 * Full index support, extending to inner-objects and embedded arrays
 * Query profiling
 * Fast, in-place updates
 * Efficient storage of binary data large objects (e.g. photos and videos)
 * Replication and fail-over support
 * Auto-sharding for cloud-level scalability
 * MapReduce for complex aggregation
 * Commercial Support, Training, and Consulting

MongoDB bridges the gap between key-value stores (which are fast and highly
scalable) and traditional RDBMS systems (which provide structured schemas and
powerful queries).

%package devel
Summary:        MongoDB header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
This package provides the header files and C++ driver for MongoDB. MongoDB is
a high-performance, open source, schema-free document-oriented database.

%prep
%setup -q -n %{name}-src-r%{version}

# Enable debuginfo
%patch0 -p1

# change dbpath
%{__sed} -i 's|/data/db/|%{_sharedstatedir}/%{name}/|' db/pdfile.cpp db/db.cpp

%build
scons %{?_smp_mflags} .

%install
%{__rm} -rf %{buildroot}
scons %{?_smp_mflags} install --prefix=%{buildroot}%{_prefix}
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
%{__rm} -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c "MongoDB Database Server" %{name}
exit 0

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
%doc README GNU-AGPL-3.0.txt
%dir %attr(0755, mongodb, root) %{_sharedstatedir}/%{name}
%dir %attr(0755, mongodb, root) %{_localstatedir}/log/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/mongo*
%{_initddir}/%{name}

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/mongo
%{_libdir}/libmongoclient.a

%changelog
* Fri Apr 22 2010 Silas Sewell <silas@sewell.ch> - 1.4.1-1
- Update to 1.4.1

* Fri Mar 05 2010 Silas Sewell <silas@sewell.ch> - 1.2.4-1
- Update to 1.2.4

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.0.1-1
- Update to 1.0.1

* Fri Oct  2 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-3
- fixed libpath issue for 64bit systems

* Thu Oct  1 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-2
- added virtual -static package

* Mon Aug 31 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-1
- Initial release.
