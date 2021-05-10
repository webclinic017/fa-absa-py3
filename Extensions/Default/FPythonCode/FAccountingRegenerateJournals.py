""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingRegenerateJournals.py"
import acm
import os, time, traceback
import FUxCore
import FRunScriptGUI

try:
    from FOperationsLoggers import CreateLogger
    from FOperationsIO import IsFileNameValid, IsPathValid, GetDefaultPath, ShowInvalidDataDialog
    from FAccountingAISelectDialog import ShowDialog, AISelectionDialog
    from FAccountingEngineBaseCreator import CreateEngineForTrades, CreateEngineForSettlements, CreateParameters
    from FAccountingOperations import Operation
    import FAccountingParams as Params
except Exception as e:
    acm.Log('Failed to import FAccountingRegenerateJournals')
    acm.Log('Traceback: {}'.format(traceback.format_exc()))
    raise e

#-------------------------------------------------------------------------
def OnOkButtonClicked(panel, cd):
    panel.SetSelection()

    (isValidData, errorMsg) = panel.ValidateFields()

    if isValidData:
        panel.Regenerate()
    else:
        ShowInvalidDataDialog(errorMsg, panel.Shell())

#-------------------------------------------------------------------------
def OnBrowseButtonClicked(panel, cd):
    sel = acm.FFileSelection()
    sel.PickDirectory(True)
    directoryExists = acm.UX().Dialogs().BrowseForFile(acm.UX().SessionManager().Shell(), sel)
    selectedDirectory = None if not directoryExists else sel.SelectedDirectory()
    if not selectedDirectory:
        return None
    panel.m_pathSel.SetValue(selectedDirectory)

#-------------------------------------------------------------------------
def OnLogToFile(panel, cd):
    if panel.m_logToFile.Checked():
        panel.m_pathSelectionBtn.Enabled(True)
        panel.m_pathSel.Enabled(True)
        panel.m_fileName.Enabled(True)
    else:
        panel.m_pathSelectionBtn.Enabled(False)
        panel.m_pathSel.Enabled(False)
        panel.m_fileName.Enabled(False)

#-------------------------------------------------------------------------
def OnAiSelection(panel, cd):
    shell = panel.Shell()
    ShowDialog(shell, panel.m_aiSelectionDialog)
    selectionString = ''
    panel.m_selectedAis.Editable(True)
    panel.m_selectedAis.SetData(selectionString)
    for ai in panel.GetSelectedAccountingInstructions():
        if len(selectionString):
            selectionString += ', ' + ai.Name()
        else:
            selectionString += ai.Name()
    if len(selectionString):
        panel.m_selectedAis.Editable(False)
        panel.m_selectedAis.SetData(selectionString)

#-------------------------------------------------------------------------
def GetParameters():
    extension = acm.FExtensionContext['Standard'].GetExtension('FParameters', 'FObject', 'FRegenerateJournalsParameters')
    param = extension.Value()

    return {str(key): str(param[key]) for key in param.Keys()}

