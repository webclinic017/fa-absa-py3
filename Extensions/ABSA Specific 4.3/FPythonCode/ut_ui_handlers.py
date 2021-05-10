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
import json
from types import ModuleType

import acm
from at_logging import getLogger


LOGGER = getLogger(__name__)
LOG_FRAMES = (
    'CInfoManAppFrame',
    'CTradeFilterAppFrame',
)


class RecentFilesHandler(object):
    
    def __init__(self, user_preferences, can_print=False):
        self._user_name = user_preferences.User().Name()
        self._recent_files = user_preferences.RecentFiles().Clone()
        self._recent_dict = self._convert_to_dict()
        self._old_dict = self._get_saved_preferences()
        self._can_print = can_print

    @staticmethod
    def _get_empty_pref_dict():
        output_dict = {}
        for key in LOG_FRAMES:
            output_dict[key] = []
        return output_dict

    @staticmethod
    def _translate_values(entry_list):
        output_list = []
        for entry in entry_list:
            try:
                output_list.append(entry.Name())
            except AttributeError:
                output_list.append(str(entry))
        return output_list
    
    @staticmethod
    def _diff_entries(old_list, new_list):
        if not new_list:
            return []
        if not old_list:
            return new_list
        if not new_list[0] == old_list[0]:
            return new_list[:1]
        return []
    
    def _get_cto(self):
        return acm.FCustomTextObject['%s_PREFERENCES' % self._user_name]
    
    def _create_cto(self):
        cto = acm.FCustomTextObject()
        cto.Name('%s_PREFERENCES' % self._user_name)
        cto.SubType('USER_PREFERENCES')
        return cto
    
    def _convert_to_dict(self):
        output_dict = self._get_empty_pref_dict()
        for key in self._recent_files:
            if str(key) in LOG_FRAMES:
                value = self._translate_values(self._recent_files.At(key))
                output_dict[str(key)] = value
        return output_dict
    
    def _get_saved_preferences(self):
        cto = self._get_cto()
        if cto:
            return json.loads(cto.Text())
        return self._get_empty_pref_dict()
    
    def get_updates(self):
        output_dict = {}
        for key in self._recent_dict:
            if not key in self._old_dict:
                output_dict[key] = self._recent_dict[key]
                continue
            diff_entry_list = self._diff_entries(self._old_dict[key],
                                                 self._recent_dict[key])
            if diff_entry_list:
                output_dict[key] = diff_entry_list
        return output_dict
    
    def update_cto(self):
        if self._recent_dict == self._old_dict:
            return
        cto = self._get_cto()
        if not cto:
            cto = self._create_cto()
        cto.Text(json.dumps(self._recent_dict))
        try:
            cto.Commit()
        except:
            if self._can_print:
                LOGGER.exception('Failed to commit TextObject %s.' % cto.Name())


class EventHandlerBase(object):
    
    @staticmethod
    def _create_cto():
        cto = acm.FCustomTextObject()
        cto.Name('%s_UI' % acm.User().Name())
        cto.SubType('USER_UI')
        return cto
    
    @classmethod
    def update_cto(cls, subject_type, subject_name):
        user_name = acm.User().Name()
        cto = acm.FCustomTextObject['%s_UI' % user_name]
        if not cto:
            cto = cls._create_cto()
        text = '%s\n%s\n%s' % (user_name, subject_type, subject_name)
        cto.Text(text)
        try:
            cto.Commit()
        except:
            pass


class EventHandlerManagerBase(EventHandlerBase):
    
    def ServerUpdate(self, server, aspect, parameter):
        source_workbook = server.ActiveWorkbook().StoredSourceWorkbook()
        if not source_workbook:
            return
        
        # FUiTrdMgrFrame or FBackOfficeManagerFrame
        subject_type = type(server).__name__
        self.update_cto(subject_type, source_workbook.Name())


class EventHandlerASQL(EventHandlerBase):
    
    def ServerUpdate(self, server, aspect, parameter):
        asql_query = server.CurrentObject()
        if not asql_query:
            return
        
        # FASQLEditorFrame
        subject_type = type(server).__name__
        self.update_cto(subject_type, asql_query.Name())


class EventHandlerApps(EventHandlerBase):
    
    def __init__(self):
        self._first_update = True
    
    def ServerUpdate(self, server, aspect, parameter):
        # Update user preferences every time a GUI frame triggers an event
        preferences = acm.GetUserPreferences()
        recent_files = RecentFilesHandler(preferences)
        updates_dict = recent_files.get_updates()
        for key in updates_dict:
            for entry in updates_dict[key]:
                self.update_cto(key, entry)
        recent_files.update_cto()
        
        # Log Workbooks opened in workspace
        if not self._first_update:
            return
        self._first_update = False
        for app in server:
            if ((app.IsKindOf(acm.FUiTrdMgrFrame) or app.IsKindOf(acm.FBackOfficeManagerFrame))
                    and app.ActiveWorkbook().StoredSourceWorkbook()):
                source_workbook = app.ActiveWorkbook().StoredSourceWorkbook()
                subject_type = type(app).__name__
                self.update_cto(subject_type, source_workbook.Name())


def on_create_manager_frame(eii):
    ext_object = eii.ExtensionObject()
    handler = EventHandlerManagerBase()
    ext_object.AddDependent(handler)


def on_create_asql_frame(eii):
    ext_object = eii.ExtensionObject()
    handler = EventHandlerASQL()
    ext_object.AddDependent(handler)


def on_create_run_script_frame(eii):
    ext_object = eii.ExtensionObject()
    current_object = ext_object.CurrentObject()
    if not current_object:
        return
    
    if isinstance(current_object, ModuleType):
        # RunScriptAppFrame
        subject_type = type(ext_object).__name__
        subject_name = current_object.__name__
    else:
        # FAelTask
        subject_type = type(current_object).__name__
        subject_name = current_object.Name()
    
    EventHandlerBase.update_cto(subject_type, subject_name)


def on_create_session(eii):    
    handler = EventHandlerApps()
    ext_object = eii.ExtensionObject()
    ext_object.RunningApplications().AddDependent(handler)
