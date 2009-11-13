%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-keyczar
Version:        0.6b
Release:        1%{?dist}
Summary:        Toolkit for safe and simple cryptography

Group:          Development/Languages
License:        MIT
URL:            http://code.google.com/p/keyczar/
Source0:        http://keyczar.googlecode.com/files/keyczar06b-python.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  python-setuptools-devel
Requires:       python
Requires:       python-crypto
Requires:       python-pyasn1

%description
Keyczar is an open source cryptographic toolkit designed to make it easier and
safer for devlopers to use cryptography in their applications. Keyczar supports
authentication and encryption with both symmetric and asymmetric keys.

%prep
%setup -q -n keyczar06b-python

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CREDITS HISTORY INSTALL LICENSE README demo/ doc/ test/
%{python_sitelib}/*

%changelog
* Tue Feb 24 2009 Silas Sewell <silas at sewell ch> - 0.5.1-1
- Initial build
