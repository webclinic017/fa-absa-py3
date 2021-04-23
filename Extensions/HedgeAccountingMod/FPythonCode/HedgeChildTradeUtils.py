'''
===================================================================================================
PURPOSE: The HedgeChildTradeUtils module contains all the business logic required to create child
            trades used in the Hedge Effectiveness Suite. The business logic varies per type of
            instrument and Hedge Type of the specific trade included in a Hedge Relationship.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
29-08-2018 FIS Team            Dedesignation implementation
10-05-2019 FIS Team            Dedesignation touch ups (
===================================================================================================
'''

import acm
import HedgeConstants
import FLogger

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)
CONTEXT = acm.GetDefaultContext()
SHEET =  HedgeConstants.STR_TRADE_SHEET
tradeSheetCalcSpace = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET)

def get_instrument_price(instrument_name, price_date):
    '''Get the Internal market closing price for a instrument
        on a specific date.
    '''

    query = 'instrument = "%s" and market = "%s" and day <= "%s"'\
            % (instrument_name, "internal", price_date)
    prices = acm.FPrice.Select(query).SortByProperty('Day', False)

    if prices:
        price = prices[0].Settle()
        logger.LOG('Historical price (%s) found for instrument="%s" and date="%s"'
                   % (price, instrument_name, price_date))

        return price

    logger.WLOG('No historical price for instrument %s and date %s. Set price to 0.'
                % (instrument_name, price_date))

    return 0.0


def get_cashflow(cashFlows, referenceDate):
    '''Retrieve the cashflow that falls over the reference date
    '''

    for cashflow in cashFlows:
        if cashflow.StartDate() <= referenceDate and referenceDate <= cashflow.EndDate():

            return cashflow

    return None


def create_base_trade_clone(old_Trade, designation_date, hedge_trade_type):
    '''Create a new trade with only some properties copied from the
        specified 'oldtrade' trade.
    '''

    new_trade = acm.FTrade()

    new_trade.Trader(old_Trade.Trader())
    new_trade.Currency(old_Trade.Currency())
    new_trade.Instrument(old_Trade.Instrument())
    new_trade.TrxTrade(old_Trade.Oid())

    new_trade.Text1(hedge_trade_type)
    new_trade.Text2(old_Trade.Oid())

    new_trade.Type('Normal')
    new_trade.Status(HedgeConstants.STR_CHILD_TRADE_STATUS)
    new_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)

    new_trade.Acquirer(HedgeConstants.STR_CHILD_TRADE_ACQUIRER)
    new_trade.Counterparty(HedgeConstants.STR_CHILD_TRADE_COUNTERPARTY)

    new_trade.TradeTime(designation_date)
    new_trade.ValueDay(designation_date)
    new_trade.AcquireDay(designation_date)

    new_trade.RegisterInStorage()

    return new_trade


def get_leg_accrued_premium(trade, leg, designation_date):
    '''Calculate the accrued premium for a specific FLeg at the start of the child trade
        (designation date).
    '''

    instrument = trade.Instrument()
    calendar = instrument.Currency().Calendar()
    calendarInfo = calendar.CalendarInformation()

    leg_accrued_ratio = 0.0
    leg_accrued_premium = 0.0

    cashflow = get_cashflow(leg.CashFlows(), designation_date)

    if cashflow:
        try:
            leg_accrued_ratio = calendarInfo.YearsBetween(cashflow.StartDate(),
                                                          designation_date,
                                                          leg.DayCountMethod())
        except Exception:
            leg_accrued_ratio = 0.0
        acm_calc = acm.Calculations()
        stdCalculationSpaceCollection = acm_calc.CreateStandardCalculationsSpaceCollection()

        # calc leg accrued portion
        try:
            cf_calc = cashflow.Calculation()
            cashflow_forward_rate = cf_calc.ForwardRate(stdCalculationSpaceCollection)
        except Exception:
            cashflow_forward_rate = 0.0

        try:
            cashflow_nominal = cashflow.Calculation().Nominal(stdCalculationSpaceCollection,
                                                              trade,
                                                              leg.Currency())
        except Exception:
            cashflow_nominal = 0.0

        if cashflow_nominal:
            if cashflow_nominal.IsKindOf(acm.FDenominatedValue):
                cashflow_nominal = cashflow_nominal.Value().Number()
        else:
            cashflow_nominal = 0

        if not cashflow_forward_rate:
            cashflow_forward_rate = 0.0

        if not leg_accrued_ratio:
            leg_accrued_ratio = 0.0

        leg_accrued_premium = cashflow_nominal * cashflow_forward_rate * leg_accrued_ratio

    return leg_accrued_premium


def get_accrued_premium(trade, designation_date):
    '''Calculate the accrued premium at the start of the child trade (designation date).
    '''

    total_accrued_premium = 0

    instrument = trade.Instrument()

    for leg in instrument.Legs():
        leg_accrued_premium = 0

        leg_accrued_premium = get_leg_accrued_premium(trade, leg, designation_date)

        # aggregate into total accrued premium
        total_accrued_premium = total_accrued_premium + leg_accrued_premium

    return total_accrued_premium

def add_payment(trade, pay_date, valid_from_date, paymentType='Cash', amount=0, currency=None):
    '''Add a payment to the specified trade.
    '''

    if amount:
        payment = acm.FPayment()
        payment.Trade(trade)
        payment.RegisterInStorage()

        if currency:
            payment.Currency(currency)
        else:
            payment.Currency(trade.Currency())

        payment.Party(trade.Counterparty())
        payment.Amount(amount)
        payment.Type(paymentType)
        payment.PayDay(pay_date)
        payment.ValidFrom(valid_from_date)

        trade.Payments().Add(payment)


def remove_payments(trade):
    '''Remove all payments from a trade.
    '''

    while trade.Payments():
        trade.Payments().Clear()

        try:
            trade.Commit()
        except Exception:
            pass


