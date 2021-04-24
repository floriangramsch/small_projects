from kivy.app import App
from kivy.config import KIVY_CONFIG_VERSION
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from crimp import Crimp

import time

class MyMainApp(App):
    progress_bar = ObjectProperty()
    def build(self):
        # self.clock = Clock()

        vbox = BoxLayout(orientation="vertical")

        self.start_button = Button(text="Start Workout")
        self.start_button.bind(on_release=self.crimp)

        self.label = Label(text="Helo World")
        self.pb = ProgressBar(max=10)
        self.pb2 = ProgressBar(max=10)
        self.pb2.value = 0

        vbox.add_widget(self.start_button)
        vbox.add_widget(self.label)
        vbox.add_widget(self.pb)
        vbox.add_widget(self.pb2)

        return vbox

    def crimp(self, instance):
        Clock.schedule_interval(self.next, 1)
        Clock.schedule_interval(self.next2, 1)
        pass

    def next(self, dt):
        self.pb.value = 0
        if self.pb.value >= 10:
            return False
        self.pb.value += 1
        
    def next2(self, dt):
        self.pb2.value = 0
        if self.pb2.value >= 10:
            return False
        self.pb2.value += 1



if __name__ == "__main__":
    MyMainApp().run()