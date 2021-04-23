"""-----------------------------------------------------------------------------
PROJECT         :  Prime Brokerage Project
PURPOSE         :  General functions for prime brokerage
DEPATMENT       :  Prime Services
REQUESTER       :  Francois Henrion
DEVELOPER       :  Paul Jacot-Guillarmod
CR NUMBER       :  666125
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-05-25 666125        Paul J.-Guillarmod Initial Implementation
2011-06-17 685737        Paul J.-Guillarmod Added a function to calculate yesterdays TPL from the pswap
2011-06-07 685737        Francois Truter    Added methods to retrieve trade calculations
2011-07-18 715943        Herman Hoon        Amend the XTPTradeType function
2011-09-14 768482        Rohan van der Walt Grouping functions
2011-11-08 823082        Rohan van der Walt Grouping Closed Out flag and rename
2012-01-26 882208        Anil Parbhoo       Redefine the hasSettled function differently for BsB
2013-02-18 C809119       Peter Kutnik       Updates for Voice fees on Equities
2013-03-08 857456        Peter Basista      Added getCallAccounts function which was previously present in
                                            the module PS_MarginRequirementWarning as _getCallAccounts.
                                            In this function an ASQL query which gets call accounts has
                                            been adjusted so that it will look into more portfolios.
2013-06-13 1092563       Peter Fabian       Added TradeBenchmarkDelta function
2014-04-07 1942759       Rohan van der Walt Update hasSettled grouping logic to include FRAs and Terminated statuses
2014-06-02 2032997       Hynek Urban        Optimize the GetTPLValue function
2015-05-19 2839606       Jakub Tomaga       Function hasSettled modified to cater for Combinations
2015-06-05 ?             Peter Basista      Extract the functionality to determine the fund's short name from
                                            PS_CashReconReport
2015-06-15 ?             Peter Basista      Update the isFinanced function to look at the trade instead of the pf
2015-06-16 ?             Peter Basista      Add several convenience functions which return the counterparty,
                                            call account and loan account of a prime brokerage fund
2015-06-24 ?             Jakub Tomaga       Add a function which returns a list of active prime brokerage funds'
                                            counterparties
2015-06-24 ?             Jakub Tomaga       Add a function which modifies the provided object of type FASQLQuery
2015-07-15 ?             Peter Basista      Add a function for getting the counterparty of a prime brokerage
                                            fund with the provided short name
2016-03-17 3506685       Ondrej Bahounek    Accommodate PBA.
2018-09-10 CHG1000894852 Tibor Reiss        Add new function to determine call deposit sign
2019-10-22 FAPE-91       Tibor Reiss        Memoized function for speed
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
2020-01-29 FAPE-120      Tibor Reiss        Remove code for old funding method
2020-03-12 FAPE-225      Tibor Reiss        Include CDS in hasSettled
-----------------------------------------------------------------------------"""
import Queue
from collections import deque

import acm
import ael

from FBDPCommon import acm_to_ael, is_acm_object
import NamespaceTimeFunctions
import PS_FundingCalculations
import PS_FundingSweeper
from PS_TimeSeriesFunctions import GetTimeSeries, GetTimeSeriesPoint
from at_logging import getLogger
from sl_functions import YTM_To_Price


LOGGER = getLogger(__name__)

CALENDAR = acm.FCalendar['ZAR Johannesburg']
INCEPTION = acm.Time().DateFromYMD(1970, 1, 1)
TODAY = acm.Time().DateToday()
FIRSTOFYEAR = acm.Time().FirstDayOfYear(TODAY)
FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
TWOBUSDAYSAGO = CALENDAR.AdjustBankingDays(TODAY, -2)

# Generate date lists to be used as drop downs in the GUI.
START_DATE_LIST = {'Inception': INCEPTION,
                   'First Of Year': FIRSTOFYEAR,
                   'First Of Month': FIRSTOFMONTH,
                   'PrevBusDay': PREVBUSDAY,
                   'TwoBusinessDaysAgo': TWOBUSDAYSAGO,
                   'TwoDaysAgo': TWODAYSAGO,
                   'Yesterday': YESTERDAY,
                   'Custom Date': TODAY,
                   'Now': TODAY}
START_DATE_KEYS = START_DATE_LIST.keys()
START_DATE_KEYS.sort()

END_DATE_LIST = {'Now': TODAY,
               'TwoDaysAgo': TWODAYSAGO,
               'PrevBusDay': PREVBUSDAY,
               'Yesterday': YESTERDAY,
               'Custom Date': TODAY}
END_DATE_KEYS = END_DATE_LIST.keys()
END_DATE_KEYS.sort()


# SoftBroker aliases which are not used directly in Front Arena
EXCEPTION_SHORT_NAME_MAP = {
    "BLUE_INK": "BLUE_INK_FI"
}


