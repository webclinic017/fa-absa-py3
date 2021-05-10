import acm
from DealPackageDevKit import DealPackageDefinition, CommandActionBase, Delegate, Object
from DealPackageUtil import UnpackPaneInfo, CreateCleanPackageCopy, SetStatus, LockInTradeTime
from DealPackageTradeActionCorrect import TradeActionCorrect

class DealTradeActionCorrect(TradeActionCorrect):
    
    def AssemblePackage(self, arguments):
        origDeal = arguments.At('dealPackage')
        origTrade = origDeal.DealPackage().Trades().First().Originator()
        definition = acm.DealCapturing.CustomInstrumentDefinition(origDeal)
        origEdit = acm.Deal.WrapAsDecorator(origTrade, self.DealPackage().GUI(), definition)
        origEdit = self.DealPackage().AddChildDealPackage(origEdit, 'original')
        correct = CreateCleanPackageCopy(origDeal, fromOriginator=True, lockInTradeTime=True)
        correct = origEdit.AddAsLifeCyclePackage(correct, 'correct', 'Correct')
        
        origEdit.Trades().First().CorrectionTrade(origEdit.Trades().First())
        
        LockInTradeTime(correct)
        SetStatus(correct, arguments)
    
    def IsValid(self, exceptionAccumulator, aspect):
        if self.CorrectDealPackage().Instruments().First().IsModified():
            exceptionAccumulator('Instrument Package has been changed. Correcting Instrument Package is not supported')
        if not (self.text1 or self.text2):
            exceptionAccumulator('Must enter reason for correction in text fields')
        

        
