%global realname ops

Name:           python-%{realname}
Version:        0.2.0
Release:        1%{?dist}
Summary:        Python modules and tools for system applications

Group:          Development/Languages
License:        MIT
URL:            https://github.com/opsdojo/ops
Source0:        https://github.com/downloads/opsdojo/ops/ops-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx

%description
ops is a collection of Python modules and tools that makes building and running
system applications a little easier.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build
pushd docs; make html; popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
nosetests

%files
%defattr(-,root,root,-)
%doc LICENSE README.md docs/build/html
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-py*.egg-info

%changelog
* Thu Jan 27 2011 Silas Sewell <silas@sewell.ch> - 0.2.0-1
- Add settings module
- Remove utils.dir, utils.pushd, and utils.popd

* Sat Dec 18 2010 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial build