def get_payment_tpl_dirty(trade, designation_date):

    # simulate global end date to designation date
    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date',
                                            'Custom Date')

    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                            designation_date)

    tpl_calc = tradeSheetCalcSpace.CreateCalculation(trade, 'Portfolio Total Profit and Loss')
    tpl_value = tpl_calc.Value().Number()

    tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

    return tpl_value


def get_payment_tpl(trade, designation_date):

    # simulate global end date to designation date
    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date',
                                            'Custom Date')

    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                            designation_date)

    clean_tpl_calc = tradeSheetCalcSpace.CreateCalculation(trade, 'Portfolio Clean PnL')

    total_clean_pnl = 0
    if clean_tpl_calc and clean_tpl_calc.Value():
        total_clean_pnl = clean_tpl_calc.Value().Number()

    tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

    return total_clean_pnl


def close_out_trade(trade, acquire_day, value_day, nominal, premium, payments):
    '''Create the close-out trade for the specified trade
    '''
    close_trade = acm.TradeActions().CloseTrade(trade,                          # trade
                                                acquire_day,                    # acquireDay
                                                value_day,                      # valueDay
                                                nominal,                        # nominal
                                                premium,                        # premium
                                                payments)                       # payments
    close_trade.TradeTime = acquire_day
    close_trade.Status("FO Confirmed")
    return close_trade


def get_trading_manager_column_value(calcSpace, trade, end_date, columnId):

    # simulate global end date to designation date
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date',
                                  'Custom Date')

    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                  end_date)

    result = 0
    calc_result_value = calcSpace.CreateCalculation(trade, columnId)

    if calc_result_value:
        result = calc_result_value.Value().Number()

    # remove simulations
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

    return result


def create_external_child(external_trade, designation_date, hedge_trade_type, percentage):
    '''Switch External Trades to the appropriate instrument specific logic funtion to
    create child trades.
    '''
    child_trade = None

    instrument = external_trade.Instrument()

    if instrument.InsType() == 'Swap':
        child_trade = create_interest_rate_swap_child(external_trade,
                                                      percentage,
                                                      designation_date,
                                                      hedge_trade_type)

    elif instrument.InsType() == 'IndexLinkedSwap':
        child_trade = create_index_linked_swap_child(external_trade,
                                                     percentage,
                                                     designation_date,
                                                     hedge_trade_type)

    elif instrument.InsType() == 'CurrSwap':
        child_trade = create_currency_swap_child(external_trade,
                                                 percentage,
                                                 designation_date,
                                                 hedge_trade_type)

    elif instrument.InsType() == 'FRA':
        child_trade = create_fra_child(external_trade,
                                       percentage,
                                       designation_date,
                                       hedge_trade_type)

    elif instrument.InsType() == 'Curr':
        child_trade = create_fx_forward_child(external_trade,
                                              percentage,
                                              designation_date,
                                              hedge_trade_type)

    elif instrument.InsType() == 'Deposit':
        child_trade = create_deposit_child(external_trade,
                                           percentage,
                                           designation_date,
                                           hedge_trade_type)

    else:
        raise Exception('Invalid trade type used as External Trade. External Trades needs to be '
                        'of type: [Swap, IndexLinkedSwap, CurrSwap, FRA]')

    return child_trade


def update_external_child(external_trade, child_trade, designation_date,
                          hedge_trade_type, percentage):
    '''Switch External Trades to the appropriate instrument specific logic funtion to
        update child trades.
    '''

    instrument = external_trade.Instrument()

    if instrument.InsType() == 'Swap':
        child_trade = set_interest_rate_swap_child(external_trade,
                                                   child_trade,
                                                   percentage,
                                                   designation_date)

    elif instrument.InsType() == 'IndexLinkedSwap':
        child_trade = set_index_linked_swap_child(external_trade,
                                                  child_trade,
                                                  percentage,
                                                  designation_date)

    elif instrument.InsType() == 'CurrSwap':
        child_trade = set_currency_swap_child(external_trade,
                                              child_trade,
                                              percentage,
                                              designation_date)

    elif instrument.InsType() == 'FRA':
        child_trade = set_fra_child(external_trade,
                                    child_trade,
                                    percentage,
                                    designation_date)

    elif instrument.InsType() == 'Curr':
        child_trade = set_fx_forward_child(external_trade,
                                           child_trade,
                                           percentage,
                                           designation_date)

    elif instrument.InsType() == 'Deposit':
        child_trade = set_deposit_child(external_trade,
                                        child_trade,
                                        percentage,
                                        designation_date)

    else:
        raise Exception('Invalid trade type used as External Trade. External Trades needs to '
                        'be of type: [Swap, IndexLinkedSwap, CurrSwap, FRA]')

    return child_trade


