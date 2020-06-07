from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.uix.camera import Camera
import cv2
import pyperclip
from emoji.camera import EmojiRecognitionCamera

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
        emoji = Image(source=emoji_source, size_hint=(None, None), height=45, width=45)
        self.layout.add_widget(emoji)
        return

    def clear_emoji(self):
        return self.layout.clear_widgets()


class MainScreen(Screen):
    emoji_string = None
    emoji_display = None
    camera = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.emoji_string = ''
        self.emoji_display = EmojiDisplay(self.ids.emoji_display)
        self._request_android_permissions()

    def print_emoji(self):
        emoji, emoji_png = self.camera.get_current_emoji()
        self.emoji_string += emoji
        self.emoji_display.add_emoji(emoji_png)

    def clear_screen(self):
        self.emoji_string = ''
        self.emoji_display.clear_emoji()

    def copy_output(self):
        pyperclip.copy(self.emoji_string)
        Factory.Toast().open()

    def set_camera(self, capture):
        if self.is_android():
            self.camera = Camera(index=1)
        else:
            self.camera = EmojiRecognitionCamera(capture=capture, fps=30)
        self.ids.camera_layout.add_widget(self.camera)

    @staticmethod
    def is_android():
        return platform == 'android'

    def _request_android_permissions(self):
        """
        Requests CAMERA permission on Android.
        """
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)


class Emotive(App):
    capture = None

    def build(self):
        self.root = ScreenManager()
        self.capture = cv2.VideoCapture(0)
        ms = MainScreen(name='main')
        ms.set_camera(self.capture)
        self.root.add_widget(ms)
        return self.root

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    Emotive().run()
