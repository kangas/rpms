%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name eventlet

Name:           python-%{upstream_name}
Version:        0.9.7
Release:        1%{?dist}
Summary:        Highly concurrent Python networking library

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/eventlet
Source0:        http://pypi.python.org/packages/source/p/pytc/eventlet-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       libevent

%description
Eventlet is a concurrent networking library for Python that allows you to
change how you run your code, not how you write it.

It uses epoll or libevent for highly scalable non-blocking I/O. Coroutines
ensure that the developer uses a blocking style of programming that is similar
to threading, but provide the benefits of non-blocking I/O. The event dispatch
is implicit, which means you can easily use Eventlet from the Python
interpreter, or as a small part of a larger application.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build  --without-greenlet

# Remove hidden file
%{__rm} -f examples/._producer_consumer.py

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove benchmarks which are installed into site-packages
%{__rm} -fr %{buildroot}%{python_sitelib}/benchmarks

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE NEWS README README.twisted examples/
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Wed Mar 17 2010 Silas Sewell <silas@sewell.ch> - 0.9.7-1
- Initial build
