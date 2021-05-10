""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceMainPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceMainPanel

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FWorkbookPanel import WorkbookPanel
from FRiskComplianceLogging import logger
import FEvent
import acm

class RiskComplianceMainPanel(WorkbookPanel):

    def RowSelectionChanged(self, selection):
        try:
            businessProcesses = self._BusinessProcesses(selection)
            event = FEvent.CreateEvent('OnBusinessProcessChanged',
                                        FEvent.BaseEvent,
                                        self,
                                        businessProcesses=businessProcesses)
            self.SendEvent(event)
        except IndexError as e:
            pass

    def _BusinessProcesses(self, selection):
        businessProcesses = acm.FArray()
        rowObjects = selection.SelectedRowObjects()
        if rowObjects and rowObjects[0].IsKindOf(acm.FBusinessProcess):
            businessProcesses = rowObjects
        return businessProcesses
