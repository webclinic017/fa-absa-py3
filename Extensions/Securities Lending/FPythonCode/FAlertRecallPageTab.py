""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FAlertRecallPageTab.py"

import acm, ael
import FSheetUtils
from FParameterSettings import ParameterSettingsCreator
from FAlertPageBase import AlertPage
from FIntegratedWorkbenchUtils import GetAttributeInModule 
from FSecLendUtils import logger

class AlertRecallPage(AlertPage):

    _SETTINGS = ParameterSettingsCreator.FromRootParameter('AlertRecallPage')

    TAB_NAME = 'Recall'
    COMPLIANCE_RULE = list(_SETTINGS.ComplianceRules())
    DEFAULT_FOLDER = _SETTINGS.DefaultStoredQueryFolder()
 
    def InitControls(self, layout):
        self.m_sheet = FSheetUtils.Sheet(layout.GetControl('sheet').GetCustomControl())
        self.m_sheet.ShowGroupLabels(False)
        self.m_sheet.ShowRowHeaders(False)
        
        self.SetDefaultContents()
        self.dismiss = layout.GetControl('dismiss')
        self.dismiss.AddCallback('Activate', self.DismissSelectedAlerts, None)
        self.dismiss.SetIcon('Delete', False)
        
        self.reset = layout.GetControl('reset')
        self.reset.AddCallback('Activate', self.ResetFilter, None)
        self.reset.SetIcon('Refresh', False)
        
        self.clear = layout.GetControl('clear')
        self.clear.AddCallback('Activate', self.ClearAlerts, None)
        self.clear.SetIcon('Delete', False)

        self.filter = layout.GetControl('filter')
        self.filter.AddCallback('Activate', self.EditFilter, None)
        self.filter.SetIcon('Filter', False)
        
        self.handle = layout.GetControl('handle')
        self.handle.AddCallback('Activate', self.OnHandle, None)
        self.handle.SetIcon('Goto', False)
                
        self.details = layout.GetControl('details')
        self.details.AddCallback('Activate', self.OnDetails, None)
        self.details.SetIcon('MoveSheet', False)
                

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.          AddButton('handle', 'Apply',  True, False)
        b.          AddButton('dismiss', 'Clear',  True, False)
        b.          AddButton('details', 'Details..', True, False)
        b.          AddFill()
        b.          AddButton('clear',   'Clear All',  True, False)
        b.          AddButton('reset',   'Reset',      True, False)
        b.          AddButton('filter',  'Filter..',  True, False)
        b.  EndBox()
        b.  AddCustom('sheet', 'sheet.FAlertSheet', 1040, 200, -1, -1, self.SettingsContents())
        b.EndBox()
        return b 

