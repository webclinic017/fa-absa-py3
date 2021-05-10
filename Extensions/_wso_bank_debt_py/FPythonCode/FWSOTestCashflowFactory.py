""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FCashflowFactory.py"
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

    MOCK_IPF_DICT = {
        'CashFlowType': 'Float Rate',
        'StartDate': '2015-01-01',
        'EndDate': '2015-03-31',
        'PayDate': '2015-03-31',
        'Spread': 0.05,
        'NominalFactor': 1,
    }
    
    def Cashflow(self):
        return mock.Mock(return_value=mock.sentinel.Cashflow)
    
    def Frn(self):
        frn = mock.Mock()
        frn.NominalAmount.return_value = 0.5
        return frn
    
    def IpfDict(self):
        return self.MOCK_IPF_DICT
    
    def IpfDictAsMock(self):
        return mock.Mock()
    

class Patches(object):

    mocks = Mocks()
    
    def CreateCashflowFromIpfDict(self, cashflow=None):
        cashflow = self.mocks.Cashflow() if not cashflow else cashflow
        return mock.patch('FWSOCashflowFactory.CashflowFactory._CreateCashflowFromIpfDict', return_value = cashflow)
        

class TestCashflowFactory(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def setUp(self):
        from FWSOCashflowFactory import CashflowFactory
        self.factory = CashflowFactory(self.mocks.Frn(), self.mocks.IpfDictAsMock())
        self.factory.ipfDict = self.mocks.IpfDict()
        self.factory.frn = self.mocks.Frn()
    
    def test_IpfDictAttributes(self):
        self.assertEqual(self.factory.ipfDict.get('CashFlowType'), 'Float Rate')

    def test_Spread(self):
        ipfSpreadExpected = 0.05
        spreadExpected = 5.0
        self.assertEqual(self.factory.ipfDict.get('Spread'), ipfSpreadExpected)
        self.assertEqual(self.factory._Spread(), spreadExpected)
            
    def test_NominalFactor(self):
        nominalFactorExpected = 1.0
        self.assertEqual(self.factory.ipfDict.get('NominalFactor'), nominalFactorExpected)

    def test_Create(self):
        cashflow = self.mocks.Cashflow()
        with self.patch.CreateCashflowFromIpfDict(cashflow):
            createdCashflow = self.factory.Create()
            self.assertEqual(createdCashflow, cashflow)
            self.assertTrue(self.factory._CreateCashflowFromIpfDict)
