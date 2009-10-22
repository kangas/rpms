%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-cmd2
Version:        0.5.2
Release:        2%{?dist}
Summary:        Enhancements for Python's cmd module

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/cmd2
Source0:        http://pypi.python.org/packages/source/c/cmd2/cmd2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       pyparsing >= 1.5.1

%description
A drop-in replacement for Python's cmd which adds several features for
command-prompt tools:
 * Searchable command history (commands: "hi", "li", "run")
 * Load commands from file, save to file, edit commands in file
 * Multi-line commands
 * Case-insensitive commands
 * Special-character shortcut commands (beyond cmd's "@" and "!")
 * Settable environment parameters
 * Parsing commands with flags
 * > (filename), >> (filename) redirect output to file
 * < (filename) gets input from file
 * bare >, >>, < redirect to/from paste buffer
 * accepts abbreviated commands when unambiguous
 * py enters interactive Python console
 * test apps against sample session transcript (see example/example.py)

%prep
%setup -q -n cmd2-%{version}
# Fix spurious-executable-perm warning
chmod 0644 README.txt
# Fix wrong-script-end-of-line-encoding error
sed -i 's/\r//' README.txt

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc PKG-INFO README.txt
%{python_sitelib}/cmd2.py*
%{python_sitelib}/cmd2-%{version}-*.egg-info

%changelog
* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 0.5.2-2
- Normalize spec

* Sat Apr 11 2009 Silas Sewell <silas@sewell.ch> - 0.5.2-1
- Initial package
