Name:           libv8
Version:        2.2.4.2
Release:        1%{?dist}
Summary:        V8 JavaScript Engine

Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/apis/v8
# svn export http://v8.googlecode.com/svn/tags/%{version} %{name}-%{version}
# tar -czf %{name}-%{version}.tar.gz %{name}-%{version}/
Source0:        %{name}-%{version}.tar.gz
Patch0:         libv8-fix-soname-2.2.4.2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  scons

%description
V8 is Google's open source JavaScript engine which implements ECMAScript as
specified in ECMA-262.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%if 0%{?fedora} > 10
export GCC_VERSION='44'
%endif
%ifarch x86_64
export OPTIONS="arch=x64"
%else
export OPTIONS="arch=ia32"
%endif
scons %{?_smp_mflags} library=shared soname=on mode=release snapshot=on os=linux \
    console=readline $OPTIONS
# Rename libv8-*.*.*.*.so to libv8.so.*.*.*.*
ls libv8-*.so | %{__sed} 's/.so//' | %{__awk} -F'-' '{ print $1".so."$2 }' | xargs %{__mv} $( ls libv8-*.so )

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_includedir}
%{__mkdir_p} %{buildroot}/%{_libdir}
%{__install} -p -D -m 644 include/v8.h %{buildroot}/%{_includedir}/v8.h
%{__install} -p -D -m 644 include/v8-debug.h %{buildroot}/%{_includedir}/v8-debug.h
%{__install} -p -D -m 755 libv8.so.* %{buildroot}/%{_libdir}/
( cd %{buildroot}/%{_libdir}/ && ln -sf libv8.so.* libv8.so )

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{_libdir}/libv8.so.*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog samples/
%{_includedir}/*
%{_libdir}/libv8.so

%changelog
* Sun Apr 25 2010 Silas Sewell <silas@sewell.ch> - 2.2.4.2-1
- Update 2.2.4.2

* Sun Jun 21 2009 Silas Sewell <silas@sewell.ch> - 1.2-0.20090621svnr2220
- Initial build