# Clients whose short names are not used directly in Front Arena
EXCEPTION_MAP = {
    'ACU_BLUEINK': 'Acumen_BlueInk_FI',
    'ACU_INVEST': 'Acumen_Invest_FI',
    'MAP501': 'MAP_501',
    'NITRO_TRUST': 'Nitrogen_Trust',
    'MAP250': 'MAP_250_FI',
    'MAP290': 'XFM_MAP290'
}


class NotExactlyOneTrade(RuntimeError):
    """
    Custom exception class which indicates that an instrument
    does not have exactly one relevant trade.
    """
    pass


class NotExactlyOneAlias(RuntimeError):
    """
    Custom exception class which indicates that there is not exactly one
    party alias of type SoftBroker whose name is equal
    to the provided short name of a prime brokerage fund.
    """
    pass


class UnspecifiedValue(ValueError):
    """
    Custom exception class which indicates that
    the desired attribute does not have its value set.
    """
    pass


class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]


def get_pb_fund_counterparties():
    """
    Return a list of active prime brokerage funds' counterparties.
    """
    # Hardcoded
    counterparties_qf = acm.FStoredASQLQuery["pb_funds_counterparties"]
    counterparties_query = counterparties_qf.Query()
    trades = counterparties_query.Select()
    counterparties = [trade.Counterparty() for trade in trades]
    # Removing duplicates
    return list(set(counterparties))


def modify_asql_query(acm_query,
                      field_to_modify,
                      fields_not_flag,
                      new_value=None,
                      new_operator=None):
    """
    Return a temporary (uncommitted) object of type FASQLQuery
    with the modified values and operators
    of all the fields which match the provided specification.
    """
    asql_nodes = acm_query.AsqlNodes().Clone()
    # The initial "not" flags are False
    deck = deque([(False, node) for node in asql_nodes])
    while deck:
        not_flag, node = deck.popleft()
        if node.IsKindOf(acm.FASQLAttrNode):
            attribute_string = node.AsqlAttribute().AttributeString().Text()
            if (attribute_string == field_to_modify
                    and not_flag == fields_not_flag):
                if not new_value is None:
                    node.AsqlValue(new_value)
                if not new_operator is None:
                    node.AsqlOperator(new_operator)
        elif node.IsKindOf(acm.FASQLOpNode):
            not_flag = node.Not()
            child_nodes = node.AsqlNodes()
            deck.extend([(not_flag, node) for node in child_nodes])
    query_clone = acm_query.Clone()
    query_clone.AsqlNodes(asql_nodes)
    return query_clone


def add_currency_to_query(acm_query, curr):
    acm_query = modify_asql_query(
        acm_query,
        'Currency.Name',
        False,
        new_value=curr)
    return acm_query


def add_ff_flag_to_query(acm_query):
    """
    Return a temporary (uncommitted) object of type FASQLQuery
    modified in a way that it selects the fully funded positions.

    By default, sweeping class query folders select the financed positions.
    """
    acm_query = modify_asql_query(
        acm_query,
        "AdditionalInfo.PB_Fully_Funded",
        False,
        new_value=1)  # value "true"
    acm_query = modify_asql_query(
        acm_query,
        "Portfolio.AdditionalInfo.PS_FullyFunded",
        False,
        new_value=1,  # value "true"
        new_operator=0)  # operator "equal to"
    return acm_query


@Memoize
def get_pb_fund_pswaps_memo(cp_name):
    return get_pb_fund_pswaps(acm.FParty[cp_name])

def get_pb_fund_pswaps(acm_counterparty):
    """
    Return a list of all portfolio swaps
    belonging to the prime brokerage fund
    specified the provided counterparty.
    """
    # Hardcoded
    pswap_qf = acm.FStoredASQLQuery["pb_fund_pswaps"]
    pswap_query = pswap_qf.Query()
    modified_query = modify_asql_query(
        pswap_query,
        "Counterparty.Name",
        False,
        new_value=acm_counterparty.Name())
    trades = modified_query.Select()
    portfolio_swaps = [trade.Instrument() for trade in trades]
    # Removing duplicates
    return list(set(portfolio_swaps))


def get_pb_fund_counterparty(shortname):
    """
    Return a counterparty representing the prime brokerage fund
    with the provided short name.
    """
    # reverse dictionary lookup
    try:
        # We suppose that the value will either be unique
        # or not present at all.
        shortname = next((key for key, value
                     in EXCEPTION_SHORT_NAME_MAP.iteritems()
                     if value == shortname))
    except StopIteration:
        pass
    candidate_aliases = acm.FPartyAlias.Select(
        "type = 'SoftBroker' and alias = '{0}'".format(shortname))
    if not candidate_aliases:
        candidate_aliases = acm.FPartyAlias.Select(
            "type = 'SoftBroker' and alias = 'Position_View_{0}'".format(
                shortname))

    if len(candidate_aliases) != 1:
        exception_message = ("There is not exactly one party alias "
                             "of type SoftBroker and name '{0}'. "
                             "Instead, there are {1} of them.").format(
                                 shortname, len(candidate_aliases))
        raise NotExactlyOneAlias(exception_message)
    return candidate_aliases[0].Party()


