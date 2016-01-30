#!/usr/bin/env python
# coding: utf-8
from logger import logger
import sys
import os

from windowManager import check_tickeys_running_status

__author__ = 'Huang xiongbiao(billo@qq.com)'


def run_GUI():
    check_root()
    check_system()
    try:
        from GUI import TickeysApp
        TickeysApp().run()
    except Exception, e:
        logger.exception(e)
        logger.error("Run GUI Fail, reason:")
        os._exit(0)


def check_root():
    logger.info("Root checking...")
    if os.getegid() != 0:
        logger.info("This program must be run as root..")
        sys.exit(0)
    logger.info("Root checking success. You have the root permission")
    logger.debug("File path:" + os.path.dirname(__file__))

def check_system():
    systems = ['Linux', 'SunOS', 'FreeBSD', 'Unix', 'OpenBSD', 'NetBSD']
    try:
        logger.info("System checking...")
        import platform
        system_name = platform.system()
        if system_name not in systems:
            logger.error("System %s is not supported." % system_name)
            sys.exit(0)
        else:
            logger.info("System checking success. Your system is supported")
    except Exception, e:
        logger.error("System checking fail:")
        logger.exception(e)
        sys.exit(0)


def main():
    logger.debug("Tickeys start........")
    is_running = check_tickeys_running_status()
    if is_running:
        return
    run_GUI()

if __name__ == '__main__':
    main()
