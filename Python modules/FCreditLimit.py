"""
Purpose                 :Amended the calc_credit_util_cp method
                         which was throwing an error on redemption amount
                         when it was the first trade on an instrument
                         Changed in such a way
                         that if redemption amount fails,
                         that we return the trade nominal
                         to do the credit limit check against
Department and Desk     :FO
Requester:              :Maralize Knoetze
Developer               :Anwar Banoo
CR Number               :315007


History
=======

2013-04-29 Phumzile Mgcima  CR984724: Add logic to pull balance given trade and date instead of Redemption amount
2015-02-13 Peter Basista    FA-Upgrade-2014: Add some new functions which will be used for refactored deposit balance calculation
2016-03-14 Vojtech Sidorin  ABITFA-4121: Move logic to get_credit_limit; improve coding style.
2016-04-11 Vojtech Sidorin  ABITFA-4237: Fix function limit_cp: Return 0 if credit limit is not set.
2016-05-11 Vojtech Sidorin  ABITFA-4291: get_credit_limits: Return zero limits if none are set at the Funding Desk.
2017/06/15 Bhavnisha Sarawan ABITFA-4942: Production issue: Credit Limits columns. Changed columns to look at both counterparty and acquirer.
2017/06/15 Bhavnisha Sarawan No Jira: Production issue: Add acquirer parameter for the asql function.
"""

import acm
import ael
import zak_funcs


def calc_credit_util_cp(trade, date=None):
    ret = 0

    if trade.insaddr.instype == 'Deposit':
        if trade.status not in ('Simulated', 'Void', 'Terminated'):
            if trade.acquirer_ptynbr:
            #if trade.acquirer_ptynbr.ptyid == 'Funding Desk':
                if trade.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                    if trade.add_info('Funding Instype') in ('Call Loan DTI', 'Call Loan NonDTI'):
                        #Anwar
                        #MM issue when booking a call loan on a new account - redemption amount throwing range errors
                        #allowing default nominal amount to return as fix for this issue but to keep the credit limit check intact
                        try:
                            if date:
                                ret = zak_funcs.Balance(trade, date)
                            else:
                                ret = zak_funcs.Balance(trade)
                        except Exception, e:
                            print e
                            ret = trade.nominal_amount()
                else:
                    if trade.insaddr.exp_day > ael.date_today():
                        if trade.add_info('Funding Instype') in ('FLI', 'FTL'):
                            ret = trade.nominal_amount()                       
    ret = max(ret, 0)
    return ret

def limit_cp_asql(party, *rest):
    return limit_cp(party)


def get_credit_limits(party, department=None):
    """Return credit limits for party.

    If department is set, get only credit limits with this department.

    If department is Funding Desk (ptynbr: 2247) and the Party has not set any
    credit limit, return zero credit limits (empty credit limits ael object).

    Returns:
        List of CreditLimit entities.
    """
    funding_desk = ael.Party[2247]  # Funding Desk
    credit_limits = None
    if party.group_limit:
        if party.parent_ptynbr: # not a parent
            credit_limits = ael.CreditLimit.select('ptynbr=%d' %party.parent_ptynbr.ptynbr)
        else:
            credit_limits = ael.CreditLimit.select('ptynbr=%d' %party.ptynbr)
    else:
        credit_limits = ael.CreditLimit.select('ptynbr=%d' % party.ptynbr)
    if department is not None:
        credit_limits = [cl for cl in credit_limits if cl.depnbr is department]
    # At the Funding Desk, return zero (empty) credit limits if not set.
    if department is funding_desk and not credit_limits:
        credit_limits = [ael.CreditLimit.new()]
    return credit_limits


def limit_cp(party, department=None):
    if department:
        desk = department
    else:
        desk = ael.Party['Funding Desk']
    credit_limits = get_credit_limits(party, desk)
    if credit_limits:
        if len(credit_limits) == 1:
            credit_limit = credit_limits[0]
            return getattr(credit_limit, "limit[0]", 0)
        else:
            for credit_limit in credit_limits:
                if credit_limit.depnbr and credit_limit.depnbr is desk:
                    return getattr(credit_limit, "limit[0]", 0)
    return 0


def credit_tot_cp_asql(party, acquirer,date=None, *rest):
    return credit_tot_cp(party, acquirer, date)

def credit_tot_cp(party, acquirer, date=None):
    tot = 0
    flag = 0
    if party.group_limit:
        if party.parent_ptynbr: # not a parent
            flag = 1
        else:
            flag = 2
    if flag == 0:
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.ptynbr))
        for x in tradesA:
            if x.status not in ('Simulated', 'Void', 'Terminated') and x.insaddr.instype == 'Deposit':
                if x.acquirer_ptynbr.ptyid == acquirer.ptyid:
                    cc = calc_credit_util_cp(x, date)
                    tot = tot + cc
    elif flag == 1: #child
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.parent_ptynbr.ptynbr))
        for x in tradesA:
            if x.status not in ('Simulated', 'Void', 'Terminated') and x.insaddr.instype == 'Deposit':
                if x.acquirer_ptynbr == acquirer.ptynbr:
                    cc = calc_credit_util_cp(x, date)
                    tot = tot + cc
            for p in ael.Party.select('parent_ptynbr =' + str(party.parent_ptynbr.ptynbr)):
                tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(p.ptynbr))
                for x in tradesA:
                    if x.status not in ('Simulated', 'Void', 'Terminated') and x.insaddr.instype == 'Deposit':
                        if x.acquirer_ptynbr == acquirer.ptynbr:
                            cc = calc_credit_util_cp(x, date)
                            tot = tot + cc
    else: #parent
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.ptynbr))
        for x in tradesA:
            if x.status not in ('Simulated', 'Void', 'Terminated') and x.insaddr.instype == 'Deposit':
                if x.acquirer_ptynbr == acquirer.ptynbr:
                    cc = calc_credit_util_cp(x, date)
                    tot = tot + cc
        for p in ael.Party.select('parent_ptynbr =' + str(party.ptynbr)):
            tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(p.ptynbr))
            for x in tradesA:
                if x.status not in ('Simulated', 'Void', 'Terminated') and x.insaddr.instype == 'Deposit':
                    if x.acquirer_ptynbr == acquirer.ptynbr:
                        cc = calc_credit_util_cp(x, date)
                        tot = tot + cc
    return tot