def get_pb_fund_shortname(acm_counterparty):
    """
    Return the short name of a prime brokerage fund
    represented by the provided counterparty.
    """
    alias_prefix = "Position_View_"
    for alias in acm_counterparty.Aliases():
        if alias.Type().Name() == "SoftBroker":
            alias_name = alias.Name()
            if alias_name.startswith(alias_prefix):
                alias_name = alias_name[len(alias_prefix):]
            return EXCEPTION_SHORT_NAME_MAP.get(
                alias_name, alias_name)


def get_instrument_trade(acm_instrument, ignored_statuses=None):
    """
    Return the only relevant trade on the provided instrument.

    Raise an exception if there is not exactly one such trade.
    """
    trades = acm_instrument.Trades()
    if ignored_statuses is None:
        ignored_statuses = ["Simulated", "Terminated", "Void"]
    relevant_trades = [trade for trade in trades
                       if trade.Status() not in ignored_statuses]
    if len(relevant_trades) != 1:
        exception_message = ("Instrument '{0}' does not have "
                             "exactly one relevant trade!".format(
                                 acm_instrument.Name()))
        raise NotExactlyOneTrade(exception_message)
    return relevant_trades[0]


def get_pb_trade_ff_flag(acm_trade):
    """
    Return True if the provided prime brokerage trade is fully funded,
    return False if it is financed.
    Otherwise return None.
    """
    return acm_trade.AdditionalInfo().PB_Fully_Funded()


def get_pb_pswap_ff_flag(acm_pswap):
    """
    Return True if the provided prime brokerage portfolio swap is fully funded,
    return False if it is financed.
    Otherwise return None.
    """
    return acm_pswap.AdditionalInfo().PB_PS_Fully_Funded()


def get_pb_call_account(acm_counterparty, currency="ZAR"):
    """
    Return the call account instrument linked to the Prime Brokerage fund
    represented by the provided counterparty.
    
    PBA version:
        - counterparty can have more call accounts which differ in currency
        - return call account with the given currency
    """
    if currency == "ZAR":
        return acm_counterparty.AdditionalInfo().PB_Call_Account()
    else:
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Counterparty.Oid', 'EQUAL', acm_counterparty.Oid())
        for status in ['Void', 'Confirmed Void', 'Simulated', 'Terminated']:
            query.AddAttrNode('Status', 'NOT_EQUAL',
                acm.EnumFromString('TradeStatus', status))
        query.AddAttrNode('Instrument.InsType', 'EQUAL',
            acm.EnumFromString('InsType', 'Deposit'))
        query.AddAttrNode('Currency.Name', 'EQUAL', currency)
        result = query.Select()
        if len(result) > 1:
            LOGGER.warning("WARNING: More than 1 call account found for cpty '{0}' and currency '{1}'" \
                .format(acm_counterparty.Name(), currency))
        return query.Select()[0].Instrument()


def get_pb_loan_account(acm_counterparty):
    """
    Return the loan account instrument linked to the Prime Brokerage fund
    represented by the provided counterparty.
    """
    return acm_counterparty.AdditionalInfo().PB_Loan_Account()


def get_pb_reporting_portfolio(acm_counterparty):
    """
    Return the reporting portfolio of the Prime Brokerage fund
    represented by the provided counterparty.
    """
    return acm_counterparty.AdditionalInfo().PB_Reporting_Prf()


def get_pb_collateral_portfolio(acm_counterparty):
    """
    Return the collateral portfolio of the Prime Brokerage fund
    represented by the provided counterparty.
    """
    return acm_counterparty.AdditionalInfo().PB_Collateral_Prf()


def get_trades(instrument_class, portfolio_name):
    """Return instrument class trades from given portfolio."""
    query = acm.FStoredASQLQuery[instrument_class]
    query = modify_asql_query(
        query.Query(),
        "Portfolio.Name",
        False,
        new_value=portfolio_name)
    return list(query.Select())


def link_portfolios(parent_portfolio, child_portfolio):
    """
    Make the provided child portfolio
    a direct descendant of the provided parent portfolio.
    """
    portfolio_link = acm.FPortfolioLink()
    portfolio_link.OwnerPortfolio(parent_portfolio)
    portfolio_link.MemberPortfolio(child_portfolio)
    portfolio_link.Commit()


def _RemoveTime(date):
    """ Remove the time from an acm datetime and return the date.
    """
    return acm.Time().DateFromYMD(*acm.Time().DateToYMD(date))

def SetAdditionalInfo(entity, addInfoName, addInfoValue):
    """ Sets an additional info field on a given entity.
    """
    if is_acm_object(entity):
        entity = acm_to_ael(entity)
    entityClone = entity.clone()

    for addInfo in entity.additional_infos():
        if addInfo.addinf_specnbr.field_name == addInfoName:
            newAddInfo = addInfo.clone()
            break
    else:
        newAddInfo = ael.AdditionalInfo.new(entityClone)
        newAddInfo.addinf_specnbr = ael.AdditionalInfoSpec[addInfoName]

    newAddInfo.value = str(addInfoValue)
    try:
        newAddInfo.commit()
        entityClone.commit()
    except:
        LOGGER.exception('Error: Could not update additional info value %s' % (addInfoName))

