""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FFixPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FFixPerform - Module which executes fixing.

DESCRIPTION
    This module executes the fixing procedure based on the
    parameters passed from the script FFixing.


----------------------------------------------------------------------------"""
#Import builtin modules
import time
import FBDPString

#Import Front modules
import acm
import ael

space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

logme = FBDPString.logme
from FBDPCommon import SummaryLocal
hook = False
try:
    from FBDPHook import calculate_fixing
except ImportError:
    pass
else:
    hook = calculate_fixing

fixingCategorization = False
try:
    from CustomCategorizationHelper import FixingCategorization
    fixingCategorization = True
except ImportError:
    pass

spread_hook = False
w = None
try:
    from FSpreadHook import calculate_spread 
    from FSpreadHook import Wrapper
except ImportError:
    pass
else:
    spread_hook = calculate_spread
    w = Wrapper( None )

interpol_hook = False
try:
    from FFixingEstimate import interpol_fixing
except ImportError:
    pass
else:
    interpol_hook = interpol_fixing

def IsOpenEnded( instr ):
    if instr.OpenEnd() == "Open End":
        return True
    return False

def IsCallFloatNotOverNight(instr):
    legs = instr.Legs()
    
    for leg in legs:
        if (leg.LegType() == "Call Float" and leg.ResetPeriod() != '1d'):
            return True
    return False


def extend_open_end( inst, summary ):
    logme('Extending open ended...')
    if not len(inst):
        inst = acm.FInstrument.Select('openEnd = "Open End"')

    for i in inst:
        if not IsOpenEnded(i):
            ael.log('Extend open end: Instrument %s not extended, Open End status %s'%(i.Name(), i.OpenEnd()))
            continue

        if IsCallFloatNotOverNight(i):
            ael.log('Extend open end: Instrument %s not extended, Call Float and reset period != 1 day not supported.'%i.Name())
            continue

        try:
            i.ExtendOpenEnd()
        except RuntimeError as msg:
            summary.fail_update(i, msg, i.Name())
            continue
        summary.ok_update(i)

def fix(args):
    summary = SummaryLocal()

    if hook:
        logme('Calculate_fixing hook enabled!')
    if spread_hook:
        logme('calculate_spread hook enabled!')
    if interpol_hook:
        logme('interpol_hook enabled!')
    
    getOpManFixingRates = args['GetOpManFixingRates_DoNotCommit']
    backdateResets = args['backdateResets']


    for r in args['resets']:
        if getOpManFixingRates:
            # Use the OpMan Reset Clone - Do Not Commit
            reset = r    
        else: 
            reset = acm.FReset[r.Oid()]
            
        if not reset:
            continue
        cashFlow = reset.CashFlow()
        if not cashFlow:
            continue
        leg = cashFlow.Leg()

        if leg.LegType() == "Call Fixed Adjustable":            
            summary.ignore_action(reset, 'Leg is of type Call Fixed Adjustable', reset.Oid())
            continue
        if leg.LegType() == "Zero Coupon Fixed" and reset.ResetType()=="Compound":            
            summary.ignore_action(reset, 'Leg is of type Zero Coupon Fixed', reset.Oid())
            continue

        ins = leg.Instrument()
        
        if reset.ResetType() == 'Spread':
            SpreadFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
        
        elif reset.ResetType() == 'Tax Factor':
            TaxFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
            
        elif not reset.FixResetFromReference():
            if fixingCategorization:
                toCurrency = leg.FixingCurrency(reset.ResetType())
                CustomCategoryFixing(summary, reset, leg, ins, None, None, getOpManFixingRates, backdateResets, toCurrency)
                
        elif reset.FixingInstrument() and reset.FixingInstrument().IsCPIPriceIndex():
            CPIFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)

        elif reset.IsAggregatingRate():
            if( spread_hook ):
                SpreadHookFixing(summary, reset, leg, ins, hook, interpol_hook, spread_hook, getOpManFixingRates, backdateResets)
            else:            
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, backdateResets)

        elif reset.ResetType() == 'Settlement FX':
            toCurrency = leg.Currency()
            FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)

        elif reset.ResetType() == 'Float Reference FX':
            fxRate = leg.FloatReferenceFxFixingFxRate()
            toCurrency = fxRate.DomesticCurrency() if fxRate.ForeignCurrency().IsEqual(reset.FixingInstrument()) else fxRate.ForeignCurrency()
            FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
		
        elif reset.ResetType() == 'Index Reference FX':
            toCurrency = leg.Instrument().Currency()
            FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
		
        elif reset.ResetType() == 'Single':
            if( spread_hook ):
                SpreadHookFixing(summary, reset, leg, ins, hook, interpol_hook, spread_hook, getOpManFixingRates, backdateResets)
            elif reset.StubEstimation() != None:
                if 'Closest' == reset.StubEstimation().FixingMethod():
                    FlatStubFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
                elif 'Interpolate' == reset.StubEstimation().FixingMethod():
                    InterpolateStubFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
                else:
                    UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
            else:
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, backdateResets)

        elif reset.ResetType() == 'Nominal Scaling':
            if leg.NominalScaling() in ('FX', 'FX Fixing In Arrears'):
                toCurrency = leg.ScalingCurrency()
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
            elif leg.NominalScaling() in ('Price', 'None', 'Dividend'):
                toCurrency = leg.NominalScalingCurrency()
                PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
        
        elif reset.ResetType() == 'Nominal Scaling FX':
            if leg.NominalScaling() in ('None', 'Price', 'Initial Price', 'Dividend', 'Dividend Initial Price'):
                toCurrency = leg.ScalingCurrency()
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)

        elif reset.ResetType() == 'Dividend Scaling':
            if leg.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                toCurrency = ins.Currency()
                PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
                
        elif reset.ResetType() == 'Return':
            if leg.NominalScaling() in  ('Price', 'Initial Price', 'None'):
                if 'TotalReturnSwap' == ins.InsType():
                    toCurrency = leg.ScalingCurrency()
                    PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
                else:
                    StandardFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)  
            elif leg.NominalScaling() in ('FX', 'FX Fixing In Arrears'):
                toCurrency = leg.ScalingCurrency()
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets, toCurrency)
            elif leg.NominalScaling() == 'Dividend':
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, backdateResets)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
        elif reset.ResetType() == 'Trigger':
            TriggerFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, backdateResets)
        elif reset.ResetType() == 'Total Cash Flow':
            TotalCashFlowFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)
        else:
            UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, backdateResets)

    if args['extend_oe']:
        extend_open_end(args['extend_ins'], summary)
    summary.log(args)

def fix_insdef_entry_point(acm_reset_array):
    if acm_reset_array:
        pyargs = {}
        pyargs["resets"] = acm_reset_array
        pyargs["GetOpManFixingRates_DoNotCommit"] = True
        pyargs["extend_oe"] = False
        pyargs["backdateResets"] = True

        logme.setLogmeVar("", # ScriptName
                          0,  # LogMode
                          0,  # LogToConsole
                          0,  # LogToFile
                          "", # LogFile
                          0,  # SendReportByMail
                          "", # MailList
                          "") # ReportMessageType
        fix(pyargs)

def UsedPrice(ins, date, curr = None, market = None):
    if date < acm.Time.DateToday():
        price = acm.PriceRetrieval.SimpleHistoricalPrice(ins, date, curr, market, 'None')
        if price.Type().Text() == 'Missing':
            return acm.Math.NotANumber()
	else:
            return price.Number()
    else:
        marketPriceParams = acm.FDictionary()
        if None != date:
            marketPriceParams['priceDate'] = date
        if None != curr:
            marketPriceParams['currency'] = curr
        if None != market:
            marketPriceParams['marketPlace'] = market
            marketPriceParams['useSpecificMarketPlace'] = True
        return ins.Calculation().MarketPriceParams(space, marketPriceParams).Value().Number()

def InterpolatedInflationValue(fixing_instrument, date, index_type, firstCashFlowPayDateIfAUD, mappedCPIFunctionLink):
    interpolatedInflationValueParams = acm.FDictionary()
    interpolatedInflationValueParams['inflationTargetDate'] = date
    interpolatedInflationValueParams['inflationInstrumentIndexType'] = index_type
    interpolatedInflationValueParams['firstCashFlowPayDateForStandardCalculation'] = firstCashFlowPayDateIfAUD
    interpolatedInflationValueParams['mappedCPIFunctionLinkForStandardCalculation'] = mappedCPIFunctionLink
    return fixing_instrument.Calculation().InterpolatedInflationValueParams(space, interpolatedInflationValueParams).Value().Number()

class StandardFixing:

    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_fn = None, getOpManFixingRates = 0, backdateResets = False):
        self.summary = summary
        self.reset = reset
        self.leg = leg
        self.ins = ins
        self.hook_fn = hook_fn
        self.interpol_fn = interpol_fn
        self.getOpManFixingRates = getOpManFixingRates
        self.ok = 0
        self.backdateResets = backdateResets
        self.rate = self.CalculateRate()
        self.rate2 = self.CalculateRate2()
        if self.ok:
            self.save()

    def reference(self):
        return self.reset.FixingInstrument()

    def calculate(self):
        market = self.leg.FloatRefFixingSource()
        return UsedPrice(self.reference(), self.reset.Day(), None, market)  

    def reference2(self):
        return self.reset.FixingInstrument2()

    def calculate2(self):
        return UsedPrice(self.reference2(), self.reset.Day(), None, None)  

    def CalculateRate(self):
        if self.hook_fn and self.hook_fn(self.reset, 1):
            rate = self.hook_fn(self.reset, 1)
            if (acm.Math().IsFinite(rate)):
                self.ok = 1
                return rate
            else:
                logme('No rate found from hook %s' %(self.reset.Oid()), 'DEBUG')
                self.summary.ignore_action(self.reset, 'No rate found from hook', self.reset.Oid())
        elif self.interpol_fn and self.interpol_fn(ael.CashFlow[self.reset.CashFlow().Oid()], ael.Reset[self.reset.Oid()]):
            rate = self.interpol_fn(ael.CashFlow[self.reset.CashFlow().Oid()], ael.Reset[self.reset.Oid()])
            if (acm.Math().IsFinite(rate)):
                self.ok = 1
                return rate
            else:
                logme('No rate found from interpolation hook %s' %(self.reset.Oid()), 'DEBUG')
                self.summary.ignore_action(self.reset, 'No rate found from interpolation hook', self.reset.Oid())
        else:
            ref = self.reference()
            if ref or self.reset.ResetType() == "Total Cash Flow" or self.reset.ResetType() == "Spread":
                rate = self.calculate()
                if (acm.Math().IsFinite(rate)):
                    self.ok = 1
                    return rate
                else:
                    logme('No rate found for reset %s' %(self.reset.Oid()), 'DEBUG')
                    self.summary.ignore_action(self.reset, 'No rate found', self.reset.Oid())
            else:
                logme('No fixing reference found %s' %(self.reset.Oid()), 'DEBUG')
                self.summary.ignore_action(self.reset, 'Undefined fixing reference', self.reset.Oid())
                
    def CalculateRate2(self):
        if self.reference2():
            if self.hook_fn and self.hook_fn(self.reset, 2):
                rate = self.hook_fn(self.reset, 2)
                if (acm.Math().IsFinite(rate)):
                    return rate
                else:
                    self.ok = 0
                    logme('No rate 2 found from hook %s' %(self.reset.Oid()), 'DEBUG')
                    self.summary.ignore_action(self.reset, 'No rate 2 found from hook', self.reset.Oid())
            else:
                rate = self.calculate2()
                if (acm.Math().IsFinite(rate)):
                    return rate
                else:
                    self.ok = 0
                    logme('No rate 2 found for reset %s' %(self.reset.Oid()), 'DEBUG')
                    self.summary.ignore_action(self.reset, 'No rate 2 found', self.reset.Oid())
        return 0

    def save(self):
        if self.getOpManFixingRates:
            # Do Not Commit Changes
            self.reset.FixFixingValue(self.rate)
            self.reset.FixFixingValue2(self.rate2)
            if self.backdateResets:
                self.reset.ReadTime( self.reset.Day() )
            logme('Get Rate Reset value %f [%s]' % (self.reset.FixingValue(), self.ins.Name()))        
        else:
            r_clone = self.reset.Clone()
            r_clone.FixFixingValue(self.rate)
            r_clone.FixFixingValue2(self.rate2)
            if self.backdateResets:
                r_clone.ReadTime( self.reset.Day() )
            self.reset.Apply(r_clone)
            self.reset.Commit()
            logme('Saved Reset value %f [%s]' % (r_clone.FixingValue(), self.ins.Name()))
        self.summary.ok_update(self.reset)

class StandardFXFixing(StandardFixing):
    
    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_fn = None, getOpManFixingRates = 0, backdateResets = False, toCurrency = None):
        self.toCurrency = toCurrency
        StandardFixing.__init__(self, summary, reset, leg, ins, hook_fn, interpol_hook, getOpManFixingRates, backdateResets)
        
    def ToCurrency(self):
        return self.toCurrency

class PriceInterpretationFixing(StandardFXFixing):

    def calculate(self):
        reference = self.reference()
        if reference.MtmFromFeed():
            p = UsedPrice(reference, self.reset.Day(), None, None)
        else:
            p = reference.Calculation().TheoreticalPrice(space).Number()
            
        if acm.Math().IsFinite(p):
            if 'All In' == self.reset.Leg().PriceInterpretationType():
                getObject = acm.GetFunction('getObject', 2)
                dirty = getObject('FQuotation', 'Pct of Nominal')
                p = reference.Calculation().PriceConvertSource(space, p, reference.Quotation(), dirty, self.reset.Day()).Value().Number()  
                
            curr1 = reference.Currency()
            curr2 = self.ToCurrency()
            
            if (None != curr1) and (None != curr2) and (curr1 != curr2):
                fx = UsedPrice(curr1, self.reset.Day(), curr2, None)  
                if acm.Math().IsFinite(fx):
                    p *= fx   
        else:
            p = None 
           
        return p
      
class CPIFixing(StandardFixing):

    def firstCashFlowPayDateIfAUD(self):
        leg = self.reset.Leg()
        cfs = leg.CashFlows()
        firstCashFlowPayDate = None
        for cf in cfs:
            if firstCashFlowPayDate is None:
                firstCashFlowPayDate = cf.PayDate()
            if cf.PayDate() <firstCashFlowPayDate:      
                firstCashFlowPayDate = cf.PayDate()
        return firstCashFlowPayDate

    def mappedCPIFunctionLink(self):
        if (self.ins.MappedCPIFunctionLink().Link()):
            link = self.ins.MappedCPIFunctionLink().Link()
        else:
            link = self.reference().MappedCPIFunctionLink().Link()
        return link

    def calculate(self):
        index_type = self.ins.IndexType() if self.ins.IndexType() != 'None' else self.reference().IndexType()
        if index_type == "CPI AUD":
            firstCashFlowPayDateIfAUD = self.firstCashFlowPayDateIfAUD()
        else:  
            firstCashFlowPayDateIfAUD = 0
        if index_type == "Custom":
            mappedCPIFunctionLink = self.mappedCPIFunctionLink()
        else:
            mappedCPIFunctionLink = ""
        p = InterpolatedInflationValue(self.reference(), self.reset.Day(), index_type, firstCashFlowPayDateIfAUD, mappedCPIFunctionLink)
        if not acm.Math().IsFinite(p):
            p = None
        return p


class FXFixing(StandardFXFixing):
   
    def calculate(self):
        market = self.leg.Instrument().FixingSource()
        return UsedPrice(self.reference(), self.reset.Day(), self.ToCurrency(), market)


class CustomCategoryFixing(StandardFXFixing):
    def reference(self):
        return True
    
    def calculate(self):
        fixingParams = acm.FDictionary()
        fixingParams["fixingDate"] = self.reset.Day()
        fixingParams["resetType"] = self.reset.ResetType()
        fixingParams["fixingCurrency"] = self.ToCurrency()
        fixingValue = self.leg.Calculation().FixingValueFromCategorizationParamsSource(space, fixingParams)
        return fixingValue.Value().Number()

class UnknownFixing(StandardFixing):

    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_fn = None, getOpManFixingRates = 0, backDatedResets = None):
        logme('Unknown fixing with reset type '+reset.ResetType()+' and leg nominal scaling '+leg.NominalScaling()+'.')
        """
        super('UnknownFixing', self).__init__(summary, reset, leg, ins, hook_fn, interpol_fn, getOpManFixingRates)
        """
        
    def reference(self):
        return None

    def calculate(self):
        return None

class TotalCashFlowFixing(StandardFixing):
    def calculate(self):
        cf = self.reset.CashFlow()
        createVirtualTrade = acm.GetFunction("createVirtualTradeFromInstrument", 1)
        trade = createVirtualTrade(cf.Leg().Instrument())
        trade.TradeTime("1970-01-01")
        trade.AcquireDay("1970-01-01")
        val = cf.Calculation().Projected(space, trade).Value().Number()
        if cf.Leg().PayLeg():
            val = val * -1.0
        return val

class SpreadFixing(StandardFixing):
    def calculate(self):
        return self.leg.Calculation().CustomSpreadFixing(space, self.reset.Day()).Number()

class SpreadHookFixing(StandardFixing):

    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_hook = None, spread_hook_fn = None, getOpManFixingRates = 0, backdateResets = None):
        self.reset = reset
        self.spread_hook_fn = spread_hook_fn           
        StandardFixing.__init__(self, summary, reset, leg, ins, hook_fn, interpol_hook, getOpManFixingRates, backdateResets)

    def calculate(self):
        rate = StandardFixing.calculate(self)
        if( rate == None ):
          return None
        spread = 0.0
        if( self.spread_hook_fn ):
            spread = self.spread_hook_fn( self.reset, w )

        logme('Calculated rate: %f ' % (rate) )
        logme('Calculated spread: %f ' % (spread) )
        return rate + spread
        
class FlatStubFixing(StandardFixing):
   
    def reference(self):
        return self.reset.StubEstimation().FixingRef1()

class InterpolateStubFixing(StandardFixing):
    
    def reference(self):
        return self.reset.StubEstimation().FixingRef1() and self.reset.StubEstimation().FixingRef2()
        
    def calculate(self):
        reference1 = self.reset.StubEstimation().FixingRef1()
        reference2 = self.reset.StubEstimation().FixingRef2()
        prevFixingValue = UsedPrice(reference1, self.reset.Day(), None, None)
        nextFixingValue = UsedPrice(reference2, self.reset.Day(), None, None)
        return self.reset.StubEstimation().CalculateInterpolatedValue(self.reset.Day(), self.reset.CashFlow().StartDate(), self.reset.CashFlow().EndDate(), self.reset.Leg().DayCountMethod(), prevFixingValue, nextFixingValue, False)
        
class TaxFixing(StandardFixing):
    def reference(self):
        return True
    def calculate(self):
        return self.leg.Calculation().CustomTaxFixing(space, self.reset.Day()).Number()

class TriggerFixing(StandardFixing):
    def calculate(self):
        market = self.leg.TrigRefFixingSource()
        return UsedPrice(self.reference(), self.reset.Day(), None, market)  
