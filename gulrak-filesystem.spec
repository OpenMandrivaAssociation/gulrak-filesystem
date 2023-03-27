# No compiled binaries are installed, so this would be empty.
%global debug_package %{nil}

%define major 2
%define devname %mklibname %{name} -d
%define libname %mklibname %{name} %major

# FIXME: clang fails:
# ... examples/dir.cpp:1:10: fatal error: 'chrono' file not found
# #include <chrono>
#           ^~~~~~~~
%bcond_with examples
# FIXME: it still requires catch2 v2
%bcond_with tests

Summary:	An implementation of C++17 std::filesystem for C++11 /C++14/C++17/C++20
Name:		gulrak-filesystem
Version:	1.5.14
Release:	1
License:	MIT
URL:		https://github.com/gulrak/filesystem
Source0:	https://github.com/gulrak/filesystem/archive/v%{version}/filesystem-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
%if %{with tests}
BuildRequires:  pkgconfig(catch2)
%endif

%description
This is a header-only single-file std::filesystem compatible helper library,
based on the C++17 and C++20 specs, but implemented for C++11, C++14, C++17 or
C++20 (tightly following  the C++17 standard with very few documented exceptions).
It is currently tested on macOS 10.12/10.14/10.15/11.6, Windows 10, Ubuntu 18.04,
Ubuntu 20.04, CentOS 7, CentOS 8, FreeBSD 12, Alpine ARM/ARM64 Linux and Solaris
10 but should work on other systems too, as long as you have at least a C++11
compatible compiler. It should work with Android NDK, Emscripten and I even had
reports of it being used on iOS (within sandboxing constraints) and with v1.5.6
there is experimental support for QNX. The support of Android NDK, Emscripten and
QNX is not backed up by automated testing but PRs and bug reports are welcome for
those too. It is of course in its own namespace `ghc::filesystem` to not interfere
with a regular std::filesystem should you use it in a mixed C++17 environment
(which is possible).

#----------------------------------------------------------------------------

%package devel
Summary:	An header only implementation of C++17 std::filesystem for C++11 /C++14/C++17/C++20

%description devel
This is a header-only single-file std::filesystem compatible helper library,
based on the C++17 and C++20 specs, but implemented for C++11, C++14, C++17 or
C++20 (tightly following  the C++17 standard with very few documented exceptions).
It is currently tested on macOS 10.12/10.14/10.15/11.6, Windows 10, Ubuntu 18.04,
Ubuntu 20.04, CentOS 7, CentOS 8, FreeBSD 12, Alpine ARM/ARM64 Linux and Solaris
10 but should work on other systems too, as long as you have at least a C++11
compatible compiler. It should work with Android NDK, Emscripten and I even had
reports of it being used on iOS (within sandboxing constraints) and with v1.5.6
there is experimental support for QNX. The support of Android NDK, Emscripten and
QNX is not backed up by automated testing but PRs and bug reports are welcome for
those too. It is of course in its own namespace `ghc::filesystem` to not interfere
with a regular std::filesystem should you use it in a mixed C++17 environment
(which is possible).

%files devel
%license LICENSE
%doc README.md
%doc examples
%{_includedir}/ghc
%{_libdir}/cmake/ghc_filesystem

#----------------------------------------------------------------------------

%prep
%autosetup -n filesystem-%{version}

# Remove bundled Catch library and use the system version
%if %{with tests}
rm -vf test/catch.hpp
sed -r -i 's|(include[[:blank:]]+")(catch.hpp")|\1catch2/\2|' test/*.cpp
sed -r -i 's|[[:blank:]]+catch\.hpp||' test/CMakeLists.txt
%endif

sed -i -e "s|<chrono>|<bits/chrono>|g" examples/dir.cpp

%build
%cmake \
	-DGHC_FILESYSTEM_BUILD_EXAMPLES:BOOL=%{?with_examples:ON}%{?!with_examples:OFF} \
	-DGHC_FILESYSTEM_BUILD_TESTING:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-DGHC_FILESYSTEM_WITH_INSTALL:BOOL=ON \
	-G Ninja
pwd
%ninja_build

%install
%ninja_install -C build