def create_interest_rate_swap_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for Interest Rate Swaps
    '''
    child_trade = create_base_trade_clone(external_trade, designation_date, hedge_trade_type)
    return set_interest_rate_swap_child(external_trade, child_trade, percentage, designation_date)


def set_interest_rate_swap_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trades specific to Interest Rate Swaps
    '''

    # first remove all old payments
    remove_payments(child_trade)

    # calc & set quantity
    quantity = external_trade.Quantity() * percentage
    child_trade.Quantity(quantity)

    # calc & set premium
    premium_accrued_at_start = 0
    premium = 0

    instrument = external_trade.Instrument()

    if external_trade.Premium() != 0:

        if external_trade.Price():

            quantity = external_trade.Quantity()
            contract_size = instrument.ContractSize()
            leg_nominal_factor = 1

            premium = quantity * contract_size * leg_nominal_factor * percentage
        else:
            premium = external_trade.Premium() * percentage

    premium_accrued_at_start = get_accrued_premium(child_trade, designation_date)

    premium = premium + (premium_accrued_at_start * -1)
    child_trade.Premium(premium)

    # update trade dates:
    child_trade.TradeTime(designation_date)
    child_trade.ValueDay(designation_date)
    child_trade.AcquireDay(designation_date)

    # create & set trade payments

    valuation_start_date = '1970-01-01'  # start valuations at inception date

    stdCalculationSpaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    # Cash payment to reverse accrued starting premium
    pay_date = child_trade.TradeTime()
    valid_from_date = child_trade.AcquireDay()
    try:
        add_payment(child_trade, pay_date, valid_from_date, 'Cash', premium_accrued_at_start)
    except:
        pass

    child_trade.Commit()

    # accrued interest calc & payment
    accrued_interest = child_trade.Calculation().AccruedInterest(stdCalculationSpaceCollection,
                                                                 valuation_start_date,
                                                                 designation_date,
                                                                 child_trade.Currency())
    try:
        add_payment(child_trade,
                    pay_date,
                    pay_date,
                    'Accrued Interest Adjustment',
                    (-1 * accrued_interest))
    except:
        pass

    clean_pnl = get_payment_tpl(child_trade, designation_date)
    try:
        add_payment(child_trade, pay_date, pay_date, 'Cash', (-1 * clean_pnl))  # MS
    except:
        pass

    child_trade.Commit()

    return child_trade


def create_index_linked_swap_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for Index Linked Swaps
    '''

    child_trade = create_base_trade_clone(external_trade, designation_date, hedge_trade_type)
    return set_index_linked_swap_child(external_trade, child_trade, percentage, designation_date)


def set_index_linked_swap_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trades - Index linked Swaps
    '''

    # Index linked swaps should be follow the same rules as Interest Rate Swaps
    return set_interest_rate_swap_child(external_trade, child_trade, percentage, designation_date)


def create_currency_swap_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for Currency Swaps
    '''

    # copy instrument

    original_contract_size = external_trade.Instrument().ContractSize()

    instrument_clone = external_trade.Instrument().Clone()
    instrument_clone_name = instrument_clone.SuggestName()
    instrument_clone.Name(instrument_clone_name)

    # set the new nominal
    nominal = original_contract_size * percentage
    instrument_clone.ContractSize(nominal)

    # regenerate the cashflows
    for leg in instrument_clone.Legs():
        leg.GenerateCashFlows(None)

    instrument_clone.Commit()

    # create trade

    child_trade = acm.FTrade()

    child_trade.Instrument(instrument_clone)
    child_trade.Quantity(external_trade.Quantity())

    child_trade.Trader(external_trade.Trader())
    child_trade.Currency(external_trade.Currency())
    child_trade.TrxTrade(external_trade.Oid())
    child_trade.Price(external_trade.Price())

    child_trade.Text1(hedge_trade_type)
    child_trade.Text2(external_trade.Oid())

    child_trade.Type('Normal')
    child_trade.Status(HedgeConstants.STR_CHILD_TRADE_STATUS)
    child_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)
    child_trade.Acquirer(HedgeConstants.STR_CHILD_TRADE_ACQUIRER)
    child_trade.Counterparty(HedgeConstants.STR_CHILD_TRADE_COUNTERPARTY)

    child_trade.TradeTime(designation_date)
    child_trade.ValueDay(designation_date)
    child_trade.AcquireDay(designation_date)

    child_trade.RegisterInStorage()
    child_trade.Commit()

    return set_currency_swap_child(external_trade, child_trade, percentage, designation_date)


def set_currency_swap_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trade - Currency Swaps
    '''

    # first remove all old payments
    remove_payments(child_trade)

    # Create Instrument clone for swap and update nominal value

    original_contract_size = external_trade.Instrument().ContractSize()

    child_instrument = child_trade.Instrument().Clone()

    nominal = original_contract_size * percentage
    child_instrument.ContractSize(nominal)

    # regenerate the cashflows
    for leg in child_instrument.Legs():
        leg.GenerateCashFlows(None)

    child_trade.Instrument().Apply(child_instrument)
    child_trade.Instrument().Commit()

    # update the price table for the new instrument (add a price for designation date)

    t_query = "instrument = %d and market = '%s' and currency = '%s' and day = '%s'"
    price_query = t_query % (child_trade.Instrument().Oid(),
                             HedgeConstants.STR_MTM_PRICE_MARKET,
                             child_trade.Instrument().Currency().Oid(),
                             designation_date)

    price_at_designation = acm.FPrice.Select(price_query)

    if price_at_designation:
        price_at_designation = price_at_designation[0]
    else:
        price_at_designation = acm.FPrice()
        price_at_designation.Day(designation_date)
        price_at_designation.Instrument(child_trade.Instrument())
        price_at_designation.Currency(child_trade.Instrument().Currency())
        price_at_designation.Market(HedgeConstants.STR_MTM_PRICE_MARKET)

    tradeSheetCalcSpace.SimulateGlobalValue('Valuation Date', designation_date)
    new_theoretical_price = tradeSheetCalcSpace.CalculateValue(child_trade.Instrument(), 'Price Theor')
    tradeSheetCalcSpace.RemoveGlobalSimulation('Valuation Date')

    price_at_designation.Settle(new_theoretical_price)
    price_at_designation.Commit()

    # update trade dates

    child_trade.TradeTime(designation_date)
    child_trade.ValueDay(designation_date)
    child_trade.AcquireDay(designation_date)

    child_trade.Commit()

    # create & set trade payments
    #   -> Payments needs to be calculated and set per leg.

    for leg in child_trade.Instrument().Legs():

        leg_accrued_premium = get_leg_accrued_premium(external_trade, leg, designation_date)

        acm_calc = acm.Calculations()
        stdCalculationSpaceCollection = acm_calc.CreateStandardCalculationsSpaceCollection()

        # Cash payment to reverse accrued starting premium
        pay_date = child_trade.TradeTime()
        valid_from_date = child_trade.AcquireDay()

        # Premium
        add_payment(child_trade, pay_date, valid_from_date, 'Premium', (leg_accrued_premium * -1),
                    leg.Currency())

        # Cash
        add_payment(child_trade, pay_date, valid_from_date, 'Cash', leg_accrued_premium,
                    leg.Currency())

        # Accrued Interest Adjustment
        l_calc = leg.Calculation()
        accrued_interest = l_calc.AccruedInterest(stdCalculationSpaceCollection,
                                                  child_trade,
                                                  child_trade.ValueDay(),
                                                  acm.Time.DateAddDelta(designation_date, 0, 0, 1),
                                                  leg.Currency())
        add_payment(child_trade,
                    pay_date,
                    pay_date,
                    'Accrued Interest Adjustment',
                    (accrued_interest * -1),
                    leg.Currency())

        child_trade.Commit()

        # simulate global end date to designation date
        tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date',
                                                'Custom Date')

        tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom',
                                                designation_date)

        legAndTrade = acm.Risk.CreateLegAndTrades(leg, child_trade)
        clean_tpl_calc = tradeSheetCalcSpace.CreateCalculation(legAndTrade, 'Portfolio Clean PnL')

        total_pnl = clean_tpl_calc.Value().Number()

        tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

        add_payment(child_trade, pay_date, pay_date, 'Cash', total_pnl, leg.Currency())

    child_trade.Commit()

    return child_trade


