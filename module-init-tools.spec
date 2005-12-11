Summary:	Module utilities without kerneld
Summary(de):	Module-Utilities
Summary(es):	Utilitarios para módulos y kerneld
Summary(fr):	Utiltaires de modules
Summary(pl):	Narzêdzia do modu³ów j±dra systemu bez kerneld
Summary(pt_BR):	Utilitários para módulos e kerneld
Summary(ru):	õÔÉÌÉÔÙ ÄÌÑ ÒÁÂÏÔÙ Ó ÍÏÄÕÌÑÍÉ ÑÄÒÁ
Summary(tr):	Modül programları
Summary(uk):	õÔÉÌ¦ÔÉ ÄÌÑ ÒÏÂÏÔÉ Ú ÍÏÄÕÌÑÍÉ ÑÄÒÁ
Name:		module-init-tools
Version:	3.2.2
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://kernel.org/pub/linux/utils/kernel/module-init-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	a1ad0a09d3231673f70d631f3f5040e9
# TODO:
# - update manual to this patch too
Patch0:		%{name}-modutils.patch
Patch1:		%{name}-shared-zlib.patch
Patch2:		%{name}-insmod-zlib.patch
Patch3:		%{name}-sparc.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	glibc-static
BuildRequires:	zlib-static
Conflicts:	modutils < 2.4.25-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/sbin
%define		_sbindir	/sbin

%description
This package contains a set of programs for loading, inserting, and
removing kernel modules for Linux (versions 2.5.47 and above). It
serves the same function that the "modutils" package serves for Linux
2.4.

%description -l pl
Ten pakiet zawiera zestaw programów do wczytywania, wstawiania i
usuwania modu³ów j±dra Linuksa (w wersji 2.5.47 i wy¿szych). S³u¿y do
tego samego, co pakiet modutils dla Linuksa 2.4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,%{_mandir}/man{5,8}}

%{__make} install install-am \
	DESTDIR=$RPM_BUILD_ROOT \
	mandir=%{_mandir} \
	INSTALL=install

:> $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.conf

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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/modprobe.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
