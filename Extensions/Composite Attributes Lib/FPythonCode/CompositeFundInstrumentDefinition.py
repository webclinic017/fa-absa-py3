import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, CalcVal, ParseSuffixedFloat
from ChoicesExprInstrument import getExerciseTypeChoices, getOptionTypeChoices
from CompositeInstrumentDefinition import InstrumentDefinition

class FundInstrumentDefinition(InstrumentDefinition):

    def OnInit(self, instrument, **kwargs):
        super(FundInstrumentDefinition, self).OnInit(instrument, **kwargs)

    def Attributes(self):
        
        attributes = super(FundInstrumentDefinition, self).Attributes()
        
        attributes['fundPortfolio']           = Object( label='Fund Portf',
                                                        objMapping=self._instrument+'.FundPortfolio')
                                                        
        attributes['quotation']               = Object( label='Quotation',
                                                        objMapping=self._instrument+'.Quotation',
                                                        choiceListSource=self.UniqueCallback('@QuotationChoices'),
                                                        visible = '@IsShowModeInstrumentDetail')
                                                        
        
        return attributes
     
    # Enabled callbacks
        
    # Visible callbacks
        
    # ChoiceListSource callbacks      
       
    # Transform callbacks
        
    # OnChanged callbacks
        
    # Util


        
