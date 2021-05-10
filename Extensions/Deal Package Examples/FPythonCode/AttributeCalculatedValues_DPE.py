import acm
from DealPackageDevKit import DealPackageDefinition, CalcVal, Object, Settings, Text
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetDefaultColumns=['Call or Put', 'Price Theor', 'Portfolio Present Value'])
class AttributeCalculatedValues(DealPackageDefinition):
    """
    Calculated values as attributes in different sheets.
     - Theor Price for the four options in the package calculated in Deal Sheet
     - Total PV for the package calculated in the Deal Package Sheet
     - Total PV of the call/put options calculated in the Portfolio Sheet
     - Setting Quantity updates the quantity of all trades and affects PV calculations
    """
    
    ipName      = Object(  label='Name',
                           objMapping='InstrumentPackage.Name') 

    theorPrice1 = CalcVal( label='Theor Price 1',
                           calcMapping='Trade1:FDealSheet:Price Theor')
                           
    theorPrice2 = CalcVal( label='Theor Price 2',
                           calcMapping='Trade2:FDealSheet:Price Theor')
                           
    theorPrice3 = CalcVal( label='Theor Price 3',
                           calcMapping='Trade3:FDealSheet:Price Theor')
                           
    theorPrice4 = CalcVal( label='Theor Price 4',
                           calcMapping='Trade4:FDealSheet:Price Theor')
                           
    totalPV     = CalcVal( label='Total PV',
                           calcMapping='DealPackage:FDealPackageSheet:Portfolio Present Value')
                           
    callPV      = CalcVal( label='Call PV',
                           calcMapping='CallPortfolio:FPortfolioSheet:Portfolio Present Value')
    
    putPV       = CalcVal( label='Put PV',
                           calcMapping='PutPortfolio:FPortfolioSheet:Portfolio Present Value')
                           
    quantity    = Object(  defaultValue=1000000,
                           label='Quantity',
                           objMapping="Trades.Quantity")
                                    
    doc         = Text(    defaultValue=cleandoc(__doc__),
                           editable=False,
                           height=95)
 
    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def CustomPanes(self):
        return [ 
                    {'General' : """
                                vbox{;
                                  ipName;
                                  quantity;
                                };
                                vbox[Deal Sheet;
                                  theorPrice1;
                                  theorPrice2;
                                  theorPrice3;
                                  theorPrice4;
                                ];
                                vbox[Deal Package Sheet;
                                  totalPV;
                                ];
                                vbox[Portfolio Sheet;
                                  callPV;
                                  putPV;
                                ];
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ] 

    def AssemblePackage(self):
        def AddFxoTrade(name, strikePrice, flip):
            fxoTradeDeco = self.DealPackage().CreateTrade('FX Option', name)
            fxoInsDec = fxoTradeDeco.Instrument()
            fxoInsDec.StrikePrice(strikePrice)
            fxoInsDec.ForeignCurrency('EUR')
            fxoInsDec.DomesticCurrency('USD')
            if flip:
                fxoTradeDeco.FxoFlip()
            
        AddFxoTrade('trade1', 1.1, False)
        AddFxoTrade('trade2', 1.2, False)
        AddFxoTrade('trade3', 1.3, True)
        AddFxoTrade('trade4', 1.4, True)
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Trade1(self):
        return self.TradeAt('trade1')
        
    def Trade2(self):
        return self.TradeAt('trade2')
        
    def Trade3(self):
        return self.TradeAt('trade3')

    def Trade4(self):
        return self.TradeAt('trade4')
        
    def CallPortfolio(self):
        return self._GetPortfolio(True)
    
    def PutPortfolio(self):
        return self._GetPortfolio(False)
        
    def _GetPortfolio(self, isCall):
        portfolio = acm.FAdhocPortfolio()
        for trade in self.Trades():
            if trade.Instrument().IsCall() == isCall:
                portfolio.Add(trade)
        return portfolio
            
