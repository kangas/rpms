%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name riak

Name:           python-%{upstream_name}
Version:        0.0.1
Release:        1%{?dist}
Summary:        A Riak Python client

Group:          Development/Languages
License:        ASL 2.0
URL:            https://bitbucket.org/basho/riak-python-client
# hg clone http://bitbucket.org/basho/riak-python-client python-riak-%{version}
# rm -fr python-riak-%{version}/.hg
# tar -czf python-riak-%{version}.tar.gz python-riak-%{version}/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  protobuf-compiler
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       protobuf-python
Requires:       python-pycurl

%description
Riak is a Dynamo-inspired key/value store that scales predictably and easily.

This is a Python interface to Riak.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Thu Apr 21 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
