""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FWSODictAccessor.py"
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

    WSO_DICTS = {
        'Asset': {
            '12': {'Asset_Name':'Good Facility B'},
        },
        'Bank': {
            '18': {'Bank_Name': 'Fine Bank',},
        },
        'Contract': {
            '45464': {'ContractAmount': '3000000.0000',},
        },
        'ContractDetail': {
            '44777': {'ContractIPF_Spread': '0.035'}
        },
        'Facility': {
            '117': {'Facility_Name': 'Good Facility B'},
        },
        'Issuer': {
            '9': {'Issuer_AbbrevName': 'IssuersInc'},
        },
        'Portfolio': {
            '113': {'Portfolio_Name': 'Eastern Loans EUR'},
        },
        'Position': {
            '341': {'Position_Asset_ID': '14'},
        },
        'Trade': {
            '77677': {'Trade_Price':'97.875'},
        },
    }
    
    WSO_DICTS_EMPTY = dict()

    def WsoDicts(self):
        return self.WSO_DICTS

    def WsoDictsEmpty(self):
        return self.WSO_DICTS_EMPTY

    def WSODirToWSODict(self):
        mockWSODicts = mock.Mock()
        mockWSODicts.WSODicts.return_value = self.WsoDicts()
        return mockWSODicts
        
    def WSODirToWSODictEmpty(self):
        mockWSODicts = mock.Mock()
        mockWSODicts.WSODicts.return_value = self.WsoDictsEmpty()
        return mockWSODicts


class Patches(object):

    mocks = Mocks()

    def WSODirToWSODict(self):
        return mock.patch('FWSODirToWSODict.WSODirToWSODict', return_value=self.mocks.WSODirToWSODict())
        
    def WSODirToWSODictEmpty(self):
        return mock.patch('FWSODirToWSODict.WSODirToWSODict', return_value=self.mocks.WSODirToWSODictEmpty())


class TestWSODictAccessor(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def setUp(self):
        from FWSODictAccessor import WSODictAccessor
        self.accessor = WSODictAccessor()

    def test_AssetBase(self):
        assetNameExpected = 'Good Facility B'
        with self.patch.WSODirToWSODict():
            assetsDict = self.accessor.AssetBase()
            assetDict = assetsDict.get('12')
            assetName = assetDict.get('Asset_Name')
            self.assertEqual(assetName, assetNameExpected)
    
    def test_Bank(self):
        bankNameExpected = 'Fine Bank'
        with self.patch.WSODirToWSODict():
            banksDict = self.accessor.Bank()
            bankDict = banksDict.get('18')
            bankName = bankDict.get('Bank_Name')
            self.assertEqual(bankName, bankNameExpected)
            
    def test_Contract(self):
        contractAmountExpected = '3000000.0000'
        with self.patch.WSODirToWSODict():
            contractsDict = self.accessor.Contract()
            contractDict = contractsDict.get('45464')
            contractAmount = contractDict.get('ContractAmount')
            self.assertEqual(contractAmount, contractAmountExpected)
            
    def test_ContractDetail(self):
        spreadExpected = '0.035'
        with self.patch.WSODirToWSODict():
            contractDetailsDict = self.accessor.ContractDetail()
            contractDetailDict = contractDetailsDict.get('44777')
            spread = contractDetailDict.get('ContractIPF_Spread')
            self.assertEqual(spread, spreadExpected)
            
    def test_Facility(self):
        facilityNameExpected = 'Good Facility B'
        with self.patch.WSODirToWSODict():
            facilitiesDict = self.accessor.Facility()
            facilityDict = facilitiesDict.get('117')
            facilityName = facilityDict.get('Facility_Name')
            self.assertEqual(facilityName, facilityNameExpected)

    def test_Issuer(self):
        issuerNameExpected = 'IssuersInc'
        with self.patch.WSODirToWSODict():
            issuersDict = self.accessor.Issuer()
            issuerDict = issuersDict.get('9')
            issuerName = issuerDict.get('Issuer_AbbrevName')
            self.assertEqual(issuerName, issuerNameExpected)
            
    def test_Portfolio(self):
        portfolioNameExpected = 'Eastern Loans EUR'
        with self.patch.WSODirToWSODict():
            portfoliosDict = self.accessor.Portfolio()
            portfolioDict = portfoliosDict.get('113')
            portfolioName = portfolioDict.get('Portfolio_Name')
            self.assertEqual(portfolioName, portfolioNameExpected)

    def test_Position(self):
        assetIdExpected = '14'
        with self.patch.WSODirToWSODict():
            positionsDict = self.accessor.Position()
            positionDict = positionsDict.get('341')
            assetId = positionDict.get('Position_Asset_ID')
            self.assertEqual(assetId, assetIdExpected)
            
    def test_Trade(self):
        tradePriceExpected = '97.875'
        with self.patch.WSODirToWSODict():
            tradesDict = self.accessor.Trade()
            tradeDict = tradesDict.get('77677')
            tradePrice = tradeDict.get('Trade_Price')
            self.assertEqual(tradePrice, tradePriceExpected)
            
    def test_MissingDataSourceRaisesException(self):
        from FWSOUtils import MissingDataSourceException
        with self.patch.WSODirToWSODictEmpty():
            self.assertRaises(MissingDataSourceException, self.accessor.Position)
