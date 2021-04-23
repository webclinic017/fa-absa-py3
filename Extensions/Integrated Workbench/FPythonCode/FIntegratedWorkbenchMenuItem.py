""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbench/./etc/FIntegratedWorkbenchMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIntegratedWorkbenchMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FUxCore
from FIntegratedWorkbench import GetView, GetHandlerByName
from FIntegratedWorkbenchLogging import logger

class IntegratedWorkbenchMenuItem(FUxCore.MenuItem, object):

    def __init__(self, frame, view):
        self._frame = frame
        self._view = view

    def Invoke(self, _eii):
        self.InvokeAsynch(_eii)

    def InvokeAsynch(self, _eii):
        raise NotImplementedError()

    def Applicable(self):
        return True

    def EnabledFunction(self):
        """
            Override EnabledFunction to extend Enabled-check
        """
        return True

    def Enabled(self):
        try:
            if self.View():
                if self._view is None or self.View().Name() == self._view:
                    return self.EnabledFunction()
        except Exception as err:
            logger.debug('Class %s', str(self.__class__))
            logger.debug('error in EnabledFunction: {0}'.format(err))
        return False

    def View(self):
        return GetView(self._frame)

    def _Handler(self, handlerName):
        return GetHandlerByName(self.View(), handlerName)

    def _Panel(self, panelName):
        try:
            return self.View().Panel(panelName)
        except Exception:
            pass

    def _Dispatcher(self):
        return self.View().Dispatcher()
