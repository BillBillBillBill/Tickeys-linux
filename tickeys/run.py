#!/usr/bin/env python
# coding: utf-8
from logger import logger
import sys
import os
import commands

__version__ = '0.1.7'
import json
import requests

__author__ = 'Huang xiongbiao(billo@qq.com)'


def run_GUI():
    check_root()
    check_update()
    try:
        stat, terminalId = commands.getstatusoutput('xdotool getactivewindow')
        from GUI import TickeysApp
        if stat == 0:
            TickeysApp(terminalId).run()
        else:
            TickeysApp().run()

    except Exception, e:
        logger.info("Run GUI Fail, use CLI instead..Fail msg:%s" % str(e))
        run_CLI()


def run_CLI():
    check_root()
    check_update()
    from CLI import CLI
    CLI().cmdloop()


def check_root():
    logger.info("Root checking...")
    if os.getegid() != 0:
        logger.info("This program must be run as root..")
        sys.exit(0)
    logger.info("Root checking success..")
    logger.debug("File path:" + os.path.dirname(__file__))


def check_update():
    try:
        logger.debug("Version checking...")
        r = requests.get("http://billbill.sinaapp.com/tickeys")
        returnInfor = json.loads(r.text)
        # print returnInfor
        if returnInfor["version"] <= __version__:
            logger.debug("It is the latest version...")
            return
        else:
            # show update notify
            import pynotify
            pynotify.init('Tickeys')
            title = '<h2>Tickeys</h2>'
            body = '<span style="color: #00B8CB; font-size:15px">Tickeys</span>有可用的<span style="color: #FF4500">更新：</span>\n 版本：%s \n 内容：%s' % (returnInfor["version"], returnInfor["update"])
            iconfile = os.getcwd() + '/tickeys.png'
            notify = pynotify.Notification(title, body, iconfile)
            notify.show()
    except Exception, e:
        logger.error("Version check fail:" + str(e))


def main():
    logger.debug("Tickeys start........")
    if len(sys.argv) != 2 or sys.argv[1] not in ['-c', '-g']:
        print "Usage: python run.py -c     ---CLI mode"
        print "       python run.py -g     ---GUI mode"
        if len(sys.argv) == 1:
            run_GUI()
        sys.exit(0)
    if sys.argv[1] == '-g':
        del sys.argv[1]  # otherwise kivy would regard it as option
        run_GUI()
    else:
        run_CLI()

if __name__ == '__main__':
    main()
