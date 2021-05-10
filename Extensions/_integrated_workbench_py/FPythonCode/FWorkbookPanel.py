""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


from FMainPanel import MainPanel
from FACMObserver import WorkbookObserver

import FSheetUtils
import FEvent

class WorkbookPanel(MainPanel):

    def __init__(self, application):
        super(WorkbookPanel, self).__init__(application)
        self._sheet = None

    def ApplicationObserver(self):
        if self._applicationObserver is None:
            self._applicationObserver = WorkbookObserver(self)
        return self._applicationObserver

    def Sheet(self):
        activeSheet = self.Application().ActiveSheet()
        if self._sheet is None:
            self._sheet = FSheetUtils.Sheet(activeSheet)
        self._sheet.Sheet(activeSheet)
        return self._sheet


class DefaultWorkbookPanel(WorkbookPanel):
    """ Default implementation of a Workbook panel. Will dispatch
        events to the view for changes in the workbook sheet. """

    def Notify(self, name, selection):
        try:
            event = self.CreateEvent(name, selection, baseClass=FEvent.OnObjectsSelected)
            self.SendEvent(event)
        except IndexError:
            pass

    """ Event callbacks passing on and refining the core
        'selection changed' callback. """
    def SelectionChanged(self, selection):
        self.Notify('OnSelectionChanged', selection)

    def RowSelectionChanged(self, selection):
        self.Notify('OnRowSelectionChanged', selection)

    def ColumnSelectionChanged(self, selection):
        self.Notify('OnColumnSelectionChanged', selection)

    def SheetSelectionChanged(self, selection):
        self.Notify('OnSheetSelectionChanged', selection)
