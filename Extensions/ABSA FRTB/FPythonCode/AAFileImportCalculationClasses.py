""" Compiled: 2020-01-21 09:44:05 """

#__src_file__ = "extensions/aa_integration/./etc/AAFileImportCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAFileImportCalculationClasses - Performer class for performing AA CSV Import file data
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import os
import xml.etree.ElementTree as xmlElementTree

import AACalculationBase
import importlib
importlib.reload(AACalculationBase)
import AAAttributes
importlib.reload(AAAttributes)
import AAIntegrationUtility
importlib.reload(AAIntegrationUtility)
import FBDPCommon

class Manager(AACalculationBase.CalculationManagerBase):
    ANALYSIS_TYPES = ('CSV Import',)
    CALCULATION_TYPES = ('CSV Import',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AAFileImportArtiQCalculationClasses
        importlib.reload(AAFileImportArtiQCalculationClasses)

        return AAFileImportArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'CSV Import'
    _REQUEST_NAME = 'CSV Import'
    _DEFAULT_ATTRIBUTES = AAAttributes.CSVFILEIMPORTATTRIBUTES
    #NO _CUSTOM_ATTRIBUTES
    
    def __init__(self, dictionary):

        self._file_path = dictionary.get('FilePath', "")
        self._file_name = dictionary.get('FileName', "").AsString()
        self._cube_catalog = dictionary['CubeCatalog']
        self._cube_name = dictionary['CubeName']
        self.appendDate = dictionary['AppendReferenceDate']
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        self._trdtagfile = dictionary['TradeTags'].AsString()
        self._booktagfile = dictionary['BookTags'].AsString()
        
    def _getFileNames(self):
        if len(self._file_name) > 0 :
            return self._file_name
        
        addDateStr = ''
        if self.appendDate:
            addDateStr = '\\' + str(self.ref_date)

        fileNames = self._file_path.AsString() + addDateStr + '\*.csv'
        return fileNames
        
    def _updateRequest(self, request_element):
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Files', value=self._getFileNames()
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Trade Tags', value=self._trdtagfile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=self._booktagfile 
        )

        return
