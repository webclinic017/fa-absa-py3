"""-----------------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-06-07 677654        Paul J.-Guillarmod Added a CalculateOvernightFunding function to be called from trading manager
2011-06-17 685737        Paul J.-Guillarmod Updated the get fee function to deal with different fee types
2013-04-25 980134        Peter Fabian       Fixed TotalFunding function to look only at funding cash flows
2013-08-06 1232225       Peter Fabian       Added support for groupers for funding/warehousing
2015-01-14 2562289       Hynek Urban        Use sum_over_multiple where appropriate
2015-04-08 FAU-678       Ondrej Bahounek    Exclude voided trades from tradesInPosition
2016-03-17 3506685       Ondrej Bahounek    Accommodate PBA.
2018-12-06 CHG1001113453 Tibor Reiss        Enable fully funded CFD for MMIBETA2
2018-11-22 CHG1001204171 Tibor Reiss        Rewrite funding calculation
2019-03-27 FAPE-65       Tibor Reiss        Remove fully funded CFD for MMIBETA2(you are reading it correctly)
2019-10-22 FAPE-91       Tibor Reiss        Put funding on correct pswap even if trade is booked in wrong pf
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
2020-01-29 FAPE-120      Tibor Reiss        Remove code for old funding method
-----------------------------------------------------------------------------"""
from collections import defaultdict

import acm
import PS_FundingSweeper
import PS_Functions

import at_calculation_space
from at_decorators import sum_over_multiple
from at_logging import getLogger


LOGGER = getLogger(__name__)
ALL_TRADES_CACHE = defaultdict(lambda: defaultdict(lambda: defaultdict(acm.FIndexedCollection)))
ZAR_CALENDAR = acm.FCalendar['ZAR Johannesburg']
DAYS_PERCENT = 36500.0
FUNDING_LEGS = defaultdict(lambda: defaultdict(set))


class FundingData:
    """
    Stores all the data needed to calculate funding for a single day.
    When calculating Monthly or Yearly funding for the TPL columns, if the 1st of a month or year falls on a
    non-banking day, instead of calculating funding for all the non-banking days, only one days worth of
    funding will be calculated.
    e.g. If the 1st is on a Sunday, instead of calculating funding for three days (Sat, Sun, Mon), just
    calculate one days worth of funding.
    """
    def __init__(self, startDate, endDate, fundingType):
        numDays = acm.Time().DateDifference(endDate, startDate)
        if fundingType == 'Monthly' and numDays > 1:
            firstOfMonth = acm.Time().FirstDayOfMonth(endDate)
            if startDate <= firstOfMonth < endDate:
                self.NumDays = 1
            else:
                self.NumDays = numDays
        elif fundingType == 'Yearly' and numDays > 1:
            firstOfYear = acm.Time().FirstDayOfYear(endDate)
            if startDate <= firstOfYear < endDate:
                self.NumDays = 1
            else:
                self.NumDays = numDays
        else:
            self.NumDays = numDays
            
        self.Value = 0.0   # The fixing value from the Nominal Scaling reset
        self.Rate = 0.0    # The fixing value from the Simple Overnight reset


def GetResetValues(cashFlow, startDate, endDate, fundingType):
    """
    Generate a dictionary of FundingData objects excluding data for the startDate and including data for the endDate.
    Because the data needed to calculate daily funding is stored in two separate resets we can't calculate
    the funding in a single iteration of the resets.  Instead we store the data needed to calculate each
    days funding in a dictionary.
    """
    resetValues = {}
    for reset in cashFlow.Resets():
        resetDate = reset.Day()
        if startDate < resetDate <= endDate:
            if resetDate in resetValues:
                resetData = resetValues[resetDate]
            else:
                resetData = FundingData(reset.StartDate(), reset.EndDate(), fundingType)
                resetValues[resetDate] = resetData
                
            resetType = reset.ResetType()
            if resetType == 'Nominal Scaling':
                resetData.Value = reset.FixingValue()
            elif resetType == 'Simple Overnight':
                resetData.Rate = reset.FixingValue()
                
    return resetValues


