"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FXOptionDocumentGeneral

DESCRIPTION
    This module contains general functionality related to FX Option documentation.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-03-01      FAOPS-385       Cuen Edwards            Letitia Carboni         Refactored out from other modules.
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Addition of support for FX Option confirmations.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import DocumentGeneral


def is_fx_option(instrument):
    """
    Determine whether or not an instrument is an FX option.
    """
    if instrument.InsType() != 'Option':
        return False
    return instrument.UnderlyingType() == 'Curr'


def is_fx_option_standalone_trade(trade):
    """
    Determine whether or not a trade is a supported standalone FX
    Option trade (as opposed to being part of an FX Option structure)
    for documentation generation purposes.
    """
    # It seems that standalone FX Option trades are sometimes
    # booked with a Trx Trade ref - allow for this as long as
    # there is only one supported FX Option trade in the
    # transaction and that trade is the same trade that was
    # passed in.
    fx_option_trades = get_supported_fx_option_trades(trade)
    if len(fx_option_trades) == 1:
        return True
    return False


def is_fx_option_structure_trade(trade):
    """
    Determine whether or not a trade is part of a supported FX Option
    structure (as opposed to being a standalone FX Option trade) for
    documentation generation purposes.
    """
    fx_option_trades = get_supported_fx_option_trades(trade)
    if len(fx_option_trades) > 1:
        return True
    return False


def get_supported_fx_option_trades(trade):
    """
    Get all supported FX Option trades related to a trade.
    """
    fx_option_trades = list()
    if not is_supported_fx_option_trade(trade):
        return fx_option_trades
    if trade.TrxTrade() is None:
        # Standalone trade without a trx trade.
        fx_option_trades.append(trade)
    else:
        # Standalone trade with a trx trade or a structure trade.
        for trx_trade in trade.TrxTrade().TrxTrades():
            if is_supported_fx_option_trade(trx_trade):
                fx_option_trades.append(trx_trade)
    return fx_option_trades


def is_supported_fx_option_trade(trade):
    """
    Determine whether or not a trade is a supported FX Option trade
    for documentation generation purposes.
    """
    if trade.Type() != 'Normal':
        return False
    if trade.Status() in ['Void', 'Confirmed Void']:
        return False
    instrument = trade.Instrument()
    if not is_fx_option(instrument):
        return False
    if instrument.FxOptionType() not in ['Vanilla', 'Barrier']:
        return False
    if instrument.Digital():
        return False
    # Allow for trades where the counterparty has not been specified yet.
    counterparty = trade.Counterparty()
    if counterparty is not None and counterparty.Type() not in ('Counterparty', 'Client'):
        return False
    return True


def get_product_type(instrument):
    """
    Get the instrument product type.
    """
    if instrument.ProductTypeChlItem() is None:
        return None
    return instrument.ProductTypeChlItem().Name()


def get_buyer_name(trade):
    """
    Get the name of the buyer of the FX Option.
    """
    if trade.Bought():
        return DocumentGeneral.get_default_bank_name()
    return DocumentGeneral.get_party_full_name(trade.Counterparty())


def get_seller_name(trade):
    """
    Get the name of the seller of the FX Option.
    """
    if trade.Bought():
        return DocumentGeneral.get_party_full_name(trade.Counterparty())
    return DocumentGeneral.get_default_bank_name()


def get_call_currency(instrument):
    """
    Get the FX Option call currency.
    """
    if instrument.IsCallOption():
        return instrument.Underlying()
    return instrument.StrikeCurrency()


def get_call_amount(trade, instrument):
    """
    Get the FX Option call currency amount.
    """
    call_amount = None
    if instrument.IsCallOption():
        call_amount = trade.Nominal()
    else:
        call_amount = trade.Nominal() * instrument.StrikePrice()
    return abs(round(call_amount, 2))


def get_put_currency(instrument):
    """
    Get the FX Option put currency.
    """
    if instrument.IsPutOption():
        return instrument.Underlying()
    return instrument.StrikeCurrency()


def get_put_amount(trade, instrument):
    """
    Get the FX Option put currency amount.
    """
    put_amount = None
    if instrument.IsPutOption():
        put_amount = trade.Nominal()
    else:
        put_amount = trade.Nominal() * instrument.StrikePrice()
    return abs(round(put_amount, 2))


def get_currency_pair_name(call_currency, put_currency):
    """
    Get the FX Option currency pair in the form non-ZAR/ZAR.
    """
    if _is_zar_currency(call_currency):
        return put_currency.Name() + '/' + call_currency.Name()
    return call_currency.Name() + '/' + put_currency.Name()


def get_settlement_type(instrument):
    """
    Get a description of the FX Option settlement type.
    """
    if instrument.SettlementType() == 'Physical Delivery':
        return 'Physical'
    elif instrument.SettlementType() == 'Cash':
        return 'Cash'
    raise ValueError("Unsupported settlement type '{settlement_type}' specified.".format(
        settlement_type=instrument.SettlementType()
    ))


def get_barrier_date_exotic_events(instrument):
    """
    Get any barrier date exotic events.
    """
    barrier_date_exotic_events = list()
    exotic_events = instrument.ExoticEvents().AsArray().SortByProperty('Date')
    for exotic_event in exotic_events:
        if exotic_event.Type() != 'Barrier date':
            continue
        barrier_date_exotic_events.append(exotic_event)
    return barrier_date_exotic_events


def get_business_days(instrument):
    """
    Get a description of the FX Option calendars.
    """
    call_currency = get_call_currency(instrument)
    put_currency = get_put_currency(instrument)
    return call_currency.Calendar().Name() + ', ' + put_currency.Calendar().Name()


def _is_zar_currency(currency):
    """
    Determine whether or not a currency is ZAR.
    """
    return currency.Name() == 'ZAR'
