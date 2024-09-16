# Settings

This documentation will show you how to create a setting file. 

## Example of a setting file

A setting file is a json file like this. 
```json
{
    "volume": {
        "BGM": 0.7499999999999998,
        "BGS": 0.6999999999999997,
        "SE": 0.6999999999999997
    },
    "keys": {
        "up": 1073741906,
        "down": 1073741905,
        "left": 1073741904,
        "right": 1073741903,
        "confirm_1": 122,
        "confirm_2": 32,
        "cancel_1": 27,
        "cancel_2": 120,
        "menu_1": 27,
        "menu_2": 120,
        "run": 1073742049,
        "page_left": 113,
        "page_right": 119,
        "journal": 109
    }
}
```

## Introduction

This file can be editted by the menu in the game (press ESC). 

There are two parts in this file. 

### Part 1. "volume"

This part is for controlling the voices' volume in the game, including "BGM", "BGS", and "SE", whose values are floats ranging from 0 to 1. 

### Part 2. "keys"

This part is not neccessary. If this part isn't exist, the system will automatically fill it out as default. 

In this part, there're several items, such as "up", "down", etc. For all items, view the example above. 
