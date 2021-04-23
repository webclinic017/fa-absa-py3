""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASIMMCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASIMMCalculationClasses - Performer class for performing AA SIMM 
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
    ANALYSIS_TYPES = ('SIMM',)
    CALCULATION_TYPES = ('SIMM',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AASIMMArtiQCalculationClasses
        importlib.reload(AASIMMArtiQCalculationClasses)

        return AASIMMArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'SIMM'
    _REQUEST_NAME = 'ISDA SIMM (CRIF)'
    _DEFAULT_ATTRIBUTES = AAAttributes.SIMMATTRIBUTES
    #NO _CUSTOM_ATTRIBUTES
    
    def __init__(self, dictionary):

        self._file_path = dictionary['CRIFFilePath']
        self._cube_catalog = dictionary['CubeCatalog']
        self._cube_name = dictionary['CubeName']
        self.appendDate = dictionary['AppendReferenceDate']
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        market_data_path = dictionary['MarketDataPath']
        self._market_data_path = AAIntegrationUtility.forwardSlashedPath(
            path=market_data_path, real=True, check=True
        )
        currency = dictionary['Currency']
        self._currency = currency.Name()
        static_data_path = dictionary['StaticDataPath']
        self._static_data_path = AAIntegrationUtility.forwardSlashedPath(
            path=static_data_path, real=True, check=True
        )
        self._horizon = dictionary.get('Horizon', '10d')
        self._isCounterparty = 'Yes' if dictionary.get('IsCounterParty', 0) else 'No'
        self._counterparty = dictionary.get('CounterParty', None)
        
    def _updateRequest(self, request_element):
        addDateStr = ''
        if self.appendDate:
            addDateStr = '\\' + str(self.ref_date)

        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Reporting Currency', value=self._currency
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Market Data', value=self._market_data_path
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='External Sensitivities', value=self._file_path.AsString() + addDateStr + '\*.tsv'
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Static Data', value=self._static_data_path
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Horizon', value=self._horizon
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name="Is Counterparty&#8217;s CRIF file", value=self._isCounterparty
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name="Counterparty", value=self._counterparty
        )
        return
