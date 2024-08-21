import json
import os 

from settings import *
from level import Level
from backup.event import ChangeMapParam
from menu import MenuReturnParam

class MapCtrl:
    def __init__(self) -> None:
        self.save_data_path = ORIGIN_SAVE_FILE_PATH
        self.load_save_data()
        self.repair_save_data()
        self.proceeding_map = self.save_data["proceeding-map"]
        
        self.level = Level(self.save_data, self.proceeding_map)

    def load_save_data(self):
        with open(self.save_data_path, mode = "r", encoding = "utf8") as file:
            self.save_data = json.load(file)

    def repair_save_data(self):
        if self.save_data.get("proceeding-map") is None:
            self.save_data["proceeding-map"] = "Map01"
        if self.save_data.get("map-details") is None:
            self.save_data["map-details"] = {}
        for root, dirs, files in os.walk("../data/map"):
            for file in files:
                if file == "template.json":
                    continue
                with open(os.path.join(root, file), mode = "r", encoding = "utf8") as fp:
                    data = json.load(fp)
                if self.save_data["map-details"].get(data["name"]) is None:
                    self.save_data["map-details"][data["name"]] = data

    def redirect_map(self, change_map_param: ChangeMapParam):
        self.save_data["proceeding-map"] = change_map_param.to_map
        self.save_data["player-status"] = change_map_param.player_status
        self.proceeding_map = change_map_param.to_map
        self.level = Level(self.save_data, self.proceeding_map, change_map_param)

    def save_load_map(self, menu_return_param: MenuReturnParam):
        self.save_data_path = menu_return_param.save_load_path
        self.load_save_data()
        self.repair_save_data()
        self.proceeding_map = self.save_data["proceeding-map"]

        self.level = Level(self.save_data, self.proceeding_map)

    def run(self):
        param = self.level.run()
        if isinstance(param, MenuReturnParam):
            self.save_load_map(param)
        elif isinstance(param, ChangeMapParam):
            self.redirect_map(param)

