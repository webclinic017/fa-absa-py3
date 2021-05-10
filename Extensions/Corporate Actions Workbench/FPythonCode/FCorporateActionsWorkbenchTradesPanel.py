""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchTradesPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchTradesPanel

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm

from FEvent import EventCallback
from FSheetPanel import SheetPanel
from FCorpActionsWorkbenchLogger import logger


class CorporateActionsWorkbenchTradesPanel(SheetPanel):

    def __init__(self):
        super(CorporateActionsWorkbenchTradesPanel, self).__init__()
        self._action = None

    @EventCallback
    def OnPortfoliosSelected(self, event):
        self._action = event.Action()
        folders = (self.CreateFolder(rowObj) for rowObj in event.Objects())
        self.Sheet().InsertObject(folders)
        
    def CreateFolder(self, rowObject):
        # Show ALL (eligible and generated) trades to avoid confusion
        return rowObject

