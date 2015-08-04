import ConfigParser
import os
from logger import logger


class Configer():
    """docstring for Configer"""
    def __init__(self, *arg):
        try:
            os.chdir(os.path.dirname(__file__))
        except Exception:
            pass
        self.cf = ConfigParser.ConfigParser()
        self.read_config()

    def read_config(self):
        try:
            assert self.cf.read('tickeys.conf')
            self.volume = self.cf.getfloat('options', 'volume')
            self.pitch = self.cf.getfloat('options', 'pitch')
            self.style = self.cf.get('options', 'style')
        except Exception, e:
            logger.debug(e)
            self.style = 'mechanical'
            self.volume = 1.0
            self.pitch = 1.0
            self.save_config()

    def save_config(self):
        if not self.cf.sections():
            self.cf.add_section('options')
        self.cf.set('options', 'volume', self.volume)
        self.cf.set('options', 'pitch', self.pitch)
        self.cf.set('options', 'style', self.style)

        with open('tickeys.conf', 'w') as f:
            self.cf.write(f)

    @property
    def volume(self):
        return self.volume

    @property
    def pitch(self):
        return self.pitch

    @property
    def style(self):
        return self.style
