#!/usr/bin/env python
# coding: utf-8
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from KeyboardHandler import KeyboardHandler
from kivy.lang import Builder
from StartupHandler import add_startup_linux, check_startup_file, delete_startup_linux
from __init__ import __version__

import sys
import commands
import webbrowser
reload(sys)
sys.setdefaultencoding("utf-8")

Builder.load_string('''
<Main>:
    pos: 0,0
    padding: 50
    rows: 6
    row_force_default: True
    row_default_height: 50
    spacing: 50
    orientation: 'vertical'

    canvas:
        Color:
            rgb: 0.42, 0.42, 0.42, 1
        Rectangle:
            pos: 0,0
            size: self.size
    Label:
        bold: True
        text: 'Tickeys'
        font_size: 42
        size_hint_y: None

    SpinnerRow
    AdjustVol
    AdjustPitch
    ExitAndSwitchRow

    InforRow


<AdjustVol>
    Label:
        bold: True
        color: 1, 1, 1, 1
        font_size: 25
        size_hint_x: None
        width: 250
        text: 'Vol:'
    Slider:
        min: 0.0
        max: 1.0
        value: 1.0
        width: 300
        on_value: root.setVolume(self.value)

<AdjustPitch>
    Label:
        bold: True
        color: 1, 1, 1, 1
        font_size: 25
        size_hint_x: None
        width: 250
        text: 'Pitch:'
    Slider:
        min: 0.0
        max: 3.0
        value: 1.0
        width: 300
        on_value: root.setPitch(self.value)


<SpinnerRow>:
    Label:
        bold: True
        color: 1, 1, 1, 1
        font_size: 25
        size_hint_x: None
        text: "Sound Effect:"
        width: 250
    EffectSpinner:
        on_text: root.change_style()


<EffectSpinner>:
    bold: True
    font_size: 25
    text: 'bubble'
    background_color: 2, 2, 2, 1
    color: 1, 1, 1, 1
    values:['bubble', 'mechanical', 'sword', 'typewriter',]

<ExitAndSwitchRow>:
    Label:
        size_hint_x: None
        width: root.width/6.0 - 120
    Label:
        size_hint_x: None
        color: 1, 1, 1, 1
        font_size: 17
        width: root.width/6.0 + 60
        text: 'Open at startup:'
    Switch:
        size_hint_x: None
        width: 40
        id: switcher
        active: root.have_added
        on_active: root.add_delete_startup_file(self.active)
    Label:
        size_hint_x: None
        width: root.width/6.0 - 35
    Button:
        size_hint_x: None
        width: 150
        background_color: 2, 2, 2, 1
        bold: True
        text: "EXIT"
        color: 0,0,0,1
        on_press: root.Exit()



<InforRow>:
    Label:
        color: 0.7, 0.7, 0.7, 1
        font_size: 23
        size_hint_x: None
        text: root.getVersion()
        width: root.width/3.0
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        markup: True
        text: "[ref=->website]Project website[/ref]"
        width: root.width/3.0
        on_ref_press:root.openProjectWebsite()
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 18
        size_hint_x: None
        text: "Author: Bill (billo@qq.com)"
        width: root.width/3.0
        border: 1,1,1,1
        on_touch_move:
'''.encode('utf-8'))


class EffectSpinner(Spinner):
    pass


class SpinnerRow(BoxLayout):
    def change_style(self):
        self.parent.detecter.setStyle(self.children[0].text)


class AdjustVol(BoxLayout):
    def setVolume(self, volume):
        self.parent.detecter.setVolume(volume)


class AdjustPitch(BoxLayout):
    def setPitch(self, pitch):
        self.parent.detecter.setPitch(pitch)


class SwitcherRow(BoxLayout):
    pass


class ExitAndSwitchRow(BoxLayout):
    def Exit(self):
        self.parent.Exit()

    def add_delete_startup_file(self, active):
        if active:
            add_startup_linux()
        else:
            delete_startup_linux()

    @property
    def have_added(self):
        return check_startup_file()


class InforRow(BoxLayout):
    def openProjectWebsite(self):
        webbrowser.open_new("http://www.yingdev.com/projects/tickeys")

    def getVersion(self):
        return 'Version: '+__version__


class Main(GridLayout):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.terminalId = args[0] if args else None
        self.GUIID = None
        # tool works preget
        if self.terminalId:
            stat, GUIID = commands.getstatusoutput('xdotool getactivewindow')
            if stat == 0:
                self.GUIID = GUIID
            # hide itself
                commands.getstatusoutput(
                    'xdotool getactivewindow windowminimize')
        self.detecter = KeyboardHandler()
        self.detecter.startDetecting()
        self.detecter.GUIID = self.GUIID
        self.hideTerminal()

    # @property
    # def detecter(self):
    #     return self.detecter

    def hideTerminal(self):
        if not self.terminalId:
            return
        commands.getstatusoutput(
            "xdotool windowactivate --sync %s" % self.terminalId)
        commands.getstatusoutput(
            "xdotool getactivewindow windowunmap")
        # if want to show terminal use windowminimize

    def Exit(self):
        self.detecter.stopDetecting()
        # Show the terminal
        # if self.terminalId:
        #     commands.getstatusoutput(
        #    "xdotool windowactivate --sync %s" % self.terminalId)
        #     commands.getstatusoutput(
        #    "xdotool getactivewindow windowmap")
        sys.exit(0)


class TickeysApp(App):
    def __init__(self, *args, **kwargs):
        super(TickeysApp, self).__init__(**kwargs)
        self.terminalId = args[0] if args else None

    def build(self):
        root = Main(self.terminalId)
        self.icon = 'tickeys.png'
        return root

    def on_stop(self):
        self.root.Exit()


if __name__ == '__main__':
    TickeysApp().run()
