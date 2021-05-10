import acm
from DealPackageDevKit import CalcVal

from DealPackageTradeActionCloseBase import TradeActionCloseBase

class TradeActionClose(TradeActionCloseBase):
    pv             = CalcVal(    label='Current PV',
                                 calcMapping='CloseDealPackageAsPortfolio:FPortfolioSheet:Portfolio Present Value',
                                 enabled=False)
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_TradeActionClose')
    
    def OnSave(self, config):
        super(TradeActionClose, self).OnSave(config)
        acm.DealPackageActions.CloseDealPackageTrades(self.OrigDealPackage(), self.CloseDealPackage())
    
    def OpenAfterSave(self, config):
        return self.CloseDealPackage()
    
    def CloseEventType(self):
        return 'Close'
    
    def ClosingNominalLabel(self, *args):
        return 'Closing Nominal'
    
    def UpdateClosingAmount(self, *args):
        try:
            self.closingAmount = - self.pv.Value()
        except Exception:
            self.closingAmount = 0.0

    def CreateCleanPackageCopy(self, origDp):
        copy = super(TradeActionClose, self).CreateCleanPackageCopy(origDp)
        for link in copy.TradeLinks():
            if link.Name() != '':
                b2bParams = copy.B2BTradeParamsAt(link.Name())
                b2bDecorator = acm.FBusinessLogicDecorator.WrapObject(b2bParams)
                if b2bDecorator.SalesCoverEnabled():
                    b2bDecorator.SalesMargin(0.0)
        for t in copy.AllOpeningTrades():
            t.Price(0)
            t.Premium(0)
        return copy

