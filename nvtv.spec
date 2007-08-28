%define name	nvtv 
%define version	0.4.7
%define release	%mkrel 11

%define major		0
%define libname		%mklibname nvtvsimple %major
%define develname	%mklibname nvtvsimple -d

Name: 		%{name}
Version: 	%{version}
Release:	%{release}
Source0:	http://downloads.sourceforge.net/nv-tv-out/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/nv-tv-out/libnvtvsimple-0.4.7a.tar.gz
Source2:	nvtv.png
Patch0:		nvtv-0.4.7-ppc-build-fix.patch
License: 	GPLv2
Group:		Video
Summary: 	Enable TV-Out on Linux for NVIDIA cards	
URL:		http://sourceforge.net/projects/nv-tv-out/	
BuildRequires:	pciutils-devel 
BuildRequires:	gtk2-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	ImageMagick
Requires:	pam
Requires:	xorg-x11
Requires:	usermode
Requires:	usermode-consoleonly

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

%build
%configure2_5x --prefix=/bin --with-gtk=gtk2
%make
pushd lib
%configure2_5x --with-gtk=gtk2
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

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

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
