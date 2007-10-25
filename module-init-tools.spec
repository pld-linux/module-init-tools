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
Version:	3.2.2
Release:	3.1
License:	GPL
Group:		Applications/System
Source0:	http://kernel.org/pub/linux/utils/kernel/module-init-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	a1ad0a09d3231673f70d631f3f5040e9
Source1:	%{name}-blacklist
# TODO:
# - update manual to this patch too
Patch0:		%{name}-modutils.patch
Patch1:		%{name}-shared-zlib.patch
Patch2:		%{name}-insmod-zlib.patch
Patch3:		%{name}-sparc.patch
Patch4:		%{name}-modprobe_d.patch
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	docbook-dtd41-sgml
#BuildRequires:	docbook-utils
BuildRequires:	glibc-static
BuildRequires:	zlib-static
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
%configure \
	--enable-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{cron.d,modprobe.d},%{_mandir}/man{5,8}}

%{__make} install install-am \
	DESTDIR=$RPM_BUILD_ROOT \
	mandir=%{_mandir} \
	INSTALL=install

:> $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.conf

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/blacklist

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -s %{_sysconfdir}/modprobe.conf -a -x /sbin/modprobe.modutils -a -f /etc/modules.conf ] && [ -d /lib/modules/`uname -r` ]; then
	echo "Generating %{_sysconfdir}/modprobe.conf from obsolete /etc/modules.conf"
	%{_sbindir}/generate-modprobe.conf %{_sysconfdir}/modprobe.conf
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/blacklist
%dir %{_sysconfdir}/modprobe.d
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
