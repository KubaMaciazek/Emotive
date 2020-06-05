from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('screens/main-screen.kv')


class MainScreen(Screen):
    pass


class Emotive(App):

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(MainScreen(name='main'))
        return self.root


if __name__ == '__main__':
    Emotive().run()
