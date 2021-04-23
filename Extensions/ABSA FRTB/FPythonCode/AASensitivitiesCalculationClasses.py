""" Compiled: 2020-09-18 10:41:36 """

#__src_file__ = "extensions/aa_integration/./etc/AASensitivitiesCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASensitivityCalculationClasses - Performer class for performing Sensitivity External
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
    ANALYSIS_TYPES = ('Sensitivities',)
    CALCULATION_TYPES = ('Sensitivities',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AASensitivitiesArtiQCalculationClasses
        importlib.reload(AASensitivitiesArtiQCalculationClasses)

        return AASensitivitiesArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'Sensitivities'
    _REQUEST_NAME = 'Sensitivities (External)'
    _DEFAULT_ATTRIBUTES = AAAttributes.DEFAULTATTRIBUTES
    #NO _CUSTOM_ATTRIBUTES
    
    def __init__(self, dictionary):

        self._datafile = dictionary['SensitivityData'].AsString()
        self._trdtagfile = dictionary['TradeTagsSen'].AsString()
        self._booktagfile = dictionary['BookTagsSen'].AsString()
        self._validatefile = dictionary['ValidateFileSen'].AsString()
        self._cube_catalog = dictionary['CubeCatalog']
        self._cube_name = dictionary['CubeName']
        self.appendDate = dictionary['AppendReferenceDate']
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        

    def _updateRequest(self, request_element):
        addDateStr = ''
        if self.appendDate:
            filePath = self._datafile + '\\' + str(self.ref_date) + '\\'
        else:
            filePath = self._datafile + '\\'

        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Trade Tags', value=self._trdtagfile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=self._booktagfile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Sensitivity Data', value=filePath
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Validate Market Sensitivities File', value=self._validatefile
        )
        return
