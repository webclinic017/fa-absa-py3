import acm
from DealPackageDevKit import CalcVal
from DealPackageUtil import CreateCleanPackageCopy, SetStatus
from DealTradeActionCloseBase import DealTradeActionCloseBase

class DealTradeActionClose(DealTradeActionCloseBase):    
                    
        
    pv             = CalcVal(    label='Current PV',
                                 calcMapping='CloseDealPackageAsPortfolio:FPortfolioSheet:Portfolio Present Value',
                                 enabled=False)
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_TradeActionClose')
    
    def OnSave(self, config):
        super(DealTradeActionClose, self).OnSave(config)
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
        copy = super(DealTradeActionClose, self).CreateCleanPackageCopy(origDp)
        for t in copy.AllOpeningTrades():
            t.Price(0)
            t.Premium(0)
        return copy
