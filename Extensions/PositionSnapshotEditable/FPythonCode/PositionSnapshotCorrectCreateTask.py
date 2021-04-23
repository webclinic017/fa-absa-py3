
import acm
import CreateValueSessionTraits
import uuid
import FPaceConsumer
import time
import PositionApplicationCore

def GenerateAndAddDates(definition, taskDefinition):
    if definition.At(acm.FSymbol('calendar')):
        calendar = definition.At(acm.FSymbol('calendar'))
    else:
        calendar = acm.UsedValuationParameters().AccountingCurrency().Calendar()
    startDate = definition.At(acm.FSymbol('fromDate'))
    if definition.At(acm.FSymbol('toDate')):
        endDate = definition.At(acm.FSymbol('toDate'))
    else:
        endDate = acm.Time.DateToday()
    dateDiff = acm.Time.DateDifference(endDate, startDate)
    i = 0
    while i <= dateDiff:
        tempDate = acm.Time.DateAddDelta(startDate, 0, 0, i)
        if not calendar.IsNonBankingDay(None, None, tempDate):
            parameters = taskDefinition.parameters.add()
            parameters.historicalDate = tempDate
        i = i + 1

class TaskListener( PositionApplicationCore.TaskListenerBase, object):
    def PrivateCreateTaskFromDefinition(self, definition):
        taskDefinition = CreateValueSessionTraits.Definition()

        disposition = definition.At(acm.FSymbol("disposition") )
        taskDefinition.dataDispositionStorageId = disposition.Oid()
        taskDefinition.sessionType = definition.At(acm.FSymbol("sessionType") )
        taskDefinition.uniqueId = str(uuid.uuid4())
        if definition.At(acm.FSymbol("calculationEnvironment") ):
            taskDefinition.channelKey = definition.At(acm.FSymbol("calculationEnvironment") )
        if definition.At(acm.FSymbol("valueSession") ):
            valueSession = definition.At(acm.FSymbol("valueSession") )
            taskDefinition.amendSessionStorageId = valueSession.Oid()
        if definition.At(acm.FSymbol("positionFilter") ):
            taskDefinition.positionFilterName = definition.At(acm.FSymbol("positionFilter") ).Name()
        if definition.At(acm.FSymbol("storeHistory") ):
            taskDefinition.createAudit = True
        if definition.At(acm.FSymbol("correctionComment") ):
            taskDefinition.description = definition.At(acm.FSymbol("correctionComment") )
        if definition.At(acm.FSymbol('fromDate')):
            GenerateAndAddDates(definition, taskDefinition)
        else:
            taskDefinition.parameters.add()

        return FPaceConsumer.Create('FrontArena.HierarchicalGrid.PositionSheet.CreateValueSession', taskDefinition)

    def PrivateOnResultUpdated(self, resultKey, resultEvent, result):
        if result.HasField('errorText'):
            errorStr =  'Encountered error when processing item'
            if result.HasField('historicalDate'):
                errorStr = errorStr + ' with historical date %s' % result.historicalDate
            errorStr = errorStr + ': %s' % result.errorText
            self.m_encounteredErrors = self.m_encounteredErrors + 1
            print( errorStr )
        else:
            returnStr = 'Created %i records for value session with id %i' % ( result.createdRecords, (result.amendedSessionId if result.HasField('amendedSessionId')  else result.sessionStorageId))
            if result.HasField('historicalDate'):
                returnStr = returnStr + ' and historical date %s' % result.historicalDate
            if result.movedRecords:
                returnStr = returnStr + ' and moved %i records to audit session %i' % (result.movedRecords, result.sessionStorageId)
            returnStr = returnStr + '.'
            print( returnStr)

    def PrivateOnInitialPopulateDone(self):
        self.m_statusMessage = None
        if self.m_encounteredErrors:
            self.m_statusMessage = 'Task done, encountered errors for %i Snapshots. See output for details.' % self.m_encounteredErrors


def CreateActivity(definition):
    activity = TaskListener.CreateActivity(definition)
    return activity
