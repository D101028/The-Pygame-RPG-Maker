from configparser import ConfigParser

config = ConfigParser()
config.read("../../config.conf")

class Config:
    ICON = config["default"].get("ICON")
    NAME = config["default"].get("NAME")
