%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define upstream_name beanstalkc

Name:           python-%{upstream_name}
Version:        0.1.1
Release:        1%{?dist}
Summary:        A beanstalkd client library for Python

Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/earl/beanstalkc
Source0:        http://pypi.python.org/packages/source/b/beanstalkc/%{upstream_name}-%{version}.tar.gz
Patch0:         beanstalkc-0.1.1.py24-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       PyYAML

%description
beanstalkc is a Python client library for beanstalkd.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix for Python 2.4 (7880eaa3f4ed02cb2e0aebba01fee9fcdffeb7f9)
%patch0 -p1
# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/env python/,+1 d' beanstalkc.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/%{upstream_name}.*
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Tue Nov 10 2009 Silas Sewell <silas@sewell.ch> - 0.1.1-1
- Initial package
