from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.graphics import Canvas
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

from ResultFile import *
from TrophyColorPicker import *
from CSVReader import *
from PlayerIdenfication import *
from util import *
from WscfWidget import *
from DivisionScreen import *

current_selection = None
current_top = 0
current_max = 15
identification_triples = []

class MiscPlayerIdentificationScreen(Screen):
    player_list         = ObjectProperty(None)
    selection_list      = ObjectProperty(None)
    description_list    = ObjectProperty(None)
    color_list          = ObjectProperty(None)
    all_players         = ObjectProperty(None)
    current_color_label = ObjectProperty(None)

    playerIdentList     = []

    def enter_screen(self):
        self.player_list.clear_widgets()
        self.selection_list.clear_widgets()
        self.description_list.clear_widgets()
        self.color_list.clear_widgets()
        all_players = []

        for resultFile in self.manager.i_file_results:
            reader = CSVReader(resultFile.id)
            newLine = reader.getNext()
            while newLine != None:
                all_players.append(reader.getItem("Name", newLine))
                newLine = reader.getNext()

        all_players = sorted(all_players, key=str.lower)
        self.playerIdentList = []
        index = 0

        for p in all_players:
            player = PlayerIdentification()
            player.name = p
            self.playerIdentList.append(player)

        self.moveUp()

    def moveUp(self):
        global current_top
        if current_top > 0:
            current_top -= 1

        self.player_list.clear_widgets()
        end = current_top + current_max
        if end > len(self.playerIdentList):
            end = len(self.playerIdentList)

        for i in range(current_top, end):
            self.player_list.add_widget(self.newPlayerLabel(self.playerIdentList[i].name))

    def moveDown(self):
        global current_top
        if current_top < len(self.playerIdentList) - current_max:
            current_top += 1

        self.player_list.clear_widgets()
        end = current_top + current_max
        if end > len(self.playerIdentList):
            end = len(self.playerIdentList)

        for i in range(current_top, end):
            self.player_list.add_widget(self.newPlayerLabel(self.playerIdentList[i].name))

    def leave_screen(self):
        self.manager.player_identification_list.clear()
        for playerTrip in identification_triples:
            player              = PlayerIdentification()
            
            player.name         = playerTrip.player.text
            player.description  = playerTrip.description.text
            player.col          = playerTrip.color.col

            self.manager.player_identification_list.append(player)

    def move_right(self):
        global current_selection
        global identification_triples

        if current_selection in self.player_list.children:
            newTriple = Triple()
            newLabel = self.newPlayerLabel(current_selection.text)
            newDescription = self.newPlayerInput(newLabel.text)
            newColor = self.newPlayerColor(newLabel.text)

            newTriple.player = newLabel
            newTriple.description = newDescription
            newTriple.color = newColor

            self.selection_list.add_widget(newTriple.player)
            self.description_list.add_widget(newTriple.description)
            self.color_list.add_widget(newTriple.color)

            identification_triples.append(newTriple)

            self.unhighlight(current_selection)

    def move_left(self):
        global current_selection
        global identification_triples

        if current_selection in self.selection_list.children:
            triple = None
            
            for trip in identification_triples:
                if current_selection.text == trip.player.text:
                    triple = trip

            Logger.info("MoveLeft: triple: " + str(triple))
            if triple == None:
                return

            self.selection_list.remove_widget(triple.player)
            self.description_list.remove_widget(triple.description)
            self.color_list.remove_widget(triple.color)

            self.unhighlight(current_selection)

    def newPlayerLabel(self, player_name):
        newLabel = PlayerIdentificationLabel()
        newLabel.bind(on_touch_down=self.highlight)
        newLabel.text = player_name

        return newLabel

    def newPlayerInput(self, _id):
        textInput = SimpleInput()
        textInput.text = "Enter Description"
        textInput.id = str(_id)
        return textInput

    def newPlayerColor(self, _id):
        colorInput = ColorButton()
        colorInput.id = _id
        colorInput.bind(on_release=self.choose_color)

        return colorInput

    def highlight(self, label, motionEvent):
        global current_selection
        if label.collide_point(motionEvent.ox, motionEvent.oy):
            self.dohighlight(label)
            if(current_selection != None):
                self.unhighlight(current_selection)
            current_selection = label

    def dohighlight(self, label):
        with label.canvas.before:
                Color(.8, .8, .8)
                Rectangle(pos=label.pos, size=label.size)

    def unhighlight(self, label):
        with label.canvas.before:
            Color(1, 1, 1)
            Rectangle(pos=label.pos, size=label.size)


    def choose_color(self, _input):
        content = TrophyColorPicker(done=self.color_selected)
        self.current_color_label = _input
        self._popup = Popup(title="Choose Color", content=content, size_hint=(.9,.9))
        self._popup.open()

    def color_selected(self, _input):
        self._popup.dismiss()
        Logger.info("HeaderScreen: color:" + str(_input.color_picker.color))
        Logger.info("HeaderScreen: current_color_label: " + str(self.current_color_label))

        self.current_color_label.col = _input.color_picker.color
        self.current_color_label.redraw()

class Triple():
    player = None
    description = None
    color = None
