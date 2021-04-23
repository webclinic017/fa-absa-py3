

import ael, acm
import FBDPGui
reload(FBDPGui)

from FBDPCommon import Summary
import FBDPString
logme = FBDPString.logme
from at_addInfo import get
from at_time import acm_date

space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
today = acm.Time().DateNow()

FX_SPOT_BASE_INSTRUMENT = acm.FCurrencyPair['USD/ZAR']
FX_SPOT_BASE_MARKET     = acm.FParty['WMR LDN 16:00PM']

class StandardFixing:

    def __init__(self, exoticEvent, testmode):
        self.exoticEvent = exoticEvent
        self.ok = 0
        self.fxRate = self.calculateFxRate()
        self.testmode = testmode
        if self.ok:
            self.save()

    def getMappedCurve(self, curr):
    
        try:
            curve = curr.MappedRepoLink().Link().YieldCurveComponent()
            mappedCurve = None
            mappedCurveInformation = None
            if curve.IsKindOf(acm.FYCAttribute):
               mappedCurve = curve.Curve()
               mappedCurveInformation = curve.IrCurveInformation(curr.MappedRepoLink().Link().YieldCurveComponent().UnderlyingCurve().IrCurveInformation(), ael.date_today())
            if curve.IsKindOf(acm.FBenchmarkCurve):
                mappedCurve = curve 
                mappedCurveInformation = curve.IrCurveInformation()
        except:
            return [None, None]
        return [mappedCurve, mappedCurveInformation] 


    def getFxRate(self, date, curr1, curr2):
        
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        if acm.Time().DateDifference(date, acm.Time().DateToday()) < 0:
            date = acm.Time().DateToday()
        return curr1.Calculation().FXRate(space, curr2, date).Value().Number()
        

    def calculateFxRate(self):
        if self.exoticEvent:
            #logme('debug logging', 'DEBUG')
            try:
                exoticEvent     = self.exoticEvent
                inst            = exoticEvent.Instrument()
                spotDate        = ael.date_today()
                exoticEventDate = exoticEvent.Date()
                instCurr        = inst.Currency()
                #fxSpotBase      = acm.FInstrument[FX_SPOT_BASE_INSTRUMENT]
                market          = FX_SPOT_BASE_MARKET
                fixingValue     = None
                undInstCurr     = None
                todayIsfixed    = False
                
                fixing_currency = get(inst, 'Fixing_Currency')
                fixing_source = get(inst, 'Fixing_Source')
                
                if fixing_currency:
                    fixing_currency = acm.FCurrencyPair[fixing_currency.FieldValue()]
                if fixing_currency:
                    currency1 = fixing_currency.Currency1()
                    currency2 = fixing_currency.Currency2()
                else:
                    fixing_currency = FX_SPOT_BASE_INSTRUMENT
                    currency1 = fixing_currency.Currency1()
                    currency2 = fixing_currency.Currency2()
                
                if fixing_source:
                    fixing_source = acm.FParty[fixing_source.FieldValue()]
                if not fixing_source:
                    fixing_source = FX_SPOT_BASE_MARKET
                
                """
                if not fxSpotBase:
                    Summary().fail(self.exoticEvent, Summary().action,"%s not defined" % FX_SPOT_BASE_INSTRUMENT, exoticEvent.Oid())
                    return
                """
     
                if not fixing_source:
                    Summary().fail(self.exoticEvent, Summary().action, "%s not defined" % fixing_source, exoticEvent.Oid())
                    return
              
                for l in inst.Legs():
                    if l.FloatRateReference():
                        undInstCurr = l.FloatRateReference().Currency()

                if not undInstCurr:
                    Summary().fail(self.exoticEvent, Summary().action, "Underlying float instrument not found for %s" % inst.Name(), exoticEvent.Oid())
                    return
                
                if instCurr.Name() != 'ZAR':
                    Summary().fail(self.exoticEvent, Summary().action, "%s Instument currency is not ZAR" % inst.Name(), exoticEvent.Oid())
                    return

                if undInstCurr.Name() != 'USD':
                    Summary().fail(self.exoticEvent, Summary().action, "%s Underlying instrument currency is not USD" % inst.Name(), exoticEvent.Oid())
                    return
                
                
                if  acm.Time().DateToday() > exoticEventDate:
                    p = acm.FPrice.Select01("instrument='%s' day='%s' currency='%s' market='%s'" % ( currency1.Name(), exoticEventDate, currency2.Name(), fixing_source.Name()), '')
                elif fixing_source.Type() == 'MtM Market':
                    p = acm.FPrice.Select01("instrument='%s' day='%s' currency='%s' market='%s'" % ( currency1.Name(), exoticEventDate, currency2.Name(), fixing_source.Name()), '')
                else: 
                    p = acm.FPrice.Select01("instrument='%s' currency='%s' market='%s'" % ( currency1.Name(), currency2.Name(), fixing_source.Name()), '')
                    
                if not p:
                    p = acm.FPrice.Select01("instrument='%s' day='%s' currency='%s' market='%s'" % ( currency1.Name(), acm_date('%s-1d'%exoticEventDate), currency2.Name(), fixing_source.Name()), '')
                    
                if not p:
                    Summary().fail(self.exoticEvent, Summary().action, "Cannot get fixing value of %s for date %s" % (FX_SPOT_BASE_INSTRUMENT.Name(), exoticEventDate), exoticEvent.Oid())
                    return
                else:
                    fixingValue = p.Settle()
              
                if ael.date(exoticEventDate) < ael.date(today):
                    logme("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    logme("Instrument %s Exotic Event %s fixing for date %s" % (inst.Name(), exoticEvent.Oid(), exoticEventDate))
                    logme("Reading historical fx rate from %s and market %s at date %s" % (fixing_currency.Name(), fixing_source.Name(), exoticEventDate))
                    logme("Fixing value: %s" % fixingValue)                
                else:
                    logme("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    logme("Instrument %s Exotic Event %s fixing for date %s" % (inst.Name(), exoticEvent.Oid(), exoticEventDate))
                    logme("Fixing with fx rate from %s and market %s at date %s" % (fixing_currency.Name(), fixing_source.Name(), exoticEventDate))
                    logme("Fixing value: %s" % fixingValue)
              

                self.ok = 1
                return fixingValue
            except:
                raise
                Summary().fail(self.exoticEvent, Summary().action, "Calculating fx rate for instrument %s and Date %s" % (inst.Name(), exoticEventDate), exoticEvent.Oid())
              
            #logme('Get Rate Reset value %f [%s]' % (self.reset.FixingValue(), self.ins.Name()))  
        else:  
            logme('No rate found from interpolation hook %s' %(self.reset.Oid()), 'DEBUG')
            Summary().ignore(self.reset, Summary().action, 'No rate found from hook', exoticEvent.Oid())
        
    def save(self):
    
        e_clone = self.exoticEvent.Clone()
        if not self.testmode:
            e_clone.EventValue(self.fxRate)
            self.exoticEvent.Apply(e_clone)
            self.exoticEvent.Commit()
        logme('Saved exotic event value %f [%s]' % (e_clone.EventValue(), e_clone.Instrument().Name()))
        Summary().ok(self.exoticEvent, Summary().CREATE)

def fixExoticEvents(args):

    exoticEventsDict = {}
    exoticEvents = args['exoticEvents']
    for ev in exoticEvents:
        if exoticEventsDict.has_key(ev.Instrument().Name()):
            exoticEventsDict[ev.Instrument().Name()].Add(ev)
        else:
            exoticEventsDict[ev.Instrument().Name()] = acm.FArray()
            exoticEventsDict[ev.Instrument().Name()].Add(ev)

    for i in exoticEventsDict.keys():
        exoticEvents = exoticEventsDict[i].SortByProperty('Date', True)
        for exoticEvent in exoticEvents:
            insName = exoticEvent.Instrument().Name()
            exoticEvent = acm.FExoticEvent[exoticEvent.Oid()]
            if not exoticEvent:
                continue
            
            if exoticEvent.Instrument().InsType() != 'PriceSwap':
                Summary().ignore(exoticEvent, Summary().action, 'Instrument %s is not of type PriceSwap' % insName, exoticEvent.Oid())
                continue
                
            if exoticEvent.Type() != 'Fx Rate':
                Summary().ignore(exoticEvent, Summary().action, 'Exotic Event on instrument %s is not of type Fx Rate' % insName, exoticEvent.Oid())
                continue
            StandardFixing(exoticEvent, args['testmode'])
      
    Summary().log(args)

