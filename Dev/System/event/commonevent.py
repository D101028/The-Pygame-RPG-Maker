from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mapctrl import MapCtrl

from aniblock import AnimationBlock
from event.process import ChangeMap, ShowText, ShowChoices, ShowPicture, GameOver, OpenDarkCover, CloseDarkCover

class CommonEvent:
    def __init__(self, mapctrl: MapCtrl, event_data: list, index: int | None) -> None:
        self.mapctrl = mapctrl

        self.index = index

        self.event_sprites_list = None

        self.event_data = event_data

        self.local_switches: dict[str, bool] = event_data["self-switches"]
        self.local_variables: dict[str, int] = event_data["self-variables"]
        
        self.is_erased = False

        self.is_commands_proceeding = False

        self.lock_player = False

    def focus_page(self):
        page_index = None
        for index, contents in enumerate(self.event_data["pages"]):
            if contents["condition"] is None:
                page_index = index
            else:
                if self.is_condition(contents["condition"]):
                    page_index = index
                    break
        return page_index

    def refresh_page(self):
        """must have a focused page"""
        self.page_index = self.focus_page()
        self.trigger = self.event_data["pages"][self.page_index]["trigger"]
        self.contents = self.event_data["pages"][self.page_index]["contents"]

    def get_switch(self, name):
        result = self.local_switches.get(name)
        if result is None:
            return self.mapctrl.save_data["switches"][name]
        else:
            return result

    def get_variable(self, name):
        result = self.local_variables.get(name)
        if result is None:
            return self.mapctrl.save_data["variables"][name]
        else:
            return result

    def is_condition(self, condition: str) -> bool:
        if "s[" in condition:
            switch_name = condition[2: -1]
            return self.get_switch(switch_name)
        elif "v[" in condition:
            a, operator, b = condition.split()
            if "v[" in a:
                a = self.get_variable(a[2:-1])
            else:
                a = int(a)
            if "v[" in b:
                b = self.get_variable(b[2:-1])
            else:
                b = int(b)
            if operator == ">":
                return a > b
            elif operator == "<":
                return a < b
            elif operator == "!=":
                return a != b
            elif operator == "==":
                return a == b
        raise RuntimeError(f"wrong condition format: '{condition}'")

    def get_event_sprites_list(self):
        self.event_sprites_list = []
        for sprite in self.mapctrl.level.event_sprites:
            if sprite.event_id == self.index:
                self.event_sprites_list.append(sprite)

    def is_triggering(self) -> bool:
        """return whether the trigger of the focused page is achieved"""
        if self.trigger == "Action Button":
            if self.index is None:
                raise RuntimeError("unable to trigger event with index type: None")
            if len(self.event_sprites_list) == 0:
                raise RuntimeError("unable to trigger this event because of no satisfied event sprites id")
            for event_sprite in self.event_sprites_list:
                if self.mapctrl.eventctrl.button_event_listener(event_sprite):
                    return True
            else:
                return False
        elif self.trigger == "Player Touch":
            for event_sprite in self.event_sprites_list:
                if self.mapctrl.eventctrl.touch_event_listener(event_sprite):
                    return True
            else:
                return False
        elif self.trigger == "Autorun":
            return True
        elif self.trigger == "Parallel":
            return True
        
        raise RuntimeError(f"unsupported trigger: `{self.trigger}`")

    def run(self):
        if self.is_erased:
            return 
        self.lock_player = False
        if self.event_sprites_list is None:
            self.get_event_sprites_list()
        if not self.is_commands_proceeding:
            self.refresh_page()
            self.commands = Commands(self, self.contents)
            if not self.is_triggering():
                return 
        self.commands.run()
        self.is_commands_proceeding = not self.commands.is_finished

class Commands:
    def __init__(self, commonevent: CommonEvent, contents) -> None:
        self.commonevent = commonevent
        self.mapctrl = commonevent.mapctrl
        self.contents = contents
        self.is_finished = False

        self.running_command = None
    
    def run(self):
        if len(self.contents) == 0:
            self.is_finished = True
            return 
        if self.running_command is None:
            self.proceeding_command_num = 0
            self.running_command = Command(self, self.commonevent, self.contents[0])
            self.running_command.run()
        if self.running_command.is_finished:
            while self.running_command.is_finished:
                self.proceeding_command_num += 1
                if self.proceeding_command_num >= len(self.contents):
                    self.is_finished = True
                    return 
                else:
                    self.running_command = Command(self, self.commonevent, self.contents[self.proceeding_command_num])
                    self.running_command.run()
        else:
            self.running_command.run()

