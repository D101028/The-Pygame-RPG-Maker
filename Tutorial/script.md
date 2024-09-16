# Script

This documentation will introduce you the usage of a script file. 

## Example of a script file

A script file is a yaml file like this. 
```yaml
message_1:
  speakerName: null
  text: |-
    漂亮的人魚雕像。
message_2:
  speakerName: null
  text: |-
    雄偉的銅人。

choice_1:
  text: |-
    你能幫到我嗎？
choice_2:
  text: |-
    你誰啊
choice_3:
  text: |-
    我想進到下一關，可以幫幫我嗎？
```

## Introduction

Script files are recommended to be placed in `/Dev/Script/`

The part of `message_*` is linked to the [Command Unit](./map-data.md#command-unit) of function `Show Text`. 

The part of `choice_*` is linked to the [Command Unit](./map-data.md#command-unit) of function `Show Choices`. 