def create_fra_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for FRA's
    '''

    child_trade = create_base_trade_clone(external_trade, designation_date, hedge_trade_type)
    return set_fra_child(external_trade, child_trade, percentage, designation_date)


def set_fra_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trade - FRA
    '''

    # first remove all old payments
    remove_payments(child_trade)

    # override trades dates for FRA
    if designation_date < external_trade.AcquireDay():
        child_trade.TradeTime(external_trade.TradeTime())
        child_trade.ValueDay(external_trade.ValueDay())
        child_trade.AcquireDay(external_trade.AcquireDay())
    else:
        # update trade dates:
        child_trade.TradeTime(designation_date)
        child_trade.ValueDay(designation_date)
        child_trade.AcquireDay(designation_date)

    # calc & set nominal (FRA does not have trade quantity)
    nominal = external_trade.Nominal() * percentage
    child_trade.Nominal(nominal)

    # calc & set premium
    premium = 0

    if external_trade.Premium() != 0:
        if external_trade.Price():

            quantity = external_trade.Quantity()
            contract_size = external_trade.Instrument().ContractSize()
            leg_nominal_factor = 1

            premium = quantity * contract_size * leg_nominal_factor * percentage

        else:
            premium = external_trade.Premium() * percentage

    premium_accrued_at_start = get_accrued_premium(child_trade, designation_date)

    premium = premium + (premium_accrued_at_start * -1)
    child_trade.Premium(premium)

    # create & set trade payments

    # Cash payment to reverse accrued starting premium
    pay_date = child_trade.TradeTime()

    child_trade.Commit()

    clean_pnl = get_payment_tpl(child_trade, designation_date)
    add_payment(child_trade, pay_date, pay_date, 'Cash', (-1 * clean_pnl))
    child_trade.Commit()

    return child_trade


def create_fx_forward_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for FX Forward (FX Cash)
    '''

    original_trade_oid = external_trade.Oid()

    child_trade = external_trade.Clone()

    child_trade.TrxTrade(original_trade_oid)

    child_trade.Text1(hedge_trade_type)
    child_trade.Text2(external_trade.Oid())

    child_trade.Status(HedgeConstants.STR_CHILD_TRADE_STATUS)
    child_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)

    child_trade.RegisterInStorage()

    return set_fx_forward_child(external_trade, child_trade, percentage, designation_date)


def set_fx_forward_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trade - FX Forwards (FX Cash)
    '''

    # first remove all old payments
    remove_payments(child_trade)

    # calc quantity & premium
    original_trade_qty = external_trade.Quantity()
    quantity = original_trade_qty * percentage

    child_trade.Quantity(quantity)

    # premium should be the inverse for FX_Forwards
    premium = quantity * child_trade.Price() * -1
    child_trade.Premium(premium)

    # update trade dates (tradeTime only - value date should stay the
    #                    as on original trade).

    child_trade.TradeTime(designation_date)
    child_trade.ValueDay(external_trade.ValueDay())
    child_trade.AcquireDay(external_trade.AcquireDay())

    # create & set trade payments

    # Cash payment to reverse accrued starting premium
    pay_date = child_trade.TradeTime()

    child_trade.Commit()

    clean_pnl = get_payment_tpl(child_trade, designation_date)
    add_payment(child_trade, pay_date, pay_date, 'Cash', clean_pnl)
    child_trade.Commit()

    return child_trade


