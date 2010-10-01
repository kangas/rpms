%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name cyclone

Name:           python-%{upstream_name}
Version:        0.4
Release:        1%{?dist}
Summary:        An API very similar to the one implemented by the Tornado web server

Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/fiorix/cyclone
Source0:        http://github.com/downloads/fiorix/cyclone/python-cyclone-%{version}.tar.gz
Patch0:         cyclone-0.4-twisted-web.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-twisted-core
Requires:       python-twisted-mail
Requires:       python-twisted-web >= 10.1

%description
Cyclone is a low-level network toolkit, which provides support for HTTP 1.1 in
an API very similar to the one implemented by the Tornado web server - which
was developed by FriendFeed and later released as open source / free software
by Facebook.

%prep
%setup -q -n %{upstream_name}-%{version}
%patch0 -p1
sed -i '/#!\/usr\/bin\/env python/g' %{upstream_name}/*.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE README.rst
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*egg-info

%changelog
* Wed Sep 25 2010 Silas Sewell <silas@sewell.ch> - 0.4-1
- Initial package
