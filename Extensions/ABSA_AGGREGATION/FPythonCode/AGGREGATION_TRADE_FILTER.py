"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-03-22  CHG1001539200  Tibor Reiss        Update and refactor to enable PS aggregation
2019-11-19  FAPE-101       Tibor Reiss        New payment type to improve PS aggregation
-----------------------------------------------------------------------------"""
import copy

import acm
from FBDPCurrentContext import Logme
from AGGREGATION_PARAMETERS import PARAMETERS
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS


PV_TOLERANCE = 0.00005


class TRADE_FILTER():
    def __init__(self, setOfTrades):
        self.__setOfTrades = setOfTrades
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)
        self.__validPortfolios = []
        self.__getValidPortfolios()
        self.__filterInvalidPortfolios()
        self.__filterRestrictedPortfolios()
        self.__filterPresentValue()
        self.__filterYearEndCrossTrades()
        self.__filterYearEndFutureTrades()
        self.__filterHedgeRefTrades()
        self.__filterSimulatedTrades()
        self.__filterVoidedTrades()
        self.__filterSingleTradeOnCashPostingInstrument()
        self.__filterZeroTrades()

    def __getValidPortfolios(self):
        Logme()('DEBUG: Retreiving valid Portfolios', 'DEBUG')
        for key in self.__setOfTrades.keys():
            if key[1] not in self.__validPortfolios:
                self.__validPortfolios.append(key[1])

    def __filterInvalidPortfolios(self):
        Logme()('DEBUG: Filter invalid Portfolios', 'DEBUG')
        helpers = GENERIC_HELPERS()
        filterList = []
        for key in self.__tempSetOfTrades.keys():
            tempList = []
            for trade in self.__tempSetOfTrades[key]:
                if trade.TrueMirrorPortfolio():
                    if trade.TrueMirrorPortfolio() in self.__validPortfolios:
                        tempList.append(trade)
                    else:
                        filterList.append(trade)
                else:
                    tempList.append(trade)
            self.__setOfTrades[key] = tempList
            #if key[5] not in self.__validPortfolios and key[5] != 'No Trade: CounterPortfolio':
            #    del self.__setOfTrades[key]
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)
        Logme()('DEBUG: The following trades are being filtered due to be linked to invalid '
                'portfolios. %s' % helpers.acmOidToLinstInts(filterList), 'DEBUG')

    def __filterRestrictedPortfolios(self):
        Logme()('DEBUG: Filter restricted Portfolios', 'DEBUG')
        helpers = GENERIC_HELPERS()
        filterList = []
        for key in self.__tempSetOfTrades.keys():
            tempList = []
            for trade in self.__tempSetOfTrades[key]:
                if trade.Portfolio():
                    portfolio = trade.Portfolio().Name()
                else:
                    portfolio = 'No Portfolio'
                if trade.TrueMirrorPortfolio():
                    mirrorPortfolio = trade.TrueMirrorPortfolio()
                else:
                    mirrorPortfolio = 'No Mirror Portfolio'

                if (portfolio not in  PARAMETERS.restrictedPortfolios) and \
                   (mirrorPortfolio not in  PARAMETERS.restrictedPortfolios):
                    tempList.append(trade)
                else:
                    filterList.append(trade)
                self.__setOfTrades[key] = tempList
            #if key[1] in PARAMETERS.restrictedPortfolios or key[5] in PARAMETERS.restrictedPortfolios:
            #    del self.__setOfTrades[key]
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)
        Logme()('DEBUG: The following trades are being filtered due to be linked to restricted '
                'portfolios. %s' % helpers.acmOidToLinstInts(filterList), 'DEBUG')

    def __filterSingleTradeOnCashPostingInstrument(self):
        Logme()('DEBUG: Filter single trade on Cash Posting Instrument', 'DEBUG')
        helpers = GENERIC_HELPERS()
        for key in self.__tempSetOfTrades.keys():
            if len(self.__setOfTrades[key]) == 1 and \
               self.__setOfTrades[key][0].Instrument().Name() == PARAMETERS.cashPostingInstrument.Name():
                Logme()('DEBUG: The following trades are being filtered due to being a single trade '
                        'on the cash posting instrument. %s' %
                        helpers.acmOidToLinstInts(self.__setOfTrades[key]), 'DEBUG')
                del self.__setOfTrades[key]
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __getPresentValue(self, trades, key):
        if not trades:
            return 0
        presentValue = PARAMETERS.calcSpaceClass.getPresentValue(trades)
        try:
            value = abs(round(presentValue.Value().Number(), 2))
            if value >= PV_TOLERANCE:
                Logme()('WARNING: This grouper, %s, has an existing PV of %s.' % (str(key), value), 'WARNING')
                if PARAMETERS.preservePSYearlyTPL:
                    Logme()('DEBUG: Running the second grouper...', 'DEBUG')
                    self.__filterTradesWithNonZeroPV(trades, key)
                else:
                    return 1
        except Exception as e:
            Logme()('ERROR: This grouper, %s, could not get a PV from Trading Manager. '
                    '%s with error %s: ' % (str(key), str(presentValue), str(e)), 'ERROR')
            return 1
        return 0

    def __filterPresentValue(self):
        helpers = GENERIC_HELPERS()
        Logme()('DEBUG: Filter Present Value and Mirror Present Value', 'DEBUG')
        for key in self.__tempSetOfTrades.keys():
            presentValue = self.__getPresentValue(self.__tempSetOfTrades[key], key)

            if presentValue == 1:
                Logme()('DEBUG: The following trades are being filtered due to errors. %s' %
                        helpers.acmOidToLinstInts(self.__setOfTrades[key]), 'DEBUG')
                del self.__setOfTrades[key]
            else:
                mirrorTrades = helpers.getMirrorTrades(self.__tempSetOfTrades[key])
                if mirrorTrades:
                    mirrorPV = self.__getPresentValue(mirrorTrades, key)
                    if mirrorPV == 1:
                        Logme()('DEBUG: The following trades are being filtered due to their '
                                'mirror trade errors. %s' %
                                helpers.acmOidToLinstInts(self.__setOfTrades[key]), 'DEBUG')
                        del self.__setOfTrades[key]

        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterZeroTrades(self):
        Logme()('DEBUG: Filter Groupers with zero trades', 'DEBUG')
        for key in self.__tempSetOfTrades.keys():
            if len(self.__tempSetOfTrades[key]) < 1:
                Logme()('DEBUG: The following grouper have no trades. Grouper will be removed', 'DEBUG')
                del self.__setOfTrades[key]
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterYearEndCrossTrades(self):
        if PARAMETERS.filterYearEndCrossTrades == False:
            return

        Logme()('DEBUG: Filter trades that starts in the prior year and expires in the current year.', 'DEBUG')
        helpers = GENERIC_HELPERS()
        firstDateOfYear = acm.Time.FirstDayOfYear(PARAMETERS.reportDate)
        tradesToRemove = []
        for key in self.__tempSetOfTrades.keys():
            filteredTrades = []
            for trade in self.__tempSetOfTrades[key]:
                if trade.Instrument().StartDate() >= firstDateOfYear or \
                   trade.Instrument().ExpiryDate() < firstDateOfYear:
                    filteredTrades.append(trade)
                else:
                    tradesToRemove.append(trade)
            self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterYearEndFutureTrades(self):
        if PARAMETERS.filterYearEndCrossTrades == False:
            return

        Logme()('DEBUG: Filter trades that have a trade time in the prior year and '
                'where the instrument expires in the current year.', 'DEBUG')
        helpers = GENERIC_HELPERS()
        firstDateOfYear = acm.Time.FirstDayOfYear(PARAMETERS.reportDate)
        tradesToRemove = []
        for key in self.__tempSetOfTrades.keys():
            filteredTrades = []
            for trade in self.__tempSetOfTrades[key]:
                if trade.TradeTime() < firstDateOfYear and \
                   trade.Instrument().ExpiryDate() >= firstDateOfYear:
                    tradesToRemove.append(trade)
                else:
                    filteredTrades.append(trade)
            self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

        if tradesToRemove:
            Logme()('DEBUG: The following trades will be removed %s.' %
                    helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterHedgeRefTrades(self):
        Logme()('DEBUG: Filter trades that are linked to the same hedge '
                'reference where the instruments are still live.', 'DEBUG')
        helpers = GENERIC_HELPERS()
        tradesToRemove = []
        for key in self.__tempSetOfTrades.keys():
            filteredTrades = []
            for trade in self.__tempSetOfTrades[key]:
                removeTrade = False
                hedgeTrade = trade.HedgeTrade()
                if hedgeTrade:
                    hedgeRefTrades = acm.FTrade.Select('hedgeTrade = %i' %hedgeTrade.Oid())
                    for hedgeRefTrade in hedgeRefTrades:
                        if hedgeRefTrade.Instrument().ExpiryDate() > PARAMETERS.reportDate:
                            removeTrade = True
                            break

                if removeTrade == True:
                    tradesToRemove.append(trade)
                else:
                    filteredTrades.append(trade)

            self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterSimulatedTrades(self):
        Logme()('DEBUG: Filter trades that are in status Simulated.', 'DEBUG')
        helpers = GENERIC_HELPERS()
        tradesToRemove = []
        for key in self.__tempSetOfTrades.keys():
            filteredTrades = []
            for trade in self.__tempSetOfTrades[key]:
                if PARAMETERS.status != 'Simulated':
                    if trade.Status() == 'Simulated':
                        tradesToRemove.append(trade)
                    else:
                        filteredTrades.append(trade)
                else:
                    if trade.Status() == 'Simulated':
                        filteredTrades.append(trade)
                    else:
                        tradesToRemove.append(trade)
            self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterVoidedTrades(self):
        Logme()('DEBUG: Filter trades that are in status Void.', 'DEBUG')
        helpers = GENERIC_HELPERS()
        tradesToRemove = []
        for key in self.__tempSetOfTrades.keys():
            filteredTrades = []
            for trade in self.__tempSetOfTrades[key]:
                if PARAMETERS.status != 'Void':
                    if trade.Status() == 'Void':
                        tradesToRemove.append(trade)
                    else:
                        filteredTrades.append(trade)
                else:
                    if trade.Status() == 'Void':
                        filteredTrades.append(trade)
                    else:
                        tradesToRemove.append(trade)
            self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def __filterTradesWithNonZeroPV(self, trades, key):
        """
        This is specifically for Prime Services (PS). But the function will be executed if preservePSYearlyTPL == True
        is defined.
        Explanation based on an example: In PS, swaps (and FRAs) have an opening and a closing trade in case the trade
        is terminated. If a group of terminated trades has a PV, this is usually because one of the two trades is
        missing or was not terminated. Instead of not aggregating anything from this grouper, this function filters
        out all these trades so that the rest can be still aggregated.
        Implementation: the function checks the lowest level grouping - which should be instrument -  for the PV.
        """
        Logme()('DEBUG: Filter trades with non-zero PV', 'DEBUG')
        helpers = GENERIC_HELPERS()
        tradesToRemove = []
        filteredTrades = []
        grouper_name = "Agg_Instrument_PVFiltering"
        grouper = acm.FStoredPortfolioGrouper.Select01("user='AGGREGATION' and name='%s'" % grouper_name, None)
        PARAMETERS.calcSpaceClass.setupCalculationWithGrouper(trades, grouper.Grouper())
        iterator = PARAMETERS.calcSpace.RowTreeIterator()
        while iterator.NextUsingDepthFirst():
            firstChild = iterator.Clone().FirstChild()
            if firstChild and firstChild.Tree().Item().IsKindOf(acm.FTradeRow):
                presentValue = PARAMETERS.calcSpaceClass.calculateValue(iterator.Tree())
                presentValue = presentValue.Value().Number()
                presentValue = abs(round(presentValue))
                while firstChild:
                    oid = firstChild.Tree().Item().StringKey()
                    if presentValue >= PV_TOLERANCE:
                        tradesToRemove.append(acm.FTrade[oid])
                    else:
                        filteredTrades.append(acm.FTrade[oid])
                    firstChild = firstChild.NextSibling()
        self.__setOfTrades[key] = filteredTrades
        Logme()('DEBUG: The following trades will be removed %s.' %
                helpers.acmOidToLinstInts(tradesToRemove), 'DEBUG')
        self.__tempSetOfTrades = copy.copy(self.__setOfTrades)

    def getFilteredTrades(self):
        return self.__setOfTrades


class TRADE_DEPENDENCY_FILTER():
    def __init__(self, setOfTrades):
        self.__setOfTrades = setOfTrades

    def getFilteredTrades(self):
        return self.__setOfTrades
