""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCurrentActiveObjects.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveObjects

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

from FHandler import Handler
from FIntegratedWorkbenchUtils import IsKindOf
from FIntegratedWorkbenchLogging import logger
from FEvent import EventCallback

class CurrentActiveObjects(Handler):

    def __init__(self, dispatcher):
        super(CurrentActiveObjects, self).__init__(dispatcher)
        self._objMap = dict()

    def Object(self, key):
        return self._objMap[key] if key in self._objMap else None

    @EventCallback
    def OnObjectsSelected(self, event):
        try:
            for obj in event.Objects():
                logger.debug("CurrentActiveObjects.OnObjectSelected() Selection "
                    "is FObject: %s obj: %s" % (IsKindOf(obj, acm.FObject), (obj != None)))
                if (obj != None) and IsKindOf(obj, acm.FObject):
                    key = None
                    if IsKindOf(obj, acm.FInstrument):
                        key = 'Instrument'
                    elif IsKindOf(obj, acm.FCounterParty):
                        key = 'Party'
                    if key:
                        self._objMap[key] = obj
                    logger.debug("CurrentActiveObjects.OnObjectSelected() Key: %s "
                                 "Type: %s" % (key, str(obj.Class())))
        except Exception as stderr:
            logger.error("CurrentActiveObjects.OnObjectSelected() Exception: %s" % (stderr))
            logger.error(stderr, exc_info=True)
