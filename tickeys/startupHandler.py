#!/usr/bin/env python
# coding:utf-8

from __future__ import with_statement
from logger import logger
import os
import commands
from config import configer


executable_filename = "tickeys"
python2 = os.popen('python2 -V 2>&1').read().startswith('Python 2.') and 'python2' or 'python'
DesktopEntryName = 'Tickeys.desktop'
StartupPath = ['/etc/xdg/autostart', '~/.config/autostart', '~/.config/openbox/autostart']


def check_startup_file():
    return bool(configer.autostart)


def delete_startup_linux():
    try:
        command_list = []
        for dirname in map(os.path.expanduser, StartupPath):
            command_list.append("rm %s/%s" % (dirname, DesktopEntryName))
        command_str = " | ".join(command_list)
        command = "gksudo --message password " + command_str
        commands.getstatusoutput(command)
        configer.autostart = False
        configer.save_config()
    except Exception, e:
        logger.debug("Delete startup fail:" + str(e))
        return False
    return True


def command_exist(command='gksu'):
    command += ' --help'
    try:
        if commands.getstatusoutput(command)[0] != 32512:
            logger.debug(command + " exist")
            return True
        else:
            logger.debug(command + " dosen't exist")
            return False
    except Exception:
        logger.debug(command + " dosen't exist")
        return False


def add_startup_linux():
    filename = os.path.abspath(__file__)
    dirname = os.path.dirname(filename)

    if os.path.exists("/usr/share/applications/Tickeys.desktop"):
        # install by deb
        with open("/usr/share/applications/Tickeys.desktop") as f:
            DESKTOP_FILE = f.read()
    elif command_exist('tickeys'):
        # used pip installed
        DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Application;
Exec=tickeys
Icon=%s/tickeys.png
Terminal=true
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
''' % dirname
    else:
        # not install yet(run in py)
        DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Application;
Path=%s
Exec=python run.py
Terminal=true
Icon=%s/tickeys.png
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
''' % (dirname, dirname)
    try:
        # it is stupid
        command_list = []
        for dirname in map(os.path.expanduser, StartupPath):
            filename = os.path.join(dirname, DesktopEntryName)
            command_list.append('"mkdir -p %s"' % dirname)
            command_list.append('echo "%s" >> %s' % (DESKTOP_FILE, filename))
            command_list.append('chmod 777 %s' % filename)
        command_str = " | ".join(command_list)
        command = "gksudo --message password " + command_str
        commands.getstatusoutput(command)
        configer.autostart = True
        configer.save_config()
    except Exception, e:
        print e
        logger.debug("Add to startup fail:" + str(e))
        return False
    return True
