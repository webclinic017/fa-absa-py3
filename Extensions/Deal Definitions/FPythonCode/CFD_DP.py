import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import DerivativeInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('CFD') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class CFDDefinition(DealDefinition):

    ins                 = DerivativeInstrumentDefinition( instrument="Instrument" )
    
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
             'ins_expiryDateTime'                               : dict(enabled=False),
             'ins_payDayOffset'                                 : dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation'                                    : dict(onChanged='@OnQuotationChanged'),
             'ins_settlementType'                               : dict(visible='@IsShowModeInstrumentDetail'),                                                          
             'insProperties_spotBankingDaysOffset'              : dict(enabled=False),
             'trade_price'                                      : dict(visible=True),
             'trade_premium'                                    : dict(visible=True)
            }
        )    
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_CFD'
        
    def TradePanes(self):
        return 'CustomPanes_CFDTrade'
