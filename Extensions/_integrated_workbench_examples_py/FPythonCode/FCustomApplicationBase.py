""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FCustomApplicationBase.py"
"""--------------------------------------------------------------------------
MODULE
    FCustomApplicationBase

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Example of baseclass if you want to use a layout application as
    the application for your view. Communication with other panels goes into
    the MainPanel layer.Communicate with MainPanel using SendUpdate.
-----------------------------------------------------------------------------"""
from FUxCore import LayoutApplication
from FIntegratedWorkbenchLogging import logger

class CustomApplicationBase(LayoutApplication):

    def __init__(self):
        LayoutApplication.__init__(self)
        self._dependents = set()

    def AddDependent(self, dependent):
        self._dependents.add(dependent)

    def RemoveDependent(self, dependent):
        try:
            self._dependents.remove(dependent)
        except KeyError:
            pass

    def SendUpdate(self, update):
        message = 'Custom Application: Error trying to call ServerUpdate on dependent {0}: {1}'
        for dependent in self._dependents:
            try:
                dependent.ServerUpdate(update)
            except AttributeError as error:
                logger.debug(message.format(dependent, error))
