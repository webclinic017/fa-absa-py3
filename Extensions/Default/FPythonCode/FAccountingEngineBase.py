""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineBase.py"

# operations
from FOperationsExceptions import UnSupportedObjectException

# accounting
from FAccountingEngineContracts import IAccountingEngine
from FAccountingOperations import Operation
from FAccountingReader import ReadJournalInfosReadOnly

#-------------------------------------------------------------------------
# Accounting Processing engine - used by FAccountingEOD, FAccountingRegenerateJournals and FAccountingMain
#-------------------------------------------------------------------------
class AccountingEngine(IAccountingEngine):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(AccountingEngine, self).__init__(configuration)

        self.__creatorIF = configuration.creatorIF
        self.__creatorIF.PO_Init(self)

        self.__amendmentIF = configuration.amendmentIF
        self.__amendmentIF.PO_Init(self)
        self.__processFilter = configuration.processFilter
        self.__objClass = configuration.objClass

        self.__objectModifierIF = configuration.objectModifierIF
        self.__objectModifierIF.PO_Init(self)

        self.ValidateParameters()

    #-------------------------------------------------------------------------
    def AE_IsPositionCached(self, positionKey):
        return self.__creatorIF.AOC_IsPositionCached(positionKey)

    #-------------------------------------------------------------------------
    def AE_CallObjectModifier(self, obj):
        self.__objectModifierIF.OM_ModifyObjects([obj])

    #-------------------------------------------------------------------------
    def Clear(self):
        super(AccountingEngine, self).Clear()
        self.__creatorIF.PO_Clear()
        self.__amendmentIF.PO_Clear()

    #-------------------------------------------------------------------------
    def ValidateParameters(self):
        assert self._params['startDate'] != None, 'Start Date must be set'
        assert self._params['endDate'] != None, 'End Date must be set'
        assert self._params['endOfDayDate'] != None, 'EndofDay Date must be set'
        assert self._params['processDate'] != None, 'Process Date must be set'
        assert self._params['startDate'] <= self._params['endDate'], 'Start Date must be earlier or equal to endDate'

    #-------------------------------------------------------------------------
    def ObjectClass(self):
        return self.__objClass

    #-------------------------------------------------------------------------
    def ClearCalculations(self):
        self.__creatorIF.AOC_ClearCalculations()

    #-------------------------------------------------------------------------
    def ClearProcessedPositions(self):
        self.__creatorIF.AOC_ClearProcessedPositions()
        self.__amendmentIF.AM_ClearProcessedPositions()

    #-------------------------------------------------------------------------
    def Process(self, objs):
        try:
            self.Clear()
            totalResult = self._writerIF.WR_CreateResult()

            for obj in objs:

                try:
                    self._loggerIF.LP_Log('Processing {} {}'.format(obj.ClassName(), obj.Oid()))
                    self.__ProcessObject(obj, totalResult)

                except UnSupportedObjectException as e:
                    totalResult.RE_AddFailedObject(obj.Oid())

                except Exception as e:
                    self._loggerIF.LP_Log('ERROR: An exception occurred when processing {} {}: {}'.format(obj.ClassName(), obj.Oid(), str(e)))

                self._loggerIF.LP_Flush()
                self.Clear()

            self.__ProcessCancelledPositions(totalResult)

        except Exception as e:
            self._loggerIF.LP_Log('ERROR: An exception occurred: {}'.format(str(e)))

        self._loggerIF.LP_Flush()
        self.Clear()

        return totalResult

    #-------------------------------------------------------------------------
    def __ProcessObject(self, obj, totalResult):
        if self.__processFilter.IsValidObject(obj):
            startDate, journals, journalInformations = self.__creatorIF.AOC_CreateObjects(obj)

            self.__ApplyClientModification(journals, journalInformations)

            self.__ReplaceJournalInfosWithPersisted(journals, journalInformations)

            self.__amendmentIF.AM_Amend(obj, startDate, journals)
            created, updated = self.__WriteResult(totalResult)

            self._loggerIF.LP_LogVerbose('{} journals created'.format(created))
            self._loggerIF.LP_LogVerbose('{} journals updated'.format(updated))
        else:
            self._loggerIF.LP_LogVerbose('{} {} does not match the filter and will not be processed'.format(obj.ClassName(), obj.Oid()))

    #-------------------------------------------------------------------------
    def __ApplyClientModification(self, journals, journalInformations):
        self.__objectModifierIF.OM_ModifyObjects(journals)
        self.__objectModifierIF.OM_ModifyObjects(journalInformations)

    #-------------------------------------------------------------------------
    def __ReplaceJournalInfosWithPersisted(self, journals, journalInformations):
        self.__objectModifierIF.OM_ModifyReplace(journals, 'JournalInformation', ReadJournalInfosReadOnly(journalInformations))

    #-------------------------------------------------------------------------
    def __ProcessCancelledPositions(self, totalResult):
        self.__amendmentIF.AM_AmendCancelledPositions()
        created, updated = self.__WriteResult(totalResult)

        self._loggerIF.LP_LogVerbose('{} journals created due to cancelled positions'.format(created))
        self._loggerIF.LP_LogVerbose('{} journals updated due to cancelled positions'.format(updated))

    #-------------------------------------------------------------------------
    def __WriteResult(self, totalResult):
        result = self._writerIF.WR_Commit()
        totalResult.RE_Accumulate(result)
        created = result.RE_ResultOpAndObjectType(Operation.CREATE, 'FJournal')
        updated = result.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal')
        return created, updated
