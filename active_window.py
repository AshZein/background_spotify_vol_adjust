import psutil
import win32gui
import win32process

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

import psutil
import win32gui
import win32process

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
#>>>>>>> fcbb245ca87b85934ae786a9a3bca2a61ecac463
