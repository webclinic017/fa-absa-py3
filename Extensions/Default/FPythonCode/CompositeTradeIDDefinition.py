import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, Object, Bool
from ChoicesExprInstrument import getCategories, getCombCategories
from CompositeAttributes import SelectInstrumentsDialog, AliasTableTrade

class TradeIDDefinition(CompositeAttributeDefinition):
    
    def OnInit(self, trade, **kwargs):
        self._trade = trade 
        
    def Attributes(self):
        return { 
                 'aliases'              : AliasTableTrade ( label='Trade Aliases',
                                                  trade=self._trade)           
               }
    # Label callbacks

    # ChoiceListSource callbacks
        
    # Visible callbacks
        
    # Util
    def Trade(self):
        return self.GetMethod(self._trade)()
        
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                    vbox{;
                        aliases;
                    };
                   """
               )
