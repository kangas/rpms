%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           httptask
Version:        0.0.1
Release:        1%{?dist}
Summary:        An HTTP interface to various job and queueing systems

Group:          Development/Languages
License:        MIT
URL:            http://github.com/silas/httptask
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-beanstalkc

%description
%{name} is a system which accepts jobs from various queueing systems on behalf
of a client and submits those jobs to specified URLs. The client must respond
with a predefined header or httptask will assume the job failed and resubmit
it.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-*.egg-info

%changelog
* Wed Dec 02 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
