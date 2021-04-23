""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPCalculatePosition.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FBDPCalculatePosition - Calculate positions using aggregation code.

DESCRIPTION
    This module contains functionality to use the acm function
    CalculatePosition, which returns trades calculated with the
    aggregation c-code.

EXTERNAL DEPENDENCIES
    PRIME client 2.8 or later (excluding PRIME 3.0).
----------------------------------------------------------------------------"""


import ael
import acm


from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import FBDPCommon


class CalcTrades(list):
    dirty = False
    errMsg = ''


# Function unittested by test_FBDPCalculatePosition
def checkForDirtyPositions(cp, showSummary):
    tradePositions = CalcTrades([])
    for pos in cp:
        if pos:
            posName = pos['name']
            posError = pos['error']
            posWarning = pos['warning']
            posMessage = pos['message']
            if posError:
                tradePositions.dirty = True
                tradePositions.errMsg = posError
                if posMessage:
                    Logme()(posMessage, 'WARNING')
                if showSummary:
                    Summary().ignore(Summary().POSITION, Summary().action,
                            posError, posName)
            elif posWarning:
                if posMessage:
                    Logme()(posMessage, 'WARNING')
                if showSummary:
                    Summary().warning(Summary().POSITION, Summary().action,
                            posWarning, posName)
            if not posError:
                tradePositions.append([pos['calculated_trades'],
                        pos['original_trades']])
    return tradePositions


def _calculate(i, start_date=None, end_date=acm.Time.DateToday(), portfolio=[],
        showSummary=True, hookArguments={}, usePlClearDate=1):

    if Logme().ScriptName == 'Clear Profit and Loss':
        Summary().action = Summary().CLEAR

    if not start_date:
        start_date = "1970-01-01"

    for n in range(len(portfolio)):
        if isinstance(portfolio[n], type("")):
            portfolio[n] = acm.FPhysicalPortfolio[portfolio[n]]

    cp = CalcTrades([])
    if i.Trades():
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        dic = i.CalculatePosition(start_date, end_date, portfolio,
                useSelectedFundingDay, 1, usePlClearDate)
        cp = CalcTrades(dic["calculatedPositions"])
        cp = checkForDirtyPositions(cp, showSummary)

    return cp


def convertPositions(calculatedPositions, toAel=True):
    """
    Converts trades from ACM to AEL if toAel is True, else toAel is False.
    """
    convertedPositions = CalcTrades([])
    convertedPositions.dirty = calculatedPositions.dirty
    for calcPos in calculatedPositions:
        calcTrades = calcPos[0]
        origTrades = calcPos[1]
        if toAel:
            convCalcTrades = [ael.Trade[t.Oid()] for t in calcTrades]
            convOrigTrades = [ael.Trade[t.Oid()] for t in origTrades]
        else:
            convCalcTrades = [acm.FTrade[t.trdnbr] for t in calcTrades]
            convOrigTrades = [acm.FTrade[t.trdnbr] for t in origTrades]
        convertedPositions.append([convCalcTrades, convOrigTrades])
    return convertedPositions

def CalculatePositionUsingGrouper(i, port, grouper=None, start_date=None,
    end_date=acm.Time.DateToday(), hookArguments={}, usePlClearDate=1):
    if not start_date:
        start_date = "1970-01-01"

    cp = CalcTrades([])
    if port:
        trades = acm.FTrade.Select('portfolio="' + port.Name() + \
        '" and instrument="' + i.Name() + '"')
    else:
        trades = acm.FTrade.Select("instrument=" + i.Name() + '"')

    if trades:
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        dic = i.CalculatePositionUsingGrouper(
        start_date, end_date, port,
        [trades], grouper, useSelectedFundingDay, usePlClearDate)

        cp = CalcTrades(dic["calculatedPositions"])
        cp = checkForDirtyPositions(cp, 1)

    cp = convertPositions(cp, True)
    try:
        from FBDPHook import recalculate_position
    except Exception:
        pass
    else:
        cp = recalculate_position(i, cp, hookArguments)

    return cp


def CalculatePosition(i, start_date=None, end_date=acm.Time.DateToday(),
        portfolio=[], showSummary=True, hookArguments={}, usePlClearDate=1):
    """
    --------------------------------------------------------------------------
    FUNCTION
        calculatePosition(instrument, start_date = "1970-01-01",
        end_date = acm.Time.DateToday(), portfolio = [])

    DESCRIPTION
        calculatePosition() uses the ACM function
        FInstrument.CalculatePosition(), which calculates the aggregated values
        for the positions in the given instrument [and portfolio] between
        start_date and end_date in the same way as the ACM function
        AggregateTrades(). All trades in the instrument (and portfolio) are
        included.
        The Grouping Criteria defined in the Position Rules are used for
        grouping the trades.

        Usage:
          instrument.CalculatePosition(start_date, end_date, portfolio,
          useSelectedFundingDay, useAggregationRules, useClearPLDate)

    ARGUMENTS
        Default values:
        start_date =    1970-01-01
        end_date =      today
        port folio =     None (i.e. all portfolios)
        use_agg_rules = 1

    RETURNS
        Returns a list of positions, each positions contains a list of trades
        (with aggregated values) and a list of all trades that belongs to the
        position.
    ------------------------------------------------------------------------"""

    cp = _calculate(i, start_date, end_date, portfolio, showSummary,
            hookArguments, usePlClearDate)

    try:
        from FBDPHook import recalculate_position
    except Exception:
        pass
    else:
        aelPositions = convertPositions(cp, True)
        aelPositions = recalculate_position(i, aelPositions, hookArguments)
        cp = convertPositions(aelPositions, False)
    return cp


def calculatePosition(i, start_date=None, end_date=ael.date_today(),
        portfolio=[], showSummary=True, hookArguments={}):
    if Logme().ScriptName == 'Clear Profit and Loss':
        Summary().action = Summary().CLEAR

    if not start_date:
        start_date = ael.date_from_time(0)

    ins = acm.FInstrument[i.insaddr]
    portList = []
    for port in portfolio:
        if port != None and port != 'None':
            portList.append(acm.FPhysicalPortfolio[port.prfnbr])
        else:
            portList.append(None)

    cp = _calculate(ins, str(start_date), str(end_date), portList, showSummary,
            hookArguments)
    cp = convertPositions(cp, True)
    try:
        from FBDPHook import recalculate_position
    except Exception:
        pass
    else:
        cp = recalculate_position(i, cp, hookArguments)
    return cp


"""-----------------------------------------------------------------------
#How to use the code:
#SPECIFY THE INSTRUMENT TO BE TESTED:
#i = acm.FInstrument['BMW']
#i = acm.FInstrument['BMW03D30']
i = acm.Instrument['TEST']
#i = acm.Instrument['BMW02I36']
#i = acm.Instrument['ALIV3P']
cp = calculatePosition(i,portfolio=[acm.FPhysicalPortfolio['EQ500']])
#If run from another module, this is an example of how the function can be
#used:
#import acm, FBDPCalculatePosition
#ins = [acm.FInstrument['BMW'], acm.FInstrument['BMW03C32'],
#    acm.FInstrument['BMW03C30'], acm.FInstrument['BMW02I36']]
#port = [acm.FPhysicalPortfolio['EQ500'], acm.FPhysicalPortfolio['EQ300']]
#for i in ins:
#    cp = FBDPCalculatePosition.calculatePosition(i,
#        start_date="2003-01-01",
#        end_date=acm.Time.DateToday(),
#        portfolio=port)
-----------------------------------------------------------------------"""
