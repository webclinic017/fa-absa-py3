""" Compiled: 2013-04-12 13:37:02 """

"""----------------------------------------------------------------------------
MODULE
    FBDPInstrument - Common functions that handle instruments.

    (c) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""


import re

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
                # Cross Currency rates not catered for
                acm_ins = acm.FInstrument[ins.insid]
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                acm_curr = acm.FInstrument[curr.insid]
                p = acm_ins.Calculation().MarketPrice(calcSpace, str(date), 0, acm_curr).Number()
                calcSpace.Clear()
                calcSpace.Delete()
                if p:
                    Logme()('Found cross rate for %s price for %s on %s (%s market):%f'\
                        %(curr.insid, ins.insid, str(date), market.ptyid, p), 'DEBUG')
                    return p
            Logme()('No %s price for %s on %s (%s market)'\
                %(curr.insid, ins.insid, str(date), market.ptyid), 'WARNING')
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
    fixingSource = acm.FAdditionalInfoSpec['Fixing Source']
    if fixingSource:
        mask1 = fixingSource.SubRecMask1()
        mask2 = fixingSource.SubRecMask2()
        enums = []
        for j in range(1, 32):
            if (mask1 & (1<<j-1)):
                enums.append(ael.enum_to_string('InsType', j))
        for j in range(1, 32):
            if (mask2 & (1<<j)):
                enums.append(ael.enum_to_string('InsType', j + 32))
        i = acm.FInstrument[fixing_source_ins.insid]
        for type_ in enums:
            if i.InsType() == type_:
                if i.AdditionalInfo().Fixing_Source() and i.AdditionalInfo().Fixing_Source().Name():
                    settlement_market = i.AdditionalInfo().Fixing_Source().Name()
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

    if not curr:
        curr = settle_ins.curr
    return find_price(settle_ins, date, curr, settlement_market)




def isExpired(ins, gui_date_time=acm.Time.DateToday(), comb_ins=[]):
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
            return is_comb_ins_expired_at(ins, gui_date_time, comb_ins)


def is_comb_ins_expired_at(ins, valuation_date_time, comb_ins=[]):
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
        comb_ins.append(ins)
        if not ins.InstrumentMaps():
            return False
        # Combination instrument is not expired unless all member instruments
        # are expired.
        for m in ins.InstrumentMaps():
            if (m.Instrument() and m.Instrument() not in comb_ins and
                not isExpired(m.Instrument(), valuation_date_time)):
                    return False
        return True
    else:
        return False


def select_instruments(portfolios=[], is_traded=0, instypes=[],
        not_instypes=[], undtypes=[], instruments=[], markets=[],
        underlyings=[], not_underlyings=[], exp_day=None,
        select_before_exp_day=1, otc=None, settlement=None, ins_list=[],
        aliastypes=[], distributors=[], do_log=0, exclude_generic=1):
    """------------------------------------------------------------------------
    FUNCTION
        select_instruments(...)
    DESCRIPTION
        Returns a sorted list of ael_entity of type instrument that fullfill
        the selection criteria.
    ARGUMENTS
        select_instruments(instypes=[], undtypes=[], instruments=[],
                markets=[], underlyings=[], exp_day=ael_date,
                exp_time='hh:mm:ss' settlement='Cash'/'Physical Delivery',
                ins_list=[], aliastypes=[], distributors=[],
                select_before_exp_day = 0/1)
    RETURNS
        tmp     list of ael_entities of type instrument
    NOTE:
        - instrument, undtypes, underlyings, instypes, aliastypes and
        distributors selects, the rest filters.
        - ins_list means instrument list e.g. DAX.
        - Arguments such as instypes could either be string, list of strings or
        comma separated string e.g. 'Stock',['Stock','Option'],'Stock,Option'
        - The argument 'select_before_exp_day' controls whether instruments
        expiring before or after exp_day should be selected
    ------------------------------------------------------------------------"""
    elements = {}  # insaddr: ael_entity
    if exp_day:
        exp_day = acm.Time.AsDate(exp_day)
    if do_log:
        do_log = int(do_log)  # Remove after checking all scripts
    if otc:
        otc = int(otc)

    class LogRemoved:
        singleton = None

        def __init__(self, elements):
            self.oldLength = len(elements)

        def __call__(self, elements, msg=None):
            removed = self.oldLength - len(elements)
            self.oldLength = len(elements)
            if removed:
                Logme()(('%d instruments removed by ' + msg + ' filtering') %
                        removed, 'DEBUG')

    def logRemoved(elements, msg=None):
        if LogRemoved.singleton:
            LogRemoved.singleton(elements, msg)
        else:
            LogRemoved.singleton = LogRemoved(elements)
            Logme()('%d instruments initially selected' % len(elements),
                    'DEBUG')

    # -----------------------------------------------------------
    # Load the instruments
    # -----------------------------------------------------------
    if not (instypes or instruments or underlyings or aliastypes or
            distributors or undtypes or portfolios):
        all_ins = acm.FInstrument.Select('')
        for i in all_ins:
            # Select All instruments unless criteria above
            elements[i.Oid()] = i
        logRemoved(elements)
    if instruments:
        for ID in instruments:
            i = acm.FInstrument[ID]
            if i:
                elements[i.Oid()] = i
            else:
                Logme()("Instrument %s doesn't exist" % ID, 'DEBUG')
        logRemoved(elements)
    if underlyings:
        if not_underlyings:
            raise Exception("InputError, underlyings and not_underlyings "
                    "cannot both be set")

        tmp = {}  # Will replace elements
        for ID in underlyings:
            und = acm.FInstrument[ID]
            if not instruments or und.Oid() in elements:
                tmp[und.Oid()] = und
            c = ("underlying=%d" % und.Oid())
            for der in acm.FInstrument.Select(c):
                if not instruments or der.Oid() in elements:
                    tmp[der.Oid()] = der
        elements = tmp
        logRemoved(elements, 'underlying')
    if portfolios:
        if instruments or underlyings:
            for oid, i in elements.items():
                for t in i.Trades():
                    if t.Portfolio() and t.Portfolio().Name() in portfolios:
                        break
                else:
                    del elements[oid]
        else:
            for pf in portfolios:
                for i in acm.FPhysicalPortfolio[pf].Instruments():
                    elements[i.Oid()] = i
        logRemoved(elements, 'portfolio')
    if instypes:
        if not_instypes:
            raise Exception("InputError, instypes and not_instypes cannot "
                    "both be set")
        if instruments or underlyings or portfolios:
            for insaddr, i in elements.items():
                if not i.InsType() in instypes:
                    del elements[insaddr]
        else:
            for t in instypes:
                for i in acm.FInstrument.Select('insType="%s"' % t):
                    elements[i.Oid()] = i
        logRemoved(elements, 'instype')
    if undtypes:
        if instruments or underlyings or instypes or portfolios:
            for insaddr, i in elements.items():
                if ((i.Underlying() and
                              i.Underlying().InsType() not in undtypes) or
                     (not i.Underlying().InsType() and
                              i.InsType() not in undtypes)):
                    del elements[insaddr]
        else:
            for undtype in undtypes:
                for und in acm.FInstrument.Select('insType="%s"' % undtype):
                    for der in acm.FInstrument.Select('underlying=%d' %
                            und.Oid()):
                        elements[der.Oid()] = der
        logRemoved(elements, 'undtype')
    if aliastypes:
        if instruments or underlyings or instypes or undtypes or portfolios:
            for insaddr, i in elements.items():
                for a in i.Aliases():
                    try:
                        if a.Type().AliasTypeName() in aliastypes:
                            break
                    except AttributeError:
                        continue
                else:
                    del elements[insaddr]
        else:
            try:
                for at in aliastypes:
                    for iat in acm.FInstrAliasType.Select(
                            "aliasTypeName = '%s'" % at):
                        for a in acm.FInstrumentAlias.Select(
                                "type = '%s'" % iat.Oid()):
                            elements[a.Instrument().Oid()] = a.Instrument()
            except:
                pass
        logRemoved(elements, 'aliastype')
    if distributors:
        if (instruments or underlyings or instypes or undtypes or aliastypes or
                portfolios):
            for insaddr, i in elements.items():
                for pd in acm.FPriceDefinition.Select('instrument=%d' %
                        insaddr):
                    if pd.PriceDistributor().Name() in distributors:
                        break
                else:
                    del elements[insaddr]
        else:
            try:
                for d in distributors:
                    dist = acm.FPriceDistributor[d]
                    for pd in acm.FPriceDefinition.Select(
                            "priceDistributor = %d" % dist.Oid()):
                        elements[pd.Instrument().Oid()] = pd.Instrument()
            except:
                pass
        logRemoved(elements, 'price distributor')

    #-----------------------------------------------------------
    listnodes = {}  # Note: listnodes has no unique id
    if markets:
        # Note: can't use market_ptynbr constraint on ListNode
        for ln in ael.ListNode.select():
            if (ln.market_ptynbr and ln.market_ptynbr.type == 'Market' and
                    ln.market_ptynbr.ptyid in markets):
                listnodes[ln.nodnbr] = None

    if ins_list:
        #Note: can't use market_ptynbr constraint on ListNode
        tmp = {}
        for ln in ael.ListNode.select():
            if ln.id in ins_list or ln.nodnbr in ins_list:
                for child in ln.reference_in():
                    if child.record_type == 'ListNode':
                        listnodes[child.nodnbr] = None
                    elif child.record_type == 'ListLeaf':
                        listnodes[ln.nodnbr] = None
    # ---------------------------------
    # Filter generic and default instruments
    # ---------------------------------
    if exclude_generic:
        for (insaddr, i) in elements.items():
            if i.Generic():
                del elements[insaddr]
        logRemoved(elements, '"generic"')
    for (insaddr, i) in elements.items():
        if re.search('DEFAULT', i.Name(), re.I):
            del elements[insaddr]
    logRemoved(elements, 'default instrument')
    # ---------------------------------
    # Filter on exp_day and exp_time, underlyings are also handled
    # ---------------------------------
    if exp_day:
        for (insaddr, i) in elements.items():
            if select_before_exp_day:  # select only expired instruments
                if not isExpired(i, exp_day):
                    del elements[insaddr]
            else:  # select only "live" instruments
                if isExpired(i, exp_day):
                    del elements[insaddr]
        logRemoved(elements, 'exp_day')
    if ins_list or markets:
        filters = [(listnodes, ael.ListNode, ['ListLeaf', 'OrderBook'],
                'Listnodes/Pages')]

        for (values, ael_table, record_types, logging) in filters:
            flt = {}  # of insaddr numbers
            for v in values.keys():
                Logme()("+ process %s: %s" % (logging, ael_table[v].id),
                        'DEBUG')
                for e in ael_table[v].reference_in():
                    if e.record_type in record_types:
                        # ! Works for many record_types:
                        try:
                            flt[e.insaddr.insaddr] = None
                        except:
                            pass
            for insaddr in elements.keys():
                if insaddr not in flt:
                    del elements[insaddr]
        logRemoved(elements, logging)
    # ---------------------------------
    # Filter on otc 0/1
    # ---------------------------------
    if otc != None:
        for (insaddr, i) in elements.items():
            if i.Otc() != otc:
                del elements[insaddr]
        logRemoved(elements, 'otc')
    # ---------------------------------
    # Filter on settlement
    # ---------------------------------
    if settlement != None:
        for (insaddr, i) in elements.items():
            if i.SettlementType() != settlement:
                del elements[insaddr]
        logRemoved(elements, 'cash/physical delivery')
    # ---------------------------------
    # Filter on not_underlyings etc.
    # ---------------------------------
    if not_underlyings:
        for (insaddr, i) in elements.items():
            if ((i.Underlying() and i.Underlying().Name() in not_underlyings)
                    or i.Name() in not_underlyings):
                del elements[insaddr]
        logRemoved(elements, 'underlying')

    if not_instypes:
        for (insaddr, i) in elements.items():
            if (i.InsType() in not_instypes):
                del elements[insaddr]
        logRemoved(elements, 'instype')
    if is_traded:
        for (insaddr, i) in elements.items():
            if not i.Trades():
                del elements[insaddr]
        logRemoved(elements, '"not traded"')
    Logme()("Number of selected instruments: %d" % len(elements), 'DEBUG')
    tmp = [(i.Name(), i) for i in elements.values()]
    tmp.sort()
    return [i[1] for i in tmp]


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
