"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        Billing solution for SBL. The script recalculates and
                        books Loan and Finder Fees for the billing period (i.e. 
                        previous calendar month). The fees are physically 
                        represented by additional trade payments linked to the
                        corresponding sec loan trade.
DESK                 :  SBL PTS
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0102113     Libor Svoboda       Initial Implementation
"""
from collections import defaultdict

import acm
import ael
import sl_functions
from at_ael_variables import AelVariableHandler
from at_time import acm_date
from at_logging import getLogger
from PS_BrokerFeesRates import get_vat_for_date


LOGGER = getLogger(__name__)
CALENDAR = acm.FCalendar['ZAR Johannesburg']

TODAY = acm.Time.DateToday()
FIRST_OF_THIS_MONTH = acm.Time.FirstDayOfMonth(TODAY)
LAST_OF_PREVIOUS_MONTH = acm.Time.DateAddDelta(FIRST_OF_THIS_MONTH, 0, 0, -1)
FIRST_OF_PREVIOUS_MONTH = acm.Time.FirstDayOfMonth(LAST_OF_PREVIOUS_MONTH)

MIN_FEE_TYPE = 'Cash'

CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

DATE_CHOICES = {
    'Date Today': TODAY,
    'First of Previous Month': FIRST_OF_PREVIOUS_MONTH,
    'Last of Previous Month': LAST_OF_PREVIOUS_MONTH,
    'First of This Month': FIRST_OF_THIS_MONTH,
    '1st BD of This Month': CALENDAR.AdjustBankingDays(LAST_OF_PREVIOUS_MONTH, 1),
    '5th BD of This Month': CALENDAR.AdjustBankingDays(LAST_OF_PREVIOUS_MONTH, 5),
}

SBL_FINDER_MAPPING = {
    acm.FParty['SLL SPECIALISED PS FINDER']: 'Specialised Portfolio Services',
    acm.FParty['SLL AG CAPITAL FINDER']: 'AG CAPITAL',
    acm.FParty['SLL OPTIMIZE FIN SERVICE FINDER']: 'Optimize Financial Services (Pty) Limit',
    acm.FParty['SLL AXON ORG FINDER']: 'Axon/ORG',
}

VALID_SBL_STATUS = (
    'FO Confirmed',
    'BO Confirmed',
    'BO-BO Confirmed',
)


def process_consolidated_fee_report(_report, _params, xml_string):
    import xml.etree.cElementTree as ET
    root = ET.fromstring(xml_string)
    table = root.find(".//Table")
    party_level = table.findall("./Rows/Row/Rows/Row")
    for party_row in party_level:
        payment_level = party_row.find("./Rows")
        party_row.remove(payment_level)
    return  ET.tostring(root, "ISO-8859-1")


def regenerate_cashflows(instrument, start_date=''):
    ael_ins = ael.Instrument[instrument.Oid()]
    if not ael_ins:
        raise RuntimeError('Instrument "%s" not found (insaddr: %s).' 
                           % (instrument.Name(), instrument.Oid()))
    sl_cfd = instrument.AdditionalInfo().SL_CFD()
    ael_ins_clone = ael_ins.clone()
    for leg in ael_ins_clone.legs():
        regenerate = False
        fee_rate = leg.fixed_rate
        leg_start = leg.start_day
        regenerate_date = ael.date(start_date) if start_date else leg_start
        nominal_factor_updated = any([(abs(cf.nominal_factor) != 1.0) 
                                        for cf in leg.cash_flows()])
        if leg.type != 'Fixed':
            leg.type = 'Fixed'
            regenerate = True
        if leg.pay_day_method != 'None':
            leg.pay_day_method = 'None'
            regenerate = True
        if sl_cfd and leg.rolling_period != '1d':
            leg.rolling_period = '1d'
            regenerate = True
        if not sl_cfd and leg.rolling_period != '1m':
            leg.rolling_period = '1m'
            regenerate = True
        if (not sl_cfd 
                and leg.rolling_base_day != leg.rolling_base_day.first_day_of_month()):
            base_day = leg_start.first_day_of_month().add_months(1)
            leg.rolling_base_day = base_day
            regenerate = True
        if (sl_cfd or nominal_factor_updated 
                or regenerate or regenerate_date == leg_start):
            leg.regenerate()
            regenerate_date = leg_start
        for cf in leg.cash_flows():
            cf.rate = fee_rate
            if sl_cfd and cf.start_day >= regenerate_date:
                cf_start = acm.Time.DateFromYMD(*cf.start_day.to_ymd())
                nf = sl_functions.CalculateNominalFactor(instrument, cf_start)
                cf.nominal_factor = nf
    ael_ins_clone.commit()
    acm.PollDbEvents()


def get_vat_rate(party, vat_date):
    if party.AdditionalInfo().TAXABLE_STATUS():
        return get_vat_for_date(vat_date)
    return 1.0


def enable_custom_date(ael_input, custom_date_var):
    """Hook enabling custom date."""
    custom_date = ael_variables.get(custom_date_var)
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = TODAY


def enable_tab(ael_input, tab_name):
    """Hook enabling options on a particular tab."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if tab_name in var.label and var is not ael_input:
            var.enabled = enabled


