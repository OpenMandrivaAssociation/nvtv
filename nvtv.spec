%define name	nvtv 
%define version	0.4.7

%define major		0
%define libname		%mklibname nvtvsimple %major
%define develname	%mklibname nvtvsimple -d

Name: 		%{name}
Version: 	%{version}
Release:	%mkrel 20
Source0:	http://downloads.sourceforge.net/nv-tv-out/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/nv-tv-out/libnvtvsimple-0.4.7a.tar.gz
Source2:	nvtv.png
Patch0:		nvtv-0.4.7-ppc-build-fix.patch
Patch1:		libnvtvsimple-0.4.7a-fix-linking.patch
License: 	GPLv2
Group:		Video
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary: 	Enable TV-Out on Linux for NVIDIA cards	
URL:		http://sourceforge.net/projects/nv-tv-out/	
BuildRequires:	pciutils-devel 
BuildRequires:	gtk2-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	imagemagick
Requires:	pam
Requires:	xorg-x11
Requires:	usermode
Requires:	usermode-consoleonly
ExclusiveArch:	%{ix86} x86_64

%description
This is a tool to enable TV-Out on Linux for NVIDIA cards. It does not
need the kernel, supports multiple TV encoder chips. You may use all the
features of the chip, down to direct register access, and all resolutions 
and sizes the chip supports.

%package -n %libname
Group: System/Libraries
Summary: Library to enable TV-Out on Linux for NVIDIA cards

%description -n %libname
This is a shared library to enable TV-Out on Linux for NVIDIA cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%package -n %develname
Group: Development/C
Requires: %libname = %version-%release
Provides: libnvtvsimple-devel = %version
Obsoletes: %mklibname nvtvsimple 0 -d
Summary: Library to enable TV-Out on Linux for NVIDIA cards

%description -n %develname
This is a shared library to enable TV-Out on Linux for NVIDIA cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%prep
%setup -q -b 1
%patch0 -p1 -b .ppc-build-fix
%patch1 -p1
cd lib
libtoolize --copy --force
aclocal
autoconf
automake -a -c --foreign

%build
%configure2_5x --prefix=/bin --with-gtk=gtk2
%make
pushd lib
%configure2_5x
%make
popd

%install
rm -rf ${RPM_BUILD_ROOT}
install -D -m755 src/nvtv ${RPM_BUILD_ROOT}/%{_sbindir}/nvtv
install -D -m755 src/nvtvd ${RPM_BUILD_ROOT}/%{_sbindir}/nvtvd

# icons
mkdir -p ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
install -m644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{SOURCE2} ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{SOURCE2} ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

pushd lib
%makeinstall_std
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Nvidia TV Output
Comment=Frontend for Nvidia TV output
Exec=%{_bindir}/%{name}
Icon=%{name}
StartupNotify=true
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;
Type=Application
EOF


