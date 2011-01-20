%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global realname txmongo

Name:           python-%{realname}
Version:        0.3
Release:        0.1%{?dist}
Summary:        An asynchronous MongoDB driver (Twisted)

Group:          Development/Languages
License:        ASL 2.0
# wget https://github.com/fiorix/mongo-async-python-driver/tarball/7ade28f35bd25cfefb1ab86127b9a3bf7fc40b73
# tar -xzf fiorix-mongo-async-python-driver-7ade28f.tar.gz
# mv fiorix-mongo-async-python-driver-7ade28f txmongo-0.3
# tar -czf txmongo-0.3.tar.gz txmongo-0.3/
URL:            https://github.com/fiorix/mongo-async-python-driver
Source0:        %{realname}-%{version}.tar.gz
Patch0:         txmongo-0.3-fix-setup.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-twisted-core

%description
An asynchronous Python driver for the Mongo database, based on Twisted. The
txmongo package is an alternative to the original pymongo shipped with the
Mongo database.

Because the original pymongo package has it's own connection pool and blocking
low-level socket operations, it is hard to fully implement network servers
using the Twisted framework. Instead of deferring database operations to
threads, now it's possible to do it asynchronously, as easy as using the
original API.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst TODO
%{python_sitearch}/%{realname}
%{python_sitearch}/%{realname}-%{version}-*.egg-info

%changelog
* Thu Jan 20 2011 Silas Sewell <silas@shutterstock.ch> - 0.0-0.1
- Initial build
