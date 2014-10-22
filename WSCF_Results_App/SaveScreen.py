from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.graphics import Canvas

from PDFGen import *
from util import *
from pyPdf import PdfFileWriter, PdfFileReader

from SaveDialog import *
from LoadDialog import *

import os

class SaveScreen(Screen):
    appended_pdfs = []

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
        merge_filename = "merged_" + filename
        filepath = os.path.abspath(os.path.join(path, filename))
        merge_filepath = os.path.abspath(os.path.join(path, merge_filename))

        myCanvas = canvas.Canvas(filepath, pagesize=(WIDTH, HEIGHT))

        first = True
        for result in self.manager.i_file_results:
            if first == True:
                first = False
                printResultHeader(myCanvas, self.manager.tournament_name, self.manager.tournament_date, self.manager.num_players, result.division, self.manager.head_td_name, self.manager.num_players_to_date)

                printIndividual(myCanvas, INCH, 6.5 * INCH, result.id, self.manager.num_indi_trophy_winners, self.manager.indi_trophy_highlight, self.manager.player_identification_list)

            else:
                printIndividualHeader(myCanvas, result.division)
                printIndividual(myCanvas, INCH, MARGIN_TOP - 32, result.id, self.manager.num_indi_trophy_winners, self.manager.indi_trophy_highlight, self.manager.player_identification_list)

            myCanvas.showPage()

        for result in self.manager.t_file_results:
            printTeamHeader(myCanvas, result.division)
            printTeamStandings(myCanvas, MARGIN_TOP - 32, result.id, self.manager.num_team_trophy_winners, self.manager.team_trophy_highlight)
            myCanvas.showPage()

        myCanvas.save()

        self.dismiss_popup()

        if len(self.appended_pdfs) > 0:
            base_input = file(filepath, "rb")
            base = PdfFileReader(base_input)
            output = PdfFileWriter()
            [output.addPage(base.getPage(page_num)) for page_num in xrange(base.getNumPages())]

            for pdf in self.appended_pdfs:
                inpu = PdfFileReader(file(pdf, "rb"))
                [output.addPage(inpu.getPage(page_num)) for page_num in xrange(inpu.getNumPages())]

            output.write(file(merge_filepath, "wb"))

            del base


    def dismiss_popup(self):
        self._popup.dismiss()

    def new(self):
        self.manager.restart()

    def attach(self):
        Logger.info("load_file")
        content = LoadFileDialog(load=self.loadFile, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load File", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


    def loadFile(self, path, filename):
        filepath = os.path.abspath(os.path.join(path, filename[0]))
        self.appended_pdfs.append(filepath)

        self.dismiss_popup()