%global upstream_name asyncmongo

Name:           python-%{upstream_name}
Version:        0.1
Release:        1%{?dist}
Summary:        An asynchronous Python MongoDB library

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/bitly/asyncmongo
Source0:        https://github.com/downloads/bitly/asyncmongo/asyncmongo-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

Requires:       pymongo >= 1.9
Requires:       python-bson
Requires:       python-tornado

%description
AsyncMongo is an asynchronous Python library for accessing MongoDB using the
Tornado IOLoop.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix non-executable-script error
sed -i '/^#!\/bin\/env python$/,+1 d' asyncmongo/*.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}*.egg-info

%changelog
* Thu Nov 18 2010 Silas Sewell <silas@sewell.ch> - 0.1-1
- Initial package