def create_deposit_child(external_trade, percentage, designation_date, hedge_trade_type):
    '''Create the child trade for Deposits
    '''
    # copy instrument

    original_contract_size = external_trade.Instrument().ContractSize()

    original_quantity = external_trade.Quantity()

    instrument_clone = external_trade.Instrument().Clone()
    instrument_clone_name = instrument_clone.SuggestName()
    instrument_clone.Name(instrument_clone_name)

    # set the new nominal
    nominal = original_contract_size * percentage
    instrument_clone.ContractSize(nominal)

    # regenerate the cashflows
    for leg in instrument_clone.Legs():
        leg.GenerateCashFlows(None)

    instrument_clone.Commit()

    # create trade

    child_trade = acm.FTrade()

    child_trade.Instrument(instrument_clone)
    child_trade.Quantity(original_quantity)

    child_trade.Trader(external_trade.Trader())
    child_trade.Currency(external_trade.Currency())
    child_trade.TrxTrade(external_trade.Oid())
    child_trade.Price(external_trade.Price())

    child_trade.Text1(hedge_trade_type)
    child_trade.Text2(external_trade.Oid())

    child_trade.Type('Normal')
    child_trade.Status(HedgeConstants.STR_CHILD_TRADE_STATUS)
    child_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)
    child_trade.Acquirer(HedgeConstants.STR_CHILD_TRADE_ACQUIRER)
    child_trade.Counterparty(HedgeConstants.STR_CHILD_TRADE_COUNTERPARTY)

    child_trade.TradeTime(designation_date)
    child_trade.ValueDay(designation_date)
    child_trade.AcquireDay(designation_date)

    external_add_info = external_trade.AdditionalInfo().Funding_Instype()
    child_trade.AdditionalInfo().Funding_Instype(external_add_info)

    child_trade.RegisterInStorage()
    child_trade.Commit()

    return set_deposit_child(external_trade, child_trade, percentage, designation_date)


def set_deposit_child(external_trade, child_trade, percentage, designation_date):
    '''Update child trade - Deposit
    '''

    # invoke same logic as for currency swap
    child_trade = set_currency_swap_child(external_trade,
                                          child_trade,
                                          percentage,
                                          designation_date)
    return child_trade


def create_original_child(original_trade, designation_date, hedge_trade_type, percentage):
    '''Switch Original Trades to the appropriate instrument specific logic funtion to
        create child trades.
    '''
    instrument = original_trade.Instrument()

    child_trade = create_base_trade_clone(original_trade, designation_date, hedge_trade_type)

    if instrument.InsType() == 'Deposit':
        child_trade = set_original_deposit_child(original_trade,
                                                 child_trade,
                                                 percentage,
                                                 designation_date)
    elif instrument.InsType() == 'CD':
        child_trade = set_original_cd_child(original_trade,
                                            child_trade,
                                            percentage,
                                            designation_date)
    else:
        child_trade = set_original_default_child(original_trade,
                                                 child_trade,
                                                 designation_date,
                                                 hedge_trade_type,
                                                 percentage)

    return child_trade


def set_original_child(original_trade, child_trade, designation_date, hedge_trade_type, percentage):
    '''Switch Original Trades to the appropriate instrument specific logic funtion to
        update child trades.
    '''
    instrument = original_trade.Instrument()

    if instrument.InsType() == 'Deposit':
        child_trade = set_original_deposit_child(original_trade,
                                                 child_trade,
                                                 percentage,
                                                 designation_date)
    elif instrument.InsType() == 'CD':
        child_trade = set_original_cd_child(original_trade,
                                            child_trade,
                                            percentage,
                                            designation_date)
    else:
        child_trade = set_original_default_child(original_trade,
                                                 child_trade,
                                                 designation_date,
                                                 hedge_trade_type,
                                                 percentage)

    return child_trade


def set_original_deposit_child(original_trade, child_trade, percentage, designation_date):
    '''Update child trades - deposits
    '''
    instrument = original_trade.Instrument()

    currency = child_trade.Currency()
    calendar = currency.Calendar()
    value_date = instrument.SpotDate(designation_date, calendar)

    child_trade.TradeTime(designation_date)
    child_trade.AcquireDay(value_date)
    child_trade.ValueDay(value_date)

    original_trade_qty = original_trade.Quantity()

    quantity = original_trade_qty * percentage
    child_trade.Quantity(quantity)

    original_add_info = original_trade.AdditionalInfo().Funding_Instype()
    child_trade.AdditionalInfo().Funding_Instype(original_add_info)

    child_trade.Commit()

    return child_trade


def set_original_cd_child(original_trade, child_trade, percentage, designation_date):
    '''Update child trades - CD's
    '''
    instrument = original_trade.Instrument()

    currency = child_trade.Currency()
    calendar = currency.Calendar()
    value_date = instrument.SpotDate(designation_date, calendar)

    child_trade.TradeTime(designation_date)
    child_trade.AcquireDay(value_date)
    child_trade.ValueDay(value_date)

    original_trade_qty = original_trade.Quantity()

    quantity = original_trade_qty * percentage
    child_trade.Quantity(quantity)

    original_add_info = original_trade.AdditionalInfo().Funding_Instype()
    child_trade.AdditionalInfo().Funding_Instype(original_add_info)

    trade_decorator = acm.FTradeLogicDecorator(child_trade, None)
    trade_decorator.Price(original_trade.Price())

    child_trade.Commit()

    return child_trade


def set_original_default_child(original_trade, child_trade, designation_date, hedge_trade_type,
                               percentage):
    '''Create a child trade for trades for 'Original' trades in the Hedge Effectiveness suite.
    '''

    instrument = original_trade.Instrument()

    original_trade_qty = original_trade.Quantity()

    currency = child_trade.Currency()
    calendar = currency.Calendar()
    value_date = instrument.SpotDate(designation_date, calendar)

    child_trade.TradeTime(designation_date)
    child_trade.AcquireDay(value_date)
    child_trade.ValueDay(value_date)

    quantity = original_trade_qty * percentage
    child_trade.Quantity(quantity)

    previous_price = get_instrument_price(instrument.Name(), designation_date)
    trade_decorator = acm.FTradeLogicDecorator(child_trade, None)

    if original_trade.TradeTime()[:10] == designation_date[:10]:
        trade_decorator.Price(original_trade.Price())
    else:
        trade_decorator.Price(previous_price)

    child_trade.Commit()

    return child_trade


