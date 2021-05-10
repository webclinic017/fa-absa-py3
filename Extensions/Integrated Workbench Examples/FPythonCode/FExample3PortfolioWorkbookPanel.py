""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExample3PortfolioWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExample3PortfolioWorkbookPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FWorkbookPanel import WorkbookPanel
from FEvent import EventCallback
from FSheetUtils import AsFolder



class Example3PortfolioWorkbookPanel(WorkbookPanel):

    @EventCallback
    def OnInstrumentsSelected(self, event):
        self.Sheet().RemoveAllRows()
        ins = self.GetInstrument(event.Objects())
        self.Sheet().InsertObject(AsFolder(ins, acm.FTrade), 0)
            
    def GetInstrument(self, insId):
        return acm.FInstrument[insId]