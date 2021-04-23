
"""----------------------------------------------------------------------------
MODULE
    FFixPerform - Module which executes fixing.

    (c) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module executes the fixing procedure based on the
    parameters passed from the script FFixing.

Comments of the 2010 version:

Date            Who                             What
    
2010-07-02      Paul Jacot-Guillarmod           CR 361048: When fixing total return resets for TRS's use the market price, not the spot.
2010-11-18      Herman Hoon                     CR 497952: The initial reset of TRS needs to be excluded from fixing. When the TRS currency != underlying currency, the fx conversion of the undelying price should be done.
2011-03-10      Herman Hoon                     CR 595802: For TRS Fixing exclude the Floating legs, Nominal Scaling cashflows if the value is not equal to 0.
2011-03-16      Heinrich Cronje                 CR 602188: The function extend_open_end should not pull all Open Ended
2018-04-18      Libor Svoboda                   FX fixing for Metals_Compo PriceSwaps
2019-10-01      Libor Svoboda                   FAU-445: Disable extending all open ended instruments
                             
The script is not migrated now but the following changes are included on the Default script during the upgrade 2013 project:
-The dividend scaling is always set to the initial price of the TRS 
-The initial reset of TRS needs to be excluded from fixing.
----------------------------------------------------------------------------"""
#Import builtin modules
import time
import FBDPString
import at_time

#Import Front modules
import acm
import ael

logme = FBDPString.logme
from FBDPCommon import SummaryLocal
hook = False
try:
    from FBDPHook import calculate_fixing
except ImportError:
    pass
else:
    hook = calculate_fixing

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

def get_total_return_leg(trs):
    equity_leg = None
    for leg in trs.Legs():
        if leg.LegType() == 'Total Return':
            equity_leg = leg
            break
    return equity_leg

def IsCallFloatNotOverNight(instr):
    legs = instr.Legs()
    
    for leg in legs:
        if (leg.LegType() == "Call Float" and leg.ResetPeriod() != '1d'):
            return True
    return False


