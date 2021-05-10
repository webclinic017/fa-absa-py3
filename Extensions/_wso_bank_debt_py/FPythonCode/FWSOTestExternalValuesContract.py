""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FExternalValuesContract.py"
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

    EXTERNAL_VALUES_ORIGINAL = {'Contract_Facility_ID': '1234', 'Contract_CurrencyType_ID': '48', 'Contract_MaturityDate': '2015-03-17T00:00:00+00:00', 'Contract_Issuer_ID': '323', 'Contract_CurrentIP_ID': '56789', 'Contract_CurrencyType_Identifier': 'EUR', 'Contract_BankDeal_ID': '456', 'Contract_LastChangeID': 'nilnil', 'Contract_CurrencyType_Name': 'Euro', 'Contract_GlobalAmount': '263583236.3800', 'Contract_Frequency': '12', 'Position_ID': '7878', 'ContractTypeDescription': 'Term Funded', 'Contract_Active': '-1', 'Contract_Account_ID': '4567', 'Contract_ID': '56789', 'Contract_LastChangeDate': '2015-02-17T17:42:14.977+00:00', 'Contract_AllInRate': '0.04502', 'Contract_MonthCount_ID': '1', 'Contract_Contract': '', 'Contract_AddID': 'nilnil', 'YearCountName': '360', 'Contract_ExchangeRate': '1', 'Contract_AddDate': '2015-02-17T17:41:24.457+00:00', 'Contract_FacilityOption_ID': '4545', 'Contract_Received': '0', 'Contract_Notes': '', 'Contract_Spread': '0.045', 'Contract_ContractID': '67891', 'Contract_NextPaymentDate': '2015-03-17T00:00:00+00:00', 'Contract_BaseRate': '2E-05', 'Contract_FacilityOption_Name': 'EURIBOR', 'Contract_YearCount_ID': '2', 'Contract_Portfolio_ID': '233', 'MonthCountName': 'ACT', 'Contract_InterestDue': '1692.2466', 'Contract_StartDate': '2015-02-17T00:00:00+00:00', 'Contract_Amount': '483284.2420', 'ContractBehaviorDescription': 'LIBOR', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1'}

    FA_ATTRIBUTES_DICT = {
        'New_Key': 'New Value',
    }
    
    def ExternalValuesOriginal(self):
        return self.EXTERNAL_VALUES_ORIGINAL
        
    def FAAttributesDict(self):
        return self.FA_ATTRIBUTES_DICT


class Patches(object):

    mocks = Mocks()
    
    def CustomAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._CustomAttributesDict', return_value=dict())
        
    def DefaultAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._DefaultAttributesDict', return_value=self.mocks.FAAttributesDict())

class TestFWSOExternalValuesContract(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def _MockCustomAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._CustomAttributesDict', return_value=dict())

    def _MockDefaultAttributesDict(self):
        return mock.patch('FWSOExternalValuesFacility.ExternalValuesReplacer._DefaultAttributesDict', return_value=self.mocks.FAAttributesDict())

    def test_ExistingKeyValuePair(self):
        from FWSOExternalValuesFacility import ExternalValues
        contractIdExpected = '56789'
        with self._MockDefaultAttributesDict():
            with self._MockCustomAttributesDict():
                evDict = ExternalValues(self.mocks.ExternalValuesOriginal())
                contractId = evDict['Contract_ID']
                self.assertEqual(contractId, contractIdExpected)
                
    def test_NewKeyValuePair(self):
        from FWSOExternalValuesFacility import ExternalValues
        newValueExpected = 'New Value'
        with self._MockDefaultAttributesDict():
            with self._MockCustomAttributesDict():
                evDict = ExternalValues(self.mocks.ExternalValuesOriginal())
                newValue = evDict['New_Key']
                self.assertEqual(newValue, newValueExpected)
