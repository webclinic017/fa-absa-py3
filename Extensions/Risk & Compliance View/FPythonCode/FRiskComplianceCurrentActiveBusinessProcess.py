""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceCurrentActiveBusinessProcess.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceCurrentActiveBusinessProcess

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION


-----------------------------------------------------------------------------"""

import acm
from FHandler import Handler
from FEvent import EventCallback
from FRiskComplianceLogging import logger

class RiskComplianceCurrentActiveBusinessProcess(Handler):

    def __init__(self, dispatcher):
        super(RiskComplianceCurrentActiveBusinessProcess, self).__init__(dispatcher)
        self._businessProcess = None
        self._businessProcesses = None

    def BusinessProcess(self):
        return self._businessProcess

    def BusinessProcesses(self):
        return self._businessProcesses

    @EventCallback
    def OnBusinessProcessChanged(self, event):
        try:
            self._UpdateBusinessProcesses(event.BusinessProcesses())
            event = self.CreateEvent('OnBusinessProcessSelected',
                                      businessProcess = self._businessProcess)
            self.SendEvent(event)
        except AttributeError as e:
            logger.debug('Error in OnBusinessProcessChanged: {0}'.format(e))

    def _UpdateBusinessProcesses(self, bpCollection):
        self._businessProcesses = bpCollection
        if self._businessProcesses.Size() == 1:
            self._businessProcess = self._businessProcesses.First()
        else:
            self._businessProcess = None
