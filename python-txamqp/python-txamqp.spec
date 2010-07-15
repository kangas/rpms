%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global with_thrift %{?_with_thrift: 1} %{?!_with_thrift: 0}

%global upstream_name txamqp

Name:           python-%{upstream_name}
Version:        0.3
Release:        1%{?dist}
Summary:        A Python library for communicating with AMQP peers and brokers using Twisted

Group:          Development/Languages
License:        ASL 2.0
URL:            https://launchpad.net/txamqp
Source0:        http://launchpad.net/txamqp/trunk/%{version}/+download/python-txamqp_%{version}.orig.tar.gz
Patch0:         python-txamqp-0.3.spec-path.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       amqp
Requires:       python-twisted-core

%description
txAMQP is a Python library for communicating with AMQP peers and brokers using
Twisted.

This project contains all the necessary code to connect, send and receive
messages to/from an AMQP-compliant peer or broker (Qpid, OpenAMQ, RabbitMQ)
using Twisted.

%if %{with_thrift}
%package        thrift
Summary:        Contributed Thrift libraries for Twisted
Group:          Development/Languages

Requires:       thrift-python

%description    thrift
txAMQP also includes support for using Thrift RPC over AMQP in Twisted
applications.
%endif

%prep
%setup -q
%patch0 -p1
# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/env python/,+1 d' src/txamqp/codec.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Remove thrift if we're not building it
%if !%{with_thrift}
rm -rf %{buildroot}%{python_sitelib}/%{upstream_name}/contrib/thrift
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/CHANGES doc/README doc/THANKS src/examples/simple
%dir %{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}/*.py*
%{python_sitelib}/%{upstream_name}/test
%dir %{python_sitelib}/%{upstream_name}/contrib
%{python_sitelib}/%{upstream_name}/contrib/*.py*
%{python_sitelib}/txAMQP-%{version}-*.egg-info

%if %{with_thrift}
%files thrift
%defattr(-,root,root,-)
%doc doc/README src/examples/thrift
%{python_sitelib}/%{upstream_name}/contrib/thrift
%endif

%changelog
* Wed Jul 14 2010 Silas Sewell <silas@sewell.ch> - 0.3-1
- Initial build
