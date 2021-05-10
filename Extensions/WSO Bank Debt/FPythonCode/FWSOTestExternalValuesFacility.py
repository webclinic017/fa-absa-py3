""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FExternalValuesFacility.py"
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

    EXTERNAL_VALUES_ORIGINAL = {'Asset_ID': '8765', 'Asset_IsPrivate': '0', 'CurrencyType_Name': 'Pounds Sterling', 'Asset_Country_ID': '0', 'Asset_IsPIK': '0', 'Asset_Collateralized': '0', 'Asset_AssetID_TICKER': '', 'Asset_IssueAmount': '84000000', 'Seniority_IsSecured': '0', 'Asset_RateType': '2', 'Asset_AddDate': '2015-02-17T17:12:54.357+00:00', 'Asset_DayCount2': '0', 'Asset_AssetDetail_Type_Name': 'Loan', 'Asset_AssetDetail_Type': '4', 'Asset_IsFXRisk': '0', 'Asset_InterestAccrualDate': '2014-10-01T00:00:00+01:00', 'CurrencyType_SortOrder': '3', 'Asset_IsSFO': '0', 'Asset_AssetID_LIN': '', 'Seniority_ID': '8', 'Asset_Issuer_ID': '123', 'Asset_IsGuaranteed': '0', 'Position_ID': '7654', 'Asset_AbbrevName': '2nd Lien', 'Asset_SecurityID': 'BBG54112T1L4', 'CurrencyType_ID': '3', 'Asset_AttachedWarrant': '0', 'Asset_Insurer_ID': '0', 'Seniority_Name': '2nd Lien', 'Asset_Frequency1': '4', 'Asset_AssetType_Name': 'Loan', 'Asset_RateType_Name': 'Float', 'Asset_Frequency2': '0', 'Asset_Notes': '', 'Tradar': '123456', 'LoanX': '', 'Asset_IsSynthetic': '0', 'Asset_AssetClass_Deleted': '0', 'Asset_AssetType': '1000', 'Asset_IsABS': '0', 'BBG': 'BBG11231H3L5', 'Asset_AmortizeToZero': '0', 'Asset_Name': 'Good Facility Limited 2nd Lien', 'Asset_AssetClass_ID': '0', 'Asset_DefaultType': '', 'Asset_Calendar_ID': '0', 'Asset_IsConvertible': '0', 'Asset_PayOffsetDirection': '1', 'Asset_SubType': '1', 'Asset_Deleted': '0', 'Asset_AssetDetail_ID': '4567', 'Asset_IsMostSenior': '0', 'Asset_IssueDate': '2014-10-01T00:00:00+01:00', 'Asset_MaturityDate': '2022-10-27T00:00:00+01:00', 'Asset_IsEmergingMarket': '0', 'Asset_PayOffsetDays': '0', 'Asset_ConvertibleType': '', 'Asset_UnitPrice': '1', 'Asset_IsDefaulted': '0', 'CurrencyType_Format': '#,###.00;(#,###.00);0.00;\\N\\u\\l\\l', 'Asset_Guarantor_ID': '0', 'Asset_IsRestructured': '0', 'Asset_AssetID_BBGID1': 'BBG11321H1L7', 'Asset_PriceFactor': '0.01', 'Asset_IssuePrice': '0', 'Asset_Collateral': '', 'Asset_PayOffsetType': '0', 'Seniority_Priority': '0', 'Asset_DayCount1': '2', 'CurrencyType_Identifier': 'GBP', 'Asset_LastChangeDate': '2015-02-17T17:31:16.543+00:00'}

    FA_ATTRIBUTES_DICT = {
        'New_Key': 'New Value',
    }
    
    def ExternalValuesOriginal(self):
        return self.EXTERNAL_VALUES_ORIGINAL
        
    def FAAttributesDict(self):
        return self.FA_ATTRIBUTES_DICT


class TestFWSOExternalValuesFacility(unittest.TestCase):

    mocks = Mocks()

    def _MockCustomAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._CustomAttributesDict', return_value=dict())

    def _MockDefaultAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._DefaultAttributesDict', return_value=self.mocks.FAAttributesDict())

    def test_ExistingKeyValuePair(self):
        from FWSOExternalValuesFacility import ExternalValues
        assetNameExpected = 'Good Facility Limited 2nd Lien'
        with self._MockDefaultAttributesDict():
            with self._MockCustomAttributesDict():
                evDict = ExternalValues(self.mocks.ExternalValuesOriginal())
                assetName = evDict['Asset_Name']
                self.assertEqual(assetName, assetNameExpected)
                
    def test_NewKeyValuePair(self):
        from FWSOExternalValuesFacility import ExternalValues
        newValueExpected = 'New Value'
        with self._MockDefaultAttributesDict():
            with self._MockCustomAttributesDict():
                evDict = ExternalValues(self.mocks.ExternalValuesOriginal())
                newValue = evDict['New_Key']
                self.assertEqual(newValue, newValueExpected)
