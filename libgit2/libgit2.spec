%global changeset 4eec2c0

Name:             libgit2
Version:          0.2.0
Release:          1%{?dist}
Summary:          A C git library

Group:            System Environment/Libraries
License:          GPLv2 with linking exception
URL:              https://github.com/libgit2/libgit2
Source0:          https://download.github.com/libgit2-libgit2-v%{version}-0-g4eec2c0.tar.gz

BuildRequires:    python
BuildRequires:    zlib-devel

%description
libgit2 is a portable, pure C implementation of the Git core methods provided
as a re-entrant linkable library with a solid API, allowing you to write native
speed custom Git applications in any language with bindings.

%prep
%setup -q -n libgit2-libgit2-%{changeset}

%build
./waf configure --prefix=%{_prefix}
./waf build-shared %{?_smp_mflags}

%check
./waf test

%install
./waf install --destdir=%{buildroot}

# Remove statically compiled file
rm -f %{buildroot}%{_libdir}/libgit2.a

%files
%defattr(-,root,root,-)
%doc COPYING README.md
%{_includedir}/git2.h
%{_includedir}/git2
%{_libdir}/libgit2.so
%{_libdir}/pkgconfig/libgit2.pc

%changelog
* Sat Jan 22 2011 Silas Sewell <silas@sewell.ch> - 2.0-1
- Initial package
