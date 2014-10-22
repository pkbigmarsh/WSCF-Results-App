import time

from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics.instructions import InstructionGroup

from ResultFile import *
from TrophyColorPicker import *
from MyGlobals import *

class HeaderScreen(Screen):
    input_tourny_name               = ObjectProperty(None)
    input_tourny_date               = ObjectProperty(None)
    input_head_td_nam               = ObjectProperty(None)
    input_num_players               = ObjectProperty(None)
    input_num_players_to_date       = ObjectProperty(None)
    input_num_indi_trophy_winners   = ObjectProperty(None)
    input_num_team_trophy_winners   = ObjectProperty(None)
    input_color_indi_trophies       = ObjectProperty(None)
    input_color_team_trophies       = ObjectProperty(None)

    current_color_label             = ObjectProperty(None)

    def enter_screen(self):
        if int(self.manager.num_players) == -1:
            count = 0
            for result_file in self.manager.i_file_results:
                count += file_length(result_file.id) - 1 # I need the -1 to counteract the header in a csv file

            self.manager.num_players = str(count)

        if int(self.manager.num_players_to_date) == -1:
            try:
                num_players_file = open('./Number_of_players_to_date.txt')
                self.manager.num_players_to_date = str(int(float(num_players_file.readline())) + int(float(self.manager.num_players)))
            except  IOError:
                self.manager.num_players_to_date = "Could not open Number_of_players_to_date.txt. Count lost"


        self.input_tourny_name.text             = self.manager.tournament_name
        self.input_tourny_date.text             = self.manager.tournament_date
        self.input_head_td_nam.text             = self.manager.head_td_name
        self.input_num_players.text             = self.manager.num_players
        self.input_num_players_to_date.text     = self.manager.num_players_to_date
        self.input_num_indi_trophy_winners.text = self.manager.num_indi_trophy_winners
        self.input_num_team_trophy_winners.text = self.manager.num_team_trophy_winners

    def leave_screen(self):
        self.manager.tournament_name            = self.input_tourny_name.text
        self.manager.tournament_date            = self.input_tourny_date.text
        self.manager.head_td_name               = self.input_head_td_nam.text
        self.manager.num_players                = self.input_num_players.text
        self.manager.num_players_to_date        = self.input_num_players_to_date.text

        self.manager.num_indi_trophy_winners    = self.input_num_indi_trophy_winners.text
        self.manager.num_team_trophy_winners    = self.input_num_team_trophy_winners.text   

        self.manager.indi_trophy_highlight      = self.input_color_indi_trophies.col
        self.manager.team_trophy_highlight      = self.input_color_team_trophies.col

    def choose_color(self, _input):
        content = TrophyColorPicker(done=self.color_selected)
        self.current_color_label = _input
        self._popup = Popup(title="Choose Color", content=content, size_hint=(.9,.9))
        self._popup.open()

    def color_selected(self, trophy_color_picker):
        self._popup.dismiss()
        Logger.info("HeaderScreen: color:" + str(trophy_color_picker.color_picker.color))
        Logger.info("HeaderScreen: current_color_label: " + str(self.current_color_label))

        self.current_color_label.col = trophy_color_picker.color_picker.color
        self.current_color_label.redraw()


def file_length(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

