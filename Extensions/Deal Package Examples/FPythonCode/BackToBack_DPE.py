import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Settings, AcquirerChoices, PortfolioChoices
from inspect import cleandoc

@Settings(GraphApplicable=False)
class BackToBack(DealPackageDefinition):
    """Example showing the controls needed to make a Back To Back cover of a trade"""
    
    ipName            = Object( label='Name',
                                objMapping='InstrumentPackage.Name') 

    price             = Object( defaultValue=0.0,
                                label='Price',
                                objMapping='StockTrade.Price',
                                formatter='FullPrecision')
    
    portfolio         = Object( label='Portfolio',
                                objMapping='StockTrade.Portfolio',
                                choiceListSource=PortfolioChoices())

    b2bEnabled        = Object( defaultValue=False,
                                label='B2B Cover',
                                objMapping='StockB2B.SalesCoverEnabled')

    b2bMargin         = Object( defaultValue=0.0,
                                label='Margin',
                                objMapping='StockB2B.SalesMargin',
                                formatter='FullPrecision',
                                enabled='@IsB2B')
                            
    b2bPrice          = Object( defaultValue=0.0,
                                label='Trader Price',
                                objMapping='StockB2B.TraderPrice',
                                formatter='FullPrecision',
                                enabled='@IsB2B')
                            
    b2bPrf            = Object( label='Trader Portfolio',
                                objMapping='StockB2B.TraderPortfolio',
                                choiceListSource=PortfolioChoices(),
                                enabled='@IsB2B')
             
    b2bAcq            = Object( label='Trader Acquirer',
                                objMapping='StockB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices(),
                                enabled='@IsB2B')

    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=80) 

    # ####################### #
    #   Interface Overrides   #
    # ####################### # 
    
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_BackToBack_DPE')
        
    def AssemblePackage(self): 
        self.DealPackage().CreateTrade('Stock', 'stockTrade')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def IsB2B(self, attributeName):
        return self.b2bEnabled
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def StockTrade(self):
        return self.TradeAt('stockTrade')

    def StockB2B(self):
        return self.B2BTradeParamsAt('stockTrade')
