#!/usr/bin/env python
# coding: utf-8
import cmd
from keyboardHandler import KeyboardHandler
from __init__ import __version__
import sys
reload(sys)

sys.setdefaultencoding("utf-8")


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = "Tickeys %s - Linux\nType 'help' for help" % __version__
        self.prompt = ">>> "
        self.detecter = KeyboardHandler()
        self.detecter.start_detecting()

        self.volume = self.detecter.get_player_infor()['volume'] * 100.0
        self.pitch = self.detecter.get_player_infor()['pitch'] * 10.0
        self.style = self.detecter.get_player_infor()['style']

    def default(self, line):
        print "Command '%s' is invalid, try 'help'" % line

    def help_setstyle(self):
        print "Set style, change the sound's effect"

    def do_setstyle(self, arg):
        style_index = raw_input(
            "Input the effect style number you want"
            "(0:bubble 1:mechanical 2:sword 3:typewriter 4:Cherry_G80_3000 5:Cherry_G80_3494 6:drum):")
        style_list = ['bubble', 'mechanical', 'sword', 'typewriter', 'Cherry_G80_3000', 'Cherry_G80_3494', 'drum']

        try:
            style_index = int(style_index)
            assert(0 <= style_index <= 6)
        except Exception:
            print "Input must between 0~6!!"
            return

        self.style = style_list[style_index]
        self.detecter.set_style(self.style)

    def help_setvol(self):
        print "Set volume, input the volume you want"

    def do_setvol(self, arg):
        volume = raw_input("Input the volume(0~100) you want:")

        try:
            volume = float(volume)
            assert(0 <= volume <= 100)
        except Exception:
            print "Volume must between 0~100!!"
            return

        self.volume = volume
        self.detecter.set_volume(self.volume/100.0)

    # def help_getvol(self):
    #     print "Get the volume"

    # def do_getvol(self, arg):
    #     print self.volume

    def help_setpitch(self):
        print "Set pitch, input the pitch you want"

    def do_setpitch(self, arg):
        pitch = raw_input("Input the pitch(0~30, default 10) you want:")

        try:
            pitch = float(pitch)
            assert(0 <= pitch <= 30)
        except Exception:
            print "Pitch must between 0~30!!"
            return

        self.pitch = pitch
        self.detecter.set_pitch(self.pitch/10.0)

    # def help_getpitch(self):
    #     print "Get the pitch"

    # def do_getpitch(self, arg):
    #     print self.pitch

    def help_getinfo(self):
        print "Get tickeys' sound effect, volume and pitch"

    def do_getinfo(self, arg):
        print "Sound effect: %s  Volume: %s  Pitch: %s" \
            % (self.style, self.volume, self.pitch)

    def do_quit(self, arg):
        try:
            self.detecter.stop_detecting()
        except Exception:
            pass
        finally:
            sys.exit(0)
            return True


if __name__ == "__main__":
    cli = CLI()
    cli.cmdloop()
