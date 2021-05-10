""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FExternalValuesTrade.py"
"""
#owner:Prime-OMS
#email:FrontArena.ProductSolutions.Dev@fisglobal.com
#AMF #WSOBankDebt
"""

import unittest

import acm
from FWSOUnitTests import MockImporter

if MockImporter.IsAvailable():
    import mock


class Mocks(object):

    EXTERNAL_VALUES_ORIGINAL = {'ActionCode_IsPrincipal': '-1', 'Trade_SettleDate': '2014-12-31T00:00:00+00:00', 'Trade_Broker_ID': '0', 'ActionCode_Name': 'Paydown', 'TranAsset_AddID': 'abcdef', 'ActionCode_IsTrade': '0', 'Trade_Settled': '-1', 'TranAsset_Source_ID': '23456', 'Trader_Name': '', 'Position_ID': '4567', 'Trade_ID': '12345', 'TranAsset_Source_Type': '97', 'CommitmentSettled': '12345.54321', 'Trade_CounterCompany_ID': '0', 'Trade_Portfolio_ID': '208', 'ActionCode_Description': 'Paydown', 'Position_PositionSwapType': '0', 'TranAsset_LastChangeID': 'abcdef', 'ActionCode_ID': '54321', 'Trader_ID': '0', 'Trade_Quantity': '-12345.23456', 'Trade_TradeDate': '2014-12-31T00:00:00+00:00', 'Trade_Price': '100'}

    faAttributesDict = {
        'FA_Instrument': 0,
        'FA_Currency': 'USD',
        'FA_AcquireDay': 2,
        'FA_OptionalKey': 3,
        'FA_Premium': 4,
        'FA_Trader': 5,
        'FA_ValueDay': 6,
        'FA_TradeTime': 7,
        'FA_TradeStatus': 8,
    }
    
    def ExternalValuesOriginal(self):
        return self.EXTERNAL_VALUES_ORIGINAL
        
    def FAAttributesDict(self):
        return self.faAttributesDict


class Patches(object):

    mocks = Mocks()
    
    def CustomAttributesDict(self):
        return mock.patch('FWSOExternalValuesTrade.ExternalValuesReplacer._CustomAttributesDict', return_value=dict())
        
    def DefaultAttributesDict(self):
        return mock.patch('FWSOExternalValuesTrade.ExternalValuesReplacer._DefaultAttributesDict', return_value=self.mocks.FAAttributesDict())


class TestFWSOExternalValuesTrade(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def test_ExternalValues(self):
        from FWSOExternalValuesTrade import ExternalValues
        with self.patch.DefaultAttributesDict():
            with self.patch.CustomAttributesDict():
                modifiedEvDict = ExternalValues(self.mocks.ExternalValuesOriginal())
                self.assertEqual(modifiedEvDict['FA_Currency'], 'USD')
