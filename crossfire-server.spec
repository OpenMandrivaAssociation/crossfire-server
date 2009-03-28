# A few notes:
# Intentionally don't create logrotate files. If I'm a player,
# I'll damn any server admin who try to restart game server because
# of log rotation.
%define version 1.11.0
%define release %mkrel 4

%define map_version 1.11.0

Name:		crossfire-server
Version:	%{version}
Release:	%{release}
Summary:	Crossfire - a Graphical Adventure Game
Group:		Games/Adventure
License:	GPL
URL:		http://crossfire.real-time.com
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source:		http://prdownloads.sourceforge.net/crossfire/crossfire-%{version}.tar.bz2
Source1:	%{name}.init.bz2
Patch1:		crossfire-1.11.0-fix-str-fmt.patch
Patch2:		crossfire-server-1.7.0-detach.patch
Patch3:		crossfire-1.11.0-py2.6.patch
BuildRequires:	png-devel
BuildRequires:	xpm-devel
BuildRequires:	libxaw-devel libxmu-devel libxext-devel libice-devel libxt-devel
BuildRequires:	python-devel
BuildRequires:	bzip2
BuildRequires:	flex
BuildRequires:	tetex-latex
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


%package -n	crossfire-crossedit
Summary:	Map editor for Crossfire
Group:		Games/Adventure
Requires:	%{name} = %{version}

%description -n	crossfire-crossedit
Crossfire is a highly graphical role-playing adventure game
with characteristics reminiscent of rogue, nethack, omega, and gauntlet.
It has multiplayer capability and presently runs under X11.

This package contains crossedit, a map editor for crossfire.


%prep
%setup -q -n crossfire-%{version}
%patch1 -p0
%patch2 -p1 -b .detach
%patch3 -p0

# cleanup
perl -pi -e 's/\r//g' utils/player_dl.pl.in

%build
%define _localstatedir /var/lib/games
sh ./autogen.sh
%serverbuild

%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}	
	
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
bzip2 -dc %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}
chmod 0755 $RPM_BUILD_ROOT%{_initrddir}/%{name}

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/crossfire/{add_throw.perl,mktable.script}
rm -f $RPM_BUILD_ROOT%{_libdir}/crossfire/plugins/*a

#Remove crossedit man page until it compiles again
#rm -f $RPM_BUILD_ROOT%{_mandir}/man6/crossedit.*

# touch log file
mkdir -p $RPM_BUILD_ROOT/var/log/crossfire
touch $RPM_BUILD_ROOT/var/log/crossfire/logfile

%clean
rm -rf $RPM_BUILD_ROOT

%post
%create_ghostfile /var/log/crossfire/logfile root games 0664
%create_ghostfile %{_localstatedir}/crossfire/banish_file root games 0664
%create_ghostfile %{_localstatedir}/crossfire/bookarch root games 0664
%create_ghostfile %{_localstatedir}/crossfire/clockdata root games 0664
%create_ghostfile %{_localstatedir}/crossfire/highscore root games 0664
%create_ghostfile %{_localstatedir}/crossfire/temp.maps root games 0664
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog DEVELOPERS INSTALL NEWS README TODO
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/crossfire
%attr(2111,root,games) %{_gamesbindir}/crossfire
%{_gamesbindir}/crossfire-config
%{_gamesbindir}/crossloop*
%{_gamesbindir}/player_dl.pl
%{_datadir}/games/crossfire/*
%dir %{_libdir}/crossfire
%{_libdir}/crossfire/metaserver.pl
%{_libdir}/crossfire/random_map
%dir %{_libdir}/crossfire/plugins
%{_libdir}/crossfire/plugins/*.so
%{_mandir}/man6/crossfire*
%{_mandir}/man6/crossloop*


%defattr(0660,root,games,2770)
%dir /var/log/crossfire
%ghost /var/log/crossfire/logfile
%dir %{_localstatedir}/crossfire
%ghost %{_localstatedir}/crossfire/banish_file
%ghost %{_localstatedir}/crossfire/bookarch
%ghost %{_localstatedir}/crossfire/clockdata
%ghost %{_localstatedir}/crossfire/highscore
%ghost %{_localstatedir}/crossfire/temp.maps
%dir %{_localstatedir}/crossfire/maps
%dir %{_localstatedir}/crossfire/players
%dir %{_localstatedir}/crossfire/unique-items

%files -n crossfire-crossedit
%defattr(-,root,root)
%{_gamesbindir}/crossedit
%{_mandir}/man6/crossedit.*


