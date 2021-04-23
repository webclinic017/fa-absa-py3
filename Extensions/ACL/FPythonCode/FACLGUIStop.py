""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLGUIStop.py"
import ctypes
from ctypes import wintypes
import thread
import threading
import sys
import os
import time

class FACLGUIStop(threading.Thread):
    def __init__(self):
        self.stoppedAutomatically = False
        self.windowTitle = "Stop script {0}".format(os.getpid())
        threading.Thread.__init__(self)

    def __enter__(self):
        self.setDaemon(True)
        self.start()

    def __exit__(self, type, value, traceback):
        self.stoppedAutomatically = True
        FindWindowFunc = ctypes.windll.user32.FindWindowA
        FindWindowFunc.arrgtypes = [wintypes.LPCSTR, wintypes.LPCSTR]
        FindWindowFunc.restype = wintypes.HWND
        windowHandle = FindWindowFunc(None, self.windowTitle)
        if windowHandle != 0:
            SendNotifyMessageFunc = ctypes.windll.user32.SendNotifyMessageA
            SendNotifyMessageFunc(windowHandle, 16, 0, 0)
        return False

    def run(self):
        time.sleep(2)
        if not self.stoppedAutomatically:
            MessageBox = ctypes.windll.user32.MessageBoxA
            MessageBox(None, 'Stop script', self.windowTitle, 0)
        if not self.stoppedAutomatically:
            thread.interrupt_main()
        sys.exit(0)