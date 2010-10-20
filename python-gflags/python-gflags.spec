%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name gflags

Name:           python-%{upstream_name}
Version:        1.4
Release:        1%{?dist}
Summary:        Commandline flags module for Python

Group:          Development/Languages
License:        BSD
URL:            http://code.google.com/p/python-gflags/
Source0:        http://python-gflags.googlecode.com/files/python-gflags-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-distribute

%description
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove ext from name
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{python_sitelib}/%{upstream_name}.py*
%{python_sitelib}/python_gflags-%{version}-*egg-info
%{_bindir}/gflags2man

%changelog
* Wed Oct 13 2010 Silas Sewell <silas@sewell.ch> - 1.4-1
- Initial package
