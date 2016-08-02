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
        self.detect_keyboard_list = self.find_keyboard()
        self.threads = []
        self.input_record_list = []
        self.hot_key_list = [16, 30, 44, 2, 3, 4]      # QAZ123
        self.hot_key_list2 = [16, 30, 44, 79, 80, 81]  # QAZ123 with 123 in side keyboard
        self.sp = SoundPlayer()
        self.show_device()

    # list all event's name and its device and record it
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

    # return with a list of keyboard's event
    def find_keyboard(self):
        keyboard_list = []

        device_info = open('/proc/bus/input/devices').read().lower().split('\n\n')
        logger.debug("/proc/bus/input/devices:%s" % device_info)
        exclude_pattern = 'touch|web|cam|hdmi|button|mic|phone|speak|mouse|track|point|pad'
        for i in filter(
            lambda i:
                (not re.search(exclude_pattern, i) and
                re.search('bus=0003', i)) or re.search('keyboard', i),
                device_info
        ):
            m = re.search('event\d+', i)
            if m:
                keyboard_list.append(m.group())
        assert len(keyboard_list) > 0
        logger.debug("Keyboard list: %s" % keyboard_list)
        return keyboard_list

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
    def check_show_window(self, key_code):
        if self.input_record_list and key_code == self.input_record_list[-1]:
            return
        input_record_length = len(self.input_record_list)
        next_key_code = self.hot_key_list[input_record_length]
        next_key_code2 = self.hot_key_list2[input_record_length]
        if key_code == next_key_code or key_code == next_key_code2:
            self.input_record_list.append(key_code)
            if input_record_length == 5:
                show_GUI()
                self.input_record_list = []
        else:
            # clear the record if not satisfy
            self.input_record_list = []

    def start_detecting(self):

        for i in self.detect_keyboard_list:
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
