%global with_expat2 %{?_with_expat2: 1} %{?!_with_expat: 0}

Name:             txmpp
Version:          0.0.2
Release:          2%{?dist}
Summary:          A C++ XMPP library
Group:            System Environment/Libraries
License:          BSD
URL:              http://www.tidg.org/txmpp
Source0:          http://github.com/downloads/tidg/txmpp/%{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with_expat2}
BuildRequires:    expat2-devel >= 2.0.1
%else
BuildRequires:    expat-devel >= 2.0.1
%endif
BuildRequires:    openssl-devel
BuildRequires:    scons

%description
txmpp is a permissively licensed C++ XMPP library.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
txmpp is a permissively licensed C++ XMPP library.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
scons %{?_smp_mflags} --flags="%{optflags}"

%install
rm -rf %{buildroot}
scons %{?_smp_mflags} --flags="%{optflags}" --install \
  --includedir=%{buildroot}/%{_includedir} \
  --libdir=%{buildroot}/%{_libdir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README.md
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/txmpp
%{_libdir}/*.so

%changelog
* Sun Jul 25 2010 Silas Sewell <silas@sewell.ch> - 0.0.2-2
- Remove documentation from devel package
- Fix main package group

* Fri Jul 02 2010 Silas Sewell <silas@sewell.ch> - 0.0.2-1
- Release 0.0.2
- Include AUTHORS & CHANGELOG

* Tue Jun 15 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
