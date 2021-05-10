import acm
from DealPackageDevKit import DealPackageDefinition, CalcVal, Float, Object, Settings, Text
from inspect import cleandoc

@Settings(SheetApplicable=False)
class SolveForAttributeDefinition(DealPackageDefinition):
    """
    Example on how to work with the attribute solver and calculated values.
     - Input in the field Strike will change the strike of the option
     - Input in the field Theor Price will solve for the strike that gives the entered theoretical price 
     - Input in the field Fwd Price will simulate the underlying forward price (no solving)
     - Input in the field PV will solve for the strike that gives the entered present value
     - Input in the solver section or pressing the Solve button will solve for the selected values
    """
      
    fwdPrice    = CalcVal( label='Fwd Price',
                           calcMapping='Fxo:FDealSheet:Portfolio Underlying Forward Value From Spot')
      
    theorPrice  = CalcVal( label='Theor Price',
                           calcMapping='Fxo:FDealSheet:Price Theor',
                           solverTopValue='strike')
                           
    pv          = CalcVal( label='PV',
                           calcMapping='AsPortfolio:FPortfolioSheet:Portfolio Present Value',
                           solverTopValue='strike')

    strike      = Object(  label='Strike',
                           objMapping='Fxo.StrikePrice',
                           solverParameter='@StrikeParameters')
                                    
    doc         = Text(    defaultValue=cleandoc(__doc__),
                           editable=False,
                           height=110,
                           width=400)
                                    
    # ####################### #
    #   Interface Overrides   #
    # ####################### # 
    
    def AssemblePackage(self):
        fxoTradeDecor = self.DealPackage().CreateTrade('FX Option', 'fxo')
        fxoTradeDecor.Quantity(1000000)
        fxoInsDecor = fxoTradeDecor.Instrument()
        fxoInsDecor.StrikePrice(1.3)
        fxoInsDecor.ForeignCurrency('EUR')
        fxoInsDecor.DomesticCurrency('USD')

        self.DealPackage().SetAttribute('strike', fxoInsDecor.StrikePrice())
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SolveForAttribute_DPE')
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can\'t be saved.')
                            
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
        
    def StrikeParameters(self, attributeName):
        parameters = {}
        calculation = self.DealPackage().GetAttribute('fwdPrice')
        if calculation:
            frwPrice = calculation.Value().Number()
            parameters = {'minValue':0.1 * frwPrice, 'maxValue':10.0 * frwPrice}
        return parameters
        
    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def Fxo(self):
        return self.InstrumentAt('fxo')
        
    def AsPortfolio(self):
        return self.DealPackage().AsPortfolio()
