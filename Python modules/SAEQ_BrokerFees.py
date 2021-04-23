"""-----------------------------------------------------------------------------
PURPOSE                 :Calculates the broker fees for a trade and adds or
                           updates the broker fee payment on the trade
DEPATMENT AND DESK      : SM PCG, Equity
REQUESTER               : Herman Levin
DEVELOPER               : Anil Parbhoo
CR NUMBER               : 6322906
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer           Description
--------------------------------------------------------------------------------
2011-01-21 558419    Francois Truter     Initial Implementation: extracted the
                                         code from FValidation

2011-05-26 665055    Paul Jacot-Guillarmod I've split the initial module, which was one function, into two functions,
                                           so that the broker fee calculation can be used in other procedures.  I've
                                           also added a function which is used to view the broker fee in trading manager.

2011-07-05 6322906   Anil Parbhoo          based the existing calculations only for portfolio add_info('ACS Market Maker')== 'Market Maker'
                                           for remainder of trades the brokerage will be  aflat 2.5 Bps
                                           removed the 20 % discount

2012-02-16 891977    Willie van der Bank   Added alternative calculation for all Stocks and ETFs in commodity portfolio 9923.

2012-02-23 60135     Willie van der Bank   Changed sign of calculation for all Stocks and ETFs in commodity portfolio 9923.

2012-03-28 113367    Jaysen Naicker        Updated JSE fees structure in line with JSE update 01/03/2012

2012-04-19 127129    Willie van der Bank   Changed Commodities Strate fee to 0.

2012-05-15 193158    Heinrich Cronje       Added portfolio 309377 - Myriad, STT to calculation and amended StrateFee Calculations.

2012-06-07 239605    Bhavnisha Sarawan     Added portfolio 309922 - AIB. Fees calculated for buy trades only, StrateFee and IPL are multiplied by 2 for broker fee calculations.

2012-08-03 368953    Jaysen Naicker        Add in provision to perform correct calculation for misdeals.

2013-05-15 XXXXXX    Jan Sinkora           Portfolio 333252 - Albaraka fees calculated the same way as AIB (see change comment from 2012-06-07)
2014-03-25 1830048   Peter Fabian          Added a brand new kind of brokerage fee -- Cash commission from Synth
                                           -- to Stocks in portfolios specified by CashCommissionFromSynth add info
2014-08-31 2210109   Vojtech Sidorin       Update imports to be compatible with new FValidation
2014-10-22 2385994   Jan Sinkora           JSE cost now applies to the whole ACS tree. Strate added to the commodities branch.
2014-09-30           Dmitry Kovalenko      Updated imports to not use deprecated module
2017-04-04 4452477   Libor Svoboda         JSE cost updates 2017.
2017-07-25 4793386   Marcelo Almiron       JSE fees on OD stock trades - Execution premium on ODs should be zero
2018-07-03 CHG1000166517  Libor Svoboda    JSE cost updates 2018.
2018-07-18 CHG1000685757  Libor Svoboda    Algo correction for AIB and Commodities.
2019-06-26 CHG1001930222  Marian Zdrazil   Adding A2X cost algo - FAPE-34
"""
import ael
import acm
import PS_BrokerFeesRates as Rates
from at_portfolio import create_tree
from FBDPCommon import is_acm_object, acm_to_ael
from FValidation_core import DataValidationError


BROKER_NAME = 'ABCAP SECURITIES'
EXCHANGE_NAME = 'JSE'
A2X_EXCHANGE_NAME = 'A2X PTY LTD'
BROKER_FEE_PAYMENT_TYPE = 'Broker Fee'
TRANSACTION_FEE_PAYMENT_TYPE = 'Transaction Fee'
CLEARING_FEE_PAYMENT_TYPE = 'Clearing Fee'
IPL_FEE_PAYMENT_TYPE = 'IPL'

AIB = '309922 - AIB'
COMMODITIES = '9923'

ACS_TREE = 'ABSA CAPITAL SECURITIES'

ACS_AGENCY = 'ACS Cash Equities Agency'
ACS_AGENCY_BARCAP = 'ACS Cash Equities Agency Barcap'
ACS_AGENCY_SYNDICATED = 'ACS Cash Equities Agency Syndicated Tra'

ACS_CASH_EQUITIES_TRADING = 'ACS Cash Equities Trading'
ACS_PRIME_RISK = 'ACS Prime Risk'
ACS_RTM_EQUITIES = 'ACS RTM Equities'
ACS_RTM_PRIME = 'ACS RTM Prime Services'
ACS_RTM_SYNDICATE = 'ACS RTM - Syndicate'
ACS_RTM_STRUCTURED = 'ACS RTM Structured Trading'

AEL_CALENDAR = ael.Calendar['ZAR Johannesburg']


