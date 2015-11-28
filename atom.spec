# BUILDING:
# https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md

Summary:	A hackable text editor for the 21st century
Name:		atom
Version:	1.2.4
Release:	0.1
License:	MIT
Group:		Applications/Editors
Source0:	https://github.com/atom/atom/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c39979527badc8a17d0af47d36994990
URL:		https://atom.io/
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libstdc++-devel
BuildRequires:	nodejs-devel
BuildRequires:	nodejs-gyp
BuildRequires:	npm >= 1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Atom is a desktop application based on web technologies. Like other
desktop apps, it has its own icon in the dock, native menus and
dialogs, and full access to the file system.

Open the dev tools, however, and Atom's web-based core shines through.
Whether you're tweaking the look of Atom's interface with CSS or
adding major features with HTML and JavaScript, it's never been easier
to take control of your editor.

%prep
%setup -q

%build
# Set the build directory as per grunt.option('build-dir') in Gruntfile.coffee.
# This prevents Atom from being built somewhere in /tmp.
script/build \
	--build-dir=$PWD/build-rpm

%install
rm -rf $RPM_BUILD_ROOT
# The install task honours the INSTALL_PREFIX environment variable, so specify
# it for easier packaging.
export INSTALL_PREFIX=$RPM_BUILD_ROOT%{_prefix}

# -d switch enables debugging output, -v enables verbose output
script/grunt -dv --build-dir=$PWD/build-rpm install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/atom
%attr(755,root,root) %{_bindir}/apm
