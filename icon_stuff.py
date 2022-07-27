from PIL import Image, ImageDraw
from pystray import Icon as icon, Menu as menu, MenuItem as item


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


state = True


def on_clicked(icon, item):
    global state
    global vols, autos, gamesy, activ, pref_master_vol, prev_game

    curr = None
    if state:
        new = active_window_process_name()
        if curr != new:
            print(f'Now on: {new}')

            if new in gamesy and new not in activ:
                activ[new] = vols[new]
                prev_game = new

            if new in vols:
                curr = new
                if prev_game == 'Default':
                    activ = vol_setter(activ, vols[new])
                else:
                    activ = vol_setter(activ, 1.0)
                    master_vol_set(pref_master_vol)
                    prev_game = 'Default'

            else:
                vols[new] = 1.0
                curr = new
                vol_app_adder(new)
    state = not item.checked
