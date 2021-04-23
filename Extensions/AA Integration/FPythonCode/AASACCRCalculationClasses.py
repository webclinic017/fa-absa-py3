""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASACCRCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AASACCRCalculationClasses - Performer class for performing AA SA-CCR data
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
import AASACCRAttributes
importlib.reload(AASACCRAttributes)
import AAIntegrationUtility
importlib.reload(AAIntegrationUtility)

class Manager(AACalculationBase.CalculationManagerBase):
    ANALYSIS_TYPES = ('SA-CCR',)
    CALCULATION_TYPES = ('SA-CCR',)

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AASACCRArtiQCalculationClasses
        importlib.reload(AASACCRArtiQCalculationClasses)

        return AASACCRArtiQCalculationClasses.CLASSES

class CommonCalculation(object):
    TYPE = 'SA-CCR'
    _REQUEST_NAME = 'SA-CCR'
    _DEFAULT_ATTRIBUTES = AAAttributes.SACCRATTRIBUTES
    _CUSTOM_ATTRIBUTES = AASACCRAttributes.ATTRIBUTES

    def __init__(self, dictionary):
    
        market_data_path = dictionary['MarketDataPath']
        deals_path = dictionary['DealsPath']
        rate_fixings_path = dictionary['RateFixingsPath']
        currency = dictionary['Currency']
        
        self._market_data_path = AAIntegrationUtility.forwardSlashedPath(
            path=market_data_path, real=True, check=True
        )
        self._deals_path = AAIntegrationUtility.forwardSlashedPath(
            path=deals_path, real=True, check=True
        )
        self._rate_fixings_path = AAIntegrationUtility.forwardSlashedPath(
            path=rate_fixings_path, real=True, check=True
        )
        self._currency = currency.Name()

    def _updateRequest(self, request_element):
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Market Data', value=self._market_data_path
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Deals', value=self._deals_path
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Rate Fixings', value=self._rate_fixings_path
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Reporting Currency', value=self._currency
        )
        return
