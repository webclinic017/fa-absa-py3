""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FRunScriptBase.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FRunScriptBase

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""

import acm
import FUxCore
import FRunScriptGUI
import FAssetManagementUtils
import FExportUtils

logger = FAssetManagementUtils.GetLogger()


class AelVariablesBase(object):
    """Base class for ael variables. Instantiating the class appends LogLevel
       and UpdateExportStateOnly to ael_variables.
       The method GetVariables() returns the ael variables list.
       The class also implements a method to extend ael_variables with
       query dialog variables.
       Method: AddACMQueryDialogVariable()
       Parameters:
         name; the name of the variable
         display; the display name on the field
         tt; tool tip for the field
         prefix = ''; name prefix used to filter FStoredASQLQueries
         subType = ''; query class used to filter FStoredASQLQueries
       Example:
       ael_var_base = AelVariablesBase()
       name = 'acmQuery'
       display = 'ACM Queries'
       tt = 'Select the query or queries that correspond to the set of trades to be exported.'
       ael_var_base.AddACMQueryDialogVariable(name, display, tt)
       ael_variables = ael_var_base.GetVariables()
    """

    class ACMQueryDialog(object):

        def __init__(self, prefix, subType):
            self.prefix = prefix
            self.subType = subType

        def CustomACMQueryDialog(self, shell, params):
            customDlg = SelectACMQueriesCustomDialog(shell, params, self.prefix, self.subType)
            return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)

    def __init__(self):
        self.ael_variables = []
        self._AddLogVariable()
        
    def _AddTradeQueryDialogVariable(self, queryPrefix):
        ttAcmQuery = "Select the query or queries that correspond to the set of trades to be exported."
        self.AddACMQueryDialogVariable('ACMQueries', 'Trades', ttAcmQuery, queryPrefix, 'FTrade')
        
    def _AddInstrumentQueryDialogVariable(self, queryPrefix):
        ttAcmQuery = 'Select the query or queries that correspond to the set of instruments to be exported.'
        self.AddACMQueryDialogVariable('ACMInstrumentQuery', 'Instruments to export', ttAcmQuery, queryPrefix, 'FInstrument')
        
    def AddACMQueryDialogVariable(self, name, display, tt='', prefix='', subType=''):
        acmQueryDlg = AelVariablesBase.ACMQueryDialog(prefix, subType)
        var = [name, display, 'string', [], None, 0, 1, tt, None, 1, acmQueryDlg.CustomACMQueryDialog]
        self.ael_variables.append(var)

    def _AddLogVariable(self):
        ttLogMode = 'Select the verbosity of logging output by the export task.'
        var = ['LogLevel', 'Logging Level_Advanced', 'string', sorted(FAssetManagementUtils.logDict), '1. Normal', 2, 0, ttLogMode]
        self.ael_variables.append(var)

    def GetVariables(self):
        return self.ael_variables

