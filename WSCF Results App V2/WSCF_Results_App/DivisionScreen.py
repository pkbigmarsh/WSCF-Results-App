import copy

from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.logger import Logger

from ResultFile import *
from MyGlobals import *

class DivisionScreen(Screen): 
    indi_files = ObjectProperty(None)
    indi_inputs = ObjectProperty(None)
    
    team_files = ObjectProperty(None)
    team_inputs = ObjectProperty(None)

    def update_information(self):
        self.indi_files.clear_widgets()
        self.indi_inputs.clear_widgets()
        self.team_files.clear_widgets()
        self.team_inputs.clear_widgets()

        if len(self.manager.i_file_results) == 0:
            self.indi_files.add_widget(divisionLabel("No Individual Result files loaded"))

        if len(self.manager.t_file_results) == 0:
            self.team_files.add_widget(divisionLabel("No Team Result files loaded"))


        index = 0
        for result in self.manager.i_file_results:
            self.indi_files.add_widget(divisionLabel(result.name))

            self.indi_inputs.add_widget(divisionInput(result.division, index))
            index += 1

        index = 0
        for result in self.manager.t_file_results:
            self.team_files.add_widget(divisionLabel(result.name))

            self.team_inputs.add_widget(divisionInput(result.division, index))
            index += 1

    def update_file_results(self):
        for _input in self.team_inputs.children:
            self.manager.t_file_results[int(_input.id)].division = _input.text

        for _input in self.indi_inputs.children:
            self.manager.i_file_results[int(_input.id)].division = _input.text

def divisionInput(startingText, index):
    textInput = SimpleInput()
    textInput.text = startingText
    textInput.id = str(index)
    return textInput

def divisionLabel(startingText):
    newLabel = SimpleLabel()
    newLabel.text = startingText
    return newLabel

