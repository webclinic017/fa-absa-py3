""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSODictToTradeDict.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODictToTradeDict - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Responsible for transforming WSO formatted trade dictionary to a Front Arena adapted trade dictionary.
    
-------------------------------------------------------------------------------------------------------"""

from FWSOUtils import WSOUtils as utils
from FWSOUtils import MissingPositionException, WsoLogger
import FWSOHooks as WSOHooks
from FWSODictAccessor import WSODictAccessor

logger = WsoLogger.GetLogger()


class WsoDictToTradeDict(object):

    def __init__(self, tradeDict):
        self.tradeDict = tradeDict 

    def _AssetId(self):
        return self._PositionAttribute('Position_Asset_ID')

    def _AssetAttribute(self, attribute):
        assetId = self._AssetId()
        assetsDict = WSODictAccessor.AssetBase()
        assetDict = assetsDict.get(assetId)
        value = assetDict.get(attribute)
        return value

    def _AssetDict(self):
        assetId = self._AssetId()
        assetsDict = WSODictAccessor.AssetBase()
        assetDict = assetsDict.get(assetId)
        return assetDict
    
    def _ContractSize(self):
        return 1.0
    
    def _CurrencyNameOrNone(self):
        currencyName = None
        try:
            currencyName = self._AssetAttribute('CurrencyType_Identifier')
        except MissingPositionException:
            logger.warn('Missing position: Currency is set to None.')
        return currencyName
    
    def _FacilityDict(self):
        facilitiesDict = WSODictAccessor.Facility()
        facilityId = self._FacilityId()
        facilityDict = facilitiesDict.get(facilityId)
        return facilityDict
    
    def _FacilityId(self):
        assetId = self._AssetId()
        wsoFacilitiesDict = WSODictAccessor.Facility()
        for facilityId, facilityDict in list(wsoFacilitiesDict.items()):
            if facilityDict.get('Facility_Asset_ID') != assetId:
                continue
            return facilityId
    
    def _GetWSOTradePrefix(self):
        return 'WSO_Trade_'
    
    def _InstrumentOrNone(self):
        instrumentName = None
        try:
            assetDict = self._AssetDict()
            instrumentName = WSOHooks.HookOrDefault.CombinationName(assetDict)
        except MissingPositionException:
            logger.warn('Missing position: Instrument is set to None.')
        return instrumentName
    
    def _PortfolioAttribute(self, attribute):
        wsoPortfolioDict = self._PortfolioDict()
        value = wsoPortfolioDict.get(attribute)
        return value
    
    def _PortfolioDict(self):
        portfolioId = self._TradeAttribute('Trade_Portfolio_ID')
        wsoPortfoliosDict = WSODictAccessor.Portfolio()
        wsoPortfolioDict = wsoPortfoliosDict.get(portfolioId)
        return wsoPortfolioDict
    
    def _PortfolioId(self):
        return self._TradeAttribute('Trade_Portfolio_ID')
    
    def _PositionAttribute(self, attribute):
        positionId = self._PositionId()
        wsoPositionsDict = WSODictAccessor.Position()
        wsoPositionDict = wsoPositionsDict.get(positionId)
        if not wsoPositionDict:
            logger.warn('Position with Position_ID %s not found in WSO Position XML.' % positionId)
            raise MissingPositionException('Position with Position_ID %s not found in WSO Position XML.' % positionId)
        value = wsoPositionDict.get(attribute)
        return value
    
    def _PositionId(self):
        return self._TradeAttribute('Position_ID')
        
    def _Price(self):
        return utils.AsFloat(self._TradeAttribute('Trade_Price'))
    
    def _Quantity(self):
        return utils.AsFloat(self._TradeAttribute('Trade_Quantity'))
    
    def _TradeAttribute(self, attribute):
        return self.tradeDict.get(attribute)

    def _TradeId(self):
        return self._TradeAttribute('Trade_ID')

    def _TradeSettled(self):
        return self._TradeAttribute('Trade_Settled') == '-1'

    # Public methods

    def AcquireDay(self):
        return utils.AsDate(self._TradeAttribute('Trade_SettleDate'))

    def CurrencyName(self):
        return self._CurrencyNameOrNone()

    def Instrument(self):
        return self._InstrumentOrNone()

    def OptionalKey(self):
        return self._GetWSOTradePrefix() + self._TradeId()
    
    def Premium(self):
        premiumNotScaled = -self._Quantity()*self._Price()*self._ContractSize()
        return premiumNotScaled/100.0 # Positive (negative) premium for sell (buy) trade

    def Trader(self):
        return None
    
    def TradeStatus(self):
        return 'Exchange' if self._TradeSettled() else 'Reserved'
    
    def TradeTime(self):
        return utils.AsDate(self._TradeAttribute('Trade_TradeDate'))
        
    def ValueDay(self):
        return utils.AsDate(self._TradeAttribute('Trade_SettleDate'))
