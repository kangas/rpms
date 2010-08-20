%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           tyrionhub-ejabberd
Version:        0.0.1
Release:        1%{?dist}
Summary:        TyrionHub integration with ejabberd

Group:          Applications/System
License:        BSD
URL:            http://github.com/tidg/tyrionhub-ejabberd
Source0:        http://github.com/downloads/tidg/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.logrotate
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  ejabberd
BuildRequires:  python-devel
BuildRequires:  python-twisted-core
Requires:       ejabberd
Requires:       python-twisted-core

%description
tyrionhub-ejabberd is a Twisted-based Python application which allows ejabberd
to authenticate against TyrionHub.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Non-Python stuff
install -p -D -m 644 config/%{name} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -D -m 755 scripts/%{name} %{buildroot}%{_sbindir}/%{name}
install -p -m 755 -d %{buildroot}%{_localstatedir}/log/%{name}
install -p -m 755 -d %{buildroot}%{_localstatedir}/run/%{name}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 doc/tyrionhub-ejabberd.8 %{buildroot}%{_mandir}/man8/tyrionhub-ejabberd.8

%clean
rm -rf %{buildroot}

%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS LICENSE NOTICE README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,ejabberd,ejabberd) %{_localstatedir}/log/%{name}
%attr(0755,ejabberd,ejabberd) %{_localstatedir}/run/%{name}
%{_mandir}/man8/tyrionhub-ejabberd.8*
%{_sbindir}/%{name}
%{python_sitelib}/tyrionhub_ejabberd
%{python_sitelib}/tyrionhub_ejabberd-%{version}-*.egg-info
%{python_sitelib}/twisted/plugins/tyrionhub_ejabberd_plugin.py*
# We don't want to generate dropin.cache in the Twisted plugin directory
%ghost %{python_sitelib}/twisted/plugins/dropin.cache

%changelog
* Thu Aug 19 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
