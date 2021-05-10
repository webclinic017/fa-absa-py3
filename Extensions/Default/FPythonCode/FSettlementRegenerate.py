""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementRegenerate.py"
import acm, os, traceback
import FUxCore

try:
    import FOperationsUtils as Utils
    from FOperationsIO import ShowInvalidDataDialog
    from FOperationsLoggers import CreateLogger
    from FOperationsExceptions import InvalidHookException
    
    from FSettlementTradeFilter import RegenerateSettlementTradeFilterHandler
    from FSettlementEODUtils import RegeneratePaymentSelector, EODParameters, RunEODSteps
    from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache
    
except Exception as e:
    acm.Log('Failed to import FSettlementRegenerate')
    acm.Log('Traceback: {}'.format(traceback.format_exc()))
    raise e

#-------------------------------------------------------------------------
def OnOkButtonClicked(panel, dummyCd):
    panel.SetSelection()
    if 0 == panel.m_selection.Size():
        panel.ShowNoSelection()
        return
    panel.Regenerate()

#-------------------------------------------------------------------------
def OnLogToFile(panel, dummyCd):
    if panel.m_logToFile.Checked():
        panel.m_logFilePath.Enabled(True)
    else:
        panel.m_logFilePath.Enabled(False)

#-------------------------------------------------------------------------
def OnAckToPC(panel, dummyCd):
    if panel.m_ackToPC.Checked():
        panel.m_excludePostSec.Enabled(True)
    else:
        panel.m_excludePostSec.Enabled(False)

#-------------------------------------------------------------------------
class RegenerateSettlementsPanel(FUxCore.LayoutPanel):
    def __init__(self):
        self.m_okBtn = None
        self.m_logToConsole = None
        self.m_logToFile = None
        self.m_logFilePath = None
        self.m_selection = acm.FArray()

    #-------------------------------------------------------------------------
    def HandleCreate(self):
        layout = self.SetLayout(self.BuildLayout())
        self.Owner().AddDependent(self)
        self.m_okBtn = layout.GetControl("ok")
        self.m_okBtn.AddCallback("Activate", OnOkButtonClicked, self)
        self.m_ackToPC = layout.GetControl('ackToPC')
        self.m_ackToPC.Checked(True)
        self.m_ackToPC.AddCallback("Activate", OnAckToPC, self)
        self.m_excludePostSec = layout.GetControl('excludePostSec')
        self.m_excludePostSec.Checked(False)
        self.m_createOffsettingSettlements = layout.GetControl("createOffSettingSettlements")
        self.m_createOffsettingSettlements.Checked(False)
        self.m_settleRedemptionSecurities = layout.GetControl("settleRedemptionSecurities")
        self.m_settleRedemptionSecurities.Checked(False)
        self.m_logToConsole = layout.GetControl("logToConsole")
        self.m_logToConsole.Checked(True)
        self.m_logToFile = layout.GetControl("logToFile")
        self.m_logToFile.AddCallback("Activate", OnLogToFile, self)
        self.m_logFilePath = layout.GetControl("logFilePath")
        self.m_logFilePath.SetData("RegenerateSettlements.log")
        self.m_logFilePath.Enabled(False)

    #-------------------------------------------------------------------------
    def BuildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()

        b.BeginVertBox()
        b.  BeginVertBox('EtchedIn', '')
        b.      AddCheckbox('ackToPC', 'Set Acknowledged settlements to Pending Closure')
        b.      AddCheckbox('excludePostSec', 'Exclude Acknowledged security settlements')
        b.      AddCheckbox('createOffSettingSettlements', 'Create offsetting settlements')
        b.      AddCheckbox('settleRedemptionSecurities', 'Settle Redemption Security settlements')
        b.  EndBox()

        b.  BeginVertBox('EtchedIn', 'Log Settings')
        b.    BeginHorzBox()
        b.    AddCheckbox('logToConsole', 'Log to console')
        b.    AddCheckbox('logToFile', 'Log to file')
        b.EndBox()
        b.AddInput('logFilePath', 'Log file')
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
    def ShowNoSelection(self):
        ShowInvalidDataDialog('No trades selected', self.Shell())

    #-------------------------------------------------------------------------
    def SetSelection(self):
        self.m_selection.Clear()
        self.m_selection.AddAll(self.Owner().Selection())

    #-------------------------------------------------------------------------
    def Regenerate(self):
        import FSettlementParameters as Params
        Utils.InitFromParameters(Params)
        userSelectedTrades = self.m_selection.SortByProperty('Oid', True)
        tradeFilterHandler = RegenerateSettlementTradeFilterHandler()
        
        logFilePath, logFileName = os.path.split(str(self.m_logFilePath.GetData()))
        logFilePath = logFilePath if logFilePath else acm.GetFunction('getLogDir', 0)()
    
        logger = CreateLogger(self.m_logToConsole.Checked(), self.m_logToFile.Checked(), True, logFilePath, logFileName)
        
        nettingRuleQueryCache = SettlementNettingRuleQueryCache()
        regeneratePaymentSelector = RegeneratePaymentSelector(userSelectedTrades, tradeFilterHandler, logger)
        
        eodParameters = EODParameters(
            True, 
            self.m_ackToPC.Checked(), 
            self.m_excludePostSec.Checked(),
            False, 
            self.m_createOffsettingSettlements.Checked(), 
            self.m_settleRedemptionSecurities.Checked(), 
            6, 
            'Regenerate Payments For Trades'
            )
        
        try:
            RunEODSteps(regeneratePaymentSelector, eodParameters, nettingRuleQueryCache, logger)
            
        except InvalidHookException as e:
            logger.LP_Log("Exception occurred when performing Regenerate payment for trade: {}".format(e))
            logger.LP_Flush()

#-------------------------------------------------------------------------
def PerformRegenerateSettlementsForTrade():
    arr = acm.FArray()
    arr.Add(acm.FTrade)
    arr.SortByProperty('StringKey', True)
    customPanel = RegenerateSettlementsPanel()
    acm.StartFASQLEditor('Regenerate Payments for Trade', arr, None, None, None, '', False, customPanel)

