import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Settings, Action
from CompositeAttributesLib import BuySell
from inspect import cleandoc

@Settings(GraphApplicable=False)
class DealPackageBuySellControl(DealPackageDefinition):
    """
    Example showing a Buy/Sell control. 
    - Enter a + in front of number to go from Sell to Buy
    - Enter a - in front of number to go from Buy to Sell
    - The button is there to show how the quantity is set programmatically
    """
    
    ipName    = Object( label='Name',
                        objMapping='InstrumentPackage.Name') 
                                
    quantity  = BuySell(label='Quantity',
                        buySellLabels=["Buy", "Sell", "-"],
                        choiceListWidth=8,
                        objMapping='OptionTrade.Quantity')
    
    nominal   = BuySell(label='Nominal',
                        objMapping='OptionTrade.Nominal')
    
    quantityButton = Action(label="Set Quantity to 10",
                            sizeToFit=True,
                            action="@SetQuantityToTen")
    
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
                                hbox(;
                                    quantity;
                                    quantityButton;
                                );
                                nominal;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Option', 'option')
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def SetQuantityToTen(self, attributeName):
        self.quantity_value = 10

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def OptionTrade(self):
        return self.TradeAt('option')
