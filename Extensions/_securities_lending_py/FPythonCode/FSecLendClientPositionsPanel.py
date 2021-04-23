""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendClientPositionsPanel.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendClientPositionsPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Client View - Panel showing positions for the currently selected client.

------------------------------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FSecLendEvents import OnClientViewInstrumentsSelected, OnPositionSelection
from FSecLendCommon import ExtendedWorkbookPanel, WorkbenchSheet
import FSecLendHooks


class SecLendClientPositionsPanel(ExtendedWorkbookPanel):

    def RowSelectionChanged(self, selection):
        self.SendEvent(OnPositionSelection(self, selection.SelectedRowObjects()))



class SecLendClientViewPositionSheet(WorkbenchSheet):

    def __init__(self, workbook, settings):
        super(SecLendClientViewPositionSheet, self).__init__(workbook, settings)
        self._counterparty = None
        self._searchText = None
        self._filters = {}

    def SetFilterAttributes(self, filters):
        if filters != self._filters:
            self._filters = filters
            self.UpdateSheetContents()

    def SetPartialMatchFilterAttributes(self, filters):
        if filters != self._partialMatchFilters:
            self._partialMatchFilters = filters
            self.UpdateSheetContents()

    def ShowSheetContents(self):
        # Must have a client first selected before showing anything
        return bool(self._counterparty)

    def DefaultInsertItemQuery(self):
        return FSecLendHooks.ActiveLoansQuery()

    def ApplyAdditionalQueryFilters(self, query):
        orNodeCpty = query.AddOpNode('OR')
        orNodeCpty.AddAttrNode('Counterparty.Name', 'EQUAL', self._counterparty.Name())
        if self._searchText:
            instrumentName = '*{}*'.format(self._searchText)
            orNodeText = query.AddOpNode('OR')
            orNodeText.AddAttrNode('Instrument.Name', 'RE_LIKE_NOCASE', instrumentName)
        for attribute, value in self._filters.items():
            orNodeFilter = query.AddOpNode('OR')
            orNodeFilter.AddAttrNode(attribute, 'EQUAL', value)
        return query

    def QueryFolderLabel(self):
        portfolio = FSecLendHooks.DefaultPortfolio()
        if portfolio:
            return portfolio.Name()
        return super(SecLendClientViewPositionSheet, self).QueryFolderLabel()

    @EventCallback
    def OnClientViewCounterpartySelected(self, event):
        if event.Counterparty() != self._counterparty:
            self._counterparty = event.Counterparty()
            self.UpdateSheetContents()

    @EventCallback
    def OnClientViewPositionFilterChanged(self, event):
        filters = {}
        if event.Market():
            filters['Market.Name'] = event.Market().Name()
        if event.Currency():
            filters['Currency.Name'] = event.Currency().Name()
        if filters != self._filters:
            self._filters = filters
            self.UpdateSheetContents()

    @EventCallback
    def OnClientViewPositionInstrumentSearch(self, event):
        if event.SearchText() != self._searchText:
            self._searchText = event.SearchText()
            self.UpdateSheetContents()

    def RowSelectionChanged(self, selection):
        self.SendEvent(OnClientViewInstrumentsSelected(self, selection))


