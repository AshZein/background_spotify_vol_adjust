from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

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
