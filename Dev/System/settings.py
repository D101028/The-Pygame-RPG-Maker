# game setup
WIDTH    = 960    
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player':       -26,
    'invisible':    0, 
    'event':        0, 
    'detail':       0
}

# general colors
WATER_COLOR = '#71ddee'
BLACK_COLOR = '#000000'
TEXT_COLOR  = '#EEEEEE'

# data
SAVE_FILE_PATH          = "../data/save/file{}.json"
ORIGIN_SAVE_FILE_PATH   = "../data/save/origin_file.json"
SETTING_FILE_PATH       = "../data/settings/settings.json"

# animation blocks
ANIMATION_BLOCK_SIZE_LIST = [
    (384, 384), 
    (384, 384), 
    (471, 498)
]
