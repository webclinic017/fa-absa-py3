'''-----------------------------------------------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : Base class for SWIFT MT messages
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Francois Truter
CR NUMBER               : XXXXXX
---------------------------------------------------------------------------------------------------------------------

HISTORY
=====================================================================================================================
Date            Change no       Developer                   Description
---------------------------------------------------------------------------------------------------------------------
2011-03-25      XXXXXX          Francois Truter             Initial Implementation
2015-09-02      CHNG            Lawrence Mucheka            Get SWift Code from the BIC field on the Party Main screen
2016-02-05      CHNG0003427057  Gabriel Marko               Get MT940 Recipient from MT940RecipientBIC PartyAlias
2016                            Willie van der Bank         Added functionality to not have to pass the trade cpty
                                                            for Demat
'''

import acm
from gen_swift_mt_blocks import BasicHeaderBlock
from gen_swift_mt_blocks import ApplicationHeaderBlock
from gen_swift_mt_blocks import UserHeaderBlock
from gen_swift_mt_blocks import TrailerBlock

MAX_REFERENCE_LENGTH = 16


class MtMessageBase(object):

    def __init__(self):
        self._header = BasicHeaderBlock()
        self._applicationHeader = ApplicationHeaderBlock()
        self._userHeader = UserHeaderBlock()
        self._body = None
        self._trailer = TrailerBlock()

    @property
    def Header(self):
        return self._header

    @property
    def ApplicationHeader(self):
        return self._applicationHeader

    @property
    def UserHeader(self):
        return self._userHeader

    @property
    def Body(self):
        return self._body

    @property
    def Trailer(self):
        return self._trailer

    def __str__(self):
        blocks = [
            self._header,
            self._applicationHeader,
            self._userHeader,
            self._body,
            self._trailer
        ]

        _str = ''
        for block in blocks:
            _str += str(block)
        return _str

    def SetMeridianBusinessEntityFromParty(self, party):
        if isinstance(party, str):
            self.UserHeader.MessageUserReference = party
            return
            
        businessEntity = party.AdditionalInfo().MeridianSwiftBusEnt()
        if not businessEntity:
            raise Exception("Party Additional Info 'MeridianSwiftBusEnt' is required for SWIFT messages (%s): not set for party '%s'" %
                (self.__class__.__name__, party.Name()))
        else:
            self.UserHeader.MessageUserReference = businessEntity

    def SetRecipientFromParty(self, party, additionalInfoName):
        if isinstance(party, str):
            self.ApplicationHeader.Address.BicCode = party
            return
            
        additionalInfo = party.AdditionalInfo()
        if not hasattr(additionalInfo, additionalInfoName):
            raise Exception('Party does not have additional info %s' % additionalInfoName)

        addInfoMethod = getattr(additionalInfo, additionalInfoName)
        recipient = addInfoMethod()

        if not recipient:
            raise Exception("Party Additional Info '%s' is required for SWIFT messages, it has not been set for '%s'." % (additionalInfoName, party.Name()))

        bic = recipient.SwiftAlias() or recipient.Swift()
        if not bic:
            raise Exception('Parties that have to receive SWIFT messages have to set one SWIFT Alias for the party. Could not get SWIFT Alias for [%s].' % party.Name())
        else:
            self.ApplicationHeader.Address.BicCode = bic


def GetTransactionReferenceFromStatement(object, statementDate, statementNumber):
    dateFormatter = acm.FDateFormatter('dateFormatter')
    dateFormatter.FormatDefinition('%y')
    year = dateFormatter.Format(statementDate)
    reference = 'PS%(object)i-%(year)s%(statement)s' % {'object': object.Oid(), 'year': year, 'statement': statementNumber}
    if len(reference) > MAX_REFERENCE_LENGTH:
        raise Exception('The transaction reference [%(reference)s] for %(type)s [%(object)s], statement [%(statement)s] is too long. Maximum length is 16 characters' %
            {'reference': reference, 'type': object.ClassName(), 'object': object.Name(), 'statement': statementNumber})
    return reference


def GetTransactionReferenceFromRunDate(object, statementDate):
    dateFormatter = acm.FDateFormatter('dateFormatter')
    dateFormatter.FormatDefinition('%y%m%d')
    reference = '%(object)i-%(date)s' % {'object': object.Oid(), 'date': dateFormatter.Format(statementDate)}
    if len(reference) > MAX_REFERENCE_LENGTH:
        raise Exception('The transaction reference {0} is too long. Maximum length is 16 characters.'.format(reference))
    return reference
