"""----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 699989 (Initial Deployment)

****History****

Paul Jacot-Guillarmod   CR850964 added logic to suppress trade fee calculation.
Peter Fabian            CR264971 2012-06-18 SET needs to be added in the overnight batch as well, calculation of order value accross allocation portfolios added
Peter Fabian            CR278377 2012-06-22 Fix for a bug introduced in the previous change (incorrect test for trade with allocation process)
Peter Kutnik            CHNG809119 (2013-02-18) Updates for Voice fees on Equities
Peter Basista           CHNG2018619 (2014-06-05) Handling errors in PB overnight batch correctly
Frantisek Jahoda        CHNG2092785 (2014-06-30) QF has to contain at least one portfolio
----------------------------------------------------------------------"""
import acm

from PS_Functions import get_pb_fund_shortname
import PS_TradeFees
from at_logging import getLogger, bp_start


LOGGER = getLogger(__name__)


class AddTradeFeesError(RuntimeError):
    """
    Custom exception class which can be used for exceptions
    raised in this module in order to distinguish them
    from other exceptions.
    """
    pass

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

# Generate date lists to be used as drop downs in the GUI.
dateList = {'Custom Date':TODAY,
              'Now':TODAY}
dateKeys = list(dateList.keys())
dateKeys.sort()

