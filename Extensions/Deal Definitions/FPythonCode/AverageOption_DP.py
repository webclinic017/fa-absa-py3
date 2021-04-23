import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, AddInfoDefinition, TradeBODefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Average Option')
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])
   
class AverageOptionDefinition(DealDefinition):
    
    ins                 = CashFlowInstrumentDefinition( instrument="Instrument")
    
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
            {'ins_currency'                             : dict(editable=False,
                                                               onChanged='@OnInstrumentCurrencyChanged'),
             'ins_optionType'                           : dict(label='Option Type'),
             'ins_startDate'                            : dict(onChanged='@OnInstrumentStartDateChanged'),
             'insProperties_spotBankingDaysOffset'      : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_contractSizeInQuotation'              : dict(visible=True),
             'ins_endDate'                              : dict(onChanged='@leg_UpdateRefInsChoices'),
             'leg_payOffset'                            : dict(visible=True),
             'leg_payDayMethod'                         : dict(visible=True),
             'leg_resets_resetType'                     : dict(enabled=False),
             'leg_strike'                               : dict(label='Strike',
                                                               visible=True),
             'leg_strikeType'                           : dict(choiceListSource=['Absolute']),
             'trade_price'                              : dict(visible=True),
             'trade_premium'                            : dict(visible=True)
            }
        )   
        
    def InstrumentPanes(self):
        return 'CustomPanes_AverageOption'
        
    def TradePanes(self):
        return 'CustomPanes_AverageOptionTrade'
        

def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
