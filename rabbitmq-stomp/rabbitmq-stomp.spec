%define debug_package %{nil}

Name:           rabbitmq-stomp
Version:        1.6.0
Release:        1%{?dist}
Summary:        A STOMP plugin for RabbitMQ

Group:          Development/Libraries
License:        MPLv1.1
URL:            http://www.rabbitmq.com
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  erlang
BuildRequires:  rabbitmq-server

Requires:       erlang
Requires:       rabbitmq-server

%description
rabbitmq-stomp is a STOMP adapter plugin for use with RabbitMQ.

%define _rabbit_erllibdir %{_libdir}/erlang/lib/rabbitmq_server-%{version}

%prep
%setup -q

%build
# The rabbitmq build needs escript, which is missing from /usr/bin in
# some versions of the erlang RPM.  See
# <https://bugzilla.redhat.com/show_bug.cgi?id=481302>
PATH="%{_libdir}/erlang/bin:$PATH" \
make RABBIT_SERVER_SOURCE_ROOT="%{_rabbit_erllibdir}" %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{_rabbit_erllibdir}/ebin
%{__mkdir} -p %{buildroot}%{_rabbit_erllibdir}/include

%{__install} -p -m 0644 ebin/rabbit_stomp.beam %{buildroot}%{_rabbit_erllibdir}/ebin/rabbit_stomp.beam
%{__install} -p -m 0644 ebin/stomp_frame.beam %{buildroot}%{_rabbit_erllibdir}/ebin/stomp_frame.beam
%{__install} -p -m 0644 include/stomp_frame.hrl %{buildroot}%{_rabbit_erllibdir}/include/stomp_frame.hrl

%files
%defattr(-,root,root,-)
%doc README NOTES
%{_rabbit_erllibdir}/ebin/rabbit_stomp.beam
%{_rabbit_erllibdir}/ebin/stomp_frame.beam
%{_rabbit_erllibdir}/include/stomp_frame.hrl

%clean
rm -rf %{buildroot}

%changelog
* Fri Sep 04 2009 Silas Sewell <silas@sewell.ch> 1.6.0-1
- Initial package
