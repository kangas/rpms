%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             rabbitmq-c
Version:          0.0.0
Release:          1%{?dist}
Summary:          RabbitMQ C client

Group:            Development/Libraries
License:          MPLv1.1
URL:              http://hg.rabbitmq.com/rabbitmq-c
# hg clone http://hg.rabbitmq.com/rabbitmq-c rabbitmq-c-0.0.0
# hg clone http://hg.rabbitmq.com/rabbitmq-codegen rabbitmq-c-0.0.0/codegen
# tar -czf rabbitmq-c-0.0.0.tar.gz rabbitmq-c-0.0.0/
Source0:          rabbitmq-c-%{version}.tar.gz
Patch0:           rabbitmq-c-0.0.0-python.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    autoconf
BuildRequires:    libtool
BuildRequires:    python

%description
A RabbitMQ C client.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
Tokyo Tyrant is a network interface to Tokyo Cabinet.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
# Fix python name (python2.5 => python)
%patch0 -p1

%build
autoreconf -i
%configure
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
# Remove misc files
%{__rm} -f %{buildroot}%{_libdir}/librabbitmq.a
%{__rm} -f %{buildroot}%{_libdir}/librabbitmq.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/amqp_*
%{_libdir}/librabbitmq.so.*

%files devel
%doc TODO
%{_includedir}/amqp*.h
%{_libdir}/librabbitmq.so

%changelog
* Wed Aug 19 2009 Silas Sewell <silas@sewell.ch> - 0.0.0-1
- Initial build
