from util import *
from kivy.uix.label import Label

import os
import string
import re

class ResultFile():
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.id = os.path.join(path, name)
        self.division = self.determineDivision()

    def determineDivision(self):
        regex = '(k|K)\d+'
        name = normalize(self.name)
        match = re.search(regex, name)
        if match == None:
            return None
        return match.group(0)

    def __str__(self):
        return "Path [" + self.path + "] Name [" + self.name + "]"

    def __eq__(self, other):
        return self.path == other.path and self.name == other.name

class ResultFileLabel(Label):
    pass
