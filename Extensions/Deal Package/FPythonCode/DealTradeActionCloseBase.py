import acm
from DealPackageDevKit import Object, Float, Str, TradeStatusChoices, ParseFloat, DealPackageException
from DealPackageTradeActionCloseBase import TradeActionCloseBase
from DealPackageUtil import CreateCleanPackageCopy, SetStatus

DEFAULT_PAYMENT_TYPE = 'Termination Fee'

class DealTradeActionCloseBase(TradeActionCloseBase):

    def AssemblePackage(self, arguments):
        self._args = arguments
        origDeal = arguments.At('dealPackage')
        origTrade = origDeal.DealPackage().Trades().First().Originator()
        definition = acm.DealCapturing.CustomInstrumentDefinition(origDeal)
        origEdit = acm.Deal.Wrap(origTrade, definition)
        self.DealPackage().AddChildDealPackage(origEdit, 'original')
        close = self.CreateCleanPackageCopy(origDeal)
        self.UpdateAcquireAndValueDay(close)
        origEdit.AddAsLifeCyclePackage(close, self.ClosePackageKey(), self.CloseEventType())
        
        SetStatus(close, arguments)
        acm.DealPackageActions.InvokeCloseTradeHook(origDeal, close)
        
    def ClosingNominal(self, *args):
        if len(args) == 0: #Read
            return self.CloseDealPackage().Trades().First().Nominal()
        else: #Write
            self.CloseDealPackage().Trades().First().Nominal(args[0])
    
    def RemainingNominal(self, *args):
        return self.OrigDealPackage().Trades().First().Originator().RemainingNominal()
        
    def ClosePackageKey(self):
        return self.CloseEventType()