ael_variables = AelVariableHandler()
ael_variables.add(
    'start_date',
    label='Start Date',
    collection=['First of Previous Month', 'Custom Date'],
    default='First of Previous Month',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'start_date_custom'),
    alt='Start date for cashflow selection.'
)
ael_variables.add(
    'start_date_custom',
    label='Custom Start Date',
    cls='date',
    alt='Custom start date.'
)
ael_variables.add(
    'end_date',
    label='End Date',
    collection=['Last of Previous Month', 'Custom Date'],
    default='Last of Previous Month',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'end_date_custom'),
    alt='End date for cashflow selection.'
)
ael_variables.add(
    'end_date_custom',
    label='Custom End Date',
    cls='date',
    alt='Custom end date.'
)
ael_variables.add(
    'valid_from',
    label='Valid From',
    collection=['First of This Month', '1st BD of This Month', 'Custom Date'],
    default='First of This Month',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'valid_from_custom'),
    alt='Valid from date for payments.'
)
ael_variables.add(
    'valid_from_custom',
    label='Custom Valid From',
    cls='date',
    alt='Custom valid from date.'
)
ael_variables.add(
    'pay_day',
    label='Pay Day',
    collection=['Date Today', '1st BD of This Month', 
                '5th BD of This Month', 'Custom Date'],
    default='Date Today',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'pay_day_custom'),
    alt='Pay day for payments.'
)
ael_variables.add(
    'pay_day_custom',
    label='Custom Pay Day',
    cls='date',
    alt='Custom pay day.'
)
ael_variables.add(
    'trade_query',
    label='Base Trade Query',
    cls='FStoredASQLQuery',
    default='',
    alt='Base trade query that is extended at runtime.'
)
ael_variables.add(
    'book_loan_fees',
    label='Book Loan Fee payments',
    collection=[0, 1],
    cls='int',
    hook=lambda x: enable_tab(x, '_Loan Fee'),
)
ael_variables.add(
    'book_finder_fees',
    label='Book Finder Fee payments',
    collection=[0, 1],
    cls='int',
    hook=lambda x: enable_tab(x, '_Finder Fee'),
)
ael_variables.add(
    'first_bd_only',
    label='Execute on 1st business day only',
    collection=[0, 1],
    cls='int',
    default=1,
    alt='Execute script only if date today = 1st business day of the month.'
)
ael_variables.add(
    'regenerate_only',
    label='Regenerate cashflows only',
    collection=[0, 1],
    cls='int',
    default=0,
    alt='Regenerate cashflows only, do not book any payments.'
)
ael_variables.add(
    'roll_payments',
    label='Roll payments',
    collection=[0, 1],
    cls='int',
    default=0,
    alt='Roll pay day of existing payments to today.',
    hook=lambda x: enable_tab(x, '_Roll Payments'),
)
ael_variables.add(
    'borrowers',
    label='Borrowers_Loan Fee',
    cls='FParty',
    default='',
    multiple=True,
    mandatory=False,
    alt='Borrower counterparties.'
)
ael_variables.add(
    'lenders',
    label='Lenders_Loan Fee',
    cls='FParty',
    default='',
    multiple=True,
    mandatory=False,
    alt='Lender counterparties.'
)
ael_variables.add(
    'loan_fee_payment_type',
    label='Payment Type_Loan Fee',
    cls='string',
    default='Loan Fee',
    collection=acm.FEnumeration['enum(PaymentType)'].Enumerators(),
    alt='Loan Fee payment type.'
)
ael_variables.add(
    'finders',
    label='Finders_Finder Fee',
    cls='FParty',
    default='',
    multiple=True,
    mandatory=False,
    alt='Finder counterparties.'
)
ael_variables.add(
    'finder_fee_payment_type',
    label='Payment Type_Finder Fee',
    cls='string',
    default='Finder Fee',
    collection=acm.FEnumeration['enum(PaymentType)'].Enumerators(),
    alt='Finder Fee payment type.'
)
ael_variables.add(
    'roll_payment_query',
    label='Base Payment Query_Roll Payments',
    cls='FStoredASQLQuery',
    default='',
    mandatory=False,
    alt='Base payment query that is extended at runtime.'
)
ael_variables.add(
    'roll_settlement_status',
    label='Settlement Status_Roll Payments',
    cls='string',
    default='',
    collection=acm.FEnumeration['enum(SettlementStatus)'].Enumerators(),
    mandatory=False,
    multiple=True,
    alt='Settlement status to roll.'
)


