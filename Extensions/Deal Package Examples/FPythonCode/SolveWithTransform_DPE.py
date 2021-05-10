import acm
from DealPackageDevKit import DealPackageDefinition, CalcVal, Object, Settings, Text, ParseSuffixedFloat
from inspect import cleandoc

@Settings(LogMode='Verbose',
          SheetDefaultColumns=['Price Theor', 'Portfolio Underlying Price', 'Portfolio Underlying Forward Price', 
                               'Portfolio Volatility', 'Portfolio Carry Cost', 'Instrument Delta', 'Strike Price'])
class SolveWithTransformDefinition(DealPackageDefinition):
    """
    Example showing how to work with pricing of Options. 
     - Different ways of calculating the strike is shown.
     - The Option is priced at a 50 Delta when initially created. 
     - Input in the field Delta will solve and set the Strike Price
     - Input, e.g., 50d in the field Strike Price will solve for a 50 delta and set the Strike Price
     - Input atm in the field Strike Price will calculate and set the At-the-Money strike
     - Input atmf in the field Strike Price will calculate and set the At-the-Money Forward strike
    """
                                
    underlying  = Object(  label='Underlying',
                           objMapping='Option.Underlying',
                           choiceListSource='@UnderlyingChoices')    

    optionType  = Object(  defaultValue='Call',
                           label='Type',
                           objMapping='Option.OptionType',
                           choiceListSource=['Call', 'Put'])
    
    expiryDate  = Object(  defaultValue='3m',
                           label='Expiry',
                           objMapping='Option.ExpiryDate',
                           transform='@TransformExpPeriodToDate')

    strike      = Object(  label='Strike',
                           objMapping='Option.StrikePrice',
                           backgroundColor='@SolverColor',
                           solverParameter='@StrikeSolverParams',
                           transform='@TransformStrike')
      
    delta       = CalcVal( defaultValue=0.5,
                           label='Delta',
                           calcMapping='Option:FDealSheet:Instrument Delta',
                           solverTopValue='strike')

    undPrice    = CalcVal( label='Und Price',
                           calcMapping='Option:FDealSheet:Portfolio Underlying Price')

    undFwdPrice = CalcVal( calcMapping='Option:FDealSheet:Portfolio Underlying Forward Price')

    doc         = Text(    defaultValue=cleandoc(__doc__),
                           editable=False,
                           height=120,
                           width=400)  
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
  
    def AssemblePackage(self):
        tradeDecor = self.DealPackage().CreateTrade('Option', 'opt')
        optDecor = tradeDecor.Instrument()
        optDecor.UnderlyingType('Stock')
        optDecor.Underlying(self._FindAnyStockWithPrice())
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SolveWithTransform_DPE')
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can\'t be saved.')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
    
    def StrikeSolverParams(self, *args):
        undPrice = self._UnderlyingPrice()
        return {'minValue':undPrice*0.5, 'maxValue':undPrice*2}
        
    def TransformExpPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Option().ExpiryDateFromPeriod(newDate)
        return newDate
                
    def TransformStrike(self, attributeName, input):
        if input == 'atm':
            return self._UnderlyingPrice()
        if input == 'atmf':
            return self._UnderlyingForwardPrice()
        
        f = self.GetFormatter('delta')
        delta = ParseSuffixedFloat(input, suffix=['d'], formatter=f)
        if delta is not None:
            return self.Solve(topValue='delta', parameter='strike', solverValue=delta/100.0)
            
        return input
        
    def UnderlyingChoices(self, *args):
        return acm.FStock.Instances()
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Option(self):
        return self.InstrumentAt('opt')
        
    def _FindAnyStockWithPrice(self):
        for stock in self.UnderlyingChoices():
            if stock.Prices():
                return stock
        return None
    
    def _UnderlyingForwardPrice(self):
        return self.undFwdPrice.Value().Number()
    
    def _UnderlyingPrice(self):
        return self.undPrice.Value().Number()
