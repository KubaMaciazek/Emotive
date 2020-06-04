from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('emotive.kv')


class MainScreen(Screen):
    pass


class LoadingScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(LoadingScreen(name='loading'))


class Emotive(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Emotive().run()
