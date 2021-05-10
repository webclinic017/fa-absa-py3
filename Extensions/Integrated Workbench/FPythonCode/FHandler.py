""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FHandler.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FHandler

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
   Base class of all handlers.
-------------------------------------------------------------------------------------------------------"""

__all__ = ['Handler']

from FWorkbenchObserver import WorkbenchObserver
from FParameterSettings import ParameterSettingsCreator
import FEvent

class Handler(object):

    def __init__(self, dispatcher=None):
        self._settings = None
        self._workbenchObserver = WorkbenchObserver(dispatcher, self)

    def Settings(self):
        if self._settings is None:
            self._settings = ParameterSettingsCreator.FromRootParameter(self.ClassName())
        return self._settings

    def SendEvent(self, event):
        self._workbenchObserver.SendEvent(event)

    def CreateEvent(self, name, *args, **kwargs):
        return self._workbenchObserver.CreateEvent(name, *args, **kwargs)

    @FEvent.InternalEventCallback
    def OnViewDestroyed(self, event):
        self.HandleViewDestroyed(event.View())

    def HandleViewDestroyed(self, view):
        """Override to decide when to react to OnViewDestroyed event"""
        pass

    def ClassName(self):
        return self.__class__.__name__

    def Name(self):
        return self.ClassName()

    def ReactOnEvent(self):
        return True

    @classmethod
    def Create(cls, dispatcher):
        return cls(dispatcher)
