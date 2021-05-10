""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMT395.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMT395 - Module that implements the MT 395 message functionality

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import FSwiftUtils

from FSwiftMTBase import GetRelatedEntityMessage, GetFieldValue, GetMessage
from FConfirmationEnums import ConfirmationType

def GetQueries(confirmation):
    '''A mandatory field 75 '''

    import FSwiftParameters as Global

    query = ''
    start_tag = '<MT395_ChaserComment>'
    end_tag = '</MT395_ChaserComment>'
    if confirmation.Type() == ConfirmationType.CHASER:
        diary = confirmation.Diary()
        if diary:
            diary_text = diary.Text()
            if diary_text.find(start_tag) > 0:
                startPos = diary_text.find(start_tag)+len(start_tag)
                endPos = diary_text.find(end_tag)
                query = diary_text[startPos:endPos]

    return FSwiftUtils.SwiftNarrativeTextFormatter.Format(query, Global.SEPARATOR, 35, 6)

def GetNarrative():
    ''' Optional field 77A '''

    return ''

def GetRelatedRef(confirmation):
    relatedRef = ''
    if confirmation.Type() in (ConfirmationType.CHASER):
        relatedConfirmation = confirmation.ChasingConfirmation()
        relatedConfirmationMessage = GetRelatedEntityMessage(relatedConfirmation)
        field = '20'
        relatedRef = GetFieldValue(relatedConfirmationMessage, field)

    return relatedRef

def GetOriginalMessageType(confirmation):
    ''' Mandatory field 11S '''

    mt = ''
    if confirmation.Type() == ConfirmationType.CHASER:
        relatedConfirmation = confirmation.ChasingConfirmation()
        operationDocuments =  relatedConfirmation.Documents()
        if operationDocuments:
            operationDocument = operationDocuments[0]
            mt = str(operationDocument.SwiftMessageType())

    return mt

def GetNarrativeDescription(confirmation):
    '''Optional Field 79 '''

    import FSwiftParameters as Global

    narrativeDescription = ''
    if confirmation.Type() == ConfirmationType.CHASER:
        relatedConfirmation = confirmation.ChasingConfirmation()
        operationDocuments =  relatedConfirmation.Documents()
        if operationDocuments:
            operationDocument = operationDocuments[0]
            message = GetMessage(operationDocument.DocumentId())
            swifthandler = FSwiftUtils.SwiftMessageHandler(message, operationDocument.SwiftMessageType())
            blockFieldList = swifthandler.GetBlockFieldList()
            mandatoryFieldsList = Global.MT_MANDATORY_FIELDS[operationDocument.SwiftMessageType()]
            fieldList = []

            for mandatoryField in mandatoryFieldsList:
                for fieldDict in blockFieldList:
                    if (fieldDict["Block"] == 4 and fieldDict["Field"] == mandatoryField):
                        fieldvaluestr = ":%s:%s".replace("\n", Global.SEPARATOR) % (fieldDict["Field"], fieldDict["Value"])
                        fieldList.append(fieldvaluestr)
                        break
                    narrativeDescription = Global.SEPARATOR.join(fieldList)

    return narrativeDescription


