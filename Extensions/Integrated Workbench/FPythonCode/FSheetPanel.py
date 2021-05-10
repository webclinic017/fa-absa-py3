""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FSheetPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSheetPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Panel specialization to display a sheet.
-------------------------------------------------------------------------------------------------------"""

__all__ = ['SheetPanel']

import acm
import FSheetUtils
import FGrouperUtils
import FEvent

from FPanel import Panel
from FACMObserver import SheetObserver
from FIntegratedWorkbenchLogging import logger

class SheetPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        self._sheet = None
        self._sheetObserver = None
        self._lastGrouper = None

    def SelectionChanged(self, selection):
        pass

    def RowSelectionChanged(self, selection):
        pass

    def ColumnSelectionChanged(self, selection):
        pass

    def OnDestroy(self):
        pass

    def SheetType(self):
        """ Return the sheet type. """
        return self.Settings().SheetType()

    def SheetObserver(self):
        if self._sheetObserver is None:
            self._sheetObserver = SheetObserver(self)
        return self._sheetObserver

    def Caption(self):
        """ Return the sheet caption. """
        return self.Settings().Caption()

    def Width(self):
        return self.Settings().Width()

    def Height(self):
        return self.Settings().Height()

    def SettingsContents(self):
        return FSheetUtils.SheetContents(self.Settings()).ForControl()

    def GetContents(self):
        try:
            contents = acm.FDictionary()
            contents.AtPut('sheetContents', self.Sheet().Sheet().SheetContents())
            return contents
        except AttributeError as error:
            logger.debug('Failed to return contents for sheet %s. Reason: %s', self, error)

    def IncludeRows(self):
        """ Return if rows should be included when saving
            the sheet as template. """
        return self.Settings().IncludeRows()

    def Sheet(self, wrappedUxSheet=None):
        """ Return the sheet """
        if wrappedUxSheet is None:
            return self._sheet
        self._sheet = wrappedUxSheet

    def CreateLayout(self):
        logger.debug("SheetPanel.CreateLayout(%s)" % (self.Name()))
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b. AddCustom('__Sheet', 'sheet.{0}'.format(self.SheetType()),
            self.Width(), self.Height(), -1, -1, self.SettingsContents())
        b.EndBox()
        logger.debug("CustomControlSheetImpl.CreateLayout() "
            "sheet type: '%s'" % (self.SheetType()))
        return b

    def InitControls(self, layout):
        logger.debug("SheetPanel.InitControls(%s)" % (self.Name()))
        wrappedUxSheet = FSheetUtils.Sheet(layout.GetControl('__Sheet').GetCustomControl())
        self.Sheet(wrappedUxSheet)
        if self.Settings().Grouper():
            grouper = FGrouperUtils.GetGrouper(self.Settings().Grouper(), self.Settings().SheetType())
            self.Sheet().LastGrouper(grouper)
        self.InitSheetContents()
        self.InitCustomControls(layout)

    def InitSheetContents(self):
        initialContents = self.InitialContents()
        if initialContents and initialContents.At('sheetContents'):
            self.Sheet().Sheet().SheetContents(initialContents.At('sheetContents'))

    def InitCustomControls(self, layout):
        """ Implement to add to InitControls call """
        pass

    def InitSubscriptions(self):
        self.Sheet().AddDependent(self.SheetObserver())

    def RemoveSubscriptions(self):
        self.Sheet().RemoveDependent(self.SheetObserver())

    @FEvent.InternalEventCallback
    def OnSaveSheetAsTemplate(self, event):
        if self.Sheet().Sheet() is event.Sheet():
            FSheetUtils.SaveSheetAsTemplate(self.Sheet().Sheet(), self.Name())


class DefaultSheetPanel(SheetPanel):
    pass
