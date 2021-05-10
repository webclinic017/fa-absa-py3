"""
Date                    : 2017-08-31
Purpose                 : This script is required to correctly price Futures on IndexLinkedBonds.
                          It fixes the return leg with the same end price as the equivalent BSB.
                          This script is a result of updated 'SAFI_ILBFutures_Pricing' script,
                          but uses BESA price of Future's underlying.
Department and Desk     : AAM
Requester               : Chris Watts
Developer               : Ondrej Bahounek


Date            Developer               Change
"""


import ael, acm
import aam_tpl
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_price import set_instrument_price


LOGGER = getLogger(__name__)

ael_gui_parameters = {'windowCaption':'AAM: ILBond BESA on futures update'}

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


def get_all_in_end_price(ins):
    i = ael.Instrument[ins.Name()]
    return i.und_insaddr.dirty_from_yield(i.exp_day, None, None, i.ref_price)


def fix_bond_future_price(ins, val_date):

    LOGGER.info("Fixing '%s' for '%s'...", ins.Name(), val_date)
    today = acm.Time().DateToday()
    
    ref_ins = ins.AdditionalInfo().Underlying_BSB()
    LOGGER.info("Underlying BSB: '%s'", ref_ins.Name())
    
    if not ref_ins or ref_ins.InsType() != "BuySellback":
        LOGGER.error("'%s' doesn't have ref instr in Underlying_BSB addinfo", ins.Name())
        return
    
    if ins.FreeText() != "BESA":
        LOGGER.error("Skipping '%s': missing BESA FreeText.", ins.Name())
        return

    ref_cal = ref_ins.Currency().Calendar()
    tPlus3 = ref_cal.AdjustBankingDays(today, 3)

    instr_und = ins.Underlying()
    price = aam_tpl._get_besa_price(instr_und, val_date)
    if not price:
        raise RuntimeError("Missing BESA price for '%s' [%s]" % (instr_und.Name(), val_date))
    
    LOGGER.info("BESA price '%s' [%s]: %f", instr_und.Name(), val_date, price)
    
    curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()
    
    if not curve.IsKindOf(acm.FYCAttribute):
        rate =  ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent().Rate(
            tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365') * 100
    else:
        curve = ref_ins.MappedRepoLink(ref_ins.Currency()).Link().YieldCurveComponent()
        curve = curve.IrCurveInformation(curve.UnderlyingCurve().IrCurveInformation(), today)
        rate =  curve.Rate(tPlus3, ref_ins.ExpiryDateOnly(), 'Simple', 'Act/365', 'Spot Rate') * 100

    trd = ref_ins.Trades().At(0)
    ael_trade = ael.Trade[trd.Oid()]
    
    trd.Price(price)
    ref_ins.Rate(rate)
    ref_ins.StartDate(tPlus3)
    
    ref_ins.RefPrice(ael_trade.buy_sellback_ref_price())
    ref_ins.RefValue(ael_trade.buy_sellback_ref_value(1))
    ref_ins.Commit()

    all_in_price = get_all_in_end_price(ref_ins)
    
    try:
        for market_name in ('SPOT', 'SPOT_MID', 'SPOT_BESA'):
            market = acm.FMarketPlace[market_name]
            set_instrument_price(ins, market, all_in_price, ins.Currency().Name(), val_date)
            LOGGER.info("'%s' price created.", market.Name())
    except:
        LOGGER.error("'%s' price update failed for %s", market.Name(), ins.Name())
        raise


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    val_date = ael_dict['val_date'].to_string("%Y-%m-%d")
    
    for ins in ael_dict['instruments']: 
        try:
            fix_bond_future_price(ins, val_date)
        except Exception as exc:
            LOGGER.exception("Instrument not fixed: '%s'", exc)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    if not LOGGER.msg_tracker.warnings_counter:
        LOGGER.info("Completed successfully.")
