import json

def check_content(content: list):
    if not isinstance(content, list):
        raise TypeError(f"content must be a list, not {type(content)}")
    if len(content) != 2:
        raise RuntimeError(f"wrong content length: {len(content)}")
    ########## 待完成 ###########

def check_bg_events(bgevents: list):
    check_events(bgevents)
    for event in bgevents:
        for page in event["pages"]:
            if page["trigger"] in ("Action Button", "Player Touch"):
                raise RuntimeError("trigger of background event can't be in (\"Action Button\", \"Player Touch\")")

def check_event_condition(condition: str | None):
    if condition is None:
        return 
    if not isinstance(condition, str):
        raise TypeError(f"condition in page must be None or a str, not {type(condition)}")

def check_events(events: list[dict]):
    if not isinstance(events, list):
        raise TypeError(f"events must be a list of dict, not {type(events)}")
    for event in events:
        if not isinstance(event, dict):
            raise TypeError(f"event in events must be a dict, not {type(event)}")
        if event.get("self-switches") is None:
            raise RuntimeError(f"lost event argument `self-switches`")
        if not isinstance(event["self-switches"], dict):
            raise TypeError(f"self-switches must be a dict, not " + str(type(event["self-switches"])))
        if event.get("self-variables") is None:
            raise RuntimeError(f"lost event argument `self-variables`")
        if not isinstance(event["self-variables"], dict):
            raise TypeError(f"self-switches must be a dict, not " + str(type(event["self-switches"])))
        
        if event.get("pages") is None:
            raise RuntimeError(f"lost event argument `pages`")
        if not isinstance(event["pages"], list):
            raise TypeError(f"pages must be a list, not " + str(type(event["pages"])))
        for page in event["pages"]:
            if not isinstance(page, dict):
                raise TypeError(f"page in pages must be a dict, not {type(page)}")
            try:
                page["condition"]
            except IndexError:
                raise RuntimeError(f"lost page argument `condition`")
            if not isinstance(page["condition"], type(None)) and not isinstance(page["condition"], str):
                check_event_condition(page["condition"])
            if page.get("trigger") is None:
                raise RuntimeError(f"lost page argument `trigger`")
            if page["trigger"] not in ("Autorun", "Parallel", "Player Touch", "Action Button"):
                raise RuntimeError(f'page argument trigger must be in ("Autorun", "Parallel", "Player Touch", "Action Button"), not ' + str(page["trigger"]))
            if page.get("contents") is None:
                raise RuntimeError(f"lost page argument `contents`")
            if not isinstance(page["contents"], list):
                raise TypeError(f"contents must be a list, not " + str(type(page["contents"])))
            for content in page["contents"]:
                check_content(content)

def check_map(mapdata: dict):
    if not isinstance(mapdata, dict):
        raise TypeError(f"mapdata must be a dict, not {type(mapdata)}")
    for key in ("name", "csvMap", "ground", "BGM", "BGS", "ground-SE", "script", "events", "background-events"):
        mapdata[key]
    check_events(mapdata["events"])
    check_bg_events(mapdata["background-events"])

def check_settings(setting_data: dict):
    if not isinstance(setting_data, dict):
        raise TypeError(f"setting data must be a dict, not {type(setting_data)}")
    if setting_data.get("volume") is None:
        raise RuntimeError("lost setting argument: `volume`")
    if not isinstance(setting_data["volume"], dict):
        raise TypeError(f"value of volume must be a dict, not " + str(setting_data["volume"]))
    for i in ("BGM", "BGS", "SE"):
        if setting_data["volume"].get(i) is None:
            raise RuntimeError(f"lost volume argument: `{i}`")

if __name__ == "__main__":
    with open("../data/map/Map01.json", mode = "r") as file:
        mapdata = json.load(file)

    check_map(mapdata)

    print("Everything is alright!")

