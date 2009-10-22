# Erlang
%global erlangdir %{_libdir}/erlang

# Haskell
%{!?ghc_version: %global ghc_version 6.10.1}
%global pkg_name Thrift

%bcond_without doc
%bcond_without prof

# Python
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Ruby
%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%define global_version 0.2
%define snapshot 795861

Name:             thrift
Version:          %{global_version}
Release:          0.20090720svn%{snapshot}%{?dist}
Summary:          A multi-language RPC and serialization framework

Group:            System Environment/Libraries
License:          ASL 2.0
URL:              http://incubator.apache.org/thrift
# svn export http://svn.apache.org/repos/asf/incubator/thrift/trunk -r %{snapshot} thrift-%{version}
# tar -czf thrift-%{version}.tar.gz thrift-%{version}/
Source0:          %{name}-%{version}.tar.gz
Source1:          thrift_protocol.ini
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    byacc
BuildRequires:    boost-devel >= 1.33.1
BuildRequires:    flex
BuildRequires:    libevent-devel
BuildRequires:    libtool
BuildRequires:    mono-devel >= 1.2.6
BuildRequires:    zlib-devel

%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Objective C/Cocoa, Smalltalk, Erlang,
Objective Caml, and Haskell.

%package cpp
Summary:          Libraries for %{name}
Group:            Development/Libraries

%description cpp
Libraries bindings for %{name}.

%package cpp-devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name}-cpp = %{version}-%{release}

%description cpp-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

#%package csharp
#Summary:          C# bindings for %{name}
#Group:            Development/Libraries
# sparc64 doesn't have mono
#ExcludeArch:      sparc64

#%description csharp
#C# bindings for %{name}.

%package erlang
Summary:          Erlang bindings for %{name}
Group:            Development/Libraries
BuildRequires:    erlang

%description erlang
Erlang bindings for %{name}.

%package ghc
Version:          0.1.0
Summary:          Haskell bindings for %{name}
Group:            Development/Libraries
Provides:         %{name}-ghc-devel = %{version}-%{release}
ExclusiveArch:    %{ix86} x86_64 ppc alpha
BuildRequires:    cabal-install
BuildRequires:    ghc
BuildRequires:    ghc-rpm-macros

%description ghc
Haskell bindings for %{name}.

%package ghc-devel
Version:          0.1.0
Summary:          Haskell %{pkg_name} library
Group:            Development/Libraries
Requires:         ghc = %{ghc_version}
Requires(post):   ghc = %{ghc_version}
Requires(preun):  ghc = %{ghc_version}

%description ghc-devel
This package contains the development files for %{name}-ghc-devel
built for ghc-%{ghc_version}.

%if %{with doc}
%package ghc-doc
Version:          0.1.0
Summary:          Documentation for %{name}-ghc
Group:            Development/Libraries
BuildRequires:    ghc-doc
Requires:         ghc-doc = %{ghc_version}
Requires(post):   ghc-doc = %{ghc_version}
Requires(postun): ghc-doc = %{ghc_version}

%description ghc-doc
This package contains development documentation files for the %{name}-ghc
library.
%endif

%if %{with prof}
%package ghc-prof
Version:          0.1.0
Summary:          Profiling libraries for %{name}-ghc
Group:            Development/Libraries
BuildRequires:    ghc-prof
Requires:         %{name}-ghc = %{version}-%{release}
Requires:         ghc-prof = %{ghc_version}

%description ghc-prof
This package contains profiling libraries for %{name}-ghc
built for ghc-%{ghc_version}.
%endif

%package java
Summary:          Java bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ant
BuildRequires:    jakarta-commons-lang
BuildRequires:    java-devel >= 1.5.0
BuildRequires:    log4j
Requires:         jakarta-commons-lang
Requires:         log4j

%description java
Java bindings for %{name}.

%package javadoc
Summary:          Javadoc for %{name}-java
Group:            Documentation
BuildRequires:    java-javadoc

%description javadoc
Javadoc for %{name}.

%package perl
Summary:          Perl bindings for %{name}
Group:            Development/Libraries
BuildRequires:    perl-devel
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:         perl(Bit::Vector)
Requires:         perl(Class::Accessor)

%description perl
Perl bindings for %{name}.

%package php
Summary:          PHP bindings for %{name}
Group:            Development/Libraries
BuildRequires:    php-devel
Requires:         php-common

%description php
PHP bindings for %{name}.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel

%description python
Python bindings for %{name}.

%package ruby
Summary:          Ruby bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ruby
BuildRequires:    ruby-devel

%description ruby
Ruby bindings for %{name}.

%prep
%setup -q

# Fix spurious-executable-perm warning
find tutorial/ -type f -exec chmod 0644 {} \;

# Haskell setup script won't run with blank or comment lines
sed -i '/#/d;/^$/d' lib/hs/Setup.lhs

%build
./bootstrap.sh
%configure --without-java --without-perl --without-ruby --enable-static=no
%{__make} %{?_smp_mflags}

# Build Haskell
pushd lib/hs
%cabal_configure --ghc %{!?without_prof:-p}
%cabal build
%cabal haddock
%ghc_gen_scripts
popd

# Build Java
pushd lib/java
ant dist javadoc -lib %{_javadir} -Dnoivy=
popd

# Build Perl
pushd lib/perl
perl Makefile.PL
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"
popd

# Build PHP
pushd lib/php/src/ext/thrift_protocol
phpize
%configure
make %{?_smp_mflags}
popd