def DateGenerator(startDate, endDate):
    """ Date iterator from startDate to endDate inclusive.
    """
    nextDate = startDate
    while nextDate <= endDate:
        yield nextDate
        nextDate = acm.Time().DateAddDelta(nextDate, 0, 0, 1)


def GetFundingRate(instrument, portfolio_swap, date):
    # Get the funding rate for a given position on a given date from the portfolio swap.
    funding_rate = 0.0
    funding_legs = PS_FundingCalculations.GetAllFundingLegs(portfolio_swap, instrument)
    for leg in funding_legs:
        cash_flow = PS_FundingSweeper.GetFloatCashFlow(leg, 'Funding')
        if cash_flow:
            resets = cash_flow.Resets()
            if resets and resets[0].ResetType() == "Return":
                portfolio = portfolio_swap.FundPortfolio()
                currency = portfolio_swap.Currency().Name()
                query = PS_FundingSweeper.FundingQuery(portfolio, currency)
                query.AddAttrNode("Instrument.Name", "EQUAL", instrument.Name())
                calendar = acm.FCalendar["ZAR Johannesburg"]
                previous_banking_day = calendar.AdjustBankingDays(date, -1)
                instrument_val_ends = PS_FundingSweeper.TradingManagerSweeper(query, previous_banking_day,
                                                                              ["Portfolio Value End"], False)
                for ins, valEndList in instrument_val_ends.iteritems():
                    val_end = valEndList[0]
                    break
                funding_end = None
                for reset in resets:
                    if reset.Day() == date:
                        funding_end = reset
                        funding_start = PS_FundingCalculations.GetReset(cash_flow, "Return", previous_banking_day, False, True)
                        break
                if funding_end:
                    funding = funding_end.FixingValue()
                    time_diff = 1
                    if funding_start:
                        funding -= funding_start.FixingValue()
                        time_diff = acm.Time().DateDifference(funding_end.Day(), funding_start.Day())
                    try:
                        funding_rate = funding / time_diff / val_end * 36500.0
                    except:
                        funding_rate = 0.0
    return funding_rate


# 21/11/2013 Anwar - cache strategy for tm column
__fundingDict = acm.FDictionary()
def TMOvernightFundingRate(valEnd, portfolioSwap, date):
    """ Returns the overnight funding rate for a given instrument on a given date.  This function
        is called from ADFL to be viewed in a trading manager column.
    """
    key = '%s|%s|%s' % (portfolioSwap.Oid(), valEnd < 0, str(date))
    if not __fundingDict.HasKey(key):
        fundingIndexName = portfolioSwap.add_info('PSONPremIndex')    
        if fundingIndexName:        
            fundingIndex = acm.FInstrument[fundingIndexName]
            if valEnd < 0:
                __fundingDict[key] = PS_FundingSweeper.GetOvernightFundingRate(fundingIndex, date, 'Short')
            else:
                __fundingDict[key] = PS_FundingSweeper.GetOvernightFundingRate(fundingIndex, date, 'Long')
        else:
            __fundingDict[key] = 0.0
        
    return __fundingDict[key]

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber

# 21/11/2013 Anwar - cache for tm performance
__fundingSpreadDict = acm.FDictionary()
def OvernightFundingSpread(valEnd, portfolioSwap, date):
    key = '%s|%s|%s' % (portfolioSwap.Oid(), valEnd < 0, str(date))
    
    if not __fundingSpreadDict.HasKey(key):
        spread = 0.0
        fundingIndexName = portfolioSwap.add_info('PSONPremIndex')
        if fundingIndexName:
            fundingIndex = acm.FInstrument[fundingIndexName]
            market = acm.FParty['internal']
            spreadPrice = GetInstrumentPrice(fundingIndex, date, market)
            if valEnd < 0:
                try:
                    spread = spreadPrice.Ask()
                except:
                    spread = 0.0
            else:
                try:
                    spread = spreadPrice.Bid()
                except:
                    spread = 0.0
            if not _isNumber(spread):
                spread = 0.0
        __fundingSpreadDict[key] = spread
    return __fundingSpreadDict[key]

# 21/11/2013 Anwar - cache for tm performance
__baseDict = acm.FDictionary()
def OvernightBaseRate(portfolioSwap, date):
    key = '%s|%s' % (portfolioSwap.Oid(), str(date))
    if not __baseDict.HasKey(key):
        fundingIndexName = portfolioSwap.add_info('PSONPremIndex')
        if fundingIndexName:
            fundingIndex = acm.FInstrument[fundingIndexName]
            underlyingIndex = fundingIndex.Underlying()
            if not underlyingIndex:
                underlyingIndex = fundingIndex
            market = acm.FParty['internal']
            underlyingPrice = GetInstrumentPrice(underlyingIndex, date, market)
            if underlyingPrice:
                __baseDict[key] = underlyingPrice.Settle()
            else:
                __baseDict[key] = 0.0
        else:
            __baseDict[key] = 0.0
    return __baseDict[key]

