#!/usr/bin/env python
# coding: utf-8
from pygame import mixer
from logger import logger
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
        self.config = dict(
            (i['name'], i)
            for i in json.load(file('./Resources/data/schemes.json')))
        self.style = 'bubble'
        self.soundFileList = self.config[self.style]['files']
        self.key_audio_map = self.config[self.style]['key_audio_map']
        self.non_unique_count = self.config[self.style]['non_unique_count']
        self.soundEffectCache = []
        self.volume = 1.0
        self.pitch = 1.0
        self.changing = False
        self.cacheSoundEffect()

    # preload sound effect
    def cacheSoundEffect(self):
        try:
            self.changing = True
            self.mixer.quit()
            self.mixer.init(frequency=int(self.pitch*22050))
            self.soundEffectCache = []
            for effectFile in self.soundFileList:
                soundFile = './Resources/data/%s/%s' % \
                    (self.style, effectFile)
                logger.debug('Load sound file:' + soundFile)
                self.soundEffectCache.append(self.mixer.Sound(soundFile))
            self.setVolume(self.volume)

        except Exception, e:
            logger.error('Load sound files fail:' + str(e))
        finally:
            self.changing = False

    def setStyle(self, style):
        try:
            if self.style == style:
                return
            self.style = style
            self.soundFileList = self.config[self.style]['files']
            self.key_audio_map = self.config[self.style]['key_audio_map']
            self.non_unique_count = self.config[self.style]['non_unique_count']
            self.cacheSoundEffect()
        except Exception, e:
            logger.error(e)

    def setVolume(self, volume):
        self.volume = volume
        for soundEffect in self.soundEffectCache:
            soundEffect.set_volume(self.volume)

    # May raise nonfluency when init the mixer
    def setPitch(self, pitch):
        # if abs(self.mixer.get_init()[0]/22050.0 - pitch) < 0.1:
        #     return
        # it's weird
        pitch = 0.65 + 0.3 * pitch if pitch < 1 else pitch + 0.9
        self.pitch = pitch
        self.cacheSoundEffect()

    def play(self, key):

        if not self.key_audio_map.get(str(key)):
            self.key_audio_map[str(key)] = key % self.non_unique_count

        # avoid the situation that play sound while caching
        while self.changing:
            continue

        self.soundEffectCache[self.key_audio_map[str(key)]].play()
        # dir(self.soundEffectCache[self.key_audio_map[str(key)]])
