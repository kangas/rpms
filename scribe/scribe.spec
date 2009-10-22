%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             scribe
Version:          2.01
Release:          1%{?dist}
Summary:          A server for aggregating log data streamed in real time

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://developers.facebook.com/scribe
Source0:          http://dl.sourceforge.net/sourceforge/scribeserver/%{name}-version-%{version}.tar.gz
Source1:          scribed.init
Source2:          scribed.sysconfig
Patch0:           scribe.2.01.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    automake
BuildRequires:    boost-devel
BuildRequires:    boost-devel >= 1.33
BuildRequires:    fb303-devel
BuildRequires:    libevent-devel
BuildRequires:    thrift
BuildRequires:    thrift-cpp-devel

Requires:         %{name}-python
Requires:         fb303
Requires(post):   chkconfig

%description
Scribe is a server for aggregating log data streamed in real time from a large
number of servers. It is designed to be scalable, extensible without
client-side modification, and robust to failure of the network or any specific
machine.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel
Requires:         fb303-python

%description python
Python bindings for %{name}.

%prep
%setup -q -n %{name}

# Make scribe work with Boost 1.33
%patch0 -p1

# Remove subversion directories
find . -type d -name .svn | xargs rm -fr

%build
%define configoptions --disable-static --with-thriftpath=%{_prefix} --with-fb303path=%{_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem
./bootstrap.sh %{configoptions}
%configure %{configoptions}
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

# Install manually
install -D -m 755 ./src/libscribe.so %{buildroot}%{_libdir}/libscribe.so
install -D -m 755 ./examples/scribe_cat %{buildroot}%{_bindir}/scribe_cat
install -D -m 755 ./examples/scribe_ctrl %{buildroot}%{_sbindir}/scribe_ctrl
install -D -m 644 ./examples/example1.conf %{buildroot}%{_sysconfdir}/scribed/default.conf
install -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/scribed
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/scribed

# Clean and fixes
rm ./examples/scribe_*
mv %{buildroot}%{_bindir}/scribed %{buildroot}%{_sbindir}/scribed
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.BUILD examples/
%config(noreplace) %{_sysconfdir}/scribed/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/scribed
%{_sysconfdir}/rc.d/init.d/scribed
%{_sbindir}/scribed
%{_sbindir}/scribe_ctrl

%{_libdir}/*.so

%files python
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info
%{_bindir}/scribe_cat

%post
/sbin/chkconfig --add scribed

%preun
if [ $1 = 0 ]; then
  /sbin/service scribed stop > /dev/null 2>&1
  /sbin/chkconfig --del scribed
fi

%changelog
* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Initial build
