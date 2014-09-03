from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)