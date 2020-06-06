from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.uix.camera import Camera
from emoji.parser import Parser
from kivy.graphics.texture import Texture
import cv2

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


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

    def take_photo(self):
        return None


class MainScreen(Screen):
    emoji_parser = None
    emoji_string = None
    emoji_display = None
    camera = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.emoji_parser = Parser()
        self.emoji_string = ''
        self.emoji_display = EmojiDisplay(self.ids.emoji_display)
        self._request_android_permissions()

    def print_emoji(self):
        photo = self.camera.take_photo()
        emoji, emoji_png = self.emoji_parser.get_emoji_from_photo(photo)
        self.emoji_string += emoji
        self.emoji_display.add_emoji(emoji_png)

    def clear_screen(self):
        self.emoji_string = ''
        self.emoji_display.clear_emoji()

    def copy_output(self):
        Clipboard.copy(self.emoji_string)
        Factory.Toast().open()

    def set_camera(self, capture):
        if self.is_android():
            self.camera = Camera(index=1)
        else:
            self.camera = KivyCamera(capture=capture, fps=30)
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
