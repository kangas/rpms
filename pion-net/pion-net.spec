Name:           pion-net
Version:        3.0.13
Release:        1%{?dist}
Summary:        A C++ development library for implementing lightweight HTTP interfaces

Group:          Development/Libraries
License:        Boost
URL:            http://www.pion.org/projects/pion-network-library
Source0:        http://www.pion.org/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  doxygen
BuildRequires:  openssl-devel
BuildRequires:  bzip2-devel

%description
Pion Network Library (pion-net) is a C++ development library for implementing
lightweight HTTP interfaces.

The motivation of pion-net is not to implement yet another web server, but to
provide HTTP(S) functionality to new or existing C++ applications.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Pion Network Library (pion-net) is a C++ development library for implementing
lightweight HTTP interfaces.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure F77=no --with-boost-extension=-mt
%{__make} %{?_smp_mflags} all

%check
%{__make} check

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.{a,la}
rm -f %{buildroot}%{_datadir}/*.{a,la}

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS TODO README
%{_bindir}/Pion*
%{_libdir}/libpion-common-3.0.so
%{_libdir}/libpion-net-3.0.so

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/pion
%{_libdir}/libpion-common.so
%{_libdir}/libpion-net.so
%{_datadir}/pion

%changelog
* Tue Jul 13 2010 Silas Sewell <silas@sewell.ch> - 3.0.13-1
- Initial package
