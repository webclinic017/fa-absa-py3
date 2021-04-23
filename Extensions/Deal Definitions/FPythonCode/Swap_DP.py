import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Swap')
@Settings(SheetDefaultColumns=['Multi Leg Label', 'Portfolio Present Value', 'Fixed Rate', 'Par Rate', 'Float Spread', 'Par Spread', 'Portfolio Delta Yield'])   
class SwapDefinition(DealDefinition):

    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")

    payLeg              = LegDefinition( leg='PayLeg', trade='Trade' )
    
    recLeg              = LegDefinition( leg='ReceiveLeg', trade='Trade' )
    
    payCashFlows        = CashFlowDefinition( leg='PayLeg', trade='Trade')
    
    recCashFlows        = CashFlowDefinition( leg='ReceiveLeg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade', showBuySell=False )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")

    # Attribute overrides
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
                'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
                'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
                'ins_quotation': dict(onChanged='@OnQuotationChanged'),
                'trade_salesCoverViceVersaPrice': dict(visible=False),
                'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
            }
        )  

    # Util
    def InstrumentPanes(self):
        return 'CustomPanes_Swap'
        
    def TradePanes(self):
        return 'CustomPanes_SwapTrade'
 
        
def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
