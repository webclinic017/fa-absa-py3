"""-----------------------------------------------------------------------------
PURPOSE                 : Tracking of UI events. The functionality is based on
                          FUIEventHandlers and User Preferences such that 
                          ut_ui_handlers.py stores information about the events
                          in custom text objects on the user side, and ATS 
                          (ut_ats.py) handles server-side logging.
REQUESTER               : Anwar Banoo
DEVELOPER               : Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer        Description
--------------------------------------------------------------------------------
2019-04-17  CHG1001620422  Libor Svoboda    Create CSV output, 
                                            Add OPS manager workbooks
"""
import datetime
import os

import acm
from at_ael_variables import AelVariableHandler
from at_classes import Singleton
from at_logging import getLogger
from ut_ui_handlers import RecentFilesHandler


LOGGER = getLogger(__name__)
TRANSLATE = {
    'CInfoManAppFrame': 'Information Manager',
    'RunScriptAppFrame': 'Run Script',
    'FAelTask': 'Run Task',
    'FUiTrdMgrFrame': 'Trading Manager',
    'FBackOfficeManagerFrame': 'OPS Manager',
    'FASQLEditorFrame': 'Insert Items',
    'CTradeFilterAppFrame': 'Trade Filter',
}
OUTPUT_FILE = 'User_Events_{:%Y-%m-%d}.csv'
OUTPUT_DIR = r'L:\FALOG\PRODA\USER_EVENTS'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
ATS_PARAMS = {
    'path': OUTPUT_PATH,
}
ATS_OUTPUT = {}

ael_variables = AelVariableHandler()
ael_variables.add(
    'output_dir',
    label='Output Directory',
    default=OUTPUT_DIR,
)
ael_variables.add(
    'output_file',
    label='Output File',
    default=OUTPUT_FILE,
)


def write_to_file(output_string, output_date):
    if output_date in ATS_OUTPUT:
        output_path = ATS_OUTPUT[output_date]
    else:
        dt = datetime.datetime(*acm.Time.DateToYMD(output_date))
        output_path = ATS_PARAMS['path'].format(dt)
        ATS_OUTPUT[output_date] = output_path
    open_mode = 'w'
    if os.path.exists(output_path):
        open_mode = 'a'
    with open(output_path, open_mode) as output_file:
        output_file.write(output_string + '\n')


class TrackingAts(object, metaclass=Singleton):
    
    def __init__(self):
        self._preferences_queue = []
        self._texts_queue = []
        self._preferences = acm.FPreferences.Select('')
        self._preferences.AddDependent(self)
        self._text_objects = acm.FCustomTextObject.Select('subType="USER_UI"')
        self._text_objects.AddDependent(self)
    
    @staticmethod
    def _output(*args):
        output = ','.join([acm.Time.TimeNow()] + [str(arg) for arg in args])
        LOGGER.info('User Event: %s' % output)
        write_to_file(output, acm.Time.DateToday())
    
    def ServerUpdate(self, sender, aspect, entity):
        if entity.IsKindOf(acm.FPreferences):
            self._preferences_queue.append(entity)
        
        if entity.IsKindOf(acm.FCustomTextObject):
            self._texts_queue.append(entity.Text())
    
    def process_updates(self):
        while self._preferences_queue:
            preferences = self._preferences_queue.pop(0)
            user_name = preferences.User().Name()
            recent_files = RecentFilesHandler(preferences, True)
            updates_dict = recent_files.get_updates()
            for key in updates_dict:
                for entry in updates_dict[key]:
                    self._output(user_name, TRANSLATE[key], entry)
            recent_files.update_cto()
        
        while self._texts_queue:
            text = self._texts_queue.pop(0)
            try:
                user_name, frame, subject = text.split('\n')
            except ValueError:
                LOGGER.exception('Failed to parse TextObject: %s.' % text)
            else:
                self._output(user_name, TRANSLATE[frame], subject)
    
    def remove_all_subscriptions(self):
        self._preferences.RemoveDependent(self)
        self._text_objects.RemoveDependent(self)


def start():
    TrackingAts()
    LOGGER.info('ATS Started at %s' % acm.Time.TimeNow())


def start_ex(params):
    output_path = os.path.join(params['output_dir'], params['output_file'])
    ATS_PARAMS['path'] = output_path
    start()


def stop():
    ats = TrackingAts()
    ats.remove_all_subscriptions()
    LOGGER.info('ATS Finished at %s' % acm.Time.TimeNow())


def work():
    ats = TrackingAts()
    ats.process_updates()
