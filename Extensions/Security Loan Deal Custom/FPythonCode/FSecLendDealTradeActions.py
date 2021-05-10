""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecurityLoanDealCustom/etc/FSecLendDealTradeActions.py"

import acm
from DealPackageTradeActionCloseBase import TradeActionCloseBase
from DealPackageTradeActionBase import TradeActionBase
from DealDevKit import Object, Float, Str, Date, Action, ParseFloat, TradeStatusChoices, Delegate
from DealPackageUtil import SetNew, UnpackPaneInfo, CreateCleanPackageCopy, DealPackageUserException
from FSecLendRerate import SecLendRerate


class TradeActionReturn(TradeActionCloseBase):


    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'remainingNominal': dict(label='Total Quantity',
                                     formatter='Imprecise'),
            'valueDay':         dict(validate='@DateValidate')
            })

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanTradeActionClose')

    def DateValidate(self, name, value):
        if value < self.OrigDealPackage().Instruments().First().StartDate():
            raise DealPackageUserException('Not possible to return on a date before the start date of the loan.')

    def RemainingNominal(self, *args):
        trades = self.OrigDealPackage().Trades().First().DecoratedObject().Originator().Instrument().Trades()
        return sum((t.Quantity() for t in trades if t.Status() not in ["Void", "Confirmed Void", "Simulated",]))
    
    def IsFullClose(self, *args):
        return acm.Math.AlmostZero(self.remainingNominal + self.closingNominal, 1e-10)

    def ClearPayments(self):
        for t in self.CloseDealPackage().AllOpeningTrades():
            payments = t.Payments()
            for p in payments[:]:
                p.Unsimulate()

    def SetAddInfo(self):
        source = acm.FMarketPlace['Manual']
        for t in self.CloseDealPackage().Trades():
            if source is not None:
                t.Market(source)
            if hasattr(t.AdditionalInfo(), 'SBL_PendingOrder'):
                t.AddInfoValue("SBL_PendingOrder", False)
            if hasattr(t.AdditionalInfo(), 'SBL_OrderType'):
                t.AdditionalInfo().SBL_OrderType('Firm')

    def SetTradeType(self):
        for t in self.CloseDealPackage().Trades():
            t.Type = self.ActionTradeType()

    def OnSave(self, config):
        self.ClearPayments()
        config.InstrumentPackage('Save')
        config.DealPackage('Save')
        acm.DealPackageActions.CloseDealPackageTrades(self.OrigDealPackage(), self.CloseDealPackage())
        self.SetAddInfo()
        self.SetTradeType()

    def OpenAfterSave(self, config):
        return self.CloseDealPackage()

    def ClosePackageKey(self):
        return self.CloseEventType()

    def CloseEventType(self):
        return 'Return'

    def ActionTradeType(self):
        return 'Closing'

    def ClosingNominalLabel(self, *args):
        return 'Quantity'

    def ClosingNominal(self, *args):
        if len(args) == 0: #Read
            return self.CloseDealPackage().Trades().First().Quantity()
        else: #Write
            self.CloseDealPackage().Trades().First().Quantity(args[0])

    def UpdateAcquireAndValueDay(self, dp):
        for t in dp.AllOpeningTrades():
            calendarInfo = dp.Instruments().First().Underlying().Currency().Calendar().CalendarInformation()
            adjustedDate = calendarInfo.AdjustBankingDays(acm.Time.DateToday(), self.GetDefaultSettlementDelay())
            t.AcquireDay(adjustedDate)
            t.ValueDay(adjustedDate)

    def GetDefaultSettlementDelay(self):
        return 1 # Always default to one day in the future. Market standard is typically underlying spot day - 1, i.e. typically 1 day.


class TradeActionRecall(TradeActionReturn):
    
    
    def DateValidate(self, name, value):
        if value < self.OrigDealPackage().Instruments().First().StartDate():
            raise DealPackageUserException('Not possible to recall on a date before the start date of the loan.')

    def CloseEventType(self):
        return 'Recall'

    def GetDefaultSettlementDelay(self):
        return self.OrigDealPackage().Instruments().First().Underlying().SpotBankingDaysOffset()

    def ActionTradeType(self):
        return 'RollOut'


class TradeActionIncrease(TradeActionReturn):


    increaseNominal =  Float( label='@IncreaseNominalLabel',
                              objMapping='ClosingNominal',
                              formatter='Imprecise',
                              backgroundColor='@NominalBackgroundColor',
                              transform = '@TransformNominal')

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanTradeActionIncrease')

    def DateValidate(self, name, value):
        if value < self.OrigDealPackage().Instruments().First().StartDate():
            raise DealPackageUserException('Not possible to increase on a date before the start date of the loan.')

    def CloseEventType(self):
        return 'Increase'

    def IncreaseNominalLabel(self, *args):
        return 'Quantity'

    def IncreasingSign(self):
        return -1 if ParseFloat(self.remainingNominal ) < 0 else 1

    def TransformNominal(self, name, val):
        if val:
            return abs( ParseFloat(val) )  * self.IncreasingSign()
        return 0.0

    def ActionTradeType(self):
        return 'Adjust'

    def OnNew(self):
        self.statusAttr = self._args.At('statusAttr') or 'status'
        self.closingNominalAttr = self._args.At('nominal')
        self.increaseNominal = self.IncreasingSign()