def get_broker_fee_payday(trade_date):
    first_of_next_month = trade_date.first_day_of_month().add_months(1)
    return first_of_next_month.add_days(-1).add_banking_day(AEL_CALENDAR, 5)


def is_subportfolio(prfid, compound):
    tree = create_tree(acm.FPhysicalPortfolio[compound])
    return tree.has(prfid)


def is_acs_rtm_equities(prfid):
    return is_subportfolio(prfid, ACS_RTM_EQUITIES)


def is_acs_rtm_prime(prfid):
    return is_subportfolio(prfid, ACS_RTM_PRIME)


def is_acs_rtm_syndicate(prfid):
    return is_subportfolio(prfid, ACS_RTM_SYNDICATE)


def is_acs_rtm_structured(prfid):
    return is_subportfolio(prfid, ACS_RTM_STRUCTURED)


def is_acs_agency(prfid):
    return any([is_subportfolio(prfid, ACS_AGENCY), 
                is_subportfolio(prfid, ACS_AGENCY_BARCAP),
                is_subportfolio(prfid, ACS_AGENCY_SYNDICATED)])


def is_acs(prfid):
    return any([is_subportfolio(prfid, ACS_TREE), 
                is_subportfolio(prfid, ACS_CASH_EQUITIES_TRADING),
                is_subportfolio(prfid, ACS_PRIME_RISK),
                is_acs_rtm_equities(prfid),
                is_acs_rtm_prime(prfid),
                is_acs_rtm_syndicate(prfid),
                is_acs_rtm_structured(prfid)])


def ReturnBrokerFee(trade):
    """Get broker fee as if it was applied inside FValidation.

    This gets called from adfl.

    """
    if is_acm_object(trade):
        trade = acm_to_ael(trade)

    if trade.insaddr.instype in ('Stock', 'ETF'):
        if trade.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
            if trade.counterparty_ptynbr.ptyid == EXCHANGE_NAME:
                if not(trade.add_info('Broker_Fee_Exclude') and trade.add_info('Broker_Fee_Exclude') == 'Yes'):
                    return CalculateBrokerFeeValue(trade)
    return 0.0


def get_strate_fee(trade_value):
    """Gets the strate fee for the given trade value.

    Note that the minimum fee doesn't equal to min-value * factor,
    therefore the value must be set statically.

    """
    trade_value = min(trade_value, Rates.BROKER_STRATE_UPPER_LIMIT)

    if trade_value < Rates.BROKER_STRATE_LOWER_LIMIT:
        return Rates.BROKER_STRATE_LOWER
    return Rates.BROKER_STRATE_FACTOR * trade_value


def LimitValue(value, cap, floor=0.0):
    """Limit value to the interval set by cap and floor."""
    return min(cap, max(floor, value))


def TradeValue(trade):
    if trade.insaddr.quote_type == 'Per 100 Units':
        trade_value = abs(trade.price / 100.0 * trade.quantity)
    else:
        trade_value = abs(trade.price * trade.quantity)
    return trade_value


def calculate_aib_fee(trade_value, instype='Stock'):
    comm_broker_fee = trade_value * Rates.COMM_BROKER_ACS_FEE_AIB / 100.0
    strate_fee = 2 * get_strate_fee(trade_value)
    broker_ipl_fee = 2 * trade_value * Rates.BROKER_IPL_FACTOR
    broker_stt = 0.0
    if instype == 'Stock':
        broker_stt = trade_value * Rates.BROKER_STT
    
    value = -1.0 * ((comm_broker_fee + strate_fee + broker_ipl_fee)
                  * (1.0 + Rates.VAT_FACTOR) + broker_stt)
    return value


def calculate_commodity_fee(trade_value, instype=''):
    comm_broker_fee = trade_value * Rates.COMM_BROKER_ACS_FEE / 100.0
    strate_fee = get_strate_fee(trade_value)
    broker_ipl_fee = trade_value * Rates.BROKER_IPL_FACTOR
    broker_stt = 0.0
    if instype == 'Stock':
        broker_stt = trade_value * Rates.BROKER_STT
    
    value = -1.0 * ((comm_broker_fee + strate_fee + broker_ipl_fee)
                  * (1.0 + Rates.VAT_FACTOR) + broker_stt)
    return value


