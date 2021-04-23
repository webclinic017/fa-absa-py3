""" Compiled: 2014-12-11 14:12:15 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementMain - Module that is executed by the settlement ATS.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

HISTORY
=================================================================================================================================
Date            Change no       Developer              Requester         Description
=================================================================================================================================

2016-02-02      ABITFA-3918     Lawrence Mucheka       OPS               Core Settlement ATS split
----------------------------------------------------------------------------"""
import time

try:
    import FOperationsUtils as Utils
except Exception, error:
    print "Failed to import FOperationsUtils, "  + str(error)
    raise Exception(error)
try:
    import FOperationsATSRoutines as ATSRoutines
except Exception, error:
    Utils.LogAlways("Failed to import FOperationsATSRoutines, "  + str(error))
    raise Exception(error)
try:
    from FSettlementUtils import Params as SettlementParameters
except Exception, error:
    Utils.LogAlways("Failed to import FSettlementUtils, "  + str(error))
    raise Exception(error)
try:
    import FSettlementProcess
except Exception, error:
    Utils.LogAlways("Failed to import FSettlementProcess, "  + str(error))
    raise Exception(error)
try:
    import FSettlementHookAdministrator as HookAdmin
except Exception, error:
    Utils.LogAlways("Failed to import FSettlementHookAdministrator, "  + str(error))
    raise Exception(error)
try:
    import FOperationsAMBAMessage
except Exception, error:
    Utils.LogAlways("Failed to import FOperationsAMBAMessage, "  + str(error))
    raise Exception(error)



dbTables = ['OPERATIONSDOCUMENT']
try:
    if SettlementParameters.confirmationEventHandling == True:
        dbTables.append('CONFIRMATION')
except Exception, e:
    pass

class FOperationsSettlementEngine(ATSRoutines.FOperationsATSEngine):

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    def Start(self):
        HookAdmin.GetHookAdministrator().PrintRegisteredCustomHooks()

    def Work(self, msg, obj):
        FSettlementProcess.SettlementProcess(msg, obj)

    def Stop(self):
        statusMessage = 'Stop called at %s' % (time.ctime())
        Utils.LogAlways(statusMessage)
        return


    def Status(self):
        return "Settlement ATS status"

    def IsCreateObjectFromAMBAMessage(self, msg):
        ambaMessage = FOperationsAMBAMessage.AMBAMessage(msg)
        if ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT' or ambaMessage.GetNameOfUpdatedTable() == 'PARTY':
            return False
        return True


settlementEngine = FOperationsSettlementEngine('Settlement', dbTables, SettlementParameters, 'FSettlementParametersTemplate')
aTSRoutines = ATSRoutines.FOperationsATSRoutines(settlementEngine)


#ATS entry points
def start():
    aTSRoutines.Start()

def work():
    aTSRoutines.Work()

def stop():
    aTSRoutines.Stop()

def status():
    return aTSRoutines.Status()

