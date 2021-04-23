
import acm
from DealPackageDevKit import DealPackageDefinition, Delegate, Object, CalcVal, Settings, Text, CounterpartyChoices, AcquirerChoices, TradeStatusChoices, PortfolioChoices, TradeActions, CorrectCommand
from inspect import cleandoc

@Settings(GraphApplicable=False)
class ChildDealPackage(DealPackageDefinition):    
    strike      = Object(  label='Strike',
                           objMapping='Option.StrikePrice')

    undPrice    = CalcVal( calcMapping='Option:FDealSheet:Portfolio Underlying Price')

    undFwdPrice = CalcVal( calcMapping='Option:FDealSheet:Portfolio Underlying Forward Price')
    
    expiryDate  = Object(  label='Expiry',
                           objMapping='Option.ExpiryDateTime')
                                
    underlying  = Object(  label='Underlying',
                           objMapping='Option.Underlying',
                           choiceListSource='@UnderlyingChoices')
    
    portfolio   = Object(  label='Portfolio',
                           objMapping='Trades.Portfolio',
                           choiceListSource=PortfolioChoices())
             
    acquirer    = Object(  label='Acquirer',
                           objMapping='Trades.Acquirer',
                           choiceListSource=AcquirerChoices())
                           
    cpy         = Object(  label='Counterparty',
                           objMapping='Trades.Counterparty',
                           choiceListSource=CounterpartyChoices())
                            
    status      = Object(  label='Status',
                           objMapping='Trades.Status',
                           choiceListSource=TradeStatusChoices())
                           
    

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def AssemblePackage(self):
        tradeDecor = self.DealPackage().CreateTrade('Option', 'option')
        tradeDecor.Instrument().Underlying(self._FindAnyStockWithPrice())
        
    def LeadTrade(self):
        return self.TradeAt('option')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def UnderlyingChoices(self, *args):
        return acm.FStock.Instances()

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def Option(self):
        return self.InstrumentAt('option')

    def _FindAnyStockWithPrice(self):
        for stock in self.UnderlyingChoices():
            if stock.Prices():
                return stock

@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed') )
@Settings(GraphApplicable=False,
          SheetDefaultColumns=['Price Theor', 'Underlying Instrument', 'Strike Price'],
          MultiTradingEnabled=True)
class ParentDealPackage(DealPackageDefinition):
    """
    Example on how to build Deal Package of Deal Packages, and 
    how to delegate attributes to child deal packages
    """
    
    optionStrikes         = Delegate( attributeMapping='OpeningDealPackages.strike',
                                      transform='@TransformStrike')
                                    
    underlyingInstruments = Delegate( attributeMapping='OpeningDealPackages.underlying')   
        
    expiryDate            = Delegate( defaultValue='3m',
                                      attributeMapping='OpeningDealPackages.expiryDate')
    
    portfolio             = Delegate( attributeMapping='OpeningDealPackages.portfolio')
    
    acquirer              = Delegate( attributeMapping='OpeningDealPackages.acquirer')
    
    cpy                   = Delegate( attributeMapping='OpeningDealPackages.cpy')
    
    status                = Delegate( attributeMapping='OpeningDealPackages.status')
    
    doc                   = Text(     defaultValue=cleandoc(__doc__),
                                      editable=False,
                                      height=80)
                                      
    ipName                = Object(   label='Name',
                                      objMapping='InstrumentPackage.Name')
                                      
    pv                    = CalcVal( label='PV',
                                     calcMapping='AsPortfolio:FPortfolioSheet:Portfolio Present Value')
                            

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def AsPortfolio(self):
        return self.DealPackage().AsPortfolio()
        
    def AssemblePackage(self):
        self.DealPackage().AddNewChildDealPackage('ChildDealPackage', 'Child_1')
        self.DealPackage().AddNewChildDealPackage('ChildDealPackage', 'Child_2')
        self.DealPackage().AddNewChildDealPackage('ChildDealPackage', 'Child_3')
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_DealPackageOnDealPackage_DPE')
    
    def SuggestName(self):
        return 'DealPackgeOnDealPackageInstrumentPart'
    
    def LeadTrade(self):
        return self.DealPackage().ChildDealPackageAt('Child_2').TradeAt('option')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def TransformStrike(self, attributeName, newValue):
        if newValue and isinstance(newValue, str):
            try:
                newValue = self._ValueFromStringToStrike(newValue)
            except Exception as e:
                print (e)
        return newValue        

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def _ValueFromStringToStrike(self, strikeStr):
        strikeVal = strikeStr
        if strikeStr == 'atmf':
            dpWithLongestOption = None
            for dp in self.OpeningDealPackages():
                if dpWithLongestOption == None:
                    dpWithLongestOption = dp
                else:
                    dpOption = dp.InstrumentAt('option')
                    if dpOption.ExpiryDateTime() > dpWithLongestOption.GetAttribute('expiryDate'):
                        dpWithLongestOption = dp        
            strikeVal = dpWithLongestOption.GetAttribute('undFwdPrice').Value().Number()
        return strikeVal
