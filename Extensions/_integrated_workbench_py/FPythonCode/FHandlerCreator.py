""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FHandlerCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWorkbenchCreator

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Internal classes for creating handlers and panels.
-------------------------------------------------------------------------------------------------------"""

from FIntegratedWorkbenchLogging import creationLogger
import FPanelCreator

def CreateHandlers(settingsList, dispatcher):
    for settings in settingsList:
        CreateHandler(settings, dispatcher)

def CreateHandler(settings, dispatcher):
    HandlerCreator(settings).CreateHandler(dispatcher)

class HandlerCreator(FPanelCreator.Creator):

    def __init__(self, settings):
        super(HandlerCreator, self).__init__(settings)

    def CreateHandler(self, dispatcher):
        try:
            creationLogger.debug("Creating handler: %s from module: %s" %
                         (self.Settings().Name(), self.Settings().Module()))
            return self.CreateFunction()(dispatcher)
        except StandardError as exc:
            creationLogger.error("Unable to create handler '%s': %s" % (self.Settings().Name(), exc))
