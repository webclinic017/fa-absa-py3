""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSwiftXMLSpecifier.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSwiftXMLSpecifier -

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""


from FOperationsDocumentXMLSpecifier import XmlSpecifierBase
import ael

class SettlementSwiftXMLSpecifier(XmlSpecifierBase):
    ''' Class for describing how the XML for settlement swift should be
        created. '''


    def __GetAelSettlementFromMbf(self, mbfMessage):
        ''' Helpfunction for getting the ael settlement out of the mbf-message. '''
        settlement = None
        if mbfMessage:
            mbfSettlement = None
            o = mbfMessage.mbf_find_object('TYPE', 'MBFE_BEGINNING')
            if o:
                if o.mbf_get_value() == 'INSERT_SETTLEMENT':
                    mbfSettlement = mbfMessage.mbf_find_object('+SETTLEMENT', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'UPDATE_SETTLEMENT':
                    mbfSettlement = mbfMessage.mbf_find_object('!SETTLEMENT', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'DELETE_SETTLEMENT':
                    mbfSettlement = mbfMessage.mbf_find_object('-SETTLEMENT', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'SETTLEMENT':
                    mbfSettlement = mbfMessage.mbf_find_object('SETTLEMENT', 'MBFE_BEGINNING')

            if mbfSettlement:
                o = mbfSettlement.mbf_find_object('SEQNBR', 'MBFE_BEGINNING')
                if o:
                    settlement = ael.Settlement[int(o.mbf_get_value())]

        return settlement


    def __init__(self, mbfMessage, settlement = None):
        ''' Confstructor for this class. Takes a mbf-message (the amba message). '''
        # Get the appropriate dictionary for this subclass.
        try:
            import FSettlementSwiftXMLFields as XMLFields
        except ImportError:
            import FSettlementSwiftXMLFieldsTemplate as XMLFields
        # Call base class constructor
        XmlSpecifierBase.__init__(self, XMLFields.field_dict)
        if settlement != None:
            self.__settlement = settlement
            return
        assert (str(type(mbfMessage)) == "<type 'mbf_object'>"), \
            'Constructor called without mbfMessage'   # Something nicer? raise TypeException

        # Set the base ael entity
        settlement = self.__GetAelSettlementFromMbf(mbfMessage)
        assert settlement, \
            'Constructor could not get settlement record'
        self.__settlement = settlement


    def GetObject(self, typeAsString):
        ''' Get the objects involved in this XML '''
        # Check not on a string but on a real type instead? Enum?
        retEntity = None
        if typeAsString == 'Settlement':
            retEntity = self.__settlement
        elif typeAsString == 'Trade':
            if self.__settlement:
                retEntity = self.__settlement.trdnbr
        elif typeAsString == 'Instrument':
            if (self.__settlement and self.__settlement.trdnbr):
                retEntity = self.__settlement.trdnbr.insaddr
        return retEntity


    def GetUniqueFilename(self, postfix = '', extension = 'xml'):
        ''' Creates a string that can be used to save a file with a unique filename '''
        file_prefix = 'settlement'
        seqnbr = 0
        version = 0
        settlement = self.GetObject('Settlement')
        if settlement:
            seqnbr = settlement.seqnbr
            version = settlement.version_id
        else:
            trade = self.GetObject('Trade')
            if (trade):
                seqnbr = trade.trdnbr
                version = trade.version_id

        filename = file_prefix + '_%d_%d%s.%s' % (seqnbr, version, postfix, extension)
        return filename

