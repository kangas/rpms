%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define real_name line_profiler
%define pre_release b2

Name:           python-%{real_name}
Version:        1.0
Release:        0.3.%{pre_release}%{?dist}
Summary:        A Python line-by-line profiler

Group:          Development/Languages
License:        BSD
URL:            http://packages.python.org/%{real_name}
Source0:        http://pypi.python.org/packages/source/l/%{real_name}/%{real_name}-%{version}%{pre_release}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel

%description
line_profiler will profile the time individual lines of code take to execute.

%prep
%setup -q -n %{real_name}-%{version}%{pre_release}

# Fix non-executable-script error
%{__sed} -i '/^#!\/usr\/bin\/env\ python/d' %{real_name}.py

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Fix non-standard-executable-perm error
chmod 0755 %{buildroot}%{python_sitearch}/_%{real_name}.so

# Rename kernprof.py to fix various .py bindir issues
mv %{buildroot}%{_bindir}/kernprof.py %{buildroot}%{_bindir}/kernprof

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt PKG-INFO README.txt
%{_bindir}/kernprof
%{python_sitearch}/_%{real_name}.so
%{python_sitearch}/%{real_name}.py*
%if !0%{?el5}
%{python_sitearch}/%{real_name}-*.egg-info
%endif

%changelog
* Mon Jun 01 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.3.b2
- Rename kernprof.py to kernprof

* Fri May 29 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.2.b2
- Remove pyc and pyo exclude for bindir as Koji doesn't create them

* Wed May 27 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.1.b2
- Initial build
