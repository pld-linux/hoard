%define		ver	%(echo %{version} | tr -d .)
Summary:	A fast, scalable, and memory-efficient memory allocator
Name:		hoard
Version:	3.8
Release:	1
License:	GPL
Group:		Libraries
URL:		http://www.hoard.org/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Source0:	http://www.cs.umass.edu/~emery/hoard/hoard-%{version}/source/%{name}-%{ver}.tar.gz
# Source0-md5:	f2d8ec3a13d4d9ba7b1c48c777707ef5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Hoard memory allocator is a fast, scalable, and memory-efficient
memory allocator. It runs on a variety of platforms, including Linux,
Solaris, and Windows. Hoard is a drop-in replacement for malloc() that
can dramatically improve application performance, especially for
multithreaded programs running on multiprocessors. No change to your
source is necessary. Just link it in or set just one environment
variable, e.g.:

LD_PRELOAD=%{_libdir}/libhoard.so:%{_libdir}/libdl.so

%prep
%setup -q -n %{name}-%{ver}
sed -i -e '
	s/-O/-fPIC -O/g;
	s/-static//g;
	s/-pipe//g;
	s/-march=pentiumpro //g;
	s/ -malign-double//g;
	s/g++/$(CXX)/;
	s/-O3/$(CXXFLAGS)/;
' src/Makefile

%build
%{__make} -C src generic-gcc \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -p src/libhoard.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc NEWS README THANKS
%{_libdir}/libhoard.so
