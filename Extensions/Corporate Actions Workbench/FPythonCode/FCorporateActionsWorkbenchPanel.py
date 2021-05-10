""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchPanel


DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from FWorkbookPanel import WorkbookPanel
from FCorporateActionsWorkbenchEvent import OnCorporateActionSelected
from FCorpActionsWorkbenchLogger import logger

class CorporateActionsWorkbenchPanel(WorkbookPanel):

        
    def SelectionChanged(self, selection):

        selectedCorpActions = set()
        rowObjects = selection.SelectedRowObjects()
        for rowObject in rowObjects:
            if rowObject.IsKindOf(acm.FTreeBuilderMultiItem):
                for action in rowObject.Actions():
                    selectedCorpActions.add(action)
            elif rowObject.IsKindOf(acm.FCorporateAction):
                selectedCorpActions.add(rowObject)
        self.SendEvent(OnCorporateActionSelected(self, selectedCorpActions))

