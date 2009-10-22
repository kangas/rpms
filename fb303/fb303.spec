%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define snapshot 795861

# Java
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name:             fb303
Version:          0.2
Release:          0.20090501svn%{snapshot}%{?dist}
Summary:          Facebook Bassline

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://incubator.apache.org/thrift
# svn export http://svn.apache.org/repos/asf/incubator/thrift/trunk/contrib/fb303 -r %{snapshot} fb303-%{version}
# tar -czf fb303-%{version}.tar.gz fb303-%{version}/
Source0:          %{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:         %{name} = %{version}-%{release}

BuildRequires:    automake
BuildRequires:    byacc
BuildRequires:    boost-devel >= 1.33.1
BuildRequires:    flex
BuildRequires:    libevent-devel
BuildRequires:    libtool
BuildRequires:    thrift
BuildRequires:    thrift-devel
BuildRequires:    zlib-devel

%description
Facebook Baseline is a standard interface to monitoring, dynamic options and
configuration, uptime reports, activity, and more.

%package devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package java
Summary:          Java bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ant 
BuildRequires:    java-devel
BuildRequires:    jpackage-utils

%description java
Java bindings for %{name}.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel
Requires:         thrift-python

%description python
Python bindings for %{name}.

%package php
Summary:          PHP bindings for %{name}
Group:            Development/Libraries
BuildRequires:    php-devel
Requires:         thrift-php

%description php
PHP bindings for %{name}.

%prep
%setup -q

# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/env python/,+1 d' \
  py/fb303_scripts/*.py \
  py/fb303/FacebookBase.py

%build
./bootstrap.sh
%configure --enable-static=no --with-thriftpath=%{_prefix}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

# Fix install path
sed -i 's/shareddir = lib/shareddir = ${prefix}\/lib/g' cpp/Makefile

%{__make} DESTDIR=%{buildroot} install

# Install Java
pushd java/
ant -Dthrift_home=/usr
find .
popd

# Install PHP
%{__mkdir_p} %{buildroot}%{_datadir}/php/%{name}
%{__cp} -r php/FacebookBase.php %{buildroot}%{_datadir}/php/%{name}/

# Fix lib install path on x86_64
mv %{buildroot}/usr/lib/libfb303.so %{buildroot}%{_libdir}/libfb303.so || true

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_datadir}/fb303
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/thrift/fb303
%{_libdir}/*.so

%files java
%defattr(-,root,root,-)
%doc README
%{_javadir}/libthrift.jar

%files php
%defattr(-,root,root,-)
%doc README
%{_datadir}/php/%{name}

%files python
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}_scripts
%{python_sitelib}/%{name}-*.egg-info

%changelog
* Tue Jul 21 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.20090721svn795861
- Update to latest snapshot

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.20090501svn770888
- Initial build