def calculate_jse_cost(trade_value, prfid, xtp_type='', acm_trade_date=''):
    trading_value = 0.0
    if not xtp_type in ['OD', 'OP']:
        trading_value = trade_value * Rates.BROKER_TRADING_FACTOR
        trading_value = LimitValue(trading_value, Rates.BROKER_TRADING_CAP, 
                                   Rates.BROKER_TRADING_FLOOR)
    
    clearing_value = trade_value * Rates.BROKER_CLEARING_FACTOR
    clearing_value = LimitValue(clearing_value, Rates.BROKER_CLEARING_CAP, 
                                Rates.BROKER_CLEARING_FLOOR)
    
    broker_ipl_factor = Rates.BROKER_IPL_FACTOR
    fee_suffix = ''
    if is_acs_agency(prfid):
        if not xtp_type in ['XTP_MARKET_HIT', 'OD', 'OP']:
            return 0.0
        broker_ipl_factor = 0.0
        fee_suffix = '_AGENCY'
    elif is_acs_rtm_equities(prfid):
        fee_suffix = '_EQUITIES'
    elif is_acs_rtm_prime(prfid):
        fee_suffix = '_PRIME'
    elif is_acs_rtm_syndicate(prfid) or is_acs_rtm_structured(prfid):
        fee_suffix = '_STRUCTURED'
        
    broker_strate_factor = getattr(Rates, 'BROKER_STRATE' + fee_suffix)
    broker_strate_cap = getattr(Rates, 'BROKER_STRATE_CAP' + fee_suffix)
    custody_fee_factor = getattr(Rates, 'CUSTODY_FEE' + fee_suffix)
    custody_fee_cap = getattr(Rates, 'CUSTODY_FEE_CAP' + fee_suffix)
    other_costs_factor = getattr(Rates, 'OTHER_COSTS' + fee_suffix)
    other_costs_cap = getattr(Rates, 'OTHER_COSTS_CAP' + fee_suffix)
    
    broker_strate_fee = LimitValue(trade_value * broker_strate_factor, 
                                   broker_strate_cap)
    broker_ipl_fee = trade_value * broker_ipl_factor
    custody_fee = LimitValue(trade_value * custody_fee_factor, custody_fee_cap)
    other_costs = LimitValue(trade_value * other_costs_factor, other_costs_cap)
    
    vat_rate = Rates.VAT_RATE
    if acm_trade_date:
        vat_rate = Rates.get_vat_for_date(acm_trade_date)
    
    value = -1.0 * (trading_value + clearing_value + broker_strate_fee
                  + broker_ipl_fee + custody_fee + other_costs 
                  + Rates.BROKER_JSETS) * vat_rate
    return value


def calculate_a2x_cost(trade_value, prfid, xtp_type='', xtp_aggr_type = ''):
    trading_value = 0.0
    if not xtp_type in ['OD', 'OP']:
        if xtp_aggr_type in ['AGGRESSIVE']:
            trading_value = trade_value * Rates.A2X_BROKER_TRADING_AGGRESSOR_FACTOR
        else:
            trading_value = trade_value * Rates.A2X_BROKER_TRADING_PASSIVE_FACTOR
        trading_value = LimitValue(trading_value, Rates.A2X_BROKER_TRADING_CAP)

    clearing_value = trade_value * Rates.A2X_BROKER_CLEARING_FACTOR
    clearing_value = LimitValue(clearing_value, Rates.A2X_BROKER_CLEARING_CAP)

    broker_ipl_factor = Rates.A2X_BROKER_IPL_FACTOR
    broker_ipl_fee = trade_value * broker_ipl_factor

    vat_rate = Rates.VAT_RATE

    value = -1.0 * (trading_value + clearing_value + broker_ipl_fee) * vat_rate
    return value


def calculate_a2x_transaction_cost(trade_value, prfid, xtp_type='', xtp_aggr_type = ''):
    trading_value = 0.0
    if not xtp_type in ['OD', 'OP']:
        if xtp_aggr_type in ['AGGRESSIVE']:
            trading_value = trade_value * Rates.A2X_BROKER_TRADING_AGGRESSOR_FACTOR
        else:
            trading_value = trade_value * Rates.A2X_BROKER_TRADING_PASSIVE_FACTOR
        trading_value = LimitValue(trading_value, Rates.A2X_BROKER_TRADING_CAP)

    vat_rate = Rates.VAT_RATE

    value = -1.0 * trading_value * vat_rate
    return value


def calculate_a2x_clearing_cost(trade_value, prfid, xtp_type=''):
    clearing_value = trade_value * Rates.A2X_BROKER_CLEARING_FACTOR
    clearing_value = LimitValue(clearing_value, Rates.A2X_BROKER_CLEARING_CAP)

    vat_rate = Rates.VAT_RATE

    value = -1.0 * clearing_value * vat_rate
    return value


def calculate_a2x_ipl_cost(trade_value, prfid, xtp_type=''):
    broker_ipl_factor = Rates.A2X_BROKER_IPL_FACTOR
    broker_ipl_fee = trade_value * broker_ipl_factor

    vat_rate = Rates.VAT_RATE
        
    value = -1.0 * broker_ipl_fee * vat_rate
    return value


