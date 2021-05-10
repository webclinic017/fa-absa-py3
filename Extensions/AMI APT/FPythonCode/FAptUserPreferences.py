
import os
import re
import acm
import time
import glob
import ctypes
import getpass
import FAptReportCommon
import FAptReportUtils
import xml.etree.cElementTree as ElementTree
from subprocess import Popen, call, PIPE
 

class FAptUserPreferences(object):
    USER_PREFERENCES_XML = 'APTUserPreferences'
    APTPRO_EXE = 'APTPro.exe'
    APT_PATH = 'APT_INSTALLATION_PATH'
    APT_MODELS_PATH = 'APT_MODELS_PATH'

    def __init__(self):
        self.hndws = []
        self.app_data_apt_path = self.get_app_data_apt_path()

    def foreach_window(self, hwnd, lParam):
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if IsWindowVisible(hwnd):
            if ('APTPro') in buff.value:
                self.hndws.append(hwnd)
                return False
        return True

    def hide_window(self):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        EnumWindows(EnumWindowsProc(self.foreach_window), 0)

    def run(self, command, exe):
        p = Popen(command, shell=False, executable=exe, stdout=PIPE, stderr=PIPE)
        while not self.hndws:
            self.hide_window()
        SetWindowPos = ctypes.windll.user32.SetWindowPos
        TOGGLE_HIDEWINDOW = 0x80
        for hwnd in self.hndws:
            SetWindowPos(hwnd, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)
        time.sleep(1)
        p.kill()
        self.write_apt_user_preferences_file()
        return p.communicate()

    def write_file(self, user_preferences_path):
        with open(user_preferences_path, 'w') as f:
            context = acm.GetDefaultContext()
            preferences = str(context.GetExtension("FStringResource", "FObject", self.USER_PREFERENCES_XML).Value())
            ads = ''.join((FAptReportUtils.FAptPath.get_customer_name(), '$'))
            user = getpass.getuser()
            preferences = re.sub('\*\*\*\*', user, preferences)
            preferences = re.sub('####', ads, preferences)
            f.write(preferences)
            f.close()
            
    def get_app_data_apt_path(self):
        app_data_path = FAptReportCommon.AptDatabasePath.get_csidl_appdata_path()
        return os.path.join(app_data_path, 'APT\APTPro\*')

    def write_apt_user_preferences_file(self):
        for path in glob.glob(self.app_data_apt_path):
            user_preferences_path = os.path.join(path, FAptReportCommon.AptDatabasePath.USER_PREFERENCES_FILE)
            self.write_file(user_preferences_path)
            
    @classmethod
    def get_apt_exe_path(cls):
        apt_path = FAptReportUtils.FAptReportParameters().get(cls.APT_PATH)
        os.chdir(apt_path)
        apt_exe_path = None
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if apt_exe_path:
                break
            for filename in (f for f in filenames if f == '%s' % cls.APTPRO_EXE):
                apt_exe_path = os.path.join(dirpath, filename)
        return apt_exe_path
        
    def user_preferences_exists(self):
        for path in glob.glob(self.app_data_apt_path):
            user_preferences_path = os.path.join(path, FAptReportCommon.AptDatabasePath.USER_PREFERENCES_FILE)
            if not os.path.exists(user_preferences_path):
                return 0
        return 1

    def create(self):
        if not self.user_preferences_exists():
            try:
                apt_exe_path = self.get_apt_exe_path()
                self.run(apt_exe_path, None)
            except Exception as err:
                raise err
