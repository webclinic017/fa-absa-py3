""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPInstrument.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FBDPInstrument - Common functions that handle instruments.

----------------------------------------------------------------------------"""


import acm
import ael


import ArenaFunctionBridge
import FBDPCommon
from FBDPCurrentContext import Logme


def find_price(ins, date=str(ael.date_today()), curr=None,
        settlement_market=None):
    """------------------------------------------------------------------------
    FUNCTION
        find_price(ins,
                   date=str(ael.date_today()),
                   curr=None,
                   settlement_market=None)
    DESCRIPTION
        This function will return a settlement price for an instrument that is
        passed to the function. The function will look for a price for the
        specified instrument in the specified currency on the specified date.
        A settlement market can be specified for which the function will look
        for a price.
    ARGUMENTS
        ins               ael_entity         instrument
        date              ael_date or string date
        curr              ael_entity         instrument
        settlement_market string             The name of the settlement market
    ------------------------------------------------------------------------"""
    price = 0.0
    delimiter = "*" * 40
    if not curr:
        curr = ins.curr
    Logme()(delimiter, "DEBUG")
    Logme()("Finding settlement price for instrument %s" % ins.insid, "DEBUG")
    if settlement_market:
        market = ael.Party[settlement_market]
        if market:
            p = ael.Price.read('\
                insaddr=%d and\
                day="%s" and\
                curr=%d and\
                ptynbr=%d'
                % (ins.insaddr, str(date), curr.insaddr, market.ptynbr))
            if p:
                price = p.settle
                Logme()('Found %s price for %s on %s (%s market):%f'
                        % (curr.insid, ins.insid, str(date), market.ptyid,
                        price), "DEBUG")
                if not (p.bits & 256):
                    Logme()('Settle bit in %s for %s is zero on %s.' % (
                        curr.insid, ins.insid, str(date)), "DEBUG")
                Logme()(delimiter, "DEBUG")
                return price
            #Need to check both ways in market for Currency derivatives.
            if p == None and ins.instype == 'Curr':
                Logme()('Looking the other way around', "DEBUG")
                p = ael.Price.read('insaddr=%d and day="%s" and curr=%d and '
                        'ptynbr=%d' % (curr.insaddr, str(date), ins.insaddr,
                        market.ptynbr))
                if p:
                    if not (p.bits & 256):
                        Logme()('Settle bit in %s for %s is zero on %s.' % (
                            curr.insid, ins.insid, str(date)), "DEBUG")
                        return p.settle
                    price = 1 / p.settle  # Found price needs to be inverted
                    Logme()('Found %s price for %s on %s (%s market):%f' % (
                            curr.insid, ins.insid, str(date), market.ptyid,
                            price))
                    Logme()(delimiter, "DEBUG")
                    return price
            Logme()('No %s price for %s on %s (%s market)'\
                % (curr.insid, ins.insid, str(date), market.ptyid), 'WARNING')
        else:
            Logme()('The Market %s does not exist' % settlement_market)

    date = ael.date(str(date))
    price = ArenaFunctionBridge.instrument_mtm_price(ins.insid, date,
            curr.insid)
    if price:
        Logme()('Found mtm price:%f for %s on %s in %s.' % (price, ins.insid,
                date, curr.insid), "DEBUG")
        Logme()(delimiter, "DEBUG")
        return price
    if ael.date(str(date)) == ael.date_today():
        price = ArenaFunctionBridge.instrument_used_price(ins.insid, date,
                curr.insid)
        if price:
            Logme()('Found used price:%f for %s on %s in %s.' % (price,
                    ins.insid, date, curr.insid), "DEBUG")
            Logme()(delimiter, "DEBUG")
            return price
    Logme()('No nonzero price found for %s on %s in %s.' % (ins.insid, date,
            curr.insid), 'WARNING')
    Logme()(delimiter, "DEBUG")
    return price

#----------------------------------------------------
# find_settle_price() when FixingSource field is set
#----------------------------------------------------


def find_settle_price(fixing_source_ins, settle_ins,
        date=str(ael.date_today()), curr=None, settlement_market=None):
    """------------------------------------------------------------------------
    FUNCTION
        find_settle_price(fixing_source_ins,
                   settle_ins,
                   date=str(ael.date_today()),
                   curr=None,
                   settlement_market=None)
    DESCRIPTION
        This function will return a settlement price for the settle instrument
        that is passed to the function. The function will look for a price for
        the specified settle instrument in the specified currency on the
        specified date.  If a fixing source exists for the fixing source
        instrument, then it will be used to look for the price, else if a
        settlement market is specified, then it will be used to look for the
        price.
    ARGUMENTS
        fixing_source_ins ael_entity         instrument
        settle_ins        ael_entity         instrument
        date              ael_date or string date
        curr              ael_entity         instrument
        settlement_market string             The name of the settlement market
    ------------------------------------------------------------------------"""
    #NDF
    if (settle_ins.instype == 'Future/Forward' and
            settle_ins.und_instype == 'Curr' and
            settle_ins.paytype == 'Forward' and
            settle_ins.settlement == 'Cash'):
        if settle_ins.quotation_seqnbr.name == 'Per Unit Inverse':  # inverse
            curr = settle_ins.und_insaddr
            settle_ins = settle_ins.curr
        elif settle_ins.quotation_seqnbr.name == 'Per Unit':  # per unit
            curr = settle_ins.curr
            settle_ins = settle_ins.und_insaddr

    if fixing_source_ins.fixing_source_ptynbr:
        settlement_market = fixing_source_ins.fixing_source_ptynbr.ptyid

    if not curr:
        curr = settle_ins.curr
    return find_price(settle_ins, date, curr, settlement_market)


def isExpired(ins, gui_date_time=acm.Time.DateToday()):
    """
    Is the instrument considered expired at the given date.

    Note an extra time gap is added when comparing the instrument's expiry date
    to the given date.  This is to prevent immediate removal of the instrument
    definition or the instrument's prices.
    """
    if not ins.Generic():
        if ins.ExpiryDate():
            # Open ended instruments not to be expired unless Terminated
            if ins.OpenEnd() == 'Open End':
                return False
            if (acm.Time.AsDate(ins.ExpiryDate()) >=
                    acm.Time.DateAddDelta(gui_date_time, 0, 0, 1)):
                return False
            if gui_date_time == gui_date_time[:10]:
                gui_date_time += " 23:59:59"
            return ins.ExpiryDate() <= gui_date_time
        else:
            # Special consideration for combination if no expiry date.
            return is_comb_ins_expired_at(ins, gui_date_time)


def is_comb_ins_expired_at(ins, valuation_date_time):
    """
    Helper function to check if the given combination instrument is expired at
    the given date time.  Return false for non combination instrument.

    Note, this function mimic the behaviour of FCombination.isExpired().
    However, FInstrument.isExpiredAt() on the member instrument is not used.
    The isExpired() function defined in this file is invoked instead.  It takes
    extra consideration on preventing the removal of instrument definition or
    prices immediately after it expired.
    """
    if ins.InsType() == 'Combination':
        # Combination instrument without member instrument is not considered
        # expired.
        if not ins.InstrumentMaps():
            return False
        # Combination instrument is not expired unless all member instruments
        # are expired.
        for m in ins.InstrumentMaps():
            if m.Instrument() and \
               not isExpired(m.Instrument(), valuation_date_time):
                return False
        return True
    else:
        return False


def isTradable(ins):
    """------------------------------------------------------------------------
    Function
        isTradable(ins)
    DESCRIPTION
        returns True if the instrument is tradable and False if it isn't
    ARGUMENTS
        ins, an instrument object (ael)
    ---------------------------------------------------------------------------
    """
    isACM = FBDPCommon.is_acm_object(ins)
    if not isACM:
        return isTradableAEL(ins)

    if ins.Notional():
        Logme()('Cannot have trade in notional instrument', 'DEBUG')
        return False
    if ins.Generic():
        Logme()('Cannot have trade in generic instrument', 'WARNING')
        return False
    strike_type = ('StrikeType' in dir(ins) and ins.StrikeType() or "")
    if 'Rel' in strike_type:
        Logme()('Cannot have trade in relative strike instrument', 'WARNING')
        return False
    return True


def isTradableAEL(ins):
    if ins.notional:
        Logme()('Cannot have trade in notional instrument', 'DEBUG')
        return False
    if ins.generic:
        Logme()('Cannot have trade in generic instrument', 'WARNING')
        return False
    strike_type = ins.strike_type
    if 'Rel' in strike_type:
        Logme()('Cannot have trade in relative strike instrument', 'WARNING')
        return False
    return True
