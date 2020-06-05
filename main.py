from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('screens/main-screen.kv')


class MainScreen(Screen):
    def print_emoji(self):
        self.ids.emoji_output.text += "XO"

    def clear_screen(self):
        self.ids.emoji_output.text = ""

    def copy_output(self):
        # TODO: pop up 'copied to clipboard'
        self.ids.emoji_output.text = "Copied!"


class Emotive(App):

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(MainScreen(name='main'))
        return self.root


if __name__ == '__main__':
    Emotive().run()
