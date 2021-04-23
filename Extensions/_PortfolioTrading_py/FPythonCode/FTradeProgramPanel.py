""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramPanel

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Panel that displays the generated candidate trades
-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils
from FSheetPanel import SheetPanel
from FTradeProgramTM import FTradeProgramExport
from FIntegratedWorkbenchLogging import logger
from FParameterSettings import ParameterSettingsCreator
from FEvent import EventCallback

class ActiveProgramPanelBase(SheetPanel):

    def __init__(self):
        super(ActiveProgramPanelBase, self).__init__()
        self._currentObject = None

    def ReactOnEvent(self):
        return True

    def DoTradeProgramExport(self, path):
        try:
            items = [self._currentObject]
            grouper = self._lastGrouper
            tmplName = ParameterSettingsCreator.FromRootParameter('TradeProgramSettings').ExportTemplate()
            if tmplName:
                template = acm.FTradingSheetTemplate[tmplName]
                assert template, 'No template with name {0}'.format(tmplName)
                export = FTradeProgramExport(items, grouper, sheetTemplate=template)
            else:
                export = FTradeProgramExport(items, grouper, creators=self.Sheet().ColumnCreators())
            export.ToFile(path)
        except Exception as e:
            logger.error(e, exc_info=True)
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'Export failed: {0}'.format(e))


    def _Insert(self, obj):
        self.Sheet().InsertObject(obj, 'IOAP_REPLACE')

    def Trades(self):
        try:
            return self._SelectedTrades() or self._currentObject.Trades()
        except AttributeError:
            return []

    def _SelectedTrades(self):
        self.Sheet().PrivateTestSyncSheetContents()
        selection = self.Sheet().SelectedRows().SelectedRowObjects()
        return FSheetUtils.SelectedTrades(selection)

    @EventCallback
    def OnTradeProgramExport(self, event):
        if self.IsVisible():
            self.DoTradeProgramExport(event.Path())

class TradeProgramCandidateTradesPanel(ActiveProgramPanelBase):

    @EventCallback
    def OnCandidateTradesChanged(self, event):
        if not self.IsVisible():
            self.Visible(True)

        candidateTrades = event.CandidateTrades()
        self._SetCurrentObject(candidateTrades)
        self._Insert(self._currentObject)

    @EventCallback
    def OnCandidateTradesCleared(self, event):
        self._SetCurrentObject(None)
        self._Insert(None)

    def _SetCurrentObject(self, candidateTrades):
        self._currentObject = []
        if candidateTrades:
            for action, trades in candidateTrades._tradesPerAction.iteritems():
                self._currentObject.append(FSheetUtils.GetTradesAsFolder(trades, str(action)))