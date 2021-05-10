'''----------------------------------------------------------------------
History:
Date       CR Number     Who                    What
2019-03-22 CHG1001539200 Tibor Reiss            Update and refactor to enable PS aggregation
2019-04-12 CHG1001622197 Tibor Reiss            Fix bonds which have aggregated payment types
                                                (e.g. Aggregated Accrued): retain every payment
                                                type by using generalised function for determining
                                                if it is part of cash or not
----------------------------------------------------------------------'''
from collections import defaultdict

import acm
from AGGREGATION_PARAMETERS import PARAMETERS


class CALC_SPACE():
    def __init__(self):
        self.__context = acm.GetDefaultContext()
        self.__sheetType = 'FTradeSheet'
        self.__virtualPortfolio = acm.FAdhocPortfolio()
        self.__columnId = 'Portfolio Cash Vector'
        self.__traderPerGrouper = None
        self.__presentValueColumnId = 'Portfolio Present Value'
        self.__grouper = None
        self.__queryFolder = None
        self.__generateCalcSpace()
        self.__columnConfigCurrency = self.__createColumnConfigForCurrency()
        self.__setQueryFolder()
        self.__setGrouper()
    
    def __createColumnConfigForCurrency(self, currName=None):
        vector = acm.FArray()
        if currName:
            currencies = acm.FCurrency.Select("name={}".format(currName))
        else:
            currencies = acm.FCurrency.Select('')
        for currency in currencies:
            param = acm.FNamedParameters()
            param.AddParameter('currency', acm.FCurrency[currency.Name()])
            vector.Add(param)
        return acm.Sheet.Column().ConfigurationFromVector(vector)

    def calculateCashPerCurrency(self):
        return PARAMETERS.calcSpace.CreateCalculation(
            self.__virtualPortfolio,
            self.__columnId,
            self.__columnConfigCurrency)

    def __generateCalcSpace(self):
        PARAMETERS.calcSpace = acm.Calculations().CreateCalculationSpace(self.__context, self.__sheetType)
    
    def addTradesToVirtualPortfolio(self, fTrades):
        self.__virtualPortfolio = acm.FAdhocPortfolio()
        for trade in fTrades:
            self.__virtualPortfolio.Add(trade)
    
    def ApplyGlobalSimulation(self, columnId, value):
        PARAMETERS.calcSpace.SimulateGlobalValue(columnId, value)

    def RemoveGlobalSimulation(self, columnId):
        PARAMETERS.calcSpace.RemoveGlobalSimulation(columnId)

    def RemoveGlobalDateSimulations(self):
        self.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        self.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        self.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
        self.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')

    def ApplyGlobalDateSimulations(self, start_date=None, end_date=None):
        self.RemoveGlobalDateSimulations()
        if start_date:
            PARAMETERS.calcSpaceClass.ApplyGlobalSimulation('Portfolio Profit Loss Start Date', 'Custom Date')
            PARAMETERS.calcSpaceClass.ApplyGlobalSimulation('Portfolio Profit Loss Start Date Custom', start_date)
        if end_date:
            PARAMETERS.calcSpaceClass.ApplyGlobalSimulation('Portfolio Profit Loss End Date', 'Custom Date')
            PARAMETERS.calcSpaceClass.ApplyGlobalSimulation('Portfolio Profit Loss End Date Custom', end_date)
    
    def __setQueryFolder(self):
        self.__queryFolder = PARAMETERS.queryFolder.Query()
    
    def __setGrouper(self):
        self.__grouper = PARAMETERS.grouper.Grouper()
    
    def __walkingTheTree(self, fTreeIterator):
        dict = defaultdict(list)
        masterList = []
        queueDepth = fTreeIterator.Tree().Depth() + 1
        while fTreeIterator.NextUsingDepthFirst():
            idx = fTreeIterator.Tree().Depth() - queueDepth
            if len(masterList) >= idx + 1:
                masterList[idx] = fTreeIterator.Tree().Item().StringKey()
            else:
                masterList.append(fTreeIterator.Tree().Item().StringKey())
                
            if fTreeIterator.Tree().Item().IsKindOf(acm.FTradeRow):
                key = tuple(masterList[ : idx])
                dict[key].append(fTreeIterator.Tree().Item().Trade())
        
        return dict

    def setTradesPerGrouper(self):
        PARAMETERS.calcSpace.Clear()
        topNode = PARAMETERS.calcSpace.InsertItem(self.__queryFolder)
        topNode.ApplyGrouper(self.__grouper) 
        PARAMETERS.calcSpace.Refresh()
        self.__traderPerGrouper = self.__walkingTheTree(topNode.Iterator())
        return self.__traderPerGrouper

    def setupCalculation(self, trades):
        PARAMETERS.calcSpace.Clear()
        self.RemoveGlobalDateSimulations()
        self.addTradesToVirtualPortfolio(trades)

    def setupCalculationWithGrouper(self, trades, grouper):
        self.setupCalculation(trades)
        topNode = PARAMETERS.calcSpace.InsertItem(self.__virtualPortfolio)
        topNode.ApplyGrouper(grouper)
        PARAMETERS.calcSpace.Refresh()

    def calculateValue(self, calcObject, columnId=None, start_date=None, end_date=None):
        if columnId is None:
            columnId = self.__presentValueColumnId
        self.ApplyGlobalDateSimulations(start_date, end_date)
        return PARAMETERS.calcSpace.CreateCalculation(calcObject, columnId)

    def getPresentValue(self, trades):
        self.setupCalculation(trades)
        return self.calculateValue(self.__virtualPortfolio, self.__presentValueColumnId)
