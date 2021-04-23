""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FViewCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FViewCreator

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Internal classes for creating panels.
-------------------------------------------------------------------------------------------------------"""

import acm
from FView import View
from FDispatcher import Dispatcher
from FIntegratedWorkbenchLogging import creationLogger
from FIntegratedWorkbenchUtils import ClassFactory
from FPanelCreator import CreateMainPanel, CreatePanel


def CreateView(viewName):
    creationLogger.debug("Creating view '%s'" % (viewName))
    dispatcher = Dispatcher()
    ViewClass = ClassFactory(viewName, View)
    view = ViewClass(dispatcher)
    return view

def CreatePanelsForView(view, settings):
    if view.Application().IsKindOf(acm.FUxLayoutApplicationFrame):
        CreatePanelsForCustomAppView(view, settings)
    else:
        DefaultCreatePanelsForView(view, settings)

def DefaultCreatePanelsForView(view, settings):
    creationLogger.debug("Creating panels for view '%s'" % (view.Name()))
    mainPanel = CreateMainPanel(view._app, settings.Main())
    mainPanel.SetWorkbenchObserver(view.Dispatcher())
    for panel in CreatePanels(view._app, settings.DockWindows()):
        AddPanel(view, panel)

def CreatePanelsForCustomAppView(view, settings):
    def LayoutLoaded():
        # Todo: Cleaner way to check for stored layout
        panels = settings.DockWindows()
        panels = [view.Application().GetCustomDockWindow(panel.Name()) for panel in panels]
        return any(panels)

    if LayoutLoaded():
        AddPanelsToView(view, settings)
    else:
        DefaultCreatePanelsForView(view, settings)

def AddPanelsToView(view, settings):
    creationLogger.debug("Adding panels to view '%s'" % (view.Name()))
    application = view.Application()
    mainPanel = CreateMainPanel(application, settings.Main())
    mainPanel.SetWorkbenchObserver(view.Dispatcher())
    for panel in GetCustomDockWindows(settings, application):
        AddPanel(view, panel)

def AddPanel(view, panel):
    try:
        view.AddPanel(panel)
    except Exception as error:
        creationLogger.debug("Error adding panel %s to view %s: %s", panel, view.Name(), error)

def GetCustomDockWindows(viewSettings, application):
    for panel in GetPanels(viewSettings):
        try:
            yield application.GetCustomDockWindow(panel.Name())
        except Exception as e:
            creationLogger.debug('Error trying to get DockWindow from application for view %s: %s', viewSettings.Name(), e)

def CreatePanels(app, panelsSettings):
    for panelSettings in panelsSettings:
        panel = CreatePanel(app, panelSettings)
        if panel and hasattr(panel, '__iter__'):
            for p in panel:
                yield p
        elif panel:
            yield panel

def GetPanels(settings):
    for panelSettings in settings.DockWindows():
        try:
            if panelSettings.Type() == 'TabbedPanel':
                for panel in panelSettings.DockWindows():
                    yield panel
            else:
                yield panelSettings
        except Exception as e:
            creationLogger.debug('GetPanels: Error getting panel parameter %s: %s', panelSettings, e)
