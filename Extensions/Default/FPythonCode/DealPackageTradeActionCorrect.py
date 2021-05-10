import acm
from DealPackageDevKit import DealPackageDefinition, CommandActionBase, Delegate, Object
from DealPackageUtil import UnpackPaneInfo, SetStatus, CreateCleanPackageCopy, LockInTradeTime
from DealPackageTradeActionBase import TradeActionBase

class TradeActionCorrect(TradeActionBase):
    """
    Transient Deal Package that contains the logic for Trade Action Correct. Used by CorrectCommand.
    """
    correct     = Delegate(attributeMapping='CorrectDealPackage')
    text1       = Object( label=' ',
                          objMapping='OrigDealPackage.AllOpeningTrades.Text1')
    text2       = Object( label=' ',
                          objMapping='OrigDealPackage.AllOpeningTrades.Text2')
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def AssemblePackage(self, arguments):
        origDp = arguments.At('dealPackage')
        
        origEdit = origDp.Edit()
        origEdit = self.DealPackage().AddChildDealPackage(origEdit, 'original')
        correct = CreateCleanPackageCopy(origDp, fromOriginator=True, lockInTradeTime=True)
        correct = origEdit.AddAsLifeCyclePackage(correct, 'correct', 'Correct')
        
        for t in origEdit.AllTrades():
            t.CorrectionTrade(t)
        
        LockInTradeTime(correct)    
        SetStatus(correct, arguments)
    
    def IsValid(self, exceptionAccumulator, aspect):
        if self.CorrectDealPackage().InstrumentPackage().IsModified():
            exceptionAccumulator('Instrument Package has been changed. Correcting Instrument Package is not supported')
        if not (self.text1 or self.text2):
            exceptionAccumulator('Must enter reason for correction in text fields')
    
    def OnSave(self, config):
        config.InstrumentPackage("Exclude")
        config.DealPackage("Save")
        
        businessEvents = acm.DealPackageActions.CorrectDealPackageTrades(self.OrigDealPackage(), self.CorrectDealPackage())
        return businessEvents
    
    def OpenAfterSave(self, config):
        return self.CorrectDealPackage()
    
    def CustomPanes(self):
        tabControls = self.correct.GetLayout()
        tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabControls[0])
        tabName, paneLayout = UnpackPaneInfo(tabCtrlLayout[0])
        
        paneLayout = '''vbox{; ''' + paneLayout +'''
                        vbox{Free text;
                            text1;
                            text2;
                            };
                        };'''
        
        tabCtrlLayout[0] = {tabName: paneLayout}
        return tabControls
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def OrigDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')
    
    def CorrectDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original').ChildDealPackageAt('correct')    

        
