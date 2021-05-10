""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQLookbackMonitorPriceHiLo.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQLookbackMonitorPriceHiLo - Updates lookback extreme values.

    (c) Copyright 2007 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
        The module monitors underlying prices of lookback options. If a price
        generates a new maximum / minimum value, the extreme value of the lookback
        option is updated.        
----------------------------------------------------------------------------"""
import acm
import ael
import datetime

from FSEQOptionMonitorBase import OptionCollectionUpdateHandler

updateInterval = 3
dateDifference = acm.GetFunction('dateDifference', 2)

silent = True

"""----------------------------------------------------------------------------
LookbackStrategy
    Implements the "optionStrategy"-interface used by Module FSEQOptionMonitorBase.
----------------------------------------------------------------------------"""
class LookbackStrategy:
    def __init__(self):
        self.lastUpdateDateTime = datetime.datetime.now()
        self.calcSpaceCollection = acm.FCalculationSpaceCollection()
        self.createNewCalculationSpace()
        
    def __getattr__(self, attrname):
        if attrname == "ListenToPriceUpdates":
            return False
        else:
            raise AttributeError(attrname)    
    
    def createNewCalculationSpace(self):
        context = acm.GetDefaultContext()
        self.calculationSpace = self.calcSpaceCollection.GetSpace("FOrderBookSheet", context)

    def clearCalculationSpace(self):
        self.calcSpaceCollection.Clear()
        self.createNewCalculationSpace()
        
    def needToCheck(self, instrument):
    
       if instrument.IsClone():
           return False
           
       isExpired = instrument.IsExpired()
       isLookback = instrument.IsLookback()
       
       if isExpired or not isLookback:
           return False
       
       try:
           exotic = instrument.Exotic()
       except:
           ael.log('OptionCollectionUpdateHandler.needToCheck - instrument.Exotic() failed for instrument: %s'%instrument.Name())
           return False
       
       if exotic.LookbackDiscreteMonitoring() or exotic.BarrierOptionType() == "Custom":
           return False
       
       return True
       
    def checkOption(self, instrumentId, calcObject):
        lookback = acm.FInstrument[instrumentId]
        
        try:
            exotic = lookback.Exotic()
            if not exotic:
                ael.log('LookbackStrategy.checkOption - instrument.exotic() returned None: %s'%lookback.Name())
                return True
            
            # Check for forward start dates beyond today.
            if exotic.ForwardStartType() != "None" \
                and dateDifference(exotic.ForwardStartDate(), ael.date_today()) > 0:
                return False
            
            underlying = lookback.Underlying()
            strikeCurr = lookback.StrikeCurrency()
            self.calculationSpace.SimulateValue(underlying, "Standard Calculations ADS Price Currency", strikeCurr)
            
            priceFeed = calcObject.Value()
            if not priceFeed:
                return False

            current_extreme = exotic.LookbackExtremeValue()
            lookback_type = exotic.LookbackOptionType()
            is_call = lookback.IsCallOption()
            
            update = False
            newExtreme = 0.0
            
            highPrice = priceFeed.HighPrice().Value().Number()
            lowPrice = priceFeed.LowPrice().Value().Number()
            
            if (lookback_type == "Price" and is_call) or \
               (lookback_type == "Strike" and not is_call):
                if highPrice > current_extreme: 
                    update = True
                    newExtreme = highPrice
            else:
                if lowPrice < current_extreme:
                    update = True
                    newExtreme = lowPrice
            if update:
                try: 
                    exotic.LookbackExtremeValue = newExtreme
                    exotic.Commit()
                    ael.log("The extreme value for %s has been updated to %f"%(lookback.Name(), newExtreme))                
                except RuntimeError:
                    ael.log("Could not update lookback: %s"%lookback.Name())
        except RuntimeError as e:
            ael.log("Exception caught when checking lookback %s: %s"%(lookback.Name(), str(e)))
        return False
        
    def createEvaluator(self, lookbackOption, context, ebTag):
        underlying = lookbackOption.Underlying()
        calcObject = self.calculationSpace.CreateCalculation(underlying, "Standard Calculations ADS Price Feed")
        return calcObject
        

"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    ael.log('FSEQLookbackMonitorPriceHiLo started')
    updateHandler = OptionCollectionUpdateHandler.get_instance(LookbackStrategy())
    
def stop():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    if updateHandler:
        updateHandler.unsubscribe()
        updateHandler.clearInstance()
    ael.log('FSEQLookbackMonitorPriceHiLo stopped')    
    
def status():
    pass
    
def work():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    optionStrategy = updateHandler.optionStrategy

    datetimeNow = datetime.datetime.now()
    timeDiff = datetimeNow - optionStrategy.lastUpdateDateTime
    
    if timeDiff.seconds > updateInterval:
        optionStrategy.lastUpdateTime = datetime.datetime.now()
        updateHandler.processUpdates()
        updateHandler.optionUpdateHandler.checkAllOptions()