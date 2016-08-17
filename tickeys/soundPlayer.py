#!/usr/bin/env python
# coding: utf-8
import soundfile as sf
import sounddevice as sd
import threading
from logger import logger
from config import configer
import json
import os


__author__ = 'Huang xiongbiao(billo@qq.com)'


class SoundPlayer():

    def __init__(self):
        try:
            os.chdir(os.path.dirname(__file__))
        except Exception:
            pass
        self.schemes = dict(
            (i['name'], i)
            for i in json.load(file('./Resources/data/schemes.json')))
        self.configer = configer
        self.sound_file_list = self.schemes[self.configer.style]['files']
        self.key_audio_map = self.schemes[self.configer.style]['key_audio_map']
        self.non_unique_count = self.schemes[self.configer.style]['non_unique_count']
        self.sound_effect_cache = []
        self.channel = 1
        self.cache_sound_effect()

    # preload sound effect
    def cache_sound_effect(self):
        try:
            new_sound_effect_cache = []
            for effect_file in self.sound_file_list:
                sound_file = './Resources/data/%s/%s' % \
                    (self.configer.style, effect_file)
                logger.debug('Load sound file:' + sound_file)
                data, fs = sf.read(sound_file)
                new_sound_effect_cache.append((data, fs))
            self.sound_effect_cache = new_sound_effect_cache

        except Exception, e:
            logger.error('Load sound files fail:' + str(e))

    def save_config(func):
        def _deco(*arg):
            ret = func(*arg)
            arg[0].configer.save_config()
            return ret
        return _deco

    @save_config
    def set_style(self, style):
        try:
            if self.configer.style == style:
                return
            self.configer.style = style
            self.sound_file_list = self.schemes[style]['files']
            self.key_audio_map = self.schemes[style]['key_audio_map']
            self.non_unique_count = self.schemes[style]['non_unique_count']
            self.cache_sound_effect()
        except Exception, e:
            logger.error(e)

    @save_config
    def set_volume(self, volume):
        self.configer.volume = volume

    @save_config
    def set_pitch(self, pitch):
        self.configer.pitch = pitch

    def get_infor(self):
        return {
            'style': self.configer.style,
            'volume': self.configer.volume,
            'pitch': self.configer.pitch,
        }

    def play(self, key):
        if not self.key_audio_map.get(str(key)):
            self.key_audio_map[str(key)] = key % self.non_unique_count
        data, fs = self.sound_effect_cache[self.key_audio_map[str(key)]]
        data = data * self.configer.volume
        fs = fs * self.configer.pitch
        threading.Thread(target=sd.play, args=(data, fs)).start()