#-------------------------------------------------------------------------
class RegenerateJournalsPanel(FUxCore.LayoutPanel):
    def __init__(self, createEngineCb, eventSource):
        self.m_startDate = None
        self.m_endDate = None
        self.m_pathSel = None
        self.m_fileName = None
        self.m_okBtn = None
        self.m_logToConsole = None
        self.m_logToFile = None
        self.m_selection = acm.FArray()
        self.m_aiSelectionButton = None
        self.m_aiSelectionDialog = AISelectionDialog()
        self.m_selectedAis = None
        self.m_pathSelectionBtn = None
        self.m_parameters = GetParameters()
        self.m_ValidParameterPath = True
        self.m_ValidParameterName = True
        self.m_createEngineCb = createEngineCb
        self.m_eventSource = eventSource

    #-------------------------------------------------------------------------
    def Regenerate(self):
        dateToday = acm.Time.DateToday()
        logFilePath = str(self.m_pathSel.GetValue())
        logFileName = str(self.m_fileName.GetValue())

        logger = CreateLogger(self.m_logToConsole.Checked(), self.m_logToFile.Checked(), Params.detailedLogging, logFilePath, logFileName)
        params = CreateParameters(self.m_startDate.GetValue(), self.m_endDate.GetValue(), dateToday, dateToday, None, None, GetAccountingInstructionFilter(self.GetSelectedAccountingInstructions()))

        Regenerate(self.m_createEngineCb, self.m_selection, logger, params)


    #-------------------------------------------------------------------------
    def ServerUpdate(self, sender, aspect, parameter):
        if parameter == self.m_pathSel:
            if str(self.m_pathSel.GetValue()) and not IsPathValid(str(self.m_pathSel.GetValue())):
                ShowInvalidDataDialog('Log file path does not exist.', self.Shell())
                self.m_pathSel.SetValue('')
        if parameter == self.m_fileName:
            if str(self.m_fileName.GetValue()) and not IsFileNameValid(str(self.m_fileName.GetValue())):
                ShowInvalidDataDialog('Log file name contains invalid characters.', self.Shell())
                self.m_fileName.SetValue('')

    #-------------------------------------------------------------------------
    def InitBinders(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_startDate = self.m_bindings.AddBinder('startDateCtrl', acm.GetDomain('date'), None)
        self.m_endDate = self.m_bindings.AddBinder('endDateCtrl', acm.GetDomain('date'), None)
        self.m_pathSel = self.m_bindings.AddBinder('pathSelCtrl', acm.GetDomain('string'), None)
        self.m_fileName = self.m_bindings.AddBinder('fileNameCtrl', acm.GetDomain('string'), None)

    #-------------------------------------------------------------------------
    def HandleCreate(self):
        layout = self.SetLayout(self.BuildLayout())
        self.Owner().AddDependent(self)
        self.m_okBtn = layout.GetControl("ok")
        self.m_okBtn.AddCallback("Activate", OnOkButtonClicked, self)
        self.m_logToConsole = layout.GetControl("logToConsole")
        self.m_logToConsole.Checked(True)
        self.m_logToFile = layout.GetControl("logToFile")
        self.m_logToFile.AddCallback("Activate", OnLogToFile, self)
        self.m_aiSelectionButton = layout.GetControl("aiSelection")
        self.m_aiSelectionButton.AddCallback("Activate", OnAiSelection, self)
        self.m_selectedAis = layout.GetControl("selectedAis")
        self.m_pathSelectionBtn = layout.GetControl("pathSelection")
        self.m_pathSelectionBtn.AddCallback("Activate", OnBrowseButtonClicked, self)
        self.m_pathSelectionBtn.Enabled(False)
        self.m_bindings.AddLayout(layout)
        self.m_pathSel.Enabled(False)
        self.m_fileName.Enabled(False)
        self.LoggingSettings()

    #-------------------------------------------------------------------------
    def LoggingSettings(self):
        try:
            if self.m_parameters['MandatoryLogging'] == 'True':
                self.m_logToFile.Checked(True)
                self.m_logToFile.Enabled(False)

                path = self.m_parameters['LogfilePath']
                fileName = self.m_parameters['LogfileName']

                if not IsPathValid(path):
                    self.m_ValidParameterPath = False
                elif not IsFileNameValid(fileName):
                    self.m_ValidParameterName = False
                else:
                    self.m_pathSel.SetValue(path)
                    self.m_fileName.SetValue(fileName)
                return
        except:
            acm.Log('Failed to read FParameters FRegenerateJournalsParameters.')

        self.m_logToFile.Checked(False)
        self.m_logToFile.Enabled(True)
        self.m_pathSel.SetValue(GetDefaultPath())
        self.m_fileName.SetValue("RegenerateJournals.log")

    #-------------------------------------------------------------------------
    def ValidateFields(self):
        isValidData = True
        errorMsg = ""

        startDate = self.m_startDate.GetValue()
        endDate = self.m_endDate.GetValue()

        if not self.m_ValidParameterPath:
            errorMsg = "Log file path does not exist. Please check predefined path in FParameters FRegenerateJournalsParameters in the Extension Manager."
            isValidData = False
        elif isValidData and not self.m_ValidParameterName:
            errorMsg = "Log file name contains invalid characters. Please check predefined name in FParameters FRegenerateJournalsParameters in the Extension Manager."
            isValidData = False
        elif isValidData and (self.m_selection.Size() == 0):
            errorMsg = "No {} selected.".format(self.m_eventSource)
            isValidData = False
        elif isValidData and not startDate:
            errorMsg = "Invalid Start Date."
            isValidData = False
        elif isValidData and not endDate:
            errorMsg = "Invalid End Date."
            isValidData = False
        elif isValidData and not self.IsStartLaterThanEnd(startDate, endDate):
            errorMsg = "Start Date later than End Date."
            isValidData = False
        elif isValidData and not IsPathValid(self.m_pathSel.GetValue()) and self.m_logToFile.Checked():
            errorMsg = "Log file path does not exist."
            isValidData = False
        elif isValidData and not IsFileNameValid(self.m_fileName.GetValue()) and self.m_logToFile.Checked():
            errorMsg = "Log file name contains invalid characters."
            isValidData = False
        elif isValidData and not str(self.m_fileName.GetValue()) and self.m_logToFile.Checked():
            errorMsg = "Please enter Log file name."
            isValidData = False
        return (isValidData, errorMsg)

    #-------------------------------------------------------------------------
    def BuildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()

        b.BeginVertBox()
        b.  BeginVertBox('EtchedIn', 'Journal Generation Interval')
        self.m_startDate.BuildLayoutPart(b, 'Start Date')
        self.m_endDate.BuildLayoutPart(b, 'End Date')
        b.  EndBox()

        b.  BeginVertBox('EtchedIn', 'Accounting Instruction Selection')
        b.    BeginHorzBox()
        b.      AddInput('selectedAis', '', 40)
        b.      AddButton('aiSelection', 'Select', False, False)
        b.    EndBox()
        b.EndBox()

        b.  BeginVertBox('EtchedIn', 'Log Settings')
        b.    BeginHorzBox()
        b.      AddCheckbox('logToConsole', 'Log to console')
        b.      AddCheckbox('logToFile', 'Log to file')
        b.    EndBox()
        b.    BeginHorzBox()
        self.m_pathSel.BuildLayoutPart(b, 'Log file path')
        b.      AddButton('pathSelection', '...', False, True)
        b.    EndBox()
        self.m_fileName.BuildLayoutPart(b, 'Log file')
        b.  EndBox()

        b.  BeginVertBox()
        b.    AddSpace(10)
        b.    BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'Regenerate')
        b.    EndBox()
        b.  EndBox()
        b.EndBox()

        b.AddFill()
        b.EndBox()
        return b

    #-------------------------------------------------------------------------
    def IsStartLaterThanEnd(self, startDate, endDate):
        if(startDate > endDate):
            return False
        return True

    #-------------------------------------------------------------------------
    def SetSelection(self):
        self.m_selection.Clear()
        self.m_selection.AddAll(self.Owner().Selection())

    #-------------------------------------------------------------------------
    def GetSelectedAccountingInstructions(self):
        return self.m_aiSelectionDialog.GetSelectedAccountingInstructions()

