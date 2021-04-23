""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FIntegratedWorkbench.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIntegratedWorkbench

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import ViewLauncher
from FIntegratedWorkbenchLogging import logger
from FView import View
from FACMObserver import ApplicationObserver

def LaunchView(viewName):
    try:
        return ViewLauncher.Launch(viewName)
    except AttributeError as error:
        logger.error(error)

def GetView(frame):
    """ Get the view wrapping a frame """
    for dependent in frame.Dependents():
        if isinstance(dependent, ApplicationObserver) and isinstance(dependent.Parent(), View):
            return dependent.Parent()


def GetHandler(view, handlerClass):
    try:
        for observer in view.Dispatcher().Observers():
            if isinstance(observer, handlerClass):
                return observer
    except Exception:
        pass

def GetHandlerByName(view, handlerClassName):
    try:
        for observer in view.Dispatcher().Observers():
            if type(observer).__name__ == handlerClassName:
                return observer
    except Exception:
        pass
