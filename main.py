from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView

Builder.load_file('screens/main-screen.kv')
Builder.load_file('screens/copied-toast.kv')


class Toast(ModalView):
    def __init__(self, **kwargs):
        super(Toast, self).__init__(**kwargs)
        Clock.schedule_once(self.dismiss_toast, 1)

    def dismiss_toast(self, dt):
        self.dismiss()


class MainScreen(Screen):
    def print_emoji(self):
        self.ids.emoji_output.text += "XO"

    def clear_screen(self):
        self.ids.emoji_output.text = ""

    def copy_output(self):
        Clipboard.copy(self.ids.emoji_output.text)
        Factory.Toast().open()


class Emotive(App):

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(MainScreen(name='main'))
        return self.root


if __name__ == '__main__':
    Emotive().run()
