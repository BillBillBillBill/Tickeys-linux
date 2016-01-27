#!/usr/bin/env python
# coding:utf-8

import os
import webbrowser
from windowManager import show_GUI

import pygtk
pygtk.require('2.0')

import gtk
gtk.gdk.threads_init()

try:
    import platform
    import appindicator
except:
    platform = None
    appindicator = None


class GtkTray():
    def __init__(self):
        logo_filename = 'tickeys.png'

        if platform and appindicator and platform.dist()[0].lower() == 'ubuntu':
            self.trayicon = self.ubuntu_trayicon(logo_filename)
        else:
            self.trayicon = self.gtk_trayicon(logo_filename)

    def ubuntu_trayicon(self, logo_filename):
        trayicon = appindicator.Indicator('Tickeys', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
        trayicon.set_status(appindicator.STATUS_ACTIVE)
        trayicon.set_attention_icon('indicator-messages-new')
        trayicon.set_icon(logo_filename)
        trayicon.set_menu(self.make_menu())

        return trayicon

    def gtk_trayicon(self, logo_filename):
        trayicon = gtk.StatusIcon()
        trayicon.set_from_file(logo_filename)

        trayicon.connect('popup-menu', lambda i, b, t: self.make_menu().popup(None, None, gtk.status_icon_position_menu, b, t, self.trayicon))
        trayicon.connect('activate', self.on_show)
        trayicon.set_tooltip('Tickeys')
        trayicon.set_visible(True)

        return trayicon

    def make_menu(self):
        menu = gtk.Menu()
        itemlist = [(u'显示界面', self.on_show),
                    (u'项目Github页', self.show_github_page),
                    (u'退出', self.on_quit)]
        for text, callback in itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)
        menu.show()
        return menu

    def on_show(self, widget=None, data=None):
        print "show the UI"
        show_GUI()

    def on_quit(self, widget, data=None):
        # module_init.stop_all()
        os._exit(0)
        gtk.main_quit()

    def show_github_page(self, widget=None, data=None):
        webbrowser.open_new("https://github.com/BillBillBillBill/Tickeys-linux")

    def serve_forever(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()


def main():
    sys_tray = GtkTray()
    sys_tray.serve_forever()

if __name__ == '__main__':
    main()
