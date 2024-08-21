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

    The `trigger` in the page unit in the events in `background-events` shouldn't be `Action Button` or `Player Touch`, and should only be `Autorun` or `Parallel`.

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

    **Parameters:** unneccessary

    Change local switch. 

- `Change Global Switch`

    **Parameters:** unneccessary

    Change global switch.

- `Erase Event`

    **Parameters:** unneccessary
    
    Set the event that executes this command to a null event.

- `Save Data`

    **Parameters:** unneccessary

    Open the save data surface. 
    
    Player's movement will be blocked. 

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```

- ``

    **Parameters:**
    ```json
    {
        
    }
    ```


