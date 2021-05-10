
import acm
from DealPackageTradeActionMirror import TradeActionMirror
from DealPackageUtil import CreateCleanPackageCopy

class DealTradeActionMirror(TradeActionMirror):
 
    def AssemblePackage(self, arguments):
        self._args = arguments
        origDeal = arguments.At('dealPackage')
        origTrade = origDeal.DealPackage().Trades().First().Originator()
        definition = acm.DealCapturing.CustomInstrumentDefinition(origDeal)
        origEdit = acm.Deal.Wrap(origTrade, definition)
        self._origEdit = origEdit
        mirrorDeal = CreateCleanPackageCopy(origDeal, fromOriginator=True)
        self.TouchTradeTime(mirrorDeal.AllOpeningTrades())
        self.DealPackage().AddChildDealPackage(mirrorDeal, 'mirror')
