%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-mutagen
Version:        1.19
Release:        1%{?dist}
Summary:        Mutagen is a Python module to handle audio metadata

Group:          Development/Languages
License:        GPLv2
URL:            http://code.google.com/p/mutagen
Source0:        http://mutagen.googlecode.com/files/mutagen-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
Mutagen is a Python module to handle audio metadata. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bitstreams.

%prep
%setup -q -n mutagen-%{version}
# Fix non-executable-script error
sed -i '/^#! \/usr\/bin\/env python/,+1 d' mutagen/__init__.py
# Fix wrong-file-end-of-line-encoding warning
sed -i 's/\r//' TUTORIAL

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
./setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc API-NOTES COPYING NEWS README TODO TUTORIAL
%{_bindir}/*
%{_mandir}/man*/*gz
%{python_sitelib}/mutagen
%{python_sitelib}/mutagen-%{version}-*.egg-info

%changelog
* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.19-1
- Update to 1.19
- Add tests

* Thu Feb 18 2010 Silas Sewell <silas@sewell.ch> - 1.18-1
- Update to 1.18

* Thu Oct 22 2009 Silas Sewell <silas@sewell.ch> - 1.17-1
- Update to 1.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Silas Sewell <silas@sewell.ch> - 1.16-1
- Update to 1.16
- New project URLs

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.15-3
- Normalize spec

* Fri Apr 10 2009 Silas Sewell <silas@sewell.ch> - 1.15-2
- Make sed safer
- Add back in removed changelogs

* Sun Mar 29 2009 Silas Sewell <silas@sewell.ch> - 1.15-1
- Update to 1.15

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.13-3
- Rebuild for Python 2.6

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-2
- Add egg-info to package

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-1
- 1.13

* Sat Aug 25 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.12-1
- Update to 1.12
- License tag fix

* Sat Apr 28 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.11-1
- Update to 1.11

* Wed Jan 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.10.1-1
- Update to 1.10.1

* Wed Dec 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.9-1
- Bump to 1.9

* Tue Dec 12 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-2
- Python 2.5 rebuild

* Sun Oct 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-1
- Bump to 1.8

* Fri Sep 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-2
- .pyo files no longer ghosted

* Fri Aug 11 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-1
- Update upstream to 1.6

* Fri Jul 21 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-5
- Some fixes in preamble.
- Change name from mutagen to python-mutagen.
- Delete CFLAGS declaration.

* Thu Jul 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-4
- Add BuildArch: noarch to preamble.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-3
- Remove python-abi dependency.
- Prep section deletes first two lines in __init__.py file due to rpmlint error.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-2
- Clean at files section.
- Fix charset in TUTORIAL file.

* Fri Jul 14 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-1
- First build.
