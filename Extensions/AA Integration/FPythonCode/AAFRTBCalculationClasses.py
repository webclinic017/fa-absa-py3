""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFRTBCalculationClasses.py"
"""----------------------------------------------------------------------------
MODULE
    AAFRTBCalculationClasses - Performer class for performing AA FRTB data
        calculation.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import os
import xml.etree.ElementTree as xmlElementTree

import AACalculationBase
import importlib
importlib.reload(AACalculationBase)
import AAIntegrationUtility
importlib.reload(AAIntegrationUtility)
import AAAttributes
importlib.reload(AAAttributes)
import AAFRTBAttributes
importlib.reload(AAFRTBAttributes)
import FBDPCommon

class Manager(AACalculationBase.CalculationManagerBase):
    ANALYSIS_TYPES = ('SA SBA', 'SA DRC', 'SA RRAO', 'IMA ES',
        'IMA Hypothetical_PL', 'IMA Risk_Theoretical_PL',
        'IMA SES', 'IMA DRC', 'FRTB All')

    def _getCalculationClasses(self):
        # update this tuple with any new managers created.
        import AAFRTBArtiQCalculationClasses
        importlib.reload(AAFRTBArtiQCalculationClasses)

        return AAFRTBArtiQCalculationClasses.CLASSES

class CommonCalculationBase(object):
    _DEFAULT_ATTRIBUTES = AAAttributes.FRTBATTRIBUTES
    _CUSTOM_ATTRIBUTES = AAFRTBAttributes.ATTRIBUTES

    def __init__(self, dictionary):
        self.ref_date = FBDPCommon.toDate(dictionary.get('RefDate'))
        ext = dictionary['Extension']
        self.appendDate = dictionary['AppendReferenceDate']
        dir_path = self.getDirPath(dictionary)
        filepaths = None
        if dir_path is not None:
            dir_path, filepaths = AAIntegrationUtility.getInputDirectory(
                dir_path=str(dir_path),
                ref_date=None,#ref_date=ref_date,
                ext=ext)
            self._filepaths = tuple(filepaths)
        
        self._input_path = dir_path
        self._dictionary = dictionary
        self._ext = ext.lower()

    def getFiles(self):
        return self._filepaths
    
    def getDirPath(self, dictionary):
        raise AssertionError('Base class implementation cannot be called')

class CommonCalculation(object):
    TYPE = None
    _REQUEST_NAME = None
    _INPUT_PATH_FIELD_NAME = None
    _INPUT_IS_PATH = True
    _INPUT_PATH_VARIABLE = None

    def _updateRequest(self, request_element):
        addDateStr = '/' + str(self.ref_date) if self.appendDate else ''
        if self._input_path is not None:
            xmlElementTree.SubElement(
                request_element, 'Property',
                name=self._INPUT_PATH_FIELD_NAME,
                value=self._input_path + addDateStr + \
                    (('/*' + self._ext) if self._INPUT_IS_PATH else '')
            )
        return

class CommonSACalculation(CommonCalculation):
    def _updateRequest(self, request_element):
        CommonCalculation._updateRequest(self, request_element=request_element)
        xmlElementTree.SubElement(request_element, 'Property', name='Static Data',
            value=AAIntegrationUtility.forwardSlashedPath(
                path=self._attrs['COMBINED_STATIC_DATA_PATH'],
                real=True, check=True))
        xmlElementTree.SubElement(request_element, 'Property', name='Base Currency',
            value='EUR') # USE BASE CURRENCY FROM TASK
        xmlElementTree.SubElement(request_element, 'Property', name='Trade Tags',
            value="")
        xmlElementTree.SubElement(request_element, 'Property', name='Book Tags',
            value="")
        xmlElementTree.SubElement(request_element, 'Property', name='Factor Grouping Data',
            value="")
        return

class CommonSASBACalculation(CommonSACalculation):
    TYPE = 'SA SBA'
    _REQUEST_NAME = 'FRTB SA Sensitivity Based Approach (External)'
    _INPUT_PATH_FIELD_NAME = 'External Sensitivities'
    _INPUT_PATH_VARIABLE = 'SASBASensitivities'
    _INPUT_IS_PATH = True
    def _updateRequest(self, request_element):
        CommonSACalculation._updateRequest(self, request_element=request_element)

class CommonSADRCCalculation(CommonSACalculation):
    TYPE = 'SA DRC'
    _REQUEST_NAME = 'FRTB SA Default Risk Charge (External)'
    _INPUT_PATH_FIELD_NAME = 'External Trade Data'
    _INPUT_PATH_VARIABLE = 'SADRCDeals'
    _INPUT_IS_PATH = True

class CommonSARRAOCalculation(CommonSADRCCalculation):
    TYPE = 'SA RRAO'
    _REQUEST_NAME = 'FRTB SA Residual Risk Add-On (External)'
    _INPUT_PATH_VARIABLE = 'SARRAODeals'
    _INPUT_IS_PATH = True

class CommonIMAESCalculation(CommonCalculation):
    TYPE = 'IMA ES'
    _REQUEST_NAME = 'FRTB IMA Expected Shortfall (External)'
    _INPUT_PATH_FIELD_NAME = 'External Data'
    _INPUT_PATH_VARIABLE = 'IMAESValuations'
    _INPUT_IS_PATH = True
    
    def _updateRequest(self, request_element):
        CommonCalculation._updateRequest(self, request_element=request_element)
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Scenario Data', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=""
        )
        return
        
class CommonIMASESCalculation(CommonCalculation):
    TYPE = 'IMA SES'
    _REQUEST_NAME = 'FRTB IMA Non-modellable Risk Factors (External)'
    _INPUT_PATH_FIELD_NAME = 'External Data'
    _INPUT_PATH_VARIABLE = 'IMASESValuations'
    _INPUT_IS_PATH = True
    
    def _updateRequest(self, request_element):
        CommonCalculation._updateRequest(self, request_element=request_element)
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Factor Grouping Data', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=""
        )
        return

class CommonIMADRCCalculation(CommonCalculation):
    TYPE = 'IMA DRC'
    _REQUEST_NAME = 'FRTB IMA Default Risk Charge (External)'
    _INPUT_PATH_FIELD_NAME = 'IMA DRC Deals'
    _INPUT_PATH_VARIABLE = 'IMADRCDeals'
    _INPUT_IS_PATH = True
    
    def _updateRequest(self, request_element):
        CommonCalculation._updateRequest(self, request_element=request_element)
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Factor Grouping Data', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Market Data', value=self._dictionary['MarketData'].AsString()
        )
        return

class CommonIMAHypotheticalPLCalculation(CommonCalculation):
    TYPE = 'IMA Hypothetical_PL'
    _REQUEST_NAME = 'FRTB IMA P&L (External)'
    _INPUT_PATH_FIELD_NAME = 'P&L Data'
    _SOURCE = 'Hypothetical'
    _INPUT_PATH_VARIABLE = 'IMAHypotheticalPL'
    _INPUT_IS_PATH = True
    
    def _updateRequest(self, request_element):
        CommonCalculation._updateRequest(self, request_element=request_element)
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='PL Source', value=self._SOURCE
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=""
        )
        return

class CommonIMARiskTheoreticalPLCalculation(CommonIMAHypotheticalPLCalculation):
    TYPE = 'IMA Risk_Theoretical_PL'
    _SOURCE = 'RiskTheoretical'
    _INPUT_PATH_VARIABLE = 'IMARiskTheoPL'
    _INPUT_IS_PATH = True

class CommonIMAPLAttributionCalculation(CommonCalculation):
    TYPE = 'IMA PL_Attribution'
    _REQUEST_NAME = 'FRTB IMA P&L Attribution'
    _INPUT_PATH_FIELD_NAME = 'P&L Attribution Files'
    _INPUT_IS_PATH = True

class CommonFRTBAllCalculation(CommonCalculation):
    TYPE = 'FRTB All'
    _REQUEST_NAME = 'FRTB All (External)'
    
    def _updateRequest(self, request_element):
        #SA
        addDateStr = ''
        if self.appendDate:
            addDateStr = '\\' + str(self.ref_date)
    
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='SA SBA External Sensitivities', value=self._dictionary['SASBASensitivities'].AsString() + addDateStr + '\*.csv'
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='SA DRC External Trade Data', value=self._dictionary['SADRCDeals'].AsString() +  addDateStr + '\*.csv'
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='SA RRAO External Trade Data', value=self._dictionary['SARRAODeals'].AsString() + addDateStr +'\*.csv'
        )
        #IMA
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='IMA ES External Data', value=self._dictionary['IMAESValuations'].AsString() + addDateStr +'\*.csv'
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='IMA NMRF External Data', value=self._dictionary['IMASESValuations'].AsString() + addDateStr +'\*.csv'
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='IMA DRC Deals', value=self._dictionary['IMADRCDeals'].AsString() + addDateStr + '\*.csv'
        )
        #static data
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Factor Grouping Data', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Book Tags', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Trade Tags', value=""
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Market Data', value=self._dictionary['MarketData'].AsString()
        )
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='Static Data', value=AAAttributes.FRTBATTRIBUTES['COMBINED_STATIC_DATA_PATH']
        )
        
        #Nil properties
        xmlElementTree.SubElement(
            request_element, 'Property',
            name='IMA ES Scenario Data', value=''
        )
        
        return
