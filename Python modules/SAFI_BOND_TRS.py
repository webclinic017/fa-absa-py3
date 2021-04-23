'''
Date                    : 2010-09-23, 2011-01-05
Purpose                 : This script is required to correctly price Bond Total Return Swaps. It fixes the return leg with the same end price as
                           the equivalent buy sell back
Department and Desk     : Front Office - Equity Derivatives/ Fixed Income
Requester               : Shameer Sukha/ Kelly Hattingh
Developer               : Zaakirah Kajee
CR Number               : 441973, 544522

Date            Developer               Change
2010-12-09      Paul Jacot-Guillarmod   521283: Script updated to simulate a fixng so that benchmark deltas can be calculated.
2011-01-05      Zaakirah Kajee          544522: Don't fix trs from 2 business days before expiry.
2011-05-19      Paul Jacot-Guillarmod   658112: Update the function PVSimulateFixedFilter to check the instrument type on the Total Return Leg instead of the underlying
2011-06-01      Zaakirah Kajee          680337: Updated start date of bsb to t + 3, also removed sets module for python upgrade. 
2011-08-23      Paul Jacot-Guillarmod   Upgrade Change: Update the price index, TRS_SACPI, with forward prices before fixing the TRS's
2011-12-08      Zaakirah Kajee          851616: Updated condition for TRS fixing before expiry.
2018-05-10      Ondrej Bahounek         CHG1000369823: ABITFA-5352 - New Africa Sov Bond TRSs
'''

import ael, acm
import SAFI_Update_Index_ForwardPrices
from at_logging import getLogger


LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()

ael_gui_parameters = { 'windowCaption':'Bond TRS Fixing script'}
ael_variables = [ ('Instruments', 'Instruments: ', 'FInstrument', None, None, 0, 1, 'List of Instruments')]


def GetReset(ins):
    leg = ins.FirstTotalReturnLeg()
    for cf in leg.CashFlows():
        if cf.CashFlowType() == 'Total Return':
            for r in cf.Resets():
                #print r.Day(), ins.ExpiryDateOnly()
                if r.ResetType() == 'Return' and r.Day() == leg.EndDate():
                    return r
    return None


def GetAllInEndPrice(ins):
    i = ael.Instrument[ins.Name()]
    return i.und_insaddr.dirty_from_yield(i.exp_day, None, None, i.ref_price)


def get_curve(ins):
    curve = ins.AdditionalInfo().UsedYieldCurve()
    if not curve:
        curve = ins.MappedRepoLink(ins.Currency()).Link().YieldCurveComponent()
    return curve


