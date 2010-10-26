%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name mox

Name:           python-%{upstream_name}
Version:        0.5.3
Release:        2%{?dist}
Summary:        Mock object framework

Group:          Development/Languages
License:        ASL 2.0
URL:            http://code.google.com/p/pymox
Source0:        http://pypi.python.org/packages/source/m/mox/mox-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Mox is a mock object framework for Python based on the Java mock object
framework EasyMock.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' mox.py
sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' stubout.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
%{__python} mox_test.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{python_sitelib}/%{upstream_name}.py*
%{python_sitelib}/stubout.py*
%{python_sitelib}/%{upstream_name}-%{version}*.egg-info

%changelog
* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 0.5.3-2
- Fix various issues relating to review (shebangs, url, etc..)

* Wed Oct 13 2010 Silas Sewell <silas@sewell.ch> - 0.5.3-1
- Initial package
