""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchElectionsPanel.py"
import acm
import FSheetUtils
from FCorporateActionsWorkbenchUtils import AddEntitiestoSheet
from FSheetPanel import SheetPanel
from FEvent import EventCallback
from FCorporateActionsWorkbenchEvent import OnCorporateActionSelected
from FCorporateActionsWorkbenchEvent import OnCorporateActionElectionSelected
from FCorpActionsWorkbenchLogger import logger


def buildQuery(acmObjList):
    query = acm.CreateFASQLQuery(acm.FCorporateActionElection, 'AND')
    orNode = query.AddOpNode('OR')
    for ca in acmObjList:
        andNode = orNode.AddOpNode('AND')
        andNode.AddAttrNode('CaChoice.CorpAction.Oid', 'EQUAL', ca.Oid())
    return query


class CorporateActionsWorkbenchElectionsPanel(SheetPanel):

    def __init__(self):
        super(CorporateActionsWorkbenchElectionsPanel, self).__init__()
        self._selectedActions = []

    def SelectionChanged(self, selection):
        rowObjects = selection.SelectedRowObjects()
        self.SendEvent(OnCorporateActionElectionSelected(self, rowObjects))

    @EventCallback
    def OnCorporateActionSelected(self, event):
        self._selectedActions[:] = []
        
        for rowObject in event.Objects():
            self._selectedActions.append(rowObject)
        self.InsertCorporateActionElections()

    def SortbyColumn(self):
        settings = self.Settings()
        if hasattr(settings, 'SortColumn') and settings.SortColumn():
            col_order = settings.SortColumn().split(':')
            columnName = col_order[0].strip()
            ascending = col_order[1].strip().upper() == 'ASCENDING'
        else:
            columnName = 'Eligible Position'
            ascending = True

        cIter = self.Sheet().Sheet().GridColumnIterator().First()
        while cIter:
            if cIter.GridColumn().ColumnId().Text() == columnName:
                self.Sheet().Sheet().SortColumn(cIter, ascending)
                break
            cIter = cIter.Next()

    def InsertCorporateActionElections(self):
        if not self._selectedActions:
            self.Sheet().RemoveAllRows()
        else:    
            query = buildQuery(self._selectedActions)
            folderName = 'Corporate Actions'
            if self.Settings().Folder():
                folderName = self.Settings().Folder()
            AddEntitiestoSheet(self.Sheet(),
                               query,
                               folderName)
            self.SortbyColumn()
