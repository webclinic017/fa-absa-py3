""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FBenchmarkTrackingTM.py"
"""--------------------------------------------------------------------------
MODULE
    FBenchmarkTracking

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    FIndexTrackingTM represents the interface between the TradingManager
    and the portfolio based index tracking action.
-----------------------------------------------------------------------------"""

import acm
from FManualRebalanceTM import FManualRebalanceTM, RebalancingStrategiesMenuItem
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramAction import Action
from FTradeProgramUtils import CandidateTradeCreator

class BenchmarkTrackingTM(FManualRebalanceTM):
    def __init__(self, eii, action, targetColumnId, inputColumnId,
                 relativeTo=None, name=None):
        super(BenchmarkTrackingTM, self).__init__(eii, action, targetColumnId, inputColumnId,
                                                  name=name, isTarget=True, relativeTo=relativeTo)
        self._insertedZeroPositions = list()
    
    def InsertEmptyPositions(self):
        for row in self.sheet.Selection().SelectedRowObjects():
            portfolio = row.Portfolio()
            instruments = self.InstrumentsToAdd(portfolio, self.TrackingTarget(portfolio))
            for instrument in instruments:
                trade = CandidateTradeCreator(row, instrument).CreateTrade()
                trade.Simulate()
                self._insertedZeroPositions.append(trade)

    def RemoveInsertedPositions(self):
        for trade in self._insertedZeroPositions:
            trade.Unsimulate()
        self._insertedZeroPositions = list()

    @staticmethod
    def InstrumentsToAdd(portfolio, trackingTarget):
        try:
            return list(set(trackingTarget.Instruments()) - set(portfolio.Instruments()))
        except AttributeError:
            return list()

    @staticmethod
    def TrackingTarget(portfolio):
        pass

class IndexTracking(BenchmarkTrackingTM):

    @staticmethod
    def TrackingTarget(portfolio):
        try:
            return portfolio.AdditionalInfo().Index()
        except Exception:
            return None

class StoredWeightsTracking(IndexTracking):
    
    pass

class PortfolioTracking(BenchmarkTrackingTM):

    @staticmethod
    def TrackingTarget(portfolio):
        try:
            return portfolio.AdditionalInfo().ModelPortfolio()
        except Exception:
            return None

"""---------------------------------- Menu Items -----------------------------------"""

@Action
def GetPortfolioTrackingMenuItem(eii):
    return PortfolioTrackingMenuItem(eii)

@Action
def GetIndexTrackingMenuItem(eii):
    return IndexTrackingMenuItem(eii)

@Action 
def GetStoredWeightsTrackingMenuItem(eii):
    return StoredWeightsTrackingMenuItem(eii)

class BenchmarkTrackingMenuItem(RebalancingStrategiesMenuItem):

    def __init__(self, extObj, actionName, rebalanceClass=BenchmarkTrackingTM):
        super(BenchmarkTrackingMenuItem, self).__init__(extObj, actionName)
        self._rebalanceClass = rebalanceClass

    def EnabledFunction(self):
        try:
            portfolio = self._Selection().First().Portfolio()
            return bool(self._rebalanceClass.TrackingTarget(portfolio))
        except (RuntimeError, AttributeError):
            return False
    
    def TargetColumnId(self):
        return self._settings.TargetColumnId()
    
    def InputColumn(self):
        return self._settings.InputColumnId()
    
    def _InsertInputColumn(self):
        self._InsertColumn(self.InputColumn())

    def _InsertTargetColumn(self):
        self._InsertColumn(self.TargetColumnId())
    
    def InvokeAsynch(self, eii):
        self._InsertTargetColumn()
        self._InsertInputColumn()
        rebalance = self._InitiateRebalance(eii)
        rebalance.InsertEmptyPositions()
        self.Sheet().PrivateTestSyncSheetContents()
        rebalance.Execute()
        rebalance.RemoveInsertedPositions()

    def _InitiateRebalance(self, eii):
        rebalance = self._rebalanceClass(
            eii,
            action=self.Action(),
            targetColumnId=self.TargetColumnId(),
            inputColumnId=self.InputColumn(),
            relativeTo=self._settings.RelativeTo(),
            name=self._settings.Action())
        return rebalance


class IndexTrackingMenuItem(BenchmarkTrackingMenuItem):

    def __init__(self, extObj):
        super(IndexTrackingMenuItem, self).__init__(extObj, 'Index Tracking', IndexTracking)
        self._settings = ParameterSettingsCreator.FromRootParameter('IndexTrackingSettings')

class PortfolioTrackingMenuItem(BenchmarkTrackingMenuItem):

    def __init__(self, extObj):
        super(PortfolioTrackingMenuItem, self).__init__(extObj, 'Portfolio Tracking',  PortfolioTracking)
        self._settings = ParameterSettingsCreator.FromRootParameter('PortfolioTrackingSettings')
        
class StoredWeightsTrackingMenuItem(BenchmarkTrackingMenuItem):
    def __init__(self, extObj):
        super(StoredWeightsTrackingMenuItem, self).__init__(extObj, 'Stored Weights Tracking', StoredWeightsTracking)
        self._settings = ParameterSettingsCreator.FromRootParameter('StoredWeightsTrackingSettings')

"""---------------------------- Custom Functions -------------------------"""

def Index(row):
    return IndexTracking.TrackingTarget(row.Portfolio())

def CombInstrMap(instrument, index):
    return next((insMap for insMap in index.InstrumentMaps()
                 if insMap.Instrument() == instrument), None)

def ModelPortfolio(row):
    return PortfolioTracking.TrackingTarget(row.Portfolio())

def ModelPortfolioObject(row):
    portfolio = PortfolioTracking.TrackingTarget(row.Portfolio())
    if not portfolio:
        return None

    elif row.Class() is acm.FSingleInstrumentAndTrades:
        return acm.Risk.CreateSingleInstrumentAndTradesBuilder(
            portfolio,
            row.Instrument()).GetTargetInstrumentAndTrades()

    elif row.Class() is acm.FMultiInstrumentAndTrades:
        return acm.Risk.CreateMultiInstrumentAndTrades(
            portfolio,
            row.Grouping().Grouper(), row.Grouping().GroupingValues())

    elif row.Class() is acm.FPortfolioInstrumentAndTrades:
        return acm.Risk.CreatePortfolioInstrumentAndTrades(portfolio)
