""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/ViewLauncher.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ViewLauncher

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
from FViewUtils import ViewSettings
import FViewCreator
import FHandlerCreator
import FApplicationCreator


def Launch(viewName):
    settings = ViewSettings(viewName)
    view = FViewCreator.CreateView(viewName)
    application =  FApplicationCreator.DoStartApplication(settings)
    view.Application(application)
    FViewCreator.CreatePanelsForView(view, settings)
    if hasattr(settings, 'Handlers'):
        FHandlerCreator.CreateHandlers(settings.Handlers(), view.Dispatcher())
    return application

def LaunchViewFromExistingApplication(viewName, application):
    settings = ViewSettings(viewName)
    view = FViewCreator.CreateView(viewName)
    view.Application(application)
    FViewCreator.AddPanelsToView(view, settings)
    if hasattr(settings, 'Handlers'):
        FHandlerCreator.CreateHandlers(settings.Handlers(), view.Dispatcher())
