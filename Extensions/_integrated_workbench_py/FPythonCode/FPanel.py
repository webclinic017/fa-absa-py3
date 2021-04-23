""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Panel is the base class of all panels.
-------------------------------------------------------------------------------------------------------"""

__all__ = ['Panel']

import inspect
import FEvent
from FUxCore import LayoutPanel
from FWorkbenchObserver import WorkbenchObserver
from FParameterSettings import ParameterSettingsCreator
from FIntegratedWorkbenchLogging import logger

class PanelInterface(LayoutPanel, object):
    """ Methods to be defined in panel implementations. """

    def CreateLayout(self):
        """ Called to get the FUxLayoutBuilder for this panel. """
        raise NotImplementedError

    def InitControls(self, layout):
        """ Perform custom initailization of the panel. """
        raise NotImplementedError

    def InitSubscriptions(self):
        """ Initialize custom subscriptions. """
        pass

    def RemoveSubscriptions(self):
        """ Remove custom subscriptions. """
        pass

    def HandleViewCreated(self, view):
        """Override to decide when to react to OnViewCreated event"""
        pass

    def HandleViewDestroyed(self, view):
        """Override to decide when to react to OnViewDestroyed event"""
        pass


class Panel(PanelInterface):

    def __init__(self, *args):
        self._settings = None
        self._workbenchObserver = None

    def Visible(self, visible):
        self.SendEvent(FEvent.OnPanelVisibilityChanged(self, self.Name(), visible=visible))

    def IsKindOf(self, typeName):
        for cls in inspect.getmro(self.__class__):
            if cls.__name__ == typeName:
                return True
        return False

    def HandleCreate(self):
        try:
            logger.debug("Panel.HandleCreate(%s) Creating" % (self.ClassName()))
            panelLayout = self.CreateLayout()
            layout = None
            if panelLayout:
                layout = self.SetLayout(panelLayout)
            self.InitControls(layout)
            self.InitSubscriptions()
            self.EnableOnIdleCallback(True)
            logger.debug("Panel.HandleCreate(%s) Creating, done" % (self.ClassName()))
        except Exception as exc:
            logger.error("Panel.HandleCreate(%s) Unable to create:" % (self.ClassName()))
            logger.error(exc, exc_info=True)

    def HandleDestroy(self):
        logger.debug("Panel.OnDestroy(%s) Destroying" % (self.ClassName()))
        self.EnableOnIdleCallback(False)
        self.SendEvent(self.CreateEvent('OnPanelDestroyed'))
        self.WorkbenchObserver().StopObserving()
        self.RemoveSubscriptions()

    def OnHandleOnIdle(self):
        pass

    def SetWorkbenchObserver(self, dispatcher):
        self._workbenchObserver = WorkbenchObserver(dispatcher, self)
        self.SendEvent(self.CreateEvent('OnPanelInitialized'))

    def WorkbenchObserver(self):
        return self._workbenchObserver or WorkbenchObserverDummy(self)

    def SendEvent(self, event):
        self.WorkbenchObserver().SendEvent(event)

    def CreateEvent(self, name, *args, **kwargs):
        return self.WorkbenchObserver().CreateEvent(name, *args, **kwargs)

    def Settings(self):
        if self._settings is None:
            self._settings = ParameterSettingsCreator.FromRootParameter(self.ClassName())
        return self._settings

    def ClassName(self):
        return self.__class__.__name__

    def Name(self):
        return self.ClassName()

    def IsVisible(self):
        try:
            return self.Owner().IsDockWindowVisible(self.Name())
        except Exception:
            return False

    def ReactOnEvent(self):
        return self.IsVisible()

    def AddToEventQueue(self, event):
        self.WorkbenchObserver().EventQueue().Add(event)

    def HandleOnIdle(self):
        self.OnHandleOnIdle()
        if self.ReactOnEvent() and self.WorkbenchObserver().EventQueue():
            self.WorkbenchObserver().HandleQueuedEvents()

    #pylint: disable-msg=R0201
    def Logger(self):
        """ Return the logger to be used in panel classes. """
        return logger

    @classmethod
    def Create(cls, *args):
        return cls()

    @FEvent.InternalEventCallback
    def OnViewCreated(self, event):
        self.HandleViewCreated(event.View())

    @FEvent.InternalEventCallback
    def OnViewDestroyed(self, event):
        self.HandleViewDestroyed(event.View())


class WorkbenchObserverDummy(object):

    def __init__(self, instance):
        self._instance = instance

    def __getattr__(self, attr):

        msg = 'Calling {0} on observer dummy for {1}'.format(attr, self._instance)
        logger.debug(msg)

        def func(*args, **kwargs):
            pass

        return func
