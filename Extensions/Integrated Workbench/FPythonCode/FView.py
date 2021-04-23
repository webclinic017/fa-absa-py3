""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FView.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FView

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
   Base class of all views.
-------------------------------------------------------------------------------------------------------"""

__all__ = ['View']

import acm
import FEvent

from FIntegratedWorkbenchLogging import logger
from FWorkbenchObserver import WorkbenchObserver
from FACMObserver import ApplicationObserver

class View(object):

    def __init__(self, dispatcher):
        self._workbenchObserver = WorkbenchObserver(dispatcher, self)
        self._app = None
        self._panels = dict()
        self._applicationObserver = None
        self.SendEvent(self.CreateEvent('OnViewInitialized', view=self))
        logger.debug("View '%s' created" % (self.ClassName()))

    def ApplicationObserver(self):
        if self._applicationObserver is None:
            self._applicationObserver = ApplicationObserver(self)
        return self._applicationObserver

    def RegisterPanel(self, panel):
        if panel.Name() not in self._panels:
            self._panels[panel.Name()] = panel

    def Activate(self):
        self.Application().Restore()
        self.Application().Activate()

    def Panel(self, panelName):
        try:
            return self._panels[panelName]
        except Exception:
            logger.debug("View.Panel() Unable to get Panel: %s", panelName)

    def Panels(self):
        return self._panels

    def Dispatcher(self):
        return self._workbenchObserver.Dispatcher()

    def SendEvent(self, event):
        self._workbenchObserver.SendEvent(event)

    def CreateEvent(self, name, *args, **kwargs):
        return self._workbenchObserver.CreateEvent(name, *args, **kwargs)

    def ClassName(self):
        return self.__class__.__name__

    def Name(self):
        # Left for backwards compability
        return self.ClassName()

    def StopObserving(self, dispatcher=None):
        self._workbenchObserver.StopObserving(dispatcher)

    def AddPanel(self, panel):
        panel.CustomLayoutPanel().SetWorkbenchObserver(self.Dispatcher())

    def Application(self, application=None):
        if application is None:
            return self._app
        self._app = application
        self.InitApplicationObserver()

    def InitApplicationObserver(self):
        """ This should be done on init once app is
        passed to construction """
        self._app.AddDependent(self.ApplicationObserver())
        self.SendEvent(self.CreateEvent('OnViewCreated', view=self))

    @FEvent.InternalEventCallback
    def OnPanelInitialized(self, event):
        self.RegisterPanel(event.Sender())

    @FEvent.InternalEventCallback
    def OnPanelDestroyed(self, event):
        try:
            del self._panels[event.Sender().Name()]
        except KeyError:
            pass

    @FEvent.InternalEventCallback
    def OnError(self, event):
        shell = self.Application().Shell()
        if event.MsgBoxType() == 'Information':
            acm.UX().Dialogs().MessageBoxInformation(shell, event.Msg())

    @FEvent.InternalEventCallback
    def OnPanelVisibilityChanged(self, event):
        try:
            panelName = event.PanelName()
            newVisibility = event.Visible()
            if newVisibility is None:
                newVisibility = not self._app.IsDockWindowVisible(panelName)
            self._app.ShowDockWindow(panelName, newVisibility)
        except RuntimeError as stderr:
            logger.debug("Exception for panel '%s':" % (panelName))
            logger.debug(stderr, exc_info=True)
        except Exception as stderr:
            logger.error("Exception for panel '%s':" % (panelName))
            logger.error(stderr, exc_info=True)

    def HandleDestroy(self):
        self._app.RemoveDependent(self.ApplicationObserver())
        self.SendEvent(self.CreateEvent('OnViewDestroyed', view=self))
        self.StopObserving()
