%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           peafowl
Version:        0.8
Release:        2%{?dist}
Summary:        A powerful but simple messaging server

Group:          Applications/System
License:        MIT
URL:            http://code.google.com/p/peafowl
Source0:        http://peafowl.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       memcached
Requires:       python-memcached

%description
Peafowl is a powerful but simple messaging server that enables reliable
distributed queuing with an absolutely minimal overhead by using memcache
protocol for maximum cross-platform compatibility.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README PKG-INFO tests/
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.8-2
- Normalize spec

* Thu Jan 29 2009 Silas Sewell <silas@sewell.ch> - 0.8-1
- Update to 0.8

* Tue Dec 23 2008 Silas Sewell <silas@sewell.ch> - 0.7-1
- Initial package
