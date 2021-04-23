

import acm


def create_fee_trades(client_facing_trade, acquirer,
                      additional_portfolio, trade_status, val_group):
    trade = acm.FTrade()
    instrument = client_facing_trade.Instrument().Clone()    
    instrument.Name(client_facing_trade.Instrument().Name() + '/Internal')
    if val_group:
        instrument.ValuationGrpChlItem(val_group)
        
    try:
        instrument.Commit()
    except Exception as e:        
        print('Could not create a new instrument', e)
        
    trade.Type('Normal')      
    trade.Instrument(instrument)
    trade.Currency(client_facing_trade.Currency())
    trade.Acquirer(acquirer)
    trade.Portfolio(additional_portfolio)
    trade.Counterparty(client_facing_trade.Acquirer())
    trade.TradeTime(client_facing_trade.TradeTime())
    trade.AcquireDay(client_facing_trade.AcquireDay())
    trade.ValueDay(client_facing_trade.ValueDay())
    trade.Quantity(client_facing_trade.Quantity())
    trade.HaircutType(client_facing_trade.HaircutType())
    trade.Status(trade_status)
    trade.MirrorPortfolio(client_facing_trade.Portfolio())
    trade.Trader(acm.User())
    trade.TrxTrade(client_facing_trade)
    trade.Price(client_facing_trade.Price())
    trade.Premium(client_facing_trade.Premium())    
    return trade


def create_fee_payments(trade, pay_date, payment_dict):
    payments = []
    pay_date_str = str(pay_date)
    for fee_type, (payment_amount,
                   payment_currency) in payment_dict.iteritems():
        if payment_amount == 0:
            continue
        payment_kwargs = {'trade': trade,
                          'payment_type': 'Internal fee',
                          'currency': payment_currency,
                          'amount': payment_amount,
                          'pay_date': pay_date_str,
                          'text': fee_type}
        payment = _create_payment(**payment_kwargs)
        payments.append(payment)
    return payments


def create_mirror_payments(trade, original_payments):
    new_payments = []
    for original_payment in original_payments:
        payment_kwargs = {'trade': trade,
                          'payment_type': original_payment.Type(),
                          'currency': original_payment.Currency(),
                          'amount': original_payment.Amount() * -1,
                          'pay_date': original_payment.PayDay(),
                          'text': original_payment.Text()}

        new_payment = _create_payment(**payment_kwargs)
        new_payments.append(new_payment)

    return new_payments


def _create_payment(trade, payment_type, currency,
                    amount, pay_date, text):
    payment = acm.FPayment()
    payment.Trade(trade)
    payment.Amount(amount)
    payment.Currency(currency)
    payment.Type(payment_type)
    payment.ValidFrom(acm.Time().DateNow())
    payment.PayDay(pay_date)
    payment.Party(trade.Counterparty())
    payment.Text(text)

    return payment


def commit_entities(*entity_list):
    try:
        acm.BeginTransaction()
        for entity in entity_list:
            entity.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        raise


def get_existing_bridge_trades(trade):
    if trade:
        filter_text = "trxTrade='{0}'".format(trade.Oid())
        return acm.FTrade.Select(filter_text)
    return []