#Lets make a nice dialog box asking for root perms:
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/{pam.d,security/console.apps}
cat <<EOF >${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d/%{name}
#%PAM-1.0
auth	sufficient	/lib/security/pam_rootok.so
auth	include		system-auth
session	optional	/lib/security/pam_xauth.so
account	required	/lib/security/pam_permit.so
EOF


cat <<EOF >${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps/%{name}
USER=root
PROGRAM=/usr/sbin/nvtv
SESSION=true
FALLBACK=true
EOF

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -s %{_bindir}/consolehelper $RPM_BUILD_ROOT%{_bindir}/%name

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (-,root,root)
%doc doc/*.txt doc/USAGE README TODO BUGS ChangeLog FAQ ANNOUNCE 
%{_bindir}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}d
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

%files -n %libname
%defattr (-,root,root)
%_libdir/lib*.so.*

%files -n %develname
%defattr (-,root,root)
%_includedir/*
%_libdir/lib*.so
%_libdir/lib*a
%_libdir/pkgconfig/*.pc


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.7-19mdv2011.0
+ Revision: 666636
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.7-18mdv2011.0
+ Revision: 606835
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.7-17mdv2010.1
+ Revision: 523450
- rebuilt for 2010.1

* Sun Sep 27 2009 Olivier Blin <oblin@mandriva.com> 0.4.7-16mdv2010.0
+ Revision: 450173
- build on x86 only (from Arnaud Patard)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.4.7-15mdv2010.0
+ Revision: 426262
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.4.7-14mdv2009.1
+ Revision: 301194
- rebuild for changed xcb

* Fri Jul 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.7-13mdv2009.0
+ Revision: 231642
- fix linking

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.7-12mdv2008.1
+ Revision: 179106
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - fix spacing at top of description
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Thu Jul 26 2007 Adam Williamson <awilliamson@mandriva.org> 0.4.7-11mdv2008.0
+ Revision: 56073
- buildrequires libxxf86vm-devel
- rebuild for 2008
- don't bother packaging INSTALL
- update pam.d file
- fd.o icons
- update new menu entry, no X-Mandriva
- drop old menu entry
- drop buildrequires wxgtk-devel (native GTK interface supersedes it)
- bunzip2 patches
- specify license as GPLv2
- new devel policy
- drop unnecessary patch1, it builds against GTK+ 2.0 without it
- update to release 0.4.7, separate source files for main package and lib
- Import nvtv



* Mon Jul 17 2006 Antoine Ginies <aginies@mandriva.com> 0.4.7-2.20040408.10mdv2007.0
- patch from cris_@_beebgames.com, don't use obsolete gtK1.2

* Wed Jun 28 2006 Götz Waschk <waschk@mandriva.org> 0.4.7-2.20040408.9mdv2007.0
- fix buildrequires

* Fri Jun 23 2006 Antoine Ginies <aginies@n3.mandriva.com> 0.4.7-1.20040408.8mdv2007.0
- forget a \ in xdg menu (thx fcrozat report)

* Fri Jun 23 2006 Antoine Ginies <aginies@n3.mandriva.com> 0.4.7-0.20040408.7mdv2007.0
- xdg menu

* Mon Oct 24 2005 Götz Waschk <waschk@mandriva.org> 0.4.7-0.20040408.6mdk
- fix build

* Wed Jun 16 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.4.7-0.20040408.5mdk
- fix ppc build

* Sat Apr 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.4.7-0.20040408.4mdk
- fix buildrequires

* Fri Apr 16 2004 Götz Waschk <waschk@linux-mandrake.com> 0.4.7-0.20040408.3mdk
- fix buildrequires again

* Thu Apr 15 2004 Götz Waschk <waschk@linux-mandrake.com> 0.4.7-0.20040408.2mdk
- fix buildrequires

* Thu Apr  8 2004 Götz Waschk <waschk@linux-mandrake.com> 0.4.7-0.20040408.1mdk
- build libnvtvsimple
- fix configure call
- new snapshot

* Mon Aug 25 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.4.5-3mdk 
- correct path in menu

* Tue Aug 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.5-2mdk
- rebuild

* Tue Jul 01 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.5-1mdk
- from Laurent Grawet <laurent.grawet@ibelgique.com> :
	- new release

* Sat May 31 2003 Laurent Grawet <laurent.grawet@ibelgique.com> 0.4.4-1mdk
- new release

* Fri Feb 21 2003 Antoine Ginies <aginies@bi.mandrakesoft.com> 0.4.3-4mdk 
- add forgotten links

* Tue Feb 18 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.4.3-3mdk 
- move libgtk+1.2-devel to Buildrequires :-)

* Mon Feb 17 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.4.3-2mdk
- add requires and consolehelper to avoid setuid (from fdanny@mailmij.org)

* Tue Feb 11 2003 Antoine Ginies <aginies@bi.mandrakesoft.com> 0.4.3-1mdk 
- new release

* Fri Jan 03 2003 Antoine Ginies <aginies@mandrakesoft.com> 0.4.2-2mdk
- rebuild for new glibc
* Mon Nov 18 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.4.2-1mdk
- from Roger <roger@linuxfreemail.com> :
	- 0.4.2

* Wed Nov 06 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.4.0-3mdk
- setuid nvtv (needed for user)
- add icons in menu

* Tue Sep 17 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.4.0-2mdk
- add requires  

* Tue Sep 17 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.4.0-1mdk
- first release for mandrakesoft 