def calc_credit_rem_cp(party, acquirer, date=None):
    lim = limit_cp(party)
    util = credit_tot_cp(party, acquirer, date)
    alimit = lim - util
    return alimit



def credit_tot_cp_A(trade):
    tot = 0
    flaga = 0
    alimit = 1
    flag = 0
    party = trade.counterparty_ptynbr
    lim = limit_cp(party, trade.acquirer_ptynbr)
    if party.group_limit:
        if trade.counterparty_ptynbr.parent_ptynbr: # not a parent
            #cls = ael.CreditLimit.select('ptynbr=%d' %party.parent_ptynbr.ptynbr)
            flag = 1
        else:
            #cls = ael.CreditLimit.select('ptynbr=%d' %party.ptynbr)
            flag = 2
    #else:
    #    cls = ael.CreditLimit.select('ptynbr=%d' % party.ptynbr)

    if flag == 0:
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.ptynbr))
        for x in tradesA:
            if x.acquirer_ptynbr == trade.acquirer_ptynbr:
                if x.status not in ('Simulated', 'Void', 'Terminated'):
                    cc = calc_credit_util_cp(x)
                    tot = tot + cc
                if x.trdnbr == trade.trdnbr:
                    flaga = 1
    elif flag == 1: #child
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.parent_ptynbr.ptynbr))
        for x in tradesA:
            if x.acquirer_ptynbr == trade.acquirer_ptynbr:
                if x.status not in ('Simulated', 'Void', 'Terminated'):
                    cc = calc_credit_util_cp(x)
                    tot = tot + cc
        for p in ael.Party.select('parent_ptynbr =' + str(party.parent_ptynbr.ptynbr)):
            tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(p.ptynbr))
            for x in tradesA:
                if x.acquirer_ptynbr == trade.acquirer_ptynbr:
                    if x.status not in ('Simulated', 'Void', 'Terminated'):
                        cc = calc_credit_util_cp(x)
                        tot = tot + cc
                    if x.trdnbr == trade.trdnbr:
                        flaga = 1
    else: #parent
        tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(party.ptynbr))
        for x in tradesA:
            if x.acquirer_ptynbr == trade.acquirer_ptynbr:
                if x.status not in ('Simulated', 'Void', 'Terminated'):
                    cc = calc_credit_util_cp(x)
                    tot = tot + cc
                if x.trdnbr == trade.trdnbr:
                    flaga = 1
        for p in ael.Party.select('parent_ptynbr =' + str(party.ptynbr)):
            tradesA = ael.Trade.select('counterparty_ptynbr = ' + str(p.ptynbr))
            for x in tradesA:
                if x.acquirer_ptynbr == trade.acquirer_ptynbr:
                    if x.status not in ('Simulated', 'Void', 'Terminated'):
                        cc = calc_credit_util_cp(x)
                        tot = tot + cc
    if flaga == 0:
        cc = calc_credit_util_cp(trade)
        tot = tot + cc
    alimit = lim - tot
    return alimit


def _get_relevant_cashflows(acm_leg, date_string):
    """
    Return all the cashflows of types "Fixed Amount" or
    "Interest Reinvestment" on the provided leg,
    whose pay day is strictly before or exactly the same as the provided date.
    """
    allowed_cashflow_types = ["Fixed Amount", "Interest Reinvestment"]
    cashflows = []
    for allowed_cashflow_type in allowed_cashflow_types:
        cashflows.extend(list(acm.FCashFlow.Select(
            "leg={0} and cashFlowType='{1}'".format(acm_leg.Oid(),
                                                    allowed_cashflow_type))))

    filtered_cashflows = [cf for cf in cashflows
                          # cf.PayDate() is a string
                          if acm.Time.DateDifference(date_string,
                                                     cf.PayDate()) >= 0]
    return filtered_cashflows


def get_deposit_balance(acm_instrument, date_string=None):
    """
    Return the balance of the provided deposit instrument
    which is valid for the provided date.
    """
    legs = acm_instrument.Legs()
    if len(legs) != 1:
        message = ("The provided instrument '{0}' "
                   "does not have exactly one leg!").format(
                       acm_instrument.Name())
        raise RuntimeError(message)
    acm_leg = legs[0]

    if date_string is None:
        date_string = acm.Time.DateToday()

    relevant_cashflows = _get_relevant_cashflows(acm_leg, date_string)
    instrument_balance = sum([cf.FixedAmount() for cf in relevant_cashflows])

    return instrument_balance