def get_date(params, param_name):
    date_choice = params[param_name]
    if date_choice == 'Custom Date':
        return acm_date(params[param_name + '_custom'])
    return DATE_CHOICES[date_choice]


def get_finder_cp(trade):
    finder_code = trade.AdditionalInfo().SL_G1FinderCode()
    for counterparty, finder_name in SBL_FINDER_MAPPING.iteritems():
        if finder_code == finder_name:
            return counterparty
    raise RuntimeError('Finder counterparty not found for trade %s.' % trade.Oid())


def select_trades(query, start_date, end_date, borrowers=[], lenders=[], finders=[]):
    if not borrowers and not lenders and not finders:
        return []
    start_date = acm.Time.DateAddDelta(start_date, 0, 0, -1)
    end_date = acm.Time.DateAddDelta(end_date, 0, 0, 1)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', TODAY)
    
    or_node_1 = query.AddOpNode('OR')
    sub_and_node_1 = or_node_1.AddOpNode('AND')
    sub_and_node_2 = or_node_1.AddOpNode('AND')
    sub_and_node_3 = or_node_1.AddOpNode('AND')
    sub_and_node_1.AddAttrNode('Instrument.ExpiryDate', 'GREATER', start_date)
    sub_and_node_1.AddAttrNode('Instrument.ExpiryDate', 'LESS', end_date)
    sub_and_node_2.AddAttrNode('ValueDay', 'GREATER', start_date)
    sub_and_node_2.AddAttrNode('ValueDay', 'LESS', end_date)
    sub_and_node_3.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', end_date)
    sub_and_node_3.AddAttrNode('ValueDay', 'LESS_EQUAL', start_date)
    
    or_node_2 = query.AddOpNode('OR')
    for borrower in borrowers:
        or_node_2.AddAttrNode('AdditionalInfo.SL_G1Counterparty1', 'EQUAL', borrower.Name())
    for lender in lenders:
        or_node_2.AddAttrNode('AdditionalInfo.SL_G1Counterparty2', 'EQUAL', lender.Name())
    for finder in finders:
        finder_name = SBL_FINDER_MAPPING[finder]
        or_node_2.AddAttrNode('AdditionalInfo.SL_G1FinderCode', 'EQUAL', finder_name)
    return query.Select()


