from pystray import MenuItem as item
import pystray
from PIL import Image
# got this from here:
# https://stackoverflow.com/questions/47095129/pystray-systray-icon


def action():
    pass


def action_quit():
    return False


def starter():
    image = Image.open("image.jpg")
    menu = (item('Quit', action), item('name', action))
    return image, menu


# generator = starter()
# icon = pystray.Icon("name", generator[0], "title", generator[1])
# icon.run()
