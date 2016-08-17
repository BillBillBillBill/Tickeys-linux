#!/usr/bin/env python
# coding: utf-8
import threading
from soundPlayer import SoundPlayer
from logger import logger
from pyxhook import HookManager
from windowManager import show_GUI

__author__ = 'Huang xiongbiao(billo@qq.com)'


class KeyboardHandler():

    def __init__(self):
        logger.debug("Keyboard deteccter created.")
        self.hm = HookManager()
        self.hm.KeyDown = self.key_down
        self.hm_thread = None
        self.input_record_list = []
        self.hot_key_list = [24, 38, 52, 10, 11, 12]      # QAZ123
        self.hot_key_list2 = [24, 38, 52, 87, 88, 89]  # QAZ123 with 123 in side keyboard
        self.sp = SoundPlayer()

    def set_style(self, style):
        self.sp.set_style(style)

    def set_volume(self, volume):
        self.sp.set_volume(volume)

    def set_pitch(self, pitch):
        self.sp.set_pitch(pitch)

    def get_player_infor(self):
        return self.sp.get_infor()

    def key_down(self, event):
        self.sp.play(event.ScanCode)
        self.check_show_window(event.ScanCode)
        # logger.debug(str(event))

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
        self.hm_thread = threading.Thread(target=self.hm.start, args=())
        self.hm_thread.start()

    # kill all threads
    def stop_detecting(self):
        self.hm_thread._Thread__stop()
        self.hm.cancel()

if __name__ == '__main__':
    detecter = KeyboardHandler()
    detecter.start_detecting()
