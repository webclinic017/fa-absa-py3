import acm
from DealPackageDevKit import DealPackageDefinition, Object, Text, Settings, CalcVal
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=True,
          SheetDefaultColumns=['Price Theor', 'Fixed Rate', 'Par Rate'])
class RegenerateCashFlowsDefinition(DealPackageDefinition):
    """
    Example showing how to work with cash flow instrument dates 
    and how to use transform to calculate par rate as Fixed Rate.
    * Write 'par' in the Fixed Rate field to calculate and set Fixed Rate
    """

    startDate = Object(  defaultValue='0d', 
                         label='Start Date',
                         transform='@TransformStartPeriodToDate',
                         objMapping='Bond.LegStartDate',
                         onChanged='@RegenerateCashFlows')
                     
    endDate   = Object(  defaultValue='2y',
                         label='End Date',
                         transform='@TransformEndPeriodToDate',
                         objMapping='Bond.LegEndDate',
                         onChanged='@RegenerateCashFlows')
                             
    rolling   = Object(  defaultValue='6m',
                         label='Rolling',
                         objMapping='BondLeg.RollingPeriod',
                         onChanged='@RegenerateCashFlows')
                          
    rate      = Object(  defaultValue='par',
                         label='Fixed Rate',
                         transform='@TransformRate',
                         objMapping='BondLeg.FixedRate',
                         onChanged='@RegenerateCashFlows',
                         formatter='InstrumentDefinitionFixedRate',
                         toolTip='Write par to calculate and set Par Rate as Fixed Rate')
    
    parRate   = CalcVal( calcMapping='Bond:FDealSheet:Par Rate')
    
    doc       = Text(    defaultValue=cleandoc(__doc__),
                         editable=False,
                         height=80) 
        
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def OnNew(self):
        self.RegenerateCashFlows()
    
    def AssemblePackage(self):
        tradeDeco = self.DealPackage().CreateTrade('Bond', 'bond')
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_RegenerateCashFlowsDefinition_DPE')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def RegenerateCashFlows(self, *args):
        if self.Bond().IsInfant():
            self.BondLeg().GenerateCashFlows(0)
            
    def TransformStartPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Bond().LegStartDateFromPeriod(newDate)
        return newDate
        
    def TransformEndPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Bond().LegEndDateFromPeriod(newDate)
        return newDate
        
    def TransformRate(self, attributeName, newValue):
        if newValue == 'par' and self.parRate:
            self.RegenerateCashFlows()
            newValue = 100 * self.parRate.Value().Number()
        return newValue
        
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def BondLeg(self):
        return self.Bond().FirstFixedLeg()
    
    def Bond(self):
        return self.InstrumentAt('bond')
    
    def Trade(self):
        return self.TradeAt('bond')
