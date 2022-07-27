# import time
#
# from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# x = AudioUtilities.GetAllSessions()
# for session in x:
#     try:
#         if session.Process.name() == 'Spotify.exe':
#             print('yippee')
#             time.sleep(5)
#             vol = session._ctl.QueryInterface(ISimpleAudioVolume)
#             vol.SetMasterVolume(1, None)
#     except AttributeError:
#         pass

# time.sleep(5)
# from typing import Optional
# from ctypes import wintypes, windll, create_unicode_buffer
#
# def getForegroundWindowTitle() -> Optional[str]:
#     hWnd = windll.user32.GetForegroundWindow()
#     length = windll.user32.GetWindowTextLengthW(hWnd)
#     buf = create_unicode_buffer(length + 1)
#     windll.user32.GetWindowTextW(hWnd, buf, length + 1)
#
#     # 1-liner alternative: return buf.value if buf.value else None
#     if buf.value:
#         return buf.value
#     else:
#         return None
# print(getForegroundWindowTitle())

# from win32gui import  GetWindowText, GetForegroundWindow
# print(GetWindowText(GetForegroundWindow()))


# applications = {'Overwatch': 0.18, None:}
# while True:
#     x = getForegroundWindowTitle()


# import psutil, win32process, win32gui, time
#
#
# def active_window_process_name():
#     pid = win32process.GetWindowThreadProcessId(
#         win32gui.GetForegroundWindow())  # This produces a list of PIDs active window relates to
#     # print(type(psutil.Process(pid[-1]).name())) #pid[-1] is the most likely to survive last longer
#
#
# time.sleep(3)  # click on a window you like and wait 3 seconds
# active_window_process_name()
#
# import threading, win32gui, win32process, psutil
# from tkinter import *
#
# root = Tk()
# s = StringVar()
#
#
# def active_window_process_name():
#     try:
#         pid = win32process.GetWindowThreadProcessId(
#             win32gui.GetForegroundWindow())
#         return (psutil.Process(pid[-1]).name())
#     except:
#         pass
#
#
# def to_label():
#     global s
#     while True:
#         s.set(active_window_process_name())
#     return
#
#
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# # volume.GetMute()
# #
# print(volume.GetVolumeRange())
# volume.SetMasterVolumeLevelScalar(0.35, None)
#
# # Found from this forum page: https://github.com/AndreMiras/pycaw/issues/13
# print(volume.GetMasterVolumeLevelScalar())


# import pystray
#
# from PIL import Image, ImageDraw
#
#
# def create_image(width, height, color1, color2):
#     # Generate an image and draw a pattern
#     image = Image.new('RGB', (width, height), color1)
#     dc = ImageDraw.Draw(image)
#     dc.rectangle(
#         (width // 2, 0, width, height // 2),
#         fill=color2)
#     dc.rectangle(
#         (0, height // 2, width // 2, height),
#         fill=color2)
#
#     return image
#
#
# # In order for the icon to be displayed, you must provide an icon
# # icon = pystray.Icon(
# #     'test name',
# #     icon=create_image(64, 64, 'black', 'white'))
# #
# #
# # # To finally show you icon, call run
# # icon.run()
#
# from pystray import Icon as icon, Menu as menu, MenuItem as item
#
# state = False
#
#
# def on_clicked(icon, item):
#     global state
#     print("poopCheck")
#     state = not item.checked
#
#
# # Update the state in `on_clicked` and return the new state in
# # a `checked` callable
# icon('test', create_image(64, 64, 'black', 'white'), menu=menu(
#     item(
#         'Checkable',
#         on_clicked,
#         checked=lambda item: state))).run()


import asyncio
import time

from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager


async def get_media_info():
    sessions = await MediaManager.request_async()

    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.
    current_session = sessions.get_current_session()
    #print(current_session)
    #time.sleep(10000)
    if current_session:  # there needs to be a media session running
        if current_session.source_app_user_model_id == TARGET_ID:
            info = await current_session.try_get_media_properties_async()

            # song_attr[0] != '_' ignores system attributes
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])

            return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    #raise Exception('TARGET_PROGRAM is not the current media session')


if __name__ == '__main__':
    current_media_info = asyncio.run(get_media_info())
    print(current_media_info)
