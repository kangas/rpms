%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pyftpdlib
Version:        0.5.2
Release:        1%{?dist}
Summary:        Python FTP server library

Group:          Development/Languages
License:        MIT
URL:            http://code.google.com/p/pyftpdlib
Source0:        http://pyftpdlib.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Python FTP server library provides a high-level portable interface to easily
write asynchronous FTP servers with Python. Based on asyncore framework
pyftpdlib is currently the most complete RFC-959 FTP server implementation
available for Python programming language.

%prep
%setup -q
# Fix spurious-executable-perm warning
find CREDITS HISTORY LICENSE README demo/ doc/ test/ -type f -exec chmod 0644 {} \;
# Fix wrong-script-end-of-line-encoding warning
sed -i 's/\r//' CREDITS HISTORY LICENSE README demo/* doc/* test/* pyftpdlib/ftpserver.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-executable-script error
chmod 0755 %{buildroot}%{python_sitelib}/%{name}/ftpserver.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS HISTORY LICENSE README demo/ doc/ test/
%{python_sitelib}/pyftpdlib
%{python_sitelib}/pyftpdlib-%{version}-*.egg-info

%changelog
* Wed Oct 21 2009 Silas Sewell <silas@sewell.ch> - 0.5.2-1
- Update to 0.5.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Silas Sewell <silas@sewell.ch> - 0.5.1-4
- Fix various issues reported by rpmlint
- Remove INSTALL file

* Thu Mar 26 2009 Silas Sewell <silas@sewell.ch> - 0.5.1-3
- Update package name to conform to Fedora naming standards
- Remove unneeded requires
- Change define to global

* Thu Mar 12 2009 Silas Sewell <silas@sewell.ch> - 0.5.1-2
- Fix various rpmlint issues

* Tue Feb 24 2009 Silas Sewell <silas@sewell.ch> - 0.5.1-1
- Initial build
