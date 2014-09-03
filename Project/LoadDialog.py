from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class LoadFileDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadFolderDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)