# Build Ruby
pushd lib/rb
%{__ruby} setup.rb config
%{__ruby} setup.rb setup
popd

%install
rm -rf %{buildroot}

# Install everything not listed below
make DESTDIR=%{buildroot} install
# Remove "la" files
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/%{name}/protocol/fastbinary.so

## Install C#
#%{__mkdir_p} %{buildroot}%{_libdir}/mono/gac/
#gacutil -i lib/csharp/Thrift.dll -f -package Thrift -root %{buildroot}%{_libdir}

# Install Erlang
%{__mkdir_p} %{buildroot}%{erlangdir}/lib/%{name}-%{version}
%{__cp} -rp lib/erl/* %{buildroot}%{erlangdir}/lib/%{name}-%{version}

# Cleanup Erlang install
pushd %{buildroot}%{erlangdir}/lib/%{name}-%{version}
rm -fr Makefile README build/
popd

# Install Haskell
pushd lib/hs
%cabal_install
%ghc_install_scripts
%ghc_gen_filelists %{name}
popd

# Install Java
pushd lib/java
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -p libthrift.jar %{buildroot}%{_javadir}
%{__mkdir_p} %{buildroot}%{_javadocdir}
%{__cp} -rp build/javadoc/org/apache/thrift %{buildroot}%{_javadocdir}
popd

# Install PHP
pushd lib/php/src/ext/thrift_protocol
make INSTALL_ROOT=%{buildroot} install
popd
# Install PHP INI
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cp} %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/
# Install PHP project files
%{__mkdir_p} %{buildroot}%{_datadir}/php/%{name}
%{__cp} -r lib/php/src/Thrift.php \
           lib/php/src/protocol \
           lib/php/src/transport \
           %{buildroot}%{_datadir}/php/%{name}/

# Install Perl
pushd lib/perl
%{__make} DESTDIR=%{buildroot} INSTALLSITELIB=%{perl_vendorlib} install
popd

# Cleanup Perl install
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

# Install Ruby
pushd lib/rb
ruby setup.rb install --prefix=%{buildroot}
popd

# Fix non-standard-executable-perm error
chmod 0755 %{buildroot}%{ruby_sitearch}/thrift_native.so

%clean
rm -rf %{buildroot}

%post cpp -p /sbin/ldconfig

%postun cpp -p /sbin/ldconfig

%post ghc-devel
%ghc_register_pkg

%if %{with doc}
%post ghc-doc
%ghc_reindex_haddock
%endif

%preun ghc-devel
if [ "$1" -eq 0 ]; then
%ghc_unregister_pkg
fi

%if %{with doc}
%postun ghc-doc
if [ "$1" -eq 0 ]; then
%ghc_reindex_haddock
fi
%endif

%files
%defattr(-,root,root,-)
%doc CHANGES CONTRIBUTORS LICENSE NEWS NOTICE README doc/ tutorial/
%{_bindir}/thrift

%files cpp
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files cpp-devel
%defattr(-,root,root,-)
%doc tutorial/README tutorial/cpp tutorial/*.thrift
%{_includedir}/thrift
%{_libdir}/*.so
%{_libdir}/pkgconfig/thrift*

#%files csharp
#%defattr(-,root,root,-)
#%doc lib/csharp/README
#%{_libdir}/mono/gac/Thrift
#%{_libdir}/mono/thrift

%files erlang
%defattr(-,root,root,-)
%doc lib/erl/README tutorial/erl tutorial/*.thrift
%{erlangdir}/lib/%{name}-%{version}

%files ghc
%defattr(-,root,root,-)
%doc lib/hs/README lib/hs/TODO

%files ghc-devel -f lib/hs/thrift-devel.files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{global_version}

%if %{with doc}
%files ghc-doc
%defattr(-,root,root,-)
%ghcdocdir
%endif

%if %{with prof}
%files ghc-prof -f lib/hs/thrift-prof.files
%defattr(-,root,root,-)
%doc lib/hs/README
%endif

%files java
%defattr(-,root,root,-)
%doc lib/java/README tutorial/java tutorial/*.thrift
%{_javadir}/libthrift.jar

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/thrift

%files perl
%defattr(-,root,root,-)
%doc lib/perl/README tutorial/perl tutorial/*.thrift
%{perl_vendorlib}/Thrift*

%files php
%defattr(-,root,root,-)
%doc lib/php/README lib/php/README.apache tutorial/php tutorial/*.thrift
%config(noreplace) %{_sysconfdir}/php.d/thrift_protocol.ini
%{_datadir}/php/%{name}
%{php_extdir}/thrift_protocol.so

%files python
%defattr(-,root,root,-)
%doc lib/py/README tutorial/py tutorial/*.thrift
%{python_sitearch}/%{name}
%{python_sitearch}/Thrift-*.egg-info

%files ruby
%defattr(-,root,root,-)
%doc lib/rb/CHANGELOG lib/rb/README tutorial/rb tutorial/*.thrift
%{ruby_sitearch}/thrift_native.so
%{ruby_sitelib}/thrift*

%changelog
* Mon Jul 20 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.20090720svn795861
- Update to latest snapshot

* Mon May 25 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.20090525svn777690
- Update to latest snapshot
- Fix version, release syntax and perl requires

* Wed May 06 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.20090505svn770888
- Fix various require issues
- Change lib to cpp and devel to cpp-devel
- Use ghc version macro
- Add documentation to language specific libraries

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.20090501svn770888
- Initial build
