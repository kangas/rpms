%define with_expat2 %{?_without_expat2: 0} %{?!_without_expat: 1}

Name:             txmpp
Version:          0.0.1
Release:          1%{?dist}
Summary:          A C++ XMPP library
Group:            Development/Libraries
License:          BSD
URL:              http://github.com/silas/txmpp
Source0:          http://github.com/downloads/silas/txmpp/%{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with_expat2}
BuildRequires:    expat2-devel >= 2.0.1
%else
BuildRequires:    expat-devel >= 2.0.1
%endif
BuildRequires:    openssl-devel
BuildRequires:    scons

Requires:         %{name}-libs = %{version}-%{release}

%description
txmpp is a C++ XMPP library.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
txmpp is a C++ XMPP library.

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
%doc LICENSE README.md
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_includedir}/txmpp
%{_libdir}/*.so

%changelog
* Tue Jun 15 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
