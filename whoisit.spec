%define _requires_exceptions perl\(MyAsterisk\)

Summary:	Facilities to Announce incoming callers over the computer speakers 
Name:		whoisit
Version:	1.1
Release:	%mkrel 4
License:	GPL
Group:		System/Servers
URL:		http://www.voip-info.org/wiki-Asterisk+WhoIsIt
Source0:	http://wyoming.e-tools.com/WhoIsIt-%{version}.tar.bz2
Requires:	asterisk
Requires:	festival
BuildRequires:	sox
BuildRequires:	festival
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This program is intended to be used in the Asterisk
extensions.conf file to announce (over your system's speakers) the
calling party. 

%prep

%setup -q -n WhoIsIt-%{version}

%build

gcc %{optflags} -o who-is-it who-is-it.c
gcc %{optflags} -o who-is-it-agi who-is-it-agi.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_localstatedir}/lib/asterisk/agi-bin
install -d %{buildroot}%{_localstatedir}/lib/asterisk/sounds/CID-PLACES/country-codes
install -d %{buildroot}%{_localstatedir}/lib/asterisk/sounds/priv-callerintros

install -m0644 international.gsm %{buildroot}%{_localstatedir}/lib/asterisk/sounds/CID-PLACES/
install -m0644 priv-unlisted.gsm %{buildroot}%{_localstatedir}/lib/asterisk/sounds/
install -m0644 unknowncallerfrom.gsm %{buildroot}%{_localstatedir}/lib/asterisk/sounds/
install -m0644 somewhereinstate.gsm %{buildroot}%{_localstatedir}/lib/asterisk/sounds/
install -m0644 somewhereoutstate.gsm %{buildroot}%{_localstatedir}/lib/asterisk/sounds/
install -m0755 who-is-it %{buildroot}%{_bindir}
install -m0755 who-is-it-agi %{buildroot}%{_localstatedir}/lib/asterisk/agi-bin/
install -m0755 submit-announce.agi %{buildroot}%{_localstatedir}/lib/asterisk/agi-bin/

# this will generate the gsm files :)
cp areacodescript areacodescript.tmp
cp countrycodes-script countrycodes-script.tmp
perl -pi -e "s|%{_localstatedir}/lib|%{buildroot}%{_localstatedir}/lib|g" *.tmp

festival < areacodescript.tmp
festival < countrycodes-script.tmp

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO areacodescript countrycodes-script
%attr(0755,root,root) %{_bindir}/who-is-it
%attr(0755,root,root) %{_localstatedir}/lib/asterisk/agi-bin/who-is-it-agi
%attr(0755,root,root) %{_localstatedir}/lib/asterisk/agi-bin/submit-announce.agi
%attr(0755,root,root) %dir %{_localstatedir}/lib/asterisk/sounds/CID-PLACES
%attr(0755,root,root) %dir %{_localstatedir}/lib/asterisk/sounds/CID-PLACES/country-codes
%attr(0755,root,root) %dir %{_localstatedir}/lib/asterisk/sounds/priv-callerintros
%attr(0644,root,root) %{_localstatedir}/lib/asterisk/sounds/CID-PLACES/*.gsm
%attr(0644,root,root) %{_localstatedir}/lib/asterisk/sounds/CID-PLACES/country-codes/*.gsm
%attr(0644,root,root) %{_localstatedir}/lib/asterisk/sounds/*.gsm
