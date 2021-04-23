""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMTBase.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftMTBase - Module that is the base of the SWIFT framework
    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module provides the base framework for classes that derive from this
    to use. Example for Swift message MT103 there is a class FSwiftMT103 that
    uses a lot of methods implemented in this module.

DATA-PREP
    None

REFERENCES
    None - this section will be updated later.

----------------------------------------------------------------------------"""

import FSwiftMessageTypeCalculator
import FOperationsUtils as Utils
import FOperationsDocumentService as DocumentService

METADATA_OPTIONS = {
                  103: {'ORDERING_CUSTOMER':['A', 'K', 'F'],
                        'INTERMEDIARY_INSTITUTION':['A', 'C', 'D'],
                        'BENEFICIARY_CUSTOMER':['A', '', 'F'],
                        'ACCOUNT_WITH_INSTITUTION':['A', 'C', 'D'],
                        'SENDERS_CORRESPONDENT': ['A', 'D'],
                        'ORDERING_INSTITUTION':['A', 'D']},
                  192: {},
                  199: {},
                  202: {'ACCOUNT_WITH_INSTITUTION':['A', 'D'],
                        'BENEFICIARY_INSTITUTION':['A', 'D'],
                        'INTERMEDIARY':['A', 'D'],
                        'SENDERS_CORRESPONDENT': ['A', 'D'],
                        'ORDERING_INSTITUTION':['A', 'D']},
                  210: {'ORDERING_CUSTOMER':['C', ''],
                        'ORDERING_INSTITUTION':['A', 'D'],
                        'INTERMEDIARY':['A', 'D']},
                  292: {},
                  299: {},
                  300:{'BUY_RECEIVING_AGENT': ['A',  'D',],
                       'SELL_RECEIVING_AGENT': ['A', 'D'],
                       'PARTY_B': ['A', 'D'],
                       'PARTY_A': ['A', 'D'],
                       'BUY_DELIVERY_AGENT' : ['A', 'D', 'J'],
                       'SELL_DELIVERY_AGENT' : ['A', 'D', 'J'],
                       'SELL_BENEFICIARY_INSTITUTION' : ['A', 'D', 'J'],
                       'BUY_INTERMEDIARY' : ['A', 'D'],
                       'SELL_INTERMEDIARY' : ['A', 'D'],
                       'REPORTING_PARTY' : ['A', 'D']},
                  305: {'SENDER_CORRESPONDENT': ['A', 'D'],
                       'ACCOUNT_WITH_INSTITUTION': ['A',  'D'],
                       'PARTY_B': ['A',  'D',],
                       'INTERMEDIARY': ['A', 'D'],
                       'PARTY_A': ['A', 'D',],
                       'REPORTING_PARTY' : ['A', 'D']},
                  306:{'SIP_PARTY_RECEIVING_AGENT': ['A', 'D'],
                       'PARTY_B': ['A', 'D'],
                       'PARTY_A': ['A', 'D'],
                       'PAYOUT_RECEIVING_AGENT':['J'],
                       'CALCULATION_AGENT':['A', 'D', 'J']},
                  320:{'SIA_PARTY_A_RECEIVING_AGENT': ['A', 'D'],
                       'SIA_PARTY_B_RECEIVING_AGENT': ['A', 'D'],
                       'SIA_PARTY_A_INTERMEDIARY': ['A', 'D'], \
                       'SIA_PARTY_B_INTERMEDIARY': ['A', 'D'], \
                       'PARTY_B': ['A', 'D'],
                       'PARTY_A': ['A', 'D']},
                  330:{'SIA_PARTY_A_RECEIVING_AGENT': ['A', 'D'],
                       'SIA_PARTY_B_RECEIVING_AGENT': ['A', 'D'],
                       'PARTY_B': ['A', 'D'],
                       'PARTY_A': ['A', 'D']},
                  362:{'NAP_PARTY_A_RECEIVING_AGENT': ['A', 'D'],
                       'NAP_PARTY_B_RECEIVING_AGENT': ['A', 'D'],
                       'PARTY_B': ['A', 'D'],
                       'PARTY_A': ['A', 'D']},

                  395:{},

                  540:{'SETTLEMENT_DATETIME':['A'],
                       'ACCOUNT':['A'],
                       'PARTY':['C', 'P', 'Q'],
                       'SAFEKEEPING_ACCOUNT':['A']},
                  541:{'SETTLEMENT_DATETIME':['A'],
                       'ACCOUNT':['A'],
                       'PARTY':['C', 'P', 'Q'],
                       'SAFEKEEPING_ACCOUNT':['A']},
                  542:{'SETTLEMENT_DATETIME':['A'],
                       'ACCOUNT':['A'],
                       'PARTY':['C', 'P', 'Q'],
                       'SAFEKEEPING_ACCOUNT':['A']},
                  543:{'SETTLEMENT_DATETIME':['A'],
                       'ACCOUNT':['A'],
                       'PARTY':['C', 'P', 'Q'],
                       'SAFEKEEPING_ACCOUNT':['A']}
                 }

def Init():
    pass

def GetSwiftMessageType(fObject):
    swiftMessageType = FSwiftMessageTypeCalculator.Calculate(fObject)
    if swiftMessageType == 199:
        swiftMessageType = 103
    elif swiftMessageType == 299:
        swiftMessageType = 202
    return swiftMessageType

def GetNarrativeSeparator():
    '''NARRATIVE_SEPARATOR will be used when creating new lines.
    Default is newline.'''
    import FSwiftParameters as Global

    return Global.SEPARATOR

def GetCodewordNewline():
    '''CODEWORD_NEWLINE will be used to specify the start of a codeword.
    Default value is codeword.'''
    import FSwiftParameters as Global

    return Global.CODEWORD_NEWLINE

def GetVersion(confirmation):
    '''Returns the version of the record.'''
    return confirmation.VersionId()

def GetRelatedEntityMessage(fObject):
    relatedEntityMessage = ''
    opdocs = fObject.Documents()
    if not opdocs.IsEmpty():
        relatedEntityMessage = GetMessage(opdocs[0].DocumentId())

    return relatedEntityMessage

def GetFieldValue(message, field):
    '''Returns Value for the first occurence of the specified field from the
                SWIFT MT message '''

    Value = ""
    if len(message):
        field = ":" + field + ":"
        start = message.find(field)
        if start:
            end = message.find("\r\n", start)
            field = message[start:end]
            if len(field):
                pos = field.rfind(":")
                Value = field[pos+1:]

    return Value

def GetMessage(docId):
    '''Returns ACII document representation of the MT message
    via document id. '''

    import FDocumentationParameters as DocumentParameters

    try:
        docService = DocumentService.CreateDocumentService(DocumentParameters)
        mt = ''
        if docService.IsConnected():
            document = docService.GetDocument(docId, DocumentService.DocumentFormat.ASCII)
            mt = document.GetData()
        else:
            Utils.LogAlways('No connection to document service.')
        return mt

    except DocumentService.DocumentServiceException as e:
        Utils.LogAlways('Could not do fetch document %d: %s' % \
                    (docId, e))
        return ""

def GetOptionValue(key, fObject):
    import FSwiftParameters as Global

    option = ''
    mt = GetSwiftMessageType(fObject)
    if mt in Global.OPTIONS:
        if key in Global.OPTIONS[mt]:
            option = Global.OPTIONS[mt][key]
    return option

def GetPartyBic(account):
    bic = ''
    if account.NetworkAlias():
        bic = account.NetworkAlias().Alias()
    if not bic:
        assert account.Party(), "The account has no party reference"
        bic = account.Party().Swift()
    return bic

def GetPartyAddress(party):
    return "{} {} {}".format(GetPartyStreetAndNumber(party), party.City(), party.Country())

def GetPartyStreetAndNumber(party):
    return "{} {}".format(party.Address(), party.Address2()) if party.Address() != party.Address2() and party.Address2() != "" else party.Address()

def GetPartyFullName(party):
    import FSwiftParameters as Global

    name = ''
    if Global.USE_PARTY_FULLNAME:
        name = party.Fullname()
    if not name:
        name = party.Id()
    return name
