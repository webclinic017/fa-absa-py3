import acm
from DealPackageDevKit import DealPackageDefinition, Action, List, Settings, Str, Text, ContextMenu, ContextMenuCommand, CommandActionBase, CustomActions
from inspect import cleandoc

CALC_MAP = {'strikePrice'      : 'Strike Price',
            'theorPrice'       : 'Price Theor',
            'delta'            : 'Instrument Delta',
            'vol'              : 'Portfolio Volatility',
            'undVal'           : 'Underlying Value',
            'foreignRepoRate'  : 'Foreign Repo Rate',
            'domesticRepoRate' : 'Domestic Repo Rate'}

class UnsimulateAction(CommandActionBase):
    DISPLAY_NAME = 'Unsimulate'
    def Invoke(self):
        unsim = self.DealPackage().GetAttribute('unsimulate')
        if unsim:
            unsim()

@Settings(GraphApplicable=False,
          SheetApplicable=False)
@CustomActions(unsimulate = UnsimulateAction)
class AdditionalCalculatedValues(DealPackageDefinition):
    """
    Additional calculations shown in list.
    - Selecting a row in the list will update the entry field above.
    - Entering a value in the entry field will simulate the corresponding calculation.
    - Pressing Unsimulate or clearing the entry field will unsimulate the selected calculation.

    NOTE: Use CalcMappings instead of additional calculations when applicable.
    """
    
    selectedCalc = Str(    label='@SelectedCalculationLabel',
                           onChanged='@Simulate')
                           
    unsimulate   = Action( label='Unsimulate',
                           action='@Unsimulate')
                           
    calculations = List(   label='Additional Calculations',
                           columns=[{'methodChain': 'StringKey',      'label': 'Name'}, 
                                    {'methodChain': 'Value',          'label': 'Result'}, 
                                    {'methodChain': 'FormattedValue', 'label': 'Form. Result'}],
                                    
                           onSelectionChanged='@SetSelected|UpdateSimulatedCalc',
                           onRightClick = ContextMenu('@UnsimulateContextMenuItem')    )
                           
    doc          = Text(   defaultValue=cleandoc(__doc__),
                           editable=False,
                           width=430,
                           height=110)
                           
    # ####################### #
    #   Interface Overrides   #
    # ####################### # 
    
    def UnsimulateContextMenuItem(self, name):  
        return ContextMenuCommand(commandPath = 'Unsimulate', 
                                  invoke= '@RightClickInvoke',
                                  enabled = '@RightClickEnabled',
                                  default = True)
   
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                hbox(;
                                    selectedCalc;
                                    unsimulate;
                                );
                                calculations;
                                vbox(;
                                    space(1);
                                );
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ]
                
    def OnInit(self):
        self._selected = 'strikePrice'
        
    def AssemblePackage(self):
        fxoTradeDeco = self.DealPackage().CreateTrade('FX Option', 'fxoTrade')
        fxoInsDec = fxoTradeDeco.Instrument()
        fxoInsDec.StrikePrice(1.3)
        fxoInsDec.ForeignCurrency('EUR')
        fxoInsDec.DomesticCurrency('USD')
        
    def OnNew(self):
        self._CreateAdditionalCalculations()
        self.UpdateSimulatedCalc()
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used to demonstrate additional calculations and can not be saved.')
        
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
    
    def SetSelected(self, attributeName, selectedElement):
        if selectedElement:
            index = self.calculations.IndexOf(selectedElement)
            self._selected = list(CALC_MAP.keys())[index]

    def UpdateSimulatedCalc(self, *args):
        self.SetAttribute('selectedCalc', self.GetCalculation(self._selected).FormattedValue(), silent=True)
    
    def SelectedCalculationLabel(self, attributeName):
        return CALC_MAP[self._selected]
        
    def Simulate(self, attributeName, old, new, userInputAttributeName):
        self._SimulateSelected(new)
        
    def Unsimulate(self, attributeName):
        self._SimulateSelected('')

    # ####################### #
    #   Convenience Methods   #
    # ####################### # 
    
    def FxoTrade(self):
        return self.TradeAt('fxoTrade')
    
    def _CreateAdditionalCalculations(self):
        for calcName, column in CALC_MAP.items():
            calcMapping = 'FxoTrade:FDealSheet:' + column
            self.CreateCalculation(calcName, calcMapping)
            self.calculations.Add(self.GetCalculation(calcName))
        
    def _SimulateSelected(self, value):
        self.SimulateCalculation(self._selected, value)
        self.UpdateSimulatedCalc() 
    
    def _IsSelectedCalculationSimulated(self):
        return self.IsCalculationSimulated(self._selected)
        
    # ################################# #
    #   Right click menu controllers    #
    # ################################# #
    
    def RightClickInvoke(self, name):
        self._SimulateSelected('')
        
    def RightClickEnabled(self, name):
        return self._IsSelectedCalculationSimulated()