#-------------------------------------------------------------------------
def GetAccountingInstructionFilter(ais):
    filter = None
    if len(ais):
        aiFilter = acm.CreateFASQLQuery(acm.FTreatmentLink, 'OR')
        for accountingInstruction in ais:
            aiFilter.AddAttrNode('AccountingInstruction.Oid', 'EQUAL', accountingInstruction.Oid())
        filter = aiFilter
    return filter

#-------------------------------------------------------------------------
def Regenerate(createEngineCb, objs, logger, params):
    engine = createEngineCb(params, logger, None, None, False)

    eventSource = str(objs[0].ClassName())

    logger.LP_Log('Regenerate {} journals started by user {} at {}\n'.format(eventSource, str(acm.UserName()), time.ctime()))
    logger.LP_Flush()

    totalResult = engine.Process(objs)

    createdJournals = totalResult.RE_ResultOpAndObjectType(Operation.CREATE, 'FJournal')
    updatedJournals = totalResult.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal')
    nbrExceptions = len(totalResult.RE_Exceptions())

    engine.ClearCalculations()

    logger.LP_Log('\nRegenerate {} journals finished at {}'.format(eventSource, time.ctime()))
    logger.LP_Log('{} journals were created.'.format(createdJournals))
    logger.LP_Log('{} journals were updated.'.format(updatedJournals))
    logger.LP_Log('{} transactions failed to commit.'.format(nbrExceptions))
    logger.LP_Flush()

