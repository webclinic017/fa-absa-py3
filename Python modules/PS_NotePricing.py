"""
------------------------------------------------------------------------------------------------------------------------
Project:    Prime Brokerage Project
Department: Prime Services
Requester:  Eveshnee Naidoo
Developer:  Marian Zdrazil
CR Number:  FAPE-288 (Initial Deployment)
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Developer               Change no     Date            Description
-----------------------------------------------------------------------------------------------------------------------
Marian Zdrazil          FAPE-288      2020-05-04      Initial implementation
Marian Zdrazil          FAPE-288      2020-10-20      Hotfix: skip adding note fees on aggregate trades
-----------------------------------------------------------------------------------------------------------------------
"""
import acm

from PS_UploadPrices import _setInstrumentPrice
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

import PS_TradeFees

LOGGER = getLogger(__name__)

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), "FPortfolioSheet")
PORTFOLIO_VALUE_COLUMN = "PS Fair Value NAV"


def getPortfolioValue(calcSpace, portfolio, date):
    calcSpace.SimulateGlobalValue("Valuation Date", date)
    return calcSpace.CalculateValue(portfolio, PORTFOLIO_VALUE_COLUMN)


def selectTrades(physicalPortfolio, counterParty=None):
    """
        Generate a query that selects all trades that need to
        have prices added to them.
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    if counterParty:
        query.AddAttrNode('Counterparty.Name', 'EQUAL', counterParty.Name())

    # If create_time or trade_time is equal to date, include it in the query
    andNode = query.AddOpNode('AND')
    andNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Stock')
    andNode.AddAttrNode('Portfolio.Name', 'EQUAL', physicalPortfolio.Name())
    return query.Select()


def customDateHook(selected_variable):
    """
        Enable/Disable Custom Date based on Date value.
    """
    varName = selected_variable.name

    dateValue = selected_variable.handler.get(varName)
    dateCustom = selected_variable.handler.get("valDateCustom")

    if dateValue.value == 'Custom Date':
        dateCustom.enabled = True
    else:
        dateCustom.enabled = False


calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

# Generate date lists to be used as drop downs in the GUI.
dateList = {'Custom Date': TODAY,
            'Now': TODAY}
dateKeys = list(dateList.keys())
dateKeys.sort()

ael_variables = AelVariableHandler()
ael_variables.add('physicalPortfolio',
                  label='Physical Portfolio',
                  cls='FPhysicalPortfolio',
                  collection=None,
                  default=acm.FPhysicalPortfolio["PB_CE_FF_BIDGLOBLB_CR"],
                  mandatory=True,
                  multiple=False,
                  alt=('Prices will be added to BIDVEST note trades from this portfolio.'),
                  hook=None,
                  enabled=True)
ael_variables.add('dependencyQF',
                  label='Dependency Query Folder',
                  cls=acm.FStoredASQLQuery,
                  collection=None,
                  default=acm.FStoredASQLQuery["PS_Valuations_BIDGLOBL"],
                  mandatory=True,
                  multiple=False,
                  alt=('Dependency Query folder to extract PS Fair Value NAV from.'),
                  hook=None,
                  enabled=True)
ael_variables.add('clientName',
                  label='Counterparty',
                  cls='string',
                  collection=None,
                  default="ABSA BANK LTD",
                  mandatory=True,
                  multiple=False,
                  alt=("Counterparty name."),
                  hook=None,
                  enabled=True)
ael_variables.add('valDate',
                  label='Valuation Date',
                  cls='string',
                  collection=dateKeys,
                  default='Now',
                  mandatory=True,
                  multiple=False,
                  alt=('All notes in the portfolio on this date will have prices entries created for them.'),
                  hook=customDateHook,
                  enabled=True)
ael_variables.add('valDateCustom',
                  label='Valuation Date Custom',
                  cls='string',
                  collection=None,
                  default=TODAY,
                  mandatory=False,
                  multiple=False,
                  alt='Custom valuation date',
                  hook=None,
                  enabled=True)


def ael_main(ael_dict):
    notePortfolio = ael_dict['physicalPortfolio']
    dependencyQF = ael_dict['dependencyQF']
    cptyName = ael_dict['clientName']
    counterParty = acm.FParty[cptyName]

    if ael_dict['valDate'] == 'Custom Date':
        valDate = ael_dict['valDateCustom']
    else:
        valDate = dateList[ael_dict['valDate']]

    if notePortfolio:
        noteTrades = selectTrades(notePortfolio, counterParty)

    try:
        numTrades = len(noteTrades)
        LOGGER.info("Going through trades with BIDVEST notes: %s trade(s)" % numTrades)
        for trade in noteTrades:
            instrument = trade.Instrument()
            price = getPortfolioValue(CALC_SPACE, dependencyQF, valDate).Number()
            _setInstrumentPrice(instrument, price, valDate, 'SPOT')
            _setInstrumentPrice(instrument, price, valDate, 'internal')
            LOGGER.info("Created price for %s with value %s, trade id %s" % (instrument.Name(),
                                                                             price, trade.Oid()))
            if not(PS_TradeFees.isTakeonTrade(trade)):
                if trade.Aggregate() == 0:
                    PS_TradeFees.add_note_fee(trade)
                    LOGGER.info("Added execution fee for trade id %s on %s instrument" %
                                (trade.Oid(), instrument.Name()))
                else:
                    LOGGER.warning("Trade %s on %s instrument is an aggregate trade, cannot add note fee." %
                                   (trade.Oid(), instrument.Name()))
    except Exception as exc:
        LOGGER.error("Cannot create price and/or add execution fee: %s" % exc)
    else:
        LOGGER.info("Completed Successfully.")
