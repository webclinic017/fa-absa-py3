""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTCancellation.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMTCancellation - Module that implements the MT n92 message series

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

from FSwiftMTBase import GetMessage, GetFieldValue
from FSettlementEnums import RelationType, SettlementStatus
from FOperationsDocumentEnums import OperationsDocumentStatus


def Init():
    pass

def IsCancellation(settlement):
    return settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT]

def IsNakCancellation(settlement):
    return settlement.Status() == SettlementStatus.PENDING_CANCELLATION

def GetRelatedSettlement(settlement):
    if IsCancellation(settlement):
        return settlement.Children()[0]
    elif IsNakCancellation(settlement):
        return settlement
    return None

def GetDocumentsToCancel(settlement):
    operationDocuments =  GetRelatedSettlement(settlement).Documents()
    documentsToCancel = []
    if IsNakCancellation(settlement):
        for document in operationDocuments:
            if document.Status() == OperationsDocumentStatus.SENT_SUCCESSFULLY:
                documentsToCancel.append(document)
    else:
        documentsToCancel = operationDocuments

    return documentsToCancel

def GetRelatedRef(settlement):
    '''Mandatory field 21, for n92 Settlement '''
    documentsToCancel = GetDocumentsToCancel(settlement)
    relatedReference = ''
    if len(documentsToCancel) == 1:
        document = documentsToCancel[0]
        message = GetMessage(document.DocumentId())
        field = '20'
        relatedReference = GetFieldValue(message, field)

    elif len(documentsToCancel) == 2:
        # assumption here is that one of two documents is for n99
        for document in documentsToCancel:
            messageType = document.SwiftMessageType()
            message = GetMessage(document.DocumentId())
            field = '20'
            relatedReferenceValue = GetFieldValue(message, field)
            if messageType in (103, 202, 210):
                relatedReference = relatedReferenceValue
    return relatedReference

def GetRelatedRef99(settlement):
    '''Mandatory field 21, for n99 Settlement '''
    documentsToCancel = GetDocumentsToCancel(settlement)
    relatedReference99 = ''
    if len(documentsToCancel) == 2:
        # assumption here is that one of two documents is for n99
        for document in documentsToCancel:
            messageType = document.SwiftMessageType()
            message = GetMessage(document.DocumentId())
            field = '20'
            relatedReferenceValue = GetFieldValue(message, field)
            if messageType in (199, 299):
                relatedReference99 = relatedReferenceValue
    return relatedReference99

def GetOriginalMessageType(settlement):
    '''Mandatory field 11S for n92 settlement'''
    documentsToCancel = GetDocumentsToCancel(settlement)
    messageType = ''
    if len(documentsToCancel) == 1:
        document = documentsToCancel[0]
        messageType = document.SwiftMessageType()

    elif len(documentsToCancel) == 2:
        # assumption here is that one of two documents is for n99
        for document in documentsToCancel:
            messageTypeValue = document.SwiftMessageType()
            if messageTypeValue in (103, 202, 210):
                messageType = messageTypeValue
    return messageType

def GetOriginalMessageType99(settlement):
    '''Mandatory field 11S for n92 settlement. Used if n99 is also to be
    cancelled.'''
    documentsToCancel = GetDocumentsToCancel(settlement)
    messageType99 = ''
    if len(documentsToCancel) == 2:
        # assumption here is that one of two documents is for n99
        for document in documentsToCancel:
            messageTypeValue = document.SwiftMessageType()
            if messageTypeValue in (199, 299):
                messageType99 = messageTypeValue
    return messageType99

def GetOriginalMessageDate(settlement):
    '''Mandatory field 11S '''

    import FSwiftParameters as Global

    relatedSettlement = GetRelatedSettlement(settlement)
    if relatedSettlement and Global.POPULATE_RELEASE_DAY:
        return relatedSettlement.ValueDay()

    return ''

def GetOriginalMessageDate99(settlement):
    '''Mandatory field 11S. Used if n99 is also to be cancelled.'''

    import FSwiftParameters as Global
    
    if GetOriginalMessageType99(settlement) != '':
        relatedSettlement = GetRelatedSettlement(settlement)
        if relatedSettlement and Global.POPULATE_RELEASE_DAY:
            return relatedSettlement.ValueDay()

    return ''

def GetNarrativeDescription(settlement):
    '''Optional field 79 for n92 Settlement. '''

    narrativeDescription = ''
    if IsCancellation(settlement):
        relatedSettlement = GetRelatedSettlement(settlement)
        narrativeDescription = 'Settlement Id %s was due to %s' % \
            (relatedSettlement.Oid(),
            relatedSettlement.ValueDay())
    elif IsNakCancellation(settlement):
        narrativeDescription = 'Cancelling previous MT%s' % (GetOriginalMessageType(settlement))

    return narrativeDescription

def GetNarrativeDescription99(settlement):
    '''Optional field 79 for n92 Settlement. Used if n99 is also
    to be cancelled. '''

    narrativeDescription = ''
    messagetype99 = GetOriginalMessageType99(settlement)
    if messagetype99 != '':
        if IsCancellation(settlement):
            relatedSettlement = GetRelatedSettlement(settlement)
            narrativeDescription = 'Settlement Id %s was due to %s' % \
                (relatedSettlement.Oid(),
                relatedSettlement.ValueDay())
        elif IsNakCancellation(settlement):
            narrativeDescription = 'Cancelling previous MT%s' % (messagetype99)

    return narrativeDescription

