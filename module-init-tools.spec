#
# Conditional build
%bcond_without	initrd	# don't build initrd package
%bcond_without	uClibc	# don't link with uclibc, use glibc
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
Version:	3.5
Release:	3
License:	GPL v2+
Group:		Applications/System
Source0:	http://kernel.org/pub/linux/utils/kernel/module-init-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	2b47686247fc9a99bfdb9dd1d1d80e6f
Source1:	%{name}-blacklist
Source2:	%{name}-usb
# TODO:
# - update manual to this patch too
Patch0:		%{name}-modutils.patch
Patch1:		%{name}-shared-zlib.patch
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
%{?with_uClibc:BuildRequires:	uClibc-static >= 3:0.9.29-23}
%endif
Obsoletes:	modutils
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
Summary(pl.UTF-8):	Narzędzia do modułów jądra systemu bez kerneld - statyczne binarki dla initrd
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description initrd
Module utilities without kerneld - static binary for initrd.

%description initrd -l pl.UTF-8
Narzędzia do modułów jądra systemu bez kerneld - statyczne binarki dla initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%if %{with initrd}
%configure \
	%{?with_uClibc:LDFLAGS="%{rpmldflags} -static"} \
	%{?with_uClibc:CC="%{_target_cpu}-uclibc-gcc"} \
	--enable-zlib

%{__make} \
	ZLIB=/usr/lib/libz.a

%{__make} install-exec-am \
	DESTDIR=initrd-mod

%{__make} clean
%endif

%configure \
	--enable-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,modprobe.d},%{_mandir}/man{5,8}}

%{__make} install install-am \
	DESTDIR=$RPM_BUILD_ROOT \
	mandir=%{_mandir} \
	INSTALL=install

:> $RPM_BUILD_ROOT/etc/modprobe.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/modprobe.d/blacklist.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/modprobe.d/usb.conf

%if %{with initrd}
install initrd-mod/sbin/depmod $RPM_BUILD_ROOT%{_sbindir}/initrd-depmod
install initrd-mod/sbin/insmod $RPM_BUILD_ROOT%{_sbindir}/initrd-insmod
install initrd-mod/sbin/lsmod $RPM_BUILD_ROOT%{_sbindir}/initrd-lsmod
install initrd-mod/sbin/modprobe $RPM_BUILD_ROOT%{_sbindir}/initrd-modprobe
install initrd-mod/sbin/rmmod $RPM_BUILD_ROOT%{_sbindir}/initrd-rmmod
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -s /etc/modprobe.conf -a -x /sbin/modprobe.modutils -a -f /etc/modules.conf ] && [ -d /lib/modules/`uname -r` ]; then
	echo "Generating /etc/modprobe.conf from obsolete /etc/modules.conf"
	%{_sbindir}/generate-modprobe.conf /etc/modprobe.conf
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/modprobe.conf
%dir /etc/modprobe.d
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/*.conf
%attr(755,root,root) %{_sbindir}/*
%if %{with initrd}
%exclude %{_sbindir}/initrd-*
%endif
%{_mandir}/man5/depmod.conf.5*
%{_mandir}/man5/modprobe.conf.5*
%{_mandir}/man5/modules.dep.5*
%{_mandir}/man8/*.8*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-*
%endif
