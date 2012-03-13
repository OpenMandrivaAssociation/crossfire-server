# A few notes:
# Intentionally don't create logrotate files. If I'm a player,
# I'll damn any server admin who try to restart game server because
# of log rotation.
%define version 1.60.0
%define release %mkrel 1

%define map_version 1.50.0
%define _localstatedir /var/lib/games

Name:		crossfire-server
Version:	%{version}
Release:	%{release}
Summary:	Crossfire - a Graphical Adventure Game
Group:		Games/Adventure
License:	GPL
URL:		http://crossfire.real-time.com
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

Source0:	http://prdownloads.sourceforge.net/crossfire/crossfire-%{version}.tar.gz
Source1:	%{name}.init
Patch2:		crossfire-server-1.50.0-detach.patch
Patch3:		crossfire-server-1.50.0-py2.7.patch
BuildRequires:	png-devel
BuildRequires:	xpm-devel
BuildRequires:	libxaw-devel libxmu-devel libxext-devel libice-devel libxt-devel
BuildRequires:	python-devel
BuildRequires:	flex
BuildRequires:	tetex-latex
BuildRequires:	curl-devel
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
%patch3 -p0 -b .python

# cleanup
perl -pi -e 's/\r//g' utils/player_dl.pl.in

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--disable-static
	
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#mkdir -p %{buildroot}%{_initrddir}
install -Dm0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# remove unpackaged files
rm -f %{buildroot}%{_libdir}/crossfire/{add_throw.perl,mktable.script}
rm -f %{buildroot}%{_libdir}/crossfire/plugins/*a

#Remove crossedit man page until it compiles again
#rm -f %{buildroot}%{_mandir}/man6/crossedit.*

# touch log file
mkdir -p %{buildroot}%{_logdir}/crossfire
touch %{buildroot}%{_logdir}/crossfire/logfile

%clean
rm -rf %{buildroot}

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
%defattr(-,root,root)
%doc AUTHORS ChangeLog DEVELOPERS INSTALL NEWS README TODO
%config(noreplace) %{_initrddir}/%{name}
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
