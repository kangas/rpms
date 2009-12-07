%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global pre_release pre7

Name:           lamson
Version:        1.0
Release:        0.3.%{pre_release}%{?dist}
Summary:        A Python mail server framework

Group:          Development/Languages
License:        GPLv3
URL:            http://lamsonproject.org
Source0:        http://pypi.python.org/packages/source/l/lamson/%{name}-%{version}%{pre_release}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-chardet
Requires:       python-daemon
Requires:       python-jinja2
# python-lockfile is required until 513546 is fixed
Requires:       python-lockfile
Requires:       python-nose
Requires:       python-sqlalchemy

%description
Lamson is a pure Python SMTP server designed to create robust and complex mail
applications in the style of modern web frameworks such as Django. Unlike
traditional SMTP servers like Postfix or Sendmail, Lamson has all the features
of a web application stack (ORM, templates, routing, handlers, state machines,
Python) without needing to configure alias files, run newaliases, or juggle
tons of tiny fragile processes.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}%{pre_release}
# Fix wrong-script-end-of-line-encoding error
%{__sed} -i 's/\r//' README
# Fix lots of issues with metaphonp
metaphone='examples/librelist/lib/metaphone.py'
# Fix wrong-script-end-of-line-encoding error
%{__sed} -i 's/\r//' $metaphone
# Fix file-not-utf8 warning
iconv -f ISO_8859-1 -t UTF8 $metaphone -o $metaphone.tmp
%{__mv} -f $metaphone.tmp $metaphone
# Fix wrong-script-interpreter error
%{__sed} -i '/^#!python$/,+1 d' $metaphone
# Fix hidden-file-or-dir warnings
find doc examples -name '.*' -delete
# Fix zero-length errors
find doc examples -size 0 -delete
# Fix doc-file-dependency and spurious-executable-perm warnings
find examples -name '*.py' -exec chmod 0644 {} \;

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README
%{_bindir}/lamson
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info

%files doc
%defattr(-,root,root,-)
%doc examples/ doc/lamsonproject.org/output

%changelog
* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.3.pre7
- Update to 1.0pre7

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.2.pre6
- Update to 1.0pre6
- Add doc subpackage

* Thu Jul 23 2009 Silas Sewell <silas@sewell.ch> - 1.0-0.1.pre1
- Update to 1.0pre1

* Sat May 25 2009 Silas Sewell <silas@sewell.ch> - 0.9.0-1
- Update to 0.9.0

* Sat May 25 2009 Silas Sewell <silas@sewell.ch> - 0.8.4-1
- Update to 0.8.4

* Sat May 16 2009 Silas Sewell <silas@sewell.ch> - 0.8.3-1
- Initial package
