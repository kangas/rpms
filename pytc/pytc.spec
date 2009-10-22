%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pytc
Version:        0.8
Release:        2%{?dist}
Summary:        Tokyo Cabinet Python bindings

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/pytc
Source0:        http://pypi.python.org/packages/source/p/pytc/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  tokyocabinet-devel
BuildRequires:  python-setuptools

%description
Python bindings for Tokyo Cabinet.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
chmod 0755 %{buildroot}%{python_sitearch}/%{name}.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO
%{python_sitearch}/%{name}.so
%{python_sitearch}/%{name}-%{version}-*.egg-info

%changelog
* Sun Jun 07 2009 Silas Sewell <silas@sewell.ch> - 0.8-2
- Release bump for libtokyocabinet soname change
- According to changelog functions were added but not changed

* Mon May 25 2009 Silas Sewell <silas@sewell.ch> - 0.8-1
- Update to 0.8

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.7-3
- Normalize spec

* Thu Mar 26 2009 Silas Sewell <silas@sewell.ch> - 0.7-2
- Update package name to conform to Fedora naming standards
- Remove unneeded requires
- Change define to global

* Wed Mar 11 2009 Silas Sewell <silas@sewell.ch> - 0.7-1
- Initial build
