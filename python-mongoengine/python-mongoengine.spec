%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name mongoengine

Name:           python-%{upstream_name}
Version:        0.4
Release:        1%{?dist}
Summary:        An object-document mapper to connect Python and MongoDB

Group:          Development/Languages
License:        MIT
URL:            http://mongoengine.org
Source0:        http://pypi.python.org/packages/source/m/mongoengine/mongoengine-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       pymongo
Requires:       pymongo-gridfs

%description
MongoEngine is a Document-Object Mapper (think ORM, but for document databases)
for working with MongoDB from Python. It uses a simple declarative API, similar
to the Django ORM.

%package django
Summary:        MongoEngine Django libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       Django

%description django
Libraries for using MongoEngine with Django.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove tests from global namespace
rm -fr %{buildroot}%{python_sitelib}/tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%dir %{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}/*.py*
%{python_sitelib}/%{upstream_name}-%{version}-*egg-info

%files django
%{python_sitelib}/%{upstream_name}/django

%changelog
* Tue Oct 19 2010 Silas Sewell <silas@sewell.ch> - 0.4-1
- Initial package
