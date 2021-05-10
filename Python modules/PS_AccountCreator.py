"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2018-10-02                  Tibor Reiss           Initial Implementation

"""


import acm

from at_logging import getLogger
from PS_AssetClasses import (COMMODITIES,
                             SAFEX,
                             YIELDX)
from PS_Names import (CALLACCNT_GENERAL,
                      CALLACCNT_LOAN,
                      CALLACCNT_COMMODITIES,
                      CALLACCNT_SAFEX,
                      CALLACCNT_YIELDX,
                      get_callaccnt_name,
                      get_portfolio_name_by_id)


LOGGER = getLogger()
MINIMUM_PIECE = -1000000000
DAY_COUNT_METHOD = 'Act/365'
CURRENCY = 'ZAR'


def _setup_account_general(insid, start_date, rate_dict, counterparty,
                           prf_name, account_name, reinvest,
                           funding_instype, external_id=None):
    """
    A general function for call/loan account creation.

    It has been heavily inspired by PS_IntFut_CallAccountCreator.

    <rate_dict> can have one of two formats:
        {'type': 'fixed', 'rate': <float>}
        or
        {'type': 'float', 'ref': <ref_name>, 'spread': <float>}

    """
    calendar = acm.FCalendar['ZAR Johannesburg']
    next_bus_day = calendar.AdjustBankingDays(acm.Time.DateToday(), 1)
    day_after_start_date = calendar.AdjustBankingDays(start_date, 1)
    # Make sure that two conditions are met:
    #   1. End date doesn't lie in the past.
    #   2. Start date predates end date.
    end_date = max(next_bus_day, day_after_start_date)

    deposit = acm.FInstrument[insid]
    if deposit:
        LOGGER.info("The instrument {} already exists".format(insid))
        if deposit.ExternalId1():
            LOGGER.info("Updating the external id from {} to {}".format(
                        deposit.ExternalId1(), external_id))
            deposit.ExternalId1(external_id)
            deposit.Commit()
        return None

    LOGGER.info('Creating %s...', insid)
    acm.BeginTransaction()
    try:
        # Instrument
        deposit = acm.FDeposit()
        deposit.Currency(CURRENCY)
        deposit.Name(insid)
        deposit.DayCountMethod(DAY_COUNT_METHOD)
        deposit.SpotBankingDaysOffset(0)
        # this sets the exp_time, which has a higher priority over exp_day,
        # which is set when calling re_rate(...) from ael. If the exp_time
        # is not set, acm (trading manager) uses the exp_day.
        # deposit.ExpiryDate(end_date)
        deposit.ContractSize(1)
        deposit.Quotation('Clean')
        deposit.QuoteType('Clean')
        deposit.OpenEnd('Open End')
        deposit.MinimumPiece(MINIMUM_PIECE)
        deposit.PayOffsetMethod('Business Days')
        if external_id:
            deposit.ExternalId1(external_id)

        # Leg
        leg = deposit.CreateLeg(1)
        leg.LegType('Call Fixed Adjustable')
        leg.Decimals(11)
        leg.StartDate(start_date)
        leg.EndDate(end_date)
        leg.EndPeriodUnit('Days')
        leg.DayCountMethod(DAY_COUNT_METHOD)
        if rate_dict['type'] == 'fixed':
            leg.FixedRate(rate_dict['rate'])
        leg.ResetDayOffset(0)
        leg.ResetType('Weighted')
        leg.ResetPeriod('1d')
        leg.ResetDayMethod('Following')
        leg.Currency(CURRENCY)
        leg.NominalFactor(1)
        leg.Rounding('Normal')
        leg.RollingPeriod('1m')
        leg.RollingPeriodBase(acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(
            start_date, 0, 1, 0)))
        leg.PayDayMethod('Following')
        leg.PayCalendar(calendar)
        leg.FixedCoupon(True)
        leg.NominalAtEnd(True)
        leg.FloatRateFactor(1)
        leg.FixedCoupon(True)
        leg.StartPeriod('-1d')
        leg.Reinvest(reinvest)
        if rate_dict['type'] == 'float':
            deposit.AddInfoValue('CallFloatRef', rate_dict['ref'])
            deposit.AddInfoValue('CallFloatSpread', rate_dict['spread'])
        deposit.Commit()  # Commits both the instrument and the leg.

        # Trade
        trade = acm.FTrade()
        trade.Instrument(deposit)
        trade.Counterparty(counterparty)
        trade.Acquirer('PRIME SERVICES DESK')
        trade.AcquireDay(start_date)
        trade.ValueDay(start_date)
        trade.Quantity(1)
        trade.TradeTime(start_date)
        trade.Currency(CURRENCY)
        trade.Price(0)
        trade.Portfolio(acm.FPhysicalPortfolio[prf_name])
        trade.Type('Normal')
        trade.TradeTime(start_date)
        trade.Status('Simulated')  # To allow for delete in case of rollback.
        trade.AddInfoValue('Funding Instype', funding_instype)
        trade.AddInfoValue('Call_Region', 'BB SANDTON')
        trade.AddInfoValue('Account_Name', account_name)
        trade.Commit()
    
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        LOGGER.exception("Could not create call/loan account {}".format(insid))
        raise e

    deposit = acm.FInstrument[insid]
    if deposit:
        trades = deposit.Trades()
        if trades:
            LOGGER.info('The following trade has been created:{}\n'.format(trades[0].Oid()))
        else:
            raise RuntimeError('Could not create trade!')
    else:
        raise RuntimeError('Could not create deposit!')


def setup_call_account(config):
    """
    Set up the client's call account.

    His call account portfolio needs to be set up already.

    """
    kwargs = {
        'insid': get_callaccnt_name(config['shortName'], CALLACCNT_GENERAL),
        'start_date': config['startDate'],
        'rate_dict': {'type': 'float',
                      'ref': config['generalCallAccountRateIndex'],
                      'spread': config['generalCallAccountSpread']},
        'counterparty': config['counterparty'],
        'prf_name': get_portfolio_name_by_id("CALLACCNT", config['shortName']),
        'account_name': config['shortName'] + '_Margin',
        'reinvest': True,
        'funding_instype': 'Call Prime Brokerage Funding',
    }
    return _setup_account_general(**kwargs)


def setup_loan_account(config):
    kwargs = {
        'insid': get_callaccnt_name(config['shortName'], CALLACCNT_LOAN),
        'start_date': config['startDate'],
        'rate_dict': {'type': 'fixed', 'rate': 0.0},
        'counterparty': config['counterparty'],
        'prf_name': get_portfolio_name_by_id("FINANCING", config['shortName']),
        'account_name': config['shortName'] + '_Loan',
        'reinvest': True,
        'funding_instype': 'Call Prime Brokerage Funding',
    }
    return _setup_account_general(**kwargs)


def setup_commodities_call_account(config):
    kwargs = {
        'insid': get_callaccnt_name(config['shortName'], CALLACCNT_COMMODITIES),
        'start_date': config['startDate'],
        'rate_dict': {'type': 'float',
                      'ref': config['commoditiesCallAccountRateIndex'],
                      'spread': config['commoditiesCallAccountSpread']},
        'counterparty': 'SAFEX',
        'prf_name': get_portfolio_name_by_id("FINANCING", config['shortName']),
        'account_name': 'APD_' + config['shortName'],
        'reinvest': False,
        'funding_instype': 'Call Deposit NonDTI',
        'external_id': config['commoditiesCallAccountCode'],
    }
    return _setup_account_general(**kwargs)


def setup_safex_call_account(config):
    kwargs = {
        'insid': get_callaccnt_name(config['shortName'], CALLACCNT_SAFEX),
        'start_date': config['startDate'],
        'rate_dict': {'type': 'float',
                      'ref': config['safexCallAccountRateIndex'],
                      'spread': config['safexCallAccountSpread']},
        'counterparty': 'SAFEX',
        'prf_name': get_portfolio_name_by_id("FINANCING", config['shortName']),
        'account_name': '%s SAFEX Initial Margin' % config['shortName'],
        'reinvest': False,
        'funding_instype': 'Call Deposit NonDTI',
        'external_id': config['safexCallAccountCode'],
    }
    return _setup_account_general(**kwargs)


def setup_yieldx_call_account(config):
    kwargs = {
        'insid': get_callaccnt_name(config['shortName'], CALLACCNT_YIELDX),
        'start_date': config['startDate'],
        'rate_dict': {'type': 'float',
                      'ref': config['yieldxCallAccountRateIndex'],
                      'spread': config['yieldxCallAccountSpread']},
        'counterparty': 'JSE',
        'prf_name': get_portfolio_name_by_id("FINANCING", config['shortName']),
        'account_name': 'YIELDX_' + config['shortName'],
        'reinvest': False,
        'funding_instype': 'Call Deposit NonDTI',
        'external_id': config['yieldxCallAccountCode'],
    }
    return _setup_account_general(**kwargs)


def setup_call_accounts(config):
    call_account_functions = (
        (setup_call_account, True, 'general call account'),
        (setup_loan_account, True, 'loan account'),
        (setup_commodities_call_account, config[COMMODITIES.key], 'commodities call account'),
        (setup_safex_call_account, config[SAFEX.key], 'safex call account'),
        (setup_yieldx_call_account, config[YIELDX.key], 'yieldx call account'),
    )
    for setup_function, create_account_condition, account_type in call_account_functions:
        if not create_account_condition:
            continue
        if config['dryRun']:
            LOGGER.warning('Skipping the actual creation according to the Dry Run setting.')
            continue
        try:
            setup_function(config)
        except Exception as e:
            LOGGER.exception("Could not create {}".format(account_type))
            raise e
