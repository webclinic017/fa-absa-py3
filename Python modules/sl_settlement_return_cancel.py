"""
History
=======
2020-10-06  Faize Adams FAOPS-913: fixed instrument not open ending for revert scenarions.
2020-11-06  Faize Adams FAOPS-948: fixed FreeText1 field not updating when a full return is reverted.
2021-03-01  Faize Adams            Clear Unique_Strate_ID addinfo when reverting collateral trade.
"""
from at_logging import getLogger
from datetime import datetime
import acm
import FSwiftMLUtils

LOGGER = getLogger()


def cancel_return_settlement(settlement):
    cancellation_bpr = None
    cancellation_state_chart = acm.FStateChart['FPTSSettlementCancellation']
    bprs = acm.BusinessProcess.FindBySubjectAndStateChart(settlement, cancellation_state_chart)

    if bprs:
        cancellation_bpr = bprs.Last()

    trade = settlement.Trade()
    original_status = trade.Status()

    if trade.TradeCategory() == "Collateral" and trade.SettleCategoryChlItem():
        settlement_category = trade.SettleCategoryChlItem().Name()
        acquirer = trade.Acquirer().Name()
        if settlement_category == "SL_STRATE" and acquirer == "SECURITY LENDINGS DESK":
            correct_all_collateral_trades(trade)
    else:    
        set_trade_to_void(trade)
        last_trade_in_chain = get_last_trade(trade)
        previous_trade = get_previous_trade(trade)
        if previous_trade.Oid() != trade.Oid():
            next_trade = get_next_trade(trade)
            if last_trade_in_chain.Oid() == trade.Oid() or next_trade.Oid() == trade.Oid():
                if original_status != 'Void':
                    set_trade_to_open_ended(previous_trade)
                canceled_settlement_notification(settlement)
                if cancellation_bpr:
                    FSwiftMLUtils.trigger_event(cancellation_bpr, 'Cancel')
            else:
                if original_status != 'Void':
                    trade_settlement_amount = float(trade.add_info("SL_ReturnedQty"))
                    correct_all_subsequent_secloan_trades_in_chain(next_trade, previous_trade, last_trade_in_chain, trade_settlement_amount)
                failed_settlement_notification(settlement)
                if cancellation_bpr:
                    FSwiftMLUtils.trigger_event(cancellation_bpr, 'Cancel')
        else:
            LOGGER.info("There are no previous trades in the daisy chain which trade {0} could revert to.".format(trade.Oid()))
            if cancellation_bpr:
                FSwiftMLUtils.trigger_event(cancellation_bpr, 'Fail')


def correct_all_collateral_trades(trade):
    LOGGER.info("correcting collateral trade %s" % trade.Oid())
    try:
        if trade.TrxTrade() is None and trade.OptKey1() is None and trade.Text1() == "":
            LOGGER.info("newloan set to void %s" % trade.Oid())
            set_trade_to_void(trade)
        else:
            opposite_leg = get_connected_trade(trade)
            if not (opposite_leg and opposite_leg.Status() == "Void"):
                LOGGER.info("Booking new trade")
                new_trade = book_new_collateral_trade(trade)

                if opposite_leg:
                    LOGGER.info("Booking revert trade for %s" % opposite_leg.Oid())
                    opposite_new_trade = book_new_collateral_trade(opposite_leg)
                    correct_ref = new_trade.Oid()
                    LOGGER.info("Correct contract ref %s" % correct_ref)
                    new_trade.ContractTrade(correct_ref)
                    new_trade.Commit()

                    opposite_new_trade.ContractTrade(correct_ref)
                    opposite_new_trade.Commit()

            prev_trade = trade.TrxTrade()
            if prev_trade:
                LOGGER.info("Previous trade %s" % prev_trade.Oid())
                correct_collateral_full_return(prev_trade)

            set_trade_to_void(trade)
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def book_new_collateral_trade(trade):
    LOGGER.info("Cloning trade %s" % trade.Oid())
    today = datetime.today().strftime("%Y-%m-%d")
    new_trade= trade.Clone()
    new_trade.Status("BO Confirmed")
    new_trade.FaceValue(new_trade.FaceValue()*-1)
    new_trade.Text1(None)
    new_trade.TrxTrade(None)
    new_trade.ValueDay(today)
    new_trade.AcquireDay(today)
    new_trade.OptKey1("Collateral balance trade")
    new_trade.AddInfoValue("Unique_Strate_ID", "")
    new_trade.Commit()
           
    new_settlements = new_trade.Settlements()
    for settlement in new_settlements:
        settlement_si = settlement.StorageImage()
        settlement_si.Status("Settled")
        settlement_si.Commit()
        LOGGER.info("Settled %s trade=%s" % (settlement.Oid(), settlement.Trade().Oid()))
    return new_trade


def correct_collateral_full_return(trade, visited=[]):
    if trade.Oid() in visited:
        return
    elif trade.Text1() == "FULL_RETURN":
        LOGGER.info("reverting full return %s" % trade.Oid())
        revert_full_return(trade)
    else:
        visited.append(trade.Oid())
        transref_trades = get_transaction_ref_trades(trade)
        for connected_trade in transref_trades:
            correct_collateral_full_return(connected_trade, visited)


