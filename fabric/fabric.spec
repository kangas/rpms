%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global package_name Fabric

Name:           fabric
Version:        0.9.2
Release:        1%{?dist}
Summary:        A simple Pythonic remote deployment tool

Group:          Applications/System
License:        BSD
URL:            http://www.fabfile.org
Source0:        http://code.fabfile.org/projects/fabric/files/%{package_name}-%{version}.tar.gz
# Upstream issue to add man page http://code.fabfile.org/issues/show/35
# wget http://github.com/adamv/fabric/raw/a7027fd810344c455ada6c31435dbb0905ad4e55/man/fab.1
Source1:        fab.1
# Fix in http://github.com/adamv/fabric/commit/4630d896ffc56696ba7083ff0d458b63928ad9e8
Patch0:         Fabric-%{version}.fix-setup-py.patch
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
%setup -q -n %{package_name}-%{version}
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -fr %{buildroot}%{python_sitelib}/paramiko
%{__install} -p -m 0644 -D %{SOURCE1} %{buildroot}%{_mandir}/man1/fab.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%{_bindir}/fab
%{python_sitelib}/fabric
%{python_sitelib}/%{package_name}*%{version}*.egg-info
%{_mandir}/man1/fab.1.gz

%changelog
* Sat Oct 09 2010 Silas Sewell <silas@sewell.ch> - 0.9.2-1
- Update to 0.9.2
- Import man page from upstream branch
- Apply upstream patch to fix incorrect requirements

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 0.9.1-1
- Update to 0.9.1
- Add man page

* Mon Nov 09 2009 Silas Sewell <silas@sewell.ch> - 0.9.0-1
- Update to 0.9.0

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
