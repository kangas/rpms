Name:           lxc
Version:        0.6.3
Release:        2%{?dist}
Summary:        Linux Resource Containers

Group:          Applications/System
License:        LGPLv2+
URL:            http://lxc.sourceforge.net
Source0:        http://lxc.sourceforge.net/download/lxc/%{name}-%{version}.tar.gz
# Upstream commit 90e0a869ac5f3a889487126568f1d3c7c34b7046
Patch0:         lxc-0.6.3.netlink-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake
BuildRequires:  docbook-utils
BuildRequires:  kernel-headers
BuildRequires:  libcap-devel
BuildRequires:  libtool

%description
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

%package        libs
Summary:        Runtime library files for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    libs
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-libs package contains libraries for running %{name} applications.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Linux Resource Containers provide process and resource isolation without the
overhead of full virtualization.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
./autogen.sh
%configure F77=no --enable-static=no
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/%{name}-*
%{_libexecdir}/%{name}-init
%{_mandir}/man*/%{name}*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/liblxc-%{version}.so

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_datadir}/pkgconfig/%{name}.pc
%{_includedir}/*
%{_libdir}/liblxc.so

%changelog
* Mon Jul 27 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-2
- Apply patch for rawhide kernel

* Sat Jul 25 2009 Silas Sewell <silas@sewell.ch> - 0.6.3-1
- Initial package
