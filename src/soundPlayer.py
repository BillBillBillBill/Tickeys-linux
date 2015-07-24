#!/usr/bin/env python
#coding: utf-8
from pygame import mixer
import json
from logger import logger

__author__ = 'Huang xiongbiao(billo@qq.com)'


class soundPlayer():

    def __init__(self):
        mixer.init()
        self.config = dict((i['name'], i) for i in json.load(file('../Resources/data/schemes.json')))
        self.style = 'bubble'
        self.soundFileList = self.config[self.style]['files']
        self.key_audio_map = self.config[self.style]['key_audio_map']
        self.non_unique_count = self.config[self.style]['non_unique_count']
        self.soundEffectCache = []
        self.volume = 1.0
        self.pitch = 1.0
        self.cacheSoundEffect()

    # preload sound effect
    def cacheSoundEffect(self):
        try:
            self.soundEffectCache = []

            for effectFile in self.soundFileList:
                soundFile = '../Resources/data/%s/%s' % (self.style, effectFile)
                logger.debug('Load sound file:' + soundFile)
                self.soundEffectCache.append(mixer.Sound(soundFile))

            self.setVolume(self.volume)
            self.setPitch(self.pitch)
        except Exception, e:
            logger.error('Load sound files fail:' + str(e))

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

    # with some bug to fix
    def setPitch(self, pitch):
        if abs(mixer.get_init()[0]/22050.0 - pitch) < 0.1:
            return
        mixer.quit()
        pitch = 0.6 + 0.4 * pitch if pitch < 1 else pitch
        self.pitch = pitch
        freq = int(pitch * 22050)
        mixer.init(frequency=freq)

    def play(self, key):

        if not self.key_audio_map.get(str(key)):
            self.key_audio_map[str(key)] = key % self.non_unique_count

        self.soundEffectCache[self.key_audio_map[str(key)]].play()
