""" Compiled: 2019-05-28 12:54:12 """

#__src_file__ = "extensions/settlement/etc/FSettlementMain.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementMain - Module that is executed by the settlement ATS.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
# core
import time
import traceback
import sys

# operations
import FOperationsATSRoutines as ATSRoutines
import FOperationsAMBAMessage
from FOperationsLoggers import ConsoleLogger

# settlements
import FSettlementParameters as SettlementParameters
import FSettlementHookAdministrator as HookAdmin
from FSettlementProcessEngineCreator import CreateSettlementProcessEngine

#-------------------------------------------------------------------------
dbTables = ['TRADE', 'INSTRUMENT', 'PARTY', 'OPERATIONSDOCUMENT', 'BUSINESSEVENT']
try:
    if SettlementParameters.confirmationEventHandling == True:
        dbTables.append('CONFIRMATION')
except Exception as error:
    Utils.LogAlways("Exception Error: %s" % error)
    traceback.print_exc(file=sys.stdout)

#-------------------------------------------------------------------------
class FOperationsSettlementEngine(ATSRoutines.FOperationsATSEngine):

    #-------------------------------------------------------------------------
    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)
        self.__logger = ConsoleLogger(paramsModule.detailedLogging)
        self.__settlementEngine = CreateSettlementProcessEngine(self.__logger)

    #-------------------------------------------------------------------------
    def Start(self):
        HookAdmin.GetHookAdministrator().PrintRegisteredCustomHooks()

    #-------------------------------------------------------------------------
    def Work(self, msg, obj):
        self.__settlementEngine.Process(msg, obj)

    #-------------------------------------------------------------------------
    def Stop(self):
        statusMessage = 'Stop called at %s' % (time.ctime())
        self.__logger.LP_Logg(statusMessage)
        return

    #-------------------------------------------------------------------------
    def Status(self):
        return "Settlement ATS status"

    #-------------------------------------------------------------------------
    def IsCreateObjectFromAMBAMessage(self, msg):
        ambaMessage = FOperationsAMBAMessage.AMBAMessage(msg)
        if ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT' or ambaMessage.GetNameOfUpdatedTable() == 'PARTY':
            return False
        return True


#-------------------------------------------------------------------------
settlementEngine = FOperationsSettlementEngine('Settlement', dbTables, SettlementParameters, 'FSettlementParametersTemplate')
aTSRoutines = ATSRoutines.FOperationsATSRoutines(settlementEngine)


#ATS entry points
#-------------------------------------------------------------------------
def start():
    aTSRoutines.Start()

#-------------------------------------------------------------------------
def work():
    aTSRoutines.Work()

#-------------------------------------------------------------------------
def stop():
    aTSRoutines.Stop()

#-------------------------------------------------------------------------
def status():
    return aTSRoutines.Status()
