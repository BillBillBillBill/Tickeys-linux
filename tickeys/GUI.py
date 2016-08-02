#!/usr/bin/env python
# coding: utf-8
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from keyboardHandler import KeyboardHandler
from kivy.lang import Builder
from startupHandler import add_startup_linux, check_startup_file, delete_startup_linux
from logger import logger
from config import Configer
from __init__ import __version__, debug_mode

import sys
import os
import gettext
from ast import literal_eval

from threading import Thread
import notify2
from windowManager import hide_GUI, save_GUI_window_id

reload(sys)
sys.setdefaultencoding("utf-8")

# set font
from kivy.core.text import Label as textLabel
try:
    os.chdir(os.path.dirname(__file__))
except Exception:
    pass
textLabel.register("DroidSans", "./Resources/fonts/DroidSansFallbackFull.ttf")


configer = Configer()
t = gettext.translation('tickeys', 'locale', languages=[configer.lang], fallback=True)
_ = t.ugettext

Builder.load_string(('''
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
        text: '%s'
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
        text: '%s'
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
        text: "%s"
        width: 250
    EffectSpinner:
        on_text: root.change_style()


<EffectSpinner>:
    bold: True
    font_size: 30
    text: root.get_style_name()
    background_color: 3, 3, 3, 1
    color: 0.1, 0.67, 0.93, 1
    values: %s

<ExitAndSwitchRow>:
    Label:
        size_hint_x: None
        width: root.width/6.0 - 120
    Label:
        size_hint_x: None
        color: 1, 1, 1, 1
        font_size: 17
        width: root.width/6.0 + 60
        text: '%s：'
    Switch:
        size_hint_x: None
        width: 40
        id: switcher
        active: root.have_added
        on_active: root.add_delete_startup_file(self.active)
    Label:
        size_hint_x: None
        width: root.width/6.0 - 85
    Spinner:
        width: 40
        bold: True
        font_size: 20
        text: root.get_language_name()
        background_color: 3, 3, 3, 1
        color: 0.1, 0.67, 0.93, 1
        values: ['English', '简体中文']
        on_text: root.set_language(self.text)
    Label:
        size_hint_x: None
        width: 20
    Button:
        size_hint_x: None
        width: 150
        font_size: 20
        background_color: 3, 3, 3, 1
        bold: True
        text: "%s"
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
        text: "%s"
        color: 0,0,0,1
        on_release: root.Hide()

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
        text: "[ref=%s]%s[/ref]"
        width: root.width/3.0
        on_ref_press:root.open_project_website()
    Label:
        color: 0.8, 0.8, 0.8, 1
        font_size: 20
        size_hint_x: None
        text: "%s： Bill (billo@qq.com)"
        width: root.width/3.0
        border: 1,1,1,1
        on_touch_move:
''' % (_("Volume"), _("Pitch"), _("Sound Style"), _("Sound Style Items"), _("Start at startup"), _("Quit"), _("Hide"), _("Project Website"), _("Project Website"), _("Author"))).encode('utf-8'))


def show_notify(notify_content=""):
    try:
        notify2.init('Tickeys')
        title = 'Tickeys'
        icon_file_path = os.getcwd() + '/tickeys.png'
        notify = notify2.Notification(title, notify_content, icon_file_path)
        notify.show()
    except Exception, e:
        logger.exception(e)
        logger.error("show notify fail")


def show_startup_notify():
    notify_content = _("Startup Notify")
    show_notify(notify_content)


def check_update_and_notify():
    try:
        import urllib
        import json
        logger.info("Version checking...")
        r = urllib.urlopen('http://billbill.sinaapp.com/tickeys')
        return_msg = json.loads(r.read())
        print return_msg
        if return_msg["version"] <= __version__:
            logger.debug("Version checking success. It is the latest version...")
        else:
            # show update notify
            notify_content = _("Update Notify") % (return_msg["version"], return_msg["update"])
            print notify_content
            show_notify(notify_content)
    except Exception, e:
        logger.exception(e)
        logger.error("Version checking fail:" + str(e))


class EffectSpinner(Spinner):
    def get_style_name(self):
        style_list = literal_eval(_("Sound Style Items"))
        style_display_name_map = {
            'bubble': style_list[0],
            'typewriter': style_list[1],
            'mechanical': style_list[2],
            'sword': style_list[3],
            'Cherry_G80_3000': style_list[4],
            'Cherry_G80_3494': style_list[5],
            'drum': style_list[6]
        }
        name = self.parent.parent.Configer.style
        return style_display_name_map.get(name, name)


class SpinnerRow(BoxLayout):
    def change_style(self):
        style_list = literal_eval(_("Sound Style Items"))
        style_display_name_map = {
            style_list[0]: "bubble",
            style_list[1]: "typewriter",
            style_list[2]: "mechanical",
            style_list[3]: "sword",
            style_list[4]: "Cherry_G80_3000",
            style_list[5]: "Cherry_G80_3494",
            style_list[6]: "drum"
        }
        # for safe
        if self.children[0].text not in style_display_name_map:
            return
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

    def set_language(self, language):
        language_map = {
            "English": "en_US",
            "简体中文": "zh_CN"
        }
        self.parent.Configer.lang = language_map.get(language, "en_US")
        self.parent.Configer.save_config()
        # show popup hint
        view = ModalView(size_hint=(None, None), size=(0, 0))
        view.add_widget(Label(text=_("This will take effect next time you start"), font_size=30))
        view.open()

    def get_language_name(self):
        lang_display_name_map = {
            "en_US": "English",
            "zh_CN": "简体中文"
        }
        lang = self.parent.Configer.lang
        return lang_display_name_map.get(lang, "English")

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
        Thread(target=show_startup_notify).start()
        # now not check update
        # Thread(target=check_update_and_notify).start()

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
