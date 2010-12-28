Name:             mongrel2
Version:          1.4
Release:          1%{?dist}
Summary:          A language agnostic web server
Group:            System Environment/Libraries
License:          BSD
URL:              http://mongrel2.org
Source0:          http://mongrel2.org/static/downloads/mongrel2-%{version}.tar.bz2
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    zeromq-devel
BuildRequires:    sqlite-devel
BuildRequires:    latex

%description
Mongrel2 is an application, language, and network architecture agnostic web
server that focuses on web applications using modern browser technologies.

%prep
%setup -q

%build
make OPTLIBS="-lpthread" build

%install
rm -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} OPTLIBS="-lpthread" install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE examples/
%{_bindir}/m2sh
%{_bindir}/mongrel2

%changelog
* Fri Dec 24 2010 Silas Sewell <silas@sewell.ch> - 1.4-1
- Initial build
