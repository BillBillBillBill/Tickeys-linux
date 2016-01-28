#!/bin/bash

echo "Creating tickeys.deb"
#Creating a .deb..
mkdir -p tickeys/usr/local/bin
mkdir -p tickeys/usr/share/applications
mkdir -p tickeys/usr/share/app-install/desktop
mkdir -p tickeys/usr/share/Tickeys/icons
mkdir -p tickeys/DEBIAN

cp tickeys.png tickeys/usr/share/Tickeys/icons/tickeys.png

deb_control="Source: Tickeys
Priority: extra
Maintainer: Bill <billo@qq.com>
Author: Bill <billo@qq.com>
Build-Depends: debhelper (>= 8.0.0)
Standards-Version: 3.9.2
Package: tickeys
Version: 0.2.3
Architecture: i386
Installed-Size: 32253411
Description: Instant audio feedback when typing, For Linux. (https://github.com/BillBillBillBill/Tickeys-linux)
"

echo "$deb_control" > tickeys/DEBIAN/control
chown root tickeys/DEBIAN/control

desktop="#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Categories=Application;
Exec=gksu /usr/local/bin/Tickeys
Icon=/usr/share/Tickeys/icons/tickeys.png
Terminal=false
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
"

echo "$desktop" >  tickeys/usr/share/applications/Tickeys.desktop
chmod a+x tickeys/usr/share/applications/Tickeys.desktop
chown root tickeys/usr/share/applications/Tickeys.desktop

echo "$desktop" >  tickeys/usr/share/app-install/desktop/Tickeys.desktop
chmod a+x tickeys/usr/share/app-install/desktop/Tickeys.desktop
chown root tickeys/usr/share/app-install/desktop/Tickeys.desktop

cp Tickeys tickeys/usr/local/bin/Tickeys

dpkg-deb -z9 -b tickeys


echo "ok."
