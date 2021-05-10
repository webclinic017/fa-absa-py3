import acm
from DealPackageDevKit import Object, Float, Str, Bool
from DealPackageUtil import CreateCleanPackageCopy, SetStatus
from DealPackageTradeActionCloseBase import TradeActionCloseBase, DEFAULT_PAYMENT_TYPE

class TradeActionNovate(TradeActionCloseBase):
    assignedAmount  = Float(  label='Amount',
                              enabled='@IsNotStepOut',
                              visible='@IsNotStepOut')
                                 
    assignedPayType = Object( label='Payment Type',
                              domain='enum(PaymentType)',
                              defaultValue = DEFAULT_PAYMENT_TYPE,
                              enabled='@IsNotStepOut',
                              visible='@IsNotStepOut')
    
    assignedCpy     = Object( label='Counterparty',
                              objMapping='AssignedTrades.Counterparty',
                              enabled='@IsNotStepOut',
                              visible='@IsNotStepOut')
    
    assignedPayCpy  = Object( label='Counterparty',
                              objMapping='AssignedTrades.Counterparty',
                              enabled=False,
                              visible='@IsNotStepOut')
    
    stepOut         = Bool( label='Step Out')
                            
                              
    
    def AssemblePackage(self, arguments):
        super(TradeActionNovate, self).AssemblePackage(arguments)
        origDp = arguments.At('dealPackage')
        
        assigned = CreateCleanPackageCopy(origDp, fromOriginator=True)
        self.UpdateAcquireAndValueDay(assigned)
        self.OrigDealPackage().AddAsLifeCyclePackage(assigned, self.PackageKey('Novated Assigned'), 'Novated Assigned')
        
        SetStatus(assigned, arguments)
        acm.DealPackageActions.InvokeCloseTradeHook(origDp, assigned)

    
    def OnNew(self):
        super(TradeActionNovate, self).OnNew()
        self.assignedCpy = None
    
    def IsValid(self, exceptionAccumulator, aspect):
        if not self.stepOut and self.assignedCpy == None:
            exceptionAccumulator('Must select a Counterparty')
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_TradeActionNovate')
    
    
    def OnSave(self, config):
        super(TradeActionNovate, self).OnSave(config)
        if self.stepOut:
            self.OrigDealPackage().RemoveChildDealPackage(self.AssignedDealPackage(), True)
            return acm.DealPackageActions.NovateDealPackageTrades( self.OrigDealPackage(),
                                                                   self.CloseDealPackage(),
                                                                   None )
        else:
            self.AddPayment(self.AssignedDealPackage().LeadTrade(),
                            self.assignedAmount,
                            self.assignedPayType)
            return acm.DealPackageActions.NovateDealPackageTrades( self.OrigDealPackage(),
                                                                   self.CloseDealPackage(),
                                                                   self.AssignedDealPackage() )
    
    def OpenAfterSave(self, config):
        if self.stepOut:
            return [self.CloseDealPackage()]
        else:
            return [self.CloseDealPackage(), self.AssignedDealPackage()]
    
    def AssignedDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original').ChildDealPackageAt(self.PackageKey('Novated Assigned'))
    
    def ClosingNominal(self, *args):
        retVal = super(TradeActionNovate, self).ClosingNominal(*args)
        if len(args) == 0: #Read
            return retVal
        else: #Write
            invertedValue = -args[0]
            self.SetPackageNominal(self.AssignedDealPackage(), invertedValue)
    
    def CloseEventType(self):
        return 'Novated'
    
    def AssignedTrades(self):
        if self.stepOut:
            return []
        return self.AssignedDealPackage().AllOpeningTrades()
    
    def NewTrades(self):
        newTrades = acm.FArray()
        newTrades.AddAll(self.ClosingTrades())
        newTrades.AddAll(self.AssignedTrades())
        return newTrades
    
    def ClosingNominalLabel(self, *args):
        return 'Nominal'
    
    def IsNotStepOut(self, *args):
        return not self.stepOut
        
