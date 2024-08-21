
from data import SaveData, MapData, SettingData, ScriptData
from event.eventctrl import EventCtrl
from key import KeyPress
from level import Level
from menu import Menu
from savepage import SavePage
from settings import *

class MapCtrl:
    def __init__(self) -> None:
        # setting data
        self.setting_data = SettingData(SETTING_FILE_PATH)
        self.reload_from_save_data(ORIGIN_SAVE_FILE_PATH)

    def reload_from_save_data(self, save_data_path: str):
        # save data
        self.save_data = SaveData(save_data_path)
        self.proceeding_map = self.save_data["player-status"]["map"]

        # map data
        self.map_data = MapData(f"../data/map/{self.proceeding_map}.json")

        # script data
        self.script_data = ScriptData(self.map_data["script"])
        
        # init
        self.menu = Menu(self)
        self.savepage = SavePage(self)
        self.eventctrl = EventCtrl(self)
        self.level = Level(self.eventctrl, self.map_data, self.save_data, self.setting_data, 
                           self.menu, self.savepage)

    def change_map_to(self, to_map: str, player_status):
        self.level.stop_bgm_and_bgs()
        self.save_data.data["player-status"] = player_status
        self.proceeding_map = to_map

        self.map_data = MapData(f"../data/map/{self.proceeding_map}.json")
        
        self.script_data = ScriptData(self.map_data["script"])

        self.menu = Menu(self)
        self.savepage = SavePage(self)
        self.eventctrl = EventCtrl(self)
        self.level = Level(self.eventctrl, self.map_data, self.save_data, self.setting_data, 
                           self.menu, self.savepage)

    def run(self):
        KeyPress.update()
        self.level.run()

