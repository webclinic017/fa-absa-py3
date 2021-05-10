
import acm

from DealDevKit import SalesTradingInteraction

class DealSTI(SalesTradingInteraction):
    statusAttr='trade_status'
    status='FO Confirmed'
    tradeTimeAttr='trade_tradeTime'
    clientAttr='trade_counterparty' 
    acquirerAttr='trade_acquirer'
    portfolioAttr='trade_portfolio'

    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        self.SetAmountAttribute(*args)
        self.SetCustomPanes(*args)
    
    def SetAmountAttribute(self, *args):
        amountAttr = 'trade_quantity_value'
        if len(args):
            insType = args[0]
            ins = acm.DealCapturing.CreateNewInstrument(insType)
            if not SalesTradingInteraction.UseQuantity(ins, None):
                amountAttr = 'trade_nominal_value'
        self._kwargs['amountInfo'] = {'amountAttr' : amountAttr}
    
    def SetCustomPanes(self, *args):
        salesCustomPane = ''
        tradingCustomPane = ''
        if len(args):
            insType = args[0]
            salesCustomPane = 'CustomPanes_' + insType.replace("/", "") + 'Sales'
            tradingCustomPane = 'CustomPanes_' + insType.replace("/", "") + 'Trading'
        self._kwargs['salesCustomPane'] = salesCustomPane
        self._kwargs['tradingCustomPane'] = tradingCustomPane