def GetAllFundingLegs(portfolio_swap, instrument):
    ''' In the case of CFD portfolio swaps there will be two funding legs, one for overnight funding (receive leg)
        and one for short funding (pay leg).  The daily funding will need to be calculated from both of these legs.

        In the case of multi-instrument portfolio swaps both short and overnight funding is calculated using a
        single leg.
    '''
    pswap_name = portfolio_swap.Name()
    ins_name = instrument.Name()
    if not (pswap_name in FUNDING_LEGS and ins_name in FUNDING_LEGS[pswap_name]):
        for leg in portfolio_swap.Legs():
            if leg.LegType() == 'Float':
                FUNDING_LEGS[pswap_name][leg.IndexRef().Name()].add(leg.Oid())
    leg_oids = FUNDING_LEGS[pswap_name][ins_name]
    return [acm.FLeg[oid] for oid in leg_oids]


def PortfolioSwapType(portfolio_swap):
    ''' Return the type of portfolio swap, either CFD or General.
    '''
    fund_portfolio = portfolio_swap.FundPortfolio()
    return fund_portfolio.add_info('PS_PortfolioType')


def GetOvernightFundingLeg(portfolioSwap, instrument):
    """
    In the case of CFD portfolio swaps the receive Float leg is the overnight funding leg.
    In the case of General portfolio swaps just return the Float leg.
    """
    portfolioSwapType = PortfolioSwapType(portfolioSwap)
    instrumentName = instrument.Name()

    for leg in portfolioSwap.Legs():
        if portfolioSwapType == 'CFD' and not leg.PayLeg() and leg.IndexRef().Name() == instrumentName and leg.LegType() == 'Float':
            return leg
        elif portfolioSwapType == 'General' and leg.IndexRef().Name() == instrument.Name() and leg.LegType() == 'Float':
            return leg
    return None


@sum_over_multiple('portfolioSwap')
def TotalFunding(instrument, portfolioSwap):
    """
    Calculate the total funding for an instrument by retrieving the projected value from the cashflow.
    This should be faster than looping through the resets when the calculations are over a longer time period.
    """
    totalFunding = 0.0
    legs = GetAllFundingLegs(portfolioSwap, instrument)
    for leg in legs:
        cashFlow = PS_FundingSweeper.GetFloatCashFlow(leg, 'Funding')
        if cashFlow:
            totalFunding += acm.GetCalculatedValueFromString(cashFlow, acm.GetDefaultContext(), "projectedCashFlow", None).Value().Number()
    return totalFunding


def _getCalcValue(query, columnName, date, simulatedValues):
    value = at_calculation_space.calculate_value('FPortfolioSheet', query, 
                                                 columnName, False, simulatedValues)
    
    try:
        value = value.Number()
    except:
        pass
    
    # If a value is a NaN, # or #QNaN return 0.  This is to make sure 
    # the call account sweeping continues the issue will get picked up
    # in the scheduled report PS_Sweeping_Recon and get manually resolved.
    if PS_FundingSweeper._isNumber(value):
        return value
    else:
        return 0


def valEndForTrades(trades, query, date):
    """Return the first Portfolio Value End for first instrument specified either by query or by trades iterable"""
    if not query:
        if not trades:
            raise ValueError("ValEndForTrades error -- no trades or query supported")
        else:
            query = acm.FAdhocPortfolio()
            for trd in trades:
                query.Add(trd)
    
    simulatedValues = {
        'Portfolio Profit Loss End Date': 'Custom Date', 
        'Portfolio Profit Loss End Date Custom': date,
    }
    
    valEnd = _getCalcValue(query, 'Portfolio Value End', date, simulatedValues)
    return valEnd


