import acm
from DealDevKit import DealDefinition, Settings, SalesTradingInteraction, ReturnDomainDecorator, Object
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, TradeIDDefinition, InstrumentRegulatoryInfoDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI

@DealSTI('CurrSwap') 
@Settings(SheetDefaultColumns=['Multi Leg Label', 'Portfolio Present Value', 'Fixed Rate', 'Par Rate', 'Float Spread', 'Par Spread', 'Portfolio Currency'])   
class CurrSwapDefinition(DealDefinition):

    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")
    
    tradeID             = TradeIDDefinition( trade="Trade")
    
    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")

    payLeg              = LegDefinition( leg='PayLeg', trade='Trade', showBuySell=False )
    
    recLeg              = LegDefinition( leg='ReceiveLeg', trade='Trade', showBuySell=False )
    
    payCashFlows        = CashFlowDefinition( leg='PayLeg', trade='Trade')
    
    recCashFlows        = CashFlowDefinition( leg='ReceiveLeg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade', showBuySell=False )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")
                                  
    currSwapRecNominal = Object( label='Rec Nom',
                                 objMapping='Trade.CurrSwapRecNominal',
                                 editable=False,
                                 visible='@IsShowModeTradeDetail')
                                 
    currSwapPayNominal = Object( label='Pay Nom',
                                 objMapping='Trade.CurrSwapPayNominal',
                                 editable=False,
                                 visible='@IsShowModeTradeDetail')                                 
    
    # Attribute overrides
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
                'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
                'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
                'ins_quotation': dict(visible='@IsShowModeInstrumentDetail', 
                                                               onChanged='@OnQuotationChanged'),
                'trade_salesCoverViceVersaPrice': dict(visible=False),
                'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
                'recLeg_currency': dict(label='',
                                                               width=6),
                'recLeg_nonDeliverableCurrency': dict(label='',
                                                               width=6),
                'payLeg_currency': dict(label='',
                                                               width=6),
                'payLeg_nonDeliverableCurrency': dict(label='',
                                                               width=6),                                                     
            }
        )  

    
    # Label Callbacks
    def CurrPair(self, attributeName):
        return self.PayLeg().Currency().Name() + '/' + self.ReceiveLeg().Currency().Name()
        
    # Editable Callbacks
    def FxRateEditable(self, attributeName):
        return self.Instrument().FixNominalLeg() != 'None'
    
    # Util
    def InstrumentPanes(self):
        return 'CustomPanes_CurrSwap'
        
    def TradePanes(self):
        return 'CustomPanes_CurrSwapTrade'
 
        
def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
