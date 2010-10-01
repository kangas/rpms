%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global snapshot r292

Name:             openstack-nova
Version:          0.9.1
Release:          1%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/nova
Source0:          nova-%{version}.%{snapshot}.tar.bz2
Patch0:           %{name}-%{version}.r292.patch
BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools

%description
Nove here.

%prep
%setup -q -n nova-%{version}.%{snapshot}
%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%files
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{python_sitelib}/nova
%{python_sitelib}/nova/*.py*

%changelog
* Sat Sep 25 2010 Silas Sewell <silas@sewell.ch> - 0.9.1.292-1
- Initial build
