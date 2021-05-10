""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationDataTypeHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationDataTypeHandler

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


class FDataTypeHandler(object):

    def __init__(self, dataTypeName):
        self._dataTypeName = dataTypeName

    def _IsBuiltInDataType(self, dataTypeName):
        return dataTypeName in ('integer', 'float', 'date', 'string')

    def IsCustomDataType(self):
        return self._dataTypeName not in ('string', 'integer', 'float')
        
    def IsNumericDataType(self):
        return self.GetDataType() not in ('string', 'date')

    def _GetTypeSpecification(self):
        typeSpecValue = None
        typeSpecification = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self._dataTypeName)
        if typeSpecification:
            typeSpecValue = typeSpecification.Value()
        return typeSpecValue

    def GetDataType(self):
        dataTypeName = self._dataTypeName
        if not self._IsBuiltInDataType(self._dataTypeName):
            dataTypeName = self._GetAttributeValue('data_type')
            if not self._IsBuiltInDataType(dataTypeName):
                msg = "Specified data type '%s' of base type '%s' is not supported." % (self._dataTypeName, dataTypeName)
                logger.error(msg)
                raise TypeError(msg)
        return dataTypeName

    def _GetAttributeValue(self, attributeName):
        attributeValue = None
        typeSpec = self._GetTypeSpecification()
        if typeSpec:
            attributeValue = typeSpec.At(attributeName)
        if attributeValue:
            attributeValue = str(attributeValue)
        return attributeValue

    def ThousandSeparator(self):
        return self._GetAttributeValue('thousand_separator')

    def DateFormat(self):
        return self._GetAttributeValue('date_format')

    def DecimalSign(self):
        return self._GetAttributeValue('decimal_sign')

    def SignificatDecimals(self):
        return self._GetAttributeValue('significant_decimals')

    def ThresholdAbsolute(self):
        return self._GetAttributeValue('threshold_absolute')

    def ThresholdPercentage(self):
        return self._GetAttributeValue('threshold_percentage')


