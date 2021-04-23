import acm
from DealPackageDevKit import DealPackageDefinition, Date, Str, Object, Float, Action, DealPackageException, CalcVal, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, Settings, CorrectCommand, NovateCommand, CloseCommand, TradeActions
from FAssetManagementUtils import GetInstruments

TWO_WAY_SIGN_MAP = {'Buy':  1, (1): 'Buy', 
                    'Sell': -1,(-1): 'Sell',  
                    '-':  0, (0): '-'}


@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed'),
               novate = NovateCommand(nominal='quantity'),
               close  = CloseCommand(nominal='quantity'))
@Settings(MultiTradingEnabled=False, ShowSheetInitially=True, GraphApplicable=False, ShowGraphInitially=False, SheetDefaultColumns=['Trade Quantity', 'Instrument Market Price', 'Price Theor', 'Fund Net Asset Value', 'Instrument Fund Units'])
class MasterFeederFundDefinition(DealPackageDefinition):

    # *************************************************
    # Instrument Package Attributes

    ipName =          Str(  label='Package Name',
                            objMapping='InstrumentPackage.Name',
                            toolTip='The name of the instrument package. If an instrument package is found on the same fund, this one will be used instead.',
                            enabled=True )

    # *************************************************
    # Instrument Attributes

    instrument  =       Object( label='@FundInstrumentLabel',
                                objMapping='FeederTrade.Instrument|MasterTrade.Instrument',
                                toolTip='Instrument name',
                                choiceListSource='@AllFundChoices',
                                onChanged='@InstrumentChanged')
                            
    fundPortfolio =    Object(  label="@FundPortfolioLabel",
                                objMapping="FeederTrade.Instrument.FundPortfolio|MasterTrade.Portfolio",
                                toolTip='The portfolio underlying the fund',
                                enabled=False)
    # *************************************************
    # Trade Attributes
                            
    buySell   = Str(    label = 'Quantity',
                        onChanged='@UpdateQuantity',
                        choiceListSource=['Buy', 'Sell', '-'],
                        maxWidth=8,
                        width=8)

    quantity  = Object( label='',
                        objMapping='Trades.Quantity',
                        onChanged='@QuantityChanged',
                        formatter='PackageAbsNominal',
                        transform='@TransformQuantity',
                        backgroundColor='@QuantityBackgroundColor')
                       
    price =     Float(  label='@TradeColumnDefinitionLabel',
                        objMapping='Trades.Price',
                        onChanged='@UpdatePremiumOrQuantity',
                        formatter='SixDecimalDetailedTruncateTrailingZeroShowZero' )
                                
    cashAmount =           Float(   label='Cash Amount',
                                    formatter='AbsShowZeroHideNaN',
                                    objMapping='MasterTrade.Premium',
                                    transform='@TransformCashAmount',
                                    onChanged='@CashAmountChanged',
                                    backgroundColor='@CashAmountBackgroundColor')
                               
    feederCounterparty = Object(  label='@TradeColumnDefinitionLabel',
                                  objMapping="FeederTrade.Counterparty",
                                  choiceListSource=CounterpartyChoices() )
                                  
    masterCounterparty = Object(  label='@TradeColumnDefinitionLabel',
                                  objMapping="MasterTrade.Counterparty",
                                  choiceListSource=CounterpartyChoices() )
    
    feederPortfolio =    Object(  label='@TradeColumnDefinitionLabel',
                            objMapping="FeederTrade.Portfolio" )
    
    masterAcquirer =     Object(  label='@TradeColumnDefinitionLabel',
                            objMapping="MasterTrade.Acquirer",
                            choiceListSource=AcquirerChoices() )
                            
    feederAcquirer =     Object(  label='@TradeColumnDefinitionLabel',
                            objMapping="FeederTrade.Acquirer",
                            choiceListSource=AcquirerChoices() )
    
    tradeTime =    Object(  defaultValue=acm.Time().DateToday(),
                            label='@TradeColumnDefinitionLabel',
                            objMapping="Trades.TradeTime",
                            transform="@TransformPeriodToDate" )                   

    status =       Object(  defaultValue="Simulated",
                            label='@TradeColumnDefinitionLabel',
                            objMapping="Trades.Status",
                            choiceListSource=TradeStatusChoices())
           
    def OnInit(self):
        self.cashAmountInternal = None
        DealPackageDefinition.OnInit(self)
                 
    # *************************************************
    # UI Panes      
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_MasterFeederFundPackage")
        
    # *************************************************
    # Object Mapping         
    def MasterTrade(self):
        return self.PrivateTradeAt("Master")
        
    def FeederTrade(self):
        return self.PrivateTradeAt("Feeder")
        
    def PrivateTradeAt(self, key):
        return self.TradeAt(key) if key in self.DealPackage().TradeKeys() else self.Trades().First()
        
    def LeadTrade(self):
        return self.PrivateTradeAt("Feeder")
        
    # *************************************************
    # Transform Callbacks   
   
    def TransformPeriodToDate(self, name, date):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    def TransformQuantity(self, name, input):
        if not isinstance(input, basestring):
            return input
        
        parsed = self.GetFormatter(name).Parse(input)
        if parsed is None:
            return input
        
        if input.startswith( ('+', '-') ):
            sign = {'+':1, '-':-1}[input[0]]
        else:
            sign = self._BuySellSign() if self._BuySellSign() else 1
        
        return sign * abs(parsed)
        
    def TransformCashAmount(self, name, input):
        cashAmount = self.TransformQuantity(name, input)
        self.cashAmountInternal = cashAmount
        return cashAmount

    # *************************************************
    # Appearance Callbacks
    
    def TradeColumnDefinitionLabel(self, attr):
        prefix = ""
        if "feeder" in attr:
            prefix = "Feeder "
            columnId = attr[6].upper() + attr[7:]
        elif "master" in attr:
            prefix = "Master "
            columnId = attr[6].upper() + attr[7:]
        else:
            columnId = attr[0].upper() + attr[1:]
        
        return self._ColumnLabel(columnId, acm.FTrade)
    
    def QuantityBackgroundColor(self, *args):
        return 'BkgTickerOwnBuyTrade' if self.quantity >= 0 else 'BkgTickerOwnSellTrade'
        
    def CashAmountBackgroundColor(self, *args):
        return 'BkgTickerOwnBuyTrade' if self.cashAmount >= 0 else 'BkgTickerOwnSellTrade'
        
    def FundInstrumentLabel(self, *args):
        return 'Instrument'

    def FundPortfolioLabel(self, *args):
        return self._ColumnLabel('FundPortfolio', acm.FFund)
        
    def _ColumnLabel(self, columnid, targetCls):
        return str(self._ColumnDefinition(columnid, targetCls).At('ColumnName'))
        
    def _ColumnDefinition(self, columnid, targetCls):
        return acm.GetDefaultContext().GetExtension("FColumnDefinition", targetCls, columnid).Value()
        
        
    # *************************************************
    # Deal Package Interface Methods        
        
    def SuggestedPrice(self, instrument):
        suggestedMtMColumn = 'Suggested Mark-to-Market Price'
        calcSpace = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
        return calcSpace.CalculateValue(instrument, suggestedMtMColumn).Value().Number()
    
    def SetDefaultAttributes(self):
        self.price = self.SuggestedPrice(self.MasterTrade().Instrument())
        
    def AddFeederTrade(self, fundInstrument):
        fundTrade = acm.DealCapturing().CreateNewTrade(fundInstrument)
        self.DealPackage().AddTrade(fundTrade, 'Feeder')
            
    def AddMasterTrade(self, fundInstrument):
        fundTrade = acm.DealCapturing().CreateNewTrade(fundInstrument)
        fundTrade.TradeCategory = 'Subscription'
        fundTrade.Portfolio = fundInstrument.FundPortfolio()
        self.DealPackage().AddTrade(fundTrade, 'Master')
    
    def AssemblePackage(self, fundInstrument = None):
        if fundInstrument is None:
            fundInstruments = acm.FFund.Select('')
            try:
                fundInstrument = fundInstruments[0]
            except IndexError:
                raise DealPackageException('No Fund instruments available')
        self.AddFeederTrade(fundInstrument)
        self.AddMasterTrade(fundInstrument)
        self.SetDefaultAttributes()
    
    def IsValid(self, exceptionAccumulator, aspect):
        if not self.Trades().Size() == 2:
            exceptionAccumulator.ValidationError('Missing component')
        if not self.Instruments().Size() == 1:
            exceptionAccumulator.ValidationError('All instruments must be the same')
        masterTrade = self.DealPackage().TradeAt('Master')
        if masterTrade.TradeCategory() != 'Subscription':
            exceptionAccumulator.ValidationError('Master trade missing')
        if masterTrade.Instrument().FundPortfolio() != masterTrade.Portfolio():
            exceptionAccumulator.ValidationError('Master trade in wrong portfolio')
    
    def IsLiveTrade(self, trade):
        return not trade.Instrument().IsExpired()
        
    def OnOpen(self):
        self.UpdateBuySell()
    
    def OnNew(self):
        self.UpdateBuySell()
        
    # *************************************************
    # Callbacks
    
    def UpdatePremiumOrQuantity(self, attribute, old_value, new_value, *args):    
        if self.cashAmountInternal:
            self.cashAmount = self.cashAmountInternal
            self.quantity = self._DeriveQuantityFromCashAmount()

    def QuantityChanged(self, *args):
        self.cashAmountInternal = None
        self.UpdateBuySell()
        
    def CashAmountChanged(self, *args):
        if self.cashAmountInternal:
            quantity = self._DeriveQuantityFromCashAmount()
            if quantity != self.quantity:
                self.SetAttribute('quantity', quantity, silent = True)
                self.UpdateBuySell()
        
    def InstrumentChanged(self, attribute, old_value, new_value, *args):
        if new_value and new_value != old_value:
            for t in self.DealPackage().Trades():
                self.DealPackage().RemoveTrade(t)
            for i in self.DealPackage().Instruments():
                self.DealPackage().RemoveInstrument(i)
            self.cashAmountInternal = None
            self.AssemblePackage(new_value)
        
    def _BuySellSign(self):
        return TWO_WAY_SIGN_MAP[self.buySell]
        
    def _QuantitySign(self):
        return cmp(self.quantity, 0)
        
    def _DeriveQuantityFromCashAmount(self):
        try:
            price = 1 / self.price
        except ZeroDivisionError:
            return self.quantity
        else:
            tradeDecoratorClone1 = self.MasterTrade().Clone()
            tradeDecoratorClone1.Nominal = self.cashAmount
            tradeDecoratorClone2 = self.MasterTrade().Clone()        
            tradeDecoratorClone2.Nominal = self.CalculatePremium(tradeDecoratorClone1, price)
            return tradeDecoratorClone2.Quantity()
       
    def CalculatePremium(self, trade, price):
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        acquireDay = trade.AcquireDay()
        return trade.Calculation().PriceToPremium(space, acquireDay, price)
    
    def UpdateBuySell(self, *args):
        sign = TWO_WAY_SIGN_MAP[self._QuantitySign()]
        self.SetAttribute('buySell', sign, silent = True)
        
    def UpdateQuantity(self, *args):
        newQuantity = self._BuySellSign() * abs(self.quantity)
        self.SetAttribute('quantity', newQuantity)
        
    # *************************************************
    # Choicelists          
        
    def AllFundChoices(self, *args):
        return acm.FFund.Select('')

    # *************************************************
    # OnSave
    
    def OnSave(self, config):
        self._ReplaceExistingInstrumentPackage(config)
        DealPackageDefinition.OnSave(self, config)
        
                
    def _GetExistingInstrumentPackage(self):
        dp = self.DealPackage()
        instrument = dp.Instruments().First()
        links = instrument.Originator().DealPackageInstrumentLinks()
        for link in links:
            ip = link.InstrumentPackage()
            if not ip.IsInfant() and (ip.Definition() == self.DealPackage().Definition()):
                return ip
        
    def _ReplaceExistingInstrumentPackage(self, config):
        if self.DealPackage().InstrumentPackage().IsInfant() or config.InstrumentPackage() == "SaveNew":
            existingInsPackage = self._GetExistingInstrumentPackage()
            if existingInsPackage:
                config.InstrumentPackage('Exclude')
                existingInsPackage = existingInsPackage.StorageImage()
                self.DealPackage().InstrumentPackage(existingInsPackage)

def StartMasterFeederFund(eii):
    try:
        fundInstruments = GetInstruments(eii)
        ins = fundInstruments.First() if fundInstruments.First().IsKindOf(acm.FFund) else None
    except Exception:
        ins = None
    dp = acm.DealPackage.New('MasterFeederFund', ins)
    acm.UX().SessionManager().StartApplication('Deal Package', dp)
    return  
