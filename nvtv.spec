%define major	0
%define libname	%mklibname nvtvsimple %{major}
%define devname	%mklibname nvtvsimple -d
%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	Enable TV-Out on Linux for NVIDIA cards	
Name:		nvtv
Version:	0.4.7
Release:	33
License:	GPLv2
Group:		Video
Url:		http://sourceforge.net/projects/nv-tv-out/	
Source0:	http://downloads.sourceforge.net/nv-tv-out/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/nv-tv-out/libnvtvsimple-0.4.7a.tar.gz
Source2:	nvtv.png
Patch0:		nvtv-0.4.7-ppc-build-fix.patch
Patch1:		libnvtvsimple-0.4.7a-fix-linking.patch
Patch2:		nvtv-automake-1.13.patch
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xxf86vm)
Requires:	pam
Requires:	usermode
Requires:	xorg-x11
Requires:	usermode-consoleonly

%description
This is a tool to enable TV-Out on Linux for NVIDIA cards. It does not
need the kernel, supports multiple TV encoder chips. You may use all the
features of the chip, down to direct register access, and all resolutions 
and sizes the chip supports.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library to enable TV-Out on Linux for NVIDIA cards

%description -n %{libname}
This is a shared library to enable TV-Out on Linux for NVIDIA cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%package -n %{devname}
Group:		Development/C
Requires:	%{libname} = %version-%release
Provides:	libnvtvsimple-devel = %version
Obsoletes:	%mklibname nvtvsimple 0 -d
Summary:	Library to enable TV-Out on Linux for NVIDIA cards

%description -n %{devname}
This is a shared library to enable TV-Out on Linux for NVIDIA cards.
It does not need the kernel, supports multiple TV encoder chips. You
may use all the features of the chip, down to direct register access,
and all resolutions and sizes the chip supports.

%prep
%setup -q -b 1
%autopatch -p1
cd lib
touch NEWS AUTHORS ChangeLog
autoreconf -fi

%build
export CC='gcc -fgnu89-inline'
%configure --prefix=/bin --with-gtk=gtk2
%make
pushd lib
%configure
%make
popd

%install
install -D -m755 src/nvtv %{buildroot}/%{_sbindir}/nvtv
install -D -m755 src/nvtvd %{buildroot}/%{_sbindir}/nvtvd

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
install -m644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%makeinstall_std -C lib

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
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
mkdir -p %{buildroot}%{_sysconfdir}/{pam.d,security/console.apps}
cat <<EOF >%{buildroot}%{_sysconfdir}/pam.d/%{name}
#%PAM-1.0
auth	sufficient	/lib/security/pam_rootok.so
auth	include		system-auth
session	optional	/lib/security/pam_xauth.so
account	required	/lib/security/pam_permit.so
EOF

cat <<EOF >%{buildroot}%{_sysconfdir}/security/console.apps/%{name}
USER=root
PROGRAM=/usr/sbin/nvtv
SESSION=true
FALLBACK=true
EOF

mkdir -p %{buildroot}%{_bindir}
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%name

%files
%doc doc/*.txt doc/USAGE README TODO BUGS ChangeLog FAQ ANNOUNCE 
%{_bindir}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}d
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%files -n %{libname}
%{_libdir}/libnvtvsimple.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