def create_internal_child(internal_trade, designation_date, hedge_trade_type, percentage):
    '''Logic to create the Internal trade child trade.
    '''

    original_trade_oid = internal_trade.Oid()

    child_trade = acm.FTrade()
    child_trade.Apply(internal_trade)

    #remove unique keys
    child_trade.OptionalKey('')

    # update some non-measurable details
    child_trade.Text1(hedge_trade_type)
    child_trade.Text2(original_trade_oid)
    child_trade.TrxTrade(original_trade_oid)

    child_trade.Status(HedgeConstants.STR_CHILD_TRADE_STATUS)
    child_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)

    child_trade.Acquirer(HedgeConstants.STR_CHILD_TRADE_ACQUIRER)
    child_trade.Counterparty(HedgeConstants.STR_CHILD_TRADE_COUNTERPARTY)

    child_trade.MirrorTrade(None)
    child_trade.ConnectedTrade(None)
    child_trade.Contract(None)

    child_trade.RegisterInStorage()
    child_trade.Commit()

    return set_internal_child(internal_trade,
                              child_trade,
                              designation_date,
                              hedge_trade_type,
                              percentage)


def set_internal_child(internal_trade, child_trade, designation_date, hedge_trade_type, percentage):
    '''Update a child trade for trades for 'Internal' trades in the Hedge Effectiveness suite.
    '''

    quantity = internal_trade.Quantity() * percentage
    child_trade.Quantity(quantity)

    child_trade.Commit()

    return child_trade


def create_child_trade(trade, designation_date, hedge_trade_type, percentage):
    '''Entry point to create child trades for Hedge Effectiveness Testing purposes.
    '''
    # try:
    child_trade = None

    percentage_float = float(percentage) / 100

    if hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Original:
        child_trade = create_original_child(trade,
                                            designation_date,
                                            hedge_trade_type,
                                            percentage_float)

    elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.External:
        child_trade = create_external_child(trade,
                                            designation_date,
                                            hedge_trade_type,
                                            percentage_float)

    elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Internal:
        child_trade = create_internal_child(trade,
                                            designation_date,
                                            hedge_trade_type,
                                            percentage_float)

    elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.ZeroBond:
        child_trade = None

    elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Hypo:
        child_trade = None

    return child_trade

    # except Exception, ex:
    #    message = 'Error creating child trade for trade [%s]. %s' %(trade.Oid(), ex)
    #    logger.ELOG(message)
    #    raise ex


def update_child_trade(trade, child_trade, designation_date, hedge_trade_type, percentage):
    '''Entry point to update child trades for Hedge Effectiveness Testing purposes.
    '''

    try:
        percentage_float = float(percentage) / 100

        if hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Original:
            child_trade = set_original_child(trade,
                                             child_trade,
                                             designation_date,
                                             hedge_trade_type,
                                             percentage_float)

        elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.External:
            child_trade = update_external_child(trade,
                                                child_trade,
                                                designation_date,
                                                hedge_trade_type,
                                                percentage_float)

        elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Internal:
        	child_trade = set_internal_child(trade,
                                             child_trade,
                                             designation_date,
                                             hedge_trade_type,
                                             percentage_float)

        elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.ZeroBond:
            child_trade = None

        elif hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Hypo:
            child_trade = None

            return child_trade

    except Exception, ex:
        message = 'Error updating child trade for trade [%s]. %s' % (trade.Oid(), ex)
        logger.ELOG(message)
        raise ex


def get_termination_payment_or_premium(terminationReason):
    '''This method determines the payment type to be used for payments added to trades
    on dedesignatio of a Hedge Relationship. The payment type is determined from
    the dedesignation reason specified by the user.

    terminationReason [string] - HedgeConstants.DedesignationReason
    '''

    payment_type = None

    if terminationReason == HedgeConstants.DedesignationReason.Voluntary or\
            terminationReason == HedgeConstants.DedesignationReason.ExernalExpired or\
            terminationReason == HedgeConstants.DedesignationReason.ExternalSold or\
            terminationReason == HedgeConstants.DedesignationReason.ExternalTerminated or\
            terminationReason == HedgeConstants.DedesignationReason.Ineffective or\
            terminationReason == HedgeConstants.DedesignationReason.ReBalanced:

        payment_type = 'Premium'

    elif terminationReason == HedgeConstants.DedesignationReason.OriginalExpired or\
            terminationReason == HedgeConstants.DedesignationReason.OriginalSold or\
            terminationReason == HedgeConstants.DedesignationReason.OriginalTerminated or\
            terminationReason == HedgeConstants.DedesignationReason.PartialDedesignation:

        payment_type = 'Termination Fee'

    return payment_type


def get_value_day(child_trade, dedesignation_date):
    ins = child_trade.Instrument()
    if ins.InsType() in ['Swap', 'CurrSwap', 'IndexLinkedSwap', 'FRA', 'Deposit']:
        value_day = dedesignation_date
    else:
        value_day = child_trade.ValueDay()
    return value_day


def get_close_out_zero(source_trade, dedesignation_date, premium, nominal, buy_or_sell):
    zero_instrument = acm.DealCapturing().CreateNewInstrument('Zero')

    zero_instrument.RegisterInStorage()
    zero_instrument_name = zero_instrument.SuggestName()
    zero_instrument.Name(zero_instrument_name)
    zero_instrument.SpotBankingDaysOffset(0)
    zero_instrument.MtmFromFeed(False)

    zero_instrument.Legs()[0].EndDate(source_trade.Instrument().EndDate())
    zero_instrument.Legs()[0].StartDate(dedesignation_date)

    # regenerate the cashflows
    for leg in zero_instrument.Legs():
        leg.GenerateCashFlows(None)

    zero_instrument.Commit()

    new_trade = acm.FTrade()
    new_trade.Trader(source_trade.Trader())
    new_trade.Currency(source_trade.Currency())
    new_trade.Instrument(zero_instrument)
    new_trade.Text1('Close Zero')
    new_trade.Text2(source_trade.Oid())
    new_trade.Type('Normal')
    new_trade.Status('FO Confirmed')
    new_trade.Portfolio(source_trade.Portfolio())
    new_trade.Acquirer(source_trade.Acquirer())
    new_trade.Counterparty(source_trade.Counterparty())
    new_trade.TradeTime(dedesignation_date)
    new_trade.ValueDay(dedesignation_date)
    new_trade.AcquireDay(dedesignation_date)
    new_trade.Nominal(nominal)
    new_trade.Quantity(-0.00000001 * buy_or_sell)
    new_trade.Premium(premium)
    new_trade.Price(premium / nominal)

    return new_trade

