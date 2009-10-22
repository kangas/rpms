%define snapshot 20090828225927

Name:             fossil
Version:          0.0
Release:          0.2.%{snapshot}%{?dist}
Summary:          A distributed SCM with bug tracking and wiki

Group:            Development/Tools
License:          GPLv2
URL:              http://www.fossil-scm.org/
Source0:          http://www.fossil-scm.org/download/%{name}-src-%{snapshot}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    zlib-devel

%description
Fossil is a simple, high-reliability, distributed software configuration
management with distributed bug tracking, distributed wiki and built-in web
interface.

%package doc
Summary:          Fossil documentation
Group:            Documentation

%description doc
Documentation in HTML format for %{name}.

%prep
%setup -q -n %{name}-src-%{snapshot}

%build
%{__make} CFLAGS="%{optflags}" %{?_smp_mflags}

%install
%{__rm} -fr %{buildroot}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -p -m 0755 fossil %{buildroot}%{_bindir}/fossil

%clean
%{__rm} -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYRIGHT-GPL2.txt
%{_bindir}/fossil

%files doc
%defattr(-,root,root,-)
%doc www

%changelog
* Tue Sep 08 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.2.20090828225927
- Add doc subpackage and make optflags

* Mon Sep 07 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.1.20090828225927
- Initial package
