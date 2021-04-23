import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, AddInfoDefinition, TradeBODefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Convertible')
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class ConvertibleDefinition(DealDefinition):
    
    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    leg                 = LegDefinition( leg='Leg', trade='Trade' )
    
    legCashFlows        = CashFlowDefinition( leg='Leg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )

    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")
    
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_startDate': dict(onChanged='@OnInstrumentStartDateChanged'),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_discountingType': dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation': dict(visible='@IsShowModeInstrumentDetail',
                                                               onChanged='@OnQuotationChanged'),
             'leg_fixedRate': dict(solverParameter=None,
                                                               backgroundColor=None,
                                                               transform=None),                                                            
             'leg_payCalendar': dict(visible='@IsShowModeInstrumentDetail'),
             'trade_price': dict(visible=True),
             'trade_premium': dict(visible=True),
            }
        )   
        
    def InstrumentPanes(self):
        return 'CustomPanes_Convertible'
        
    def TradePanes(self):
        return 'CustomPanes_ConvertibleTrade'

def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
