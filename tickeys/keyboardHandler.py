#!/usr/bin/env python
# coding: utf-8
import os
import re
import threading
from evdev import InputDevice
from select import select
from soundPlayer import SoundPlayer
from logger import logger

from windowManager import show_GUI

__author__ = 'Huang xiongbiao(billo@qq.com)'

# input device file path
deviceFilePath = '/sys/class/input/'


class KeyboardHandler():

    def __init__(self):
        logger.debug("Keyboard deteccter created.")
        self.keyboardList = self.find_keyboard()
        self.threads = []
        self.inputRecord = []
        self.hotKey = [16, 30, 44, 2, 3, 4]  # QAZ123
        self.sp = SoundPlayer()
        self.show_device()

    # list all event's name and its device
    def show_device(self):
        # os.chdir(deviceFilePath)
        logger.debug("List all device")
        for i in os.listdir(deviceFilePath):
            namePath = deviceFilePath + i + '/device/name'
            if os.path.isfile(namePath):
                logger.debug("Name: %s Device: %s" % (i, file(namePath).read()))

    def set_style(self, style):
        self.sp.set_style(style)

    def set_volume(self, volume):
        self.sp.set_volume(volume)

    def set_pitch(self, pitch):
        self.sp.set_pitch(pitch)

    def get_player_infor(self):
        return self.sp.get_infor()

    # new way to find keyboard
    # return with a list of keyboard's event
    def find_keyboard(self):
        keyboardList = []

        deviceInfo = open('/proc/bus/input/devices').read().lower().split('\n\n')
        for i in filter(lambda i: not re.search('touch|web|cam|hdmi|button|mic|phone', i) and
            ((not re.search('mouse', i) and re.search('bus=0003', i)) or re.search('keyboard', i))
            , deviceInfo):
            m = re.search('event\d+', i)
            if m:
                keyboardList.append(m.group())
        assert len(keyboardList) > 0
        logger.debug("keyboard list: %s" % keyboardList)
        return keyboardList

    # return with a list of keyboard's event
    # def find_keyboard(self):
    #     # os.chdir(deviceFilePath)
    #     keyboardList = []
    #     for event in os.listdir(deviceFilePath):
    #         namePath = deviceFilePath + event + '/device/name'
    #         namePathExist = os.path.isfile(namePath)
    #         deviceName = file(namePath).read().lower() if namePathExist else None

    #         if deviceName and deviceName.find('keyboard') != -1:
    #             keyboardList.append(event)
    #             continue

    #         # check other USB device
    #         bustypePath = deviceFilePath + event + '/device/id/bustype'
    #         bustypePathExist = os.path.isfile(bustypePath)
    #         bustype = file(bustypePath).read() if bustypePathExist else None
    #         # 0003 = USB device, consider it !mouse = keyboard :)
    #         isUSBKB = bustype and bustype.find('0003') != -1 and \
    #             deviceName and deviceName.find('mouse') == -1
    #         if isUSBKB:
    #             keyboardList.append(event)

    #     try:
    #         logger.debug(keyboardList)
    #         assert len(keyboardList) > 0
    #     except AssertionError:
    #         logger.error("Keyborad Not Found!!")
    #     return keyboardList

    # event.value:1 for pressed, 0 for release
    def detect_input_from_event(self, eventName):
        dev = InputDevice('/dev/input/' + eventName)
        while True:
            select([dev], [], [])
            for event in dev.read():
                if (event.value == 1 or event.value == 0) and event.code != 0:
                    if event.value == 1:
                        self.sp.play(event.code)
                        self.check_show_window(event.code)
                    logger.debug(
                        "Key: %s Status: %s" %
                        (event.code, "pressed" if event.value else "release"))

    # check input if satisfy the hotkey
    def check_show_window(self, keycode):
        if len(self.inputRecord) > 0 and keycode == self.inputRecord[-1]:
            return
        if keycode == self.hotKey[len(self.inputRecord)]:
            self.inputRecord.append(keycode)
            logger.debug(self.inputRecord)
            if len(self.inputRecord) == 6:
                show_GUI()
                self.inputRecord = []
        else:
            self.inputRecord = []

    def start_detecting(self):

        for i in self.keyboardList:
            t = threading.Thread(target=self.detect_input_from_event, args=(i,))
            self.threads.append(t)
            t.start()

    # kill all threads
    def stop_detecting(self):
        for t in self.threads:
            t._Thread__stop()

if __name__ == '__main__':
    detecter = KeyboardHandler()
    detecter.start_detecting()