def FixTRSReset(ins, simulate=False):
    
    ref_ins = ins.AdditionalInfo().TRS_Ref_Instrument()
    if not ref_ins:
        LOGGER.info("Skipping '%s': missing 'TRS Ref Instrument' addinfo", ins.Name())
        return
        
    if ref_ins.InsType() != "BuySellback":
        raise RuntimeError("%s: 'TRS Ref Instrument' addinfo is not BSB", ins.Name())
    
    cal = ins.Currency().Calendar()
    endDate = ins.FirstTotalReturnLeg().EndDate()
    
    if cal.BankingDaysBetween(TODAY, endDate) > 2 and endDate > TODAY:
        RefCal = ref_ins.Currency().Calendar()
        tPlus_days = RefCal.AdjustBankingDays(TODAY, 3)
        if ref_ins.Currency().Name() in ('USD', 'EUR') and ref_ins.add_info('UsedYieldCurve'):
            tPlus_days = RefCal.AdjustBankingDays(TODAY, 2)
        
        resetval = 0
        ref_und = ref_ins.Underlying()

        t = ref_ins.Trades().At(0)
        ael_trade = ael.Trade[t.Oid()]
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        if ref_und.ValuationGrpChlItem().Name().startswith('AC_GLOBAL_CORP'):           
            price= ref_und.Calculation().TheoreticalPrice(calcSpace).Number()
        else:
            price= ref_und.Calculation().MarketPrice(calcSpace).Number()
        
        curve = get_curve(ref_ins)
        day_count_method = ref_ins.DayCountMethod()

        if curve.IsKindOf(acm.FYCAttribute):
            curve_ir = curve.IrCurveInformation(curve.UnderlyingCurve().IrCurveInformation(), TODAY)
            rate = curve_ir.Rate(tPlus_days, ref_ins.ExpiryDateOnly(), 'Simple', day_count_method, 'Spot Rate') * 100
        else:
            rate = curve.Rate(tPlus_days, ref_ins.ExpiryDateOnly(), 'Simple', day_count_method) * 100
        
        t.Price(price)
        ref_ins.Rate(rate)
        ref_ins.StartDate(tPlus_days)
        
        ref_ins.RefPrice(ael_trade.buy_sellback_ref_price())
        ref_ins.RefValue(ael_trade.buy_sellback_ref_value(1))
        
        reset = GetReset(ins)
        
        if ins.FirstTotalReturnLeg().PriceInterpretationType() == 'All In':
            resetval = GetAllInEndPrice(ref_ins)
        if ins.FirstTotalReturnLeg().PriceInterpretationType() == 'As Reference':
            resetval = 0.0  # ref_ins.RefPrice()

        if reset and resetval != 0:
            reset.FixingValue(resetval)
            reset.ReadTime(acm.Time().TimeNow())
            if simulate:
                return
                
            # Note: When commiting any new entities update the SimulateTRS procedure to reflect this
            t.Commit()
            ref_ins.Commit()
            reset.Commit()
            ins.Commit()
            LOGGER.info("Instrument '%s' has been fixed.", ins.Name())

        else:
            raise RuntimeError("'%s' could not find correct reset to fix." % ins.Name())
    else:
        LOGGER.warning("TRS '%s' not fixed because end date is within 2 business days.", ins.Name())


def SimulateTRS(instrument, simulate):
    ''' Given a TRS simulate/unsimulate the TRS, TRS reset, BSB (instrument and trade) 
    '''
    refInstrument = instrument.AdditionalInfo().TRS_Ref_Instrument() 
    trade = refInstrument.Trades().At(0)
    reset = GetReset(instrument)
    
    if simulate:
        instrument.Simulate()
        refInstrument.Simulate()
        trade.Simulate()
        if reset:
            reset.Simulate()
    else:
        instrument.Unsimulate()
        refInstrument.Unsimulate()
        trade.Unsimulate()
        if reset:
            reset.Unsimulate()


def PresentValue(tradeFilter):
    ''' Return the present value of a tradefilter.  This is done in ael as its more memory
        efficient than the acm equivalent.
    '''
    aelFilter = ael.TradeFilter[tradeFilter.Name()]
    return aelFilter.present_value()


def PVSimulateFixedFilter(tradeFilter):
    ''' Simulate the fixing to all bond TRS's in the tradefilter and return the PV of the tradefilter
    '''
    trsInstruments = set([])
    for trade in tradeFilter.Trades():
        instrument = trade.Instrument()
        if instrument.InsType() in ['TotalReturnSwap'] and instrument.FirstTotalReturnLeg().IndexRef().InsType() in ['Bond', 'IndexLinkedBond']:
            trsInstruments.add(instrument)
    
    for trs in trsInstruments:
        SimulateTRS(trs, True)
        
    try:
        for trs in trsInstruments:
            FixTRSReset(trs, True)
    except:
        if trsInstruments:
            for trs in trsInstruments:
                SimulateTRS(trs, False)
    
    pv = PresentValue(tradeFilter)
    
    for trs in trsInstruments:
        SimulateTRS(trs, False)
    
    return pv


def ael_main(data):
    LOGGER.msg_tracker.reset()
    
    priceIndex = acm.FInstrument['TRS_SACPI']
    SAFI_Update_Index_ForwardPrices.AddForwardPrices(priceIndex, 10)
    
    for ins in data['Instruments']:
        try:
            LOGGER.info("Fixing '%s'...", ins.Name())
            FixTRSReset(ins, False)
        except:
            LOGGER.exception("Instrument not fixed.")
        
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.info("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")
