from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from emoji.parser import Parser

Builder.load_file('screens/main-screen.kv')
Builder.load_file('screens/copied-toast.kv')


class Toast(ModalView):
    def __init__(self, **kwargs):
        super(Toast, self).__init__(**kwargs)
        Clock.schedule_once(self.dismiss_toast, 1)

    def dismiss_toast(self, dt):
        self.dismiss()


class EmojiDisplay:
    layout = None

    def __init__(self, anchor_layout):
        self.layout = anchor_layout

    def add_emoji(self, emoji_source):
        emoji = Image(source=emoji_source, size_hint=(None, None), height=100, width=100)
        self.layout.add_widget(emoji)
        return

    def clear_emoji(self):
        return self.layout.clear_widgets()


class MainScreen(Screen):
    emoji_parser = None
    emoji_string = None
    emoji_display = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.emoji_parser = Parser()
        self.emoji_string = ''
        self.emoji_display = EmojiDisplay(self.ids.emoji_display)

    def print_emoji(self):
        photo = None
        emoji = self.emoji_parser.get_emoji_from_photo(photo)
        self.emoji_string += emoji
        emoji_png = self.emoji_parser.get_emoji_png(emoji)
        self.emoji_display.add_emoji(emoji_png)

    def clear_screen(self):
        self.emoji_string = ''
        self.emoji_display.clear_emoji()

    def copy_output(self):
        Clipboard.copy(self.emoji_string)
        Factory.Toast().open()


class Emotive(App):

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(MainScreen(name='main'))
        return self.root


if __name__ == '__main__':
    Emotive().run()
