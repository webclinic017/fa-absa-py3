""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryActiveLoansPanels.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInventoryActiveLoansPanels

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Inventory View - Panel displaying the currently selected security loan instrument(s)
                     and active trades/positions in them.

------------------------------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FSecLendCommon import CommonSheetPanelBase
import FSecLendHooks
from FSecLendUtils import ASQLPortfolioProvider, ActiveLoansBaseQuery
from FSecLendEvents import OnInventoryViewInventoryViewPositionSelected


class SecLendInventoryActiveLoansPanel(CommonSheetPanelBase):

    def __init__(self):
        super(SecLendInventoryActiveLoansPanel, self).__init__()
        self._instrument = None

    def UpdateInventorySheetContents(self, instrument, status=None):
        if instrument:
            query = ActiveLoansBaseQuery()
            orNodeUnd = query.AddOpNode('OR')
            orNodeUnd.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', instrument.Name())
            orNodePort = query.AddOpNode('OR')
            portfolio = FSecLendHooks.DefaultPortfolio()
            if portfolio:
                prtfs = portfolio.AllPhysicalPortfolios() if portfolio.IsKindOf(acm.FCompoundPortfolio) else [portfolio]
                for prtf in prtfs:
                    orNodePort.AddAttrNode('Portfolio.Name', 'EQUAL', prtf.Name())
            if status:
                query.AddAttrNodeEnum('Status', status)
            folder = acm.FASQLQueryFolder()
            folder.Name('{0} - {1}'.format(instrument.Name(), portfolio.Name()))
            folder.AsqlQuery(query)
            asqlPortfolio = ASQLPortfolioProvider().GetOrCreateFromQuery(folder)
            self.SetSheetContents(asqlPortfolio)

    def SelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        if rowObjects:
            self.SendEvent(OnInventoryViewInventoryViewPositionSelected(self, rowObjects))

    def ClearPositionSelection(self):
        self.SendEvent(OnInventoryViewInventoryViewPositionSelected(self, None))

class SecLendInventoryActivePanel(SecLendInventoryActiveLoansPanel):

    def SetSheetContents(self, folder):
        self.Sheet().InsertObject(folder, 'IOAP_REPLACE')
        self.Sheet().RowTreeIterator(0).Tree().Expand(True, self.Settings().ExpandTreeLevels())
        rowIter = self.Sheet().RowTreeIterator(True).FirstChild()
        rowIter.Tree().VisibilityController().ShowZeroPositions(False)

    @EventCallback
    def OnInventoryViewInstrumentsSelected(self, event):
        """Active should have all trades statues since it's a portfolio sheet. exclusion should be
        done in the valuation parameters."""
        instrument = event.GetUnderlyingOrSelf()
        if self._instrument != instrument:
            self._instrument = instrument
            self.UpdateInventorySheetContents(instrument)
            self.ClearPositionSelection()



class SecLendInventoryPendingPanel(SecLendInventoryActiveLoansPanel):

    def SetSheetContents(self, folder):
        self.Sheet().InsertObject(folder, 'IOAP_REPLACE')
        self.Sheet().RowTreeIterator(0).Tree().Expand(True, self.Settings().ExpandTreeLevels())

    @EventCallback
    def OnInventoryViewInstrumentsSelected(self, event):
        """Filter on trade status here since pending will have only the trades not yet
         settled"""
        instrument = event.GetUnderlyingOrSelf()
        if self._instrument != instrument:
            self._instrument = instrument
            self.UpdateInventorySheetContents(instrument, FSecLendHooks.FillTradeStatus())
            self.ClearPositionSelection()