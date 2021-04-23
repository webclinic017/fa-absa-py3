""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FACMObserver.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FACMObserver

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

__all__ = [
    'ACMObserver',
    'ApplicationObserver',
    'SheetObserver',
    'WorkbookObserver'
    ]

from FIntegratedWorkbenchLogging import logger


class ACMObserver(object):
    """ Helper class for listening to ServerUpdates from an acm object. """

    def __init__(self, parent):
        self._parent = parent

    def Parent(self):
        return self._parent

    def HandleDestroy(self, sender, param):
        self.Parent().HandleDestroy()

    def HandleSelectionChanged(self, sender, param):
        self.Parent().SelectionChanged(sender)

    def HandleAspect(self, sender, aspect, *args):
        self.Parent().HandleAspect(aspect, *args)

    def HandleServerUpdate(self, sender, aspect, param):
        try:
            if aspect == 'SelectionChanged':
                self.HandleSelectionChanged(sender, param)
            elif aspect == 'OnDestroy':
                self.HandleDestroy(sender, param)
            else:
                self.HandleAspect(sender, aspect, param)
        except AttributeError:
            logger.debug("Observer tried to dispatch event with "
                         "aspect {0} to {1}".format(aspect, self.Parent()))

    def ServerUpdate(self, sender, aspectSymbol, param=None):
        try:
            self.HandleServerUpdate(sender, str(aspectSymbol), param)
        except Exception as exc:
            logger.error("Observer.ServerUpdate() Exception:")
            logger.error(exc, exc_info=True)


class ApplicationObserver(ACMObserver):

    def __init__(self, parent):
        super(ApplicationObserver, self).__init__(parent)


class SheetObserver(ACMObserver):

    def __init__(self, parent):
        super(SheetObserver, self).__init__(parent)
        self._selectedColumn = None
        self._selectedCells = None
        self._selectedRows = None

    def _UpdateSelection(self, selection):
        self._selectedRows = self._RowsFromSelection(selection)
        self._selectedColumn = self._ColumnsFromSelection(selection)
        self._selectedCells = self._CellsFromSelection(selection)

    def _RowsFromSelection(self, selection):
        if selection:
            return set(selection.SelectedRowObjects())

    def _ColumnsFromSelection(self, selection):
        if selection:
            return set(cell.Column() for cell in selection.SelectedCells())

    def _CellsFromSelection(self, selection):
        if selection:
            return selection.SelectedCells()

    def _HasRowChanged(self, selection):
        return self._selectedRows != self._RowsFromSelection(selection)

    def _HasColumnChanged(self, selection):
        return self._selectedColumn != self._ColumnsFromSelection(selection)

    def HandleSelectionChanged(self, sender, param):
        selection = sender.Selection()
        for function in self._ChangeFunctions(selection):
            try:
                getattr(self.Parent(), function)(selection)
            except AttributeError:
                pass
        self._UpdateSelection(selection)

    def _ChangeFunctions(self, selection):
        yield 'SelectionChanged'
        if self._HasRowChanged(selection):
            yield 'RowSelectionChanged'
        if self._HasColumnChanged(selection):
            yield 'ColumnSelectionChanged'


class WorkbookObserver(SheetObserver):

    def __init__(self, parent):
        super(WorkbookObserver, self).__init__(parent)
        self._activeSheet = None

    def HasSheetChanged(self, sheet):
        return self.ActiveSheet() != sheet

    def IsValidSheet(self):
        # Check if stored sheet is valid or has been destroyed
        try:
            self._activeSheet.AsString()
            return True
        except AttributeError:
            return True
        except RuntimeError:
            return False

    def ActiveSheet(self, activeSheet=None):
        if activeSheet is None:
            if not self.IsValidSheet():
                self._activeSheet = None
            return self._activeSheet
        self._activeSheet = activeSheet

    def HandleSheetChanged(self, sheet):
        if self.HasSheetChanged(sheet):
            try:
                self.ActiveSheet(sheet)
                getattr(self.Parent(), 'SheetChanged')(sheet)
            except Exception:
                pass

    def HandleSelectionChanged(self, sender, param):
        sheet = sender.ActiveSheet()
        self.HandleSheetChanged(sheet)
        super(WorkbookObserver, self).HandleSelectionChanged(sheet, param)
