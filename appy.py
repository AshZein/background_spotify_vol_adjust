import time

from file_manip import *
from volume_manip import *
from active_window import active_window_process_name

# Written by Ashkan.Z

if __name__ == '__main__':
    settings = settings_retriever()

    vols = settings['all']
    autos = settings['auto_pause']
    gamesy = settings['games']
    # activ stores the current open applications, so spotify volume is not
    # adjusted while for example using chrome while waiting for a match to load
    activ = {}
    pref_master_vol = settings["pref_master_vol"]
    prev_game = 'Default'

    print("----STARTED----")

    # *** NOTE add gui update button the says following: "sorry, function not
    # available please update to add"
    startty = True
    curr = None
    while True:
        # the or True is a placeholder for when I fix is_spot_open
        if True:
            new = active_window_process_name()
            if curr != new:
                print(f'Now on: {new}')

                # checks to see if current window is a game, adds it to activ
                if new in gamesy and new not in activ:
                    activ[new] = vols[new]
                    prev_game = new

                # checks if the current focused window has been used before, while
                # program is running
                if new in vols:
                    curr = new

                    # if prev_game is default that means the current focused window
                    # is not one in which volume adjustment is needed
                    if prev_game == 'Default':
                        activ = vol_setter(activ, vols[new])

                    # an application which needs spotify's volume adjusted
                    else:
                        activ = vol_setter(activ)
                        master_vol_set(pref_master_vol)
                        # master_vol_set(vols[prev_game])
                        prev_game = 'Default'

                # adds the current focused window to the json file for review by the
                # user.
                else:
                    vols[new] = 1.0
                    curr = new
                    vol_app_adder(new)
