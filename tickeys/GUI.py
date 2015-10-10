#!/usr/bin/env python
# coding: utf-8
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from KeyboardHandler import KeyboardHandler
from kivy.lang import Builder
from StartupHandler import add_startup_linux, check_startup_file, delete_startup_linux
from logger import logger
from config import Configer
from __init__ import __version__


import sys
import os
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
            rgb: 0.368, 0.384, 0.447, 1
        Rectangle:
            pos: 0,0
            size: self.size
    Label:
        bold: True
        text: 'Tickeys'
        font_size: 50
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
        font_size: 33
        size_hint_x: None
        width: 250
        text: 'Volume:'
    Slider:
        min: 0.0
        max: 1.0
        value: root.parent.Configer.volume
        width: 300
        on_value: root.setVolume(self.value)

<AdjustPitch>
    Label:
        bold: True
        color: 1, 1, 1, 1
        font_size: 33
        size_hint_x: None
        width: 250
        text: 'Pitch:'
    Slider:
        min: 0.0
        max: 3.0
        value: root.parent.Configer.pitch
        width: 300
        on_value: root.setPitch(self.value)


<SpinnerRow>:
    Label:
        bold: True
        color: 1, 1, 1, 1
        font_size: 33
        size_hint_x: None
        text: "Sound:"
        width: 250
    EffectSpinner:
        on_text: root.change_style()


<EffectSpinner>:
    bold: True
    font_size: 30
    text: root.parent.parent.Configer.style
    background_color: 3, 3, 3, 1
    color: 0.1, 0.67, 0.93, 1
    values:['bubble', 'mechanical', 'sword', 'typewriter', 'Cherry_G80_3000', 'Cherry_G80_3494',]

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
        font_size: 20
        background_color: 3, 3, 3, 1
        bold: True
        text: "QUIT"
        color: 0,0,0,1
        on_press: root.Exit()
    Label:
        size_hint_x: None
        width: 20
    Button:
        size_hint_x: None
        width: 150
        font_size: 20
        background_color: 3, 3, 3, 1
        bold: True
        text: "Hide"
        color: 0,0,0,1
        on_press: root.Hide()


<InforRow>:
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        text: root.get_version()
        width: root.width/3.0
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        markup: True
        text: "[ref=->website]Project website[/ref]"
        width: root.width/3.0
        on_ref_press:root.open_project_website()
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        text: "Author: Bill (billo@qq.com)"
        width: root.width/3.0
        border: 1,1,1,1
        on_touch_move:
'''.encode('utf-8'))


def show_notify():
    try:
        import pynotify
        pynotify.init('Tickeys')
        title = 'Tickeys'
        body = '<span style="color: #00B8CB; font-size:15px">Tickeys</span>正在运行\n随时按<span style="color: #00B8CB">QAZ123</span>唤出设置窗口'
        iconfile = os.getcwd() + '/tickeys.png'
        notify = pynotify.Notification(title, body, iconfile)
        notify.show()
    except Exception:
        return


class EffectSpinner(Spinner):
    pass


class SpinnerRow(BoxLayout):
    def change_style(self):
        self.parent.detecter.set_style(self.children[0].text)


class AdjustVol(BoxLayout):
    def setVolume(self, volume):
        self.parent.detecter.set_volume(volume)


class AdjustPitch(BoxLayout):
    def setPitch(self, pitch):
        self.parent.detecter.set_pitch(pitch)


class SwitcherRow(BoxLayout):
    pass


class ExitAndSwitchRow(BoxLayout):
    def Exit(self):
        self.parent.Exit()

    def Hide(self):
        self.parent.Hide()

    def add_delete_startup_file(self, active):
        if active:
            add_startup_linux()
        else:
            delete_startup_linux()

    @property
    def have_added(self):
        return check_startup_file()


class InforRow(BoxLayout):
    def open_project_website(self):
        webbrowser.open_new("http://www.yingdev.com/projects/tickeys")

    def get_version(self):
        return 'Version: '+__version__


class Main(GridLayout):
    def __init__(self, *args, **kwargs):
        self.Configer = Configer()
        super(Main, self).__init__(**kwargs)
        self.terminalId = args[0] if args else None
        self.GUIID = None
        # tool works preget
        if self.terminalId:
            stat, GUIID = commands.getstatusoutput('xdotool getactivewindow')
            if stat == 0:
                self.GUIID = GUIID
            # hide itself
                # commands.getstatusoutput(
                #     'xdotool getactivewindow windowminimize')
                self.hide_GUI()
        self.detecter = KeyboardHandler()
        self.detecter.start_detecting()
        self.detecter.GUIID = self.GUIID
        self.hide_terminal()
        show_notify()

    # @property
    # def detecter(self):
    #     return self.detecter

    def hide_terminal(self):
        if not self.terminalId:
            return
        commands.getstatusoutput(
            "xdotool windowactivate --sync %s" % self.terminalId)
        commands.getstatusoutput(
            "xdotool getactivewindow windowunmap")
        # if want to show terminal use windowminimize

    def hide_GUI(self):
        try:
            commands.getstatusoutput(
                'xdotool windowunmap --sync %s' % self.GUIID)
        except Exception,e:
            logger.error(str(e))

    def Exit(self):
        self.detecter.stop_detecting()
        # Show the terminal
        # if self.terminalId:
        #     commands.getstatusoutput(
        #    "xdotool windowactivate --sync %s" % self.terminalId)
        #     commands.getstatusoutput(
        #    "xdotool getactivewindow windowmap")
        sys.exit(0)

    def Hide(self):
        self.hide_GUI()


class TickeysApp(App):
    def __init__(self, *args, **kwargs):
        super(TickeysApp, self).__init__(**kwargs)
        self.terminalId = args[0] if args else None

    def build(self):
        self.icon = 'tickeys.png'
        root = Main(self.terminalId)
        return root

    def on_stop(self):
        self.root.Exit()


if __name__ == '__main__':
    TickeysApp().run()