def set_trade_status(trade, status):
    try:
        trade_si = trade.StorageImage()
        trade_si.Status(status)
        trade_si.Commit()
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def correct_all_subsequent_secloan_trades_in_chain(trade, previous_trade, last_trade_in_chain, trade_settlement_amount):
    trade_quantity = trade.FaceValue()
    new_end_date = trade.Instrument().StartDate()
    set_correct_end_date_on_trade(previous_trade, new_end_date)
    
    if last_trade_in_chain.Text1() == "FULL_RETURN":
        if trade.Oid() < last_trade_in_chain.Oid() and trade.Status() != 'Void' :
            set_correct_qty_on_trade(trade, trade_quantity + trade_settlement_amount)
            set_trade_to_open_ended(trade)
            
    if trade.Oid() == last_trade_in_chain.Oid():
        if trade.Text1() == "FULL_RETURN":
            new_trade_quantity = trade_settlement_amount
            revert_full_return(trade, previous_trade)
        else:
            new_trade_quantity = trade_quantity + trade_settlement_amount
        set_correct_qty_on_trade(trade, new_trade_quantity)
        set_trade_to_open_ended(trade)
        return
    else:
        next_trade = get_next_trade(trade)
        return correct_all_subsequent_secloan_trades_in_chain(next_trade, trade, last_trade_in_chain, trade_settlement_amount)


def revert_full_return(trade, previous_trade=None):
    try:
        trade_si = trade.StorageImage()
        if previous_trade:
            rate = previous_trade.Instrument().Legs()[0].FixedRate()
            leg = trade_si.Instrument().Legs()[0]
            leg_si = leg.StorageImage()
            leg_si.FixedRate(rate)
            leg_si.Commit()
        trade_si.Text1("PARTIAL_RETURN")
        trade_si.Type(0)
        trade_si.Commit()
        LOGGER.info("setting trade {0} to partial return".format(trade.Oid()))
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def set_correct_end_date_on_trade(trade, new_end_date):
    acm.BeginTransaction()
    try:
        instrument_si = trade.Instrument().StorageImage()
        legs = instrument_si.Legs()
        for leg in legs:
            leg_si = leg.StorageImage()
            leg_si.EndDate(new_end_date)
            leg_si.Commit()
        instrument_si.ExpiryDate(new_end_date)
        LOGGER.info("setting instrument {0} end date".format(trade.Instrument().Oid()))
        instrument_si.Commit()
        acm.CommitTransaction()
        return
    except Exception, error_msg:
        acm.AbortTransaction()
        LOGGER.exception('Error')
        return


def set_trade_to_void(trade):
    try:
        trade_si = trade.StorageImage()
        trade_si.Status('Void')
        LOGGER.info("setting trade {0} to Void".format(trade.Oid()))
        trade_si.Commit()
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def set_trade_to_open_ended(trade):
    try:
        instrument_si = trade.Instrument().StorageImage()
        instrument_si.OpenEnd('Open End')
        LOGGER.info("setting instrument {0} to open ended".format(trade.Instrument().Name()))
        instrument_si.Commit()
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def set_correct_qty_on_trade(trade, qty):
    try:
        trade_si = trade.StorageImage()
        trade_si.FaceValue(qty)
        LOGGER.info("in seting qty on trade")
        LOGGER.info("setting trade {0} to have quantity {1}".format(trade.Oid(), qty))
        trade_si.Commit()
        return
    except Exception, error_msg:
        LOGGER.exception('Error')
        return


def canceled_settlement_notification(settlement):
    statement = """
                Settlement {0} has been cancelled
                Associated trade {1} has been voided
                Original position has been re-opened by setting {2} back to open ended/n
                """
    trade = settlement.Trade()
    previous_trade = get_previous_trade(trade)
    LOGGER.info(statement.format(settlement.Oid(), settlement.Trade().Oid(), previous_trade.Oid()))


def failed_settlement_notification(settlement):
    statement = """
                Settlement {0} has failed in processing
                Associated trade {1} has been voided
                All subsequent valid trades {2} have had their quantities amended to reflect the failure.
                """
    trade = settlement.Trade()
    trx_trades = acm.FTrade.Select("trxTrade = {0}".format(trade.Oid()))
    trade_list = [_trade.Oid() for _trade in trx_trades if _trade.Status() != 'Void' and _trade.Oid() > trade.Oid()]
    LOGGER.info(statement.format(settlement.Oid(), settlement.Trade().Oid(), str(trade_list)))


def get_transaction_ref_trades(trade):
    trades_in_chain = acm.FTrade.Select("trxTrade = %i and oid <> %i" % (trade.Oid(), trade.Oid()))
    if len(trades_in_chain) > 0:
        return trades_in_chain
    return []


def get_last_trade(trade):
    trades_in_chain = acm.FTrade.Select("contractTrdnbr = %i and status <> 'Void'" % trade.ContractTrdnbr())
    if len(trades_in_chain) > 0:
        return trades_in_chain[-1]


def get_connected_trade(trade):
    trades_in_chain = acm.FTrade.Select("contractTrdnbr = %i and oid <> %i" % (trade.ContractTrdnbr(), trade.Oid()))
    if len(trades_in_chain) > 0:
        return trades_in_chain[0] 
    return None


def get_first_trade(trade):
    trades_in_chain = acm.FTrade.Select("contractTrdnbr = %i and status <> 'Void'" % trade.ContractTrdnbr())
    if len(trades_in_chain) > 0:
        return trades_in_chain[0]


def get_previous_trade(trade):
    conn_trades_in_chain = acm.FTrade.Select("contractTrdnbr = %i and status <> 'Void'" % trade.ContractTrdnbr())
    trades_in_chain = [_trd for _trd in conn_trades_in_chain if _trd.Oid() < trade.Oid()]
    if len(trades_in_chain) > 0:
        return trades_in_chain[-1]
    return trade


def get_next_trade(trade):
    conn_trades_in_chain = acm.FTrade.Select("contractTrdnbr = %i and status <> 'Void'" % trade.ContractTrdnbr())
    trades_in_chain = [_trd for _trd in conn_trades_in_chain if _trd.Oid() > trade.Oid()]
    if len(trades_in_chain) > 0:
        return trades_in_chain[0]
    return trade