class AelVariablesExport(AelVariablesBase):

    def __init__(self):
        super(AelVariablesExport, self).__init__()
        self._AddUpdateExportStateOnlyVariable()
        self._AddTestModeVariable()
        self._AddUseGUIPartyVariable()
        self._AddPartyVariable()
        self._AddForceProcessAllTradesVariable()
        self._AddRetryFailedExportsVariable()
        
    def _AddUpdateExportStateOnlyVariable(self):
        ttUpdateExportStateOnly = 'Update the state of exportable trades only. An export of data to the remote party will not be performed.'
        var = ['UpdateExportStateOnly', 'Update trade export states only', 'string', [True, False], False, 0, 0, ttUpdateExportStateOnly, self._UpdateExportStateOnlyCb, True]
        self.ael_variables.append(var)

    def _AddAlwaysGenerateFileVariable(self):
        ttAlwaysGenerateFile = 'Always generate export file even no trade has been created/updated'
        var = ['AlwaysGenerateFile', 'Always generate export file_Advanced', 'string', [True, False], False, 0, 0, ttAlwaysGenerateFile, None, False]
        self.ael_variables.append(var)
        
    def _AddTestModeVariable(self):
        ttTestMode = 'Perform an export test. Export files will be created, but business processes will not be updated.'
        var = ['TestMode', 'Test mode_Advanced', 'string', FExportUtils.ExportTestMode.MODES, FExportUtils.ExportTestMode.DEFAULT_MODE, 2, 0, ttTestMode, self._DontSendExportCb, 1]
        self.ael_variables.append(var)
        
    def _AddUseGUIPartyVariable(self):
        ttPartyDef = 'Use GUI to select which party to send file to.'
        var = ['UseGUIParty', 'Enable party selection_Advanced', 'string', [True, False], False, 0, 0, ttPartyDef, self._UseGUIPartyCb, True]
        self.ael_variables.append(var)
    
    def _AddPartyVariable(self):
        ttParty = 'Choose Party to send file to.'
        var = ['Party', 'Party_Advanced', 'string', FExportUtils.ExportParty.MODES, FExportUtils.ExportParty.DEFAULT_MODE, 2, 0, ttParty, None, 0]
        self.ael_variables.append(var)

    def _AddForceProcessAllTradesVariable(self):
        ttForceProcessAllTrades = 'Force processing of ALL exportable trades, regardless of whether they have been updated or not.'
        var = ['ForceProcessAllTrades', 'Force processing of all exportable trades_Advanced', 'string', [True, False], False, 0, 0, ttForceProcessAllTrades, None, 1]
        self.ael_variables.append(var)
    
    def _AddRetryFailedExportsVariable(self):
        ttRetry = 'Retry to send export files that failed in a previous export'
        var = ['RetryFailedExports', 'Retry failed exports_Advanced', 'string', [True, False], False, 0, 0, ttRetry]
        self.ael_variables.append(var)

    def _UpdateExportStateOnlyCb(self, index, fieldValues):
        exportOnlyCtrls = (i for i in range(len(self.ael_variables)) if self.ael_variables[i][0] in ('ACMQueries', 'TestMode', 'UseGUIParty', 'Party', 'AlwaysGenerateFile'))

        for ctrlIndex in exportOnlyCtrls:
            if self.ael_variables[ctrlIndex][FRunScriptGUI.Controls.NAME] == 'Party':
                self.ael_variables[ctrlIndex][FRunScriptGUI.Controls.ENABLED] = False
                continue
            if self.ael_variables[ctrlIndex][FRunScriptGUI.Controls.NAME] == 'UseGUIParty':
                fieldValues[ctrlIndex] = False
                
            self.ael_variables[ctrlIndex][FRunScriptGUI.Controls.ENABLED] = (fieldValues[index] == 'false')
        return fieldValues
        
    def _DontSendExportCb(self, index, fieldValues):
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][0] == 'UseGUIParty':
                ctrlIndex = i
            if self.ael_variables[i][0] == 'Party':
                partyCtrl = i
        self.ael_variables[ctrlIndex][9] = True
        if fieldValues[index] in ('Disabled - Do NOT transfer export file(s)', 'Enabled - Do NOT transfer export file(s)'):
            fieldValues[ctrlIndex] = False
            self.ael_variables[partyCtrl][9] = False
            self.ael_variables[ctrlIndex][9] = False
        return fieldValues
        
    def _UseGUIPartyCb(self, index, fieldValues):
        guiPartyCtrls = (i for i in range(len(self.ael_variables)) if self.ael_variables[i][0] == 'Party')
        for ctrlIndex in guiPartyCtrls:
            self.ael_variables[ctrlIndex][9] = (fieldValues[index] == 'true')
        return fieldValues
        
    def _AddEmailSettingVariables(self):
        ttEmail = 'Send an email notification with the exported trades.'
        var = ['SendEmail', 'Enable email notification_Email Settings', 'string', [True, False], False, 
            False, False, ttEmail, self._SetEnabled]
        self.ael_variables.append(var)
    
        ttRecipient = 'The recipients of the email notification'
        var = ['EmailRecipient', 'Recipient_Email Settings', 'string', None, None, False, False, ttRecipient, 
                None, True]
        self.ael_variables.append(var)
    
        ttSender = 'The sender field used in email notifications.'
        var = ['EmailSender', 'Sender_Email Settings', 'string', None, 
            'noreply.export@frontarena.com', False, False, ttSender, None, True]
        self.ael_variables.append(var)
        
        variables = ('%EXPORT_DATE%', '%EXPORT_TIME%', '%FILENAME%', '%PARTY%', 
            '%SHEET_TEMPLATE%', '%RECIPIENTS%', '%INTEGRATION%')
        ttVariables = 'The following variables may be used: ' + ', '.join(variables)
        
        ttSubject = 'The subject used in email notifications. ' + ttVariables
        var = ['EmailSubject', 'Subject_Email Settings', 'string', None, 
            'Exported file %FILENAME%', False, False, ttSubject, None, True]
        self.ael_variables.append(var)
        
        ttBody = 'The body/message used in email notifications. ' + ttVariables
        var = ['EmailBody', 'Body_Email Settings', 'string', None, 
            'Exported trades using sheet template %SHEET_TEMPLATE% to %PARTY% at %EXPORT_DATE% %EXPORT_TIME%.', 
            False, False, ttBody, None, True]
        self.ael_variables.append(var)
        
    def _SetDefaultRecipient(self, partyId, FTPContactName):
        recipient = None
        party = acm.FParty[partyId]
        for contact in party.Contacts():
            if contact.Name() == FTPContactName:
                recipient = contact.Email()
        
        for var in self.ael_variables:
            if var[FRunScriptGUI.Controls.NAME] == 'EmailRecipient':
                var[FRunScriptGUI.Controls.DEFAULT] = recipient
                        
    def _AddEnableFileSettingVariables(self):
        ttFileSettings = "Configure the exported file's name and path"
        var = ['EnableFileSettings', 'Enable file settings_File Settings', 'string', [True, False], False,  
                False, False, ttFileSettings, self._SetEnabled]
        self.ael_variables.append(var)
        
                        
    def _AddFileSettingVariables(self):
        
        ttFilePath = 'The path where the file will be saved' 
        var = ['FilePath', 'File path_File Settings', 'string', None, 'C:\\', False, False, ttFilePath, None,
                True]
        self.ael_variables.append(var)
        
        variables = ('%EXPORT_DATE%', '%EXPORT_TIME%', '%PARTY%', '%SHEET_TEMPLATE%')
        ttFilename = 'The following variables may be used for the filename: ' + ', '.join(variables)
        var = ['FileName', 'Filename_File Settings', 'string', None, 'filename', False, False, ttFilename, 
                None, True]
        self.ael_variables.append(var)
    
    def _SetEnabled(self, index, fieldValues):
        enabled = fieldValues[index]
        fieldPrefix = None
        if self.ael_variables[index][FRunScriptGUI.Controls.NAME] == 'SendEmail':
            fieldPrefix = 'Email'
        elif self.ael_variables[index][FRunScriptGUI.Controls.NAME] == 'EnableFileSettings':
            fieldPrefix = 'File'
        
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][FRunScriptGUI.Controls.NAME].startswith(fieldPrefix):
                self.ael_variables[i][FRunScriptGUI.Controls.ENABLED] = enabled
        return fieldValues

