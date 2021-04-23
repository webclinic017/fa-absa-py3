""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAPLRatesCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAPLRatesCalculationClasses - Performer class for performing PL Rates External
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
    ANALYSIS_TYPES = ('PLRates',)
    CALCULATION_TYPES = ('PLRates',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AAPLRatesArtiQCalculationClasses
        importlib.reload(AAPLRatesArtiQCalculationClasses)

        return AAPLRatesArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'PLRates'
    _REQUEST_NAME = 'P&amp;L Rates (External)'
    _DEFAULT_ATTRIBUTES = AAAttributes.DEFAULTATTRIBUTES
    #NO _CUSTOM_ATTRIBUTES
    
    def __init__(self, dictionary):

        self._plratesfile = dictionary['PLRateData'].AsString()
        self._cube_catalog = dictionary['CubeCatalog']
        self._cube_name = dictionary['CubeName']
        self.appendDate = dictionary['AppendReferenceDate']
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        

    def _updateRequest(self, request_element):

        xmlElementTree.SubElement(
            request_element, 'Property',
            name='P&amp;L Rates Data', value=self._plratesfile
        )
        return