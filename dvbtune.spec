%define name	dvbtune
%define version 0.5
%define release	%mkrel 11

%define kernel_dir /usr/src/linux
%define kernel_inc %kernel_dir/include

Summary:	Tuning application for DVB cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://osdn.dl.sourceforge.net/dvbtools/%{name}-%{version}.tar.bz2
URL:		http://www.linuxstb.org
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
Prefix:		%{_prefix}
BuildRequires:	kernel-source
BuildRequires:	libxml2-devel
Requires(post):	update-alternatives

%description
DVBtune is a simple tuning application for DVB cards supported by the
Linux DVB driver (www.linuxtv.org).

%prep
%setup -q

%build
#UK
make INCS=-I%kernel_inc
make xml2vdr
install -m755 dvbtune dvbtune-uk
install -m755 xml2vdr dvb_xml2vdr-uk

make clean
#Finland
make INCS=-I%kernel_inc FINLAND=1
make FINLAND=1 xml2vdr
install -m755 dvbtune dvbtune-fin
install -m755 xml2vdr dvb_xml2vdr-fin

make clean

make INCS=-I%kernel_inc FINLAND2=1
make FINLAND2=1 xml2vdr
install -m755 dvbtune dvbtune-fin2
install -m755 xml2vdr dvb_xml2vdr-fin2


%install
rm -rf $RPM_BUILD_ROOT
install -d -m755 %buildroot%_bindir
install -m755 dvbtune-* %buildroot%_bindir/
install -m755 dvb_* %buildroot%_bindir/

install -d -m755 %buildroot%_libdir/%name
install -m755 scripts/* %buildroot%_libdir/%name/


echo "update-alternatives --install %_bindir/dvbtune dvbtune %_bindir/dvbtune-uk 30 \\" >> dvbtune-setup-alternatives.sh
echo "--slave  %_bindir/dvb_xml2vdr dvb_xml2vdr %_bindir/dvb_xml2vdr-uk \\" >> dvbtune-setup-alternatives.sh
echo >> dvbtune-setup-alternatives.sh

echo "update-alternatives --install %_bindir/dvbtune dvbtune %_bindir/dvbtune-fin 20 \\" >> dvbtune-setup-alternatives.sh
echo "--slave  %_bindir/dvb_xml2vdr dvb_xml2vdr %_bindir/dvb_xml2vdr-fin \\" >> dvbtune-setup-alternatives.sh
echo >> dvbtune-setup-alternatives.sh


echo "update-alternatives --install %_bindir/dvbtune dvbtune %_bindir/dvbtune-fin2 10 \\" >> dvbtune-setup-alternatives.sh
echo "--slave  %_bindir/dvb_xml2vdr dvb_xml2vdr %_bindir/dvb_xml2vdr-fin2 \\" >> dvbtune-setup-alternatives.sh
echo >> dvbtune-setup-alternatives.sh

%post -f dvbtune-setup-alternatives.sh

%postun
if [ $1 = 0 ]; then
	update-alternatives --remove dvbtune %_bindir/dvbtune-uk
	update-alternatives --remove dvbtune %_bindir/dvbtune-fin
	update-alternatives --remove dvbtune %_bindir/dvbtune-fin2
fi
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%_bindir/*
%dir %_libdir/%name
%_libdir/%name/*

