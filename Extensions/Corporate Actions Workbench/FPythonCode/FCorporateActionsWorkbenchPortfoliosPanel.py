""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchPortfoliosPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchPortfoliosPanel

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils

from FSheetPanel import SheetPanel
from FCorpActionsWorkbenchLogger import logger
from FEvent import EventCallback, BaseEvent, CreateEvent
from FCorpActionUtils import GetTradesForAction, BuildASQLQueryFolder

class CorporateActionsWorkbenchPortfoliosPanel(SheetPanel):

    COLUMN_ID = 'Corp Action Parameter'
    
    def __init__(self):
        super(CorporateActionsWorkbenchPortfoliosPanel, self).__init__()
        self._action = None

    def SendPortfoliosSelectedEvent(self, objs, corpAction):
        event = CreateEvent('OnPortfoliosSelected', 
                            BaseEvent, 
                            self, 
                            objects=objs, 
                            action=corpAction)
        self.SendEvent(event)

    def SelectionChanged(self, selection):
        self.SendPortfoliosSelectedEvent(selection.SelectedRowObjects(), 
                                        self._action)

    def CleanConnectedSheets(self):
        self._action = None
        self.Sheet().RemoveAllRows()
        self.SendPortfoliosSelectedEvent([], 
                                        None)

    @EventCallback
    def OnCorporateActionSelected(self, event):
        self.CleanConnectedSheets()
        for row in event.Objects():
            self._action = self.GetActionFromRow(row)
            self.InsertPositionsFromAction(self._action)
            self.ApplyCorpAction(self._action)
            break

    def ApplyCorpAction(self, action):
        self.Sheet().SimulateGlobalValue(self.COLUMN_ID, action)
                
    def InsertPositionsFromAction(self, action):
        if action:
            self.Sheet().InsertObject(BuildASQLQueryFolder(action), 'IOAP_LAST')
            FSheetUtils.ExpandTree(self.Sheet())
            self.Sheet().PrivateTestSyncSheetContents()
            return
        else:
            self.Sheet().RemoveAllRows()

    @staticmethod
    def GetActionFromRow(row):
        return row if row.IsKindOf(acm.FCorporateAction) else None
    
