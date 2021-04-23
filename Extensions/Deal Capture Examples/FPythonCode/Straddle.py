

import acm
from DealPackageDevKit import DealPackageDefinition, Date, Str, Object, Float, Action, DealPackageException, CalcVal, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, TradeActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, Settings
from CompositeAttributes import PaymentsDialog
import FUxCore
import decimal


@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed'),
               novate = NovateCommand(nominal='nominal'),
               close  = CloseCommand(nominal='nominal'),
               mirror = MirrorCommand(statusAttr='status', newStatus='Simulated'))
@Settings(MultiTradingEnabled=True)
class StraddleDefinition(DealPackageDefinition):

    ipName   =     Object(  label='Name',
                            objMapping='InstrumentPackage.Name') 

    # Instrument Attributes
    currency1 =    Object(  defaultValue=acm.FCurrency['EUR'],
                            label="Curr 1",
                            objMapping = "Instruments.ForeignCurrency|Trades.Currency",
                            onChanged="@OnCurrencyChanged")
    
    currency2 =    Object(  defaultValue=acm.FCurrency['USD'],
                            label="Curr 2",
                            objMapping = "Instruments.DomesticCurrency",
                            onChanged="@OnCurrencyChanged" )
    
    expiry =       Object(  defaultValue="1m",
                            label="Expiry",
                            objMapping="Instruments.FxoExpiryDate",
                            transform="@TransformExpiryPeriodToDate" )
                            
    strike =       Object(  label="Strike",
                            formatter="FXRate",
                            objMapping="Instruments.StrikePrice" )
                          
    # Trade Attributes
    longShort =    Str(     label="Nominal",
                            onChanged="@LongShortChanged",
                            choiceListSource=['Long', 'Short', '-'],
                            width=8)
                            
    nominal =      Object(  defaultValue=1000000,
                            label="Nominal",
                            objMapping="Trades.Quantity",
                            onChanged="@NominalChanged")
                            
    nominalDisplay = Float( label="",
                            onChanged="@NominalDisplayChanged",
                            backgroundColor='@NominalBackgroundColor')
                               
    counterparty = Object(  label="Counterparty",
                            objMapping="Trades.Counterparty",
                            choiceListSource=CounterpartyChoices() )
    
    portfolio =    Object(  label="Portfolio",
                            objMapping="Trades.Portfolio" )
    
    acquirer =     Object(  label="Acquirer",
                            objMapping="Trades.Acquirer",
                            choiceListSource=AcquirerChoices() )
    
    tradeTime =    Object(  label="Trade Time",
                            formatter="DateTime",
                            objMapping="Trades.TradeTime",
                            transform="@TransformPeriodToDate" )                   

    status =       Object(  defaultValue="Simulated",
                            label="Status",
                            objMapping="Trades.Status",
                            choiceListSource=TradeStatusChoices())
                            
    payments =     PaymentsDialog( trade="LeadTrade" )  
    
    setPrices =    Action(  label='Update Option Prices',
                            action="@SetOptionTradePriceFromTheor")
                          
    # B2B Attributes
    b2bEnabled =   Object(  defaultValue=False,
                            label="B2B Cover",
                            objMapping="CallB2B.SalesCoverEnabled|PutB2B.SalesCoverEnabled",
                            onChanged="@OnB2bEnabledChanged");
                            
    b2bCallPrice = Object(  defaultValue=0.0,
                            label="Call Trader Price",
                            objMapping="CallB2B.TraderPrice",
                            formatter="FullPrecision" );
                            
    b2bPutPrice =  Object(  defaultValue=0.0,
                            label="Put Trader Price",
                            objMapping="PutB2B.TraderPrice",
                            formatter="FullPrecision" );
                            
    b2bPrf =       Object(  label="Trader Prf",
                            objMapping="CallB2B.TraderPortfolio|PutB2B.TraderPortfolio",
                            choiceListSource=PortfolioChoices() );
             
    b2bAcq =       Object(  label="Trader Acq",
                            objMapping="CallB2B.TraderAcquirer|PutB2B.TraderAcquirer",
                            choiceListSource=AcquirerChoices() );

    # Calculated Values Attributes                     
    irCurr1 =      CalcVal( label="Int.Rate Curr 1",
                            calcMapping="CallOption:FDealSheet:Foreign Repo Rate" )
       
    irCurr2 =      CalcVal( label="Int.Rate Curr 2",
                            calcMapping="CallOption:FDealSheet:Domestic Repo Rate" )
                     
    undSpot =      CalcVal( label="Underlying Spot",
                            calcMapping="CallOption:FDealSheet:Underlying Value" )
                            
    # *************************************************
    # UI Panes      
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue("CustomPanes_Straddle")
        
    # *************************************************
    # Override GraphXValues        
    def GraphXValues(self):
        strike = self.DealPackage().GetAttribute("strike")
        xValues = acm.FArray()
        for i in range(95, 106, 1):
            xValues.Add( strike * i / 100 )
        return xValues
        
    # *************************************************
    # Object Mapping         
    def CallOption(self):
        return self.InstrumentAt("Call")
        
    def CallOptionTrade(self):        
        return self.TradeAt("Call")
        
    def PutOption(self):
        return self.InstrumentAt("Put")
        
    def PutOptionTrade(self):
        return self.TradeAt("Put")
        
    def CallB2B(self):
        return self.B2BTradeParamsAt("Call")

    def PutB2B(self):
        return self.B2BTradeParamsAt("Put")
        
    # *************************************************
    # Lead Trade (Confirmation/Payments)    
    def LeadTrade(self):
        return self.CallOptionTrade()
        
    # *************************************************
    # Transform Callbacks      
    def TransformExpiryPeriodToDate(self, name, newDate):
        self.CallOption().FxoExpiryDate(newDate)
        return self.CallOption().FxoExpiryDate()

    # *************************************************
    # Changed Callbacks                     
    def OnCurrencyChanged(self, attrCurrency, oldCurrency, newCurrency, *args):
        if oldCurrency and newCurrency and oldCurrency != newCurrency:
            self.strike = self.GetStrikePrice()
            
    def OnB2bEnabledChanged(self, attr, oldValue, newValue, *args):
        if newValue:
            self.b2bCallPrice = self.CallOption().Calculation().TheoreticalPrice(self._GetStdCalcSpace()).Value().Number()
            self.b2bPutPrice = self.PutOption().Calculation().TheoreticalPrice(self._GetStdCalcSpace()).Value().Number()
        else:
            self.b2bCallPrice = 0.0
            self.b2bPutPrice = 0.0
            
    def LongShortChanged(self, name, oldValue, newValue, *args):
        self.nominal = self.NominalDirection() * self.nominalDisplay
 
    def NominalDisplayChanged(self, name, oldValue, newValue, *args):
        direction = 1
        if self.NominalDirection():
            direction = self.NominalDirection()
        self.SilentUpdateLongShort(newValue * direction)
        self.SilentUpdateNominalDisplay(newValue)
        self.nominal = self.NominalDirection() * self.nominalDisplay
        
    def NominalChanged(self, name, oldValue, newValue, *args):
        self.UpdateLongShortAttribute(newValue)

    # *************************************************
    # Appearance Callbaks          
    def NominalBackgroundColor(self, *args):
        return 'BkgTickerOwnBuyTrade' if self.nominal >= 0 else 'BkgTickerOwnSellTrade'
        
    # *************************************************
    # Misc. Util Methods             
    def GetStrikePrice(self):
        today = acm.Time().DateToday()
        fxRate = 1
        if self.currency1 and self.currency2:
            try:
                fxRate = self.currency1.Calculation().FXRate(self._GetStdCalcSpace(), self.currency2, today).Value().Number()
                fxRate = round(decimal.Decimal(str(fxRate)), 4)
            except:
                print ("No exchange rate for chosen currency pair")
                
        return fxRate
        
    def SetOptionTradePriceFromTheor(self, *args):
        self.CallOptionTrade().Price(self.CallOption().Calculation().TheoreticalPrice(self._GetStdCalcSpace()))
        self.PutOptionTrade().Price(self.PutOption().Calculation().TheoreticalPrice(self._GetStdCalcSpace()))
            
    def NominalDirection(self):
        direction = 1
        if self.longShort == 'Short':
            direction = -1
        elif self.longShort == '-':
            direction = 0
        return direction
 
    def SilentUpdateLongShort(self, nominal):
        if nominal > 0:
            sign = 'Long'
        elif nominal < 0:
            sign = 'Short'
        else:
            sign = '-'
        self.SetAttribute('longShort', sign, silent=True)
    
    def SilentUpdateNominalDisplay(self, nominal):
        self.SetAttribute('nominalDisplay', abs(nominal), silent=True)
            
    def UpdateLongShortAttribute(self, nominal = None):
        if not nominal:
            nominal = self.CallOptionTrade().Quantity()
        self.SilentUpdateLongShort(nominal)
        self.SilentUpdateNominalDisplay(nominal)
        
   
    # *************************************************
    # Deal Package Interface Methods        

    def OnOpen(self):
        self.UpdateLongShortAttribute(self.nominal)
        
    def AssemblePackage(self):
        def AddFXOption(type):
            opt = acm.DealCapturing().CreateNewInstrument("FX Option")
            optDeco = acm.FBusinessLogicDecorator.WrapObject(opt)
            optTrade = acm.DealCapturing().CreateNewTrade(opt)
            optDeco.OptionType(type)
            self.DealPackage().AddTrade(optTrade, type)

        AddFXOption('Call')
        AddFXOption('Put')
    
    def OnNew(self):
        self.strike = round(self.CallOption().Calculation().UnderlyingPrice(self._GetStdCalcSpace()).Value().Number(), 4)
        self.UpdateLongShortAttribute(self.nominal)
        
    def IsValid(self, exceptionAccumulator, aspect):
        if not self.Trades().Size() == 2:
            exceptionAccumulator('Missing Straddle Component')
    
    def TransformPeriodToDate(self, name, date):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
    
    def IsLiveTrade(self, trade):
        return not trade.Instrument().IsExpired()


def StartStraddleApplication(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Straddle')
    return  