def regenerate_instruments(trades, start_date=''):
    for trade in trades:
        instrument = trade.Instrument()
        try:
            regenerate_cashflows(instrument, start_date)
        except:
            LOGGER.exception('Trade %s: failed to regenerate instrument %s.' 
                             % (trade.Oid(), instrument.Name()))
        else:
            LOGGER.info('Trade %s: Regenerated instrument %s.' 
                        % (trade.Oid(), instrument.Name()))


def calculate_loan_fee_values(trades, start_date, end_date, settle_types=['Fixed Rate']):
    end_date = acm.Time.DateAddDelta(end_date, 0, 0, 1)
    payments = defaultdict(lambda: defaultdict(float))
    for trade in trades:
        mfs = trade.MoneyFlows(start_date, end_date)
        for mf in mfs:
            if mf.StartDate() < start_date or mf.EndDate() > end_date:
                continue
            if mf.Type() not in settle_types:
                continue
            try:
                projected = abs(float(mf.Calculation().Projected(CALC_SPACE)))
            except:
                LOGGER.exception('Failed to calculate Projected amount: %s' % mf)
                continue
            payments[trade.Oid()][mf.Currency().Name()] += float(projected)
        if not payments[trade.Oid()]:
            payments[trade.Oid()][trade.Currency().Name()] = 0.0
    return payments


def calculate_finder_fee_values(trades, start_date, end_date):
    end_date_adjusted = acm.Time.DateAddDelta(end_date, 0, 0, 1)
    payments = defaultdict(lambda: defaultdict(float))
    for trade in trades:
        instrument = trade.Instrument()
        quotation_factor = instrument.Quotation().QuotationFactor()
        loan_price = trade.AllInPrice() * quotation_factor
        loan_quantity = abs(trade.Quantity() * instrument.RefValue())
        loan_start_date = (start_date if instrument.StartDate() < start_date 
                           else instrument.StartDate())
        loan_end_date = min(end_date_adjusted, instrument.ExpiryDateOnly())
        duration = acm.Time.DateDifference(loan_end_date, loan_start_date)
        loan_rate = float(trade.AdditionalInfo().SL_G1FinderRate())
        party = get_finder_cp(trade)
        vat_rate = get_vat_rate(party, end_date)
        amount = (loan_price * loan_quantity * loan_rate * vat_rate * duration 
                   / (365.0 * 100))
        payments[trade.Oid()][trade.Currency().Name()] += amount
    return payments


def find_existing_payments(trade, payment_type, currency=None, 
                           valid_from='', party=None, include_min_fee=False):
    query = 'trade=%s and type="%s"' % (trade.Oid(), payment_type)
    if party:
        query += ' and party=%s' % party.Oid()
    if currency:
        query += ' and currency="%s"' % currency.Name()
    if valid_from:
        period_start = acm.Time.FirstDayOfMonth(valid_from)
        period_end = acm.Time.DateAddDelta(period_start, 0, 0, 
                                           acm.Time.DaysInMonth(valid_from)-1)
        query += ' and validFrom>="%s" and validFrom<="%s"' % (period_start, period_end)
    if include_min_fee:
        query += ' and text="Minimum Fee"'
    return acm.FPayment.Select(query)


def revert_payments(trade, payments):
    clone = trade.Clone()
    for payment in payments:
        LOGGER.info('Trade %s: reverting payment %s.' 
                    % (trade.Oid(), payment.Oid()))
        new_payment = clone.CreatePayment()
        new_payment.Apply(payment)
        new_payment.Amount(-payment.Amount())
    try:
        trade.Apply(clone)
        trade.Commit()
    except:
        trade.Undo()
        LOGGER.exception('Trade %s: failed to revert payment.' % trade.Oid())
    else:
        LOGGER.info('Trade %s: payment reverted successfully.' % trade.Oid())


