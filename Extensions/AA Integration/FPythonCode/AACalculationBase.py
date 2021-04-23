""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AACalculationBase.py"
from __future__ import print_function
import importlib
"""----------------------------------------------------------------------------
MODULE
    AACalculationBase - AA calculation request base class.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import re
import xml.etree.ElementTree as xmlElementTree

import AAIntegrationUtility
importlib.reload(AAIntegrationUtility)
from AACalculate import Calculate
from AAAttributes import CALC_SNAPSHOT_MAP
import FBDPCommon

class CalculationManagerBase(object):
    """
    Responsible for determining which requestor to use.
    """
    ANALYSIS_TYPES = None
    SINKS = ('artiQ', 'artiQ Store')

    @staticmethod
    def getAllCalculationClasses(manager, callee_module_attrs):
        classes = []
        for calc_type in manager.ANALYSIS_TYPES:
            calc_name = ''.join(re.split(' |_|\-', calc_type))
            for sink in manager.SINKS:
                parts = sink.split()
                sink = ''
                for part in parts:
                    for i, s in enumerate(part):
                        sink += s.upper() if i == 0 else s

                cls_name = sink + calc_name + 'Calculation'
                classes.append(callee_module_attrs[cls_name])

        return tuple(classes)

    def __init__(self):
        self._calculation_classes = tuple(self._getCalculationClasses())
        self._performChecks()

    def getCalculationClass(self, sink, calc_type):
        calc_class = None
        for cc in self._calculation_classes:
            if (cc.SINK == sink) and (cc.TYPE == calc_type):
                    calc_class = cc
                    break

        if calc_class == None:
            raise Exception('Unable to select AA calculation class.')

        calc_class.NAME = 'AA ' + calc_class.TYPE.lower() + ' calculation requester'
        return calc_class

    def _getCalculationClasses(self):
        raise NotImplementedError

    def _performChecks(self):
        types = sorted(self.ANALYSIS_TYPES)
        print(types)
        for sink in self.SINKS:
            calc_types = [
                cls.TYPE for cls in self._calculation_classes if cls.SINK == sink
            ]
            print(calc_types)
            assert sorted(calc_types) == types, \
                'Not all %s calculation managers are of calculation types: %s' % (
                sink, str(types))
        return

class CalculationBase(object):
    """
    Responsible for forming and sending the calculation request.
    """
    NAME = SINK = TYPE = _REQUEST_NAME = None
    _DEFAULT_ATTRIBUTES = None
    _CUSTOM_ATTRIBUTES = None

    def __init__(self, dictionary):
        self._attrs = self._DEFAULT_ATTRIBUTES.copy()
        self._attrs.update(self._CUSTOM_ATTRIBUTES or {})
        Calculate.initialise(attributes=self._attrs)
        self._attrs.update(Calculate.getAttributes())
        self._base_date = AAIntegrationUtility.getAAFormattedDate(
            date=FBDPCommon.toDate(dictionary.get('RefDate'))
        )
        calcType = dictionary.get('CalculationType', None)
        self._correction = True if calcType == 'Correction' else False
        self._whatIf = "What-if" if calcType == 'What-if' else ""

    def performRequest(self):
        print(self.NAME)
        calculation_request = self._generateRequest().replace('&amp;', '&')
        print(calculation_request)
        calculation_response = Calculate.sendRequest(calculation_request)
        print(calculation_response)
        return calculation_response

    def _getAttributes(self):
        raise NotImplementedError

    def _generateRequest(self):
        raise NotImplementedError

class ArtiQCalculationBase(CalculationBase):
    SINK = 'artiQ'
    
    def __init__(self, dictionary):
        CalculationBase.__init__(self, dictionary)

    def _generateRequest(self):
        request_element = xmlElementTree.Element(
            'Calculation', name=self._REQUEST_NAME, sink=self.SINK
        )
        self._updateRequestWithDestination(request_element=request_element)
        xmlElementTree.SubElement(request_element, 'Property', name='Base Date', value=self._base_date)
        self._updateRequest(request_element)
        if self._correction == True:
            self._updateRequestWithCorrection(request_element)
        request = xmlElementTree.tostring(request_element).decode()
        return request
    
    def _updateRequestWithCorrection(self, request_element):
        sub = xmlElementTree.SubElement(
            request_element, 'Map')
        xmlElementTree.SubElement(
            sub, 'Map',
            source='Trade.Reference', target="Trade.Reference+")
        return

    def _updateRequestWithDestination(self, request_element):
        snap_shot = CALC_SNAPSHOT_MAP[self.TYPE]
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Destination Catalog', value=self._getCatalogName()
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Destination Cube', value=self._getCubeName()
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Destination Snapshot',
            value=str(snap_shot)
        )
        if self.SINK == 'artiQ Store':
            xmlElementTree.SubElement(
                request_element, 'Property',
                name='Destination Increment', value=self._whatIf
            )
        return

    def _updateRequest(self, request_element):
        raise NotImplementedError

    def _getCubeName(self):
        return 'Default'

    def _getCatalogName(self):
        raise NotImplementedError

class ArtiQStoreCalculationBase(ArtiQCalculationBase):
    SINK = 'artiQ Store'
    def __init__(self, dictionary):
        ArtiQCalculationBase.__init__(self, dictionary)
