import time

import psutil
import win32gui
import win32process
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from file_manip import *
from icon_stuff import *


def master_vol_set(level: float) -> None:
    """
    Sets the windows master volume to <level>
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if volume.GetMasterVolumeLevelScalar() > level:
        # Found from this forum page: https://github.com/AndreMiras/pycaw/issues/13
        volume.SetMasterVolumeLevelScalar(level, None)
        print(f"changed master volume to:{level}")


def vol_setter(active: dict, level=1.0) -> dict:
    """
    Sets spotify's volume to the correct intended level. Does not change volume
    if the game is still open, that's what the active list is for.

    Note: defaults to 1.0

    *** inspired by Pycaw docs example

    *** Consider a bit of graduation to the change in volume level, 2-3seconds
        for 0-1.0, adjust accordingly i.e. 0.2- 0.6 would be 0.8-1.2seconds
    """
    sessions = AudioUtilities.GetAllSessions()
    acti = {}
    level_temp = level
    # checking whether a game session is still active.
    for session in sessions:
        try:
            if session.Process.name() in active:
                acti = active
                level_temp = active[session.Process.name()]
        except AttributeError:
            pass

    # setting spotifies volume level
    for session in sessions:
        try:
            if session.Process.name() == 'Spotify.exe':
                vol = session._ctl.QueryInterface(ISimpleAudioVolume)
                vol.SetMasterVolume(level_temp, None)
                print(f"Spotify vol now: {level_temp}")
        except AttributeError:
            pass

    return acti


def auto_pause():
    """
    autopause for when media is playing from certain sites (i.e. youtube..)
    """


def active_window_process_name() -> str:
    """Gets the active window in its application name format (so .exe form)

    retrieved from:
    https://stackoverflow.com/questions/14394513/win32gui-get-the-current-active-application-name
    """
    while True:
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.
                                                        GetForegroundWindow())
            return psutil.Process(pid[-1]).name()
        except:
            pass


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
                    prev_game = 'Default'

            # adds the current focused window to the json file for review by the
            # user.
            else:
                vols[new] = 1.0
                curr = new
                vol_app_adder(new)
