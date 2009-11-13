Name:           libmp3splt
Version:        0.5.4
Summary:        A library to split mp3 and ogg files
Release:        1%{?dist}

Group:          Applications/Multimedia
License:        GPL
URL:            http://mp3splt.sourceforge.net
Source0:        http://prdownloads.sourceforge.net/mp3splt/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libid3tag-devel
BuildRequires:  libmad-devel
BuildRequires:  libogg-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libvorbis-devel
Requires:       libmad
Requires:       libogg
Requires:       libvorbis

%description
Mp3splt-project is a utility to split mp3 and ogg files selecting a begin and an
end time position, without decoding.

%package devel
Summary:        The libraries and header files needed for libmp3splt development.
Group:          Development/Libraries
Requires:       libmp3splt

%description devel
The libraries and header files needed for libmp3splt development.

%prep
%setup -q

%build
%configure --with-distro=redhat
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/*
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc LIMITS
%doc NEWS
%doc README
%doc TODO

%files devel
%defattr(-,root,root)
/usr/include/*

%changelog
* Wed Feb 18 2009 Silas Sewell <silas@sewell.ch> - 0.5.4-1
- Initial build
