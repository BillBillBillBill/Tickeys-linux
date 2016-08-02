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

    def init_config(self):
        self.style = 'mechanical'
        self.volume = 1.0
        self.pitch = 1.0
        self.lang = 'en_US'
        self.save_config()

    def read_config(self):
        try:
            config_path = [
                "/usr/share/Tickeys",
                "/usr/share/Tickeys/config",
                "/usr/share/Tickeys/config/tickeys.conf"
            ]
            if not all([os.path.exists(cp) for cp in config_path]):
                if not os.path.exists("/usr/share/Tickeys"):
                    os.mkdir("/usr/share/Tickeys")
                if not os.path.exists("/usr/share/Tickeys/config"):
                    os.mkdir("/usr/share/Tickeys/config")
                self.init_config()
            else:
                self.cf.read('/usr/share/Tickeys/config/tickeys.conf')
                self.volume = self.cf.getfloat('options', 'volume')
                self.pitch = self.cf.getfloat('options', 'pitch')
                self.style = self.cf.get('options', 'style')
                self.lang = self.cf.get('options', 'lang') if 'lang' in self.cf.options("options") else "en_US"
        except Exception, e:
            logger.debug(e)

    def save_config(self):
        if not self.cf.sections():
            self.cf.add_section('options')
        self.cf.set('options', 'volume', self.volume)
        self.cf.set('options', 'pitch', self.pitch)
        self.cf.set('options', 'style', self.style)
        self.cf.set('options', 'lang', self.lang)

        with open('/usr/share/Tickeys/config/tickeys.conf', 'w') as f:
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
