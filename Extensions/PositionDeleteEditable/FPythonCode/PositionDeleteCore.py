
import acm
import PositionDeleteTraits
import FPaceConsumer
import FPaceCoreTypes
import time
import PaceVariantTools
import PositionApplicationCore

type_tt = "The type of value session for which position calculations should be deleted."
disposition_tt = "The data disposition for which position calculations should be deleted."
from_tt = "The beginning of the date time range for which positions calculations should be deleted."
to_tt = "The end of the date time range for which position calculations should be deleted."
    
def DateTimeStrAsDouble(dateTimeStr):
    return acm.Time.NumberOfUtcDays(dateTimeStr)

def BuildAndAddSessionFilterToDefinition(messageDefinition, sessiontType, dateFrom, dateTo, dataDisposition):
    if sessiontType:
        typeFilter = messageDefinition.sessionFilter.descendents.add()
        AddFilterPartCompare( typeFilter, "type_seqnbr", [PaceVariantTools.VariantFromInt64(sessiontType.Oid())] )

    if dateFrom or dateTo:
        timeFilter = messageDefinition.sessionFilter.descendents.add()
        AddFilterPartRange(timeFilter, "time", dateFrom, dateTo)

    if dataDisposition:
        dispositionFilter = messageDefinition.sessionFilter.descendents.add()
        AddFilterPartCompare( dispositionFilter, "data_disposition", [PaceVariantTools.VariantFromString(dataDisposition.Name())] )

def AddFilterPartCompare(filter, uniqueId, variantValues):
    filterPart = filter.part
    filterPart.uniqueId = uniqueId
    filterPartCompare = filterPart.compare
    for variantValue in variantValues:
        nullableVariant = filterPartCompare.values.add()
        nullableVariant.variant.MergeFrom(variantValue)

def AddFilterPartRange(filter, uniqueId, dateFrom, dateTo):
    filterPart = filter.part
    filterPart.uniqueId = uniqueId
    filterPartRanges = filterPart.ranges
    range = filterPartRanges.ranges.add()
    if dateFrom:
        PaceVariantTools.AssignDatetime(range.start, dateFrom)
    if dateTo:
        PaceVariantTools.AssignDatetime(range.stop, dateTo)

class DeleteTaskListener( PositionApplicationCore.TaskListenerBase, object):        
    def PrivateCreateTaskFromDefinition(self, definition):
        taskDefinition = PositionDeleteTraits.Definition()
        
        sessiontType = definition.At( acm.FSymbol("sessionType") )
        dateFromAsDouble = DateTimeStrAsDouble(definition.At( acm.FSymbol("dateFrom") )) if  definition.At( acm.FSymbol("dateFrom") ) else None
        dateToAsDouble = DateTimeStrAsDouble(definition.At( acm.FSymbol("dateTo") ) ) if definition.At( acm.FSymbol("dateTo") ) else None
        dataDisposition = definition.At( acm.FSymbol("dataDisposition") )
        BuildAndAddSessionFilterToDefinition(taskDefinition, sessiontType, dateFromAsDouble, dateToAsDouble, dataDisposition)
        taskDefinition.deleteValueSessions = True
        
        return FPaceConsumer.Create( 'FrontArena.PositionStorage.Delete', taskDefinition )
    
    def PrivateOnResultUpdated(self, resultKey, resultEvent, result):  
        enumeration = acm.FEnumeration['enum(B92RecordType)']
        returnStr = "Deleted "
        for typeResult in result.recordTypeResults:
            if typeResult.HasField('failedRecordId'):
                returnStr = "Deletion failed for %s with storage id %i due to error: '%s'.\n" % \
                (enumeration.Enumerator(typeResult.recordType), typeResult.failedRecordId, typeResult.errorMessage) + returnStr 
            returnStr = returnStr + " %i of a total of %i %ss," % (typeResult.deletedRecords, typeResult.totalRecords, enumeration.Enumerator(typeResult.recordType))
        returnStr = returnStr[:-1] + "."
        print( returnStr )
  
    def PrivateOnInitialPopulateDone(self):
        self.m_statusMessage = None
        if self.m_encounteredErrors:
            self.m_statusMessage = 'Task done, encountered errors for %i records. See output for details.' % self.m_encounteredErrors


def CreateActivity(definition):
    activity = DeleteTaskListener.CreateActivity(definition)
    return activity
