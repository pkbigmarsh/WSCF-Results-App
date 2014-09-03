from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import time

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty

from WscfWidget import *
from DivisionScreen import *
from HeaderScreen import *
from MiscPlayerIdentification import *
from SaveScreen import *

Builder.load_file("./kvLayouts/util.kv")
Builder.load_file("./kvLayouts/WscfLayout.kv")
Builder.load_file("./kvLayouts/DivisionLayout.kv")
Builder.load_file("./kvLayouts/SaveLayout.kv")
Builder.load_file("./kvLayouts/LoadLayouts.kv")
Builder.load_file("./kvLayouts/HeaderLayout.kv")
Builder.load_file("./kvLayouts/TrophyColorPicker.kv")
Builder.load_file("./kvLayouts/MiscPlayerIdentification.kv")
Builder.load_file("./kvLayouts/SaveScreen.kv")

class DataScreenManager(ScreenManager):
    i_file_results              = ListProperty([])
    t_file_results              = ListProperty([])
    tournament_name             = StringProperty("")
    tournament_date             = StringProperty(time.strftime("%m/%d/%Y"))
    head_td_name                = StringProperty("")
    num_players                 = StringProperty(None)
    num_players_to_date         = StringProperty(None)

    num_indi_trophy_winners     = StringProperty("0")
    num_team_trophy_winners     = StringProperty("0")
    indi_trophy_highlight       = ListProperty([])
    team_trophy_highlight       = ListProperty([])

    player_identification_list  = ListProperty([])

class WscfApp(App):
    def build(self):
        screenManager = DataScreenManager()
        screenManager.add_widget(WscfWidget(name="main"))
        screenManager.add_widget(DivisionScreen(name="Division"))
        screenManager.add_widget(HeaderScreen(name="Header"))
        screenManager.add_widget(MiscPlayerIdentificationScreen(name="Player Identification"))
        screenManager.add_widget(SaveScreen(name="Save"))
        return screenManager

if __name__ == '__main__':
    WscfApp().run()