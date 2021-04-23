import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import DerivativeInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, FxForwardTradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
 
@Settings(SheetApplicable=False)   
class FXForwardDefinition(DealDefinition):

    ins                 = DerivativeInstrumentDefinition( instrument='Instrument', trade='Trade' )
    
    insProperties       = InstrumentPropertiesDefinition( instrument='Instrument' )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo='InstrumentRegulatoryInfo')

    trade               = FxForwardTradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo='TradeRegulatoryInfo')

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_discountingType': dict(onChanged='@OnDiscountingTypeChanged'),
             'ins_quotation': dict(onChanged='@OnQuotationChanged'),
             'ins_fixingSource': dict(label='Fixing Src'),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'insProperties_priceFindingChlItem': dict(visible='@IsShowModeInstrumentDetail'),
             'trade_price': dict(visible=True,
                                                               formatter='InstrumentDefinitionFxPrice'),
             'trade_referencePrice': dict(formatter='InstrumentDefinitionFxPrice'),
             'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
            }
        )            
    
    def OnSave(self, saveConfig):
        self.Trade().SuggestBaseCurrencyEquivalent()
        DealDefinition.OnSave(self, saveConfig)
        
    #OnChanged
    def OnDiscountingTypeChanged(self, *args):    
        self.Trade().UpdateFxForwardPrice()
        self.trade_price = self.Trade().Price()
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_FXForward'
        
    def TradePanes(self):
        return 'CustomPanes_FXForwardTrade'
        
def UpdateDefaultInstrument(ins):
    ins.SettlementType = 'Physical Delivery'
    ins.UnderlyingType = 'Curr'
    ins.Underlying = None
    ins.PayType = 'Forward'
    ins.ContractSize = 1
    ins.PayOffsetMethod = 'Calendar Days'

