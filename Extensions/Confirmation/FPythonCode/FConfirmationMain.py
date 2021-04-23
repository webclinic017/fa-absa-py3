""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationMain.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FConfirmationMain - Module that is executed by the confirmation ATS.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import time
try:
    import FOperationsUtils as Utils
except ImportError as error:
    print('Failed to import FOperationsUtils, ' + str(error))
    raise ImportError(error)
try:
    import FOperationsATSRoutines as ATSRoutines
except ImportError as error:
    Utils.LogAlways("Failed to import FOperationsATSRoutines, "  + str(error))
    raise ImportError(error)
try:
    import FConfirmationParameters as ConfirmationParameters
except ImportError as error:
    Utils.LogAlways("Failed to import FConfirmationParameters, "  + str(error))
    raise ImportError(error)
try:
    from FConfirmationSingletons import GetSingleton, EventChoiceListItemHandler, ConfirmationPreventionRulesHandler
except ImportError as error:
    Utils.LogAlways("Failed to import FConfirmationSingletons, "  + str(error))
    raise ImportError(error)
try:
    from FConfirmationHookAdministrator import GetConfirmationHookAdministrator
except ImportError as error:
    Utils.LogAlways("Failed to import FConfirmationHookAdministrator, "  + str(error))
    raise ImportError(error)
try:
    import FConfirmationProcess
except ImportError as error:
    Utils.LogAlways("Failed to import FConfirmationProcess, "  + str(error))
    raise ImportError(error)
try:
    import FOperationsAMBAMessage
except ImportError as error:
    Utils.LogAlways("Failed to import FOperationsAMBAMessage, "  + str(error))
    raise ImportError(error)
try:
    from FConfirmationExceptions import ConfirmationClientValidationException
except ImportError as error:
    Utils.LogAlways("Failed to import FConfirmationExceptions, "  + str(error))
    raise ImportError(error)


dbTables = ['TRADE', 'OPERATIONSDOCUMENT', 'INSTRUMENT', 'PARTY', 'DEALPACKAGE']


class FOperationsConfirmationEngine(ATSRoutines.FOperationsATSEngine):

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    def Start(self):
        try:
            self.__ValidateConfirmationClientValidation()
        except ConfirmationClientValidationException as error:
            Utils.LogAlways(str(error))
            Utils.LogAlways('Confirmation ATS will be shut down...')
            raise SystemExit()
        GetSingleton(ConfirmationPreventionRulesHandler)
        GetSingleton(EventChoiceListItemHandler)
        GetConfirmationHookAdministrator().PrintRegisteredCustomHooks()

    def Work(self, msg, obj):
        FConfirmationProcess.ConfirmationProcess(msg, obj)

    def Stop(self):
        statusMessage = 'Stop called at %s' % (time.ctime())
        Utils.LogAlways(statusMessage)
        return

    def Status(self):
        return "Confirmation ATS status"

    def IsCreateObjectFromAMBAMessage(self, msg):
        ambaMessage = FOperationsAMBAMessage.AMBAMessage(msg)
        if ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT' or ambaMessage.GetNameOfUpdatedTable() == 'PARTY':
            return False
        return True
    
    def __ValidateConfirmationClientValidation(self):
        import inspect
        clientValidationTemplate = __import__('FConfirmationClientValidationTemplate')
        try:
            clientValidation = __import__('FConfirmationClientValidation')
            for attribute in dir(clientValidationTemplate):
                if inspect.isfunction(clientValidationTemplate.__dict__[attribute]):
                    if (True == (attribute in clientValidation.__dict__)):
                        if (False == inspect.isfunction(clientValidation.__dict__[attribute])):
                            msg = 'Incorrect attribute type for attribute %s in FConfirmationClientValidation. Should be a function' % attribute
                            raise ConfirmationClientValidationException(msg)
                    else:
                        msg = 'FConfirmationClientValidation misses function implementation %s' % attribute
                        raise ConfirmationClientValidationException(msg)
        except ImportError:
            pass


confirmationEngine = FOperationsConfirmationEngine('Confirmation', dbTables, ConfirmationParameters, 'FConfirmationParametersTemplate')
aTSRoutines = ATSRoutines.FOperationsATSRoutines(confirmationEngine)

#ATS entry points
def start():
    aTSRoutines.Start()

def work():
    aTSRoutines.Work()

def stop():
    aTSRoutines.Stop()

def status():
    return aTSRoutines.Status()

