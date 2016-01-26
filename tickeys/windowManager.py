# coding: utf-8
import commands

from logger import logger


def save_terminal_window_id():
    try:
        stat, terminalId = commands.getstatusoutput('xdotool getactivewindow')
        assert stat == 0
        with open("/tmp/tickeys_terminal_window_id", "w+") as f:
            f.write(terminalId)
    except Exception, e:
        logger.error("Save terminal window id fail:" + str(e))


def read_terminal_window_id():
    with open("/tmp/tickeys_terminal_window_id", "r") as f:
        return f.read()


def hide_terminal():
    try:
        terminalId = read_terminal_window_id()
        if not terminalId:
            return
        commands.getstatusoutput(
            "xdotool windowactivate --sync %s" % terminalId)
        commands.getstatusoutput(
            "xdotool getactivewindow windowunmap")
    except Exception,e:
        logger.error(str(e))


def save_GUI_window_id():
    try:
        stat, GUIID = commands.getstatusoutput('xdotool getactivewindow')
        assert stat == 0
        with open("/tmp/tickeys_GUI_window_id", "w+") as f:
            f.write(GUIID)
    except Exception, e:
        logger.error("Save GUI window id fail:" + str(e))


def read_GUI_window_id():
    with open("/tmp/tickeys_GUI_window_id", "r") as f:
        return f.read()


def hide_GUI():
    try:
        GUIID = read_GUI_window_id()
        commands.getstatusoutput(
                'xdotool windowunmap --sync %s' % GUIID)
    except Exception,e:
        logger.error(str(e))


def show_GUI():
    try:
        GUIID = read_GUI_window_id()
        if not GUIID:
            return
        # read window ids
        command = "xdotool windowmap --sync %s && xdotool windowactivate --sync %s" % (GUIID, GUIID)
        stat, output = commands.getstatusoutput(command)
        return str(stat)
    except Exception, e:
        logger.error(str(e))
        return '256'

def check_tickeys_running_status():
    save_terminal_window_id()
    stat = show_GUI()
    if stat != "0":
        return False
    else:
        print "Tickeys is already running, show it"
        return True
