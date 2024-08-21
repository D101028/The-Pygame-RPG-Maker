# Map Data Documentation

This documentation will introduce you the usage of map data in this project. 

### Index
- [Introduction](#introduction-of-main-construction)
- [Part Introduction](#part-introduction)
- [Event Unit](#event-unit)
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

    Format: [Event Unit](#event-unit)

## Event Unit

## Command Unit

## Command Usage
