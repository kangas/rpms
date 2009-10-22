%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define upstream_name webunit

Name:           python-%{upstream_name}
Version:        1.3.8
Release:        1%{?dist}
Summary:        Unit test a website

Group:          Development/Languages
License:        GPLv2
URL:            http://mechanicalcat.net/tech/webunit
Source0:        http://pypi.python.org/packages/source/f/funkload/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
webunit is a library for testing your websites with code that acts like a web
browser.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix file-not-utf8 warning
iconv -f ISO_8859-1 -t UTF8 CHANGES.txt -o CHANGES.txt.tmp
%{__mv} -f CHANGES.txt.tmp CHANGES.txt

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Remove demo directory from site-packages
%{__rm} -fr %{buildroot}%{python_sitelib}/demo

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.txt demo/
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Mon Sep 28 2009 Silas Sewell <silas@sewel.ch> - 1.3.8-1
- Initial build
