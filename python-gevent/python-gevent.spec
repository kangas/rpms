%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global upstream_name gevent

Name:           python-%{upstream_name}
Version:        0.12.2
Release:        1%{?dist}
Summary:        A coroutine-based Python networking library

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/gevent
Source0:        http://pypi.python.org/packages/source/g/gevent/gevent-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  libevent-devel >= 1.4.0
Requires:       python-greenlet

%description
gevent is a coroutine-based Python networking library that uses greenlet to
provide a high-level synchronous API on top of libevent event loop.

Features include:

  * convenient API around greenlets
  * familiar synchronization primitives (gevent.event, gevent.queue)
  * socket module that cooperates
  * WSGI server on top of libevent-http
  * DNS requests done through libevent-dns
  * monkey patching utility to get pure Python modules to cooperate

%prep
%setup -q -n %{upstream_name}-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
%{__chmod} 0755 %{buildroot}%{python_sitearch}/%{upstream_name}/core.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python_sitearch}/%{upstream_name}
%{python_sitearch}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Wed Mar 17 2010 Silas Sewell <silas@sewell.ch> - 0.12.2-1
- Initial build
