#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	numpy
Summary:	Python 3.x numerical facilities
Summary(pl.UTF-8):	Moduły do obliczeń numerycznych dla języka Python 3.x
Name:		python3-%{module}
Version:	1.19.4
Release:	3
Epoch:		1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/numpy/numpy/releases/
Source0:	https://github.com/numpy/numpy/releases/download/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	a25e91ea62ffd37ccf8e0d917484962c
URL:		http://sourceforge.net/projects/numpy/
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel >= 3.1.1-2
BuildRequires:	python3-Cython >= 0.29.21
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-libs >= 1:3.6
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
%pyrequires_eq	python-devel
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

%build
# numpy.distutils uses CFLAGS/LDFLAGS as its own flags replacements,
# instead of appending proper options (like -fPIC/-shared resp.)
CFLAGS="%{rpmcflags} -fPIC"
LDFLAGS="%{rpmldflags} -shared"

%py3_build

%if %{with tests}
%{__python3} runtests.py --mode=full
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/doc
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/random/_examples
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/*/tests
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/LICENSE.txt

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/distutils/mingw/gfortran_vs2003_hack.c

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt THANKS.txt
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/compat
%{py3_sitedir}/%{module}/compat/*.py
%{py3_sitedir}/%{module}/compat/__pycache__
%dir %{py3_sitedir}/%{module}/core
%{py3_sitedir}/%{module}/core/*.py
%{py3_sitedir}/%{module}/core/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/core/*.cpython-3*.so
%dir %{py3_sitedir}/%{module}/distutils
%{py3_sitedir}/%{module}/distutils/*.py
%{py3_sitedir}/%{module}/distutils/__pycache__
%dir %{py3_sitedir}/%{module}/distutils/command
%{py3_sitedir}/%{module}/distutils/command/*.py
%{py3_sitedir}/%{module}/distutils/command/__pycache__
%dir %{py3_sitedir}/%{module}/distutils/fcompiler
%{py3_sitedir}/%{module}/distutils/fcompiler/*.py
%{py3_sitedir}/%{module}/distutils/fcompiler/__pycache__
%dir %{py3_sitedir}/%{module}/fft
%{py3_sitedir}/%{module}/fft/*.py
%{py3_sitedir}/%{module}/fft/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/fft/_pocketfft_internal.cpython-3*.so
%dir %{py3_sitedir}/%{module}/lib
%{py3_sitedir}/%{module}/lib/*.py
%{py3_sitedir}/%{module}/lib/__pycache__
%dir %{py3_sitedir}/%{module}/linalg
%{py3_sitedir}/%{module}/linalg/*.py
%{py3_sitedir}/%{module}/linalg/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/linalg/_umath_linalg.cpython-3*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/linalg/lapack_lite.cpython-3*.so
%dir %{py3_sitedir}/%{module}/ma
%{py3_sitedir}/%{module}/ma/*.py
%{py3_sitedir}/%{module}/ma/__pycache__
%dir %{py3_sitedir}/%{module}/matrixlib
%{py3_sitedir}/%{module}/matrixlib/*.py
%{py3_sitedir}/%{module}/matrixlib/__pycache__
%dir %{py3_sitedir}/%{module}/polynomial
%{py3_sitedir}/%{module}/polynomial/*.py
%{py3_sitedir}/%{module}/polynomial/__pycache__
%dir %{py3_sitedir}/%{module}/random
%{py3_sitedir}/%{module}/random/*.py
%{py3_sitedir}/%{module}/random/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/random/*.cpython-3*.so
%dir %{py3_sitedir}/%{module}/testing
%{py3_sitedir}/%{module}/testing/_private
%{py3_sitedir}/%{module}/testing/*.py
%{py3_sitedir}/%{module}/testing/__pycache__
%{py3_sitedir}/numpy-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{py3_sitedir}/%{module}/*.pxd
%{py3_sitedir}/%{module}/core/include
%{py3_sitedir}/%{module}/core/lib
%{py3_sitedir}/%{module}/random/*.pxd
%{py3_sitedir}/%{module}/random/lib

%files -n f2py3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/f2py3
%attr(755,root,root) %{_bindir}/f2py%{py3_ver}
%dir %{py3_sitedir}/%{module}/f2py
%{py3_sitedir}/%{module}/f2py/*.py
%{py3_sitedir}/%{module}/f2py/__pycache__
%{py3_sitedir}/%{module}/f2py/src
