%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global snapshot dev100

Name:           django-tinymce
Version:        1.5.1
Release:        0.1.%{snapshot}%{?dist}
Summary:        A Django application that contains a widget to render a form field as a TinyMCE editor

Group:          Development/Languages
License:        MIT
URL:            http://code.google.com/p/django-tinymce/
Source0:        http://pypi.python.org/packages/source/d/django-tinymce/django-tinymce-%{version}.%{snapshot}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
A Django application that contains a widget to render a form field as a TinyMCE editor.

Use the TinyMCE editor for your form textareas.

Features:

  * Use as a form widget or with a view.
  * Enhanced support for content languages.
  * Integration with the TinyMCE spellchecker.
  * Enables predefined link and image lists for dialogs.
  * Can compress the TinyMCE javascript files.
  * Integration with django-filebrowser.

%prep
%setup -q -n %{name}-%{version}.%{snapshot}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove testtinymce
rm -fr %{buildroot}%{python_sitelib}/testtinymce

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%{python_sitelib}/tinymce
%{python_sitelib}/django_tinymce-%{version}.*.egg-info

%changelog
* Thu Sep 30 2010 Silas Sewell <silas@sewell.ch> - 1.5.1-0.1.dev100
- Initial build
