%global realname huck

Name:           python-%{realname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        A web framework based on Twisted

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/silas/huck
Source0:        http://pypi.python.org/packages/source/h/huck/huck-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-twisted-core
Requires:       python-twisted-mail
Requires:       python-twisted-web >= 10.1

%description
Huck is a web application framework based on Twisted and derived from Tornado
and Cyclone.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*egg-info

%changelog
* Thu Jan 27 2011 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial package