def OnAddClicked(self, cd ):
    key = self.m_keys.GetData()
    if key:
        AddItem(self.valueList, self.m_values, key)
        RemoveItem(self.keyList, self.m_keys, key)

def AddItem(objList, itemList, item):
    objList.Add(item)
    objList.SortByProperty('Name')
    itemList.Populate(objList)
    itemList.SetData(item)

def RemoveItem(objList, itemList, item):
    index = objList.IndexOf(item)
    objList.Remove(item)
    itemList.RemoveItem(item)
    if objList:
        if len(objList) <= index:
            index -= 1
        newItem = objList[index]
        if newItem:
            itemList.SetData(newItem)

def OnRemoveClicked(self, cd ):
    value = self.m_values.GetData()
    if value:
        AddItem(self.keyList, self.m_keys, value)
        RemoveItem(self.valueList, self.m_values, value)

def OnRemoveAllClicked(self, cd ):
    for key in self.valueList:
        self.keyList.Add(key)
    self.valueList = acm.FList()
    self.m_values.Clear()
    self.keyList.SortByProperty('Name')
    self.m_keys.Populate(self.keyList)
    SelectFirstItem(self.keyList, self.m_keys)

def SelectFirstItem(objList, itemList):
    if objList:
        firstItem = objList[0]
        itemList.SetData(firstItem)

