%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name gnupg

Name:             php-pecl-%{pecl_name}
Version:          1.3.1
Release:          1%{?dist}
Summary:          A gpgme wrapper

Group:            Development/Languages
License:          PHP
URL:              http://pecl.php.net/package/%{pecl_name}
Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    chrpath
BuildRequires:    gpgme-devel
BuildRequires:    libgpg-error
BuildRequires:    php-devel
BuildRequires:    php-pear

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}
Requires:         php-common
Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
Provides:         php-pecl(%{pecl_name}) = %{version}-%{release}

%description
php-pecl-gnupgp is wrapper around the gpgme library.

%prep 
%setup -q -n %{pecl_name}-%{version}

%build
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} INSTALL_ROOT=%{buildroot} install
# Create ini
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF
# Fix rpath
chrpath --delete %{buildroot}%{php_extdir}/gnupg.so

%clean
%{__rm} -rf %{buildroot}

%if 0%{?pecl_install:1}
%post
  %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif

%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
  %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%changelog
* Fri Jul 24 2009 Silas Sewell <silas@sewell.ch> - 1.3.1-1
- Initial build
