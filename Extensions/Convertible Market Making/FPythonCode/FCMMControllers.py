""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ConvertibleMarketMaking/etc/FCMMControllers.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCMMControllers

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FUxCore
from FCMMDeltaNuke import UpdateFallbackDelta
from FCMMSaveNukeParameters import SaveNukeParameters, \
                                   RebaseDeltaNuke, \
                                   TickBasePrices, \
                                   TickProposedQuotePrice
import FAssetManagementUtils

logger = FAssetManagementUtils.logger


class MenuItem(FUxCore.MenuItem):

    def __init__(self, extObj):
        self._app = extObj

    def IsQuoteSheetFrame(self):
        if self._app.ActiveSheet():
            return self._app.ActiveSheet().SheetClass().IsEqual(acm.FQuoteSheet)

    def Invoke(self, eii):
        raise NotImplementedError

class SaveNukeParametersMenuItem(MenuItem):

    def __init__(self, extObj):
        MenuItem.__init__(self, extObj)

    def Applicable(self):
        return self.IsQuoteSheetFrame()

    def Invoke(self, eii):
        try:
            SaveNukeParameters(eii)
        except Exception as e:
            logger.error("Failed to save nuke parameters.\nReason: %s" % str(e))

class TriggerDeltaCalibrationMenuItem(MenuItem):

    def __init__(self, extObj):
        MenuItem.__init__(self, extObj)

    def Applicable(self):
        return self.IsQuoteSheetFrame()

    def Invoke(self, eii):
        UpdateFallbackDelta(FAssetManagementUtils.GetInstruments(eii))

def CreateSaveNukeParametersMenuItem(eii):
    return SaveNukeParametersMenuItem(eii)

def CreateTriggerDeltaCalibrationMenuItem(eii):
    return TriggerDeltaCalibrationMenuItem(eii)

#Support for "Base" button in Market Making View
def showSaveButton(eii):
    cell = eii.Parameter("Cell")
    if cell:
        try:
            rowObject = cell.RowObject()
            if rowObject.IsKindOf('FQuoteLevelRow'):
                return '1' == rowObject.StringKey()
        except:
            pass
    return False
    
def showTickButton(eii):
    cell = eii.Parameter("Cell")
    if cell:
        try:
            rowObject = cell.RowObject()
            if rowObject.IsKindOf('FQuoteLevelRow'):
                return '1' == rowObject.StringKey()
        except:
            pass
    return False    
    
def onTickUp(eii):
    try:
        TickBasePrices(eii, True)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))

def onTickDown(eii):
    try:
        TickBasePrices(eii, False)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))
        
def onTickProposedBidQuoteUp(eii):
    quoteSide = 'Bid'
    try:
        TickProposedQuotePrice(eii, quoteSide, True)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))
        
def onTickProposedBidQuoteDown(eii):
    quoteSide = 'Bid'
    try:
        TickProposedQuotePrice(eii, quoteSide, False)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))        

def onTickProposedAskQuoteUp(eii):
    quoteSide = 'Ask'
    try:
        TickProposedQuotePrice(eii, quoteSide, True)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))

def onTickProposedAskQuoteDown(eii):
    quoteSide = 'Ask'
    try:
        TickProposedQuotePrice(eii, quoteSide, False)
    except Exception as e:
        logger.error('Tick failed. \nReason: %s' % str(e))    

def nukeRebase(eii):
    try:
        RebaseDeltaNuke(eii)
    except Exception as e:
        logger.error("Rebase failed.\nReason: %s" % str(e))
