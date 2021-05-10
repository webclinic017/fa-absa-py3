""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FMainPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FMainPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of utility functions used by the sheet panels.
-------------------------------------------------------------------------------------------------------"""

import acm


from FACMObserver import ACMObserver
from FWorkbenchObserver import WorkbenchObserver
from FParameterSettings import ParameterSettingsCreator


class MainPanel(object):

    ON_IDLE_FREQ = 0.5

    def __init__(self, application):
        self._settings = None
        self._application = application
        self._workbenchObserver = None
        self._applicationObserver = None
        self._onIdleCallback = None
        self.HandleCreate()

    def HandleCreate(self):
        self.Application().AddDependent(self.ApplicationObserver())
        self.InitOnIdleCallback()

    def HandleDestroy(self):
        self.RemoveOnIdleCallback()
        self.Application().RemoveDependent(self.ApplicationObserver())
        self.SendEvent(self.CreateEvent('OnPanelDestroyed'))

    def ApplicationObserver(self):
        if self._applicationObserver is None:
            self._applicationObserver = ACMObserver(self)
        return self._applicationObserver

    def SetWorkbenchObserver(self, dispatcher):
        self._workbenchObserver = WorkbenchObserver(dispatcher, self)
        self.SendEvent(self.CreateEvent('OnPanelInitialized'))

    def Application(self):
        return self._application

    def InitOnIdleCallback(self):
        if self._onIdleCallback is None:
            self._onIdleCallback = acm.Time.Timer().CreatePeriodicTimerEvent(
                    self.ON_IDLE_FREQ, self.OnHandleOnIdle, None)

    def RemoveOnIdleCallback(self):
        acm.Time.Timer().RemoveTimerEvent(self._onIdleCallback)
        self._onIdleCallback = None

    def OnHandleOnIdle(self, *args):
        pass

    def SendEvent(self, event):
        self._workbenchObserver.SendEvent(event)

    def CreateEvent(self, name, *args, **kwargs):
        return self._workbenchObserver.CreateEvent(name, *args, **kwargs)

    def Settings(self):
        if self._settings is None:
            self._settings = ParameterSettingsCreator.FromRootParameter(self.ClassName())
        return self._settings

    def ClassName(self):
        return self.__class__.__name__

    def Name(self):
        return self.ClassName()

    def ReactOnEvent(self):
        return True

    @classmethod
    def Create(cls, application):
        return cls(application)


class DefaultMainPanel(MainPanel):

    def HandleAspect(self, aspect, *args):
        self.SendEvent(self.CreateEvent('On' + aspect, params=args))
