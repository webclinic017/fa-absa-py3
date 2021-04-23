"""Deprecated FValidation module.

This module contains rules that have not (yet) been fully refactored
and integrated into the new FValidation modules.  No new rules should
be added to this module, only hotfixes if necessary.
"""

# Lukas Paluzga  CHNG0001240250    Sets price for FX Options.
#                                  Computes delivery date for USD/ZAR trades so it get the same values as if booked using Front GUI.
#                                  Front Arena and PACE check only T+2 for US holidays. Acm checks even T+1 for calculating delivery date.
# Lukas Paluzga  CHNG0001263369    Changed TRADESERVICE_USERS
# Jan Sinkora    CHNG0001629939    trade_nominal doesn't work, replaced with contract_size * quantity
# Vojtech Sidorin CHNG0002210109   Mark as deprecated module 
# 2015-08-20 Vojtech Sidorin       ABITFA-3743: Include rule numbers in messages.

import ael, acm

from FValidation_core import (ValidationError,
                              validate_entity, validate_transaction)

zarcal = ael.Calendar['ZAR Johannesburg']
usdcal = ael.Calendar['USD New York']

TRADESERVICE_USERS = ['MMG_TRD_TST', 'MMG_TRD_PRD']

def days_bw(d1, d2, cal):
    """Calculate banking days between two dates using specified calendar."""
    # The way AEL calculates bankingdays_between is just plain odd
    count = 0
    while d1 < d2:
        if d2.is_banking_day(cal):
            count += 1
        d2 = d2.add_days(-1)

    return count

def usdzar_pd_offset(exp_day):
    """Calculate payday offset for USD/ZAR trades."""
    # If the expiry is on a weekend the pay day offset should be 0
    if exp_day.day_of_week() in (6, 7):
        return 0

    # Always use 2 banking days for ZAR side
    dd = exp_day.add_banking_day(zarcal, 2)

    # Increment days until banking day is found for both sides
    while not (dd.is_banking_day(zarcal) and dd.is_banking_day(usdcal)):
        dd = dd.add_days(1)

    # Return number of banking days USD-side (we know that for ZAR side it's always >= 2)
    # For SA holidays we may get 3 (or more) banking days for US side. Normalize to 2.
    return min(days_bw(exp_day, dd, usdcal), 2)

def is_pfxo_option(trade):
    ins = trade.insaddr

    # Using only for PaceFXO booked FX Options. We cannot use directly System Source as it's saved later by TS.
    return ins.instype == 'Option' and ins.und_instype == 'Curr' and trade.optional_key.startswith('PFXO') and ael.user().userid in TRADESERVICE_USERS

def get_currpair(trade):
    """Return FX Option currency pair (curr_trd, curr_fxbase)"""
    ins = trade.insaddr

    curr_trd = trade.curr.insid

    if ins.strike_curr.insid != curr_trd:
        curr_fxbase = ins.strike_curr.insid
    elif ins.und_insaddr.insid != curr_trd:
        curr_fxbase = ins.und_insaddr.insid
    else:
        raise Exception('ERROR: The Strike and Underlying Currency is the same as the Trade Currency : %s.' %curr_trd)

    return (curr_trd, curr_fxbase)

# Rule 96
@validate_entity("Trade", "Insert", caller="validate_transaction")
def fv_update_usdzar_pd_offset(trade, op):
    """Update delivery day for Pace FX Options booked USD/ZAR deals so that USD holidays on T+1 are ignored."""
    if not is_pfxo_option(trade):
        return

    if get_currpair(trade) != ('ZAR', 'USD'):
        return

    ins = trade.insaddr.clone()
    old_pdo = ins.pay_day_offset
    ins.pay_day_offset = usdzar_pd_offset(ins.exp_day)
    ael.log('FV96: Setting new payday offset for instrument {0}: from {1} to {2}'.format(ins.insid, old_pdo, ins.pay_day_offset))

    return [(ins, 'Update')]
    #ins.commit()

# Rule 97
@validate_entity("Trade", "Insert")
def fv_update_price(trade, op):
    """Update price for Pace FX Options booked options"""
    ins = trade.insaddr

    if not is_pfxo_option(trade):
        return

    if not trade.curr:
        raise Exception('FV97-1: ERROR: Trade currency is not set.')

    curr_trd, curr_fxbase = get_currpair(trade)

    currpair = acm.FCurrencyPair[curr_trd + '/' + curr_fxbase] or acm.FCurrencyPair[curr_fxbase + '/' + curr_trd]
    if not currpair:
        raise Exception('FV97-2: ERROR: Could not find the currency pair for currencies %s and %s to set the price of the FX Option.' %(curr_trd, curr_fxbase))

    trade.price = -1 * trade.premium / (trade.quantity * ins.contr_size) / currpair.PointValue()
