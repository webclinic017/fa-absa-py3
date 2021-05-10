import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, CalcVal, ParseSuffixedFloat
from CompositeCashFlowInstrumentDefinition import CashFlowInstrumentDefinition


class AverageForwardInstrumentDefinition(CashFlowInstrumentDefinition):

    def OnInit(self, instrument, **kwargs):
        super(AverageForwardInstrumentDefinition, self).OnInit(instrument, **kwargs)


    def Attributes(self):
        
        attributes = super(AverageForwardInstrumentDefinition, self).Attributes()
                                                         
        attributes['crossCurrencyCalculation'] = Object( label='Conv Type',
                                                        objMapping=self._instrument+'.CrossCurrencyCalculation') 
                                                              

        return attributes
     

