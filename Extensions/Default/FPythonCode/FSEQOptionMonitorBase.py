""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQOptionMonitorBase.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQOptionMonitorBase - Holds the class OptionCollectionUpdateHandler used
    by modules FSEQBarrierMonitorPrice, FSEQLadderMonitorPrice and 
    FSEQLookbackMonitorPrice.

    (c) Copyright 2007 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    OptionCollectionUpdateHandler: Takes as argument an "optionStrategy"-object
    that implements the methods:
        needToCheck(instrument):bool
        checkOption(instrumentId, evaluator):void
        createEvaluator(instrument, context, ebTag):FEvaluator

----------------------------------------------------------------------------"""
import acm
import ael

debug = False

"""---------------------------------------------------------------
OptionCollectionUpdateHandler
    Monitors changes in exotic options and their underlyings prices.
---------------------------------------------------------------"""
class OptionCollectionUpdateHandler:
    global_instance = None
    
    def __init__(self, optionStrategy):
        self.optionStrategy = optionStrategy
        self.optionUpdateHandler = OptionUpdateHandler(optionStrategy)
        
        self.tableUpdates = []
        
        self.initializeInstrumentCollections()

    def initializeInstrumentCollections(self):
        self.exotic_options = acm.FOption.Select("exoticType=Other")
        self.exotic_warrants = acm.FWarrant.Select("exoticType=Other")

        self.exotic_options.AddDependent(self)
        self.exotic_warrants.AddDependent(self)
        
        for instrument in list(self.exotic_options) + list(self.exotic_warrants):
            if self.needToCheck(instrument):
                self.addOption(instrument.Oid())
       
        self.optionUpdateHandler.checkAllOptions()

    def get_instance(optionStrategy = None):
        if not OptionCollectionUpdateHandler.global_instance:
            if not optionStrategy:
                return None
            OptionCollectionUpdateHandler.global_instance = OptionCollectionUpdateHandler(optionStrategy)
        return OptionCollectionUpdateHandler.global_instance
    get_instance = staticmethod(get_instance)

    def clearAllInstruments(self):
        self.unsubscribe()
        self.optionUpdateHandler.clearAllInstruments()
        self.optionStrategy.clearCalculationSpace()

    def reinitializeInstrumentCollection(self):
        self.processUpdates()
        self.clearAllInstruments()
        self.initializeInstrumentCollections()
        
    def addOption(self, instrumentId):
        instrument = acm.FInstrument[instrumentId]
        if not instrument:
            ael.log('OptionCollectionUpdateHandler.addOption - instrument not found, instrumentId: %i'%instrumentId)
            return False
        return self.optionUpdateHandler.addInstrument(instrumentId)
        
    def removeOption(self, instrumentId):
        instrument = acm.FInstrument[instrumentId]
        
        if not instrument:
            ael.log('OptionCollectionUpdateHandler.removeOption - Unknown instrumentId: %i'%instrumentId)
        
        return self.optionUpdateHandler.removeInstrument(instrumentId)
        
    def updateOption(self, instrumentId):
        instrument = acm.FInstrument[instrumentId]
        if not instrument:
            self.removeOption(instrumentId)
            return False
        else:
            if self.needToCheck(instrument):
                self.reinitializeInstrumentCollection()
                self.addOption(instrumentId)
                return True
            return False
        
    def ServerUpdate(self, sender, aspect, instrument):

        if not sender.Class() == acm.FPersistentSet or not instrument.IsKindOf(acm.FInstrument):
            return
        self.tableUpdates.append([str(aspect), instrument.Oid()])
        return

    def needToCheck(self, instrument):
        return self.optionStrategy.needToCheck(instrument)

    def processUpdates(self):
        while self.tableUpdates != []:
            (action, instrumentId) = self.tableUpdates.pop(0)
            doCheckInstrument = False
            if action == 'insert':
                instrument = acm.FInstrument[instrumentId]
                if self.needToCheck(instrument):
                    doCheckInstrument = self.addOption(instrumentId)
            elif action == 'remove':
                self.removeOption(instrumentId)
            elif action == 'update':
                doCheckInstrument = self.updateOption(instrumentId)
            else:
                ael.log('OptionCollectionUpdateHandler.processUpdates - received unknown action identifier')
            if doCheckInstrument:
                self.optionUpdateHandler.checkOption(instrumentId)
        self.optionUpdateHandler.processUpdates()
    
    def unsubscribe(self):
        self.exotic_options.RemoveDependent(self)
        self.exotic_warrants.RemoveDependent(self)
        
        self.optionUpdateHandler.unsubscribe()
        
    def clearInstance(self):
        OptionCollectionUpdateHandler.global_instance = None
        
class OptionUpdateHandler:
    global_instance = None

    def __init__(self, optionStrategy):
        self.optionStrategy = optionStrategy
        self.default_ctx = acm.GetDefaultContext()
        self.tag = acm.CreateEBTag()
        
        self.instrWrapperDict = {}
        
    def addInstrument(self, instrumentId):
        if not self.instrWrapperDict.get(instrumentId, None):
            instrument = acm.FInstrument[instrumentId]
            if not instrument:
                return False
            instrWrapper = InstrumentWrapper(instrument, self.default_ctx, self.tag, self.optionStrategy)
            if instrWrapper.Evaluator:
                self.instrWrapperDict[instrumentId] = instrWrapper
                return True
        return False
        
    def removeInstrument(self, instrumentId):
        instrWrapper = self.instrWrapperDict.get(instrumentId, None)
        if not instrWrapper:
            return False
        instrWrapper.unsubscribe()
        del self.instrWrapperDict[instrumentId]
        
        return True

    def processUpdates(self):
        for instrWrapper in list(self.instrWrapperDict.values()):
            self.checkInstrImpl(instrWrapper)

    def checkOption(self, instrumentId):
        instrWrapper = self.instrWrapperDict.get(instrumentId, None)
        if instrWrapper:
            instrWrapper.checkUpdate()
            self.checkInstrImpl(instrWrapper)

    def checkAllOptions(self):
        for instrWrapper in list(self.instrWrapperDict.values()):
            instrWrapper.checkUpdate()
            self.checkInstrImpl(instrWrapper)

    def checkInstrImpl(self, instrWrapper):
        if instrWrapper.finished:
            self.removeInstrument(instrWrapper.Id)
            
    def clearAllInstruments(self):
        for instrWrapper in list(self.instrWrapperDict.values()):
            self.removeInstrument(instrWrapper.Id)
            
    def unsubscribe(self):
        for instrWrapper in list(self.instrWrapperDict.values()):
            instrWrapper.unsubscribe()
        
class InstrumentWrapper:
    def __init__(self, instrument, context, ebTag, optionStrategy):
        self.instrumentId = instrument.Oid()
        self.optionStrategy = optionStrategy
        self.evaluator = None
        self.finished = False
        
        self.evaluator = optionStrategy.createEvaluator(instrument, context, ebTag)
        if optionStrategy.ListenToPriceUpdates:
            self.evaluator.AddDependent(self)
    
    def __getattr__(self, attrname):
        if attrname == "Evaluator":
            return self.evaluator
        elif attrname == "Id":
            return self.instrumentId
        else:
            raise AttributeError(attrname)
            
    def ServerUpdate(self, sender, aspect, param):
        if not (sender.IsKindOf(acm.FEvaluator) or sender.IsKindOf(acm.FCalculation)):
            return
        self.checkUpdate()
        return

    def checkUpdate(self):
        if self.optionStrategy.checkOption(self.instrumentId, self.evaluator):
            self.finished = True
        return

    def unsubscribe(self):
        self.evaluator.RemoveDependent(self)
        return
