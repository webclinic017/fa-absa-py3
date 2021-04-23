import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import InstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Commodity') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class CommodityDefinition(DealDefinition):

    ins                 = InstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency'                                     : dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_contractSizeInQuotation'                      : dict(visible=True),
             'ins_settlementType'                               : dict(visible='@IsShowModeInstrumentDetail',
                                                                       label='Settlement'),
             'insProperties_spotBankingDaysOffset'              : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'trade_price'                                      : dict(visible=True),
             'trade_premium'                                    : dict(visible=True)
            }
        )    
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_Commodity'
        
    def TradePanes(self):
        return 'CustomPanes_CommodityTrade'