def GroupingFactor(tradesInPosition, portfolioSwap, instrument, date, queryType):
    """
    Return the grouping factor for group of trades vs all trades in position
    on a specific date based on Portfolio Value End column
    """

    # upgrade 2014.4 fix: exclude voided trades from tradesInPosition
    tradesInPosition = tradesInPosition.Filter(lambda t:
        t.Status() not in ['Void', 'Simulated', 'Terminated'])
    
    insName = instrument.Name()
    prf = portfolioSwap.FundPortfolio()
    prfName = prf.Name()
    
    # all trades in position cache
    if (prfName in ALL_TRADES_CACHE
        and insName in ALL_TRADES_CACHE[prfName]
        and queryType in ALL_TRADES_CACHE[prfName][insName]):
        allTrds = ALL_TRADES_CACHE[prfName][insName][queryType]
    else:
        if queryType == 'funding':
            allTradesQuery = PS_FundingSweeper.FundingQuery(prf)
        elif queryType == 'warehousing':
            allTradesQuery = PS_FundingSweeper.WarehousingQuery(prf)
        else:
            raise RuntimeError("Unknown query type")
        allTradesQuery.AddAttrNode('Instrument.Name', 'EQUAL', insName)
        allTradesQuery.AddAttrNode('Status', 'NOT_EQUAL', 
                                   acm.EnumFromString('TradeStatus', 'Void'))
        allTrds = allTradesQuery.Select()
        ALL_TRADES_CACHE[prfName][insName][queryType] = allTrds
    
    # early exit in simple case of all trades being included in group  
    if tradesInPosition.Size() == len(allTrds):
        return 1
    
    # funding on resets is based on d-1 value end, 
    # so if we want to use correct split we need to go back 1 day as well
    prevBusinessDay = ZAR_CALENDAR.AdjustBankingDays(date, -1)
    
    epsilon = 0.00001
    valEndTradesInPos = valEndForTrades(tradesInPosition.AsArray(), None, prevBusinessDay)
    if abs(valEndTradesInPos) <= epsilon:
        return 0
    
    valEndAllTrades = valEndForTrades(allTrds, None, prevBusinessDay)
    # The mtm value for the whole position should never be 0 (we create 
    # the funding resets only if val end is not zero). If the funding for 
    # the whole position is almost zero, then we shouldn't have any record 
    # about it in the portfolio swap in the first place. But sometimes that 
    # happens and the position is almost zero. In these cases the total funding 
    # is almost zero, but the funding for each group would be huge (as it would be 
    # divided by almost zero). That's why I decided to default to zero in this case 
    # for the grouping. Anyway, what the PCG is concerned about is the overall 
    # position/funding and that is why I decided to implement it like this.
    if abs(valEndAllTrades) <= epsilon:
        return 0
    
    groupingFactor = valEndTradesInPos/valEndAllTrades
    return groupingFactor


def CalculateWarehousingGroupingSupported(instrument, portfolioSwap,
                                          startDate, endDate,
                                          tradesInPosition, warehousingType = 'Daily'):
    """Calculate the warehousing for an instrument excluding the startDate and including the endDate."""
    warehousing = 0.0

    leg = PS_FundingSweeper.GetLeg(portfolioSwap, 'Float', instrument)
    if leg:
        cashFlow = PS_FundingSweeper.GetFloatCashFlow(leg, 'Warehousing')
        if cashFlow:
            resetValues = GetResetValues(cashFlow, startDate, endDate, warehousingType)
            for date, resetData in resetValues.items():
                if resetData.Rate != 0:
                    groupingFactor = GroupingFactor(tradesInPosition, portfolioSwap, 
                                                    instrument, date, 'warehousing')
                else:
                    groupingFactor = 1
                
                warehousing += (resetData.NumDays * resetData.Value 
                                * resetData.Rate * groupingFactor) / DAYS_PERCENT
    return warehousing
    

def GetPswapForCurr(pswap, currency):
    """
    Get pswap with given currency.
    Arguments:
        -- pswap: any fund's pswap
        -- currency: currency of a pswap that this function should find
    All fund's PBA pswaps differ in currency. These pswaps are in the same portfolio.
    Return pswap with given currency by searching for all pswaps in pswap portfolio.
    """
    pswap_portf = pswap.Trades()[0].Portfolio()
    pswaps = [ins for ins in pswap_portf.Instruments() if ins.Currency().Name() == currency]
    if len(pswaps) == 0:
        LOGGER.error("ERROR: no pswap found for currency '{0}'".format(currency))
        return None
    if len(pswaps) > 1:
        LOGGER.warning("WARNING: more than 1 pswap found for currency '{0}'".format(currency))
    return pswaps[0]        


def GetReset(cashFlow, resetType, day, matchExact = False, checkPrevBusDay = False, checkUntilDay = None):
    for reset in cashFlow.Resets():
        if reset.ResetType() == resetType and reset.Day() == day:
            return reset
    if matchExact:
        return None
    # Get previous reset only if requested otherwise return None
    if not checkPrevBusDay:
        return None
    else:
        prevDay = checkUntilDay
        prevReset = None
        for reset in cashFlow.Resets():
            if reset.ResetType() == resetType and reset.Day() < day and (prevDay is None or reset.Day() > prevDay):
                prevDay = reset.Day()
                prevReset = reset
        return prevReset