class TradeActionLink(TradeActionBase):

    linkedPackage = Delegate(attributeMapping='OriginalPackage')
    
    def AssemblePackage(self, arguments):
        origDp = arguments.At('dealPackage')
        origEdit = origDp.Edit()
        self.DealPackage().AddChildDealPackage(origEdit, 'original')
        self.DealPackage().AddChildDealPackage(self.CreateCleanCopy(origDp), 'linkedPackage') 
    
    def CreateCleanCopy(self, origDp):
        definition = acm.DealCapturing.CustomInstrumentDefinition(origDp)
        tradeCopy = origDp.DealPackage().Trades().First().Originator()
        copy = acm.Deal.WrapAsDecorator(tradeCopy, origDp.GUI(), definition)
        SetNew(copy.Instruments())
        SetNew(copy.Trades())
        return copy
    
    def OnNew(self):
        self.ConnectTrade(self.LinkedPackage().Trades().First(), self.OriginalPackage().Trades().First().Originator())
        
    def OpenAfterSave(self, config):
        return self.LinkedPackage()
    
    def ConnectTrade(self, trade, refTrade):
        trade.AddInfoValue("SL_LinkedTrade", refTrade)
    
    def CustomPanes(self):
        tabControls = self.linkedPackage.GetLayout()
        tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabControls[0])
        tabName, paneLayout = UnpackPaneInfo(tabCtrlLayout[0])
        
        paneLayout = '''vbox{; ''' + paneLayout +''' };'''
        
        tabCtrlLayout[0] = {tabName: paneLayout}
        return tabControls
    
    def OriginalPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')  
    
    def LinkedPackage(self):
        return self.DealPackage().ChildDealPackageAt('linkedPackage')


class TradeActionRerate(TradeActionBase):


    rerateDate = Date(label='Date',
                      transform='@TransformPeriodToDate',
                      validate='@DateValidate')
    
    rerateFee = Float(label='Fee(bp)',
                      toolTip="Fee in basis points.",
                      defaultValue=0.0,
                      formatter='SolitaryPricePercentToBasisPoint')

    applyButton = Action(label='Apply',
                         action='@Apply')

    def AssemblePackage(self, arguments):
        origDp = arguments.At('dealPackage')
        trade = origDp.Trades().First().Trade().Originator()
        origEdit = acm.Deal().WrapAsDecorator(trade, None, 'Security Loan Deal')
        
        # Disable Cash Flow Generation dialog
        uxCallbacks = origEdit.GetAttribute('uxCallbacks')
        uxCallbacks.RemoveKey('dialog')
        
        self.DealPackage().AddChildDealPackage(origEdit, 'original')

    def OnNew(self):
        self.SetDefaultRerateValues()

    def CustomPanes(self):
        return [{'Rerate':  """
                            vbox(;
                                rerateDate;
                                rerateFee;
                                );
                            hbox(;
                                fill;
                                applyButton;
                                );
                            """}]

    def OnSave(self, config):
        self.Rerate()
        
        config.DealPackage('Exclude')
        config.InstrumentPackage('Save')

    def OpenAfterSave(self, config):
        return None

    def Apply(self, *args):
        self.DealPackage().Save()
        self.CloseDialog()

    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date

    def DateValidate(self, name, value):
        if value < acm.Time.DateToday():
            raise DealPackageUserException('Not possible to rerate historically')

    def SetDefaultRerateValues(self):
        rerate = SecLendRerate(self.OriginalPackage().Instruments().First())
        self.rerateDate = rerate.DefaultExtendDate()
        self.rerateFee = self.GetFixingValue()

    def Rerate(self):
        ins = self.OriginalPackage().Instruments().First()
        rerate = SecLendRerate(ins, self.rerateFee, self.rerateDate)
        rerate.ExtendSecurityLoan()
        rerate.DoRerate()

    def OriginalPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')

    def GetFixingValue(self):
        try:
            calcSpaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            calcSpace = calcSpaceCollection.GetSpace('FDealSheet', acm.GetDefaultContext())
            
            ins = self.OriginalPackage().Instruments().First().Instrument()
            calculation = calcSpace.CreateCalculation(ins, 'Security Loan Fixing Value', None)
            return calculation.Value() if calculation.Value() is not None else 0.0
        except:
            return 0.0


class TradeActionExtend(TradeActionBase):


    extendDate = Date(label='Date',
                      transform='@TransformPeriodToDate',
                      validate='@DateValidate')

    applyButton = Action(label='Apply',
                         action='@Apply')

    def AssemblePackage(self, arguments):
        origDp = arguments.At('dealPackage')
        trade = origDp.Trades().First().Trade().Originator()
        origEdit = acm.Deal().WrapAsDecorator(trade, None, 'Security Loan Deal')
        
        # Disable Cash Flow Generation dialog
        uxCallbacks = origEdit.GetAttribute('uxCallbacks')
        uxCallbacks.RemoveKey('dialog')
        
        self.DealPackage().AddChildDealPackage(origEdit, 'original')

    def OnNew(self):
        self.SetDefaultExtendDate()

    def CustomPanes(self):
        return [{'Extend':  """
                            vbox(;
                                extendDate;
                                );
                            hbox(;
                                fill;
                                applyButton;
                                );
                            """}]

    def OnSave(self, config):
        self.Extend()

        config.DealPackage('Exclude')
        config.InstrumentPackage('Save')

    def OpenAfterSave(self, config):
        return None

    def Apply(self, *args):
        if self.extendDate < self.OriginalPackage().Instruments().First().EndDate():
            raise DealPackageUserException('Instrument is already extended')
        self.DealPackage().Save()
        self.CloseDialog()

    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date

    def DateValidate(self, name, value):
        if value < acm.Time.DateToday():
            raise DealPackageUserException('Not possible to extend historically')

    def SetDefaultExtendDate(self):
        rerate = SecLendRerate(self.OriginalPackage().Instruments().First())
        self.extendDate = rerate.DefaultExtendDate()

    def Extend(self):
        ins = self.OriginalPackage().Instruments().First()
        rerate = SecLendRerate(ins, 0.0, self.extendDate)
        rerate.ExtendSecurityLoan()

    def OriginalPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')
