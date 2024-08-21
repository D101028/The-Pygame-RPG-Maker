import pygame
import yaml

from menu import Menu
from player import Player
from settings import *
from support import draw_text

class ChangeMapParam:
    def __init__(self, from_map, to_map, inherit_events, player_status) -> None:
        self.from_map = from_map
        self.to_map = to_map
        self.inherit_events = inherit_events
        self.player_status = player_status

class Process:
    def __init__(self, func, param = None, event_data = None, **kwargs) -> None:
        """`func` must be a function, whose first parameter 
        is self (Self@Process), and return a bool on behalf
        of whether to remove itself from processes list after 
        running the process"""
        self.func = func
        self.param = param
        self.event_data = event_data
        self.kwargs = kwargs
    
    def run(self) -> bool:
        """return the bool that `self.func` has return"""
        if self.param is None:
            return self.func(self)
        else:
            return self.func(self, self.param)

class EventCtrl:
    def __init__(self, player: Player, event_sprites, map_name, change_map_param: ChangeMapParam | None, menu: Menu) -> None:
        self.player = player
        self.menu = menu

        self.action_event_dict = {
            "test-print": self.test_print, 
            "proceed-dialog": self.proceed_dialog, 
            "save-data": self.save, 
            "change-map": self.change_map, 
            "play-close-door-sound": self.play_close_door_sound, 
            "play-sound": self.play_sound, 
            "show-picture": self.show_picture, 
            "show-choices": self.show_choices, 
            "modify-event-status": self.modify_event_status
        }
        self.is_event_listening = False
        self.is_collision_event_listening = True
        self.event_sprites = event_sprites
        self.map_name = map_name
        self.events_data = self.menu.save_data["map-details"][self.map_name]["events"]
        self.ID_to_event = {}
        self.auto_collision_events_id = []
        self.create_ID_event_dict()

        # get script contents
        self.get_script_contents()

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # process list
        self.processes: list[Process] = []

        # play start map animate
        self.start_map_animate()

        # run inherit events
        self.run_inherit_events(change_map_param)

        # init map changing parameter
        self.change_map_param = None # None for not to change else be a ChangeMapParam object

        # save
        self.is_open_saving = False

    # special event functions
    def start_map_animate(self):
        process = Process(self._start_map_animate, event_data = {"lock-player": True}, 
                          alpha = 255, 
                          surface = pygame.Surface((WIDTH, HEIGTH)))
        self.processes.append(process)

    # player event functions
    def test_print(self, event_data):
        print(event_data)
        self.set_event_status(event_data["id"], "finished")
        self.processes.append(Process(lambda event_data: True, event_data = event_data))
    
    def proceed_dialog(self, event_data):
        """`script_range` example: `["1:10", "12:30"]`"""
        dialog_surf = pygame.image.load("../Graphics/layer/dialog_box.png").convert_alpha()
        dialog_surf.set_alpha(230)
        dialog_topleft = ((WIDTH - dialog_surf.get_width()) // 2, HEIGTH - dialog_surf.get_height())
        triangle_surf = pygame.image.load("../Graphics/layer/triangle.png").convert_alpha()
        triangle_topleft = ((WIDTH - triangle_surf.get_width()) // 2, HEIGTH - triangle_surf.get_height() - 5)
        dialog_surf.set_alpha(230)

        script_range = event_data["param"]["message_code"]
        script_list = []
        for r in script_range:
            start, end = map(int, r.split("-"))
            script_list += [f"message_{i}" for i in range(start, end + 1)]
        sound = pygame.mixer.Sound("../Audio/SE/subtitle_run.ogg")
        sound.set_volume(self.menu.settings["volume"]["SE"])
        process = Process(self._dialog_process, event_data = event_data, 
                          script_list = script_list, 
                          script_count = 0, 
                          script_chr_count = 0, 
                          dialog_surf = dialog_surf, 
                          dialog_topleft = dialog_topleft, 
                          triangle_surf = triangle_surf, 
                          triangle_topleft = triangle_topleft, 
                          is_key_listening = False, 
                          sound = sound)
        self.processes.append(process)

    def save(self, event_data):
        self.set_event_status(event_data["id"], "untriggered")
        self.is_open_saving = True
        self.processes.append(Process(lambda event_data: True, event_data = event_data))

    def change_map(self, event_data):
        process = Process(self._change_map_animate, event_data = event_data, 
                          alpha = 0, 
                          surface = pygame.Surface((WIDTH, HEIGTH)), 
                          change_map_param = ChangeMapParam(self.map_name, 
                                                            event_data["param"]["to_map"], 
                                                            event_data["param"]["inherit_events"], 
                                                            event_data["param"]["player_status"]))
        self.processes.append(process)
        if event_data["param"]["is_open_door_sound"]:
            sound = pygame.mixer.Sound("../Audio/SE/door_open.ogg")
            sound.set_volume(self.menu.settings["volume"]["SE"])
            sound.play()

    def play_close_door_sound(self, event_data = None):
        if event_data is not None:
            self.set_event_status(event_data["id"], "untriggered")
        sound = pygame.mixer.Sound("../Audio/SE/door_close.ogg")
        sound.set_volume(self.menu.settings["volume"]["SE"])
        sound.play()

    def play_sound(self, event_data):
        sound = pygame.mixer.Sound(event_data["param"]["path"])
        sound.set_volume(self.menu.settings["volume"]["SE"])
        sound.play(event_data["param"]["loop"])

    def show_picture(self, event_data):
        img = pygame.image.load(event_data["param"]["img_path"]).convert_alpha()
        w, h = img.get_width(), img.get_height()
        x = (WIDTH - w) // 2
        y = int(HEIGTH*0.4) - (h // 2)
        if event_data["param"].get("is_alpha_animate") is not None:
            if event_data["param"]["is_alpha_animate"]:
                alpha = 0
            else:
                alpha = 255
        else:
            alpha = 255
        process = Process(self._show_picture, event_data = event_data, 
                          img = img, pos = (x, y), alpha = alpha, is_key_listening = False)
        self.processes.append(process)

    def show_choices(self, event_data):
        choice_msg_list = []
        for r in event_data["param"]["choice_code"]:
            start, end = map(int, r.split("-"))
            choice_msg_list += [f"{i}" for i in range(start, end + 1)]
        
        # load image
        surf = pygame.image.load("../Graphics/layer/choice.png").convert_alpha()

        # calculate position
        w, h = surf.get_width(), surf.get_height()
        topleft_list = []
        x = (WIDTH - w) // 2
        for index in range(len(choice_msg_list))[::-1]:
            y = HEIGTH - h - 60 * index - 20
            topleft_list.append((x, y))

        process = Process(self._choice_process, event_data = event_data, 
                          choice_msg_list = choice_msg_list, 
                          topleft_list = topleft_list, 
                          focused_choice = 0, 
                          is_key_listening = False)
        self.processes.append(process)

    def modify_event_status(self, event_data):
        self.set_event_status(event_data["id"], "untriggered")
        mapname = event_data["param"]["map"]
        _id = event_data["param"]["id"]
        status = event_data["param"]["status"]
        self.menu.save_data["map-details"][mapname]["events"][_id]["status"] = status

    # process associated functions
    def _start_map_animate(self, process_class: Process) -> bool:
        speed = 4
        surface = process_class.kwargs["surface"]
        process_class.kwargs["alpha"] -= speed

        if process_class.kwargs["alpha"] <= 0:
            return True

        surface.set_alpha(process_class.kwargs["alpha"])
        self.display_surface.blit(surface, (0,0))
        return False

    def _dialog_process(self, process_class: Process) -> bool:
        kwargs = process_class.kwargs

        self.display_surface.blit(kwargs["dialog_surf"], kwargs["dialog_topleft"])
        
        # script content
        script_content = self.script_contents[kwargs["script_list"][kwargs["script_count"]]]
        speaker_name = script_content.get("speakerName")
        content = script_content["text"]

        # play/stop sound
        sound = kwargs["sound"]
        if kwargs["script_chr_count"] == 0:
            sound.play(-1)
        elif kwargs["script_chr_count"] >= len(content) + 1:
            sound.stop()

        # text animate
        speed = 0.3
        kwargs["script_chr_count"] += speed
        if kwargs["script_chr_count"] >= len(content) + 1:
            kwargs["script_chr_count"] = len(content) + 1
        draw_content = content[:int(kwargs["script_chr_count"])]
        # draw text
        lines = draw_content.split("\n")
        x = kwargs["dialog_topleft"][0] + 40
        y = kwargs["dialog_topleft"][1]
        if speaker_name is not None:
            draw_text(self.display_surface, f"【{speaker_name}】", 30, x, y + 20)
        else:
            y -= 40
        for index, line in enumerate(lines):
            draw_text(self.display_surface, line, 22, x + 20, y + 60 + index*30)

        # draw triangle
        if kwargs["script_chr_count"] == len(content) + 1:
            self.display_surface.blit(kwargs["triangle_surf"], kwargs["triangle_topleft"])

        # next text
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
            if kwargs["is_key_listening"]:
                kwargs["is_key_listening"] = False
                if kwargs["script_chr_count"] < len(content) + 1:
                    kwargs["script_chr_count"] = len(content) + 1
                    sound.stop()
                else:
                    kwargs["script_count"] += 1
                    kwargs["script_chr_count"] = 0
                    if kwargs["script_count"] >= len(kwargs["script_list"]):
                        sound.stop()
                        if process_class.event_data["param"]["is_trigger_available"]:
                            self.set_event_status(process_class.event_data["id"], "untriggered")
                        else:
                            self.set_event_status(process_class.event_data["id"], "finished")
                        return True
        else:
            kwargs["is_key_listening"] = True

        return False

    def _change_map_animate(self, process_class: Process) -> bool:
        speed = 4
        surface = process_class.kwargs["surface"]
        process_class.kwargs["alpha"] += speed

        if process_class.kwargs["alpha"] > 255:
            surface.set_alpha(255)
            self.display_surface.blit(surface, (0,0))
            self.change_map_param = process_class.kwargs["change_map_param"]
            self.set_event_status(process_class.event_data["id"], "untriggered")
            return False
        
        surface.set_alpha(process_class.kwargs["alpha"])
        self.display_surface.blit(surface, (0,0))
        return False

    def _show_picture(self, process_class: Process) -> bool:

        kwargs = process_class.kwargs
        
        # alpha animate
        speed = 4
        kwargs["alpha"] += speed
        if kwargs["alpha"] > 255:
            kwargs["alpha"] = 255
        kwargs["img"].set_alpha(kwargs["alpha"])

        # get key pressed
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
            if kwargs["is_key_listening"]:
                kwargs["is_key_listening"] = False
                if kwargs["alpha"] < 255:
                    kwargs["alpha"] = 255
                else:
                    return True
        else:
            kwargs["is_key_listening"] = True

        self.display_surface.blit(kwargs["img"], kwargs["pos"])

        return False

    def _choice_process(self, process_class: Process) -> bool:
        kwargs = process_class.kwargs

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            if kwargs["is_key_listening"]:
                kwargs["is_key_listening"] = False
                if keys[pygame.K_UP]:
                    kwargs["focused_choice"] = (kwargs["focused_choice"] - 1) % len(kwargs["choice_msg_list"])
                    self.menu.switch_sound.play()
                if keys[pygame.K_DOWN]:
                    kwargs["focused_choice"] = (kwargs["focused_choice"] + 1) % len(kwargs["choice_msg_list"])
                    self.menu.switch_sound.play()
                if keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    self.menu.choose_sound.play()
                    choice = kwargs["choice_msg_list"][kwargs["focused_choice"]]
                    event_id = process_class.event_data["param"]["trigger_event"][choice]
                    self.set_event_status(process_class.event_data["id"], "finished")
                    self.run_event(event_id)
                    return True
        else:
            kwargs["is_key_listening"] = True

        for index, choice in enumerate(kwargs["choice_msg_list"]):
            text = self.script_contents["choice_" + choice]["text"]
            pos = kwargs["topleft_list"][index]
            if index == kwargs["focused_choice"]:
                surf = pygame.image.load("../Graphics/layer/choice_focus.png").convert_alpha()
                surf.set_alpha(230)
                draw_text(surf, text, 22, None, None)
                self.display_surface.blit(surf, pos)
            else:
                surf = pygame.image.load("../Graphics/layer/choice.png").convert_alpha()
                surf.set_alpha(230)
                draw_text(surf, text, 22, None, None)
                self.display_surface.blit(surf, pos)

        return False

    # other functions
    def lock_player(self):
        self.player.direction.x, self.player.direction.y = 0, 0
        self.player.is_keyboard_forbidden = True
    
    def unlock_player(self):
        self.player.is_keyboard_forbidden = False

    def set_event_status(self, event_id, status):
        self.events_data[event_id]["status"] = status

    # system functions
    def create_ID_event_dict(self):
        for event in self.events_data:
            self.ID_to_event.update({event["id"]: self.action_event_dict[event["action"]]})
            if event["type"] == "auto":
                self.auto_collision_events_id.append(event["id"])
    
    def get_script_contents(self):
        with open(self.menu.save_data["map-details"][self.map_name]["script"], mode = "r", encoding = "utf8") as fp:
            self.script_contents = yaml.safe_load(fp)

    def run_inherit_events(self, change_map_param: ChangeMapParam):
        if change_map_param is None:
            return 
        for i in change_map_param.inherit_events:
            if isinstance(i, int):
                self.run_event(i)
            elif isinstance(i, str):
                self.action_event_dict[i]() # only support None param available function

    def run_event(self, event_id):
        self.set_event_status(event_id, "proceeding")
        self.ID_to_event[event_id](self.events_data[event_id])

        # run sync subevents
        if self.events_data[event_id].get("subevents") is not None:
            if self.events_data[event_id]["subevents"].get("sync") is not None:
                for subevent_id in self.events_data[event_id]["subevents"]["sync"]:
                    self.run_event(subevent_id)

    def event_sprite_collision_judge(self, event_sprite):
        trigger = False
        if "up" in self.player.status:
            trigger = -TILESIZE//2 <= self.player.hitbox.topleft[1] - event_sprite.hitbox.bottomleft[1] <= TILESIZE//2 and event_sprite.hitbox.bottomleft[0] <= self.player.hitbox.center[0] <= event_sprite.hitbox.bottomright[0]
        elif "down" in self.player.status:
            trigger = -TILESIZE//2 <= event_sprite.hitbox.topleft[1] - self.player.hitbox.bottomleft[1] <= TILESIZE//2 and event_sprite.hitbox.bottomleft[0] <= self.player.hitbox.center[0] <= event_sprite.hitbox.bottomright[0]
        elif "left" in self.player.status:
            trigger = -TILESIZE//2 <= self.player.hitbox.topleft[0] - event_sprite.hitbox.topright[0] <= TILESIZE//2 and event_sprite.hitbox.topright[1] <= self.player.hitbox.center[1] <= event_sprite.hitbox.bottomright[1]
        elif "right" in self.player.status:
            trigger = -TILESIZE//2 <= event_sprite.hitbox.topleft[0] - self.player.hitbox.topright[0] <= TILESIZE//2 and event_sprite.hitbox.topleft[1] <= self.player.hitbox.center[1] <= event_sprite.hitbox.bottomleft[1]
        return trigger

    def event_trigger_judge(self, event_sprite):
        event_id = event_sprite.event_id
        # whether collided
        if not self.event_sprite_collision_judge(event_sprite):
            return False
        # whether has other requirements
        if self.events_data[event_id].get("events-status-required") is None:
            return True
        for requirement in self.events_data[event_id]["events-status-required"]:
            if self.menu.save_data["map-details"][requirement["map"]]["events"][requirement["id"]]["status"] != requirement["status"]:
                return False
        return True

    def event_listener(self):
        keys = pygame.key.get_pressed()
        events_status = {}
        if not self.player.is_keyboard_forbidden:
            if (keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                if self.is_event_listening:
                    for event_sprite in self.event_sprites:
                        if self.events_data[event_sprite.event_id]["status"] == "untriggered":
                            events_status[event_sprite.event_id] = self.event_trigger_judge(event_sprite)
                        elif self.events_data[event_sprite.event_id]["status"] == "finished":
                            if self.events_data[event_sprite.event_id].get("finished-after-event") is not None:
                                new_event_id = self.events_data[event_sprite.event_id]["finished-after-event"]
                                self.events_data[event_sprite.event_id] = self.events_data[new_event_id]
                                self.events_data[event_sprite.event_id]["id"] = event_sprite.event_id
                                events_status[event_sprite.event_id] = self.event_trigger_judge(event_sprite) and self.events_data[event_sprite.event_id]["status"] == "untriggered"
                    self.is_event_listening = False
            else:
                self.is_event_listening = True
        return events_status

    def collision_auto_events(self):
        if self.is_collision_event_listening and self.is_event_listening:
            for event_sprite in self.event_sprites:
                if event_sprite.event_id in self.auto_collision_events_id:
                    # for event_sprite in self.event_sprites:
                    event_data = self.events_data[event_sprite.event_id]
                    if event_data["status"] != "untriggered":
                        continue
                    if self.event_trigger_judge(event_sprite):
                        self.run_event(event_sprite.event_id)
                        self.is_collision_event_listening = False
        else:
            self.is_collision_event_listening = True

    def listen_and_run_events(self):
        events_status = self.event_listener()
        for event_id, event_status in events_status.items():
            if event_status:
                self.run_event(event_id)

    def run_processes(self):
        remove_list = []
        subevent_id_list = []
        processes_copy = self.processes.copy()
        for index, process in enumerate(self.processes):
            if process.run():
                if process.event_data is not None:
                    if process.event_data.get("subevents") is not None:
                        if process.event_data["subevents"].get("after") is not None:
                            subevent_id_list += process.event_data["subevents"]["after"]
                remove_list.append(index)
        for index in remove_list[::-1]:
            del self.processes[index]
        for event_id in subevent_id_list:
            self.run_event(event_id)
        
        # lock/unlock player
        for process in processes_copy:
            if process.event_data is None:
                continue
            if process.event_data.get("lock-player") is None:
                continue
            if process.event_data["lock-player"]:
                self.lock_player()
                break
        else:
            self.unlock_player()

    def run(self):
        # run auto events
        self.collision_auto_events()

        # run events
        self.listen_and_run_events()

        # run event processes
        self.run_processes()

        return self.change_map_param
