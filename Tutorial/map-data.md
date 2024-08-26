# Map Data Documentation

This documentation will introduce you the usage of map data in this project. 

### Index
- [Introduction](#introduction-of-main-construction)
- [Part Introduction](#part-introduction)
- [Event Unit](#event-unit)
- [Page Unit](#page-unit)
- [Command Unit](#command-unit)
- [Command Usage](#command-usage)

## Introduction of Main Construction

Let's start with an example: 
```json
{
    "name": "Map03",
    "csvMap": "../Map/map03",
    "ground": "../Graphics/tilemap/ground03.png",
    "BGM": null,
    "BGS": null,
    "ground-SE": [
       {
           "id": 0,
           "path": "../Audio/SE/walking_on_hard_floor.ogg"
       }
    ],
    "script": "../Script/script03.yaml",
    "events": [
        {
            "self-switches": {}, 
            "self-variables": {}, 
            "pages": [
                {
                    "condition": null,
                    "trigger": "Action Button",
                    "contents": [
                        ["Save Data", {}]
                    ]
                }
            ]
        }
    ],
    "background-events": [
        {
            "self-switches": {
                "cover-animate": true
            }, 
            "self-variables": {}, 
            "pages": [
                {
                    "condition": null, 
                    "trigger": "Parallel", 
                    "contents": []
                }, 
                {
                    "condition": "s[cover-animate]",
                    "trigger": "Parallel",
                    "contents": [
                        ["Open Dark Cover", {
                            "size": 128, 
                            "is_animate": true
                        }], 
                        ["Change Local Switch", {
                            "switch": "cover-animate" 
                        }]
                    ]
                }
            ]
        }
    ]
}
```
This is an example of the map data. It can be splitted into several parts. 

First of all, the part
```json
    "name": "Map03",
    "csvMap": "../Map/map03",
    "ground": "../Graphics/tilemap/ground03.png",
    "BGM": null,
    "BGS": null,
    "ground-SE": [
       {
           "id": 0,
           "path": "../Audio/SE/walking_on_hard_floor.ogg"
       }
    ],
    "script": "../Script/script03.yaml",
```
is the basic data of the map. 

Moreover, the parts
```json
    "events": [
        {
            "self-switches": {}, 
            "self-variables": {}, 
            "pages": [
                {
                    "condition": null,
                    "trigger": "Action Button",
                    "contents": [
                        ["Save Data", {}]
                    ]
                }
            ]
        }
    ],
```
and 
```json
    "background-events": [
        {
            "self-switches": {
                "cover-animate": true
            }, 
            "self-variables": {}, 
            "pages": [
                {
                    "condition": null, 
                    "trigger": "Parallel", 
                    "contents": []
                }, 
                {
                    "condition": "s[cover-animate]",
                    "trigger": "Parallel",
                    "contents": [
                        ["Open Dark Cover", {
                            "size": 128, 
                            "is_animate": true
                        }], 
                        ["Change Local Switch", {
                            "switch": "cover-animate" 
                        }]
                    ]
                }
            ]
        }
    ]
```
are the place that events should be placed. 

## Part Introduction

It is strongly recommended to follow the recommendation to name the files and variables, and put files into the recommended directories.

- `name`

    The map name of the file. 
    
- `csvMap`

    The folder path where the map csv files.

    **Recommend:** Name the folder as the map name. Place the folder in `./Dev/Map`.

- `ground`

    The file path of the graphic of the map ground picture. 

    **Recommend:** Place the file in `./Dev/Graphics/bgtile`.

- `BGM`

    The file path of the background music that would be played when the map is loaded, and loop until the map is changed. `null` for not playing any bgm. 

    **Recommend:** Place the file in `./Dev/Audio/BGM`

- `BGS`

    The file path of the background sound that would be played when the map is loaded, and loop until the map is changed. `null` for not playing any bgs. 

    **Recommend:** Place the file in `./Dev/Audio/SE`

- `ground-SE`

    The sound effect data of the ground (walking sound). 
    
    Each sound should be a dictionary like this:
    ```json
    {
        "id": 0, 
        "path": "../Audio/SE/walking_on_hard_floor.ogg"
    }
    ```
    `id` denote the index of the sound, linking to the id in the csv file `map_Groundtype.csv` in `csvMap` folder.

    All of the sounds must be placed in a list as the value of `ground-SE`, like this:
    ```json
    [
        {
            "id": 0, 
            "path": "..."
        }
    ]
    ```

    The `id` in each sound data must match with its index in the list. 

    **Recommend:** Place the Sound files in `./Dev/Audio/SE`.

- `script`

    The file path of the script file including all dialogs in the game.

    Format:
    ```yaml
    message_1: 
    speakerName: name1
    text: |- 
        text1

    message_2: 
    speakerName: name2
    text: |- 
        text2

    choice_1:
    text: |-
        choice 1

    choice_2:
    text: |-
        choice 2
    ```

    **Recommend:** Place the script file in `./Dev/Script`.

- `events`

    Events that will be given an unique id (by its index in list), linking to the id in the csv file `map_Events.csv` in `csvMap`. 

    Format: [Event Unit](#event-unit)

- `background-events`

    Events that will be activated at the background. 

    The `trigger` in the page unit in the events in `background-events` shouldn't be `Action Button` or `Player Touch`; namely, it should only be `Autorun` or `Parallel`.

    Format: [Event Unit](#event-unit)

## Event Unit

Format:
```json
{
    "self-switches": {}, 
    "self-variables": {}, 
    "pages": [
        /* page units */
    ]
}
```

- `self-switches`

    Local switches of the event. Switches saved here will be discarded (refreshed) when the map unloaded (changed).

    Format:
    ```json
    {
        "self-switches": {
            "switch-name": true,  /* a bool */
            "switch-name-2": false
        }
    }
    ```

    Switch name mustn't have characters: `[`, `]`, space.

- `self-variables`

    Local variables of the event. Variables saved here will be discarded (refreshed) when the map unloaded (changed).

    Format:
    ```json
    {
        "self-variables": {
            "variable-name": "value", /* a string */
            "variable-name-2": "value2"
        }
    }
    ```

    Variable name mustn't have characters: `[`, `]`, space.

- `pages`

    A list contains several page units. 
    
    Just like `match` in Python. The begin of every page unit has a `condition` denoting if the case (page) is selected. And the selected page (as same as this event) will be activated when `trigger` condition is achieved. 

    For details, view [Page Unit](#page-unit).

## Page Unit

Format:

```json
{
    "condition": null, 
    "trigger": "Action Button", 
    "contents": [
        /* command units */
    ]
}
```

- `condition`

    The condition for whether to select this page. 

    The value can be a string or null (null for default). The string law is showed below.

    - `s[switch-name]`

        Get the switch named "switch-name" from Local switches and Global switches respectively. If not found, raise an error. 
    
    - `v[variable-name] (operator) (value)`

        Get the variable named "variable-name" from Local variables and Global variables respectively. If not found, raise an error. 

        `(operator)` must be replaced by `==`, `>`, `<`, `>=`, `<=`, `!=`. 

        `(value)` must be replaced by an integer like `0`, `-1`, `100`, or another variable. 

- `trigger`

    The type of how to trigger the event. 

    There're 4 types, which are showing below.

    - `Action Button`

        Event will be activated when player presses the confirm key and character is facing and near to the event block. 

    - `Player Touch`

        Event will be activated when player touches the event block. 

    - `Autorun`

        Event will be activated while the page unit is selected. Player's movement will be locked during the Autorun events.

    - `Parallel`

        Similar to `Autorun`, but player's movement won't be blocked.

- `contents`

    List of command units. 

    Format: [Command Unit](#command-unit)

There must be one page unit in the pages which `condition` value is null. 

## Command Unit

Basis of the components of command unit: 
```json
["(Command Name)", {
    /* parameters */
}]
```
`(Command Name)` must be replaced by any command name listed in [Command Usage](#command-usage), and the parameters must be given properly. 

## Command Usage

- `Print Test`

    **Parameters:** 
    ```json
    {
        "text": "value", /* a string */
    }
    ```

    Print the text value in terminal. 

- `Set Local Variable`

    **Parameters:**
    ```json
    {
        "variable": "value", /* a string */
        "value": 0 /* an integer */
    }
    ```

    Set a local variable. 

- `Set Local Switch`

    **Parameters:**
    ```json
    {
        "switch": "value", // a string
        "value": true // a bool
    }
    ```

    Set a local switch.

- `Set Global Variable`

    **Parameters:**
    ```json
    {
        "variable": "value", // a string
        "value": 0 // an integer
    }
    ```

    Set a global variable.

- `Set Global Switch`

    **Parameters:**
    ```json
    {
        "switch": "value", // a string
        "value": true // an integer
    }
    ```

    Set a global switch.

- `Change Local Switch`

    **Parameters:** 
    ```json
    {
        "switch": "value" // a string
    }
    ```

    Change local switch. 

- `Change Global Switch`

    **Parameters:** 
    ```json
    {
        "switch": "value" // a string
    }
    ```

    Change global switch.

- `Erase Event`

    **Parameters:** unneccessary
    
    Set the event that executes this command to a null event.

- `Save Data`

    **Parameters:** unneccessary

    Open the save data surface. 
    
    Player's movement will be blocked. 

- `Change Map`

    **Parameters:**
    ```json
    {
        "to_map": "Map01", // a string 
        "exit_sound": "/path/to/sound/file", // a string (default: null)
        "enter_sound": "/path/to/sound/file", // a string (default: null)
        "player_status": {
            "pos": [0, 0], // a two-integer list
            "status": "up_idle", // a string
            "map": "Map01", // a string
        }
    }
    ```

    @`to_map`: Name of the map you want to change to. \
    @`exit_sound`: File path of the sound you want to play when unloading the map. \
    @`enter_sound`: File path of the sound you want to play when entering the map. \
    @`player_status`: A dictionary of player status when entering the map. 
    - @`pos`: Player tile position. 
    - @`status`: Player graphic status. 
    - @`map`: Map name. (must be as same as the `to_map` parameter)

    Change the map to another map. 

- `Show Text`

    **Parameters:**
    ```json
    {
        "script_ranges": [
            "1-5", "7-7"
        ] // a string list
    }
    ```

    @`script_ranges`: String format: `(int1)-(int2)`, where `(int1)` and `(int2)` are two integers and `(int1) <= (int2)`, denoting the script ranges in file `script` from `message_(int1)` to `message_(int2)`. 

    Show the dialog of text in the scripts in the file `script`. 

    Player's movement will be blocked. 

- `Show Choices`

    **Parameters:**
    ```json
    {
        "script_ranges": [
            "1-3", "4-4"
        ], // a string list
        "after": {
            "(choice 1)": [/* command units */], 
            "(choice 2)": [/* command units */], 
            "(choice 3)": [/* command units */], 
            "(choice 4)": [/* command units */]
        } // a dictionary, key: a string; value: a list of command units
    }
    ```

    @`script_ranges`: String format: `(int1)-(int2)`, where `(int1)` and `(int2)` are two integers and `(int1) <= (int2)`, denoting the script ranges in file `script` from `choice_(int1)` to `choice_(int2)`. \
    @`after`: A dictionary, in which keys must be the choice strings, and values must be a list of command units. 

    Show the dialog of choices in the scripts in the file `script`. The value of `after` (command units) will be run when the choice of its key are chosen. 

    Player's movement will be blocked. 

- `Show Picture`

    **Parameters:**
    ```json
    {
        "filepath": "/path/to/picture", // a string
        "is_alpha_animate": true // a bool (default: false)
    }
    ```

    @`filepath`: The file path of a picture you want to show. \
    @`is_alpha_animate`: Whether the enter/exit animation should be played. 

    Show the given picture on the screen. 

    Player's movement will be blocked.

- `Conditional Branch`

    **Parameters:**
    ```json
    {
        "if": "s[switch-name]", // a string
        "then": [/* command units */], // a list of command units
        "else": [/* command units */] // a list of command units (default: null)
    }
    ```

    @`if`: A condition-type string (such as a switch, variables with operator) \
    @`then`: Command units here will be run if the `if` condition is true. \
    @`else`: Command units here will be run if the `if` condition is false. 

    An if-else conditional branch. 

- `Loop`

    **Parameters:**
    ```json
    {
        "condition": "s[switch-name]", // a string
        "do": [/* command units */] // a list of command units
    }
    ```

    @`condition`: A condition-type string (such as a switch, variables with operator) \
    @`do`: Command units here will be run looply if the `condition` is true until the `condition` turns false. 

    A while-like loop. 

- `Game Over`

    **Parameters:**
    ```json
    {
        "script_ranges": [
            "1-2", "3-3"
        ], // a string list (default: null)
        "play_sound": "/path/to/sound" // a string (default: null)
    }
    ```
    @`script_ranges`: String format: `(int1)-(int2)`, where `(int1)` and `(int2)` are two integers and `(int1) <= (int2)`, denoting the script ranges in file `script` from `message_(int1)` to `message_(int2)`. \
    @`play_sound`: File path of the file you want to play. 

    Show the game over surface and show the given text and play the given sound. 

    Player can do nothing but open and manipulate the menu after triggering this command unit. 

- `Open Dark Cover`

    **Parameters:**
    ```json
    {
        "size": 64, // an integer
        "is_animate": false // a bool (default: false)
    }
    ```

    @`size`: The radius of the bright area around the player's character. \
    @`is_animate`: Whether to play the dark appearing animation. 

    Open the dark surface to block player's vision. 

- `Close Dark Cover`

    **Parameters:**
    ```json
    {
        "is_animate": false // a bool (default: false)
    }
    ```

    @`is_animate`: Whether to play the dark removing animation. 

    Close the dark surface that blocking player's vision. 

- `Add Animation Block`

    **Parameters:**
    ```json
    {
        "unit_pos": [1, 2], // a two-integer list
        "animation_id": 0, // an integer (default: null)
        "file_path": "/path/to/graphic", // a string (default: null)
        "animation_speed": 0.87, // a float (default: 0.15)
        "unit_move_route": [
            [0.1, 0.3], [8, 1.2]
        ], // a list of two-float lists(default: null)
        "interval": 87, // an interger (default: 60)
        "loop": 3 // (default: -1)
    }
    ```

    @`unit_pos`: The original tile position of the animation block. \
    @`animation_id`: The id of the animation graphic. \
    @`file_path`: The file path of the animation graphic. \
    @`animation_speed`: The reciprocal of the frames number between the change of the animation. \
    @`unit_move_route`: The tile positions that the animation block will move through. \
    @`interval`: The frames number of the animation block moving between two adjacent positions. \
    @`loop`: The number of how many times the animation block will move through the route repeadedly. 

    Blit the animation block on the map. 
