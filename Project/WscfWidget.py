from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.graphics import Canvas
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from PDFGen import *
from util import *
from ResultFile import *
from LoadDialog import *
from SaveDialog import *
from MyGlobals import * 

import os

current_selection = None

class WscfWidget(Screen):
    individual_files = ObjectProperty(None)
    team_files = ObjectProperty(None)

    def enter_screen(self):
        pass

    def leave_screen(self):
        pass

    def load_file(self):
        Logger.info("load_file")
        content = LoadFileDialog(load=self.loadFile, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load File", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load_folder(self):
        Logger.info("load_folder")
        content = LoadFolderDialog(load=self.loadFolder, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open() 

    def move_up(self):
        global current_selection
        if current_selection == None:
            return
        curr = current_selection
        self.unhighlight(current_selection)
        current_selection = None

        for result in self.manager.t_file_results:
            if result.id == curr.id:
                self.move(self.manager.t_file_results, result, -1)
                newLabel = self.redrawFileBox(self.team_files, self.manager.t_file_results)
                return

        for result in self.manager.i_file_results:
            if result.id == curr.id:
                self.move(self.manager.i_file_results, result, -1)
                self.redrawFileBox(self.individual_files, self.manager.i_file_results)
                return

    def move_down(self):
        global current_selection
        if current_selection == None:
            return
        curr = current_selection
        self.unhighlight(current_selection)
        current_selection = None

        for result in self.manager.t_file_results:
            if result.id == curr.id:
                self.move(self.manager.t_file_results, result, 1)
                newLabel = self.redrawFileBox(self.team_files, self.manager.t_file_results)
                return

        for result in self.manager.i_file_results:
            if result.id == curr.id:
                self.move(self.manager.i_file_results, result, 1)
                self.redrawFileBox(self.individual_files, self.manager.i_file_results)
                return

    def redrawFileBox(self, filebox, newChildren):
        targetLabel = None
        filebox.clear_widgets()

        for child in newChildren:
            newLabel = self.newFileLabel(child)
            filebox.add_widget(newLabel)

    def move(self, _list, item, distance):
        pos = -1
        for i in range(0, len(_list)):
            if _list[i] == item:
                pos = i
                break

        if pos == -1:
            return

        _list.remove(item)

        pos += distance
        if pos < 0:
            pos = 0

        if pos > len(_list):
            pos = len(_list)

        _list.insert(pos, item)

    def move_left(self):
        global current_selection
        if current_selection == None:
            return
        self.unhighlight(current_selection)
        for result in self.manager.t_file_results:
            if current_selection.id == result.id:
                self.manager.t_file_results.remove(result)
                self.team_files.remove_widget(current_selection)

                self.manager.i_file_results.append(result)
                self.individual_files.add_widget(self.newFileLabel(result))
                break

        current_selection = None

    def move_right(self):
        global current_selection
        if current_selection == None:
            return
        self.unhighlight(current_selection)
        for result in self.manager.i_file_results:
            if current_selection.id == result.id:
                self.manager.i_file_results.remove(result)
                self.individual_files.remove_widget(current_selection)

                self.manager.t_file_results.append(result)
                self.team_files.add_widget(self.newFileLabel(result))
                break

        current_selection = None

    def remove_file(self):
        global current_selection
        if current_selection == None:
            return
        self.unhighlight(current_selection)
        for result in self.manager.t_file_results:
            if current_selection.id == result.id:
                self.manager.t_file_results.remove(result)

                team = self.team_files

                team.remove_widget(current_selection)
                current_selection = None
                return

        for result in self.manager.i_file_results:
            if current_selection.id == result.id:
                self.manager.i_file_results.remove(result)

                indi = self.individual_files

                indi.remove_widget(current_selection)
                current_selection = None
                return

    def loadFile(self, path, filename):
        filepath = os.path.abspath(os.path.join(path, filename[0]))

        pathParts = os.path.split(filepath)

        singleFile = ResultFile(pathParts[0], normalize(pathParts[1]))

        if singleFile in self.manager.i_file_results or singleFile in self.manager.t_file_results:
            Logger.info("loadFile: File already loaded: " + singleFile.name)
            self.dismiss_popup()
            return

        singleFileLabel = self.newFileLabel(singleFile)

        if "team" in singleFile.name.lower():
            filebox = self.team_files
            self.manager.t_file_results.append(singleFile)
        else:
            filebox = self.individual_files
            self.manager.i_file_results.append(singleFile)

        filebox.add_widget(singleFileLabel)

        self.dismiss_popup()

    def newFileLabel(self, resultFile):
        newLabel = ResultFileLabel()
        newLabel.bind(on_touch_down=self.highlight)
        newLabel.text = resultFile.name
        newLabel.id = resultFile.id

        return newLabel

    def loadFolder(self, path, filename):
        path = os.path.join(path, filename[0])

        if os.path.isdir(path) == False:
            Logger.error("loadFolder: File is not a directory!")
            return

        files = os.listdir(path)
        for _file in files:
            filename = normalize(os.path.basename(_file))
            if ".csv" in filename:
                self.loadFile(path, [filename])
            else:
                Logger.info("loadFolder: File: " + filename + ", is not a valid choice")

        self.dismiss_popup()

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
        Logger.info("unhighlight: " + label.id)
        with label.canvas.before:
            Color(1, 1, 1)
            Rectangle(pos=label.pos, size=label.size)

    def dismiss_popup(self):
        self._popup.dismiss()