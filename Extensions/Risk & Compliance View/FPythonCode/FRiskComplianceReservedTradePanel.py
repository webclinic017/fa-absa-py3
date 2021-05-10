""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceReservedTradePanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceReservedTradePanel

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FSheetPanel import SheetPanel
from FRiskComplianceLogging import logger
from FTradeProgram import LinkedTrades
import FEvent

class RiskComplianceReservedTradePanel(SheetPanel):

    @FEvent.EventCallback
    def OnBusinessProcessSelected(self, event):
        try:
            trades = LinkedTrades(event.BusinessProcess().Subject())
            self.Sheet().InsertObject(trades)
        except IndexError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)
        except AttributeError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)