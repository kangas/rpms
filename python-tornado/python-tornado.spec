%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_version: %define python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}

%if "%{python_version}" <= "2.5"
%define python_base %{python_sitearch}
%else
%define python_base %{python_sitelib}
%endif

%define upstream_name tornado

Name:           python-%{upstream_name}
Version:        0.1
Release:        1%{?dist}
Summary:        A non-blocking web server framework

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org/
Source0:        http://www.tornadoweb.org/static/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if "%{python_version}" > "2.5"
BuildArch:      noarch
%endif
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-pycurl
Requires:       python-simplejson

%description
Tornado is a relatively simple, non-blocking web server framework written in
Python. It's designed to handle thousands of simultaneous connections, making
it ideal for real-time Web services.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix non-executable-script error
%{__sed} -i '/^#!\/usr\/bin\/env\ python/d' demos/*/*.py tornado/*.py
# Fix spurious-executable-perm warning
find demos/ -type f -exec chmod 0644 {} \;
# Fix zero-length errors
find demos/ -size 0 -delete

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%if "%{python_version}" <= "2.5"
  # Fix non-standard-executable-perm error
  %{__chmod} 0755 %{buildroot}%{python_sitearch}/%{upstream_name}/epoll.so
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README demos/
%{python_base}/%{upstream_name}*
%{python_base}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Thu Sep 10 2009 Silas Sewell <silas@sewell.ch> - 0.1-1
- Initial package
