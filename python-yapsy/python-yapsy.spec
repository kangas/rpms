%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name Yapsy

Name:           python-yapsy
Version:        1.8
Release:        1%{?dist}
Summary:        A Python plugin system

Group:          Development/Languages
License:        BSD
URL:            http://yapsy.sourceforge.net/
Source0:        http://pypi.python.org/packages/source/Y/Yapsy/Yapsy-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Yapsy is a small library implementing the core mechanisms needed to build a
plugin system into a wider application.

The main purpose is to depend only on Python's standard libraries (at least
version 2.3) and to implement only the basic functionalities needed to detect,
load and keep track of several plugins.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove global test directory
rm -fr %{buildroot}%{python_sitelib}/test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/yapsy
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Fri Nov 05 2010 Silas Sewell <silas@sewell.ch> - 1.8-1
- Initial build
