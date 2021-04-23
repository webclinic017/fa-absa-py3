""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FWSODictToTradeDict.py"
"""
#owner:Prime-OMS
#email:FrontArena.ProductSolutions.Dev@fisglobal.com
#AMF #WSOBankDebt
"""

import unittest

from FWSOUnitTests import MockImporter

if MockImporter.IsAvailable():
    import mock


class Mocks(object):
    
    EXTERNAL_VALUES = {
        'Trade_SettleDate': '2014-12-31T00:00:00+00:00',
        'Trade_Settled': '-1',
        'Position_ID': '4567',
        'Trade_ID': '12345',
        'Trade_Portfolio_ID': '208',
        'Trade_Quantity': '-12345.23456',
        'Trade_Price': '100'
    }

    ASSET_BASE = {
        '12345': {
            'Asset_Name': 'Dummy Asset Name',
            'CurrencyType_Identifier': 'EUR',
        },
    }

    FACILITY = {
        '5678': {'Facility_Asset_ID': '12345'}
    }

    POSITION = {
        '4567':{
            'Position_Asset_ID':'12345'
        }
    }
    
    def AssetId(self):
        return '12345'
        
    def AssetBase(self):
        return self.ASSET_BASE
        
    def AssetDict(self):
        return self.AssetBase().get(self.AssetId())
    
    def CombinationName(self):
        return mock.sentinel.CombinationName
    
    def ExternalValuesDict(self):
        return self.EXTERNAL_VALUES
        
    def Facility(self):
        return self.FACILITY
        
    def FacilityDict(self):
        return self.Facility().get('5678')
        
    def Position(self):
        return self.POSITION


class Patches(object):

    mocks = Mocks()
    
    def AssetId(self):
        return mock.patch('FWSODictToTradeDict.WsoDictToTradeDict._AssetId', return_value=self.mocks.AssetId())
    
    def AssetBase(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.AssetBase', return_value=self.mocks.AssetBase())

    def AssetDict(self):
        return mock.patch('FWSODictToTradeDict.WsoDictToTradeDict._AssetDict', return_value=self.mocks.AssetDict())
    
    def CombinationName(self):
        return mock.patch('FWSOHooks.HookOrDefault.CombinationName', return_value=self.mocks.CombinationName())
    
    def ContractSize(self):
        return mock.patch('FWSODictToCombinationDict.WsoDictToCombinationDict.ContractSize', return_value=1.0)
    
    def FacilitiesDict(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.Facility', return_value=self.mocks.Facility())

    def FacilityDict(self):
        return mock.patch('FWSODictToTradeDict.WsoDictToTradeDict._FacilityDict', return_value=self.mocks.FacilityDict())
        
    def Position(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.Position', return_value=self.mocks.Position())
        

class TestWSODictToTradeDict(unittest.TestCase):
    
    mocks = Mocks()
    patch = Patches()
    
    def setUp(self):
        from FWSODictToTradeDict import WsoDictToTradeDict
        evDict = self.mocks.ExternalValuesDict()
        self.toTradeDict = WsoDictToTradeDict(evDict)
    
    def test_AcquireDay(self):
        self.assertEqual(self.toTradeDict.AcquireDay(), '2014-12-31')
    
    def test_AssetId(self):
        with self.patch.Position():
            self.assertEqual(self.toTradeDict._AssetId(), self.mocks.AssetId())
    
    def test_CurrencyName(self):
        currencyNameExpected = 'EUR'
        with self.patch.AssetId():
            with self.patch.AssetBase():
                self.assertEqual(self.toTradeDict.CurrencyName(), currencyNameExpected)
    
    def test_FacilityId(self):
        facilityIdExpected = '5678'
        with self.patch.AssetId():
            with self.patch.FacilitiesDict():
                self.assertEqual(self.toTradeDict._FacilityId(), facilityIdExpected)
    
    def test_Instrument(self):
        combinationNameExpected = self.mocks.CombinationName()
        with self.patch.AssetDict():
            with self.patch.CombinationName():
                self.assertEqual(self.toTradeDict.Instrument(), combinationNameExpected)
    
    def test_OptionalKey(self):
        optionalKeyExpected = 'WSO_Trade_12345'
        self.assertEqual(self.toTradeDict.OptionalKey(), optionalKeyExpected)
    
    def test_PortfolioId(self):
        portfolioIdExpected = '208'
        self.assertEqual(self.toTradeDict._PortfolioId(), portfolioIdExpected)
    
    def test_PositionId(self):
        positionIdExpected = '4567'
        self.assertEqual(self.toTradeDict._PositionId(), positionIdExpected)
    
    def test_Premium(self):
        premiumExpected = 12345.23456
        with self.patch.AssetBase():
            with self.patch.FacilityDict():
                with self.patch.ContractSize():
                    self.assertEqual(self.toTradeDict.Premium(), premiumExpected)
        
    def test_Price(self):
        priceExpected = 100.0
        self.assertEqual(self.toTradeDict._Price(), priceExpected)
        
    def test_Quantity(self):
        quantityExpected = -12345.23456
        self.assertEqual(self.toTradeDict._Quantity(), quantityExpected)
        
    def test_Trader(self):
        traderExpected = None
        self.assertEqual(self.toTradeDict.Trader(), traderExpected)
    
    def test_TradeId(self):
        tradeIdExpected = '12345'
        self.assertEqual(self.toTradeDict._TradeId(), tradeIdExpected)
        
    def test_TradeStatus(self):
        tradeStatusExpected = 'Exchange'
        self.assertEqual(self.toTradeDict.TradeStatus(), tradeStatusExpected)
    
    def test_ValueDay(self):
        valueDayExpected = '2014-12-31'
        self.assertEqual(self.toTradeDict.ValueDay(), valueDayExpected)
