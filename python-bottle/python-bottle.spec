Name:           python-bottle
Version:        0.8.5
Release:        1%{?dist}
Summary:        A fast, simple and lightweight WSGI micro web-framework

Group:          Development/Languages
License:        MIT
URL:            http://bottle.paws.de
Source0:        http://pypi.python.org/packages/source/b/bottle/bottle-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-mako
BuildRequires:  python-jinja2

%description
Bottle is a fast, simple and lightweight WSGI micro web-framework for Python.
It is distributed as a single file module and has no dependencies other than
the Python Standard Library.

 * Routing: Requests to function-call mapping with support for clean and dynamic
   URLs.
 * Templates: Fast and Pythonic built-in template engine and support for mako,
   jinja2 and cheetah templates.
 * Utilities: Convenient access to form data, file uploads, cookies, headers and
   other HTTP related metadata.
 * Server: Built-in HTTP development server and support for paste, fapws3,
   Google App Engine, CherryPy or any other WSGI capable HTTP server.

%prep
%setup -q -n bottle-%{version}

%build
%{__python} setup.py build

%check
%{__python} test/testall.py

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/bottle.py*
%{python_sitelib}/bottle-%{version}-*egg-info

%changelog
* Tue Dec 14 2010 Silas Sewell <silas@sewell.ch> - 0.8.5-1
- Initial package
