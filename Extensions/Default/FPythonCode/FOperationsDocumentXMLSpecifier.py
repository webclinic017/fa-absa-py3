""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLSpecifier.py"
"""----------------------------------------------------------------------------
MODULE
    FOperationsDocumentXMLSpecifier - 

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION    
----------------------------------------------------------------------------"""
import FOperationsUtils


class XmlSpecifierBase():
    ''' Base class for the XmlSpecifier classes that is used as parameter to the
        FOperationsDocumentXmlCreator class. This base class is abstract and can not be
        instanciated. '''

    def __init__(self, fieldDict):
        ''' Constructor the takes the fieldDict that specifies what fields
            and tables that should be included in the XML.'''
        if self.__class__ is XmlSpecifierBase:
            raise NotImplementedError
        assert fieldDict, \
            'Base class constructor could not find a field dictionary'            
        self.fieldDict = fieldDict
        self.__XMLExtendHook = None
  

    def IncludeField(self, tableName, fieldName):
        ''' IncludeFields takes a table and a fields and returns 1 if the
            field should be included in the XML and 0 if it should not be
            included. The fieldDict in the constructor is used here. '''
        
        ret = 0
        if (tableName and fieldName and self.fieldDict):
            if self.IncludeTable(tableName):
                fieldName = fieldName.upper()
                tableName = tableName.upper()
                # Always add primary keys.
                if (FOperationsUtils.get_primary_key_field(tableName) == fieldName):
                    ret = 1
                # Check for the field in the tables dictionary
                
                elif (tableName in self.fieldDict) and (fieldName in self.fieldDict[tableName]):
                    ret = 1
        return ret
        
        
    def IncludeTable(self, tableName):
        ''' IncludeTable checks if the given table should be included in the
            XML or not. The fieldDict is used '''
        ret = 0
        if tableName and self.fieldDict:
            ret = tableName.upper() in self.fieldDict
        return ret

    def GetObject(self, typeAsString):
        ''' GetObject method is used to retrieve entities from the class.
            Since only the confirmation/settlement is picked up from the
            AMB-message, and the rest from ads/ael a sync bug could in very
            rare cases occure. '''
        raise NotImplementedError
        
    def GetUniqueFilename(self, postfix = '', extension = 'xml'):
        ''' When saving the XML as file on disk, this function can be used
            to get a unique filename. The primary key and the version_id will
            be used. '''
        raise NotImplementedError
    
    def GetExtendHook(self):
        ''' Currently not implemented yet! Supposed to deliver a hook for
            extending the XML. '''
        return self.__XMLExtendHook

    def GetSwiftBoEntity(self, entity):
        ''' Returns an object of type FSwiftBOEntity '''
        return None

    def IncludeUnderlyingInstrument(self):
        ''' IncludeUnderlyingInstrument '''
        return ('INSTRUMENT' in self.fieldDict and
                'UND_INSADDR' in self.fieldDict['INSTRUMENT'])

    def IncludeCombinationComponent(self):
        ''' IncludeCombinationComponent '''
        return ('INSTRUMENT' in self.fieldDict and
                'COMBINATIONLINK' in self.fieldDict)

    def IncludeCorrectedTrade(self):
        ''' IncludeCorrectedTrade '''
        return ('TRADE' in self.fieldDict and
                'CORRECTION_TRDNBR' in self.fieldDict['TRADE'])

    def IncludeClosedTrade(self):
        ''' IncludeClosedTrade '''
        return ('TRADE' in self.fieldDict and
                'CONTRACT_TRDNBR' in self.fieldDict['TRADE'])

    def IncludeExercisedTrade(self):
        ''' IncludeExercisedTrade '''
        return ('TRADE' in self.fieldDict and
                'CONTRACT_TRDNBR' in self.fieldDict['TRADE'])

    def IncludeCollateralTrade(self):
        ''' IncludeCollateralTrade '''

        return ('TRADE' in self.fieldDict and
                'CONNECTED_TRDNBR' in self.fieldDict['TRADE'])

    def IncludeCounterparty(self):
        ''' IncludeCounterparty '''
        return ('PARTY' in self.fieldDict and
                'TRADE' in self.fieldDict and
                'COUNTERPARTY_PTYNBR' in self.fieldDict['TRADE'])

    def IncludeAcquirer(self):
        ''' IncludeAcquirer '''
        return ('PARTY' in self.fieldDict and
                'TRADE' in self.fieldDict and
                'ACQUIRER_PTYNBR' in self.fieldDict['TRADE'])

    def IncludeBroker(self):
        ''' IncludeBroker '''
        return ('PARTY' in self.fieldDict and
                'TRADE' in self.fieldDict and
                'BROKER_PTYNBR' in self.fieldDict['TRADE'])

    def IncludeCreditRef(self):
        ''' IncludeCreditRef '''
        return ('INSTRUMENT' in self.fieldDict and
                'LEG' in self.fieldDict and
                'CREDIT_REF' in self.fieldDict['LEG'])

    def IncludeIssuer(self):
        ''' IncludeIssuer '''
        return ('INSTRUMENT' in self.fieldDict and
                'PARTY' in self.fieldDict and
                'ISSUER_PTYNBR' in self.fieldDict['INSTRUMENT'])

