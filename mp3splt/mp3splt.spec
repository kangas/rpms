Name:           mp3splt
Version:        2.2.3
Summary:        A utility to split mp3 and ogg files
Release:        1%{?dist}

Group:          Applications/Multimedia
License:        GPL
Source0:        http://prdownloads.sourceforge.net/mp3splt/%{name}-%{version}.tar.gz
URL:            http://mp3splt.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libmp3splt-devel >= 0.5.4
BuildRequires:  libtool-ltdl-devel
Requires:       libmp3splt >= 0.5.4

%description
Mp3splt-project is a utility to split mp3 and ogg files selecting a begin and an
end time position, without decoding.

%prep
%setup -q

%build
./configure --prefix=/usr --mandir=%{_mandir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%config %{_bindir}/mp3splt
%{_mandir}/*
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc NEWS
%doc README
%doc TODO

%changelog
* Wed Feb 18 2009 Silas Sewell <silas@sewell.ch> - 2.2.3-1
- Initial build
