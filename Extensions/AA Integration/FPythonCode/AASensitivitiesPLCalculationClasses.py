""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASensitivitiesPLCalculationClasses.py"
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
    ANALYSIS_TYPES = ('SensitivitiesPL',)
    CALCULATION_TYPES = ('SensitivitiesPL',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AASensitivitiesPLArtiQCalculationClasses
        importlib.reload(AASensitivitiesPLArtiQCalculationClasses)

        return AASensitivitiesPLArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'SensitivitiesPL'
    _REQUEST_NAME = 'Sensitivity-Based P&amp;L (External)'
    _DEFAULT_ATTRIBUTES = AAAttributes.DEFAULTATTRIBUTES
    #NO _CUSTOM_ATTRIBUTES
    
    def __init__(self, dictionary):

        self._datafile = dictionary['SensitivityDataPL'].AsString()
        self._trdtagfile = dictionary['TradeTagsPL'].AsString()
        self._booktagfile = dictionary['BookTagsPL'].AsString()
        self._validatefile = dictionary['ValidateFilePL'].AsString()
        self._plratesfile = dictionary['PLRateDataSenPL'].AsString()
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
            name='Trade Tags', value=self._trdtagfile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=self._booktagfile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Sensitivity Data', value=self._datafile 
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Validate Market Sensitivities File', value=self._validatefile
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='P&amp;L Rates Data', value=self._plratesfile
        )
        return
