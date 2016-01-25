#!/usr/bin/env python
# coding: utf-8
from pygame import mixer
from logger import logger
from config import Configer
import json
import os

__author__ = 'Huang xiongbiao(billo@qq.com)'


class SoundPlayer():

    def __init__(self):
        try:
            os.chdir(os.path.dirname(__file__))
        except Exception:
            pass
        self.mixer = mixer
        self.mixer.init(frequency=22050)
        self.schemes = dict(
            (i['name'], i)
            for i in json.load(file('./Resources/data/schemes.json')))
        self.Configer = Configer()
        self.soundFileList = self.schemes[self.Configer.style]['files']
        self.key_audio_map = self.schemes[self.Configer.style]['key_audio_map']
        self.non_unique_count = self.schemes[self.Configer.style]['non_unique_count']
        self.set_pitch(self.Configer.pitch)
        self.changing = False  # avoiding play sound while caching
        self.soundEffectCache = []
        self.cache_sound_effect()

    # preload sound effect
    def cache_sound_effect(self):
        try:
            self.changing = True
            self.mixer.quit()
            self.mixer.init(frequency=int(self.adjustPitch*22050))
            self.soundEffectCache = []
            for effectFile in self.soundFileList:
                soundFile = './Resources/data/%s/%s' % \
                    (self.Configer.style, effectFile)
                logger.debug('Load sound file:' + soundFile)
                self.soundEffectCache.append(self.mixer.Sound(soundFile))
            self.set_volume(self.Configer.volume)

        except Exception, e:
            logger.error('Load sound files fail:' + str(e))
        finally:
            self.changing = False

    def save_config(func):
        def _deco(*arg):
            ret = func(*arg)
            arg[0].Configer.save_config()
            return ret
        return _deco

    @save_config
    def set_style(self, style):
        try:
            if self.Configer.style == style:
                return
            self.Configer.style = style
            self.soundFileList = self.schemes[self.Configer.style]['files']
            self.key_audio_map = self.schemes[self.Configer.style]['key_audio_map']
            self.non_unique_count = self.schemes[self.Configer.style]['non_unique_count']
            self.cache_sound_effect()
        except Exception, e:
            logger.error(e)

    @save_config
    def set_volume(self, volume):
        self.Configer.volume = volume
        for soundEffect in self.soundEffectCache:
            soundEffect.set_volume(self.Configer.volume)

    # May raise nonfluency when init the mixer
    @save_config
    def set_pitch(self, pitch):
        # if abs(self.mixer.get_init()[0]/22050.0 - pitch) < 0.1:
        #     return
        # it's weird
        self.Configer.pitch = pitch
        self.adjustPitch = 0.65 + 0.3 * pitch if pitch < 1 else pitch + 0.9
        self.cache_sound_effect()

    def get_infor(self):
        return {
            'style': self.Configer.style,
            'volume': self.Configer.volume,
            'pitch': self.Configer.pitch,
        }

    def play(self, key):

        if not self.key_audio_map.get(str(key)):
            self.key_audio_map[str(key)] = key % self.non_unique_count

        # avoid the situation that play sound while caching
        while self.changing:
            continue

        self.soundEffectCache[self.key_audio_map[str(key)]].play()
        # dir(self.soundEffectCache[self.key_audio_map[str(key)]])
