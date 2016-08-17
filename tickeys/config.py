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
        self.config_path = os.environ["HOME"] + "/.tickeys/tickeys.conf"
        self.cf = ConfigParser.ConfigParser()
        self.read_config()

    def init_config(self):
        self.style = 'mechanical'
        self.volume = 1.0
        self.pitch = 1.0
        self.lang = 'en_US'
        self.autostart = False
        self.save_config()

    def read_config(self):
        try:
            if not os.path.exists(self.config_path):
                self.init_config()
            else:
                self.cf.read(self.config_path)
                self.volume = self.cf.getfloat('options', 'volume')
                self.pitch = self.cf.getfloat('options', 'pitch')
                self.style = self.cf.get('options', 'style')
                self.autostart = self.cf.get('options', 'autostart')
                self.lang = self.cf.get('options', 'lang')
        except Exception, e:
            logger.debug(e)

    def save_config(self):
        if not self.cf.sections():
            self.cf.add_section('options')
        self.cf.set('options', 'volume', self.volume)
        self.cf.set('options', 'pitch', self.pitch)
        self.cf.set('options', 'style', self.style)
        self.cf.set('options', 'lang', self.lang)
        self.cf.set('options', 'autostart', self.autostart)

        with open(self.config_path, 'w') as f:
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

    @property
    def lang(self):
        return self.lang

    @property
    def autostart(self):
        return self.autostart

configer = Configer()
