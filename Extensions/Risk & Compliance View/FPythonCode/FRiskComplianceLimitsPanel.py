""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceLimitsPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComlianceLimitsPanel

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FSheetUtils
from itertools import chain
from FSheetPanel import SheetPanel
from FEvent import EventCallback
from FRiskComplianceLogging import logger
from FTradeProgram import LinkedTrades

class RiskComplianceLimitsPanel(SheetPanel):

    COLUMNS = ('Limit Checked Value', 'Limit Current State')

    @EventCallback
    def OnBusinessProcessSelected(self, event):
        try:
            bp = event.BusinessProcess()
            trades = LinkedTrades(bp.Subject())
            limits = self.RelevantLimits(trades)
            limitsFolders = FSheetUtils.GetObjectsAsFolder(limits, 'Affected Limits')
            self.Sheet().InsertObject(limitsFolders)
            self.Sheet().ExpandTree(3)
        except IndexError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)
        except AttributeError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)

    @staticmethod
    def RelevantLimits(trades):
        affectedLimits = [acm.Limits.FindByTrade(trade) for trade in trades]
        return list(chain.from_iterable(affectedLimits))