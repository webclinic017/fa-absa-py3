import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Settings, TradeStatusChoices
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetDefaultColumns=['Trade Status', 'Trade Currency', 'Instrument Currency'],
          MultiTradingEnabled=True)
class AttributeObjectMappings(DealPackageDefinition):
    """
    Change the status and the trade status will change. Change the 
    currency and both the instrument and trade currency will change.
    """
    
    ipName    = Object( label='Name',
                        objMapping='InstrumentPackage.Name') 

    status    = Object( label='Status',
                        objMapping='Trades.Status',
                        choiceListSource=TradeStatusChoices(),
                        toolTip='Object mapping to trade status')

    currency  = Object( defaultValue='EUR',
                        label='Currency',
                        objMapping='InstrumentAndTrades.Currency',
                        toolTip='Object mapping broadcasting setting currency')
 
    doc       = Text(   defaultValue=cleandoc(__doc__),
                        editable=False,
                        height=80)
 
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                ipName;
                                status;
                                currency;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );	
                                """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Stock', 'stockTrade')

    def LeadTrade(self):
        return self.TradeAt('stockTrade')
        
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def InstrumentAndTrades(self):
        objects = acm.FArray()
        objects.AddAll(self.Trades())
        objects.AddAll(self.Instruments())
        return objects
