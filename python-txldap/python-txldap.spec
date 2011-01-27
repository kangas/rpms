%global realname txldap

Name:           python-%{realname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        Twisted wrapper for python-ldap

Group:          Development/Languages
License:        MIT
URL:            https://github.com/silas/txldap
Source0:        https://github.com/downloads/silas/txldap/txldap-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-ldap
BuildRequires:  python-twisted-core
Requires:       python-ldap
Requires:       python-twisted-core

%description
txldap is a Twisted wrapper for python-ldap.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/%{realname}.py*
%{python_sitelib}/%{realname}-%{version}-py*.egg-info

%changelog
* Thu Jan 27 2011 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial build
