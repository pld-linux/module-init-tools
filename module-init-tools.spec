# TODO:
# - zlib-capable initrd insmod requires using glibc-static or separate zlib compiled for dietlibc
#
# Conditional build
%bcond_without	initrd		# don't build initrd package
%bcond_without	dietlibc	# don't link with dietlibc, use glibc
#
Summary:	Module utilities without kerneld
Summary(de.UTF-8):	Module-Utilities
Summary(es.UTF-8):	Utilitarios para módulos y kerneld
Summary(fr.UTF-8):	Utiltaires de modules
Summary(pl.UTF-8):	Narzędzia do modułów jądra systemu bez kerneld
Summary(pt_BR.UTF-8):	Utilitários para módulos e kerneld
Summary(ru.UTF-8):	Утилиты для работы с модулями ядра
Summary(tr.UTF-8):	Modül programları
Summary(uk.UTF-8):	Утиліти для роботи з модулями ядра
Name:		module-init-tools
Version:	3.16
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://kernel.org/pub/linux/utils/kernel/module-init-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	bc44832c6e41707b8447e2847d2019f5
Source1:	%{name}-blacklist
Source2:	%{name}-usb
Patch0:		%{name}-max.patch
Patch2:		%{name}-insmod-zlib.patch
Patch3:		%{name}-sparc.patch
Patch4:		%{name}-modprobe_d.patch
URL:		http://www.kerneltools.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-to-man
BuildRequires:	glibc-static
BuildRequires:	zlib-static
%if %{with initrd}
%{?with_dietlibc:BuildRequires:	dietlibc-static}
%endif
Obsoletes:	modutils
Conflicts:	rc-scripts < 0.4.2.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/sbin
%define		_sbindir	/sbin

%description
This package contains a set of programs for loading, inserting, and
removing kernel modules for Linux (versions 2.5.47 and above). It
serves the same function that the "modutils" package serves for Linux
2.4.

%description -l pl.UTF-8
Ten pakiet zawiera zestaw programów do wczytywania, wstawiania i
usuwania modułów jądra Linuksa (w wersji 2.5.47 i wyższych). Służy do
tego samego, co pakiet modutils dla Linuksa 2.4.

%package initrd
Summary:	Module utilities without kerneld - static binary for initrd
Summary(pl.UTF-8):	Narzędzia do modułów jądra systemu bez kerneld - statyczne binaria dla initrd
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Conflicts:	geninitrd < 10000.10

%description initrd
Module utilities without kerneld - static binary for initrd.

%description initrd -l pl.UTF-8
Narzędzia do modułów jądra systemu bez kerneld - statyczne binaria dla
initrd.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
# huh?
# %patch3 -p1
%patch4 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

%if %{with initrd}
dietcc="%{__cc}"
dietcc=${dietcc#*ccache }
%configure \
	%{?with_dietlibc:CC="${dietcc} %{rpmcflags} %{rpmldflags} -Os -static"} \
	%{!?with_dietlibc:CC="%{__cc} -static"} \
	%{!?with_dietlibc:--enable-zlib}

%{__make}

%{__make} install-exec-am \
	DESTDIR=initrd-mod

%{__make} clean
%endif

%configure \
	--enable-zlib-dynamic
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,modprobe.d},%{_mandir}/man{5,8}}

%{__make} -j1 install install-am \
	DESTDIR=$RPM_BUILD_ROOT \
	mandir=%{_mandir} \
	INSTALL=install

:> $RPM_BUILD_ROOT/etc/modprobe.d/modprobe.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/modprobe.d/blacklist.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/modprobe.d/usb.conf

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install build/initrd-mod/sbin/depmod $RPM_BUILD_ROOT%{_libdir}/initrd/depmod
install build/initrd-mod/sbin/insmod $RPM_BUILD_ROOT%{_libdir}/initrd/insmod
install build/initrd-mod/sbin/lsmod $RPM_BUILD_ROOT%{_libdir}/initrd/lsmod
install build/initrd-mod/sbin/modprobe $RPM_BUILD_ROOT%{_libdir}/initrd/modprobe
install build/initrd-mod/sbin/rmmod $RPM_BUILD_ROOT%{_libdir}/initrd/rmmod
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -s /etc/modprobe.d/modprobe.conf -a -x /sbin/modprobe.modutils -a -f /etc/modules.conf ] && [ -d /lib/modules/$(uname -r) ]; then
	echo "Generating /etc/modprobe.d/modprobe.conf from obsolete /etc/modules.conf"
	%{_sbindir}/generate-modprobe.conf /etc/modprobe.d/modprobe.conf
	mv -f /etc/modules.conf{,.rpmsave}
fi

%triggerpostun -- %{name} < 3.10
if [ -f /etc/modprobe.conf.rpmsave ]; then
	cp -f /etc/modprobe.d/modprobe.conf{,.rpmnew}
	mv -f /etc/modprobe.conf.rpmsave /etc/modprobe.d/modprobe.conf
%banner -e %{name} << 'EOF'
Moved modprobe.conf to /etc/modprobe.d/modprobe.conf.
EOF
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README TODO
%dir /etc/modprobe.d
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/blacklist.conf
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/modprobe.conf
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/usb.conf
%attr(755,root,root) %{_sbindir}/depmod
%attr(755,root,root) %{_sbindir}/insmod
%attr(755,root,root) %{_sbindir}/insmod.static
%attr(755,root,root) %{_sbindir}/lsmod
%attr(755,root,root) %{_sbindir}/modinfo
%attr(755,root,root) %{_sbindir}/modprobe
%attr(755,root,root) %{_sbindir}/rmmod
%{_mandir}/man5/depmod.conf.5*
%{_mandir}/man5/depmod.d.5*
%{_mandir}/man5/modprobe.conf.5*
%{_mandir}/man5/modprobe.d.5*
%{_mandir}/man5/modules.dep.5*
%{_mandir}/man5/modules.dep.bin.5*
%{_mandir}/man8/depmod.8*
%{_mandir}/man8/insmod.8*
%{_mandir}/man8/lsmod.8*
%{_mandir}/man8/modinfo.8*
%{_mandir}/man8/modprobe.8*
%{_mandir}/man8/rmmod.8*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/depmod
%attr(755,root,root) %{_libdir}/initrd/insmod
%attr(755,root,root) %{_libdir}/initrd/lsmod
%attr(755,root,root) %{_libdir}/initrd/modprobe
%attr(755,root,root) %{_libdir}/initrd/rmmod
%endif
