""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFileImportCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAFileImportCalculationClasses - Performer class for performing AA CSV Import file data
        calculation.

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

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

        self._file_path = dictionary['FilePath']
        self._cube_catalog = dictionary['CubeCatalog']
        self._cube_name = dictionary['CubeName']
        self.appendDate = dictionary['AppendReferenceDate']
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        

    def _updateRequest(self, request_element):
        addDateStr = ''
        if self.appendDate:
            addDateStr = '\\' + str(self.ref_date)

        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Files', value=self._file_path.AsString() + addDateStr + '\*.csv'
        )
        return
