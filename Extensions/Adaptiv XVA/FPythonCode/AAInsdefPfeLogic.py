""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAInsdefPfeLogic.py"
import acm
from AAInsdefPfePanel import AAInsdefPfePanel
import AAParamsAndSettingsHelper
import AAPFE_Dialog

ERROR_NO_TRADE = "Trade needed for PFE Calculations."
ERROR_NOT_SIMULATED = "Trade has to have status 'Simulated'."
ERROR_NOT_IN_CREDIT_BALANCE = "Trade has to have a Credit Balance."
ERROR_IS_CREDIT_BALANCE = "The trade itself can't be a Credit Balance Instrument."
ERROR_NOT_SAVED = "Trade/Instrument has been modified, please save before PFE calculation."
WARNING_TRADE_MODIFIED = "Trade/Instrument has been modified since last PFE calculation."
MSG_CALC_DONE = "Calculation done."
INIT_RESULTS_MSG = {'IncPFE': "", 'PFE': "", 'AfterPFE':""}
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

class AAInsdefPfeLogic:

    def __init__(self, eii):
        
        self._panel = AAInsdefPfePanel(self)
        self.eii = eii
        self._paceConsumer = None
        usePace = AAParamsAndSettingsHelper.getUsePaceSetting()
        if usePace:
            try:
                from FPacePfeTaskConsumer import FPacePfeTaskConsumer
                self._paceConsumer = FPacePfeTaskConsumer()
                self._paceConsumer.SetObserver(self)
                
            except Exception as e:
                logger.WLOG("WARNING: %s.\nFailed to use PACE mode.\nPlease "
                            "check that you have loaded the "
                            "Pace Core Module to the current context.\n"
                            "Use local calculation instead." %(str(e)))
            
        self._modSinceLastCalc = False
        self._calcInitialized = False
        
        self._cInsdef = None
        self._editIns = None
        self._editTrd = None
        self._currentPFEResult = None
        self._currentAfterPFEResult = None
        
        
    def Panel(self):
        return self._panel

    
    def OnTaskSuccess(self, msgDic):
        self.__SetResult(msgDic)
        self.__SetStatus( MSG_CALC_DONE )
        
    def OnTaskFail(self, msg):
        self._calcInitialized = False
        self.__SetResult(INIT_RESULTS_MSG)
        self.__SetStatus(msg)
    
    def OnTaskStatus(self, msg):
        self.__SetStatus(msg)
    
    def _InitDependents(self):
        self.__UpdateDependents()
    
    def _CreateTask(self):
        self.__PrepareForNewTask()
        try:
            self.__AssertTradeUnmodified()
            self.__AssertValidTrade()
            self.__PrivateCreateTask()
        except Exception as e:
            self.__ForceSetStatus( str(e) )
            self.__UpdateControls()
    
    def _showGraph(self):
        try:
            if self._currentPFEResult and self._currentAfterPFEResult:
                customDlg = AAPFE_Dialog.AAPFEDialog(self._currentPFEResult, self._currentAfterPFEResult)
                acm.UX().Dialogs().ShowCustomDialogModal(self.eii.ExtensionObject().Shell(), 
                                                customDlg.CreateLayout(), customDlg )
            else:
                self._panel.SetStatus('No result data, Need to calculate')

        except Exception as e:
            logger.ELOG("Exception: %s " %(str(e)))

    def __PrepareForNewTask(self):
        self.__SetResult(INIT_RESULTS_MSG)
        self._modSinceLastCalc = False
        self._calcInitialized = False
        self.__ResetPaceConsumer()
        
    
    def __PrivateCreateTask(self):
        self._calcInitialized = True
        trdId = self.__CInsdef().OriginalTrade().Oid()
        if self._paceConsumer:
            self._paceConsumer.CreateTask(
                self.__CInsdef().OriginalTrade().Oid())
        else:
            try:
                msgDic = self.__CalcIPFE(trdId)
                self.OnTaskSuccess( msgDic )
            except Exception as e:
                self.OnTaskFail("Error: %s" % str(e))
        
    def __CalcIPFE(self, tradeId):
        trade = acm.FTrade[tradeId]
        msgDic = {}
        if trade: 
            cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            tradeCalc = trade.Calculation()
            result = tradeCalc.IncrementalPFE(cs)
            msg = self.__ParseResult(result.Value())
            msgDic['IncPFE'] = msg
            
            cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext (), 'FPortfolioSheet')
            cbInst = trade.CreditBalance()
            topnode =  cs.InsertItem(cbInst)
            calc = cs.CreateCalculation(topnode, 'Max PFE')
            msg = self.__ParseResult(calc.Value())
            msgDic['PFE'] = msg
            #calc = cs.CreateCalculation(topnode, 'PFE Results')
            #self._currentPFEResult = calc.Value()
            
            
            topnode = cs.InsertItem(trade)
            calc2 = cs.CreateCalculation(topnode, 'PFE and IncrementalPFE')
            msg = self.__ParseResult(calc2.Value())
            msgDic['AfterPFE'] = msg
            
            calc = cs.CreateCalculation(topnode, 'PFE Results')
            self._currentPFEResult = calc.Value()
            
            calc = cs.CreateCalculation(topnode, 'PFE Results With Incremental Trade')
            self._currentAfterPFEResult = calc.Value()
            self.__EnableGraphButton(True)
            
            return msgDic
        else:
             raise Exception("Wrong trade Id.")
    
    def __ParseResult(self, result):
        amount = int(result.Number())
        unit = str(result.Unit())
        msg = "%s %s [%s]" % (amount, unit, acm.Time().TimeNow())
        return msg
    
    def __CInsdef(self):
        return self._panel.Owner()
    
    def __AssertTradeUnmodified(self):
        if self.__CInsdef().ContentIsChanged():
            raise Exception( ERROR_NOT_SAVED )
    
    def __UpdateControls(self):
        try:
            self.__AssertValidTrade()
            self.__EnableCalcButton(True)
        except Exception as e:
            self.__ForceSetStatus( str(e) )
            self.__EnableCalcButton(False)
            if self._paceConsumer:
                self._paceConsumer.ResetPaceConsumer()
    
    def __AssertValidTrade(self):
        trade = self.__CInsdef().OriginalTrade()
        if not trade:
            raise Exception( ERROR_NO_TRADE )
        if not trade.Status() == "Simulated":
            raise Exception( ERROR_NOT_SIMULATED )
        if trade.CreditBalance() == None:
            raise Exception( ERROR_NOT_IN_CREDIT_BALANCE )
        if trade.Instrument().IsKindOf(acm.FCreditBalance):
            raise Exception( ERROR_IS_CREDIT_BALANCE )
    
    def __SetStatus(self, msg):
        if not self.__IsStatusLocked():
            self.__ForceSetStatus(msg)
    
    def __IsStatusLocked(self):
        return self._modSinceLastCalc
    
    def __ForceSetStatus(self, msg):
        self._panel.SetStatus(msg)
    
    def __SetResult(self, msg):
        self._panel.SetResult(msg)
    
    def __EnableCalcButton(self, enabled):
        self._panel.EnableCalcButton(enabled)

    def __EnableGraphButton(self, enabled):
        self._panel.EnableGraphButton(enabled)

    def ServerUpdate(self, sender, aspect, parameter):
        if str(aspect) == 'delete':
            sender.RemoveDependent(self)
        elif self.__ChangedOrUpdated(aspect):
            self.__HandleChanged()
            
        if str(aspect) == 'OnDestroy':
            self.__RemoveAllDependents()
        else:
            self.__UpdateDependents()
        
    def __ChangedOrUpdated(self, aspect):
        return str(aspect) in ('update', 'ContentsChanged') or self.__CInsdef().ContentIsChanged()
    
    def __RemoveAllDependents(self):
        if self._cInsdef: self._cInsdef.RemoveDependent(self)
        if self._editIns: self._editIns.RemoveDependent(self)
        if self._editTrd: self._editTrd.RemoveDependent(self)
    
    def __UpdateDependents(self):
        cInsdef = self.__CInsdef()
        try:
            editIns = self.__CInsdef().EditInstrument()
            editTrd = self.__CInsdef().EditTrade()
        except RuntimeError:
            editIns = None
            editTrd = None
        
        self.__UpdateSingleDependent(self._cInsdef, cInsdef)
        self.__UpdateSingleDependent(self._editIns, editIns)
        self.__UpdateSingleDependent(self._editTrd, editTrd)
        
        self._cInsdef = cInsdef
        self._editIns = editIns
        self._editTrd = editTrd
        
        self.__OnDependentsUpdated()
    
    def __OnDependentsUpdated(self):
        if self._needsReset:
            self.__HandleReset()
    
    def __UpdateSingleDependent(self, old, new):
        if old != new:
            if old: old.RemoveDependent(self)
            if new: new.AddDependent(self)
            self._needsReset = True
    
    def __HandleChanged(self):
        if self._calcInitialized:
            self.__SetStatus( WARNING_TRADE_MODIFIED )
            self._modSinceLastCalc = True
        
    def __HandleReset(self):
        self._needsReset = False
        self._modSinceLastCalc = False
        self._calcInitialized = False
        self.__SetStatus("")
        self.__SetResult(INIT_RESULTS_MSG)
        self.__ResetPaceConsumer()
        self.__UpdateControls()
        self._currentPFEResult = None
        self._currentAfterPFEResult = None
        self.__EnableGraphButton(False)
    
    def __ResetPaceConsumer(self):
        if self._paceConsumer:
            self._paceConsumer.RemovePaceConsumer()

def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    insdefPfeLogic = AAInsdefPfeLogic(eii)
    pfePanel = insdefPfeLogic.Panel()
    basicApp.CreateCustomDockWindow(pfePanel, 'AAInsdefPfePanel', 'Incremental PFE', 'Bottom', False, False)
