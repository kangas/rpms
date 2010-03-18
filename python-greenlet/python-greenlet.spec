%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global upstream_name greenlet

Name:           python-%{upstream_name}
Version:        0.2
Release:        1%{?dist}
Summary:        Lightweight in-process concurrent Python programming

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/greenlet
Source0:        http://pypi.python.org/packages/source/p/pytc/greenlet-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
The "greenlet" package is a spin-off of Stackless, a version of CPython that
supports micro-threads called "tasklets". Tasklets run pseudo-concurrently
(typically in a single or a few OS-level threads) and are synchronized with
data exchanges on "channels".

A "greenlet", on the other hand, is a still more primitive notion of
micro-thread with no implicit scheduling; coroutines, in other words. This is
useful when you want to control exactly when your code runs. You can build
custom scheduled micro-threads on top of greenlet; however, it seems that
greenlets are useful on their own as a way to make advanced control flow
structures. For example, we can recreate generators; the difference with
Python's own generators is that our generators can call nested functions and
the nested functions can yield values too. Additionally, you don't need a
"yield" keyword. See the example in test_generator.py.

Greenlets are provided as a C extension module for the regular unmodified
interpreter.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitearch}/%{upstream_name}.so
%{python_sitearch}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Wed Mar 17 2010 Silas Sewell <silas@sewell.ch> - 0.9.7-1
- Initial build
