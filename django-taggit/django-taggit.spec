Name:           django-taggit
Version:        0.9.1
Release:        1%{?dist}
Summary:        A reusable Django application for simple tagging

Group:          Development/Languages
License:        BSD
URL:            https://github.com/alex/django-taggit
Source0:        http://pypi.python.org/packages/source/d/django-taggit/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       Django >= 1.1

%description
django-taggit a simpler approach to tagging with Django. Add "taggit" to your
INSTALLED_APPS then just add a TaggableManager to your model.

Tags will show up for you automatically in forms and the admin.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/taggit
%{python_sitelib}/django_taggit-%{version}-py*.egg-info

%changelog
* Sat Dec 18 2010 Silas Sewell <silas@sewell.ch> - 0.9.1-1
- Initial build