class SelectObjCustomDialog(FUxCore.LayoutDialog):
    KEYS = 'keys'
    VALUES = 'values'
    BTN_ADD = 'btnAdd'
    BTN_REMOVE = 'btnRemove'
    BTN_REMOVE_ALL = 'btnRemoveAll'

    def __init__(self, shell, params, header):
        self.shell = shell
        self.choices = params['choices']
        self.selected = params['selected']
        self.caption = 'Select %s' % header
        self.keyLabel = header
        self.valueLbl = 'Selected %s' % header
        self.keyList = acm.FList()
        self.valueList = acm.FList()
        self.keyObj = None
        self.query = None
        self.m_keys = None
        self.m_fuxDlg = None
        self.m_values = None
        self.m_btnAdd = None
        self.m_btnRemove = None
        self.m_btnRemoveAll = None

    def HandleApply( self ):
        resultDic = acm.FDictionary()
        resultDic.AtPut('result', list(self.valueList))
        return resultDic

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_keys = layout.GetControl(self.KEYS)
        self.m_values = layout.GetControl(self.VALUES)
        self.m_btnAdd = layout.GetControl(self.BTN_ADD)
        self.m_btnAdd.AddCallback('Activate', OnAddClicked, self)
        self.m_btnRemove = layout.GetControl(self.BTN_REMOVE)
        self.m_btnRemove.AddCallback('Activate', OnRemoveClicked, self)
        self.m_btnRemoveAll = layout.GetControl(self.BTN_REMOVE_ALL)
        self.m_btnRemoveAll.AddCallback('Activate', OnRemoveAllClicked, self)
        self.PopulateControls()
        self.SetControlData()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.   AddLabel("lblKeys", self.keyLabel)
        b.   AddList(self.KEYS, 10, -1, 50, -1 )
        b.  EndBox()
        b.  BeginVertBox()
        b.   AddFill()
        b.   AddButton( self.BTN_ADD, "Add" )
        b.   AddButton( self.BTN_REMOVE, "Remove" )
        b.   AddSpace(3)
        b.   AddButton( self.BTN_REMOVE_ALL, "Remove All" )
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(2)
        b.  BeginVertBox()
        b.   AddLabel("lblValues", self.valueLbl)
        b.   AddList(self.VALUES, 10, -1, 50, -1 )
        b.  EndBox()
        b. AddSpace(3)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

    def PopulateControls(self):
        self.keyList = self.LoadData(self.keyObj)
        if self.keyList:
            self.m_keys.Populate(self.keyList)
            self.m_keys.SetData(self.keyList.First())
        else:
            logger.warn('The query "%s" on FStoredASQLQuery did not produce any result', self.query)

    def SetControlData(self):
        for key in self.selected:
            key = getattr(acm, self.keyObj)[key]
            self.keyList.Remove(key)
            self.valueList.Add(key)
        self.m_keys.Populate(self.keyList)
        self.valueList.SortByProperty('Name')
        self.m_values.Populate(self.valueList)
        SelectFirstItem(self.keyList, self.m_keys)
        SelectFirstItem(self.valueList, self.m_values)

    def LoadData(self, objName):
        collection = getattr(acm, objName).Select(self.query)
        return collection.SortByProperty('Name')


class SelectACMQueriesCustomDialog(SelectObjCustomDialog):
    def __init__(self, shell, params, queryPrefix='', subType='', header='ACM Queries'):
        SelectObjCustomDialog.__init__(self, shell, params, header)
        self.keyObj = 'FStoredASQLQuery'
        subtype_str = 'and subType = "%s"' % subType if subType else ''
        self.query = 'user = "" %s and name like %s' % (subtype_str, queryPrefix+'*')