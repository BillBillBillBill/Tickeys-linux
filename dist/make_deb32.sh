#!/bin/bash

version=0.2.4
folder_name=tickeys_$version\_i386

echo "Creating $folder_name.deb"
#Creating a .deb..
mkdir -p $folder_name/usr/bin
mkdir -p $folder_name/usr/local/bin
mkdir -p $folder_name/usr/share/applications
mkdir -p $folder_name/usr/share/app-install/desktop
mkdir -p $folder_name/usr/share/Tickeys/icons
mkdir -p $folder_name/DEBIAN

chmod -R 0755 $folder_name/DEBIAN
cp postrm $folder_name/DEBIAN/postrm
chmod -R 0755 $folder_name/DEBIAN/postrm
cp postinst $folder_name/DEBIAN/postinst
chmod -R 0755 $folder_name/DEBIAN/postinst

cp tickeys.png $folder_name/usr/share/Tickeys/icons/tickeys.png

deb_control="Source: $folder_name
Priority: extra
Maintainer: Bill <billo@qq.com>
Author: Bill <billo@qq.com>
Build-Depends: debhelper (>= 8.0.0)
Depends: xdotool(>= 2), gksu
Standards-Version: 3.9.2
Package: tickeys
Version: $version
Section: misc
Homepage: https://github.com/BillBillBillBill/Tickeys-linux
Architecture: i386
Installed-Size: 32253
Description: Tickeys是一款很强大的键盘音效软件。
 Tickeys 自带了多种声音效果方案，有打字机、冒泡、机械键盘、剑气等。
 每天都听着键盘声音是不是很烦闷，现在有了这款神器你就可以瞬间帮助自己的键盘加上逼格特效。
 项目主页：https://github.com/BillBillBillBill/Tickeys-linux
"

echo "$deb_control" > $folder_name/DEBIAN/control
chown root $folder_name/DEBIAN/control

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

echo "$desktop" >  $folder_name/usr/share/applications/Tickeys.desktop
chmod a+x $folder_name/usr/share/applications/Tickeys.desktop
chown root $folder_name/usr/share/applications/Tickeys.desktop

echo "$desktop" >  $folder_name/usr/share/app-install/desktop/Tickeys.desktop
chmod a+x $folder_name/usr/share/app-install/desktop/Tickeys.desktop
chown root $folder_name/usr/share/app-install/desktop/Tickeys.desktop

cp Tickeys $folder_name/usr/local/bin/Tickeys
ln -s /usr/local/bin/Tickeys $folder_name/usr/bin/tickeys

dpkg-deb -z9 -b $folder_name

echo "ok."
