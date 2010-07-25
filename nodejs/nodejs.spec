Name:           nodejs
Version:        0.1.101
Release:        1%{?dist}
Summary:        An evented I/O framework for V8 JavaScript

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org
# wget http://github.com/ry/node/tarball/v%{version}
# tar -xzf ry-node-v%{version}-0-*.tar.gz
# rm ry-node-v%{version}-0-*.tar.gz
# mv ry-node-* %{name}-%{version}
# tar -cjf %{name}-%{version}.tar.bz2 %{name}-%{version}/
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  waf

%description
Node is an evented I/O framework for the V8 JavaScript engine.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
Node is an evented I/O framework for the V8 JavaScript engine.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
./configure --prefix=%{buildroot}/%{_prefix}
sed -i 's|@PREFIX@|%{_prefix}|g' ./src/node_config.h.in
%{__make}

%install
rm -rf %{buildroot}
%{__make} install
# Remove unused files
rm %{buildroot}%{_bindir}/node-waf
rm -fr %{buildroot}%{_prefix}/lib/node/wafadmin
# Fix install root on x86_64
mv %{buildroot}%{_prefix}/lib/node %{buildroot}/%{_libdir} || true

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README
%{_bindir}/node
%{_bindir}/node-repl

%files devel
%defattr(-,root,root,-)
%{_includedir}/node

%changelog
* Sun Jul 25 2010 Silas Sewell <silas@sewell.ch> - 0.1.101-1
- Initial build