# 20/11/2013 Anwar - overnight report run can be optimized by looking at a cached value
__instrumentPriceDict = acm.FDictionary()
def GetInstrumentPrice(instrument, date, market):
    """ Return the price object of an instrument for a particular date and market
    """
    key = '%s|%s|%s' % (instrument.Oid(), market.Oid(), str(date))
    if not __instrumentPriceDict.HasKey(key):
        price = acm.FPrice.Select("instrument = %i and market = %i and day = %s" % (instrument.Oid(), market.Oid(), str(date)))
        if price:
            __instrumentPriceDict[key] = price.At(0)
        else:
            __instrumentPriceDict[key] = 0.0
    return __instrumentPriceDict[key]
    
def GetMtMPrice(instrument, date):
    market = acm.FParty['internal']
    mtmPrice = GetInstrumentPrice(instrument, date, market)
    if mtmPrice:
        return mtmPrice.Settle()
    else:
        return 0.0

# Front Upgrade 2013.3 -- rerouting the function to common function
def YieldToPrice(bond, date, bondYield, toDirty=True, isSettlementDate=True):
    return YTM_To_Price(bond, date, bondYield, toDirty, isSettlementDate)

def YieldToPrice_old(bond, date, bondYield, toDirty=True, isSettlementDate=True):
    """ Convert a bonds yield to price. For a given trade/settlement date, return the
        clean or dirty price for the given bondYield for settlement
    """
    denominatedvalue = acm.GetFunction('denominatedvalue', 4)
    price = denominatedvalue(bondYield, acm.FCurrency['ZAR'], None, date)
    leg = bond.Legs().At(0)
    staticLegInfo = leg.StaticLegInformation(bond, date, None)
    legInf = leg.LegInformation(date)

    if isSettlementDate:
        result = bond.QuoteToRoundedCleanUnitValue(price, date, date, toDirty, [legInf], bond.Quotation(), 1.0, 0.0)
    else:
        result = bond.QuoteToRoundedCleanUnitValue(price, date, toDirty, [legInf], [staticLegInfo], bond.Quotation(), 1.0, 0.0)
    return result.Number() * 100

def GetUnsettledCash(tradeList, date):
    """ Sum up all the unsettled premiums and trade payments for a given date.
    """
    unsettledCash = 0
    for trade in tradeList:
        if trade.Status() not in ['Void', 'Simulated'] and _RemoveTime(trade.TradeTime()) <= date:
            if date < trade.ValueDay():
                unsettledCash += trade.Premium()

            for payment in trade.Payments():
                if date < payment.PayDay():
                    unsettledCash += payment.Amount()
    return unsettledCash

def TotalPnL(callAccount, date):
    """ Total of the PnL cashflows for a given date (these are the cashflows that get generated by the call account sweeping process
        and can be identified by the fact that the PSCashType additional-info is stamped with a portfolio swap name.)
    """
    totalPnL = 0.0
    leg = callAccount.Legs().At(0)
    for cashFlow in leg.CashFlows():
        if cashFlow.CashFlowType() == 'Fixed Amount' and cashFlow.add_info('PSCashType'):
            if cashFlow.StartDate() and cashFlow.StartDate() == date:
                totalPnL += cashFlow.FixedAmount()
            elif not cashFlow.StartDate() and cashFlow.PayDate() == date:
                totalPnL += cashFlow.FixedAmount()

    return totalPnL

def GetDailyDeposit(callAccount, date, depositType):
    """ Return the total daily deposits of type depositType.  These will include SBL Deposits,
        Sundry Deposits and Margin Deposits.
    """
    depositTotal = 0.0
    leg = callAccount.Legs().At(0)
    for cashFlow in leg.CashFlows():
        if cashFlow.CashFlowType() == 'Fixed Amount' and cashFlow.add_info('PS_DepositType') == depositType:
            if cashFlow.StartDate() and cashFlow.StartDate() == date:
                depositTotal += cashFlow.FixedAmount()
            elif not cashFlow.StartDate() and cashFlow.PayDate() == date:
                depositTotal += cashFlow.FixedAmount()

    return depositTotal

def CapitalisedInterest(callAccount, date):
    legs = callAccount.Legs()
    if not legs:
        return 0
    leg = callAccount.Legs().At(0)
    for cashFlow in leg.CashFlows():
        if cashFlow.CashFlowType() == 'Call Fixed Rate Adjustable' and cashFlow.PayDate() == date:
            amount = acm.GetCalculatedValueFromString(cashFlow, acm.GetDefaultContext(), "projectedCashFlow", None).Value()
            if amount:
                return -amount.Number()
            else:
                return 0
    return 0