def enableCustomDate(_index, fieldValues):
    """
    An input hook compatible with ael_variables.
    """
    ael_variables[4][9] = (fieldValues[3] == 'Custom Date')
    return fieldValues

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['compoundPropPortfolio', 'Compound Prop-Portfolio', 'FCompoundPortfolio', None, None, 0, 0, 'Fees will be added to prop trades filtered from this portfolio.', None, 1],
                 ['compoundAgencyPortfolio', 'Compound Agency-Portfolio', 'FCompoundPortfolio', None, None, 0, 0, 'Fees will be added to agency trades filtered from this portfolio.', None, 1],
                 ['clientName', 'Client Name', 'FParty', None, None, 1, 0, 'Only trades with counterparty equal to client will have fees added to them.', None, 1],
                 ['executionDate', 'Execution Date', 'string', dateKeys, 'Now', 1, 0, 'All trades executed on this date will have fees added to them.', enableCustomDate, 1],
                 ['executionDateCustom', 'Execution Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0]]

def ael_main(ael_dict):
    process_name = "ps.add_trade_fees.{0}".format(get_pb_fund_shortname(ael_dict['clientName']))
    with bp_start(process_name, ael_main_args=ael_dict):
        
        if ael_dict['executionDate'] == 'Custom Date':
            executionDate = ael_dict['executionDateCustom']
        else:
            executionDate = dateList[ael_dict['executionDate']]
    
        compoundPropPortfolio = ael_dict['compoundPropPortfolio']
        compoundAgencyPortfolio = ael_dict['compoundAgencyPortfolio']
        counterParty = ael_dict['clientName']
    
        if compoundPropPortfolio:
            prop_trades = _select_trades(compoundPropPortfolio, executionDate, counterParty)
            _add_payments(prop_trades, executionDate, -1)
    
        if compoundAgencyPortfolio:
            agency_trades = _select_trades(compoundAgencyPortfolio, executionDate)
            _add_payments(agency_trades, executionDate, 1)
    
        LOGGER.info("Completed Successfully")

def _select_trades(compoundPortfolio, date, counterParty=None):
    """ Generate a query that selects all trades that need to
        have fee payments added to them.
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    if counterParty:
        query.AddAttrNode('Counterparty.Name', 'EQUAL', counterParty.Name())

    # If create_time or trade_time is equal to date, include it in the query
    orNode1 = query.AddOpNode('OR')
    andNode1 = orNode1.AddOpNode('AND')
    andNode1.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    andNode1.AddAttrNode('CreateTime', 'LESS_EQUAL', date)

    andNode2 = orNode1.AddOpNode('AND')
    andNode2.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    andNode2.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    # Add the sub portfolios to the query
    orNode2 = query.AddOpNode('OR')
    portfolios = [
        portfolio
        for portfolio in compoundPortfolio.AllPhysicalPortfolios()
        if portfolio.AdditionalInfo().PS_PortfolioType() == 'General'
    ]

    if not portfolios:
        # The provided portfolio has no general physical portfolios
        return []

    for portfolio in portfolios:
        orNode2.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    return query.Select()

def _get_owner_portfolio(portfolio):
    """
    Get the owner portfolio of the provided portfolio.
    """
    links = acm.FPortfolioLink.Select("memberPortfolio='{0}'".format(
        portfolio.Name()))
    if len(links) == 1:
        return links[0].OwnerPortfolio()
    elif len(links) == 0:
        return None
    else:  # len(links) > 1
        portfolio_owners = ""
        for link in links:
            portfolio_owners += "{0}\n".format(link.OwnerPortfolio())
        raise AddTradeFeesError("The provided portfolio '{0}' "
            "has more than one owner, namely:\n{1}".format(
            portfolio.Name(), portfolio_owners))

def _ParentCompoundPrf(trade):
    """
    Return a portfolio which is the closest ancestor
    of the provided trade's portfolio
    and which has the additional info
    PSClientCallAcc set to True.
    """
    prf = trade.Portfolio()
    while True:
        owner_prf = _get_owner_portfolio(prf)
        if not owner_prf:
            LOGGER.warning("owner prf for %s not found", prf.Name())
            prf = None
            break
        # this is nasty heuristics #1
        if owner_prf.AdditionalInfo().PSClientCallAcc():
            break
        prf = owner_prf
    return prf

def _AllocationPortfolios(trade):
    """
    Return a list of names of portfolios
    which are under the provided trade's portfolio's
    compound parent portfolio tree
    and which meet certain other (allocation) criteria.
    """
    portfolios = []

    compoundPortfolio = _ParentCompoundPrf(trade)
    if compoundPortfolio:
        for portfolio in compoundPortfolio.AllPhysicalPortfolios():
            # this is nasty heuristics #2
            if (portfolio.AdditionalInfo().PS_PortfolioType() == 'General' and
                    ("_CE_" in portfolio.Name() or
                    "_CASH_EQ" in portfolio.Name())):
                portfolios.append(portfolio.Name())
    return portfolios

def _CalculateBuySellValue(trade, date, buyOrSell):
    """
    Calculate the 'buy' or 'sell' value of all the trades
    on the provided trade's instrument which meet certain other criteria.
    """
    portfolioName = trade.Portfolio().Name()
    instrumentName = trade.Instrument().Name()

    query = acm.CreateFASQLQuery('FTrade', 'AND')
    # if portfolio.add_info('PS_PortfolioType') == 'General':
    # compoundPortfolio.AllPhysicalPortfolios()
    if trade.Text1() == 'Allocation Process':
        orNodePrf = query.AddOpNode('OR')
        for portfolioName in _AllocationPortfolios(trade):
            orNodePrf.AddAttrNode('Portfolio.Name', 'EQUAL', portfolioName)
    else:
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolioName)

    query.AddAttrNode('Instrument.Name', 'EQUAL', instrumentName)
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))

    # If create_time or trade_time is equal to date, include it in the query
    orNode1 = query.AddOpNode('OR')
    andNode1 = orNode1.AddOpNode('AND')
    andNode1.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    andNode1.AddAttrNode('CreateTime', 'LESS_EQUAL', date)

    andNode2 = orNode1.AddOpNode('AND')
    andNode2.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    andNode2.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    value = 0.0
    for trade in query.Select():
        tradeType = trade.EquityTradeType()

        # if trade.Text1() not in ['Allocation Process'] and
        if tradeType == 'DMA' and not(PS_TradeFees.isTakeonTrade(trade)):
            tradeQuantity = trade.Quantity()
            if buyOrSell == 'Sell' and tradeQuantity < 0:
                value += abs(trade.Premium())
            elif buyOrSell == 'Buy' and tradeQuantity > 0:
                value += abs(trade.Premium())

    return value

def _CalculateOrderValue(trade, date, orderNumber):
    """
    Given a trade and an order number calculate the value of the entire order.
    """
    portfolioName = trade.Portfolio().Name()
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolioName)
    query.AddAttrNode('AdditionalInfo.XtpOrderRef', 'EQUAL', orderNumber)
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))

    # If create_time or trade_time is equal to date, include it in the query
    orNode1 = query.AddOpNode('OR')
    andNode1 = orNode1.AddOpNode('AND')
    andNode1.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    andNode1.AddAttrNode('CreateTime', 'LESS_EQUAL', date)

    andNode2 = orNode1.AddOpNode('AND')
    andNode2.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    andNode2.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    orderValue = 0.0
    for trade in query.Select():
        if trade.Text1() not in ['Allocation Process'] and not(PS_TradeFees.isTakeonTrade(trade)):
            orderValue += abs(trade.Premium())

    return orderValue

def _add_payments(trades, date, propFactor=1):
    """
    Add fee payments to all trades.
    In the case of stock trades, the fee calculation will depend
    on the value of the total order that the trade belongs to.
    """

    # Dictionaries to cache the order value per order number in the case of done away trades
    # and per buy and sell in the case of done with trades.
    orderValueDict = {}
    buyValueDict = {}
    sellValueDict = {}

    for trade in trades:
        if not(PS_TradeFees.isTakeonTrade(trade)):
            # If stock trade is not part of the allocation process then it needs to have strate fees added to it.
            if trade.Instrument().InsType() in ['Stock', 'ETF']:  # and trade.Text1() not in ['Allocation Process']:
                # Calculate strate fees based on the value of the order for Trade Report (done away) trades
                tradeType = trade.EquityTradeType()
                if tradeType == 'Trade Report':
                    orderNumber = trade.AdditionalInfo().XtpOrderRef()
                    if orderNumber:
                        if orderNumber in orderValueDict:
                            orderValue = orderValueDict[orderNumber]
                        else:
                            orderValue = _CalculateOrderValue(trade, date, orderNumber)
                            orderValueDict[orderNumber] = orderValue
                    else:
                        orderValue = abs(trade.Premium())
                # Calculate strate fees based on the value of all buys/sells per instrument
                elif tradeType == 'DMA':
                    instrumentName = trade.Instrument().Name()
                    if trade.Quantity() < 0:
                        if instrumentName in sellValueDict:
                            orderValue = sellValueDict[instrumentName]
                        else:
                            orderValue = _CalculateBuySellValue(trade, date, 'Sell')
                            sellValueDict[instrumentName] = orderValue
                    else:
                        if instrumentName in buyValueDict:
                            orderValue = buyValueDict[instrumentName]
                        else:
                            orderValue = _CalculateBuySellValue(trade, date, 'Buy')
                            buyValueDict[instrumentName] = orderValue
                else:
                    orderValue = abs(trade.Premium())

                PS_TradeFees.add_trade_fees(trade, propFactor, orderValue)
            else:
                PS_TradeFees.add_trade_fees(trade, propFactor)
