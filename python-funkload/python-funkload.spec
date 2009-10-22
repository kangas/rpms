%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define upstream_name funkload

Name:           python-%{upstream_name}
Version:        1.10.0
Release:        1%{?dist}
Summary:        Function and load web testing

Group:          Development/Languages
License:        GPLv2
URL:            http://funkload.nuxeo.org
Source0:        http://pypi.python.org/packages/source/f/funkload/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       gnuplot
Requires:       python-docutils
Requires:       python-webunit
Requires:       python-setuptools

%description
FunkLoad is a functional and load web tester written in Python.

%prep
%setup -q -n %{upstream_name}-%{version}

# Fix non-executable-script error
%{__sed} -i '/^#!\/usr\/bin\/python/,+1 d' src/funkload/*Runner.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc BUILDOUT.txt CHANGES.txt INSTALL.txt LICENSE.txt README.txt THANKS TODO.txt doc/
%{python_sitelib}/%{upstream_name}*
%{_bindir}/fl-*

%changelog
* Mon Sep 28 2009 Silas Sewell <silas@sewell.ch> - 1.10.0-1
- Initial build