def GetTPLValue(portfolioSwap, instrument, date):
    """ Get the TPL value for the given date stored on the resets of the Position Total Return leg
        of the portfolioSwap - the blitz version.
    """
    if portfolioSwap == None:
        return 0.0
    instrumentName = instrument.Name()
    legs = acm.FLeg.Select('instrument="%s" indexRef="%s" legType="Total Return"' % (portfolioSwap.Name(), instrumentName))
    for leg in legs:
        for cashflow in leg.CashFlows():  # No need to optimize via SQL - typically, there's just a single cashflow
            cashflow_type = cashflow.add_info('PS_FundWarehouse')
            if cashflow_type and cashflow_type != 'TPL':
                continue
            resets = acm.FReset.Select('cashFlow=%i resetType="Return" day="%s"' % (cashflow.Oid(), date))
            if resets.Size() > 0:
                return resets[0].FixingValue()
    return 0.0

def ExternalDeposits(callAccount, date):
    """ Total external deposits made on the call account for a given date.  The internal cashFlows have their additional-infos
        stamped with the instrument type and portfolio swap name.
    """
    externalDeposit = 0.0
    leg = callAccount.Legs().At(0)
    for cashFlow in leg.CashFlows():
        if cashFlow.CashFlowType() == 'Fixed Amount' and not cashFlow.add_info('PSCashType'):
            if cashFlow.StartDate() and cashFlow.StartDate() == date:
                externalDeposit += cashFlow.FixedAmount()
            elif not cashFlow.StartDate() and cashFlow.PayDate() == date:
                externalDeposit += cashFlow.FixedAmount()

    return externalDeposit

def NAVDeposits(callAccount, date):
    """ Calculates the cashflows that includes interest and external deposits, up to end date.
    """
    externalDeposit = 0.0
    leg = callAccount.Legs().At(0)
    for cashFlow in leg.CashFlows():
        # Use start date instead of pay date to work for backdates
        if (cashFlow.PayDate() <= date  or cashFlow.StartDate() <= date) and cashFlow.CashFlowType() != 'Redemption Amount' and cashFlow.add_info('Prvnt_CF_Settlement') != 'Yes':
            aelCF = ael.CashFlow[cashFlow.Oid()]
            externalDeposit += aelCF.projected_cf()
    return externalDeposit

def TradeYieldDelta(trade):
    """ Calculate the interest rate yield delta for a trade.
    """
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    yieldDelta = trade.Calculation().InterestRateYieldDelta(calcSpace).Number()
    return yieldDelta

def TradeBenchmarkDelta(trade):
    """ Calculate the interest rate benchmark delta for a trade.
    """
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    benchmarkDelta = trade.Calculation().InterestRateBenchmarkDelta(calcSpace).Number()
    return benchmarkDelta

def _readDefaultExtensionAttribute(obj, extensionAttribute):
    defaultContext = acm.GetDefaultContext()
    evaluator = acm.GetCalculatedValue(obj, defaultContext, extensionAttribute)
    if not evaluator:
        raise Exception('Could not load extension attribute [%s]' % extensionAttribute)
    else:
        return evaluator.Value()

def GetPositionFactorFromTrade(trade):
    EXTENSION_ATTRIBUTE = 'propPositionFactor'
    try:
        return _readDefaultExtensionAttribute(trade, EXTENSION_ATTRIBUTE)
    except Exception, ex:
        raise Exception('Could not get Position Factor for trade %i, extension attribute [%s]: %s' % \
            (trade.Oid(), EXTENSION_ATTRIBUTE, ex))

def GetExecutionFeeFromTrade(trade):
    EXTENSION_ATTRIBUTE = 'dailyExecutionFeeCalculation'
    try:
        return _readDefaultExtensionAttribute(trade, EXTENSION_ATTRIBUTE)
    except Exception, ex:
        raise Exception('Could not get Execution Fee for trade %i, extension attribute [%s]: %s' % \
            (trade.Oid(), EXTENSION_ATTRIBUTE, ex))

def GetSecuritiesTransferTaxFromTrade(trade):
    EXTENSION_ATTRIBUTE = 'securitiesTransferTaxCalculation'
    try:
        return _readDefaultExtensionAttribute(trade, EXTENSION_ATTRIBUTE)
    except Exception, ex:
        raise Exception('Could not get Securities Transfer Tax for trade %i, extension attribute [%s]: %s' % \
            (trade.Oid(), EXTENSION_ATTRIBUTE, ex))

def XTPTradeType(trade):
    TYPE_DICT = {
        None:'DMA',
        '': 'DMA',
        'DMA':'DMA',
        'XTP_MARKET_HIT':'DMA',
        'TRADE REPORT':'Trade Report',
        'OD':'Trade Report',
        'OP':'Trade Report',
        'BK':'Trade Report',
        'CF':'Trade Report',
        'OX':'Trade Report',
        'PF':'Trade Report',
        'WX':'Trade Report',
        'TX':'Trade Report',
        'PC':'Trade Report',
        'GU':'Trade Report',

        'VOICE':'Voice'}
    if trade.Instrument().InsType() in ['Stock', 'ETF', 'CFD']:
        tradeType = trade.add_info('XtpTradeType')
        if tradeType:
            tradeType = tradeType.upper()
        try:
            return TYPE_DICT[tradeType]
        except:
            return 'Unknown'
    else:
        return 'None'

