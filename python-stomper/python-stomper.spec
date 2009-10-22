%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-stomper
Version:        0.2.2
Release:        8%{?dist}
Summary:        A Python client implementation of the STOMP protocol

Group:          Development/Languages
License:        ASL 2.0
URL:            http://code.google.com/p/stomper
Source0:        http://stomper.googlecode.com/files/stomper-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Stomper is a Python client implementation of the STOMP protocol. The client is
attempting to be transport layer neutral. This module provides functions to
create and parse STOMP messages in a programatic fashion.

%prep
%setup -q -n stomper-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Remove documentation from install root
rm -rf %{buildroot}%{python_sitelib}/stomper/examples
rm -rf %{buildroot}%{python_sitelib}/stomper/tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc lib/stomper/doc lib/stomper/examples lib/stomper/tests
%{python_sitelib}/stomper
%{python_sitelib}/stomper-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-8
- Normalize spec

* Thu Apr 09 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-7
- Remove Python version dependency

* Sun Mar 29 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-6
- Fix dependencies

* Thu Mar 26 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-5
- Update package name to conform to Fedora naming standards
- Change define to global

* Fri Mar 20 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-4
- Update upstream package to remove hidden files

* Thu Mar 05 2009 Silas Sewell <silas@sewell.ch> - 0.2.2-3
- Manually remove hidden files

* Wed Dec 17 2008 Silas Sewell <silas@sewell.ch> - 0.2.2-2
- Increase Python requirements to 2.5 because stomper uses uuid

* Wed Dec 17 2008 Silas Sewell <silas@sewell.ch> - 0.2.2-1
- Initial package
