#!/usr/bin/env python
# coding: utf-8
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from keyboardHandler import KeyboardHandler
from kivy.lang import Builder
from startupHandler import add_startup_linux, check_startup_file, delete_startup_linux
from logger import logger
from config import Configer
from __init__ import __version__, debug_mode

import sys
import os

from threading import Thread

from windowManager import hide_GUI, save_GUI_window_id

reload(sys)
sys.setdefaultencoding("utf-8")

# set font
from kivy.core.text import Label
try:
    os.chdir(os.path.dirname(__file__))
except Exception:
    pass
Label.register("DroidSans", "./Resources/fonts/DroidSansFallbackFull.ttf")

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
            rgba: 0.368, 0.384, 0.447, 0.8
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
        text: '音量：'
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
        text: '音调：'
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
        text: "声音方案："
        width: 250
    EffectSpinner:
        on_text: root.change_style()


<EffectSpinner>:
    bold: True
    font_size: 30
    text: root.get_style_name()
    background_color: 3, 3, 3, 1
    color: 0.1, 0.67, 0.93, 1
    values:['冒泡', '打字机', '机械键盘', '剑气', 'Cherry G80-3000', 'Cherry G80-3494', '爆裂鼓手']

<ExitAndSwitchRow>:
    Label:
        size_hint_x: None
        width: root.width/6.0 - 120
    Label:
        size_hint_x: None
        color: 1, 1, 1, 1
        font_size: 17
        width: root.width/6.0 + 60
        text: '开机时自启动：'
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
        text: "退出"
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
        text: "隐藏"
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
        text: "[ref=项目主页]项目主页[/ref]"
        width: root.width/3.0
        on_ref_press:root.open_project_website()
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        text: "作者： Bill (billo@qq.com)"
        width: root.width/3.0
        border: 1,1,1,1
        on_touch_move:
'''.encode('utf-8'))


def show_notify():
    try:
        import notify2
        notify2.init('Tickeys')
        title = 'Tickeys'
        body = '<span style="color: #00B8CB; font-size:15px">Tickeys</span>正在运行\n随时按<span style="color: #00B8CB">QAZ123</span>唤出设置窗口'
        iconfile = os.getcwd() + '/tickeys.png'
        notify = notify2.Notification(title, body, iconfile)
        notify.show()
    except Exception:
        return


def check_update():
    try:
        import urllib
        import json
        logger.info("Version checking...")
        r = urllib.urlopen('http://billbill.sinaapp.com/tickeys')
        return_msg = json.loads(r.read())
        if return_msg["version"] <= __version__:
            logger.debug("Version checking success. It is the latest version...")
            return
        else:
                # show update notify
                import notify2
                notify2.init('Tickeys')
                title = '<h2>Tickeys</h2>'
                body = '<span style="color: #00B8CB; font-size:15px">Tickeys</span>有可用的<span style="color: #FF4500">更新：</span>\n 版本：%s \n 内容：%s' % (return_msg["version"], return_msg["update"])
                iconfile = os.getcwd() + '/tickeys.png'
                notify = notify2.Notification(title, body, iconfile)
                notify.show()
    except Exception, e:
        logger.exception(e)
        logger.error("Version checking fail:" + str(e))


class EffectSpinner(Spinner):
    def get_style_name(self):
        style_display_name_map = {
            'bubble': "冒泡",
            'typewriter': "打字机",
            'mechanical': "机械键盘",
            'sword': "剑气",
            'Cherry_G80_3000': "Cherry G80-3000",
            'Cherry_G80_3494': "Cherry G80-3494",
            'drum': "爆裂鼓手"
        }
        name = self.parent.parent.Configer.style
        display_name = style_display_name_map[name]
        return display_name



class SpinnerRow(BoxLayout):
    def change_style(self):
        style_display_name_map = {
            '冒泡': "bubble",
            '打字机': "typewriter",
            '机械键盘': "mechanical",
            '剑气': "sword",
            'Cherry G80-3000': "Cherry_G80_3000",
            'Cherry G80-3494': "Cherry_G80_3494",
            '爆裂鼓手': "drum"
        }
        style_name = style_display_name_map[self.children[0].text]
        self.parent.detecter.set_style(style_name)


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
        os._exit(0)

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
    def open_project_website(self, *args):
        from webbrowser import open_new
        open_new("https://github.com/BillBillBillBill/Tickeys-linux")

    def get_version(self):
        return 'Version： ' + __version__


class Main(GridLayout):
    def __init__(self, *args, **kwargs):
        self.Configer = Configer()
        super(Main, self).__init__(**kwargs)
        save_GUI_window_id()
        self.Hide()
        # set up keyboard detecter
        self.detecter = KeyboardHandler()
        self.detecter.start_detecting()
        # show notify message
        Thread(target=show_notify).start()
        Thread(target=check_update).start()

    def Hide(self):
        if not debug_mode:
            hide_GUI()


class TickeysApp(App):
    def __init__(self, *args, **kwargs):
        super(TickeysApp, self).__init__(**kwargs)

    def build(self):
        self.icon = 'tickeys.png'
        root = Main()
        return root

    def on_stop(self):
        os._exit(0)


if __name__ == '__main__':
    TickeysApp().run()