class Command:
    def __init__(self, commands: Commands, commonevent: CommonEvent, content) -> None:
        self.commands = commands
        self.commonevent = commonevent
        self.mapctrl = commonevent.mapctrl
        self.content = content
        self.action: str = self.content[0]
        self.param: dict = self.content[1]

        self.is_finished = False

        self.process = None

    def insert_contents_and_init(self, contents: list):
        if len(contents) == 0:
            return 
        num = self.commands.proceeding_command_num
        self.commands.contents = self.commands.contents[:num] + contents + self.commands.contents[(num+1):]
        self.content = contents[0]
        self.action = self.content[0]
        self.param = self.content[1]
        self.extract_content_and_start_process()

    def extract_content_and_start_process(self):
        if self.commonevent.trigger == "Autorun":
            self.commonevent.lock_player = True

        if self.action == "Print Test":
            print(self.param["text"])
            self.is_finished = True

        elif self.action == "Conditional Branch":
            if self.commonevent.is_condition(self.param["if"]):
                self.insert_contents_and_init(self.param["then"])
            else:
                if self.param.get("else") is not None:
                    self.insert_contents_and_init(self.param["else"])
                else:
                    self.is_finished = True

        elif self.action == "Loop":
            if self.commonevent.is_condition(self.param["condition"]):
                self.process = Commands(self.commonevent, self.param["do"])
                self.process.run()
                while self.process.is_finished:
                    if self.commonevent.is_condition(self.param["condition"]):
                        self.process = Commands(self.commonevent, self.param["do"])
                        self.process.run()
                    else:
                        self.is_finished = True
                        break

        elif self.action == "Set Local Variable":
            self.commonevent.local_variables[self.param["variable"]] = self.param["value"]
            self.is_finished = True
        elif self.action == "Set Local Switch":
            self.commonevent.local_switches[self.param["switch"]] = self.param["value"]
            self.is_finished = True
        elif self.action == "Set Global Variable":
            self.mapctrl.save_data["variables"][self.param["variable"]] = self.param["value"]
            self.is_finished = True
        elif self.action == "Set Global Switch":
            self.mapctrl.save_data["switches"][self.param["switch"]] = self.param["value"]
            self.is_finished = True
        elif self.action == "Change Local Switch":
            self.commonevent.local_switches[self.param["switch"]] = not self.commonevent.local_switches[self.param["switch"]]
            self.is_finished = True
        elif self.action == "Change Global Switch":
            self.mapctrl.save_data["switches"][self.param["switch"]] = not self.mapctrl.save_data["switches"][self.param["switch"]]
            self.is_finished = True
        elif self.action == "Erase Event":
            self.commonevent.is_erased = True
            self.is_finished = True

        elif self.action == "Save Data":
            self.mapctrl.level.is_saving = True
            self.commonevent.lock_player = True
            self.is_finished = True

        elif self.action == "Change Map":
            self.process = ChangeMap(self.mapctrl, self.commonevent, True, 
                                     self.param["to_map"], self.param.get("exit_sound"), self.param.get("enter_sound"), self.param["player_status"])
            self.run_process()

        elif self.action == "Show Text":
            self.process = ShowText(self.mapctrl, self.commonevent, True, 
                                    self.param["script_ranges"])
            self.run_process()
        elif self.action == "Show Choices":
            self.process = ShowChoices(self.mapctrl, self.commonevent, True, 
                                       self.param["script_ranges"], self.param["after"], self)
            self.run_process()
        elif self.action == "Show Picture":
            self.process = ShowPicture(self.mapctrl, self.commonevent, True, 
                                       self.param["filepath"], self.param.get("is_alpha_animate"))
            self.run_process()

        elif self.action == "Game Over":
            self.process = GameOver(self.mapctrl, self.commonevent, True, 
                                    self.param.get("script_ranges"), self.param.get("play_sound"))
            self.run_process()
    
        elif self.action == "Open Dark Cover":
            self.process = OpenDarkCover(self.mapctrl, self.commonevent, False, 
                                         self.param["size"], self.param.get("is_animate"))
            self.run_process()
        elif self.action == "Close Dark Cover":
            self.process = CloseDarkCover(self.mapctrl, self.commonevent, False, 
                                         self.param.get("is_animate"))
            self.run_process()
        
        elif self.action == "Add Animation Block":
            if self.param["is_obstacle"]:
                groups = [self.mapctrl.level.visible_sprites, self.mapctrl.level.obstacle_sprites]
            else:
                groups = [self.mapctrl.level.visible_sprites]
            AnimationBlock(
                self.param["unit_pos"], 
                groups, 
                self.param.get("animation_id"), 
                self.param.get("file_path"), 
                self.param.get("size"), 
                self.param.get("animation_speed"), 
                self.param.get("unit_move_route"), 
                self.param.get("interval"), 
                self.param.get("loop")
            )
            self.is_finished = True

        else:
            raise RuntimeError(f"wrong content action: `{self.action}`")

    def run_process(self):
        self.process.run()
        self.is_finished = self.process.is_finished

    def run(self):
        if self.process is None:
            self.extract_content_and_start_process()
        else:
            if self.action == "Loop":
                if not self.process.is_finished:
                    self.process.run()
                while self.process.is_finished:
                    if self.commonevent.is_condition(self.param["condition"]):
                        self.process = Commands(self.commonevent, self.param["do"])
                        self.process.run()
                    else:
                        self.is_finished = True
                        break
            else:
                self.run_process()
            
