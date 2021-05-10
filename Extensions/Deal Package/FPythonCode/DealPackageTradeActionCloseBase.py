import acm
from DealPackageDevKit import Object, Float, Str, TradeStatusChoices, ParseFloat, DealPackageException
from DealPackageTradeActionBase import TradeActionBase
from DealPackageUtil import CreateCleanPackageCopy, SetStatus

DEFAULT_PAYMENT_TYPE = 'Termination Fee'

class TradeActionCloseBase(TradeActionBase):
    """
    Transient Deal Package that contains the logic for Trade Action Close. Used by CloseCommand.
    """
                                  
    closingNominal =  Float(      label = '@ClosingNominalLabel',
                                  objMapping = 'ClosingNominal',
                                  formatter = 'PackageAbsNominalSigDig',
                                  transform = '@TransformNominal',
                                  onChanged = '@UpdateClosingAmount',
                                  backgroundColor='@NominalBackgroundColor')
                                    
    remainingNominal =    Float(  label = 'Total Nominal',
                                  formatter = 'PackageAbsNominalSigDig',
                                  objMapping='RemainingNominal',
                                  enabled = False)
                                  
    valueDay       =  Object(     label='Value Day',
                                  objMapping='NewTrades.ValueDay',
                                  transform = '@TransformPeriodToDate')
                                 
    acquireDay     =  Object(     label='Acquire Day',
                                  objMapping='NewTrades.AcquireDay',
                                  onChanged='@SetTradeTime',
                                  enabled=False)
                                  
    status         =  Object(   label='Status',
                                choiceListSource=TradeStatusChoices(),
                                objMapping = 'NewTrades.Status')
                                 
    closingAmount  = Float(      label='Amount')
                                 
    closingPayType = Object(       label='Payment Type',
                                   domain='enum(PaymentType)',
                                   defaultValue = DEFAULT_PAYMENT_TYPE)
    
    closingCpy     = Object(       label='Counterparty',
                                   objMapping='ClosingTrades.Counterparty',
                                   enabled=False)
    
    closingNominalAttr = Str(   defaultValue = 'nominal', onChanged = '@UpdateNominal')
    
    statusAttr =         Str( )
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def NominalBackgroundColor(self, attributeName):
        return 'BkgTickerOwnBuyTrade' if self.closingNominal > 0 else 'BkgTickerOwnSellTrade'
        
    def ClosingSign(self):
        return 1 if ParseFloat(self.remainingNominal ) < 0 else -1
        
    def TransformNominal(self, name, val):
        if val:
            if abs( ParseFloat(val) ) > abs( ParseFloat( self.remainingNominal ) ):
                return abs( ParseFloat(self.remainingNominal ) ) * self.ClosingSign() 
            else:
                return abs( ParseFloat(val) )  * self.ClosingSign() 
        return 0.0
    
    def PackageKey(self, eventType):
        return eventType + str(1+self.NumberOfExistingPackagesOfEventType(eventType))
    
    def NumberOfExistingPackagesOfEventType(self, eventType):
        count = 0
        for dp in self.OriginatorPackage().LifeCyclePackages():
            if dp.EventType() == eventType:
                count = count + 1
        return count
                
    def UpdateClosingAmount(self, *args):
        pass

    def SetTradeTime(self, *args):
        for t in self.NewTrades():
            if acm.Time.DateDifference(t.AcquireDay(), acm.Time.TimeNow()) < 0:
                t.DecoratedObject().TradeTime = acm.Time.DateFromTime(self.acquireDay) 
            else:
                t.DecoratedObject().TradeTime = acm.Time.TimeNow()
    
    def LeadTrade(self):
        return self.CloseDealPackage().LeadTrade()
    
    def OnNew(self):
        self.statusAttr = self._args.At('statusAttr') or 'status'
        self.closingNominalAttr = self._args.At('nominal')
        self.closingNominal = - self.remainingNominal
            
    def UpdateNominal(self, *args):
        self.closingNominal = self.ClosingNominal()
        self.remainingNominal = self.RemainingNominal()
    
    def ClosePackageKey(self):
        return self.PackageKey(self.CloseEventType())
        
    def UpdateAcquireAndValueDay(self, dp):
        for t in dp.AllOpeningTrades():
            t.AcquireDay(t.Instrument().SpotDate(acm.Time.DateToday()))
            t.ValueDay(t.Instrument().SpotDate(acm.Time.DateToday()))
    
    def AssemblePackage(self, arguments):
        self._args = arguments
        origDp = arguments.At('dealPackage')
        origEdit = origDp.Edit()
        self.DealPackage().AddChildDealPackage(origEdit, 'original')
        close = self.CreateCleanPackageCopy(origDp)
        self.UpdateAcquireAndValueDay(close)
        origEdit.AddAsLifeCyclePackage(close, self.ClosePackageKey(), self.CloseEventType())
        
        SetStatus(close, arguments)
        acm.DealPackageActions.InvokeCloseTradeHook(origDp.Edit(), close)

    def OnSave(self, config):
        config.InstrumentPackage('Exclude')
        config.DealPackage('Save')
        for t in self.CloseDealPackage().AllOpeningTrades():
            payments = t.Payments()
            for p in payments[:]:
                p.Unsimulate()        
        self.AddPayment(self.CloseDealPackage().LeadTrade(),
                        self.closingAmount,
                        self.closingPayType)
        
    def AddPayment(self, trade, amount, paymentType):
        if trade and abs(amount) > 0.000001:
            payment = acm.FPayment()
            payment.Currency = trade.Currency()
            payment.Party = trade.Counterparty()
            payment.PayDay = self.valueDay
            payment.ValidFrom(acm.Time().DateToday())
            payment.Amount = amount
            payment.Type = paymentType
            
            trade.Payments().Add(payment)
        
    def ClosingNominal(self, *args):
        if len(args) == 0: #Read
            return self.GetPackageNominal(self.CloseDealPackage())
        else: #Write
            self.SetPackageNominal(self.CloseDealPackage(), args[0])
    
    def RemainingNominal(self, *args):
        def GetCorrectedClose(originalCloseDp):
            candidateDp = originalCloseDp
            while 'correct' in candidateDp.ChildDealPackageKeys():
                candidateDp = candidateDp.ChildDealPackageAt('correct')
            return candidateDp
            
        originator = self.OriginatorPackage().Edit()
        nominal = self.GetPackageNominal(originator)
        for dp in originator.LifeCyclePackages():
            if dp.EventType() == 'Close':
                correctedDp = GetCorrectedClose(dp)
                if self.GetPackageStatus(correctedDp) != 'Void':
                    nominal = nominal + self.GetPackageNominal(correctedDp)
            elif dp.EventType() == 'Novated' and self.GetPackageStatus(dp) != 'Void':
                nominal = nominal + self.GetPackageNominal(dp)
        return nominal
        
    def SetPackageNominal(self, dealPackage, val):
        if self.closingNominalAttr in dealPackage.GetAttributes():
            dealPackage.SetAttribute(self.closingNominalAttr, val )
            
    def GetPackageStatus(self, dealPackage):
        if self.statusAttr in dealPackage.GetAttributes():
            return dealPackage.GetAttribute(self.statusAttr)
    
    def GetPackageNominal(self, dealPackage):
        if self.closingNominalAttr in dealPackage.GetAttributes():
            return dealPackage.GetAttribute(self.closingNominalAttr)
        else:
            return 0.0
    
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
    
    def CreateCleanPackageCopy(self, origDp):
        copy = CreateCleanPackageCopy(origDp, fromOriginator=True)
        return copy
        
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def OrigDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')
    
    def CloseDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original').ChildDealPackageAt(self.ClosePackageKey())

    def CloseDealPackageAsPortfolio(self):
        return self.CloseDealPackage().AsPortfolio()
    
    def ClosingTrades(self):
        return self.CloseDealPackage().AllOpeningTrades()
    
    def NewTrades(self):
        return self.ClosingTrades()
        
    def OriginatorPackage(self):
        return self.OrigDealPackage().Originator()
