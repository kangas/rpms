%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-cly
Version:        0.9
Release:        3%{?dist}
Summary:        A module for adding powerful text-based consoles to your Python application

Group:          Development/Languages
License:        BSD
URL:            http://swapoff.org/cly
Source0:        http://pypi.python.org/packages/source/c/cly/cly-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-docutils
BuildRequires:  python-pygments
BuildRequires:  python-setuptools
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel

%description
CLY is a Python module for simplifying the creation of interactive shells, much
like the built-in "cmd" module on steroids.

%prep
%setup -q -n cly-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build
# Build documents
make --directory doc/

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
%{__chmod} 0755 %{buildroot}%{python_sitearch}/cly/rlext.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING PKG-INFO README doc/*.html doc/tutorial.py doc/video1.py
%{python_sitearch}/cly
%{python_sitearch}/cly-%{version}-*.egg-info

%changelog
* Fri Mar 05 2010 Silas Sewell <silas@sewell.ch> - 0.9-3
- Fix build on EPEL

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.9-2
- Normalize spec

* Sat Apr 11 2009 Silas Sewell <silas@sewell.ch> - 0.9-1
- Initial package
