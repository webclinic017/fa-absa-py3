""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ConvertibleMarketMaking/etc/FCMMDeltaNuke.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCMMDeltaNuke

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils
from FDeltaNukeUtils import DeltaNukeUtils, SaveDeltaNukeParametersPrice, \
                            ConversionRatioAdjustment, ConvertibleIsUnexpired

logger  = FAssetManagementUtils.logger


def UpdateFallbackDelta(convertibles):
    DeltaNukeCalibrationHandler.Calibrate(convertibles)


class DeltaNukeCalibrationHandler(object):
    
    @classmethod
    def MonisInCurrentContext(cls):
        return bool(cls.MonisDeltaCalibHandler())
        
    @classmethod        
    def MonisDeltaCalibHandler(cls):
        handler = None
        try:
            from FMonisUpdateFallbackNukeDelta import UpdateFallbackMonisNukeDeltaAndConversionRatio as handler
        except ImportError:
            logger.debug('Could not import Monis fallback delta calibration')
        return handler
        
    @classmethod        
    def UpdateFallbackNukeDeltaAndConversionRatio(cls, convertibles):
        data = []
        for convertible in convertibles:
            if ConvertibleIsUnexpired(convertible):
                delta = cls.ReturnDeltaFromFA(convertible)
                data.append([DeltaNukeUtils.FALLBACK_DELTA, convertible, delta])
        SaveDeltaNukeParametersPrice(data)
          
    @classmethod      
    def ReturnDeltaFromFA(cls, convertible):
        logger.debug('Processing convertible %s' % convertible.Name())
        deltaColumnId = 'CB Delta Normalized'
        calcSpace = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
        try:
            updatedDelta = calcSpace.CalculateValue(convertible, deltaColumnId).Value().Number()
        except RuntimeError as e:
            logger.error('Failed to calculate delta in Front Arena. Reason: %s' % str(e))
            return
        return updatedDelta * ConversionRatioAdjustment(convertible)
        
    @classmethod
    def GetDeltaCalibrationFunctionHandler(cls):
        handler = cls.UpdateFallbackNukeDeltaAndConversionRatio if not cls.MonisInCurrentContext() else cls.MonisDeltaCalibHandler()
        return handler        
        
    @classmethod
    def Calibrate(cls, convertibles):        
        deltaCalibrationHandler = cls.GetDeltaCalibrationFunctionHandler()
        try:              
            deltaCalibrationHandler(convertibles)
        except Exception as e:
            logger.error('Update of fallback delta failed. Reason: %s' % str(e))