""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramUtils

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Trade creators and quantity calculator and convenience methods
-----------------------------------------------------------------------------"""

#pylint: disable-msg=W0603

import FLogger
from FParameterSettings import ParameterSettingsCreator
from FTradeCreator import TradeFromRowCreator
from FWorkflowMenuItem import WorkflowMenuItem

LOGGER = None
SETTINGS = None

def TradeProgramSettings():
    global SETTINGS
    if SETTINGS is None:
        SETTINGS = ParameterSettingsCreator.FromRootParameter('TradeProgramSettings')
    return SETTINGS


def Logger():
    global LOGGER
    if LOGGER is None:
        LEVELS = {'info': 1, 'debug': 2, 'error': 3}
        logLevel = TradeProgramSettings().Log()
        level = logLevel.lower() if logLevel else 'info'
        LOGGER = FLogger.FLogger.GetLogger(name='Portfolio Trading')
        LOGGER.Reinitialize(
            level=LEVELS.get(level),
            logToConsole=1)
    return LOGGER

class CandidateTradeCreator(TradeFromRowCreator):

    PRICE_COLUMN_ID = TradeProgramSettings().Price()

    def __init__(self, templateRow, instrument=None):
        super(CandidateTradeCreator, self).__init__(templateRow, instrument)
        self.inputDict['Status'] = TradeProgramSettings().CandidateTradeStatus()


def TradeProgramAction(businessProcess):
    try:
        dealPackage = businessProcess.Subject()
        return dealPackage.Definition().DisplayName()
    except Exception:
        return None


class ColumnWorkflowMenuItem(WorkflowMenuItem):
    
    def __init__(self, extObj, workflow, event, businessProcess):
        super(ColumnWorkflowMenuItem, self).__init__(extObj, workflow, event)
        self._businessProcess = businessProcess
    
    def BusinessProcess(self):
        return self._businessProcess