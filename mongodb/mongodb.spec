Name:           mongodb
Version:        1.0.0
Release:        1%{?dist}
Summary:        A schema-free document-oriented database

Group:          Applications/System
License:        AGPLv3
URL:            http://www.mongodb.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  boost-devel
BuildRequires:  js-devel
BuildRequires:  libpcap-devel
BuildRequires:  ncurses-devel
BuildRequires:  pcre-devel
BuildRequires:  readline-devel
BuildRequires:  scons

%description
Mongo is a high-performance, open source, schema-free document-oriented 
database. MongoDB is written in C++ and offers the following features:
 * Collection oriented storage: easy storage of object/JSON-style data
 * Dynamic queries
 * Full index support, including on inner objects and embedded arrays
 * Query profiling
 * Replication and fail-over support
 * Efficient storage of binary data including large objects (e.g. videos)
 * Auto-sharding for cloud-level scalability (currently in early alpha)

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Mongo is a high-performance, open source, schema-free document-oriented 
database.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
scons %{?_smp_mflags}

%install
rm -rf %{buildroot}
scons --prefix=%{buildroot}%{_prefix} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc GNU-AGPL-3.0.txt README distsrc/
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/*
%{_libdir}/*

%changelog
* Thu Aug 27 2009 Silas Sewell <silas@sewell.ch> - 1.0.0-1
- Initial build
