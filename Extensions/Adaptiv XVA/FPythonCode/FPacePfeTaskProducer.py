""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/FPacePfeTaskProducer.py"
import acm
import FPaceProducer
import FPacePfeTaskTraits
import AAParamsAndSettingsHelper

logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def CreateProducer():
    logger.LOG('Creating PFE Pace Task Producer')
    return PetProducer()

class PetProducer(FPaceProducer.Producer):

    def __init__(self):         
        super(PetProducer, self).__init__()
                 
    def OnCreateTask(self, taskId, definition):
        try:
            import clr
        except Exception as e:
            self.SendException(taskId, "Import clr failed, %s" % str(e))
        
        try:
            import AAValuation
        except Exception as e:
            self.SendException(taskId, "Import AAValuation failed, %s" % str(e))
   
        resultKey = self.__CreateResultKey()
        result = self.__CreateResult(definition)
        self.SendInsertOrUpdate(taskId, resultKey, result)
    
    def __CreateResultKey(self):
        UNNECESSARY_UPDATE_ID = 1
        resultKey = FPacePfeTaskTraits.ResultKey()
        resultKey.updateId = UNNECESSARY_UPDATE_ID
        return resultKey
    
    def __CreateResult(self, definition):
        result = self.__InitializeNewResult()
        try:
            trade = acm.FTrade[int(definition.trdnbr)]
            result.IncPFE = self.__CalcIncrementalPfe(trade)
            result.PFE, result.AfterPFE = self.__CalcPfeAndAfterPFE(trade)
            result.success = True
        except Exception as e:
            pass
        return result
    
    def __CalcIncrementalPfe(self, trade):
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        tradeCalc = trade.Calculation()
        denomVal =  tradeCalc.IncrementalPFE(cs)
        return self.__GetResultMsg(denomVal)
    
    def __CalcPfeAndAfterPFE(self, trade):
        cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext (), 'FPortfolioSheet')
        cbInst = trade.CreditBalance()
        topnode =  cs.InsertItem(cbInst)
        calc = cs.CreateCalculation(topnode, 'Max PFE')
        pfeMsg = self.__GetResultMsg(calc.Value())
        
        topnode = cs.InsertItem(trade)
        calc2 = cs.CreateCalculation(topnode, 'PFE and IncrementalPFE')
        afterPfeMsg = "%s" %(calc2.Value())
        
        return pfeMsg, afterPfeMsg
        
    def __GetResultMsg(self, denomVal):
        amount = int(denomVal.Number())
        unit = str(denomVal.Unit())
        msg = "%s %s [%s]" % (amount, unit, acm.Time().TimeNow())
        return msg
        
    def __InitializeNewResult(self):
        result = FPacePfeTaskTraits.Result()
        result.success = False
        result.IncPFE = str("", "utf-8")
        result.PFE = str("", "utf-8")
        result.AfterPFE = str("", "utf-8")
        return result
