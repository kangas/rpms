%global realname cyclone

Name:           python-%{realname}
Version:        0.4
Release:        1%{?dist}
Summary:        A Twisted port of the Tornado web server

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/fiorix/cyclone
Source0:        https://github.com/downloads/fiorix/cyclone/python-cyclone-%{version}.tar.gz
# https://github.com/fiorix/cyclone/issues/issue/5
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
an API very similar to the one implemented by the Tornado web server.

Key differences between Cyclone and Tornado

 * Cyclone is based on Twisted, hence it may be used as a web service protocol
   for interconnection with any other protocol implemented in Twisted.
 * Localization is based upon the standard Gettext instead of the CSV
   implementation in the original Tornado. Moreover, it supports pluralization
   exactly like Tornado does.
 * It ships with an asynchronous HTTP client based on TwistedWeb, however, it's
   fully compatible with one provided by Tornado, which is based on PyCurl.
 * Native support for XMLRPC and JsonRPC.
 * WebSocket protocol class is just like any other Twisted Protocol.
 * Support for sending e-mail based on Twisted Mail, with authentication and
   TLS, plus an easy way to create plain text or HTML messages, and
   attachments.
 * Support for HTTP Authentication.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
sed -i '/#!\/usr\/bin\/env python/d' %{realname}/*.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE README.rst
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*egg-info

%changelog
* Wed Sep 25 2010 Silas Sewell <silas@sewell.ch> - 0.4-1
- Initial package
