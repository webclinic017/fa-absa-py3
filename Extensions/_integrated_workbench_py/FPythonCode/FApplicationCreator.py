""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FApplicationCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FApplicationCreator

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Internal classes for creating handlers and panels.
-------------------------------------------------------------------------------------------------------"""

import acm
from FIntegratedWorkbenchLogging import creationLogger
from FSheetUtils import SheetContents

def DoStartApplication(settings):
    return ApplicationCreator.FromSettings(settings).CreateApplication()


class ApplicationCreator(object):

    MANAGER_BASE_APPS = ('Trading Manager', 'Operations Manager')

    def __init__(self, settings):
        self._settings = settings

    def ApplicationName(self):
        return self._settings.Application()

    def Settings(self):
        return self._settings

    def CreateApplication(self):
        return self._CreateApplication()

    def _CreateApplication(self):
        return self._StartApplication()

    def _StartApplication(self, contents=None):
        try:
            return acm.StartApplication(self.ApplicationName(), contents)
        except Exception as e:
            creationLogger.error('Failed to start application %s. Reason: %s.', self.ApplicationName(), e)

    @classmethod
    def FromSettings(cls, settings):
        applicationName = settings.Application()
        if cls.IsManagerBase(applicationName):
            return ManagerBaseApplcationCreator(settings)
        return cls(settings)

    @classmethod
    def IsManagerBase(cls, applicationName):
        return applicationName in cls.MANAGER_BASE_APPS


class ManagerBaseApplcationCreator(ApplicationCreator):

    def _Sheets(self):
        return self.Settings().Main().Sheets()

    def _HasSheets(self):
        return bool(list(self._Sheets()))

    def _CreateApplication(self):
        if self._HasSheets():
            return self._CreateApplicationFromSheets()
        return self._StartApplication()

    def _CreateApplicationFromSheets(self):
        sheets = self._Sheets()
        sheet = next(sheets)
        if self.IsValid(sheet):
            app = self._StartApplication(self._Contents(sheet))
            uxWorkbook = app.ActiveWorkbook()
            for sheet in sheets:
                if self.IsValid(sheet):
                    self.AddSheet(uxWorkbook, sheet)
            uxWorkbook.ActivateSheet(uxWorkbook.Sheets().First())
            return app
        return self._StartApplication()

    @classmethod
    def AddSheet(cls, uxWorkbook, sheet):
        contents = cls._Contents(sheet)
        if contents.IsKindOf(acm.FSheetSetup):
            uxWorkbook.NewSheet(cls._SheetClassName(sheet),
                                sheet.Columns(),
                                cls._Contents(sheet)
                               )
        else:
            uxWorkbook.InsertSheet(contents)

    @staticmethod
    def _Contents(sheet):
        return SheetContents(sheet).ForApplication()

    @staticmethod
    def _SheetClassName(sheet):
        return sheet.SheetType()[1:]


    @classmethod
    def IsValid(cls, settings):
        # Not clear... checks if not string. also in panelCreator
        return not isinstance(settings, str)
