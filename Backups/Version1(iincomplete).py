import time

import psutil
import win32gui
import win32process
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume



# This Version changes the volume for any application not just games.

def settings_retriever(vol: dict, auto_pause: dict, games: dict) -> None:
    """
    Reads a file storing the data for volume adjustment and another file storing
    data to autopause spotify on certain sites.
    """
    with open("vol.txt", 'r') as volly:
        volly.readline()
        volly.readline()
        x = volly.readlines()
        non_games = []
        game = []

        gam = True
        for line in x:
            if "NOT GAMES" in line:
                gam = False
            elif line == '\n':
                pass
            elif gam:
                y = line.strip()
                game.extend(y.split('='))
            else:
                y = line.strip()
                non_games.extend(y.split('='))

        num = False
        prev = None
        for stuff in non_games:
            if num:
                vol[prev] = float(stuff)
                num = False
            else:
                vol[stuff] = None
                prev = stuff
                num = True

        num = False
        prev = None
        for stuff in game:
            if num:
                vol[prev] = float(stuff)
                games[prev] = float(stuff)
                num = False
            else:
                vol[stuff] = None
                games[stuff] = None
                prev = stuff
                num = True

    # setting up auto pause configurations
    with open('auto.txt', 'r') as auto:
        auto.readline()
        x = auto.readlines()
        w = []

        for line in x:
            y = line.strip()
            w.extend(y.split('='))

        skip = False
        prev = None

        for stuff in w:
            if skip:
                # '1' means auto pause on, '0' means autopause off
                if stuff == '1':
                    auto_pause[prev] = True
                    skip = False
                else:
                    auto_pause[prev] = False
                    skip = False
            else:
                auto_pause[stuff] = False
                prev = stuff
                skip = True


def vol_app_adder(name: str, level=1.0) -> None:
    """
    adds new app to vol.txt if not already in the file.

    Note: currently not going to support adding volume level, will just set it
          to 1.
    """
    with open('vol.txt', 'a') as volly:
        volly.write(name + '=' + str(level) + '\n')


def master_vol_set(level: float) -> None:
    """
    Sets the windows master volume to <level>
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Found from this forum page: https://github.com/AndreMiras/pycaw/issues/13
    volume.SetMasterVolumeLevelScalar(level, None)


def vol_setter(active: dict, level=1.0) -> dict:
    """
    Sets spotify's volume to the correct intended level. Does not change volume
    if the game is still open, that's what the active list is for.

    Note: defaults to 1.0

    *** inspired by Pycaw docs example
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
                vol.SetMasterVolume(level, None)
                print(f"Spotify vol now: {level_temp}")
        except AttributeError:
            pass

    return acti


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
    vols = {'Default': 1.0}
    autos = {}
    gamesy = {}
    activ = {}
    pref_master_vol = 0.25
    prev_game = 'Default'

    settings_retriever(vols, autos, gamesy)
    print("----STARTED----")

    curr = None
    while True:
        new = active_window_process_name()
        if curr != new:
            print(f'Now on: {new}')

            if new in gamesy and new not in activ:
                activ[new] = vols[new]
                prev_game = new

            if new in vols:
                curr = new
                print(activ)
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
