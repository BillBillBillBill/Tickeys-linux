#!/usr/bin/env python
#coding: utf-8
import sys
import os
import commands

__author__ = 'Huang xiongbiao(billo@qq.com)'


def runInGUI():
    try:
        stat, terminalId = commands.getstatusoutput('xdotool getactivewindow')
        from GUI import TickeysApp
        if stat == 0:
            TickeysApp(terminalId).run()
        else:
            TickeysApp().run()

    except Exception, e:
        print "Run GUI Fail, use CLI instead..Fail msg:%s" % str(e)
        runInCLI()


def runInCLI():
    from CLI import CLI
    CLI().cmdloop()


def checkRoot():
    print "Root checking..."
    if os.getegid() != 0:
        print "This program must be run as root.."
        sys.exit(0)
    print "Root checking success.."


if __name__ == '__main__':
    checkRoot()
    if len(sys.argv) != 2 or sys.argv[1] not in ['-c', '-g']:
        print "Usage: python run.py -c     ---CLI mode"
        print "       python run.py -g     ---GUI mode"
        if len(sys.argv) == 1:
            runInGUI()
        sys.exit(0)
    if sys.argv[1] == '-g':
        del sys.argv[1]  # otherwise kivy would regard it as option
        runInGUI()
    else:
        runInCLI()
