%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define pre_release b1

Name:           fabric
Version:        0.9
Release:        0.1.%{pre_release}%{?dist}
Summary:        A simple Pythonic remote deployment tool

Group:          Applications/System
License:        GPLv2+
URL:            http://www.nongnu.org/fab
Source0:        http://git.fabfile.org/cgit.cgi/fabric/snapshot/%{name}-%{version}%{pre_release}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-paramiko >= 1.7
Requires:       python-setuptools

%description
Fabric is a simple Pythonic remote deployment tool which is designed to upload
files to, and run shell commands on, a number of servers in parallel or
serially.

%prep
%setup -q -n %{name}-%{version}%{pre_release}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README TODO
%{_bindir}/fab
%{python_sitelib}/fabric
%{python_sitelib}/Fabric-*.egg-info

%changelog
* Thu Aug 27 2009 Silas Sewell <silas@sewell.ch> - 0.9-0.1.b1
- Update to latest snapshot

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.1.1-2
- Add runtime setuptools requirements
- Re-import source package

* Thu Apr 09 2009 Silas Sewell <silas@sewell.ch> - 0.1.1-1
- Update to 0.1.1
- Up Paramiko version dependency to 1.7
- Remove Python version dependency
- Make sed safer

* Sat Mar 28 2009 Silas Sewell <silas@sewell.ch> - 0.1.0-3
- Fix dependencies
- Fix non-executable-script error

* Thu Mar 26 2009 Silas Sewell <silas@sewell.ch> - 0.1.0-2
- Change define to global

* Sun Feb 22 2009 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Update to 0.1.0
- Up Python requirement to 2.5 per recommendation on official site

* Thu Nov 20 2008 Silas Sewell <silas@sewell.ch> - 0.0.9-3
- Fix changelog syntax issue

* Thu Nov 20 2008 Silas Sewell <silas@sewell.ch> - 0.0.9-2
- Fix various issues with the spec file

* Wed Nov 19 2008 Silas Sewell <silas@sewell.ch> - 0.0.9-1
- Initial package
