%define name	dvbtune
%define version 0.5
%define release	%mkrel 14

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



%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5-13mdv2011.0
+ Revision: 663897
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-12mdv2011.0
+ Revision: 604834
- rebuild

* Tue Mar 09 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.5-11mdv2010.1
+ Revision: 517047
- add missing Requires(post) on update-alternatives

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5-10mdv2010.0
+ Revision: 413413
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.5-9mdv2009.1
+ Revision: 350885
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.5-8mdv2009.0
+ Revision: 220711
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.5-7mdv2008.1
+ Revision: 170804
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 0.5-6mdv2008.1
+ Revision: 149682
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 0.5-5mdv2008.0
+ Revision: 18865
- clean spec, rebuild for new era


* Wed May 25 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.5-4mdk
- add BuildRequires: libxml2-devel

* Tue Jun 08 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-3mdk
- initial contrib

* Sun Apr 04 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-2mdk
- fix group
- rename spec to dvbtune (!dvbtune2)
  update-alternatives should be working :-)

* Sun Apr 04 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-1mdk
- initial build for club