def extend_open_end( inst, summary ):
    logme('Extending open ended...')
    # FA Upgrade 2018 - commenting out default logic
    # This should be never allowed in our environment
    #if not len(inst):
    #    inst = acm.FInstrument.Select('openEnd = "Open End"')
    for i in inst:
        if not IsOpenEnded(i):
            ael.log('Extend open end: Instrument %s not extended, Open End status %s'%(i.Name(), i.OpenEnd()))
            continue

        if IsCallFloatNotOverNight(i):
            ael.log('Extend open end: Instrument %s not extended, Call Float and reset period != 1 day not supported.'%i.Name())
            continue

        try:
            i.ExtendOpenEnd()
        except RuntimeError, msg:
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
    space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

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
        if leg.LegType() == "Zero Coupon Fixed":            
            summary.ignore_action(reset, 'Leg is of type Zero Coupon Fixed', reset.Oid())
            continue

        ins = leg.Instrument()
        if reset.ResetType() in ('Weighted', 'Unweighted', 'Compound', 'Flat Compound', 'Weighted 1m Compound', 'Accretive', 'Total Weighted', 'Compound of Weighted'):
            if (ins.InsType() == 'PriceSwap' and ins.ValuationGrpChlItem() and
                    ins.ValuationGrpChlItem().Name() == 'Metals_Compo'):
                FXFixingPriceSwap(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, space)
            elif spread_hook:
                SpreadHookFixing(summary, reset, leg, ins, hook, interpol_hook, spread_hook, getOpManFixingRates, space)
            else:            
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, space)

        elif reset.ResetType() == 'Settlement FX':
            FXOriginalCurrencyFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)

        elif reset.ResetType() == 'Single':
            if( spread_hook ):
                SpreadHookFixing(summary, reset, leg, ins, hook, interpol_hook, spread_hook, getOpManFixingRates, space)
            elif reset.StubEstimation() != None:
                if 'Closest' == reset.StubEstimation().EstimationMethod():
                    FlatStubFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                elif 'Interpolate' == reset.StubEstimation().EstimationMethod():
                    InterpolateStubFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                else:
                    UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            else:
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, space)

        if reset.FixingInstrument() and reset.FixingInstrument().IsCPIPriceIndex():            
            CPIFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)            
            
        elif reset.ResetType() == 'Nominal Scaling':           
            if leg.NominalScaling() in ('FX', 'FX Fixing In Arrears'):
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            elif leg.NominalScaling() in ('Price', 'Initial Price', 'None'):
                if 'TotalReturnSwap' == ins.InsType():
                    #The first reset is configured by the initial price field in the instrument setup
                    if ins.StartDate() != reset.Day():
                        total_return_leg = get_total_return_leg(ins)
                        funding_leg = ins.TotalReturnFundingLeg()
                        if leg != total_return_leg and not reset.IsFixed():
                            PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                        elif leg == total_return_leg:
                            PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                            if total_return_leg.NominalScaling() == 'Price' and funding_leg.NominalScaling() == 'Price':
                                funding_reset = acm.CreateFASQLQuery(acm.FReset, 'AND')
                                funding_reset.AddAttrNode('Leg.Oid', 'EQUAL', funding_leg.Oid())
                                funding_reset.AddAttrNode('ResetType', 'EQUAL', 'Nominal Scaling')
                                #better to hard code the calendar since the reset calendar is often incorrect
                                time_to = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(at_time.acm_date('Today'), 3)
                                funding_reset.AddAttrNodeNumerical('Day', at_time.acm_date('Today'), time_to)
                                funding_reset = funding_reset.Select()
                                if funding_reset.Size() == 1:
                                    funding_reset = funding_reset.At(0)
                                    funding_reset.FixFixingValue(reset.FixFixingValue())
                                    funding_reset.FixFixingValue2(reset.FixFixingValue())
                                    funding_reset.Commit()
                                    logme('TR nominal scaling reset %s fixed TR nominal scaling reset %s on the funding leg.' % (reset.Oid(), funding_reset.Oid()))
                else:
                    StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, space)
            elif leg.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
        
        elif reset.ResetType() == 'Nominal Scaling FX':
            if leg.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                FXOriginalCurrencyFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            elif leg.NominalScaling() in ('Price', 'Initial Price', 'None'):
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)

        elif reset.ResetType() == 'Dividend Scaling':
            if leg.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                
        elif reset.ResetType() == 'Return':
            if leg.NominalScaling() in  ('Price', 'Initial Price', 'None'):
                if 'TotalReturnSwap' == ins.InsType():
                    #The first reset is configured by the initial price field in the instrument setup
                    if ins.StartDate() != reset.Day() and leg.LegType() != 'Float':
                        PriceInterpretationFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
                else:
                    StandardFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)  
            elif leg.NominalScaling() in ('FX', 'FX Fixing In Arrears'):
                FXFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
            elif leg.NominalScaling() == 'Dividend':
                StandardFixing(summary, reset, leg, ins, hook, interpol_hook, getOpManFixingRates, space)
            else:
                UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)
        else:
            UnknownFixing(summary, reset, leg, ins, hook, None, getOpManFixingRates, space)

    if args['extend_oe']:
        extend_open_end(args['extend_ins'], summary)
    summary.log(args)
    
def MarketPrice(ins, date):
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
    calc_space.SimulateGlobalValue('Valuation Date', date)
    calc = calc_space.CalculateValue(ins, 'Instrument Market Price')
    return calc.Value().Number()

def fix_insdef_entry_point(acm_reset_array):
    if acm_reset_array:
        pyargs = {}
        pyargs["resets"] = acm_reset_array
        pyargs["GetOpManFixingRates_DoNotCommit"] = True
        pyargs["extend_oe"] = False

        logme.setLogmeVar("", # ScriptName
                          0,  # LogMode
                          0,  # LogToConsole
                          0,  # LogToFile
                          "", # LogFile
                          0,  # SendReportByMail
                          "", # MailList
                          "") # ReportMessageType
        fix(pyargs)

def UsedPrice(ins, date, curr = None, price_find_type = 'None', market = None, space = None):
    dict = acm.FDictionary()
    if None != date:
        dict['priceDate'] = date
    if None != curr:
        dict['currency'] = curr
    if price_find_type and price_find_type != 'None':
        if price_find_type == 'Ask' or price_find_type == 'Bid':
            dict['typeOfPrice'] = 'Average'+price_find_type+'Price'
        else:
            dict['typeOfPrice'] = price_find_type+'Price'
    if None != market:
        dict['marketPlace'] = market
        dict['useSpecificMarketPlace'] = True
    return ins.Calculation().MarketPriceParams(space, dict).Value().Number()

def toInsCurrFactor(refCurr, insCurr, date):
    aelRefCurr = ael.Instrument[refCurr]
    return aelRefCurr.used_price(ael.date(date), insCurr)   

