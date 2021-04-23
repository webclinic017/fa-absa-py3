import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import FundInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Fund') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class FundDefinition(DealDefinition):

    ins                 = FundInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )

    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")
    
    def OnOpen(self):
        self.trade.OnOpen()
    
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            { 
             'insID_productTypeChlItem': dict(visible=False),
             'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'trade_price': dict(visible=True),
             'trade_premium': dict(visible=True),
             'trade_currency': dict(visible='@IsShowModeTradeDetail'),
            }
        )    

    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_Fund'
        
    def TradePanes(self):
        return 'CustomPanes_FundTrade'
