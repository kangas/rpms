%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           funcshell
Version:        0.1
Release:        1%{?dist}
Summary:        A shell interface to Func

Group:          Applications/System
License:        MIT
URL:            http://www.silassewell.com/projects/funcshell
Source0:        http://cloud.github.com/downloads/silas/funcshell/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       func
Requires:       python-cly

%description
funchshell is a shell interface to Func.

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
%doc LICENSE
%{_bindir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-*.egg-info

%changelog
* Fri Dec 11 2009 Silas Sewell <silas@sewell.ch> - 0.1-1
- Update to 0.1
- Add async support

* Tue May 26 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-2
- Update setup.py to use setuptools

* Sun Apr 26 2009 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