def create_or_update_payment(trade, amount, party, currency, 
                             pay_day, valid_from, payment_type, min_fee=False):
    LOGGER.info('Trade %s: calculated "%s" payment amount %s %s.' 
                % (trade.Oid(), payment_type, amount, currency.Name()))
    if min_fee:
        LOGGER.info('Booking minimum fee.')
        payments = find_existing_payments(trade, payment_type, currency, 
                                          party=party, include_min_fee=True)
    else:
        payments = find_existing_payments(trade, payment_type, currency, valid_from, party)
    LOGGER.info('Trade %s: found %s existing "%s" payments.' 
                % (trade.Oid(), len(payments), payment_type))
    current_amount = sum([payment.Amount() for payment in payments])
    diff_amount = round(amount - current_amount, 5)
    if abs(diff_amount) == 0.0:
        LOGGER.info('Trade %s: payment amount already booked.' % trade.Oid())
        return
    LOGGER.info('Trade %s: creating new payment.' % trade.Oid())
    image = trade.StorageImage()
    payment = image.CreatePayment()    
    payment.Amount(diff_amount)
    payment.Party(party)
    payment.Currency(currency)
    payment.PayDay(pay_day)
    payment.ValidFrom(valid_from)
    payment.Type(payment_type)
    if min_fee:
        payment.Text("Minimum Fee")
    try:
        image.Commit()
    except:
        LOGGER.exception('Trade %s: failed to commit payment. Amount: %s, cp: %s.'
                         % (trade.Oid(), diff_amount, party.Name()))
    else:
        LOGGER.info('Trade %s: payment commited successfully. Amount: %s, cp: %s.'
                    % (trade.Oid(), diff_amount, party.Name()))


def sl_party_and_payment_factor(cp_flag):
    if cp_flag == 'Borrower':
        return sl_functions.sl_borrower, 1
    if cp_flag == 'Lender':
        return sl_functions.sl_lender, -1
    if cp_flag == 'Finder':
        return get_finder_cp, -1
    raise RuntimeError('Invalid cp_flag, only "Borrower", "Lender" or "Finder" allowed.')   


def book_payments(payment_values, valid_from, pay_day, payment_type, cp_flag):
    get_cp, payment_factor = sl_party_and_payment_factor(cp_flag)
    for trade_oid, payment_amounts in payment_values.iteritems():
        trade = acm.FTrade[trade_oid]
        if not trade:
            LOGGER.info('Trade %s not found.' % trade_oid)
            continue
        cp = get_cp(trade)
        if not cp:
            LOGGER.error('No counterparty for trade %s found.' % trade_oid)
            continue
        for curr_name, amount in payment_amounts.iteritems():
            curr = acm.FCurrency[curr_name]
            amount = amount * payment_factor
            create_or_update_payment(trade, amount, cp, curr, 
                                     pay_day, valid_from, payment_type)


def is_full_return(trade, end_date):
    if trade.Instrument().ExpiryDateOnly() > end_date:
        return False
    contract = trade.Contract().Oid()
    trades = [t for t in acm.FTrade.Select('contract=%s' % contract)
              if (t.Status() in VALID_SBL_STATUS 
                  and t.Text1() != 'FULL_RETURN')]
    if not trades:
        return False
    max_expiry = max([t.Instrument().ExpiryDateOnly() for t in trades])
    return trade.Instrument().ExpiryDateOnly() == max_expiry


