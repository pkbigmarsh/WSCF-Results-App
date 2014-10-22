import unicodedata
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Canvas
from kivy.graphics import Color
from kivy.graphics import Rectangle

class SimpleLabel(Label):
    pass

class SimpleInput(TextInput):
    pass

def normalize(unicode_text):
    if(type(unicodedata) == unicode):
        return unicodedata.normalize('NFKD', unicode_text).encode('ascii', 'ignore')
    return unicode_text

class ColorButton(Button):
	col = ObjectProperty(None)
	col = (0, .3, 0, 1)

	def redraw(self):
		with self.canvas:
			Color(self.col[0], self.col[1], self.col[2], self.col[3])
			Rectangle(pos = self.pos, size = self.size)
			Color(1,1,1,1)
			Rectangle(pos = (self.x + 10, self.y + self.height / 4),
		            size = self.texture_size,
		            texture = self.texture)