#!/bin/bash
cp Tickeys /usr/bin/tickeys
chmod 0777 /usr/bin/tickeys
mkdir /usr/share/icons/Tickeys
cp tickeys.png /usr/share/icons/Tickeys/tickeys.png
cat>>Tickeys.desktop<<EOF
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Categories=Application;
Exec=gksu /usr/bin/tickeys
Icon=/usr/share/icons/Tickeys/tickeys.png
Terminal=true
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
EOF
cp Tickeys.desktop /usr/share/applications/Tickeys.desktop
echo Install tickeys success, use command tickeys to start it