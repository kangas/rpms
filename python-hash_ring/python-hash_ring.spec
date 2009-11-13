%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-hash_ring
Version:        1.2
Release:        3%{?dist}
Summary:        Python implementation of consistent hashing

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/hash_ring
Source0:        http://pypi.python.org/packages/source/h/hash_ring/hash_ring-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-memcached

%description
hash_ring implements consistent hashing that can be used when the number of
server nodes can increase or decrease. Consistent hashing is a scheme that
provides a hash table functionality in a way that the adding or removing of one
slot does not significantly change the mapping of keys to slots.

%prep
%setup -q -n hash_ring-%{version}
# Remove bootstrap for setuptools which is provided by BuildRequires
sed -i '/^import\ ez_setup$/,+1 d' setup.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO
%{python_sitelib}/hash_ring
%{python_sitelib}/hash_ring-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.2-3
- Normalize spec

* Sat Apr 11 2009 Silas Sewell <silas@sewell.ch> - 1.2-2
- Fix license
- Make files section more explicit

* Fri Apr 10 2009 Silas Sewell <silas@sewell.ch> - 1.2-1
- Initial package
