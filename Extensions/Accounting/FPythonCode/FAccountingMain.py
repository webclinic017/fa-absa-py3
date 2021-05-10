""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingMain.py"

# core
import acm, time

# operations
from FOperationsTradesFromInstrument import GetTrades
from FOperationsLoggers import ConsoleLogger
from FOperationsExceptions import UpdateCollisionException

import FOperationsATSRoutines as ATSRoutines

# accounting
from FAccountingQueries import CreateAIFilterTriggerType
import FAccountingEngineBaseCreator as Engines

import FAccountingParams as Params #  No fallback, should always be user defined


#-------------------------------------------------------------------------
dbTables = ['TRADE', 'INSTRUMENT', 'SETTLEMENT']

#-------------------------------------------------------------------------
class FAccountingATSEngine(ATSRoutines.FOperationsATSEngine):

    #-------------------------------------------------------------------------
    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    #-------------------------------------------------------------------------
    def Start(self):
        mappingFilter = CreateAIFilterTriggerType(Params.realTimeAmendmentTriggerTypes)
        parameters = Engines.CreateParameters(treatmentLinkFilter=mappingFilter)

        loggerTrades = ConsoleLogger(Params.detailedLogging)
        loggerSettlements = ConsoleLogger(Params.detailedLogging)

        self.__settlementEngine = Engines.CreateEngineForSettlements(parameters, loggerSettlements)
        self.__tradeEngine = Engines.CreateEngineForTrades(parameters, loggerTrades)

    #-------------------------------------------------------------------------
    def Work(self, msg, obj):
        if obj.IsKindOf(acm.FSettlement):

            result = self.__settlementEngine.Process([obj])
            self.__settlementEngine.ClearCalculations()
            self.__settlementEngine.ClearProcessedPositions()
        else:

            result = self.__tradeEngine.Process(GetTrades(obj))
            self.__tradeEngine.ClearCalculations()
            self.__tradeEngine.ClearProcessedPositions()

        exceptions = result.RE_Exceptions()

        # Send UpdateCollision further up the call chain
        for exception in exceptions:
            if isinstance(exception, UpdateCollisionException):
                raise exception

    #-------------------------------------------------------------------------
    def Stop(self):
        statusMessage = 'Stop called at %s' % (time.ctime())
        acm.Log(statusMessage)
        return

    #-------------------------------------------------------------------------
    def Status(self):
        return "Accounting ATS status"

#-------------------------------------------------------------------------
accountingEngine = FAccountingATSEngine('Accounting', dbTables, Params, 'FAccountingParamsTemplate')
atsRoutines = ATSRoutines.FOperationsATSRoutines(accountingEngine)

#-------------------------------------------------------------------------
def start():
    atsRoutines.Start()

#-------------------------------------------------------------------------
def work():
    atsRoutines.Work()

#-------------------------------------------------------------------------
def stop():
    atsRoutines.Stop()

#-------------------------------------------------------------------------
def status():
    return atsRoutines.Status()
