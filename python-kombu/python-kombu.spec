%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global upstream_name kombu

Name:           python-%{upstream_name}
Version:        0.1.0
Release:        1%{?dist}
Summary:        An AMQP Messaging Framework for Python

Group:          Development/Languages
License:        BSD
URL:            http://github.com/ask/kombu
# wget http://github.com/ask/kombu/tarball/v%{version}
# tar -xzf ask-kombu-v%{version}-*.tar.gz
# rm ask-kombu-v%{version}-*.tar.gz
# mv ask-kombu-* %{name}-%{version}
# tar -cjf %{name}-%{version}.tar.bz2 %{name}-%{version}/
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-setuptools

Requires:       python-amqplib
Requires:       python-anyjson

%description
kombu is an AMQP messaging queue framework. AMQP is the Advanced Message Queuing
Protocol, an open standard protocol for message orientation, queuing, routing,
reliability and security.

The aim of kombu is to make messaging in Python as easy as possible by providing
a high-level interface for producing and consuming messages. At the same time it
is a goal to re-use what is already available as much as possible.

%prep
%setup -q
%{__sed} -i '/^#!\/usr\/bin\/python/,+1 d' kombu/tests/test_serialization.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS FAQ LICENSE README.rst
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Sun Aug 15 2010 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial build
