import acm
from DealPackageDevKit import DealPackageDefinition, CalcVal, Float, Object, Settings, Text  
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class SolveWithScenarioDefinition(DealPackageDefinition):
    """
    Example on how to work with the attribute solver and calculated values using scenarion configuration
     - Input in the field FX Shift adds a shift to the FX basis curve. This shift is applied to all calculations.
     - Input in the field Fwd Price will solve for the Fx Shift that gives the entered value.
    """

    foreignCurr  = Object(  label='Foreign',
                            objMapping='Fxo.ForeignCurrency|Fxo.Currency')
                            
    domesticCurr = Object(  label='Domestic',
                            objMapping='Fxo.DomesticCurrency')

    fxDiscShift  = Float(   label='FX Shift',
                            recreateCalcSpaceOnChange=True,
                            solverParameter='@FxDiscShiftParameters')
    
    fwdPrice     = CalcVal( label='Fwd Price',
                            calcMapping='Fxo:FDealSheet:Portfolio Underlying Forward Price',
                            calcConfiguration='@Configuration',
                            solverTopValue='fxDiscShift')
                                    
    theorPrice   = CalcVal( label='Th Price',
                            calcMapping='Fxo:FDealSheet:Price Theor',
                            calcConfiguration='@Configuration',
                            editable=False)
      
    doc          = Text(    defaultValue=cleandoc(__doc__),
                            editable=False,
                            height=65) 
 
    # ####################### #
    #   Interface Overrides   #
    # ####################### # 
    
    def AssemblePackage(self):
        fxoTradeDecor = self.DealPackage().CreateTrade('FX Option', 'fxo')
        fxoInsDecor = fxoTradeDecor.Instrument()
        fxoInsDecor.Underlying('EUR')
        fxoInsDecor.Currency('USD')
        fxoInsDecor.StrikePrice(1.3)

        self.DealPackage().SetAttribute('domesticCurr', fxoInsDecor.Currency())
        self.DealPackage().SetAttribute('foreignCurr', fxoInsDecor.Underlying())
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SolveWithScenario_DPE')
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can\'t be saved.')
        
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
        
    def Configuration(self, attributeName):
        scenario = acm.FExplicitScenario()
        filter = acm.GetFunction('currencyBaseCurveFilter', 1)(self.domesticCurr)
        scenario = self._GetScenario('deltabasispointswithfloor', 'fxDiscountCurve', filter, [[self.fxDiscShift, None]])
        config = acm.Sheet().Column().ConfigurationFromScenario(scenario, None)
        return config
    
    def FxDiscShiftParameters(self, attributeName):
        return {'minValue':-1000, 'maxValue':1000, 'maxIterations':50}
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Fxo(self):
        return self.InstrumentAt('fxo')
        
    def _GetScenario(self, shiftFunction, riskFactor, filter, values):
        scenario = acm.FExplicitScenario()
        scm = acm.CreateScenarioMember(acm.GetFunction(shiftFunction, 3), [riskFactor], filter, values)
        dim = acm.FDirectScenarioDimension()
        dim.AddScenarioMember(scm)
        scenario.AddDimension(dim)
        return scenario
