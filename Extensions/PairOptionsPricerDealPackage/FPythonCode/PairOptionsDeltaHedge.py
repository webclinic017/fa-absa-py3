import acm
from DealPackageDevKit import CompositeAttributeDefinition, Action, Object, Str, CounterpartyChoices, PortfolioChoices, ParseFloat

class DeltaHedgeCompositeAttribute(CompositeAttributeDefinition):
    def OnInit(self, deltaHedgeName):
        self._deltaHedgeName = deltaHedgeName
              
    def DeltaHedgeAttributes(self):
        return {
                'type':                Object( label='Hedge Type',
                                                objMapping='DeltaHedge.Parameters.HedgeType',
                                                onChanged='@OnHedgeTypeChanged',
                                                choiceListSource=self.UniqueCallback('@TypeChoices')),

                'valueDay':            Object( defaultValue='3m',
                                                label='Value Day',
                                                objMapping='DeltaHedge.Parameters.ValueDay',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable'),
                                                transform='@ValueDayFromPeriod'),

                'counterparty':        Object( label='Counterparty',
                                                objMapping='DeltaHedge.Counterparty',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable'),
                                                choiceListSource=CounterpartyChoices()),
            
                'portfolio':           Object( label='Portfolio',
                                                objMapping='DeltaHedge.CounterpartyPortfolio',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable'),
                                                choiceListSource=PortfolioChoices()),
                                                
                'price':               Object( label='Price',
                                                objMapping='DeltaHedge.Parameters.Price',
                                                formatter='FXRate',
                                                transform=self.UniqueCallback('@DeltaHedgeTransformNumber'),
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),

                'delta':               Object( label='Delta',
                                                objMapping='DeltaHedge.Parameters.Delta',
                                                formatter='FXDeltaHedgeAmounts',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),                                                

                'amountForeign':       Object( label='@ForeignAmountLabel',
                                                objMapping='DeltaHedge.Parameters.Amount',
                                                formatter='FXDeltaHedgeAmounts',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),                                                

                'amountDomestic':      Object( label='@DomesticAmountLabel',
                                                objMapping='DeltaHedge.Parameters.AmountCurr2',
                                                enabled=False,
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),   

                'updatePrice':         Action( label='Update Price',
                                                action='@DeltaHedgeUpdatePrice',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),
                 
                'updateDelta':         Action( label='Update Delta',
                                                action='@DeltaHedgeUpdateDelta',
                                                visible=self.UniqueCallback('@IsDeltaHedgeApplicable')),
                                                        
               }    
     
    '''*******************************************************
    * Override method
    *******************************************************'''                                
    def Attributes(self):
        return dict(self.DeltaHedgeAttributes())
     
    '''*******************************************************
    * Delta Hedge Get methods
    *******************************************************'''                                
    def DeltaHedge(self):
        return self._deltaHedgeName
    
    def IsDeltaHedgeApplicable(self, attributeName):
        return self.type != 'None'
    
    def DeltaHedgeTransformNumber(self, attributeName, value):
        return ParseFloat(value)
        
    def TypeChoices(self, *args):
        pricingOptions = self.GetMethod("PricingOptions")()
        if pricingOptions.IsKindOf('FPmOptionsPricer'):
            return ['None', 'Spot']
        else:
            return ['None', 'Spot', 'Forward']
        
    '''*******************************************************
    * Layout
    *******************************************************'''                                    
    def GetLayout(self):
        return self.UniqueLayout('''vbox[Delta Hedge;
                                      type;
                                      valueDay;   
                                      counterparty;
                                      price;
                                      delta;
                                      amountForeign;
                                      amountDomestic;
                                      updatePrice;
                                      updateDelta;
                                      ];
                                 ''')
