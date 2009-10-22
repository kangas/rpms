Name:           indefero
Version:        0.8.2
Release:        1%{?dist}
Summary:        A code, issue and documentation tracking system

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.indefero.net
Source0:        http://projects.ceondo.com/media/upload/indefero/files/%{name}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       httpd
Requires:       php >= 5
Requires:       php-mysql

%description
InDefero is a software forge which allows users to manage the life cycle of
software with integration of the code, issues, code review and documentation.

%prep
%setup -q

%install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
install -m 0644 -D -p %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf
cp -pr * ${RPM_BUILD_ROOT}%{_datadir}/%{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc license.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}/*
%{_sysconfdir}/%{name}/*

%changelog
* Wed Apr 01 2009 Silas Sewell <silas at sewell ch> - 0.8.2-1
- Initial commit