def TheoreticalPrice(ins, curr = None, space = None):
    dict = acm.FDictionary()
    if None != curr:
        dict['currency'] = curr
    return ins.Calculation().TheoreticalPriceParams(space, dict).Value().Number()

def CapitalValue(ins, date = None, space = None):
    dict = acm.FDictionary()
    if None != date:
        dict['indexDate'] = date
    return ins.Calculation().CapitalValueParams(space, dict).Value().Number()
    
def InterpolatedInflationValue(fixing_instrument, date, index_type, firstCashFlowPayDateIfAUD, mappedCPIFunctionLink, space):
    interpolatedInflationValueParams = acm.FDictionary()
    interpolatedInflationValueParams['inflationTargetDate'] = date
    interpolatedInflationValueParams['inflationInstrumentIndexType'] = index_type
    interpolatedInflationValueParams['firstCashFlowPayDateForStandardCalculation'] = firstCashFlowPayDateIfAUD
    interpolatedInflationValueParams['mappedCPIFunctionLinkForStandardCalculation'] = mappedCPIFunctionLink
    return fixing_instrument.Calculation().InterpolatedInflationValueParams(space, interpolatedInflationValueParams).Value().Number()

class StandardFixing:
    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_fn = None, getOpManFixingRates = 0, space = None):
        self.summary = summary
        self.reset = reset
        self.leg = leg
        self.ins = ins
        self.hook_fn = hook_fn
        self.interpol_fn = interpol_fn
        self.getOpManFixingRates = getOpManFixingRates
        self.ok = 0
        self.rate = self.CalculateRate(space)
        self.rate2 = self.CalculateRate2(space)
        if self.ok:
            self.save()

    def reference(self):
        return self.reset.FixingInstrument()

    def calculate(self, space):
        return UsedPrice(self.reference(), self.reset.Day(), None, 'None', None, space)

    def reference2(self):
        return self.reset.FixingInstrument2()

    def calculate2(self, space):
        return UsedPrice(self.reference2(), self.reset.Day(), None, 'None', None, space)  

    def CalculateRate(self, space):
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
            if ref:
                rate = self.calculate(space)
                if (acm.Math().IsFinite(rate)):
                    self.ok = 1
                    return rate
                else:
                    logme('No rate found for reset %s' %(self.reset.Oid()), 'DEBUG')
                    self.summary.ignore_action(self.reset, 'No rate found', self.reset.Oid())
            else:
                logme('No fixing reference found %s' %(self.reset.Oid()), 'DEBUG')
                self.summary.ignore_action(self.reset, 'Undefined fixing reference', self.reset.Oid())

    def CalculateRate2(self, space):
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
                rate = self.calculate2(space)
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
            logme('Get Rate Reset value %f [%s]' % (self.reset.FixingValue(), self.ins.Name()))        
        else:
            r_clone = self.reset.Clone()
            r_clone.FixFixingValue(self.rate)
            r_clone.FixFixingValue2(self.rate2)
            self.reset.Apply(r_clone)
            self.reset.Commit()
            logme('Saved Reset value %f [%s]' % (r_clone.FixingValue(), self.ins.Name()))
        self.summary.ok_update(self.reset)


class PriceInterpretationFixing(StandardFixing):
    def calculate(self, space):
        reference = self.reference()
        if reference.MtmFromFeed():
            p = UsedPrice(reference, self.reset.Day(), None, 'None', None, space)
        else:
            p = TheoreticalPrice(reference, None, space)
        if acm.Math().IsFinite(p):
            if 'All In' == self.reset.Leg().PriceInterpretationType():
                getObject = acm.GetFunction('getObject', 2)
                dirty = getObject('FQuotation', 'Pct of Nominal')
                try:
                    p = reference.Calculation().PriceConvertSource(space, p, reference.Quotation(), dirty, self.reset.Day()).Value().Number()
                except AttributeError:
                    print "WARNING: AttributeError in PriceInterpretationFixing"
                    #To cater for values that are float, since number throws an error for floats.
                    p = reference.Calculation().PriceConvertSource(space, p, reference.Quotation(), dirty, self.reset.Day()).Value()
                    
        else:
            p = None            
        if acm.Math().IsFinite(p):
            if 'TotalReturnSwap' == self.leg.Instrument().InsType():
                if self.reset.ResetType() in ('Nominal Scaling', 'Dividend Scaling'):
                    curr1 = reference.Currency()
                    curr2 = self.ins.Currency()
                    if self.reset.ResetType() == 'Dividend Scaling':
                        p =  self.leg.InitialIndexValue()
                elif self.reset.ResetType() == 'Return':
                    curr1 = reference.Currency()
                    curr2 = self.leg.ScalingCurrency()
                else:
                    curr1 = None
                    curr2 = None
                if (None != curr1) and (None != curr2) and (curr1 != curr2):
                    fx = UsedPrice(curr1, self.reset.Day(), curr2, 'None', None, space)  
                    if acm.Math().IsFinite(fx):
                        p = p * fx
                    else:
                        p = None
        return p

