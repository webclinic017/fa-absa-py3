import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, AutocallLegDefinition, CashFlowDefinition, TradeDefinition, AddInfoDefinition, TradeBODefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Autocallable')
@Settings(SheetDefaultColumns=['Price Theor', 'Portfolio Theoretical Value', 'Portfolio Underlying Price', 'Portfolio Volatility'])   
class AutocallableDefinition(DealDefinition):
    
    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    leg                 = AutocallLegDefinition( leg='Leg', trade='Trade' )
    
    legCashFlows        = CashFlowDefinition( leg='Leg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )

    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")
    
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency'                             : dict(onChanged='@OnInstrumentCurrencyChanged',
                                                               enabled='@CurrencyEnabled'),
             'ins_startDate'                            : dict(onChanged='@OnInstrumentStartDateChanged'),
             'insProperties_spotBankingDaysOffset'      : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_discountingType'                      : dict(visible='@IsShowModeInstrumentDetail'),
             'leg_payCalendar'                          : dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation'                            : dict(onChanged='@OnQuotationChanged',
                                                              visible='@IsShowModeInstrumentDetail'),
             'ins_settlementType'                       : dict(label='Settlement'),
             'trade_price'                              : dict(visible=True),
             'trade_premium'                            : dict(visible=True)
            }
        )   
        
    def CurrencyEnabled(self, attributeName):
        return self.Leg().IsEnabled('Currency')
        
    def InstrumentPanes(self):
        return 'CustomPanes_Autocallable'
        
    def TradePanes(self):
        return 'CustomPanes_AutocallableTrade'
'''
def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
'''