def apply_minimum_fee(fee_trade, payment_type, valid_from, pay_day, end_date, cp_flag):
    min_fee = fee_trade.Instrument().AdditionalInfo().SL_Minimum_Fee()
    if not is_full_return(fee_trade, end_date):
        min_fee = 0.0
    if not min_fee:
        min_fee_payments = find_existing_payments(fee_trade, MIN_FEE_TYPE, 
                                                  include_min_fee=True)
        if not min_fee_payments:
            return
        booked_min_fee_amount = sum([pay.Amount() for pay in min_fee_payments])
        booked_min_fee_amount = round(booked_min_fee_amount, 5)
        if abs(booked_min_fee_amount) == 0.0:
            return
        LOGGER.info('Minimum fee not applicable for trade %s, reverting existing payments.'
                    % fee_trade.Oid())
        revert_payments(fee_trade, min_fee_payments)
        return
    LOGGER.info('Minimum fee trade found %s (%s).' % (fee_trade.Oid(), min_fee))
    if min_fee < 0:
        LOGGER.error('Minimum fee not booked for %s, negative min fee.'
                     % fee_trade.Oid())
        return
    get_cp, payment_factor = sl_party_and_payment_factor(cp_flag)
    fee_party = get_cp(fee_trade)
    contract = fee_trade.Contract().Oid()
    trades = [t for t in acm.FTrade.Select('contract=%s' % contract)
              if t.Status() in VALID_SBL_STATUS]
    payments = []
    for trade in trades:
        payments.extend(find_existing_payments(trade, payment_type, party=fee_party))
    LOGGER.info('Found %s %s payments: %s.' 
                % (len(payments), payment_type, [pay.Oid() for pay in payments]))
    currencies = list({pay.Currency() for pay in payments})
    if len(currencies) > 1:
        LOGGER.error('Minimum fee not booked for %s, multiple currencies found.'
                     % fee_trade.Oid())
        return
    existing_amount = sum([pay.Amount() for pay in payments])
    existing_currecy = currencies[0]
    LOGGER.info('Current %s amount %s.' % (payment_type, existing_amount))
    min_amount = min_fee * payment_factor
    remaining_amount = 0.0
    if ((payment_factor == 1 and existing_amount >= min_amount)
            or (payment_factor == -1 and existing_amount <= min_amount)):
        LOGGER.info('Minimum fee not necessary for %s, min amount exceeded %s.'
                      % (fee_trade.Oid(), existing_amount))
    else:
        remaining_amount = min_amount - existing_amount
    LOGGER.info('Remaining Minimum fee amount %s.' % remaining_amount)
    create_or_update_payment(fee_trade, remaining_amount, fee_party, existing_currecy, 
                             pay_day, valid_from, MIN_FEE_TYPE, min_fee=True)


def book_minimum_fee(trades, payment_type, valid_from, pay_day, end_date, cp_flag):
    acm.PollDbEvents()
    for trade in trades:
        apply_minimum_fee(trade, payment_type, valid_from, pay_day, end_date, cp_flag)


def book_loan_fees(ael_params):
    start_date = get_date(ael_params, 'start_date')
    end_date = get_date(ael_params, 'end_date')
    valid_from = get_date(ael_params, 'valid_from')
    pay_day = get_date(ael_params, 'pay_day')
    borrowers = ael_params['borrowers']
    lenders = ael_params['lenders']
    if not borrowers and not lenders:
        msg = 'No borrowers or lenders specified.'
        LOGGER.error(msg)
        raise RuntimeError(msg)
    payment_type = ael_params['loan_fee_payment_type']
    LOGGER.info('Booking loan fees for date range %s - %s.' % (start_date, end_date))
    LOGGER.info('Selected payment type: %s.' % payment_type)
    
    query_borrowers = ael_params['trade_query'].Query()
    trades_borrowers = select_trades(query_borrowers, start_date, end_date, borrowers=borrowers)
    LOGGER.info('Selected %s borrower trades.' % len(trades_borrowers))
    
    query_lenders = ael_params['trade_query'].Query()
    trades_lenders = select_trades(query_lenders, start_date, end_date, lenders=lenders)
    LOGGER.info('Selected %s lender trades.' % len(trades_lenders))
    
    regenerate_instruments(trades_borrowers, start_date)
    regenerate_instruments(trades_lenders, start_date)
    if ael_params['regenerate_only']:
        LOGGER.info('Regenerated only.')
        return
    payment_vals_borrowers = calculate_loan_fee_values(trades_borrowers, start_date, end_date)
    payment_vals_lenders = calculate_loan_fee_values(trades_lenders, start_date, end_date)
    book_payments(payment_vals_borrowers, valid_from, pay_day, payment_type, 'Borrower')
    book_payments(payment_vals_lenders, valid_from, pay_day, payment_type, 'Lender')
    book_minimum_fee(trades_borrowers, payment_type, valid_from, pay_day, end_date, 'Borrower')
    book_minimum_fee(trades_lenders, payment_type, valid_from, pay_day, end_date, 'Lender')


