import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Settings, PortfolioChoices, CounterpartyChoices, AcquirerChoices
from CompositeAttributesLib import PremiumTranslation, PaymentsDialog
from inspect import cleandoc

@Settings(GraphApplicable=False)
class DealPackagePremiumTranslation(DealPackageDefinition):
    """
    Example showing a Premium Translation composite attribute. 
    To show the Premium Translation fields:
     - Turn on the show mode Detail (Layout > Slim/Detail)
    To enable fields:
     - Enter a non-zero premium. 
    """
    
    ipName       = Object( label='Name',
                           objMapping='InstrumentPackage.Name') 
                                
    trdCurr      = Object( label='Trade Curr',
                           objMapping='OptionTrade.Currency')
    
    premium      = Object( label='Premium',
                           objMapping='OptionTrade.Premium',
                           formatter='FullPrecision')
    
    fee          = Object( label='Fee',
                           objMapping='OptionTrade.Fee',
                           formatter='FullPrecision')
    
    premiumTrans = PremiumTranslation( trade='OptionTrade',
                                       showMode='IsShowModeDetail')
    
    portfolio    = Object( label='Portfolio',
                           objMapping='OptionTrade.Portfolio',
                           choiceListSource=PortfolioChoices())
    
    counterparty = Object( label='Counterparty',
                           objMapping='OptionTrade.Counterparty',
                           choiceListSource=CounterpartyChoices())
                                
    acquirer     = Object( label='Acquirer',
                           objMapping='OptionTrade.Acquirer',
                           choiceListSource=AcquirerChoices())
                                
    broker       = Object( label='Broker',
                           objMapping='OptionTrade.Broker')
                           
    payments     = PaymentsDialog(trade='OptionTrade')

    doc       = Text(   defaultValue=cleandoc(__doc__),
                        editable=False,
                        height=80)

    # ####################### #
    #   Interface Overrides   #
    # ####################### #  

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_PremiumTranslation_DPE')
        
    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Option', 'option')
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def OptionTrade(self):
        return self.TradeAt('option')
    
    def Option(self):
        return self.InstrumentAt('option')
