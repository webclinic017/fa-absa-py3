
import acm

import FPaceProducer

from math import isnan
import time
from collections import namedtuple

CalcAndUpdater = namedtuple("InstrumentCalculationAndUpdater", ["calculations", "updater"])
LiveCalcs = namedtuple("LiveSpanCalculations", ["riskArray", "delta"])
            
class CalculationsUpdater(object):
    def __init__(self, oidToUpdate, updater):
        self._oidToUpdate = oidToUpdate
        self.updater = updater
    
    def ServerUpdate(self, sender, aspect, param):
        self.updater(self._oidToUpdate)
            
class InstrumentRemover(object):
    def __init__(self, remover):
        self.remover = remover
    
    def ServerUpdate(self, sender, aspect, param):
        updateType = str(aspect)
        if self.remover is not None and updateType == "delete":
            self.remover(param)

def CreateProducer():
    acm.Log("Creating PACE Producer for Live SPAN parameters.")
    import FSpanLiveParamsTraits as TraitsModule
    return SpanLiveParamsProducer(TraitsModule)
        

def createCalculation(oid, column_id, calculationSpace):
    ins = acm.FInstrument[oid]
    if ins is None:
        raise RuntimeError("No instrument found for oid {0}".format(oid))
    calculation = calculationSpace.CreateCalculation(ins, column_id)
    return calculation

def classifyOidsAndCreateCalculations(oids, alreadyHandledOids, riskArrayCalculationColumnId, spanDeltaCalculationColumnId, calculationSpace):
    oids = oids.difference(alreadyHandledOids)
    badOidsWithExplanationStr = {}
    good_oids_with_calcs = {}
    for oid in oids:
        try:
            riskArrayCalc = createCalculation(oid, riskArrayCalculationColumnId, calculationSpace)
            spanDeltaCalc = createCalculation(oid, spanDeltaCalculationColumnId, calculationSpace)
            calcs = LiveCalcs(riskArrayCalc, spanDeltaCalc)
        except Exception as e:
            badOidsWithExplanationStr[oid] = str(e)
        else:
            good_oids_with_calcs[oid] = calcs
            
    return (good_oids_with_calcs, badOidsWithExplanationStr)


def oidsSetForStoredQuery(storedQuery):
    rv = set()
    
    selection = storedQuery.Query().Select()
    hasLoggedQueryContainsNonInstrument = False
    for element in selection:
        if element.IsKindOf(acm.FInstrument):
            rv.add(element.Oid())
        elif not hasLoggedQueryContainsNonInstrument:
            errorMsg = ("Stored Query {0}".format(storedQuery.Name()) +
                " defining instruments for Span Live Parameters" +
                " selects items which are not instruments.")
            acm.Log(errorMsg)
            hasLoggedQueryContainsNonInstrument = True
    return rv
           

def oidsFromStoredQueryOid(oid, taskId):
    insOids = set()
    storedQuery = acm.FStoredASQLQuery[oid]
    if storedQuery is not None:
        insOids = oidsSetForStoredQuery(storedQuery)        
        query_log_str = "Producing risk arrays for taskId {0} for {1} instruments found for query name {2}.".format(
            str(taskId), len(insOids), storedQuery.Name())
        acm.Log(query_log_str)
    else:
        acm.Log("No FStoredASQLQuery found for oid {0} for taskId {1}.".format(oid, taskId))
        
    return insOids