def CalculateFunding(instrument, pswap_candidates, start_date,
                     end_date, valid_trades_in_position,
                     check_prev_bus_day_for_end = False):
    ''' Calculate the funding for instrument excluding funding for the start_date
        and including funding for the end_date. If the portfolio swap is a CFD
        portfolio swap funding is calculated off two legs, the short funding leg
        and the overnight leg. Otherwise funding is calculated off a single leg
        which combines both overnight and short funding.
    '''
    funding = 0.0

    if not valid_trades_in_position:
        return funding

    funding_legs = []
    pswaps_with_funding_leg = []
    if pswap_candidates:
        for pswap in pswap_candidates:
            is_fully_funded = PS_Functions.get_pb_pswap_ff_flag(pswap)
            if is_fully_funded:
                continue
            legs = GetAllFundingLegs(pswap, instrument)
            if legs:
                pswaps_with_funding_leg.append(pswap.Name())
                funding_legs.append(legs)
    if not funding_legs:
        return funding
    if len(funding_legs) > 1:
        LOGGER.error("More than 1 pswap with funding leg: {}"
                     .format(','.join(pswaps_with_funding_leg)))
        return funding

    for leg in legs:
        cash_flow = PS_FundingSweeper.GetFloatCashFlow(leg, 'Funding')
        if cash_flow:
            if not cash_flow.Resets():
                continue
            # In the case of CFD pswaps the payleg is the short funding
            # leg, we want to subtract this from the overnight funding
            # so need to reverse the signs.
            if leg.PayLeg():
                funding_factor = 1
            else:
                funding_factor = -1
            # Values will be incorrect if going back more than 2 months
            # due to aggregation
            end_funding = GetReset(cash_flow, 'Return', end_date, True)
            if not end_funding and check_prev_bus_day_for_end:
                end_funding = GetReset(cash_flow, 'Return', end_date, False, True, start_date)
            if end_funding:
                funding += funding_factor * end_funding.FixingValue()
                start_funding = GetReset(cash_flow, 'Return', start_date, False, True)
                if start_funding:
                    funding -= funding_factor * start_funding.FixingValue()
    return funding


@sum_over_multiple('portfolioSwap')
def CalculateWarehousing(instrument, portfolioSwap, startDate, endDate, warehousingType = 'Daily'):
    """Calculate the warehousing for an instrument excluding the startDate and including the endDate."""
    warehousing = 0.0
    leg = PS_FundingSweeper.GetLeg(portfolioSwap, 'Float', instrument)
    if leg:
        cashFlow = PS_FundingSweeper.GetFloatCashFlow(leg, 'Warehousing')
        if cashFlow:
            resetValues = GetResetValues(cashFlow, startDate, endDate, warehousingType)
            for date, resetData in resetValues.items():
                warehousing += (resetData.NumDays * resetData.Value * resetData.Rate) / DAYS_PERCENT
    return warehousing
    
    
@sum_over_multiple('portfolioSwap')
def CalculateFee(instrument, portfolioSwap, feeType, isGeneralPSwap, startDate, endDate):
    """
    Calculate the fee of feeType (execution fee or STT) for an instrument excluding fees for the startDate and
    including fees for the endDate.
    If the portfolioswap is a CFD portfolio swap then the execution fee legs wont have the addinfo PS_FeeType set
    and all the cashflows on a fixed leg will be execution premiums.
    """
    totalFee = 0.0
    if not isGeneralPSwap and feeType == 'STT':
        return totalFee
    else:
        for leg in portfolioSwap.Legs():
            if (leg.IndexRef().Name() == instrument.Name() and leg.LegType() == 'Fixed' 
                and not leg.PayLeg() and leg.NominalScaling() == 'None'):
                for cashFlow in leg.CashFlows():
                    if isGeneralPSwap and cashFlow.add_info('PS_FeeType') == feeType and (startDate < cashFlow.PayDate() <= endDate):
                        totalFee += cashFlow.FixedAmount()
                    elif not isGeneralPSwap and (startDate < cashFlow.PayDate() <= endDate):
                        totalFee += cashFlow.FixedAmount()
        return totalFee
