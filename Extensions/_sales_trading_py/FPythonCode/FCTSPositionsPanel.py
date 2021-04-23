""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSPositionsPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCTSPositionsPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Displays the positions in the selected instrument and it's derivatives
    in the Portfolio set in the FParameter Portfolio

-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils

from FMultiSheetPanel import MultiSheetPanel


class CTSPositionsPanel(MultiSheetPanel):

    def __init__(self):
        MultiSheetPanel.__init__(self)

    def _PortfolioSheet(self):
        return self._GetSheetByIndex(0)

    def _TradeSheet(self):
        return self._GetSheetByIndex(1)

    def _ShowObjects(self, instruments):
        self._TradeSheet().RemoveAllRows()
        pSheet = self._PortfolioSheet()
        pSheet.RemoveAllRows()
        instrument = instruments[0] if instruments else None
        portfolio = acm.FPhysicalPortfolio[self.Settings().Portfolio()]
        if instrument and portfolio:
            self._InsertPositionFolder(pSheet, instrument, portfolio)

    def _InsertPositionFolder(self, sheet, instrument, portfolio):
        folder = acm.FASQLQueryFolder()
        query = self._CreateTradeQuery(instrument, portfolio)
        folder.AsqlQuery(query)
        folder.Name(portfolio.Name())
        sheet.InsertObject(folder, 'IOAP_REPLACE')
        self._GroupPositions(sheet)
        FSheetUtils.ExpandTree(sheet, 2)

    def _CreateTradeQuery(self, instrument, portfolio):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        self._AddPortfolioGroupNode(query, portfolio)
        self._AddInstrumentGroupNode(query, instrument)
        return query

    def _AddPortfolioGroupNode(self, query, portfolio):
       # pylint: disable-msg=W0106
        node = query.AddOpNode('OR')
        if portfolio.Compound():
            [self._AddPortfolioNode(node, p) for p in portfolio.SubPortfolios()]
        else:
            self._AddPortfolioNode(node, portfolio)

    def _AddInstrumentGroupNode(self, query, instrument):
        node = query.AddOpNode('OR')
        self._AddInstrumentAndUnderlyingNode(node, instrument)
        self._AddInstrumentAndUnderlyingNode(node, instrument.Underlying())

    @staticmethod
    def _AddPortfolioNode(node, portfolio):
        node.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())

    @staticmethod
    def _AddInstrumentAndUnderlyingNode(node, instrument):
        if instrument:
            node.AddAttrNode('Instrument.Name', 'EQUAL', instrument.Name())
            node.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', instrument.Name())

    def _GroupPositions(self, sheet):
        FSheetUtils.ApplyGrouperToSheet(sheet, 'Trade Portfolio')

    # ---- Handle events ----

    def _SendSheetChanged(self, sheet):
        if sheet == self._PortfolioSheet():
            tradeSheet = self._TradeSheet()
            tradeSheet.RemoveAllRows()
            selection = sheet.Selection()
            if selection:
                self._InsertTrades(tradeSheet, selection)

    def _InsertTrades(self, sheet, selection):
        sheet.InsertObject(None, 'IOAP_REPLACE')
        for trade in self._TradesToInsert(selection.SelectedCells()):
            sheet.InsertObject(trade, 'IOAP_LAST')

    def _TradesToInsert(self, cells):
        # pylint: disable-msg=W0640
        trades = acm.FSet()
        for cell in cells:
            if not cell.IsHeaderCell():
                filteredTrades = self._TradesAsList(cell)
                tradeFilter = self.GetFilter(cell.Column())
                if tradeFilter:
                    filteredTrades = filteredTrades.Filter(lambda trade: self.FilterFunc(trade, tradeFilter))
                trades.AddAll(filteredTrades or [])
        return trades.AsList().Sort()

    @staticmethod
    def _TradesAsList(cell):
        return cell.RowObject().Trades().AsList()

    def GetFilter(self, column):
        try:
            tradeFilter = acm.GetCalculatedValueFromString(acm.FObject,
                                                    column.Context(),
                                                    self.GetFilterName(column),
                                                    acm.GetGlobalEBTag()
                                                    ).Value()
            if tradeFilter.IsKindOf(acm.FObject):
                return tradeFilter
        except Exception:
            pass

    @staticmethod
    def GetFilterName(column):
        definition = column.Context().GetExtension(acm.FColumnDefinition,
                                                   acm.FTradingSheet,
                                                   column.ColumnId())
        return definition.Value().At('Filter', None)

    @staticmethod
    def FilterFunc(trade, tradeFilter):
        return tradeFilter.IsSatisfiedBy(trade.Instrument())
