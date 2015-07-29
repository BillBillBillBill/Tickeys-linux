#!/usr/bin/env python
# coding: utf-8
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from KeyboardHandler import KeyboardHandler
from kivy.lang import Builder
import sys
import commands

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
            rgb: 0.7, 0.7, 0.7, 0.1
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
    ExitButton
    InforRow


<AdjustVol>
    Label:
        bold: True
        color: 0, 0, 0, 1
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
        color: 0, 0, 0, 1
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
        color: 0, 0, 0, 1
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
    background_color: 255, 255, 255, 1
    color: 0, 0, 0, 1
    values:['bubble', 'mechanical', 'sword', 'typewriter',]

<ExitButton>:
    Label:
    Button:
        bold: True
        text: "EXIT"
        color: 0,0,0,1
        background_color: 255.0, 255.0, 255.0, 1.0
        on_press: root.Exit()
    Label:

<InforRow>:
    Label:
        color: 0, 0, 0, 1
        font_size: 23
        size_hint_x: None
        text: "Tickeys for linux"
        width: 250
    Label:
        color: 0, 0, 0, 1
        font_size: 20
        size_hint_x: None
        text: "v0.0.1"
        width: 250
    Label:
        color: 0, 0, 0, 1
        font_size: 18
        size_hint_x: None
        text: "Author: Bill (billo@qq.com)"
        width: 250
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


class ExitButton(BoxLayout):
    def Exit(self):
        self.parent.Exit()


class InforRow(BoxLayout):
    pass


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
        return root

    def on_stop(self):
        self.root.Exit()


if __name__ == '__main__':
    TickeysApp().run()
