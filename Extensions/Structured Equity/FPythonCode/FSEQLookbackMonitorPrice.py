""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQLookbackMonitorPrice.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQLookbackMonitorPrice - Update lookback extreme value.

    (c) Copyright 2006 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
        The module monitors underlying prices of lookback options. If a price
        generates a new maximum / minimum value, the extreme value of the lookback
        option is updated.        
----------------------------------------------------------------------------"""
import acm
import ael
from FSEQOptionMonitorBase import OptionCollectionUpdateHandler

debug = False

dateDifference = acm.GetFunction('dateDifference', 2)

"""----------------------------------------------------------------------------
LookbackStrategy
    Implements the "optionStrategy"-interface used by Module FSEQOptionMonitorBase.
----------------------------------------------------------------------------"""
class LookbackStrategy:
    global debug

    def __init__(self):
        self.calcSpaceCollection = acm.FCalculationSpaceCollection()
        self.createNewCalculationSpace()
        
    def __getattr__(self, attrname):
        if attrname == "ListenToPriceUpdates":
            return True
        else:
            raise AttributeError(attrname)    
    
    def createNewCalculationSpace(self):
        context = acm.GetDefaultContext()
        self.calculationSpace = self.calcSpaceCollection.GetSpace("FDealSheet", context)

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
            priceDV = calcObject.Value()
            price = priceDV.Number()
        
            exotic = lookback.Exotic()
            if not exotic:
                ael.log('LookbackStrategy.checkOption - instrument.exotic() returned None: %s'%lookback.Name())
                return True
            
            # Check for forward start dates beyond today.
            if exotic.ForwardStartType() != "None" \
                and dateDifference(exotic.ForwardStartDate(), ael.date_today()) > 0:
                return False
            
            current_extreme = exotic.LookbackExtremeValue()
            lookback_type = exotic.LookbackOptionType()
            is_call = lookback.IsCallOption()
            
            update = False
            if (lookback_type == "Price" and is_call) or \
               (lookback_type == "Strike" and not is_call):
                if price > current_extreme: update = True
            else:
                if price < current_extreme: update = True
                
            if update:    
                try: 
                    exotic.LookbackExtremeValue = price
                    exotic.Commit()
                    ael.log("The extreme value for %s has been updated to %f"%(lookback.Name(), price))                
                except RuntimeError:
                    ael.log("The instrument has already been updated: %s"%lookback.Name())
        except Exception as e:
            ael.log("Exception caught when checking lookback %s: %s"%(lookback.Name(), str(e)))
        return False
        
    def createEvaluator(self, lookbackOption, context, ebTag):
        calcObject = self.calculationSpace.CreateCalculation(lookbackOption, "Standard Calculations Underlying Price")
        return calcObject


"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    ael.log('FSEQLookbackMonitorPrice started')
    updateHandler = OptionCollectionUpdateHandler.get_instance(LookbackStrategy())
    
def stop():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    if updateHandler:
        updateHandler.unsubscribe()
        updateHandler.clearInstance()
    ael.log('FSEQLookbackMonitorPrice stopped')
    
def status():
    pass
    
def work():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    updateHandler.processUpdates()