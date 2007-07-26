%define name	nvtv 
%define version	0.4.7
%define cvs 20040408
%define major 0
%define libname %mklibname nvtvsimple %major
%define nbrel %mkrel 10
%define release 2.%cvs.%nbrel
%define fname %name-%cvs 

Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Source:		%{fname}.tar.bz2
Source1:	nvtv.png
Patch0:		nvtv-0.4.7-ppc-build-fix.patch.bz2
Patch1:		nvtv-disable-gtk1.2.patch.bz2
License: 	GPL
Group:		Video
Summary: 	Enable TV-Out on Linux for NVidia cards	
URL:		http://sourceforge.net/projects/nv-tv-out/	
BuildRequires:	pciutils-devel 
Requires:	pam, xorg-x11, usermode, usermode-consoleonly
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk2-devel
BuildRequires:  wxGTK-devel
BuildRequires:	libxmu-devel

%description
This is a tool to enable TV-Out on Linux for NVidia cards. It does not
need the kernel, supports multiple TV encoder chips. You may use all the
features of the chip, down to direct register access, and all resolutions 
and sizes the chip supports.

%package -n %libname
Group: System/Libraries
Summary: Library to enable TV-Out on Linux for NVidia cards

%description -n %libname

This is a shared library to enable TV-Out on Linux for NVidia cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%package -n %libname-devel
Group: Development/C
Requires: %libname = %version-%release
Provides: libnvtvsimple-devel = %version
Summary: Library to enable TV-Out on Linux for NVidia cards

%description -n %libname-devel

This is a shared library to enable TV-Out on Linux for NVidia cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%prep
%setup -q -n %name
%patch0 -p1 -b .ppc-build-fix
%patch1 -p1 -b .disable-gtk1.2
chmod +x missing
aclocal
autoheader
autoconf
automake -a -c --foreign
cd lib
aclocal
autoheader
autoconf
automake -a -c --foreign

%build
%configure2_5x --prefix=/bin --with-gtk=gtk2
%make
cd lib
%configure2_5x --with-gtk=gtk2
%make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/pixmaps
install -m644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_prefix}/share/pixmaps/
install -D -m755 src/nvtv ${RPM_BUILD_ROOT}/%{_sbindir}/nvtv
install -D -m755 src/nvtvd ${RPM_BUILD_ROOT}/%{_sbindir}/nvtvd
cd lib
%makeinstall_std
cd ..
(mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name}  <<EOF
?package(%name): \ 
command="%{_bindir}/%{name}" needs="X11" \
icon="%{_prefix}/share/pixmaps/%name.png" \
section="Multimedia/Video" \
title="NvTV"  \
longtitle="Nvidia TV" \
xdg="true"
EOF
)

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name="Nvidia TV Output"
Comment="Frontend for Nvidia TV output"
TryExec="%{name}"
Exec="%{name}"
Icon="%{_prefix}/share/pixmaps/%{name}.png"
Terminal="0"
StartupNotify=true
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;X-MandrivaLinux-Multimedia-Video;
Type="Application"
EOF


#Lets make a nice dialog box asking for root perms:
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/{pam.d,security/console.apps}
cat <<EOF >${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d/%{name}
#%PAM-1.0
auth       sufficient   /lib/security/pam_rootok.so
auth       required    /lib/security/pam_stack.so service=system-auth
session    optional     /lib/security/pam_xauth.so
account    required     /lib/security/pam_permit.so
EOF


cat <<EOF >${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps/%{name}
USER=root
PROGRAM=/usr/sbin/nvtv
SESSION=true
FALLBACK=true
EOF

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -s %{_bindir}/consolehelper $RPM_BUILD_ROOT%{_bindir}/%name

%post
%{update_menus}

%postun
%{clean_menus}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (-,root,root)
%doc doc/*.txt doc/USAGE README TODO INSTALL BUGS ChangeLog FAQ ANNOUNCE 
%{_bindir}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}d
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_prefix}/share/pixmaps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_menudir}/*

%files -n %libname
%defattr (-,root,root)
%_libdir/lib*.so.*

%files -n %libname-devel
%defattr (-,root,root)
%_includedir/*
%_libdir/lib*.so
%_libdir/lib*a
%_libdir/pkgconfig/*.pc