#-------------------------------------------------------------------------
def PerformRegenerateTradeJournals():
    arr = acm.FArray()
    arr.Add(acm.FTrade)
    arr.SortByProperty('StringKey', True)
    customPanel = RegenerateJournalsPanel(CreateEngineForTrades, 'Trades')
    customPanel.InitBinders()
    acm.StartFASQLEditor('Regenerate Journals Trade', arr, None, None, None, '', False, customPanel)

#-------------------------------------------------------------------------
def PerformRegenerateSettlementJournals():
    arr = acm.FArray()
    arr.Add(acm.FSettlement)
    arr.SortByProperty('StringKey', True)
    customPanel = RegenerateJournalsPanel(CreateEngineForSettlements, 'Settlements')
    customPanel.InitBinders()
    acm.StartFASQLEditor('Regenerate Journals Settlement', arr, None, None, None, '', False, customPanel)

#-------------------------------------------------------------------------
# FRunScriptGUI - FAccountingRegenerateJournals
#-------------------------------------------------------------------------

def CreateSettlementQuery():
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Oid', 'LESS_EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Currency.Name', 'EQUAL', None)
    op = query.AddOpNode('AND')
    op.AddAttrNode('Amount', 'GREATER_EQUAL', None)
    op.AddAttrNode('Amount', 'LESS_EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Counterparty.Name', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Acquirer.Name', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Status', 'EQUAL', None)
    op = query.AddOpNode('AND')
    op.AddAttrNode('Trade.Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Trade.Oid', 'LESS_EQUAL', None)

    return query

#-------------------------------------------------------------------------
def CreateTradeQuery():
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Oid', 'LESS_EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Instrument.Name', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('TradeTime', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Trader.Name', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Counterparty.Name', 'EQUAL', None)
    op = query.AddOpNode('OR')
    op.AddAttrNode('Type', 'EQUAL', None)

    return query

