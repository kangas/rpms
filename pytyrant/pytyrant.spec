%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pytyrant
Version:        1.1.17
Release:        2%{?dist}
Summary:        A pure Python client implementation of Tokyo Tyrant

Group:          Development/Languages
License:        MIT
URL:            http://code.google.com/p/pytyrant
Source0:        http://pypi.python.org/packages/source/p/pytyrant/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
pytyrant is a pure Python client implementation of the binary Tokyo Tyrant
protocol.

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
%doc LICENSE.txt PKG-INFO README
%{python_sitelib}/%{name}.py*
%{python_sitelib}/%{name}-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.1.17-2
- Normalize spec

* Thu Mar 26 2009 Silas Sewell <silas@sewell.ch> - 1.1.17-1
- Update to 1.1.17
- Update package name to conform to Fedora naming standards
- Remove unneeded requires
- Change define to global

* Wed Mar 11 2009 Silas Sewell <silas@sewell.ch> - 1.1.11-1
- Initial build
