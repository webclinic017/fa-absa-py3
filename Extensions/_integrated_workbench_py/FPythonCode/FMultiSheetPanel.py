""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FMultiSheetPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FMultiSheetPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils
import FEvent

from FPanel import Panel
from FIntegratedWorkbenchLogging import logger
from FIntegratedWorkbenchUtils import AsIterable

class MultiSheetPanel(Panel):

    def __init__(self):
        # pylint: disable-msg=W0612
        Panel.__init__(self)
        self._layout = None
        self._sheetObserver = FSheetUtils.SheetObserver(self)
        self._sheets = None
        self._orientationHorizontal = True
        self._lastGrouper = [None for x in self.Settings().Sheets()]
        if hasattr(self.Settings(), 'Orientation'):
            self._orientationHorizontal = (self.Settings().Orientation() != 'Vertical')

    # ---- Overrides from Panel ----

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        if self._orientationHorizontal:
            b.BeginHorzBox('None', '')
        else:
            b.BeginVertBox('None', '')
        for setting in self._SheetSettings():
            sheetType = setting.SheetType()
            contents = self._ContentsForCtrl(setting)
            logger.debug("MultiSheetPanel.CreateLayout() Adding sheet type: "
                "'%s' template: '%s'" % (sheetType, ''))
            b.AddCustom(setting.Name(), 'sheet.{0}'.format(sheetType), -1,
                self.Settings().Height(), -1, -1, contents)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self._layout = layout
        self._InitSheets()
        self.InitSheetContents()

    def InitSheetContents(self):
        initialContents = self.InitialContents()
        if initialContents:
            multiSheetContents = initialContents.At('multiSheetContents')
            if multiSheetContents and multiSheetContents.Keys():
                for key in multiSheetContents.Keys():
                    sheet = self._GetSheetByIndex(key)
                    sheet.SheetContents(multiSheetContents.At(key))

    def InitSubscriptions(self):
        for sheet in self._Sheets():
            sheet.AddDependent(self._sheetObserver)

    def RemoveSubscriptions(self):
        for sheet in self._Sheets():
            sheet.RemoveDependent(self._sheetObserver)

    # --- Defined in this class ---

    def GetContents(self):
        # Possibility to store more than just the sheet contents here
        if self._layout:
            d = acm.FDictionary()
            d.AtPut('multiSheetContents', acm.FDictionary())
            for sheet in self.Sheets():
                key = self._GetIndexFromSheet(sheet)
                content = sheet.SheetContents()
                d.At('multiSheetContents').AtPut(key, content)
            return d

    # ---- Protected methods ----

    def _InitSheets(self):
        # Make sure that the sheets are initialized
        if self._sheets == None:
            self._sheets = []
            for sheet in self.Sheets():
                self._sheets.append(sheet)

    def _GetSheetByIndex(self, idx):
        """ Return the control for sheet with given idx. """
        try:
            return self._sheets[idx]
        except (IndexError, TypeError):
            logger.debug('Could not get sheet from index %s in method _GetSheetByIndex()' % idx)

    def _GetIndexFromSheet(self, sheet):
        if self._sheets:
            try:
                return self._sheets.index(sheet)
            except IndexError:
                pass

    def _GetSheet(self, name):
        """ Return the sheet bound to the control with the given name. """
        try:
            return self._layout.GetControl(name).GetCustomControl()
        except AttributeError:
            logger.debug('Could not get sheet for control %s in method _GetSheet()' % name)

    def _ContentsForCtrl(self, settings):
        """ Return the contents to set on the layout builder for any control """
        contents = FSheetUtils.SheetContents(settings)
        return contents.ForControl()

    def _ClearAllSheets(self):
        """ Remove all rows from every sheet. """
        for sheet in self._Sheets():
            sheet.RemoveAllRows()

    def _SheetSettings(self):
        """ Return generator of the set of sheets shown in this panel. """
        for sheet in self.Settings().Sheets():
            yield sheet

    def _Sheets(self):
        for sheet in self.Settings().Sheets():
            yield self._GetSheet(sheet.Name())

    def _SendSheetChanged(self, sheet):
        pass

    def _InsertObjectAt(self, sheet, obj, pos, removeAllRows = False):
        assert sheet and obj
        if removeAllRows:
            sheet.RemoveAllRows()
        sheet.InsertObject(obj, pos)

    def _InsertObject(self, sheetIdx, obj, pos=None):
        sheet = self._GetSheetByIndex(sheetIdx)
        if not sheet:
            logger.error("MultiSheetPanel._InsertObject() Unable to get sheet with index %d" % sheetIdx)
            return

        if pos in ('IOAP_REPLACE', 'IOAP_SORTED'):
            self._InsertObjectAt(sheet, obj, pos)
        else:
            pos = pos if pos else 'IOAP_LAST'
            for o in AsIterable(obj):
                self._InsertObjectAt(sheet, o, pos, removeAllRows = True)

        grouper = FSheetUtils.GetGrouperFromSheet(sheet)
        if grouper:
            self._lastGrouper[sheetIdx] = grouper
        if self._lastGrouper[sheetIdx]:
            FSheetUtils.ApplyGrouperInstanceToSheet(sheet, self._lastGrouper[sheetIdx])

    def Sheets(self):
        return [self._GetSheet(sheet.Name()) for
                sheet in self.Settings().Sheets() if
                self._GetSheet(sheet.Name()) is not None]

    @FEvent.InternalEventCallback
    def OnSaveSheetAsTemplate(self, event):
        for sheetParam in self.Settings().Sheets():
            sheet = self._GetSheet(sheetParam.Name())
            if sheet is event.Sheet():
                FSheetUtils.SaveSheetAsTemplate(sheet, sheetParam.Name())
                break
