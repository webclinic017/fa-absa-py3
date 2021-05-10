""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FMatrixViewerPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FMatrixViewerPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import FSheetUtils

from FSheetPanel import SheetPanel


class MatrixViewerPanel(SheetPanel):

    def DisplayMatrix(self, objects):
        folders = FSheetUtils.AsFolders(objects)
        for folder in folders:
            self._AddDateToQuery(folder, self.Settings().FromDate())
            self._AddTypesToQuery(folder, self.Settings().ExcludedTypes())
        self.Sheet().InsertObject(folders)
        self.Sheet().ExpandTree()

    @staticmethod
    def _AddDateToQuery(folder, date):
        query = folder.AsqlQuery()
        query.AddAttrNode('activityTime', 'GREATER', date)
    
    @staticmethod
    def _AddTypesToQuery(folder, types):
        query = folder.AsqlQuery().AddOpNode('OR')
        for salesActivityType in types:
            query.AddAttrNode('type', 'NOT_EQUAL', salesActivityType)
