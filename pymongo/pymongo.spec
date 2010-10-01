%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Fix private-shared-object-provides error
%global _use_internal_dependency_generator 0
%global __find_provides %{_rpmconfigdir}/find-provides | grep -v cvisualmodule
%global __find_requires %{_rpmconfigdir}/find-requires | grep -v cvisualmodule

Name:           pymongo
Version:        1.9
Release:        1%{?dist}
Summary:        Python driver for MongoDB

Group:          Development/Languages
License:        ASL 2.0
URL:            http://api.mongodb.org/python
Source0:        http://pypi.python.org/packages/source/p/pymongo/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       python-bson = %{version}-%{release}

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
The Python driver for MongoDB.

%package gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description gridfs
GridFS is a storage specification for large objects in MongoDB.

%package -n python-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n python-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{python_sitearch}/%{name}/_cmessage.so
chmod 755 %{buildroot}%{python_sitearch}/bson/_cbson.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README.rst doc
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}-%{version}-*.egg-info

%files gridfs
%defattr(-,root,root,-)
%{python_sitearch}/gridfs

%files -n python-bson
%defattr(-,root,root,-)
%{python_sitearch}/bson

%changelog
* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.9-1
- Update to 1.9

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.8.1-1
- Update to 1.8.1

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.1.2-1
- Initial build
