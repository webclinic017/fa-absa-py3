""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceRulePanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceRulePanel

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
from itertools import chain

import acm
import FSheetUtils
import FComplianceRulesUtils
from FSheetPanel import SheetPanel
from FEvent import EventCallback
from FRiskComplianceLogging import logger
from FTradeProgram import LinkedTrades

class RiskComplianceRulePanel(SheetPanel):

    @EventCallback
    def OnBusinessProcessSelected(self, event):
        try:
            bp = event.BusinessProcess()
            trades = LinkedTrades(bp.Subject())
            rules = self.RelevantRules(trades)
            rulesFolder = FSheetUtils.GetObjectsAsFolder(rules, 'Affected Rules')
            self.Sheet().InsertObject(rulesFolder)
            self.Sheet().ExpandTree(3)
        except IndexError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)
        except AttributeError as e:
            logger.debug(e)
            self.Sheet().InsertObject(None)

    @staticmethod
    def RelevantRules(trades):
        portfolios = FComplianceRulesUtils.AllPortfoliosForTrades(trades)
        appliedRules = chain.from_iterable(FComplianceRulesUtils.AppliedRules(portfolio) for portfolio in portfolios)
        return list({appliedRule.ComplianceRule() for appliedRule in appliedRules})
