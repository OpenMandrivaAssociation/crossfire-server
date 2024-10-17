# A few notes:
# Intentionally don't create logrotate files. If I'm a player,
# I'll damn any server admin who try to restart game server because
# of log rotation.
%define version 1.70.0
%define release 2

%define map_version 1.70.0
%define _localstatedir /var/lib/games

Name:		crossfire-server
Version:	%{version}
Release:	%{release}
Summary:	Crossfire - a Graphical Adventure Game
Group:		Games/Adventure
License:	GPLv2
URL:		https://crossfire.real-time.com
Source0:	http://prdownloads.sourceforge.net/crossfire/crossfire-%{version}.tar.gz
Source1:	crossfire-server.service
Patch2:		crossfire-server-1.50.0-detach.patch
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	libxaw-devel pkgconfig(xmu) pkgconfig(xext) libice-devel pkgconfig(xt)
BuildRequires:	pkgconfig(python)
BuildRequires:	flex
BuildRequires:	tetex-latex
BuildRequires:	pkgconfig(libcurl)
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
Requires:	crossfire-maps = %{map_version}

%description
Crossfire is a highly graphical role-playing adventure game
with characteristics reminiscent of rogue, nethack, omega, and gauntlet.
It has multiplayer capability and presently runs under X11.

This package contains files necessary to run a local crossfire server,
or join into a network of crossfire server all over the world. If you
only want to play crossfire, you don't need this package.

%prep
%setup -q -n crossfire-%{version}
%patch2 -p1 -b .detach

sed -i 's#\r##' utils/player_dl.pl.in
# Don't use a hardcoded /tmp directory for building the image archive
sed -i "s#^\$TMPDIR=.*#\$TMPDIR=\"`pwd`\";#" lib/adm/collect_images.pl
# Don't map stdio streams to /
# This is fixed in CVS, but didn't make it into the 1.9.1 release.
sed -i 's#    (void) open ("/", O_RDONLY);#    (void) open ("/var/log/crossfire/crossfire.log", O_RDONLY);#' server/daemon.c

# Change the location of the tmp directory
sed -i "s@^#define TMPDIR \"/tmp\"@#define TMPDIR \"%{_var}/lib/games/%{name}/tmp\"@" include/config.h

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-static
	
%make

%install
%makeinstall_std

install -pD -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# remove unpackaged files
rm -f %{buildroot}%{_libdir}/crossfire/{add_throw.perl,mktable.script}
rm -f %{buildroot}%{_libdir}/crossfire/plugins/*a

#Remove crossedit man page until it compiles again
#rm -f %{buildroot}%{_mandir}/man6/crossedit.*

# touch log file
mkdir -p %{buildroot}%{_logdir}/crossfire
touch %{buildroot}%{_logdir}/crossfire/logfile

%post
%create_ghostfile %{_logdir}/crossfire/logfile root games 0664
%create_ghostfile %{_localstatedir}/crossfire/banish_file root games 0664
%create_ghostfile %{_localstatedir}/crossfire/bookarch root games 0664
%create_ghostfile %{_localstatedir}/crossfire/clockdata root games 0664
%create_ghostfile %{_localstatedir}/crossfire/highscore root games 0664
%create_ghostfile %{_localstatedir}/crossfire/temp.maps root games 0664
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc AUTHORS ChangeLog DEVELOPERS INSTALL NEWS README TODO
%config(noreplace) %{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/crossfire
%attr(2111,root,games) %{_gamesbindir}/crossfire-server
%{_gamesbindir}/crossfire-config
%{_gamesbindir}/crossloop*
%{_gamesbindir}/player_dl.pl
%{_gamesdatadir}/crossfire/*
%dir %{_libdir}/crossfire
%{_libdir}/crossfire/metaserver.pl
%{_libdir}/crossfire/random_map
%dir %{_libdir}/crossfire/plugins
%{_libdir}/crossfire/plugins/*.so
%{_mandir}/man6/crossfire*
%{_mandir}/man6/crossloop*


%defattr(0660,root,games,2770)
%dir %{_logdir}/crossfire
%ghost %{_logdir}/crossfire/logfile
%dir %{_localstatedir}/crossfire
%ghost %{_localstatedir}/crossfire/banish_file
%ghost %{_localstatedir}/crossfire/bookarch
%ghost %{_localstatedir}/crossfire/clockdata
%ghost %{_localstatedir}/crossfire/highscore
%ghost %{_localstatedir}/crossfire/temp.maps
%dir %{_localstatedir}/crossfire/maps
%dir %{_localstatedir}/crossfire/players
%dir %{_localstatedir}/crossfire/unique-items
