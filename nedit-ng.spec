Name:		nedit-ng
Version:	2018.13
Release:	1%{?dist}
Summary:	a Qt5 port of the NEdit using modern c++14

Group:		Applications/Editors
License:	GPLv2
URL:		https://github.com/eteran/nedit-ng
Source0:	https://github.com/eteran/nedit-ng/archive/%{version}.tar.gz
# From https://build.opensuse.org/package/view_file/editors/nedit-ng/nedit-ng.desktop?expand=1
Source1:	nedit-ng.desktop

BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	boost-devel
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	desktop-file-utils

%description
nedit-ng is a Qt port of the Nirvana Editor (NEdit) version 5.6. It is intended to be a drop in replacement for nedit in every practical way, just as on many systems /usr/bin/vi is now a symlink to /usr/bin/vim.

Because it is a true port of the original code, it (at least for now) inherits some (but not all) of the limitations of the original. On the other hand, some aspects have been improved simply by the fact that it is now a Qt application.

%prep
%autosetup


%build
# The -DBUILD_SHARED_LIBS:BOOL=OFF is necessary to avoid:
# CMake Error: The inter-target dependency graph contains the following strongly connected component (cycle):
#   "Util" of type SHARED_LIBRARY
#     depends on "Regex" (weak)
#   "Regex" of type SHARED_LIBRARY
#     depends on "Util" (weak)
# At least one of these targets is not a STATIC_LIBRARY.  Cyclic dependencies are allowed only among static libraries.
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF .
%make_build


%install
%make_install
install -D -m0644 src/res/nedit.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--add-category "Development;" \
	%{SOURCE1}

%check
ctest -V %{?_smp_mflags}

%files
/usr/bin/nc-ng
/usr/bin/nedit-import
/usr/bin/nedit-ng
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%doc LICENSE.md README.md


%changelog
* Wed Nov 21 2018 Mike DePaulo <mikedep333@gmail.com> - 2018.13-1
- Initial version for Fedora