def book_finder_fees(ael_params):
    start_date = get_date(ael_params, 'start_date')
    end_date = get_date(ael_params, 'end_date')
    valid_from = get_date(ael_params, 'valid_from')
    pay_day = get_date(ael_params, 'pay_day')
    finders = ael_params['finders']
    if not finders:
        msg = 'No finders specified.'
        LOGGER.error(msg)
        raise RuntimeError(msg)
    payment_type = ael_params['finder_fee_payment_type']
    LOGGER.info('Booking finder fees for date range %s - %s.' % (start_date, end_date))
    LOGGER.info('Selected payment type: %s.' % payment_type)
    
    query = ael_params['trade_query'].Query()
    trades = select_trades(query, start_date, end_date, finders=finders)
    LOGGER.info('Selected %s finder trades.' % len(trades))
    
    regenerate_instruments(trades, start_date)
    if ael_params['regenerate_only']:
        LOGGER.info('Regenerated only.')
        return
    payment_vals = calculate_finder_fee_values(trades, start_date, end_date)
    book_payments(payment_vals, valid_from, pay_day, payment_type, 'Finder')


def select_payments_to_roll(query, parties):   
    if not parties:
        return []
    query.AddAttrNode('PayDay', 'LESS', TODAY)
    or_node = query.AddOpNode('OR')
    for party in parties:
        or_node.AddAttrNode('Party.Name', 'EQUAL', party.Name())
    return query.Select()


def roll_payments(ael_params):
    acm.PollDbEvents()
    settlement_status = ael_params['roll_settlement_status']
    LOGGER.info('Rolling payments without a settlement or with a settlement status %s.'
                % ', '.join([status for status in settlement_status]))
    parties = set(list(ael_params['borrowers'])
                  + list(ael_params['lenders'])
                  + list(ael_params['finders']))
    if not parties:
        msg = 'No parties specified.'
        LOGGER.error(msg)
        raise RuntimeError(msg)
    payments = select_payments_to_roll(ael_params['roll_payment_query'].Query(), parties)
    LOGGER.info('Selected %s payments to roll.' % len(payments))
    for payment in payments:
        settlements = acm.FSettlement.Select('payment=%s' % payment.Oid())
        if settlements and all([s.Status() not in settlement_status for s in settlements]):
            continue
        clone = payment.Clone()
        clone.PayDay(TODAY)
        payment.Apply(clone)
        try:
            payment.Commit()
        except:
            payment.Undo()
            LOGGER.exception('Failed to roll payment %s.' % payment.Oid())
        else:
            LOGGER.info('Payment %s rolled to %s.' % (payment.Oid(), TODAY))


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    if CALENDAR.IsNonBankingDay(None, None, TODAY):
        LOGGER.info('%s is not a business day.' % TODAY)
        LOGGER.info('Completed successfully.')
        return
    if (ael_params['first_bd_only']
            and TODAY != DATE_CHOICES['1st BD of This Month']):
        LOGGER.info('%s is not the 1st business day of the month.' % TODAY)
        LOGGER.info('Completed successfully.')
        return
    if ael_params['book_loan_fees']:
        try:
            book_loan_fees(ael_params)
        except:
            LOGGER.exception('Failed to book loan fees.')
    
    if ael_params['book_finder_fees']:
        try:
            book_finder_fees(ael_params)
        except:
            LOGGER.exception('Failed to book finder fees.')
    
    if ael_params['roll_payments']:
        try:
            roll_payments(ael_params)
        except:
            LOGGER.exception('Failed to roll payments.')
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')

