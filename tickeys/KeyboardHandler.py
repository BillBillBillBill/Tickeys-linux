#!/usr/bin/env python
# coding: utf-8
import os
import threading
from evdev import InputDevice
from select import select
from SoundPlayer import SoundPlayer
from logger import logger
import commands

__author__ = 'Huang xiongbiao(billo@qq.com)'

# input device file path
deviceFilePath = '/sys/class/input/'


class KeyboardHandler():

    def __init__(self):
        logger.debug("Keyboard deteccter created.")
        self.keyboardList = self.findKeyboard()
        self.threads = []
        self.inputRecord = []
        self.hotKey = [16, 30, 44, 2, 3, 4]  # QAZ123
        self.sp = SoundPlayer()
        self.GUIID = None

    # list all event's name and its device
    def showDevice(self):
        # os.chdir(deviceFilePath)
        for i in os.listdir(deviceFilePath):
            namePath = deviceFilePath + i + '/device/name'
            if os.path.isfile(namePath):
                logger.info("Name: %s Device: %s" % (i, file(namePath).read()))

    def setStyle(self, style):
        self.sp.setStyle(style)

    def setVolume(self, volume):
        self.sp.setVolume(volume)

    def setPitch(self, pitch):
        self.sp.setPitch(pitch)

    @property
    def GUIID(self):
        return self.GUIID

    def showGUI(self):
        if not self.GUIID:
            return
        command = "xdotool windowactivate --sync %s" % self.GUIID
        commands.getstatusoutput(command)

    # return with a list of keyboard's event
    def findKeyboard(self):
        # os.chdir(deviceFilePath)
        keyboardList = []
        for event in os.listdir(deviceFilePath):
            namePath = deviceFilePath + event + '/device/name'
            namePathExist = os.path.isfile(namePath)
            deviceName = file(namePath).read().lower() if namePathExist else None

            if deviceName and deviceName.find('keyboard') != -1:
                keyboardList.append(event)
                continue

            # check other USB device
            bustypePath = deviceFilePath + event + '/device/id/bustype'
            bustypePathExist = os.path.isfile(bustypePath)
            bustype = file(bustypePath).read() if bustypePathExist else None
            # 0003 = USB device, consider it !mouse = keyboard :)
            isUSBKB = bustype and bustype.find('0003') != -1 and \
                deviceName and deviceName.find('mouse') == -1
            if isUSBKB:
                keyboardList.append(event)

        try:
            logger.debug(keyboardList)
            assert len(keyboardList) > 0
        except AssertionError:
            logger.error("Keyborad Not Found!!")

        return keyboardList

    # event.value:1 for pressed, 0 for release
    def detectInputKey(self, eventName):
        dev = InputDevice('/dev/input/' + eventName)
        while True:
            select([dev], [], [])
            for event in dev.read():
                if (event.value == 1 or event.value == 0) and event.code != 0:
                    if event.value == 1:
                        self.sp.play(event.code)
                        self.checkShowWindow(event.code)
                    logger.debug(
                        "Key: %s Status: %s" %
                        (event.code, "pressed" if event.value else "release"))

    # check input if satisfy the hotkey
    def checkShowWindow(self, keycode):
        if len(self.inputRecord) > 0 and keycode == self.inputRecord[-1]:
            return
        if keycode == self.hotKey[len(self.inputRecord)]:
            self.inputRecord.append(keycode)
            logger.debug(self.inputRecord)
            if len(self.inputRecord) == 6:
                self.showGUI()
                self.inputRecord = []
        else:
            self.inputRecord = []

    def startDetecting(self):

        for i in self.keyboardList:
            t = threading.Thread(target=self.detectInputKey, args=(i,))
            self.threads.append(t)
            t.start()

    # kill all threads
    def stopDetecting(self):
        for t in self.threads:
            t._Thread__stop()

if __name__ == '__main__':
    detecter = KeyboardHandler()
    detecter.startDetecting()
