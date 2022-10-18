import json
# Written by Ashkan.Z
def settings_retriever() -> None:
    """
    Reads a file storing the data for volume adjustment and another file storing
    data to autopause spotify on certain sites.
    """
    with open("vol.json", 'r') as info:
        stuff = json.load(info)
    return stuff


def vol_app_adder(name: str, level=1.0) -> None:
    """
    adds new app to vol.txt if not already in the file.

    Note: currently not going to support adding volume level, will just set it
          to 1.
    """
    with open('vol.json', 'r') as volly:
        stuff = json.load(volly)
        stuff["all"][name] = level
    with open('vol.json', 'w') as volly:
        json.dump(stuff, volly, indent=2)
