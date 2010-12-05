Name:           python-whoosh
Version:        1.3.3
Release:        1%{?dist}
Summary:        A fast, pure-Python full text indexing, search, and spell checking library

Group:          Development/Languages
# All code is ASL 2.0 except:
# - src/whoosh/lang/porter2.py (MIT)
# - src/whoosh/support/relativedelta.py (Python)
# - src/whoosh/support/unicode.py (UCD)
License:        ASL 2.0 and MIT and Python and UCD
URL:            http://bitbucket.org/mchaput/whoosh/wiki/Home
Source0:        http://pypi.python.org/packages/source/W/Whoosh/Whoosh-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
Whoosh is a fast, full-text indexing and searching library implemented in pure
Python. Programmers can use it to easily add search functionality to their
applications and websites. Every part of how Whoosh works can be extended or
replaced to meet your needs exactly.

Some of Whoosh's features include:

  * Pythonic API
  * Pure Python, no compilation or binary packages
  * Fielded indexing and search
  * Fast indexing and retrieval
  * Pluggable scoring algorithm, text analysis, storage, and posting format
  * Powerful query language
  * Pure Python spell-checker

%prep
%setup -q -n Whoosh-%{version}

# Fix spurious-executable-perm warnings
find . -type f -exec chmod 644 {} \;

%build
%{__python} setup.py build

%check
%{__python} setup.py test

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%{python_sitelib}/whoosh
%{python_sitelib}/Whoosh-%{version}-*egg-info

%changelog
* Sat Dec 04 2010 Silas Sewell <silas@sewell.ch> - 1.3.3-1
- Initial package