def get_broker_fee_counterparty(trade):
    prfid = trade.prfnbr.prfid
    if prfid == AIB or is_subportfolio(prfid, COMMODITIES):
        return ael.Party[BROKER_NAME]
    return ael.Party[EXCHANGE_NAME]


def CalculateBrokerFeeValue(trade):
    trade_value = TradeValue(trade)
    prfid = trade.prfnbr.prfid
    instype = trade.insaddr.instype
    xtp_type = trade.add_info('XtpTradeType')
    xtp_aggr_type = trade.add_info('XtpAggressorType')
    value = 0.0
    
    # Applies to the whole ABSA CAPITAL SECURITIES tree.
    if is_acs(prfid):
        counterparty_id = trade.counterparty_ptynbr.ptyid
        # JSE cost.
        if counterparty_id == EXCHANGE_NAME:
            value = calculate_jse_cost(trade_value, prfid, xtp_type)
        # A2X cost.
        elif counterparty_id == A2X_EXCHANGE_NAME:
            counterparty = ael.Party[counterparty_id]
            # Transaction fee
            value = calculate_a2x_transaction_cost(trade_value, prfid, xtp_type, xtp_aggr_type)
            AddOrUpdatePayment(trade, counterparty, value, TRANSACTION_FEE_PAYMENT_TYPE)
            # Clearing & Settlement fee
            value = calculate_a2x_clearing_cost(trade_value, prfid, xtp_type)
            AddOrUpdatePayment(trade, counterparty, value, CLEARING_FEE_PAYMENT_TYPE)
            # Investor Protection Levy (IPL)
            value = calculate_a2x_ipl_cost(trade_value, prfid, xtp_type)
            AddOrUpdatePayment(trade, counterparty, value, IPL_FEE_PAYMENT_TYPE)
            # Broker fee
            value = calculate_a2x_cost(trade_value, prfid, xtp_type, xtp_aggr_type)
            AddOrUpdatePayment(trade, counterparty, value, BROKER_FEE_PAYMENT_TYPE)
              
    #Commodities
    elif xtp_type and is_subportfolio(prfid, COMMODITIES):
        value = calculate_commodity_fee(trade_value, instype)
    #AIB
    elif prfid == AIB and trade.quantity > 0.0:
        value = calculate_aib_fee(trade_value, instype)
    return value


def CashCommissionFromSynth(trade):
    counterparty = ael.Party[BROKER_NAME]
    if not counterparty:
        raise DataValidationError('Could not find counterparty [%s] to add the Commission fee.' % BROKER_NAME)
    if trade.prfnbr.add_info('CashComFromSynth') in ('Yes', 'yes', 'true', 'True', True):
        rate = 7.5 / 100.0 / 100.0
        if trade.prfnbr.add_info('CashComFromSyntRate'):
            rate = float(trade.prfnbr.add_info('CashComFromSyntRate')) / 100.0 / 100.0
        value = - rate * TradeValue(trade)
        AddOrUpdatePayment(trade, counterparty, value, 'Commission')


def AddOrUpdatePayment(trade, counterparty, value, payment_type):
    # update already existing payment
    for payment in trade.payments():
        if payment.type == payment_type and payment.curr == ael.Instrument['ZAR']:
            payment.amount = value
            return
    if not value:
        return

    # create new payment
    payment = ael.Payment.new(trade)
    trade_date = ael.date_from_time(trade.time)
    value_date = trade.value_day
    payment.ptynbr = counterparty
    payment.amount = value
    payment.curr = ael.Instrument['ZAR']
    prfid = trade.prfnbr.prfid
    if payment_type in [BROKER_FEE_PAYMENT_TYPE, CLEARING_FEE_PAYMENT_TYPE, TRANSACTION_FEE_PAYMENT_TYPE, IPL_FEE_PAYMENT_TYPE]:
        if prfid == AIB or is_subportfolio(prfid, COMMODITIES):
            payment.payday = value_date
        else:
            payment.payday = get_broker_fee_payday(trade_date)
    elif is_subportfolio(prfid, COMMODITIES):
        payment.payday = value_date
    else:
        payment.payday = trade_date
    payment.type = payment_type
    payment.valid_from = trade_date


def AddBrokerFee(trade):
    CashCommissionFromSynth(trade)
    counterparty_id = trade.counterparty_ptynbr.ptyid

    if counterparty_id not in [EXCHANGE_NAME, A2X_EXCHANGE_NAME]:
        return
    
    value = CalculateBrokerFeeValue(trade)
    if counterparty_id == EXCHANGE_NAME:
        counterparty = get_broker_fee_counterparty(trade)
        AddOrUpdatePayment(trade, counterparty, value, BROKER_FEE_PAYMENT_TYPE)