"""******************DEDESIGNATION**********************************************"""

def book_closing_trade_and_payment(tradeOid, dedesignation_date):
    trade = acm.FTrade[tradeOid]
    nominal = -1 * trade.Instrument().ContractSize() * trade.Quantity()
    close_trade = close_out_trade(trade, dedesignation_date, dedesignation_date, nominal, 0, None)
    tpl_zeroing_payment = get_payment_tpl_dirty(close_trade, dedesignation_date)
    add_payment(close_trade, dedesignation_date, dedesignation_date, 'Cash', (tpl_zeroing_payment * -1))
    close_trade.Commit()
    return close_trade

def close_single_trade(trade_ID, dedesignation_date, hedge_trade_type, trade_list, closing_trades):
    trade = acm.FTrade[trade_ID]
    premium = get_trading_manager_column_value(tradeSheetCalcSpace, trade, dedesignation_date, 'Portfolio Realized Deprec Profit and Loss')
    close_trade = book_closing_trade_and_payment(trade_ID, dedesignation_date)
    add_payment(close_trade, dedesignation_date, dedesignation_date, 'Termination Fee', (premium * -1))
    close_trade.Commit()
    trade_list[close_trade.Oid()] = [hedge_trade_type, 100, '']
    closing_trades.Add(close_trade)
    return closing_trades


def close_all_trades_in_trade_list(trade_list, dedesignation_date):

    closing_trades = acm.FSet()

    for tradeOid in trade_list.keys():
        if acm.FTrade[tradeOid]:
            m_type, _, childTradeId = trade_list[tradeOid]

            if m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
                closing_trades = close_single_trade(tradeOid, dedesignation_date, 'Hypo Close', trade_list, closing_trades)

            elif m_type == HedgeConstants.Hedge_Trade_Types.External:
                closing_trades = close_single_trade(childTradeId, dedesignation_date, 'External', trade_list, closing_trades)

            elif m_type == HedgeConstants.Hedge_Trade_Types.Internal:
                closing_trades = close_single_trade(childTradeId, dedesignation_date, 'Internal', trade_list, closing_trades)

            elif m_type == HedgeConstants.Hedge_Trade_Types.ZeroBond:
                closing_trades = close_single_trade(tradeOid, dedesignation_date, 'Zero Bond', trade_list, closing_trades)

            elif m_type == HedgeConstants.Hedge_Trade_Types.Original:
                closing_trades = close_single_trade(childTradeId, dedesignation_date, 'Original Close', trade_list, closing_trades)

    return closing_trades, trade_list


def dedesignate_cashflow_or_nih(hedgeRelation):

    dedesignation_date = hedgeRelation.get_termination_date()
    terminationReason = hedgeRelation.get_termination()
    trade_list = hedgeRelation.get_trades()
    zero_closing_trades = acm.FSet()

    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', dedesignation_date)

    payment_or_premium = get_termination_payment_or_premium(terminationReason)

    chosen_object = acm.FDealPackage.Select("instrumentPackage = '{}'".format(hedgeRelation.get_id()))
    payment_or_premium_value = get_trading_manager_column_value(tradeSheetCalcSpace, chosen_object[0], dedesignation_date, 'Hedge Cap Limit')
    tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    buy_or_sell = 1
    if payment_or_premium_value >= 0.001 or payment_or_premium_value <= -0.001:
        buy_or_sell = payment_or_premium_value / abs(payment_or_premium_value)

    closing_trades, trade_list = close_all_trades_in_trade_list(trade_list, dedesignation_date)
    add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation)

    chosen_trade = acm.FTrade[[t for t in trade_list.keys() if trade_list[t][0]==HedgeConstants.Hedge_Trade_Types.Hypo][0]]
    nominal = 0.01  # Arbitrary. (premium - nominal) is significant

    close_out_zero_1 = get_close_out_zero(chosen_trade, dedesignation_date, 0, nominal, 1)
    close_out_zero_1.Commit()
    add_payment(close_out_zero_1, dedesignation_date, dedesignation_date, 'Termination Fee', (payment_or_premium_value * -1))
    close_out_zero_1.Commit()
    trade_list[close_out_zero_1.Oid()] = ['Close Zero', 100, '']
    zero_closing_trades.Add(close_out_zero_1)

    if payment_or_premium == 'Termination Fee':
        add_trades_to_deal_package(zero_closing_trades, trade_list, hedgeRelation)

    elif payment_or_premium == 'Premium':
        close_out_zero_2 = get_close_out_zero(chosen_trade, dedesignation_date, payment_or_premium_value, nominal, -1)
        close_out_zero_2.Commit()
        trade_list[close_out_zero_2.Oid()] = ['Close Zero', 100, '']
        zero_closing_trades.Add(close_out_zero_2)
        add_trades_to_deal_package(zero_closing_trades, trade_list, hedgeRelation)

    return True


