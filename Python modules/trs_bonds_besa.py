"""
Date                    : 2017-08-03
Purpose                 : This script is required to correctly price Bond Total Return Swaps.
                          It fixes the return leg with the same end price as the equivalent BSB.
                          This script is a result of updated 'SAFI_BOND_TRS' script,
                          but uses BESA price of TRS's index reference.
Department and Desk     : AAM
Requester               : Suvarn Naidoo
Developer               : Ondrej Bahounek
CR Number               : 4811162

Date            Developer               Change
2017-08-03      Ondrej Bahounek         4811162: Initial deployment - start using Bond BESA prices.
2014-08-08      Ondrej Bahounek         4832977: get BESA prices even for current day.
"""

import ael, acm
import aam_tpl
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)

TODAY = acm.Time.DateToday()

ael_variables = AelVariableHandler()
ael_variables.add('instruments',
    label='Instruments:',
    cls='FInstrument',
    multiple=True,
    alt=("List of Instruments"))
ael_variables.add('val_date',
    label='Valuation Date:',
    cls='date',
    default='Today',
    alt=("Date of the price. "
         "Format: YYYY-MM-DD"))


def get_reset(ins):
    leg = ins.FirstTotalReturnLeg()
    for cf in leg.CashFlows():
        if cf.CashFlowType() == 'Total Return':
            for r in cf.Resets():
                if r.ResetType() == 'Return' and r.Day() == leg.EndDate():
                    return r
    return None

    
def get_all_in_end_price(ins):
    i = ael.Instrument[ins.Name()]
    return i.und_insaddr.dirty_from_yield(i.exp_day, None, None, i.ref_price)


def fix_trx_reset(ins, val_date):
    
    LOGGER.info("Fixing '%s' for '%s'...", ins.Name(), val_date)
    
    ref_ins = ins.AdditionalInfo().TRS_Ref_Instrument()
    
    if not ref_ins or ref_ins.InsType() != "BuySellback":
        LOGGER.error("'%s' doesn't have Ref Instrument addinfo", ins.Name())
        return
    
    if ins.FreeText() != ref_ins.FreeText() != "BESA":
        LOGGER.error("Skipping '%s': missing BESA FreeText on TRS or BSB.", ins.Name())
        return
        
    cal = ins.Currency().Calendar()
    
    end_date = ins.FirstTotalReturnLeg().EndDate()
    
    if cal.BankingDaysBetween(TODAY, end_date) > 2 and end_date > TODAY:
        ref_cal = ref_ins.Currency().Calendar()
        tPlus3 = ref_cal.AdjustBankingDays(TODAY, 3)
        resetval = 0
        ref_und = ref_ins.Underlying()

        trade = ref_ins.Trades().At(0)
        
        price = aam_tpl._get_besa_price(ins.IndexReference(), val_date)
        if not price:
            raise RuntimeError("Missing BESA price for '%s' [%s]" % (ins.IndexReference().Name(), val_date))
            
        LOGGER.info("BESA price '%s' [%s]: %f", ins.IndexReference().Name(), val_date, price)
        
        curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()

        if not curve.IsKindOf(acm.FYCAttribute):
            rate =  ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent().Rate(
                tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365') * 100
        else:
            curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()
            curve = curve.IrCurveInformation(curve.UnderlyingCurve().IrCurveInformation(), TODAY)
            rate =  curve.Rate(tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365', 'Spot Rate') * 100
   
        trade.Price(price)
        ref_ins.Rate(rate)
        ref_ins.StartDate(tPlus3)
        
        ael_trade = ael.Trade[trade.Oid()]
        ref_ins.RefPrice(ael_trade.buy_sellback_ref_price())
        ref_ins.RefValue(ael_trade.buy_sellback_ref_value(1))
        
        reset = get_reset(ins)
        
        if ins.FirstTotalReturnLeg().PriceInterpretationType() == "All In":
            resetval = get_all_in_end_price(ref_ins)
        if ins.FirstTotalReturnLeg().PriceInterpretationType() == "As Reference":
            resetval = 0.0

        if reset and resetval != 0:
            reset.FixingValue(resetval)
            reset.ReadTime(acm.Time().TimeNow())
                
            trade.Commit()
            ref_ins.Commit()
            reset.Commit()
            ins.Commit()
            LOGGER.info("Instrument '%s' has been fixed.", ins.Name())
            
        else:
            raise RuntimeError("Could not find correct reset to fix.")
    else:
        LOGGER.warning("TRS '%s' not fixed because end date is within 2 business days.", ins.Name())


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    val_date = ael_dict['val_date'].to_string("%Y-%m-%d")

    for ins in ael_dict['instruments']:
        try:
            fix_trx_reset(ins, val_date)
        except Exception as exc:
            LOGGER.exception("Instrument not fixed: '%s'", exc)
        
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    if not LOGGER.msg_tracker.warnings_counter:
        LOGGER.info("Completed successfully.")

