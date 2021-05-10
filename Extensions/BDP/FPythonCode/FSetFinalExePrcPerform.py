""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FSetFinalExePrcPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FSetFinalExePrcPerform - Module that executes FSetFinalExercisePrices.

DESCRIPTION
----------------------------------------------------------------------------"""


import ael


import FBDPCommon
import FExeAssPerform
from FBDPCurrentContext import Logme


INSTYPE_ENUM_OPTION = ael.enum_from_string('InsType', 'Option')
INSTYPE_ENUM_WARRANT = ael.enum_from_string('InsType', 'Warrant')
INSTYPE_ENUM_FUTURE_FORWARD = ael.enum_from_string('InsType', 'Future/Forward')


SETTLEMENT_TYPE_ENUM_CASH = ael.enum_from_string('SettlementType', 'Cash')


TRADE_TYPE_ENUM_ASSIGN = ael.enum_from_string('TradeType', 'Assign')
TRADE_TYPE_ENUM_CLOSING = ael.enum_from_string('TradeType', 'Closing')
TRADE_TYPE_ENUM_EXERCISE = ael.enum_from_string('TradeType', 'Exercise')


def _getCandidateTradeQuery(strIsoExeDateMinus1, strIsoExeDatePlus2):
    """
    Note: Using the range [exeDate-1, exeDate+2) so that the trade on the
    exeDate with time zone adjustment would be captured.
    """
    tradeTimeCriteria = (
            't.time >= \'{0}\' AND t.time < \'{1}\''.format(
                    strIsoExeDateMinus1, strIsoExeDatePlus2))
    optWrnInsOidsCriteria = (
            'SELECT owi.insaddr '
            'FROM instrument owi '
            'WHERE owi.instype IN ({0}, {1})'.format(
                    INSTYPE_ENUM_OPTION,
                    INSTYPE_ENUM_WARRANT))
    tradeTypeExeAssCriteria = (
            't.type IN ({0}, {1}) AND '
            't.insaddr IN ({2})'.format(
                    TRADE_TYPE_ENUM_EXERCISE,
                    TRADE_TYPE_ENUM_ASSIGN,
                    optWrnInsOidsCriteria))
    cshStlFutFwdInsOidsCriteria = (
            'SELECT ffi.insaddr '
            'FROM instrument ffi '
            'WHERE ffi.instype = {0} AND ffi.settlement = {1}'.format(
                    INSTYPE_ENUM_FUTURE_FORWARD,
                    SETTLEMENT_TYPE_ENUM_CASH))
    tradeTypeClsCriteria = (
            't.type = {0} '
            'AND t.insaddr IN ({1})'.format(
                    TRADE_TYPE_ENUM_CLOSING,
                    cshStlFutFwdInsOidsCriteria)
            )
    candTrdOidQry = (
            'SELECT t.trdnbr '
            'FROM trade t '
            'WHERE ({tradeTimeCriteria}) '
                    'AND (({tradeTypeExeAssCriteria}) '
                            'OR ({tradeTypeClsCriteria}) '
                    ')'.format(
            tradeTimeCriteria=tradeTimeCriteria,
            tradeTypeExeAssCriteria=tradeTypeExeAssCriteria,
            tradeTypeClsCriteria=tradeTypeClsCriteria))
    return candTrdOidQry


def get_trades(strExeDate):

    # Find the candidate trade time boundary.  Use the range
    # [exeDate-1, exeDate+2) to accommodate possible shift in the time zone.
    aelExeDate = ael.date(strExeDate)
    aelExeDateMinus1 = aelExeDate.add_delta(
            -1,  # days
            0,   # months
            0)   # years
    aelExeDatePlus2 = aelExeDate.add_delta(
            +2,  # days
            0,   # months
            0)   # years
    strIsoExeDateMinus1 = aelExeDateMinus1.to_string(ael.DATE_ISO)
    strIsoExeDatePlus2 = aelExeDatePlus2.to_string(ael.DATE_ISO)
    # Get the candidate trade via dbsql
    candTrdOidQry = _getCandidateTradeQuery(strIsoExeDateMinus1,
            strIsoExeDatePlus2)
    tradeOidList = [row[0] for row in ael.dbsql(candTrdOidQry)[0]]
    candAelTrdList = [ael.Trade[trdOid] for trdOid in tradeOidList]
    # Final filtering, keep only the trade on the date.
    aelExeTrdList = []
    for aelTrd in candAelTrdList:
        if ael.date_from_time(aelTrd.time) == aelExeDate:
            aelExeTrdList.append(aelTrd)
            msg = ('Will update trade {0} in {1}.'.format(aelTrd.trdnbr,
                    aelTrd.insaddr.insid))
            Logme()(msg)
    return aelExeTrdList


def get_physical_trade(t_exer):
    """
    Find the physical delivery trade corresponding to the exercise trade
    """
    if not t_exer.insaddr.und_insaddr:
        return None
    ins = ael.Instrument.read('insaddr={0}'.format(t_exer.insaddr.insaddr))
    is_strike_quotation_different = 0
    if (ins.und_insaddr.quotation_seqnbr and ins.strike_quotation_seqnbr and
            ins.strike_quotation_seqnbr != ins.und_insaddr.quotation_seqnbr):
        is_strike_quotation_different = 1

    und = ael.Instrument.read('insaddr={0}'.format(
            t_exer.insaddr.und_insaddr.insaddr))
    pr_trades = ael.Trade.select('contract_trdnbr={0}'.format(
            t_exer.contract_trdnbr))
    for t in pr_trades:
        if t.insaddr.insaddr == und.insaddr:
            return t
        elif (is_strike_quotation_different and t.curr.insaddr == und.insaddr):
            return t


def update_exercise_payment(t_exer, settle, mode, TestMode):
    """
    Update the payment of type Exercise Cash or create it if it doesn't exist
    """
    found = 0
    excess_lots = t_exer.insaddr.contr_size - t_exer.insaddr.phys_contr_size

    if t_exer.insaddr.instype == 'Option':
        strike_price = FExeAssPerform.convert_price_to_und_or_strike_quotation(
                t_exer.insaddr, t_exer.insaddr.strike_price, 1)
        if t_exer.insaddr.call_option == 1:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr,
                          settle - strike_price)
        else:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr,
                          strike_price - settle)
    else:
        trade_price = settle

    premium = FExeAssPerform.trade_premium_from_quote(t_exer.trdnbr,
            trade_price, t_exer.acquire_day)
    new_amount = premium * excess_lots / t_exer.insaddr.contr_size
    payments = ael.Payment.select('trdnbr={0}'.format(t_exer.trdnbr))

    for p in payments:

        if (p.type == 'Exercise Cash' and mode == 'Strike'):
            found = 1
            payment_clone = p.clone()
            payment_clone.amount = new_amount
            if not TestMode:
                payment_clone.commit()

    t_exer_clone = t_exer.clone()
    payments_clone = t_exer_clone.payments()

    for p in payments_clone:
        if (p.type == 'Exercise Cash' and mode == 'Market'):
            found = 1
            p.delete()

    if not TestMode:
        t_exer_clone.commit()

    if not found and mode == 'Strike':
        t_exer_clone = t_exer.clone()
        new_payment = ael.Payment.new(t_exer_clone)
        new_payment.ptynbr = t_exer.counterparty_ptynbr
        new_payment.type = 'Exercise Cash'
        new_payment.amount = new_amount
        new_payment.curr = t_exer.insaddr.curr
        new_payment.payday = FExeAssPerform.trade_spot_date(t_exer.trdnbr,
                ael.date_from_time(t_exer.time))
    if not TestMode:
        t_exer_clone.commit()


def set_final_settle_prices(pr_trades, exer_date, mode, TestMode):
    """------------------------------------------------------------------------
    FUNCTION
        set_final_settle_prices(pr_trades, exer_date, mode)

    DESCRIPTION
        Sets the final settlement price in all exercising derivatives trades,
        and potential corresponding physical delivery trades, done on the
        specified date.

        Cash settled instruments: Read the price on the SETTLEMENT market
        first. If there is no such price, read the settle price from the
        market on which the trade was done. Set the price of the closing
        derivative trade to the difference between the settle price and the
        strike and change the premium accordingly.

        Physical settled instruments: Either the physical trade is done to
        market, in which case the exercise trade should carry the difference
        between strike and the settlement price, or the physical trade is done
        to the strike in which case the exercise trade should get the price
        and premium zero.

    ARGUMENTS
        The function takes the following arguments:
        1) trades - The Exercise trades found in get_trades().
        2) exer_date - Only Exercised trades done on this date are handled,
           i.e. the trade time of the trade with type Exercise, Assign or
           Abandon should equal this date. The settlement prices should also
           have been entered on this date.
        3) mode - This could either be set to Strike or to Market. This
           depends on whether the physical delivery trade is done to the
           strike price or to market price.
    ------------------------------------------------------------------------"""

    if not pr_trades:
        msg = ('No Exercise/Assign trades made on date {0}'.format(exer_date))
        Logme()(msg, 'WARNING')
        return

    for t in pr_trades:
        ins = t.insaddr
        settle_price = FExeAssPerform.getSettlePriceFromMarket(ins, exer_date,
                "SETTLEMENT")
        if not settle_price:
            msg = ('Will skip trade {0} since there is no price for this '
                     'instrument {1}.'.format(t.trdnbr, ins.insid))
            Logme()(msg)
            continue

        strike_price = FExeAssPerform.convert_price_to_und_or_strike_quotation(
                ins, ins.strike_price, 1)

        if ins.settlement == 'Cash':
            if ins.call_option:
                p_der = FBDPCommon.create_quotetype_price(ins,
                        settle_price - strike_price)
            elif ins.instype == 'Future/Forward':
                p_der = settle_price
            else:
                p_der = FBDPCommon.create_quotetype_price(ins,
                        strike_price - settle_price)

        else:  # Physical settlement
            p_phys = 0.0  # price to be set in the physical trade
            t_phys = get_physical_trade(t)
            if not t_phys:
                Logme()('Physical settlement trade does not exist for trade '
                        '{0}.'.format(t.trdnbr))
                continue
            if mode == 'Market':
                p_phys = settle_price
                if ins.instype == 'Option':
                    p_phys = settle_price
                    if ins.call_option:
                        p_der = FBDPCommon.create_quotetype_price(ins,
                                settle_price - strike_price)
                    else:
                        p_der = FBDPCommon.create_quotetype_price(ins,
                                strike_price - settle_price)
                else:  # Future
                    p_der = settle_price

            else:  # Physical is done to the strike price (Strike mode)
                p_der = 0.0
                if ins.instype == 'Option':
                    p_phys = ins.strike_price
                else:  # Future
                    p_phys = settle_price

                if (abs(ins.phys_contr_size) > 0.000001 and
                        abs(ins.phys_contr_size - ins.contr_size) > 0.000001):
                    update_exercise_payment(t, settle_price, mode, TestMode)

                phys_clone = t_phys.clone()
                phys_clone.price = p_phys
                if (ins.instype in ['Option', 'Warrant'] and
                        ins.und_instype == 'Curr'):
                    phys_clone.fx_update_non_dealt_amount(p_phys)
                else:
                    phys_clone.premium = (FExeAssPerform.
                            trade_premium_from_quote(phys_clone.trdnbr, p_phys,
                            phys_clone.acquire_day))
                if not TestMode:
                    phys_clone.commit()

        der_clone = t.clone()
        der_clone.price = p_der
        der_clone.premium = FExeAssPerform.trade_premium_from_quote(
                der_clone.trdnbr, p_der, t.acquire_day)

        if not TestMode:
            der_clone.commit()
        ael.poll()
