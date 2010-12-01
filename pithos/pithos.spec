Name:           pithos
Version:        0.3.6
Release:        1%{?dist}
Summary:        A Pandora client for the GNOME Desktop

Group:          Applications/File
License:        GPLv3
URL:            http://kevinmehall.net/p/pithos/
# bzr branch lp:pithos pithos
# bzr update -r 148
Source0:        pithos-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  python-devel
BuildRequires:  python-distutils-extra

Requires:       dbus-python
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-good
Requires:       gstreamer-python
Requires:       notify-python
Requires:       pygobject2
Requires:       pygtk2
Requires:       pyxdg

%description
Pithos is a Pandora client for the GNOME Desktop.

%prep
%setup -q
cp %{name}.desktop.in %{name}.desktop
sed -i 's|../data/|%{_datadir}/%{name}|g' pithos/pithosconfig.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --prefix=%{buildroot}%{_prefix}

desktop-file-install --delete-original \
        --dir %{buildroot}%{_datadir}/applications \
        --add-only-show-in=GNOME \
        %{name}.desktop

%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Nov 30 2010 Silas Sewell <silas@sewell.ch> - 0.3.6
- Initial package
