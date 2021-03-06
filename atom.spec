# BUILDING:
# https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md

Summary:	A hackable text editor for the 21st century
Name:		atom
Version:	1.2.4
Release:	0.5
License:	MIT
Group:		Applications/Editors
Source0:	https://github.com/atom/atom/releases/download/v%{version}/%{name}.x86_64.rpm
# NoSource0-md5:	2c1b984e9e2ce95449987006386463ca
# no point storing it in distfiles, this package is no ready
NoSource:	0
URL:		https://atom.io/
BuildRequires:	rpm-utils
Suggests:	apm
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_libdir}/%{name}

# internal caps not to provide
%define		int_caps	libgcrypt.so.11 libnode.so libnotify.so.4

# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_libdir}/%{name}
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			%{int_caps}
%define		_noautoreq  		%{_noautoprov}

%description
Atom is a desktop application based on web technologies. Like other
desktop apps, it has its own icon in the dock, native menus and
dialogs, and full access to the file system.

Open the dev tools, however, and Atom's web-based core shines through.
Whether you're tweaking the look of Atom's interface with CSS or
adding major features with HTML and JavaScript, it's never been easier
to take control of your editor.

%package -n apm
Summary:	Atom Package Manager
Group:		Development/Tools
URL:		https://github.com/atom/apm

%description -n apm
Discover and install Atom packages powered by atom.io

You can configure apm via a ~/.atom/.apmrc file similarly to npm
config.

%prep
%setup -qcT
SOURCE=%{SOURCE0}
version=$(rpm -qp --nodigest --nosignature --qf '%{V}' $SOURCE)
test version:${version} = version:%{version}
rpm2cpio $SOURCE | cpio -i -d

mv usr/share/icons .
mv usr/share/applications/* .
mv usr/share/atom .
mv usr/bin .

mv atom/LICENSE .
mv atom/chromedriver/LICENSE LICENSE.chromedrive

# unneeded
mv atom/resources/app/atom.sh .

# remove empty locales
find atom/locales -size 0 | xargs rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}

cp -a atom/* $RPM_BUILD_ROOT%{_appdir}

ln -s %{_appdir}/atom $RPM_BUILD_ROOT%{_bindir}
ln -s %{_appdir}/resources/app/apm/bin/apm $RPM_BUILD_ROOT%{_bindir}/apm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.chromedrive
%attr(755,root,root) %{_bindir}/atom
%dir %{_appdir}
%{_appdir}/version
%{_appdir}/*.bin
%{_appdir}/content_shell.pak
%{_appdir}/icudtl.dat
%attr(755,root,root) %{_appdir}/atom
%attr(755,root,root) %{_appdir}/libgcrypt.so.11
%attr(755,root,root) %{_appdir}/libnode.so
%attr(755,root,root) %{_appdir}/libnotify.so.4
%dir %{_appdir}/chromedriver
%attr(755,root,root) %{_appdir}/chromedriver/chromedriver

%{_appdir}/locales

%dir %{_appdir}/resources
%{_appdir}/resources/LICENSE.md
%dir %{_appdir}/resources/app

%{_appdir}/resources/app.asar
%{_appdir}/resources/atom.asar

# needed?
%{_appdir}/resources/app.asar.unpacked

%files -n apm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/apm

# too many files to list, assume file permissions
%defattr(-,root,root,-)
%{_appdir}/resources/app/apm
