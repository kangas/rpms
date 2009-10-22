%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-libgearman
Version:        0.0.1
Release:        1%{?dist}
Summary:        A Python wrapper of libgearman

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/python-libgearman
Source0:        http://pypi.python.org/packages/source/p/python-libgearman/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgearman-devel
BuildRequires:  libevent-devel
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
python-libgearman is a Python wrapper of libgearman.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
chmod 0755 %{buildroot}%{python_sitearch}/gearman/_libgearman.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO
%{python_sitearch}/gearman
%{python_sitearch}/python_libgearman-%{version}-*.egg-info

%changelog
* Wed Aug 19 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
