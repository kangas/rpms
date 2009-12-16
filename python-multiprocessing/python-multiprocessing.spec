%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global upstream_name multiprocessing

Name:           python-%{upstream_name}
Version:        2.6.2.1
Release:        1%{?dist}
Summary:        A backport of the Python 2.6 multiprocessing package

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/multiprocessing
Source0:        http://pypi.python.org/packages/source/m/multiprocessing/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
multiprocessing is a backport of the Python 2.6/3.0 multiprocessing
package. The multiprocessing package itself is a renamed and updated version of
R Oudkerk's pyprocessing package.

This standalone variant is intended to be compatible with Python 2.4 and 2.5,
and will draw it's fixes/improvements from python-trunk.

%prep
%setup -q -n %{upstream_name}-%{version}
# Remove test file
%{__rm} -f Lib/multiprocessing/tests.py

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
%{__chmod} 0755 %{buildroot}%{python_sitearch}/%{upstream_name}/_%{upstream_name}.so
%{__chmod} 0755 %{buildroot}%{python_sitearch}/%{upstream_name}/_mmap25.so || true

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt
%{python_sitearch}/%{upstream_name}
%{python_sitearch}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Tue Dec 15 2009 Silas Sewell <silas@sewell.ch> - 2.6.2.1-1
- Initial build
