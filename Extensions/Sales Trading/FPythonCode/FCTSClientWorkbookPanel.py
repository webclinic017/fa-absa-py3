""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSClientWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSClientWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils

from FWorkbookPanel import WorkbookPanel
from FCTSEvents import CTSClientPositionsSelected
from FEvent import EventCallback

class CTSClientWorkbookPanel(WorkbookPanel):

    def __init__(self, application):
        super(CTSClientWorkbookPanel, self).__init__(application)
        self._currentClient = None

    @EventCallback
    def CTSClientNavigationChanged(self, event):
        self._currentClient = event.First()
        sheet = self.Sheet()
        if self._currentClient:
            clientName = self._currentClient.Name()
            query = acm.CreateFASQLQuery('FTrade', 'AND')
            query.AddAttrNode('Counterparty.Name', 'EQUAL', clientName)

            folder = acm.FASQLQueryFolder()
            folder.Name(clientName)
            folder.AsqlQuery(query)

            self.Sheet().InsertObject(folder)
            sheet.RowTreeIterator(0).Tree().Expand(True, 1000)
        else:
            sheet.RemoveAllRows()

    def SelectionChanged(self, selection):
        if selection and self._currentClient:
            self.SendEvent(CTSClientPositionsSelected(self,
                                              FSheetUtils.SelectedInstruments(selection),
                                              self._currentClient))
