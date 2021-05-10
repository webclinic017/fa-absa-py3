
import acm
from DealPackageDevKit import (DealPackageDefinition, 
    # Attributes:
    Object, Text, 
    # Trade Action imports:
    TradeActions, CorrectCommand, CloseCommand, NovateCommand, MirrorCommand,
    # Multi Trading imports
    Settings, InstrumentPart, DealPart,
    # Choice list source imports
    CounterpartyChoices, AcquirerChoices, PortfolioChoices, TradeStatusChoices
    )

from inspect import cleandoc

@Settings(MultiTradingEnabled=True)
@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed'),
               novate = NovateCommand(statusAttr='status', nominal='callOptionQuantity'),
               close  = CloseCommand(statusAttr='status', nominal='callOptionQuantity'),
               mirror = MirrorCommand(statusAttr='status', newStatus='Simulated'))
class MultiTradingAndTradeActions(DealPackageDefinition):
    """
    Example showing:
     - How to add trade actions to a deal package
     - How to enable multi trading and working with InstrumentPart and DealPart
     
     - Note that the deal package must be saved to the database before
       trade actions can be invoked. For Close, Correct and Novate, the
       Deal Package must be saved in status FO Confirmed or higher.
    """

    ipName              = Object( label            = "Name",
                                  objMapping       = InstrumentPart("InstrumentPackage.Name") )

    # Instrument fields:
    underlying          = Object( label            = "Underlying",
                                  objMapping       = InstrumentPart("Instruments.Underlying"),
                                  onChanged        = '@SetStrikeATM|SetCurrencyFromUnderlying',
                                  choiceListSource = '@UnderlyingChoices')

    # Instrument and Trade fields:
    currency            = Object( label            = "Currency",
                                  objMapping       = InstrumentPart("InsCurrObjects.Currency").
                                                     DealPart("Trades.Currency"),
                                  # Using InstrumentPart and DealPart together with defaultValue 
                                  # ensures that the attribute is set correctly when creating a
                                  # new deal from an existing instrument package.
                                  defaultValue     = "USD")

    # Trade fields:
    callOptionQuantity  = Object( label            = "Quantity",
                                  objMapping       = 'CallOptionTrade.Quantity',
                                  onChanged        = "@SetPutOptionQuantity",
                                  defaultValue     = 1.0 )

    status              = Object( label            = "Trade Status",
                                  objMapping       = "Trades.Status",
                                  choiceListSource = TradeStatusChoices() )

    counterparty        = Object( label            = "Counterparty",
                                  objMapping       = "Trades.Counterparty",
                                  choiceListSource = CounterpartyChoices() )
    
    acquirer            = Object( label            = "Acquirer",
                                  objMapping       = "Trades.Acquirer",
                                  choiceListSource = AcquirerChoices() )
    
    portfolio           = Object( label            = "Portfolio",
                                  objMapping       = "Trades.Portfolio",
                                  choiceListSource = PortfolioChoices() )

    # Example information:
    doc                 = Text(   defaultValue     = cleandoc(__doc__),
                                  editable         = False,
                                  height           = 170 )

    # Not used in UI, used to enable different quantities on different trades
    # and show how this is handled in multi trading and trade actions.
    putOptionQuantity   = Object( objMapping = "PutOptionTrade.Quantity" )

    # ######################## #
    #    Interface Overrides   #
    # ######################## #      
    def AssemblePackage(self):
        self._CreateOptionTrades()

    def OnNew(self):
        self.SetPutOptionQuantity()
        
        # After a Save New on only the instrument part a new Deal part
        # will be created and OnNew will be executed. In this case we
        # need to exclude updating values on the instrument part
        if self.InstrumentPackage().IsInfant():
            self.SetStrikeATM()

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_MultiTradingAndTradeActions_DPE')

    def LeadTrade(self):
        return self.CallOptionTrade()        
    
    # ######################## #
    # Attribute Callbacks      #
    # ######################## #
    def SetPutOptionQuantity(self, *rest):
        self.putOptionQuantity = -self.callOptionQuantity

    def SetStrikeATM(self, *rest):
        price = self._GetPrice(self.underlying)
        self.CallOption().StrikePrice(price)
        self.PutOption().StrikePrice(price)

    def UnderlyingChoices(self, *args):
        return acm.FStock.Instances()

    def SetCurrencyFromUnderlying(self, *args):
        self.currency = self.underlying.Currency()

    # ######################## #
    # Component access         #
    # ######################## #
    def CallOption(self):
        return self.InstrumentAt("call")
    
    def PutOption(self):
        return self.InstrumentAt("put")
    
    def CallOptionTrade(self):
        return self.TradeAt("call")
    
    def PutOptionTrade(self):
        return self.TradeAt("put")
    
    def InsCurrObjects(self):
        currObjects = acm.FArray()
        currObjects.Add(self.CallOption())
        currObjects.Add(self.PutOption())
        return currObjects

    # ######################## #
    # Convenience methods      #
    # ######################## #
    def _FindAnyStockWithPrice(self):
        for stock in self.UnderlyingChoices():
            if stock.Prices():
                return stock
    
    def _GetPrice(self, stock):
        return stock.Calculation().MarketPrice(self._GetStdCalcSpace())

    def _CreateOptionTrades(self):
        put = acm.DealCapturing.CreateNewInstrument('Option')
        call = acm.DealCapturing.CreateNewInstrument('Option')
        stock = self._FindAnyStockWithPrice()
        put.Underlying(stock)
        call.Underlying(stock)
        put.StrikeCurrency(stock.Currency())
        call.StrikeCurrency(stock.Currency())
        put.OptionType('Put')
        call.OptionType('Call')
        put.ExerciseType('European')
        call.ExerciseType('European')
        putTrade = acm.DealCapturing.CreateNewTrade(put)
        callTrade = acm.DealCapturing.CreateNewTrade(call)
        self.DealPackage().AddTrade(putTrade, 'put')
        self.DealPackage().AddTrade(callTrade, 'call')

