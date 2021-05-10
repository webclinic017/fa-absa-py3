""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskManagerClassic.py"

import acm

# operations
from FOperationsQueries import CreateFilter
from FOperationsTaskManager import TaskManager
from FOperationsLoggers import ProxyLogger

# accounting
from FAccountingOperations import Operation
from FAccountingEngineBaseCreator import CreateParameters

#-------------------------------------------------------------------------
# AccountingTaskManagerClassic
#-------------------------------------------------------------------------
class AccountingTaskManagerClassic(TaskManager):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(AccountingTaskManagerClassic, self).__init__()

        self._name = configuration.name
        self._objectClass = configuration.objectClass
        self._createEngineCb = configuration.createEngineCb
        self._engineParams = configuration.parameters

        # Result
        self._resultCls = configuration.resultCls
        self._result = self._resultCls()

        self._engine = self.PrivateCreateEngine(self.PrivateCreateParameters())

        self._finished = True

    #-------------------------------------------------------------------------
    def TM_Name(self):
        return self._name

    #-------------------------------------------------------------------------
    def TM_ObjectClass(self):
        return self._objectClass

    #-------------------------------------------------------------------------
    def TM_Destroy(self):
        self.OO_RemoveObservers()
        self._engine = None

    #-------------------------------------------------------------------------
    def TM_Run(self, objects):
        self.PrivateRunTask(objects)

    #-------------------------------------------------------------------------
    # OperationsTaskManager:Events interface calls
    #-------------------------------------------------------------------------
    def OnOutput(self, msg):
        self.OO_NotifyObservers('TME_OnOutput', self.TM_Name(), msg)

    #-------------------------------------------------------------------------
    def OnFinished(self):
        self.OO_NotifyObservers('TME_OnFinished', self.TM_Name(), self._result)

    #-------------------------------------------------------------------------
    def PrivateCreateParameters(self):
        from FAccountingParams import detailedLogging

        startDate = self._engineParams['startDate']
        endDate = self._engineParams['endDate']
        endOfDayDate = self._engineParams['endOfDayDate']
        processDate = self._engineParams['processDate']
        booksOids = [book.Oid() for book in self._engineParams['bookIds']]
        treatmentOids = [treatment.Oid() for treatment in self._engineParams['treatmentIds']]
        aiOids = [ai.Oid() for ai in self._engineParams['aiIds']]

        bookFilter = None
        if len(booksOids):
            bookFilter = CreateFilter(acm.FBook, 'OR', 'Oid', booksOids, 'EQUAL')

        bookLinkFilter = None
        if len(treatmentOids):
            bookLinkFilter = CreateFilter(acm.FBookLink, 'OR', 'Treatment.Oid', treatmentOids, 'EQUAL')

        treatmentLinkFilter = None
        if len(aiOids):
            treatmentLinkFilter = CreateFilter(acm.FTreatmentLink, 'OR', 'AccountingInstruction.Oid', aiOids, 'EQUAL')

        params = CreateParameters(startDate, endDate, endOfDayDate, processDate, bookFilter, bookLinkFilter, treatmentLinkFilter)
        logger = ProxyLogger(detailedLogging, self.OnOutput)

        return {'params' : params, 'logger' : logger}

    #-------------------------------------------------------------------------
    def PrivateCreateEngine(self, args):
        return self._createEngineCb(args.get('params'), args.get('logger'), args.get('committerIF'), args.get('isSupportedObjectCb'))

    #-------------------------------------------------------------------------
    def PrivateRunTask(self, objects):
        self._finished = False

        result = self._engine.Process(objects)

        self._result.ATMRC_AddCreated(result.RE_ResultOpAndObjectType(Operation.CREATE, 'FJournal'))
        self._result.ATMRC_AddUpdated(result.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal'))

        self._result.ATMRC_AddExceptions(len(result.RE_Exceptions()))
        self._result.ATMRC_AddFailedObjects(result.RE_FailedObjects())

        self._finished = True

        self.OnFinished()

    #-------------------------------------------------------------------------
    def IsFinished(self):
        return self._finished
