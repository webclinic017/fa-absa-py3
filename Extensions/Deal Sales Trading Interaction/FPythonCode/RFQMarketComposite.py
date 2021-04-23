import acm
from DealPackageDevKit import CompositeAttributeDefinition
from DealPackageDevKit import CalcVal


class RFQMarket(CompositeAttributeDefinition):

    def Attributes(self):
        attributes = {}
        
        attributes.update({

                'askPrice': CalcVal(label='Ask',
                                               calcMapping=self.UniqueCallback('Instrument') + ':FOrderBookSheet:ADS Ask Price',
                                               editable=False,
                                               valuationDetails=False,
                                               visible=self.UniqueCallback('@MtMFromFeed')),
        
                'bidPrice': CalcVal(label='Bid',
                                               calcMapping=self.UniqueCallback('Instrument') + ':FOrderBookSheet:ADS Bid Price',
                                               editable=False,
                                               valuationDetails=False,
                                               visible=self.UniqueCallback('@MtMFromFeed')),                               
                                                  
                'lastPrice': CalcVal(label='Last',
                                               calcMapping=self.UniqueCallback('Instrument') + ':FOrderBookSheet:ADS Last Price',
                                               editable=False,
                                               valuationDetails=False,
                                               visible=self.UniqueCallback('@MtMFromFeed')),                                    
        })

        return attributes


    '''********************************************************************
    * Deal Definition
    ********************************************************************'''    
    def OnInit(self, instrumentName, **kwargs):
        self._instrumentName = instrumentName
        
    '''********************************************************************
    * Object Mappings
    ********************************************************************''' 
    def Instrument(self):
        return self.GetMethod(self._instrumentName)()
        
    '''********************************************************************
    * Visible callbacks
    ********************************************************************'''
    def MtMFromFeed(self, *args):
        return self.Instrument().MtmFromFeed()

    '''********************************************************************
    * Layout
    ********************************************************************'''
    def GetLayout(self):
        return self.UniqueLayout(
                    '''
                        hbox(;
                            bidPrice;
                            lastPrice;
                            askPrice;
                        );
                        
                    ''')
