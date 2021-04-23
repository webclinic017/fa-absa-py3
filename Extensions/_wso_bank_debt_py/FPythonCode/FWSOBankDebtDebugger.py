""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOBankDebtDebugger.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOBankDebtDebugger -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils


from FWSOUpload import RunUploadBasedOnParams
logger = FAssetManagementUtils.GetLogger()
        

class WSOBankDebtDebugger(object):

    def __init__(self):
        raise NotImplementedError
        
    def _BoolAsDate(self, dateString):
        import datetime
        try:
            datetime.datetime.strptime(dateString, '%Y-%m-%d')
        except ValueError:
            logger.error("Incorrect data format. Format should be in the form YYYY-MM-DD.")
            return False
        return True
            
    def _ReconSpecInADS(self, reconSpec):
        # We assume that the specification exists not only as an extension
        exts = acm.GetDefaultContext().GetAllExtensions('FParameters')
        for ext in reversed(exts):
            extName = str(ext.Value().Name())
            if extName == reconSpec:
                return True
        return False
        
    def _ConstructDictionaryFromAelVariables(self, **kwargs):
        import FWSOUploadDialog 
        
        paramsDict = dict()
        # First sweep: Look for candidate values from optional input dictionary   
        for itemKey, itemValue in kwargs.items():
            if itemKey == 'ReconciliationSpecification' and self._ReconSpecInADS(itemValue):
                value = itemValue
            elif itemKey == 'DisplayOption' and itemValue in ("0", "1",):
                value = itemValue              
            elif itemKey == 'CustomStartDate' and self._BoolAsDate(itemValue):
                value = itemValue
            elif itemKey == 'CustomEndDate' and self._BoolAsDate(itemValue):
                value = itemValue
            elif itemKey == 'StartDate' and self._BoolAsDate(itemValue):
                value = itemValue
            elif itemKey == 'EndDate' and self._BoolAsDate(itemValue):
                value = itemValue
            elif itemKey == 'ForceReRun' and itemValue in ("0", "1",):
                value = itemValue
            elif itemKey == 'LogLevel' and itemValue in ('1. Normal', '2. Warning/Error', '3. Debug',):
                value = itemValue
            else:
                continue
            paramsDict[itemKey] = value 
        
        reconSpecKey = 'ReconciliationSpecification'
        reconSpecValue = kwargs.get(reconSpecKey)
        if not reconSpecValue:
            reconSpecValue = 'WSO Upload Facility Template' 
            
        # Second sweep: Use default values for non-specified input key-value pairs
        ael_variables = FWSOUploadDialog.WSOUploadDialog(reconSpecValue)
        for i in range(len(ael_variables)):
            itemKey = ael_variables[i][0]
            if itemKey == 'ReconciliationSpecification' and itemKey not in paramsDict:
                itemValue = reconSpecValue
            elif itemKey == 'DisplayOption' and itemKey not in paramsDict:
                itemValue = "0"                
            elif itemKey == 'CustomStartDate' and itemKey not in paramsDict:
                itemValue = ''
            elif itemKey == 'CustomEndDate' and itemKey not in paramsDict:
                itemValue = ''
            elif itemKey == 'StartDate' and itemKey not in paramsDict:
                itemValue = 'Inception'
            elif itemKey == 'EndDate' and itemKey not in paramsDict:
                itemValue = 'Now'
            elif itemKey == 'ForceReRun' and itemKey not in paramsDict:
                itemValue = "1"
            elif itemKey == 'LogLevel' and itemKey not in paramsDict:
                itemValue = '1. Normal'
            else:
                logger.error('Ael variable key %s could not be identified.' % itemKey)
                continue
            paramsDict[itemKey] = itemValue 
            
        return paramsDict
 
    def RunDebugger(self):
        raise NotImplementedError('The method %s has no implementation in class %s' %('RunDebugger', self.__class__.__name__))


class WSODataUploaderDebugger(WSOBankDebtDebugger):

    def __init__(self, **kwargs):
        # pylint: disable-msg=W0231
        self.params = self._ConstructDictionaryFromAelVariables(**kwargs)

    def RunDebugger(self):
        RunUploadBasedOnParams(self.params)
        
def main(**kwargs):
    debugger = WSODataUploaderDebugger(**kwargs)
    debugger.RunDebugger()