def XTPTradeTypeAel(trade, *rest):
    acmTrade = acm.FTrade[trade.trdnbr]
    return XTPTradeType(acmTrade)

def getStrategy(self):
    """Get current Portfolio's PS_Strategy additional info value"""
    portfolio = self.Portfolio()
    stratName = portfolio.AdditionalInfo().PS_StrategyName()
    if stratName != "":
        return stratName
    else:
        return "DefaultStrategy"


def hasSettled(self):
    nst = acm.Time()
    ins = self.Instrument()

    if ins.InsType() in ['Future/Forward', 'Option', 'Swap', 'Cap', 'Floor',
                         'FRA', 'Deposit', 'CurrSwap', 'CreditDefaultSwap']:
        if self.AdditionalInfo().PS_ClosedOut() == True:
            return "Expired or Closed Out"

    if ins.InsType() in ['Future/Forward', 'Option', 'Swap', 'FRA',
                         'CurrSwap', 'CreditDefaultSwap']:
        if self.Status() == "Terminated":
            return "Expired or Closed Out"
        if ins.PayOffsetMethod() == 'Business Days':
            cal = ins.Currency().Calendar()
            settle_date = cal.AdjustBankingDays(ins.ExpiryDateOnly(), ins.PayDayOffset())
        elif ins.PayOffsetMethod() == 'Calendar Days':
            settle_date = nst.DateAddDelta(ins.ExpiryDateOnly(), 0, 0, 1)
        if self.Status() == "Terminated" or nst.DateToday() >= settle_date:
            return "Expired or Closed Out"
        return "Live"

    elif ins.InsType() in ['BuySellback', 'BasketRepo/Reverse']:
        settle_date = None
        if ins.PayOffsetMethod() == 'Business Days':
            cal = ins.Currency().Calendar()
            expiry_plus1 = nst.DateAddDelta(ins.ExpiryDateOnly(), 0, 0, 1)
            settle_date = cal.AdjustBankingDays(expiry_plus1, ins.PayDayOffset())
        elif ins.PayOffsetMethod() == 'Calendar Days':
            settle_date = nst.DateAddDelta(ins.ExpiryDateOnly(), 0, 0, 2)
        if settle_date and nst.DateToday() >= settle_date:
            return "Expired or Closed Out"
        return "Live"
    
    elif ins.InsType() in ['Combination', 'Deposit']:
        if ins.IsExpired():
            return "Expired or Closed Out"
        return "Live"

    return "Live"


def get_trade_ff_text(acm_trade):
    """
    Return a text indicating whether the provided trade
    is fully funded, financed or does not fit into any of these categories.
    It is used by a custom grouper.
    """
    value = get_pb_trade_ff_flag(acm_trade)
    if value == None:
        # FIXME: Temporary fallback. To be removed.
        trade_portfolio = acm_trade.Portfolio()
        value = trade_portfolio.AdditionalInfo().PS_FullyFunded()
        if not value == True:
            value = False
    if value == True:
        return "Fully Funded"
    elif value == False:
        return "Financed"
    else:
        return "Unspecified"

def get_pswap_ff_text(acm_pswap):
    """
    Return a text indicating whether the provided portfolio swap
    is fully funded, financed or does not fit into any of these categories.
    """
    value = get_pb_pswap_ff_flag(acm_pswap)
    if value == True:
        return "Fully Funded"
    elif value == False:
        return "Financed"
    else:
        return "Unspecified"

def getTotalMarginRequirement(dep):
    nst = acm.Time()
    Eqts = GetTimeSeries('PS_Margin_Equity', dep)
    FIts = GetTimeSeries('PS_Margin_FI', dep)
    Creditts = GetTimeSeries('PS_Margin_Credit', dep)
    eqMargin, fiMargin, creditMargin = 0, 0, 0
    # Front Upgrade 2013.3 -- Value amended to TimeValue; method name changed
    try:
        eqMargin = GetTimeSeriesPoint(Eqts, nst.DateToday()).TimeValue()
    except:
        pass
    try:
        fiMargin = GetTimeSeriesPoint(FIts, nst.DateToday()).TimeValue()
    except:
        pass
    try:
        creditMargin = GetTimeSeriesPoint(Creditts, nst.DateToday()).TimeValue()
    except:
        pass
    return eqMargin + fiMargin + creditMargin

