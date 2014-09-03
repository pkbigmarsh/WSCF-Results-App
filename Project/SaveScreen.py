from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.graphics import Canvas

from PDFGen import *
from util import *

from SaveDialog import *
from MyGlobals import * 

from HeaderScreen import *

import os

class SaveScreen(Screen):
    tourny_name               = ""
    tourny_date               = ""
    head_td_nam               = ""
    num_players               = ""
    num_players_to_date       = ""
    num_indi_trophy_winners   = ""
    num_team_trophy_winners   = ""
    color_indi_trophies       = ""
    color_team_trophies       = ""

    def enter_screen(self):
        pass

    def leave_screen(self):
        pass

    def save(self):
        content = SaveDialog(save=self.write, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def write(self, path, filename):
        filename = normalize(filename)
        if filename[-4:] != ".pdf":
            filename += ".pdf"
        filepath = os.path.abspath(os.path.join(path, filename))

        myCanvas = canvas.Canvas(filepath, pagesize=(WIDTH, HEIGHT))

        first = True
        for result in i_file_results:
            if first == True:
                first = False
                printResultHeader(myCanvas, tournament_name, tournament_date, num_players, result.division, head_td_name, num_players_to_date)

                printIndividual(myCanvas, INCH, 6.5 * INCH, result.id, num_indi_trophy_winners, indi_trophy_highlight)

            else:
                printIndividualHeader(myCanvas, result.division)
                printIndividual(myCanvas, INCH, MARGIN_TOP - 32, result.id, num_indi_trophy_winners, indi_trophy_highlight)

            myCanvas.showPage()

        for result in t_file_results:
            printTeamHeader(myCanvas, result.division)
            printTeamStandings(myCanvas, MARGIN_TOP - 32, result.id, num_team_trophy_winners, team_trophy_highlight)
            myCanvas.showPage()

        myCanvas.save()

        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

    def new(self):
        pass

    def attach(self):
        pass