class SpanLiveParamsProducer(FPaceProducer.Producer):
    def __init__(self, traits_module):
        super(SpanLiveParamsProducer, self).__init__()
        self.traits_module = traits_module
        self._calculationSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
        self._instrumentUpdater = InstrumentRemover(self.InstrumentRemoveHandler)
        self._calculatioAndUpdaterCache = {}
        self._oidsPerTask = {}
        self._calcsToEvaluate = set()
        self._isWorking = False
        self.maxCalcErrorsToLog = 1000
        self.numCalcErrorsLogged = 0
    
    def OnCreateTask(self, taskId, definition):
        queryOid = int(definition.query_oid)
        log_str = "SpanLiveParamsProducer.OnCreateTask for taskId %s and query oid %s." % (str(taskId), str(queryOid))
        acm.Log(log_str)

        insOids = oidsFromStoredQueryOid(queryOid, taskId)
    
        # no viewkeys in 2.6
        cached_oids = set(self._calculatioAndUpdaterCache.keys())  

        riskArrayColumnId = "SPAN Risk Array"
        spanDeltaColumnId = "SPAN Live Delta" 
        (good_oids_with_calcs, badOidsWithExplanationStr) =\
            classifyOidsAndCreateCalculations(insOids, cached_oids, 
                    riskArrayColumnId, spanDeltaColumnId, self._calculationSpace)
        
        for (oid, calc) in good_oids_with_calcs.items():
            updater = CalculationsUpdater(oid, self.CalculationUpdateHandler)
            calc.riskArray.AddDependent(updater)
            calc.delta.AddDependent(updater)
            self._calculatioAndUpdaterCache[oid] = CalcAndUpdater(calc, updater)

        for (oid, reason) in badOidsWithExplanationStr.items():
            log_msg = "Unabled to create risk array calculation for column {0} with oid {1} for task {2} due to {3}.".format(
                   column_id, oid, taskId, reason)
            acm.Log(log_msg)
         
        bad_oids = set(badOidsWithExplanationStr.keys())
        self._oidsPerTask[taskId] = insOids.difference(bad_oids)
        for insOid in self._oidsPerTask[taskId]:
            self.CalculateAndSendResult(taskId, insOid)
        self.SendInitialPopulateDone(taskId)

    def CalculateAndSendResult(self, taskId, insOid):
        try:
            dvRiskArray = self._calculatioAndUpdaterCache[insOid].calculations.riskArray.Value()
            floatRiskArray = [dv.Number() for dv in dvRiskArray]
            if any(isnan(element) for element in floatRiskArray):
                raise RuntimeError("At least one element of risk array is unexpectedly NaN for instrument {0}".format(insOid))
            delta = self._calculatioAndUpdaterCache[insOid].calculations.delta.Value().Number()
            if isnan(delta):
                raise RuntimeError("Span delta is unexpectedly NaN for instrument {0}".format(insOid))
            self.CreateAndSendResult(taskId, insOid, floatRiskArray, delta)
        except Exception as e:
            if not self.HasLoggedMaxCalcErrors():
                self.numCalcErrorsLogged += 1
                msg = ("SpanLiveParamsProducer: Calculation Error:" +
                       " Risk arrays and Delta are not being updated for instrument" +
                       " {0} for task {1} due to exception: {2}.".format(insOid, taskId, e))
                acm.Log(msg)
                if self.HasLoggedMaxCalcErrors():
                    msg = ("SpanLiveParamsProducer: No more Calculation Errors will" +
                           " be logged since the logging maximum of" +
                           " {0} was reached.".format(self.maxCalcErrorsToLog))
                    acm.Log(msg)
                    
    def HasLoggedMaxCalcErrors(self):
        return self.numCalcErrorsLogged >= self.maxCalcErrorsToLog

    def CreateAndSendResult(self, taskId, insOid, riskArray, delta):
        resultKey = self.traits_module.ResultKey()
        result = self.traits_module.Result()
        resultKey.ins_oid = insOid
        result.riskarray.extend(riskArray)
        result.delta = delta
        self.SendInsertOrUpdate(taskId, resultKey, result)
    
    def CalculationUpdateHandler(self, update_oid):
        self._calcsToEvaluate.add(update_oid)
            
    def InstrumentRemoveHandler(self, instrument):
        insOid = instrument.Oid()
        calc_and_updater = self._calculatioAndUpdaterCache.pop(insOid, None)
        if calc_and_updater is not None:
            for calc in calc_and_updater.calculations:
                calc.RemoveDependent(calc_and_updater.updater)
        instrument.RemoveDependent(self._instrumentUpdater)

    def OnDoPeriodicWork(self):
        # protect for reentrancy    
        if not self._isWorking:
            self._isWorking = True
    
            for (taskId, oids) in self._oidsPerTask.items():
                oids_to_update = oids.intersection(self._calcsToEvaluate)              
                for oid in oids_to_update:
                    self.CalculateAndSendResult(taskId, oid)
            self._calcsToEvaluate.clear()

            self._isWorking = False
