""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQLadderMonitorPrice.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQLadderMonitorPrice - Update ladder rung dates if ladder rung is reached.

    (c) Copyright 2005 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
        The module monitors underlying prices of ladder options. If a price
        has crossed a ladder rung, the corresponding ladder rung date is 
        updated to the crossing date.        
----------------------------------------------------------------------------"""
import acm
import ael
from FSEQOptionMonitorBase import OptionCollectionUpdateHandler


"""----------------------------------------------------------------------------
update_rungs() 
   Check for crossed Rung events and update if necessary.
----------------------------------------------------------------------------"""    
def update_rungs(i, price=0.0):
    exotic = i.Exotic()
    if not exotic:
        return False
        
    is_discrete = exotic.LadderDiscreteMonitoring()

    rungs = []
    for e in i.ExoticEvents():
        if e.Type() == 'Ladder rung' and e.Date() == i.ExpiryDateOnly():
            rungs.append([e.EventValue(), e.RunNo(), e.StorageId(), e])

    if rungs != []:
        if i.IsCallOption():
            rungs = [[(x[0] - price), x[0], x[1], x[2], x[3]] for x in rungs]
            
        else:
            rungs = [[(price - x[0]), x[0], x[1], x[2], x[3]] for x in rungs]

        if not is_discrete:
            try:
                for [res, rung_value, run_no, seqnbr, exotic] in rungs:
                    if res <= 0:
                        exotic_clone = exotic.Clone()
                        exotic_clone.Date(str(ael.date_valueday()))
                        exotic.Apply(exotic_clone)
                        exotic.Commit()
                        ael.log('%s: The spot price has crossed a ladder rung: %s'%(i.Name(), str(rung_value)))
            except Exception as e:
                ael.log('Failed to update rung status for instrument: %s'%str(e))
    
    isFinished = True
    for e in i.ExoticEvents():
        if e.Date() == i.ExpiryDateOnly():
            isFinished = False
            
    return isFinished

"""----------------------------------------------------------------------------
LadderStrategy
    Implements the "optionStrategy"-interface used by Module FSEQOptionMonitorBase.
----------------------------------------------------------------------------"""
class LadderStrategy:

    def __getattr__(self, attrname):
        if attrname == "ListenToPriceUpdates":
            return True
        else:
            raise AttributeError(attrname)

    def clearCalculationSpace(self):
        pass

    def needToCheck(self, ladder):
        if not ladder.IsLadder():
            return False

        exotic = ladder.Exotic()
        if not exotic:
            ael.log('ladderStrategy.needToCheck - instrument.Exotic() returned None: %s'%ladder.Name())
            return False
        
        is_discrete = exotic.LadderDiscreteMonitoring()
        is_expired = ladder.IsExpired()
        
        if not (is_discrete or is_expired) \
            and not exotic.BarrierOptionType() == "Custom":
            return True
        else:
            return False
    
    def checkOption(self, instrumentId, evaluator):
        ladder = acm.FInstrument[instrumentId]
        try:
            priceDV = evaluator.Value()
            price = priceDV.Number()            

            return update_rungs(ladder, price)
        except Exception as e:
            ael.log('ladderStrategy.checkOption failed - Instrument: %s, %s'%(ladder.Name(), str(e)))
            return False

    def createEvaluator(self, ladderOption, context, ebTag):
        underlyingInstrument = ladderOption.Underlying()
        evaluator = acm.GetCalculatedValueFromString(underlyingInstrument,
                                         context,
                                         'object:*"marketPriceADSLast"[priceSource:="ADS", doSplitAll]',
                                         ebTag)
        return evaluator


"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    ael.log('FSEQLadderMonitorPrice started')
    updateHandler = OptionCollectionUpdateHandler.get_instance(LadderStrategy())
    
def stop():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    if updateHandler:
        updateHandler.unsubscribe()
        updateHandler.clearInstance()
    ael.log('FSEQLadderMonitorPrice stopped')    
    
def status():
    pass
    
def work():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    updateHandler.processUpdates()