#-------------------------------------------------------------------------
class RegenerateGUI(FRunScriptGUI.AelVariablesHandler):

    #-------------------------------------------------------------------------
    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    #-------------------------------------------------------------------------
    def LogToFileCb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        return fieldValues

    #-------------------------------------------------------------------------
    def SettlementsCb(self, index, fieldValues):
        if fieldValues[index] == '1':
            self.trades.set(fieldValues, None)
            self.trades.enable(False)
            self.createTradeBasedJournals.set(fieldValues, None)
            self.settlements.enable(True)
        elif fieldValues[index] == '0':
            self.settlements.enable(False)
            self.settlements.set(fieldValues, None)

        return fieldValues

    #-------------------------------------------------------------------------
    def TradesCb(self, index, fieldValues):
        if fieldValues[index] == '1':
            self.settlements.set(fieldValues, None)
            self.settlements.enable(False)
            self.createSettlementBasedJournals.set(fieldValues, None)
            self.trades.enable(True)
        elif fieldValues[index] == '0':
            self.trades.enable(False)
            self.trades.set(fieldValues, None)

        return fieldValues

    #-------------------------------------------------------------------------
    def MandatoryFileLogging(self):
        params = GetParameters()
        return params['MandatoryLogging'] != 'True'

    #-------------------------------------------------------------------------
    def __CreateAelVariables(self):
        dirSelectionLogfile = FRunScriptGUI.DirectorySelection()
        dirSelectionLogfile.SelectedDirectory(str(GetDefaultPath()))

        #-------------------------------------------------------------------------
        runTradeRegenerateTT = 'When enabled journals will be created/updated based on trades'
        runSettlementRegenerateTT = 'When enabled journals will be created/updated based on settlements'
        startDateTT = 'Start Date'
        endDateTT = 'End Date'
        accountingIntructionTT = 'Accounting instruction to use for journal generation'
        tradesTT = 'Trades to generate journals for'
        settlementsTT = 'Settlements to generate journals for'

        ttLogToCon = 'Defines whether logging should be done to the console'
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = 'Name of the logfile. Could include the whole path, c:\log\...'


        #-------------------------------------------------------------------------
        variables = [['createTradeBasedJournals', 'Create Journals based on Trades', 'int', [1, 0], 1, 1, 0, runTradeRegenerateTT, self.TradesCb, True],
                     ['createSettlementBasedJournals', 'Create Journals based on Settlements', 'int', [1, 0], 0, 1, 0, runSettlementRegenerateTT, self.SettlementsCb, True],
                     ['startDate', 'Start Date', 'string', None, None, 1, 1, startDateTT, None],
                     ['endDate', 'End Date', 'string', None, None, 1, 1, endDateTT, None],
                     ['accountingInstructions', 'Accounting Instructions', 'string', acm.FAccountingInstruction.Select(""), None, 0, 1, accountingIntructionTT, None],
                     ['trades', 'Trades', 'FTrade', None, CreateTradeQuery(), 0, 1, tradesTT, None, True],
                     ['settlements', 'Settlements', 'FSettlement', None, CreateSettlementQuery(), 0, 1, settlementsTT, None, False],
                     ['LogToConsole', 'Log to console_Logging', 'int', [1, 0], 1, 1, 0, ttLogToCon, None],
                     ['LogToFile', 'Log to file_Logging', 'int', [1, 0], 0, 1, 0, ttLogToFile, self.LogToFileCb, self.MandatoryFileLogging()],
                     ['Logfile', 'Log file_Logging', 'string', None, 'RegenerateJournals.log', 0, 0, ttLogFile, None, False]]

        return variables


ael_gui_parameters = {'windowCaption' : 'Regenerate Journals'}

ael_variables = RegenerateGUI()

#-------------------------------------------------------------------------
def ael_main(variablesDict):

    accountingInstructions = [acm.FAccountingInstruction[aI] for aI in variablesDict['accountingInstructions']]

    startDate = acm.Time.AsDate(variablesDict['startDate'])
    endDate = acm.Time.AsDate(variablesDict['endDate'])
    dateToday = acm.Time.DateToday()

    logToConsole = variablesDict['LogToConsole']
    logToFile = variablesDict['LogToFile']
    fileName = "%s" % variablesDict['Logfile']

    logger = CreateLogger(logToConsole, logToFile, Params.detailedLogging, "", fileName)
    params = CreateParameters(startDate, endDate, dateToday, dateToday, None, None, GetAccountingInstructionFilter(accountingInstructions))

    objs = variablesDict['trades'] if variablesDict['createTradeBasedJournals'] else variablesDict['settlements']
    engine = CreateEngineForTrades if variablesDict['createTradeBasedJournals'] else CreateEngineForSettlements

    if objs.IsEmpty():
        raise Exception('No Trades/Settlements selected.')

    Regenerate(engine, objs, logger, params)
