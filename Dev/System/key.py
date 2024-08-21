import pygame

class KeySettings:
    up = pygame.K_UP
    down = pygame.K_DOWN
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    confirm_1 = pygame.K_z
    confirm_2 = pygame.K_RETURN
    cancel_1 = pygame.K_ESCAPE
    cancel_2 = pygame.K_x
    menu_1 = pygame.K_ESCAPE
    menu_2 = pygame.K_x
    run = pygame.K_LSHIFT
    page_left = pygame.K_q
    page_right = pygame.K_w
    journal = pygame.K_m

    keys_list = ["up", "down", "left", "right", 
                 "confirm_1", "confirm_2", "cancel_1", "cancel_2", 
                 "menu_1", "menu_2", "run", "page_left", "page_right", "journal"]

    @classmethod
    def get_dict(cls):
        return {
            "up": cls.up, 
            "down": cls.down, 
            "left": cls.left, 
            "right": cls.right, 
            "confirm_1": cls.confirm_1, 
            "confirm_2": cls.confirm_2, 
            "cancel_1": cls.cancel_1, 
            "cancel_2": cls.cancel_2, 
            "menu_1": cls.menu_1, 
            "menu_2": cls.menu_2, 
            "run": cls.run, 
            "page_left": cls.page_left, 
            "page_right": cls.page_right, 
            "journal": cls.journal
        }
    
    @classmethod
    def set_key_by_idx(cls, idx: int, value: int):
        match idx:
            case 0:
                cls.up = value
            case 1:
                cls.down = value
            case 2:
                cls.left = value
            case 3:
                cls.right = value
            case 4:
                cls.confirm_1 = value
            case 5:
                cls.confirm_2 = value
            case 6:
                cls.cancel_1 = value
            case 7:
                cls.cancel_2 = value
            case 8:
                cls.menu_1 = value
            case 9:
                cls.menu_2 = value
            case 10:
                cls.run = value
            case 11:
                cls.page_left = value
            case 12:
                cls.page_right = value
            case 13:
                cls.journal = value

    @classmethod
    def get_key_by_idx(cls, idx: int):
        match idx:
            case 0:
                return cls.up
            case 1:
                return cls.down
            case 2:
                return cls.left
            case 3:
                return cls.right
            case 4:
                return cls.confirm_1
            case 5:
                return cls.confirm_2
            case 6:
                return cls.cancel_1
            case 7:
                return cls.cancel_2
            case 8:
                return cls.menu_1
            case 9:
                return cls.menu_2
            case 10:
                return cls.run
            case 11:
                return cls.page_left
            case 12:
                return cls.page_right
            case 13:
                return cls.journal


class KeyPress:
    keys = pygame.key.get_pressed()

    @classmethod
    def setup(cls, data: dict):
        if data.get("up") is not None:
            KeySettings.up = data["up"]
        if data.get("down") is not None:
            KeySettings.down = data["down"]
        if data.get("left") is not None:
            KeySettings.left = data["left"]
        if data.get("right") is not None:
            KeySettings.right = data["right"]
        if data.get("confirm_1") is not None:
            KeySettings.confirm_1 = data["confirm_1"]
        if data.get("confirm_2") is not None:
            KeySettings.confirm_2 = data["confirm_2"]
        if data.get("cancel_1") is not None:
            KeySettings.cancel_1 = data["cancel_1"]
        if data.get("cancel_2") is not None:
            KeySettings.cancel_2 = data["cancel_2"]
        if data.get("menu_1") is not None:
            KeySettings.menu_1 = data["menu_1"]
        if data.get("menu_2") is not None:
            KeySettings.menu_2 = data["menu_2"]
        if data.get("run") is not None:
            KeySettings.run = data["run"]
        if data.get("page_left") is not None:
            KeySettings.page_left = data["page_left"]
        if data.get("page_right") is not None:
            KeySettings.page_right = data["page_right"]
        if data.get("journal") is not None:
            KeySettings.journal = data["journal"]

    @classmethod
    def update(cls):
        cls.keys = pygame.key.get_pressed()
    
code_key_dict = {
    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
    71: "G",
    72: "H",
    73: "I",
    74: "J",
    75: "K",
    76: "L",
    77: "M",
    78: "N",
    79: "O",
    80: "P",
    81: "Q",
    82: "R",
    83: "S",
    84: "T",
    85: "U",
    86: "V",
    87: "W",
    88: "X",
    89: "Y",
    90: "Z",
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    13: "Enter",
    32: "Space",
    8: "Backspace",
    9: "Tab",
    16: "Shift",
    17: "Ctrl",
    18: "Alt",
    20: "Caps Lock",
    27: "Esc",
    38: "Arrow Up",
    40: "Arrow Down",
    37: "Arrow Left",
    39: "Arrow Right",
    36: "Home",
    35: "End",
    33: "Page Up",
    34: "Page Down",
    45: "Insert",
    46: "Delete",
    192: "`",
    189: "-",
    187: "=",
    219: "[",
    221: "]",
    220: "\\",
    186: ";",
    222: "'",
    188: ",",
    190: ".",
    191: "/"
}
