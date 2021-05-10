""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationSwiftXMLSpecifier.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationSwiftXMLSpecifier -

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""

from FOperationsDocumentXMLSpecifier import XmlSpecifierBase
import ael


class ConfirmationSwiftXMLSpecifier(XmlSpecifierBase):


    def __GetAelConfirmationFromMbf(self, mbfMessage):

        confirmation = None
        if mbfMessage:
            mbfConfirmation = None
            o = mbfMessage.mbf_find_object('TYPE', 'MBFE_BEGINNING')
            if o:
                if o.mbf_get_value() == 'INSERT_CONFIRMATION':
                    mbfConfirmation = mbfMessage.mbf_find_object('+CONFIRMATION', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'UPDATE_CONFIRMATION':
                    mbfConfirmation = mbfMessage.mbf_find_object('!CONFIRMATION', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'DELETE_CONFIRMATION':
                    mbfConfirmation = mbfMessage.mbf_find_object('-CONFIRMATION', 'MBFE_BEGINNING')
                elif o.mbf_get_value() == 'CONFIRMATION':
                    mbfConfirmation = mbfMessage.mbf_find_object('CONFIRMATION', 'MBFE_BEGINNING')

            if mbfConfirmation:
                o = mbfConfirmation.mbf_find_object('SEQNBR', 'MBFE_BEGINNING')
                if o:
                    confirmation = ael.Confirmation[int(o.mbf_get_value())]

        return confirmation


    def __init__(self, mbfMessage, confirmation = None):
        ''' Confstructor for this class. Takes a mbf-message (the amba message). '''

        # Get the appropriate dictionary for this subclass.
        try:
            import FConfirmationSwiftXMLFields as XMLFields
        except ImportError:
            import FConfirmationSwiftXMLFieldsTemplate as XMLFields

        # Call base class constructor
        XmlSpecifierBase.__init__(self, XMLFields.field_dict)
        if confirmation != None:
            self.__confirmation = confirmation
            return

        assert (str(type(mbfMessage)) == "<type 'mbf_object'>"), \
            'Constructor called without mbfMessage'   # raise TypeException

        # Set the base ael entity
        confirmation = self.__GetAelConfirmationFromMbf(mbfMessage)
        assert confirmation, \
            'Constructor could not get confirmation record'
        self.__confirmation = confirmation


    def GetObject(self, typeAsString):
        ''' Get the objects involved in this XML '''
        # Check not on a string but on a real type instead? Enum?
        retEntity = None
        if typeAsString == 'Confirmation':
            retEntity = self.__confirmation
        elif typeAsString == 'Trade':
            if self.__confirmation:
                retEntity = self.__confirmation.trdnbr
        elif typeAsString == 'Instrument':
            if (self.__confirmation and self.__confirmation.trdnbr):
                retEntity = self.__confirmation.trdnbr.insaddr
        return retEntity


    def GetUniqueFilename(self, postfix = '', extension = 'xml'):
        ''' Creates a string that can be used to save a file with a unique filename '''
        file_prefix = 'confirmation'
        seqnbr = 0
        version = 0
        trade = None
        confirmation = self.GetObject('Confirmation')
        if confirmation:
            seqnbr = confirmation.seqnbr
            version = confirmation.version_id
        else:
            trade = self.GetObject('Trade')
            if (trade):
                seqnbr = trade.trdnbr
                version = trade.version_id

        filename = file_prefix + '_%d_%d%s.%s' % (seqnbr, version, postfix, extension)
        return filename



