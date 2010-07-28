%global debug_package %{nil}
%global snapshot release.2010.07.14
%global raw_snapshot release.2010-07-14

Name:           go
Version:        0.0.0
Release:        0.1.%{snapshot}%{?dist}
Summary:        A systems programming language

Group:          Applications/System
License:        BSD
URL:            http://golang.org
# hg clone https://go.googlecode.com/hg/ go-%{version}-%{snapshot}
# pushd go-%{version}-%{snapshot}; hg checkout %{raw_snapshot}; rm -fr .hg*; popd
# tar -cjf go-%{version}-%{snapshot}.tar.bz2 go-%{version}-%{snapshot}/
Source0:        %{name}-%{version}-%{snapshot}.tar.bz2
Source1:        go-amd64.csh
Source2:        go-amd64.sh
Source3:        go-386.csh
Source4:        go-386.sh
ExclusiveArch:  i386 i586 i686 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bison
BuildRequires:  ed
BuildRequires:  gawk

%description
Go is an expressive, concurrent, garbage-collected systems programming
language.

%prep
%setup -q -n %{name}-%{version}-%{snapshot}

%build
# Do everything in install

%install
rm -rf %{buildroot}
export GOBIN="%{buildroot}%{_bindir}"
mkdir -p $GOBIN
pushd src; ./make.bash; popd
mkdir -p %{buildroot}/opt
cp -rp ../%{name}-%{version}-%{snapshot} %{buildroot}/opt/%{name}
%ifarch x86_64
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/go.csh
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/go.sh
%else
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/go.csh
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d/go.sh
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%{_bindir}
%{_sysconfdir}/profile.d/go.csh
%{_sysconfdir}/profile.d/go.sh
/opt/%{name}

%changelog
* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 0.0.0-0.1
- Initial package