def dedesignate_fairvalue_accrued(hedgeRelation):

    dedesignation_date = hedgeRelation.get_termination_date()
    terminationReason = hedgeRelation.get_termination()
    trade_list = hedgeRelation.get_trades()
    zero_closing_trades = acm.FSet()

    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', dedesignation_date)

    payment_or_premium = get_termination_payment_or_premium(terminationReason)

    payment_or_premium_value = 0
    for tradeOid in trade_list.keys():
        if is_hypo_or_zero_trade(trade_list[tradeOid]):
            trade = acm.FTrade[tradeOid]
            amount = get_trading_manager_column_value(tradeSheetCalcSpace, trade, dedesignation_date, 'Portfolio Cost UPL')
            tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
            payment_or_premium_value += amount

    if payment_or_premium == 'Termination Fee':

        closing_trades, trade_list = close_all_trades_in_trade_list(trade_list, dedesignation_date)
        add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation)

    elif payment_or_premium == 'Premium':

        closing_trades, trade_list = close_all_trades_in_trade_list(trade_list, dedesignation_date)
        add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation)

        chosen_object = acm.FDealPackage.Select("instrumentPackage = '{}'".format(hedgeRelation.get_id()))[0]
        nominal = 0.01  # Arbitrary. (premium - nominal) is significant
        chosen_trade = acm.FTrade[[t for t in trade_list.keys() if trade_list[t][0]==HedgeConstants.Hedge_Trade_Types.Hypo][0]]
        buy_or_sell = chosen_trade.Quantity() / abs(chosen_trade.Quantity())
        nominal = 0.01  # Arbitrary. (premium - nominal) is significant

        #payment_or_premium_value = get_trading_manager_column_value(tradeSheetCalcSpace,chosen_object,dedesignation_date,'Portfolio Cost UPL')

        close_out_zero_1 = get_close_out_zero(chosen_trade, dedesignation_date, payment_or_premium_value, nominal, 1)
        close_out_zero_1.Commit()
        add_payment(close_out_zero_1, dedesignation_date, dedesignation_date, 'Termination Fee', (payment_or_premium_value * -1))
        close_out_zero_1.Commit()
        trade_list[close_out_zero_1.Oid()] = ['Close Zero', 100, '']
        zero_closing_trades.Add(close_out_zero_1)

        add_trades_to_deal_package(zero_closing_trades, trade_list, hedgeRelation)

    return True


def dedesignate_fairvalue_afs(hedgeRelation):

    dedesignation_date = hedgeRelation.get_termination_date()
    terminationReason = hedgeRelation.get_termination()
    trade_list = hedgeRelation.get_trades()
    zero_closing_trades = acm.FSet()

    tradeSheetCalcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', dedesignation_date)

    payment_or_premium = get_termination_payment_or_premium(terminationReason)

    if payment_or_premium == 'Termination Fee':

        closing_trades, trade_list = close_all_trades_in_trade_list(trade_list, dedesignation_date)
        add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation)

    elif payment_or_premium == 'Premium':

        closing_trades, trade_list = close_all_trades_in_trade_list(trade_list, dedesignation_date)
        add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation)

        chosen_object = acm.FDealPackage.Select("instrumentPackage = '{}'".format(hedgeRelation.get_id()))
        nominal = 0.01  # Arbitrary. (premium - nominal) is significant
        chosen_trade = acm.FTrade[[t for t in trade_list.keys() if trade_list[t][0]==HedgeConstants.Hedge_Trade_Types.Hypo][0]]
        buy_or_sell = chosen_trade.Quantity() / abs(chosen_trade.Quantity())
        nominal = 0.01  # Arbitrary. (premium - nominal) is significant
        payment_or_premium_value = get_trading_manager_column_value(tradeSheetCalcSpace, chosen_trade, dedesignation_date, 'Hedge AFS Reserve')
        tradeSheetCalcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')

        close_out_zero_1 = get_close_out_zero(chosen_trade, dedesignation_date, payment_or_premium_value, nominal, 1)
        close_out_zero_1.Commit()
        add_payment(close_out_zero_1, dedesignation_date, dedesignation_date, 'Termination Fee', (payment_or_premium_value * -1))
        #close_out_zero_1.Commit()
        trade_list[close_out_zero_1.Oid()] = ['Close Zero', 100, '']
        zero_closing_trades.Add(close_out_zero_1)

        add_trades_to_deal_package(zero_closing_trades, trade_list, hedgeRelation)

    return True


def is_hypo_or_zero_trade(trade_from_hr_trade_list):
    bool = trade_from_hr_trade_list[0] == 'Hypo' or\
        trade_from_hr_trade_list[0] == 'Hypo Close' or\
        trade_from_hr_trade_list[0] == 'Zero Bond'
    return bool

def add_trades_to_deal_package(closing_trades, trade_list, hedgeRelation):
    # Add closing_trades to the Deal Package
    _, dealPackageName = hedgeRelation.get_deal_package()
    if closing_trades:
        hedgeRelation.set_trades(trade_list)
        hedgeRelation.save()
        for close_trade in closing_trades:
            if dealPackageName:
                dealPackage = acm.FDealPackage[dealPackageName]
                if dealPackage:
                    dealPackage.AddTrade(close_trade)
                    close_trade.Commit()
                    dealPackage.Commit()


def dedesignation(hedgeRelation):
    '''
    Closes the trades in the deal package

    Adds required payments/premiums to trades in a HedgeRelation on dedesignation.

    hedgeRelation [HedgeRelation] - A valid instance of the HedgeRelation class representing
                a hedge relationship that has been dedesignated.
    '''

    hedge_Type = hedgeRelation.get_type()
    dedesignation_date = hedgeRelation.get_termination_date()

    if dedesignation_date:

        if hedge_Type in ['Cash Flow', 'Net Investment Hedge']:
            dedesignated = dedesignate_cashflow_or_nih(hedgeRelation)

        elif hedge_Type == 'Fair Value AC':
            dedesignated = dedesignate_fairvalue_accrued(hedgeRelation)

        elif hedge_Type == 'Fair Value AFS':
            dedesignated = dedesignate_fairvalue_afs(hedgeRelation)
            
    hedgeRelation.touch_trades()
