# TODO: how to run test suite now?
#
# Conditional build:
%bcond_with	tests	# unit tests

%define		module	numpy
Summary:	Python 3.x numerical facilities
Summary(pl.UTF-8):	Moduły do obliczeń numerycznych dla języka Python 3.x
Name:		python3-%{module}
Version:	2.2.3
Release:	2
Epoch:		1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/numpy/numpy/releases/
Source0:	https://github.com/numpy/numpy/releases/download/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	c6ee254bcdf1e2fdb13d87e0ee4166ba
URL:		https://github.com/numpy/numpy
%if "%(test -w /dev/shm ; echo $?)" != "0"
BuildRequires:	WRITABLE(/dev/shm)
%endif
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel >= 3.1.1-2
BuildRequires:	python3-Cython >= 0.29.30
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-meson-python
%if %{with tests}
BuildRequires:	python3-hypothesis >= 6.24.1
#BuildRequires:	python3-mypy >= 0.940
BuildRequires:	python3-pytest >= 6.2.5
BuildRequires:	python3-pytz >= 2024.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-libs >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NumPy is a collection of extension modules to provide high-performance
multidimensional numeric arrays to the Python programming language.

This package contains Python 3 modules.

%description -l pl.UTF-8
NumPy to zbiór modułów rozszerzeń zapewniających wydajne obliczenia
numeryczne na macierzach wielowymiarowych w języku Python.

Ten pakiet zawiera moduły Pythona 3.

%package devel
Summary:	C header files for Python 3 numerical modules
Summary(pl.UTF-8):	Pliki nagłówkowe języka C modułów numerycznych Pythona 3
Group:		Development/Languages/Python
%pyrequires_eq	python3-devel
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
C header files for Python 3 numerical modules.

%description devel -l pl.UTF-8
Pliki nagłówkowe języka C modułów numerycznych Pythona 3.

%package -n f2py3
Summary:	Fortran to Python 3 interface generator
Summary(pl.UTF-8):	Generator interfejsów z Fortranu do Pythona 3
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n f2py3
Fortran to Python 3 interface generator.

%description -n f2py3 -l pl.UTF-8
Generator interfejsów z Fortranu do Pythona 3.

%prep
%setup -q -n %{module}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
%{__sed} -i -e '1s,^#!.*python3,#!%{__python3},' numpy/testing/print_coercion_tables.py

%build
%py3_build_pyproject

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} runtests.py --mode=full
%endif

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/doc
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/random/_examples
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/random/LICENSE.md

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt THANKS.txt
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.pyi
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/_core
%{py3_sitedir}/%{module}/_core/*.py
%{py3_sitedir}/%{module}/_core/*.pyi
%{py3_sitedir}/%{module}/_core/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/_core/*.cpython-3*.so
%{py3_sitedir}/%{module}/_pyinstaller
%{py3_sitedir}/%{module}/_typing
%{py3_sitedir}/%{module}/_utils
%{py3_sitedir}/%{module}/char
%{py3_sitedir}/%{module}/compat
%{py3_sitedir}/%{module}/core
%dir %{py3_sitedir}/%{module}/fft
%{py3_sitedir}/%{module}/fft/*.py
%{py3_sitedir}/%{module}/fft/*.pyi
%{py3_sitedir}/%{module}/fft/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/fft/*.cpython-3*.so
%{py3_sitedir}/%{module}/lib
%dir %{py3_sitedir}/%{module}/linalg
%{py3_sitedir}/%{module}/linalg/*.py
%{py3_sitedir}/%{module}/linalg/*.pyi
%{py3_sitedir}/%{module}/linalg/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/linalg/*.cpython-3*.so
%{py3_sitedir}/%{module}/ma
%{py3_sitedir}/%{module}/matrixlib
%{py3_sitedir}/%{module}/polynomial
%dir %{py3_sitedir}/%{module}/random
%{py3_sitedir}/%{module}/random/*.py
%{py3_sitedir}/%{module}/random/*.pyi
%{py3_sitedir}/%{module}/random/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/random/*.cpython-3*.so
%{py3_sitedir}/%{module}/testing
%{py3_sitedir}/%{module}/rec
%{py3_sitedir}/%{module}/strings
%{py3_sitedir}/%{module}/typing
%{py3_sitedir}/numpy-%{version}.dist-info

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/numpy-config
%{py3_sitedir}/%{module}/*.pxd
%{py3_sitedir}/%{module}/_core/include
%{py3_sitedir}/%{module}/_core/lib
%{py3_sitedir}/%{module}/_core/tests
%{py3_sitedir}/%{module}/fft/tests
%{py3_sitedir}/%{module}/linalg/tests
%{py3_sitedir}/%{module}/random/*.pxd
%{py3_sitedir}/%{module}/random/lib
%{py3_sitedir}/%{module}/random/tests
%{py3_sitedir}/%{module}/tests

%files -n f2py3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/f2py
%{py3_sitedir}/%{module}/f2py
