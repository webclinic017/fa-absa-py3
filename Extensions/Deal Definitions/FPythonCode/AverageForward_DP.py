import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import AverageForwardInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, AddInfoDefinition, TradeBODefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Average Future/Forward')
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])
   
class AverageForwardDefinition(DealDefinition):
    
    ins                 = AverageForwardInstrumentDefinition( instrument="Instrument")
    
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
            {'ins_currency'                             : dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_startDate'                            : dict(onChanged='@OnInstrumentStartDateChanged'),
             'insProperties_spotBankingDaysOffset'      : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_contractSizeInQuotation'              : dict(visible=True),
             'ins_crossCurrencyCalculation'             : dict(visible='@CrossCurrencyVisible'),
             'ins_endDate'                              : dict(onChanged='@leg_UpdateRefInsChoices'),
             'leg_floatRefFXFixingDateRule'             : dict(visible='@FXFixingRuleVisible'),
             'leg_payOffset'                            : dict(visible=True),
             'leg_payDayMethod'                         : dict(visible=True),
             'leg_resets_resetType'                     : dict(enabled=False),
             'trade_price'                              : dict(visible=True),
             'trade_valueDay'                           : dict(visible='@IsShowModeTradeDetail')
            }
        )   
        
    def InstrumentPanes(self):
        return 'CustomPanes_AverageForward'
        
    def TradePanes(self):
        return 'CustomPanes_AverageForwardTrade'
        
    # Visible Callbacks
    def CrossCurrencyVisible(self, *args):
        if self.Leg().FloatRateReference():
            return self.Leg().FloatRateReference().Currency() != self.Instrument().Currency()
        else:
            return False
            
    def FXFixingRuleVisible(self, attributeName):
        return self.CrossCurrencyVisible() and self.Instrument().CrossCurrencyCalculation() == 'Average then convert'
        

def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
