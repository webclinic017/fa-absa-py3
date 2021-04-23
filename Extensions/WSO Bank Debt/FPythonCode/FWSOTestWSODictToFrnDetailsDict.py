""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FWSODictToFrnDetailsDict.py"
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

    CONTRACTS_DICT_MOCK = {
        '23456': {
            'Contract_ID': '23456',
            'Contract_Facility_ID': '123',
        },
        '23457': {
            'Contract_ID': '23457',
            'Contract_Facility_ID': '123',
        },
        '23458': {
            'Contract_ID': '23458',
            'Contract_Facility_ID': '124',
        }
    }

    CONTRACT_DETAILS_DICT_MOCK = {
        '567': {
            'Contract_MaturityDate': '2015-02-23T00:00:00+00:00',
            'ContractIPF_ID': '567',
            'Contract_ID': '23456',
            'ContractIPF_DateFrom': '2014-11-22T00:00:00+00:00',
            'ContractIPF_DateTo': '2015-01-22T00:00:00+00:00',
            'ContractIPF_Amount': '1000.0',
            'ContractIPF_Spread': '0.05',
        },
        '568': {
            'Contract_MaturityDate': '2015-02-23T00:00:00+00:00',
            'ContractIPF_ID': '568',
            'Contract_ID': '23456',
            'ContractIPF_DateFrom': '2015-01-22T00:00:00+00:00',
            'ContractIPF_DateTo': '2015-02-23T00:00:00+00:00',
            'ContractIPF_Amount': '3000.0',
            'ContractIPF_Spread': '0.05',
        }
    }

    CORRECT_FRN_DETAILS_IPF_DICT = {
        '568': {
            'ContractIPF_ID_1': {
                'NominalFactor': 1.0, 
                'StartDate': '2015-01-22', 
                'EndDate': '2015-02-23', 
                'PayDate': '2015-02-23', 
                'Spread': 0.050000000000000003, 
                'CashFlowType': 'Float Rate',
            }
        }, 
        '567': {
            'ContractIPF_ID_1': {
                'NominalFactor': 1.0, 
                'StartDate': '2014-11-22', 
                'EndDate': '2015-01-22', 
                'PayDate': '2015-02-23', 
                'Spread': 0.050000000000000003, 
                'CashFlowType': 'Float Rate',
            }
        },
    }

    CONTRACT_DICT_MOCK = CONTRACTS_DICT_MOCK.get('23456')

    CONTRACTID_CONTRACTDETAILS_DICTS = {'23457': {}, '23456': {'568': {'ContractIPF_DateFrom': '2015-01-22T00:00:00+00:00', 'ContractIPF_ID': '568', 'Contract_ID': '23456', 'ContractIPF_DateTo': '2015-02-23T00:00:00+00:00'}, '567': {'ContractIPF_DateFrom': '2014-11-22T00:00:00+00:00', 'ContractIPF_ID': '567', 'Contract_ID': '23456', 'ContractIPF_DateTo': '2015-01-22T00:00:00+00:00'}}}
    
    def ContractsDict(self):
        return self.CONTRACTS_DICT_MOCK
        
    def ContractDetailsDict(self):
        return self.CONTRACT_DETAILS_DICT_MOCK

    def ContractIdContractDetailsDicts(self):
        return self.CONTRACTID_CONTRACTDETAILS_DICTS
        
    def FrnDetailsIpfDict(self):
        return self.CORRECT_FRN_DETAILS_IPF_DICT
        
    def ContractDict(self):
        return self.CONTRACTS_DICT_MOCK.get('23456')


class Patches(object):

    mocks = Mocks()
    
    def ContractsDict(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.Contract', return_value=self.mocks.ContractsDict())
    
    def ContractDetailsDict(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.ContractDetail', return_value=self.mocks.ContractDetailsDict())


class TestWSODictToFrnDetailsDict(unittest.TestCase):
    
    mocks = Mocks()
    patch = Patches()
    
    def test_ConstructFrnDetailsIPFDictionary(self):
        from FWSODictToFrnDetailsDict import WsoDictToFrnDetailsDict
        frnDetailsIPFDictExpected = self.mocks.FrnDetailsIpfDict()
        with self.patch.ContractsDict():
            with self.patch.ContractDetailsDict():
                wsoDictToFrnDetailsDict = WsoDictToFrnDetailsDict(self.mocks.ContractDict())
                frnDetailsIPFDict = wsoDictToFrnDetailsDict.FrnDetailsDict()
                self.assertEqual(frnDetailsIPFDict['567'].get('ContractIPF_ID_1').get('NominalFactor'), 1.0)
                self.assertEqual(frnDetailsIPFDict['567'], frnDetailsIPFDictExpected['567'])
                self.assertEqual(frnDetailsIPFDict['568'], frnDetailsIPFDictExpected['568'])


class TestContractIdContractDetailIPFDictsCreator(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def setUp(self):
        from FWSODictToFrnDetailsDict import ContractIdContractDetailIPFDictsCreator
        self.creator = ContractIdContractDetailIPFDictsCreator(self.mocks.ContractDict())

    def test_ContractDetailIdsFromContractId(self):
        with self.patch.ContractDetailsDict():
            contractDetailIds = self.creator._ContractDetailIdsFromContractId(self.mocks.ContractDict())
        self.assertEqual(len(contractDetailIds), 2)
        self.assertTrue('567' in contractDetailIds, 'Contract details is missing.')
        self.assertTrue('568' in contractDetailIds, 'Contract details is missing.')
            
    def test_GetContractDetailDictsFromIds(self):
        contractDetailIds = ['567', '568',]
        with self.patch.ContractDetailsDict():
            contractDetailDicts = self.creator._GetContractDetailDictsFromIds(contractDetailIds)
        self.assertEqual(len(contractDetailDicts), 2)
        self.assertEqual(contractDetailDicts['567']['ContractIPF_ID'], '567')
        self.assertEqual(contractDetailDicts['568']['ContractIPF_ID'], '568')

    def test_GetContractIdContractDetailDictsFromContract(self):
        with self.patch.ContractsDict():
            with self.patch.ContractDetailsDict():
                contractIdContractDetailDicts = self.creator._ContractIdContractDetailDicts()
        contractIds = contractIdContractDetailDicts.keys()
        self.assertEqual(len(contractIds), 2)
        self.assertTrue('23456' in contractIds)
        self.assertTrue('23457' in contractIds)
        self.assertTrue('23458' not in contractIds)
        contractDetailDicts = contractIdContractDetailDicts.values()
        self.assertTrue('567' in contractIdContractDetailDicts['23456'].keys())
        self.assertTrue('568' in contractIdContractDetailDicts['23456'].keys())
    


class TestIPFPeriods(unittest.TestCase):

    mocks = Mocks()

    def test_GetIPFPeriods(self):
        from FWSODictToFrnDetailsDict import IPFPeriods
        contractIdContractDetailsDicts = self.mocks.ContractIdContractDetailsDicts()
        periods = IPFPeriods(contractIdContractDetailsDicts).GetPeriods()
        self.assertEqual(periods[0], ['2014-11-22', '2015-01-22'])
        self.assertEqual(periods[1], ['2015-01-22', '2015-02-23'])
