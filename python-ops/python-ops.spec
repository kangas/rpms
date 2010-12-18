%global realname ops

Name:           python-%{realname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        A collection Python modules for data center automation

Group:          Development/Languages
License:        BSD
URL:            https://github.com/opsdojo/ops
Source0:        https://github.com/downloads/opsdojo/ops/ops-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-nose

%description
ops is a collection Python modules for data center automation.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
nosetests

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-py*.egg-info

%changelog
* Sat Dec 18 2010 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial build
