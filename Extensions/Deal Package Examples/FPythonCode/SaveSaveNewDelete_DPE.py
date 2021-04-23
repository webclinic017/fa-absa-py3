
import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Action, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetDefaultColumns=['Price Theor'],
          MultiTradingEnabled=True)
class SaveSaveNewDelete(DealPackageDefinition):
    """
    Example showing a use of the methods Save, SaveNew and Delete
     - Press Save New to store a deal package containing an option and a stock 
     - Press 'Activate Save Button' to eneable the Save button
     - Save and SaveNew updates additional entities (prices). 
     - Every time the Deal Package is saved, the latest price of the stock will increase, 
       which can be seen in the Theor Price column in the pricing section. (Open the new 
       stocks Price Entry and look at the price.)
     - Pressing Save New Instrument creates a new instrument package containing the original
       stock and a new option on the stock
     - Pressing Save New Trade from an existing instrument package creates a new deal package
       in the instrument package and new trades in the instruments
    """
    
    ipName              = Object( label='Name',
                                  objMapping='InstrumentPackage.Name') 
    
    stockName           = Object( label='Stock',
                                  objMapping='Stock.Name',
                                  editable=False)
    
    stockTrdnbr         = Object( label='Trdnbr',
                                  objMapping='StockTrade.Originator.Name',
                                  editable=False)
    
    optionName          = Object( label='Option',
                                  objMapping='Option.Name',
                                  editable=False)
    
    optionTrdnbr        = Object( label='Trdnbr',
                                  objMapping='OptionTrade.Originator.Name',
                                  editable=False)
    
    touchBtn            = Action( label='Activate Save button',
                                  action='@PerformTouch',
                                  sizeToFit=True)
    
    doc                 = Text(   defaultValue=cleandoc(__doc__),
                                  editable=False,
                                  height=170) 

    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def CustomPanes(self):
        return [ 
                    {'General' : """
                                ipName;
                                hbox(;
                                    stockName;
                                    stockTrdnbr;
                                );
                                hbox(;
                                    optionName;
                                    optionTrdnbr;
                                );
                                touchBtn;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ] 

    def AssemblePackage(self): 
        self.DealPackage().CreateTrade('Stock', 'stock')
        option = acm.DealCapturing.CreateNewInstrument('Option')
        option.Underlying = self.Stock()
        optionTrade = acm.DealCapturing.CreateNewTrade(option)
        self.DealPackage().AddTrade(optionTrade, 'option')

    def OnSave(self, saveConfig):
        """ 
        Use this method to dictate the behaviour when saving deal package. Possible to return
        an array with objects that should be commited together with the dealpackage.
        """
        super(SaveSaveNewDelete, self).OnSave(saveConfig)        
        if self.Stock().IsInfant():
            return self._CreatePrice()
        else:
            return self._UpdatePrice()

    def _CreatePrice(self):
        # Create price records to be committed in the transaction
        print ('Creating Price')
        spotPrice = acm.FPrice()
        spotPrice.Instrument( self.Stock() )
        spotPrice.Currency( self.StockTrade().Currency() )
        spotPrice.Last(1.0)
        spotPrice.Market('SPOT')
        spotPrice.Day( acm.Time().DateToday() )
        
        internalPrice = spotPrice.Clone()
        internalPrice.Market('internal')
        internalPrice.Last(2.0)
        return {'commit':[spotPrice, internalPrice],
                'delete':[]}

    def _UpdatePrice(self):
        print ('Updating Price:')
        stockPrice = self.Stock().Originator().Prices().First()
        stockPriceImage = stockPrice.StorageImage()
        print ('    Old price:', stockPriceImage.Last())
        stockPriceImage.Last( stockPriceImage.Last() + 0.1 )
        print ('    New price:', stockPriceImage.Last())
        return {'commit':[stockPriceImage],
                'delete':[]}
                
    def OnDelete(self, allTrades):
        """ 
        Use this method to dictate the behaviour when deleting a deal package. 
        Return an object or a list of objects that should be deleted.
        """
        # Delete the price
        print ('OnDelete')
        stockPrice = self.Stock().Originator().Prices().First()
        print ('Deleting Price:\n', stockPrice)
        return {'commit':[],
                'delete':[stockPrice]}

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def PerformTouch(self, attributeName):
        self.DealPackage().Touch()
        self.DealPackage().Changed()

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def Stock(self):
        return self.InstrumentAt('stock')
        
    def StockTrade(self):
        return self.TradeAt('stock')
        
    def Option(self):
        return self.InstrumentAt('option')
        
    def OptionTrade(self):
        return self.TradeAt('option')
