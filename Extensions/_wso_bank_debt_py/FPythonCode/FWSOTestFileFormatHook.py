""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FFileFormatHook.py"
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

    TRADE_XML = """<NewDataSet>
      <RequestSQLTable>
        <Trade_ID>12345</Trade_ID>
        <ActionCode_Name>Paydown</ActionCode_Name>
        <ActionCode_Description>Paydown</ActionCode_Description>
        <Position_ID>4567</Position_ID>
        <Trade_Portfolio_ID>208</Trade_Portfolio_ID>
        <Trade_Price>100</Trade_Price>
        <Trade_Quantity>-12345.23456</Trade_Quantity>
        <Trade_Settled>-1</Trade_Settled>
        <Trade_SettleDate>2014-12-31T00:00:00+00:00</Trade_SettleDate>
        <Trade_TradeDate>2014-12-31T00:00:00+00:00</Trade_TradeDate>
        <Trader_Name />
        <CommitmentSettled>12345.54321</CommitmentSettled>
      </RequestSQLTable>
    </NewDataSet>"""
    
    def TradeXml(self):
        return self.TRADE_XML


class TestWSOFileFormatHook(unittest.TestCase):

    mocks = Mocks()

    def test_ParseXMLReconciliationDocument(self):
        import FWSOFileFormatHook
        fileHandle = mock.Mock()
        fileHandle.read.return_value = self.mocks.TradeXml()
        tradeDict = next(FWSOFileFormatHook.ParseXMLReconciliationDocument(fileHandle))
        self.assertEqual(len(tradeDict.keys()), 12)
        self.assertEqual(tradeDict['Trade_ID'], '12345')
        self.assertEqual(tradeDict['Trade_SettleDate'], '2014-12-31T00:00:00+00:00')