def getCallAccounts(counterparty):

    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Counterparty.Oid', 'EQUAL', counterparty.Oid())

    ca_subtree = query.AddOpNode('OR')
    ca_subtree.AddAttrNode('Portfolio.Name', 'RE_LIKE_NOCASE',
        'PB_CALL_MARGIN_.+')
    ca_subtree.AddAttrNode('Portfolio.Name', 'RE_LIKE_NOCASE',
        'PBA?_CALLACCNT_.+')

    query.AddAttrNode('Instrument.InsType', 'EQUAL',
        acm.EnumFromString('InsType', 'Deposit'))

    query.AddAttrNode('Instrument.OpenEnd', 'EQUAL',
        acm.EnumFromString('OpenEndStatus', 'Open End'))

    for status in ['Void', 'Confirmed Void', 'Simulated', 'Terminated']:
        query.AddAttrNode('Status', 'NOT_EQUAL',
            acm.EnumFromString('TradeStatus', status))

    callAccounts = set(trade.Instrument() for trade in query.Select())

    return callAccounts

def get_latest_price_movement(str_ins, report_date):
    """
    This function takes a string instrument name, and date as input.
    It returns a tuple (price_T1, price_T)
    Where:
        price_T1 = The latest settle price on or before report_date, available for either SPOT market for the instrument.
        price_T = The latest settle price on or before day() of price_T1, available for either SPOT/internal market for the instrument.
    """
    
    MARKET = 'SPOT' 
    if acm.FInstallationData.Select('').At(0).Name() == 'Playground':
        MARKET = 'SPOT_MID'  # Use 'SPOT_MID' in Playground

    nst = acm.Time()
    ins = acm.FInstrument[str_ins]
    # Use latest price for point_T
    prices = [p for p in ins.Prices() if p.Market().Name() == MARKET and p.Day() <= nst.AsDate(report_date)]
    date_T, date_T1 = None, None
    market_T, market_T1 = None, None

    if len(prices) != 0:
        date_T, point_T, market_T = prices[0].Day(), prices[0].Settle(), prices[0].Market().Name()
        tempPrice = prices[0]  # Used in case historical price for prev bus day cant be found
        prices = []
        count = 0  # Counter to ensure that the script doesn't try to find prices too far back.
        date_T1 = NamespaceTimeFunctions.DateAddDeltaType(None, date_T, -1, 'd', cal='ZAR Johannesburg', bDayMethod='Preceding')
        while len(prices) == 0:
            for p in ins.HistoricalPrices():
                if p.Market().Name() in ['internal', MARKET] and p.Day() == nst.AsDate(date_T1):
                    prices.append(p)
                    break
            else:
                if count > 5:
                    prices.append(tempPrice)
                    LOGGER.info('PrevBusinessDay price not found for curve movement: {0}'.format(str_ins))
                    break
                count += 1
                date_T1 = NamespaceTimeFunctions.DateAddDeltaType(None, date_T1, -1, 'd', cal='ZAR Johannesburg', bDayMethod='Preceding')
        point_T1 = prices[0].Settle()
        market_T1 = prices[0].Market().Name()
    else:
        # find latest prices in Historical prices
        class myPrice(object):
            def __init__(self, p):
                self.price = p
            def __cmp__(self, other):
                return -cmp(self.price.Day(), other.getPrice().Day())
            def getPrice(self):
                return self.price
        
        
        q = Queue.PriorityQueue()
        for p in ins.HistoricalPrices():
            if p.Market().Name() in ['internal', MARKET] and p.Day() <= nst.AsDate(report_date):
                q.put(myPrice(p))
                
        if q.empty():
            # No historiocal price available, will return 0 for two latest prices
            LOGGER.warning('Warning: Not enough historical prices available to get price movement for %s' % str_ins)
            return 0, 0
        else:
            point_T = q.get().getPrice()
            
        if q.empty():
            LOGGER.warning('Warning: Not enough historical prices available to get T-1 price for %s' % str_ins)
            return 0, 0
        else:
            point_T1 = q.get().getPrice()
        
        try:
            while point_T1.Day() == point_T.Day():
                point_T1 = q.get(False).getPrice()
        except:
            LOGGER.warning('Warning: Not enough historical prices available to get T-1 price movement for %s' % str_ins)
            return 0, 0
            
        point_T, date_T, market_T = point_T.Settle(), point_T.Day(), point_T.Market().Name()
        point_T1, date_T1, market_T1 = point_T1.Settle(), point_T1.Day(), point_T1.Market().Name()
        
    return point_T1, point_T   

def is_child_portf(portfolio, parent_portfolio):
    """Return True if portfolio is a give of given parent."""
    parent = portfolio
    while 1:
        current_portfolio = parent
        member_links = current_portfolio.MemberLinks()
        parent_links = [link for link in member_links
                        if link.MemberPortfolio() == current_portfolio]
        if not parent_links:
            return False
        parent = parent_links[0].OwnerPortfolio()
        if not parent:
            return False
        if parent == parent_portfolio:
            return True
    return False
    
def is_client_callaccnt(instrument):
    trades = instrument.Trades()
    if trades and trades.Size() == 1:
        ctrpty = trades[0].Counterparty()
        if ctrpty:
            pb_call_account = ctrpty.AddInfoValue("PB_Call_Account")
            if pb_call_account and pb_call_account.Name() == instrument.Name():
                return True
    return False