class TRSIndexRefFixing(StandardFixing):
    def calculate(self):
        pi_theor_price = MarketPrice(self.reference(), self.reset.Day())
        fxFactor = toInsCurrFactor(self.reference().Currency().Name(), self.ins.Currency().Name(), self.reset.Day())
        
        price = pi_theor_price * fxFactor
        
        if acm.Math().IsFinite(price):
            return price
        else:
            return None
        
    def reference(self):
        return self.leg.Currency() and self.reset.FixingInstrument()

    def calculate(self):
        return UsedPrice(self.reset.FixingInstrument(), self.reset.Day(), self.leg.Currency().Name()) or None
          
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

    def calculate(self, space):
        index_type = self.ins.IndexType() if self.ins.IndexType() != 'None' else self.reference().IndexType()
        if index_type == "CPI AUD":
            firstCashFlowPayDateIfAUD = self.firstCashFlowPayDateIfAUD()
        else:  
            firstCashFlowPayDateIfAUD = 0
        if index_type == "Custom":
            mappedCPIFunctionLink = self.mappedCPIFunctionLink()
        else:
            mappedCPIFunctionLink = ""
        p = InterpolatedInflationValue(self.reference(), self.reset.Day(), index_type, firstCashFlowPayDateIfAUD, mappedCPIFunctionLink, space)
        if not acm.Math().IsFinite(p):
            p = None
        return p

class FXFixing(StandardFixing):

    def calculate(self, space):
        return UsedPrice(self.reference(), self.reset.Day(), self.leg.ScalingCurrency(), 'None', None, space)


class FXFixingPriceSwap(StandardFixing):

    def calculate(self, space):
        fixing_source = self.ins.AdditionalInfo().Fixing_Source()
        if fixing_source:
            return (UsedPrice(self.reference(), self.reset.Day(), None, 'None', None, space)
                    * UsedPrice(self.reference().Currency(), self.reset.Day(), self.leg.Currency(), 'None', fixing_source, space))
        return UsedPrice(self.reference(), self.reset.Day(), self.leg.Currency(), 'None', None, space)


class FXOriginalCurrencyFixing(StandardFixing):

    def calculate(self, space):
        market = self.leg.Instrument().FixingSource()
        return UsedPrice(self.reference(), self.reset.Day(), self.leg.Currency(), 'None', market, space)  
    
class UnknownFixing(StandardFixing):

    def __init__(self, summary, reset, leg, ins, hook_fn = None, interpol_fn = None, getOpManFixingRates = 0, space = None):
        logme('Unknown fixing with reset type '+reset.ResetType()+' and leg nominal scaling '+leg.NominalScaling()+'.')
        """
        super('UnknownFixing', self).__init__(summary, reset, leg, ins, hook_fn, interpol_fn, getOpManFixingRates, space)
        """
        
    def reference(self):
        return None

    def calculate(self, space):
        return None

class SpreadHookFixing(StandardFixing):

    def __init__(self, reset, leg, ins, hook_fn = None, spread_hook_fn = None, getOpManFixingRates = 0, space = None):
        self.reset = reset
        self.spread_hook_fn =  spread_hook_fn           
        StandardFixing.__init__(self, reset, leg, ins, hook_fn, getOpManFixingRates, space)

    def calculate(self, space):
        rate = StandardFixing.calculate(self, space)
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
        
    def calculate(self, space):
        reference1 = self.reset.StubEstimation().FixingRef1()
        reference2 = self.reset.StubEstimation().FixingRef2()
        prevFixingValue = UsedPrice(reference1, self.reset.Day(), None, 'None', None, space)
        nextFixingValue = UsedPrice(reference2, self.reset.Day(), None, 'None', None, space)
        return self.reset.StubEstimation().CalculateInterpolatedValue(self.reset.Day(), self.reset.CashFlow().StartDate(), self.reset.CashFlow().EndDate(), self.reset.Leg().DayCountMethod(), prevFixingValue, nextFixingValue, False)
