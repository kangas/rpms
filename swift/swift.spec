%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           swift
Version:        1.0.2
Release:        1%{?dist}
Summary:        OpenStack Object Storage

Group:          Development/Languages
License:        ASL 2.0
URL:            http://www.openstack.org/projects/storage/
Source0:        http://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       python(abi) >= 2.5
Requires:       python-configobj
Requires:       python-eventlet
Requires:       python-simplejson
Requires:       python-webob
Requires:       pyxattr

%description
OpenStack Object Storage aggregates commodity servers to work together in
clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.

%package doc
Summary:        Documentation for %{name}
Group:          Development/Libraries

BuildRequires:  python-sphinx
# Required for genereating docs
BuildRequires:  python(abi) >= 2.5
BuildRequires:  python-eventlet
BuildRequires:  python-simplejson
BuildRequires:  python-webob
BuildRequires:  pyxattr


%description doc
This package contains development documentation files for the %{name} library.

%prep
%setup -q
# Fix wrong-file-end-of-line-encoding warning
sed -i 's/\r//' LICENSE

%build
%{__python} setup.py build
# Build docs
pushd doc; make html; popd
# Fix hidden-file-or-dir warning 
rm doc/build/html/.buildinfo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%{_bindir}/st
%{_bindir}/swift-*
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-*.egg-info

%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html

%changelog
* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
