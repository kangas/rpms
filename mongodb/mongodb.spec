%global snapshot e316c78

Name:           mongodb
Version:        1.0.1
Release:        1%{?dist}
Summary:        High-performance, schema-free document-oriented database
Group:          Applications/Databases
License:        AGPLv3
URL:            http://www.mongodb.org
Source0:        http://download.github.com/%{name}-mongo-%{snapshot}.tar.gz
# init-script:
Source1:        mongodb.init
Source2:        mongodb.logrotate
Patch0:         mongodb-1.0.1.SConstruct.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel >= 2.6
BuildRequires:  scons
BuildRequires:  boost-devel
BuildRequires:  pcre-devel
BuildRequires:  js-devel
BuildRequires:  readline-devel
BuildRequires:  libpcap-devel
# to run tests
BuildRequires:  unittest

Requires(post): chkconfig
Requires(preun): chkconfig

Requires(pre):  shadow-utils

# This is for /sbin/service
Requires(postun): initscripts


%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. MongoDB is written in C++ and offers the following
features:
    * Collection oriented storage: easy storage of object/JSON-style data
    * Dynamic queries
    * Full index support, including on inner objects and embedded arrays
    * Query profiling
    * Replication and fail-over support
    * Efficient storage of binary data including large objects (e.g. photos
    and videos)
    * Auto-sharding for cloud-level scalability (currently in early alpha)
    * Commercial Support Available

A key goal of MongoDB is to bridge the gap between key/value stores (which are
fast and highly scalable) and traditional RDBMS systems (which are deep in
functionality).

%package devel
Summary:        MongoDB header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
This package provides the header files and C++ driver for MongoDB. MongoDB is
a high-performance, open source, schema-free document-oriented database.

%prep
%setup -q -n %{name}-mongo-%{snapshot}

# Enable debuginfo
%patch0 -p1

# change dbpath
%{__sed} -i 's|/data/db/|%{_sharedstatedir}/%{name}/|' db/pdfile.cpp db/db.cpp


%build
scons %{?_smp_mflags} .


%install
rm -rf %{buildroot}
scons %{?_smp_mflags} install --prefix=%{buildroot}%{_prefix}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}


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
* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.0.1-1
- Update to 1.0.1

* Fri Oct  2 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-3
- fixed libpath issue for 64bit systems

* Thu Oct  1 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-2
- added virtual -static package

* Mon Aug 31 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-1
- Initial release.
