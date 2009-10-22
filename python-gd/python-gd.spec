%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define upstream_name gdmodule

Name:           python-gd
Version:        0.56
Release:        1%{?dist}
Summary:        A Python wrapper of gd

Group:          Development/Languages
License:        BSD
URL:            http://newcenturycomputers.net/projects/gdmodule.html
Source0:        http://newcenturycomputers.net/projects/download.cgi/%{upstream_name}-%{version}.tar.gz
Patch0:         gdmodule-0.56.fix-file-test.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gd-devel >= 2.0.23
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
python-hdmodule is a Python wrapper of gd.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix filetest check
%patch0 -p1

%build
CFLAGS="%{optflags}" %{__python} Setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} Setup.py install -O1 --skip-build --root %{buildroot}
# Fix non-standard-executable-perm error
%{__chmod} 0755 %{buildroot}%{python_sitearch}/_gd.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/_gd.so
%{python_sitearch}/gd.*
%{python_sitearch}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Tue Sep 29 2009 Silas Sewell <silas@sewell.ch> - 0.56-1
- Initial build
