""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FWSOFile.py"
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

    TRADE_XML = '''
    <NewDataSet>
      <RequestSQLTable>
        <Trade_ID>23753</Trade_ID>
        <Trade_Price>98.25</Trade_Price>
        <Trade_Quantity>12718125</Trade_Quantity>
        <Trade_TradeDate>2014-12-31T00:00:00+00:00</Trade_TradeDate>
      </RequestSQLTable>
    </NewDataSet>
    '''
    
    TRADE_DICT = {
        'Trade_Quantity': '12718125',
        'Trade_ID': '23753',
        'Trade_TradeDate': '2014-12-31T00:00:00+00:00',
        'Trade_Price': '98.25'
    }
    
    def TradeXml(self):
        return self.TRADE_XML
        
    def FileHandle(self):
        fileHandle = mock.Mock()
        fileHandle.read.return_value = self.TradeXml()
        return fileHandle
        
    def TradeDict(self):
        return self.TRADE_DICT
        
        
class Patches(object):

    mocks = Mocks()
    
    def Open(self):
        return mock.patch('__builtin__.open', return_value = self.mocks.FileHandle())


class TestWSOFile(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()

    def test_WsoDict(self):
        tradeIdExpected = '23753'
        tradeDictExpected = self.mocks.TradeDict()
        filePath = r'C:\temp\some_path.xml'
        primaryKeyName = 'Trade_ID'
        from FWSOFile import WSOFile
        with self.patch.Open():
            wsoFile = WSOFile(filePath, primaryKeyName)
            wsoDict = wsoFile.WsoDict()
        tradeIds = list(wsoDict.keys())
        tradeDict = wsoDict.get(tradeIdExpected)
        self.assertEqual(tradeIds, [tradeIdExpected,])
        self.assertEqual(tradeDict, tradeDictExpected)
