import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import OptionInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition, ExoticDefinition
from DealSTI import DealSTI
 
@DealSTI('Warrant') 
@Settings(SheetDefaultColumns=['Price Theor', 'Portfolio Underlying Future Method Price', 'Portfolio Underlying Forward Price', 'Portfolio Volatility', 'Portfolio Carry Cost', 'Portfolio Discount Rate', 'Time to Carry', 'Time to Expiry', 'Time to Discount', 'Instrument Delta', 'Instrument Gamma', 'Instrument Vega', 'Dividend Forward Value'])   

class WarrantDefinition(DealDefinition):

    ins                 = OptionInstrumentDefinition( instrument='Instrument', trade='Trade' )
    
    insProperties       = InstrumentPropertiesDefinition( instrument='Instrument' )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")

    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")
    
    exotic              = ExoticDefinition( instrument='Instrument', trade='Trade' )

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency'                                     : dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_discountingType'                              : dict(visible='@DiscountingTypeVisible'),
             'ins_fixingSource'                                 : dict(label='Exp Cutoff'),
             'ins_issuer'                                       : dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation'                                    : dict(onChanged='@OnQuotationChanged'),
             'ins_strikeCurrency'                               : dict(enabled='@StrikeCurrencyEnabled'),
             'ins_barrier'                                      : dict(visible='@IsBarrier'),
             'ins_rebate'                                       : dict(visible='@IsBarrier'),
             'insProperties_spotBankingDaysOffset'              : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'trade_price'                                      : dict(visible=True),
             'trade_premium'                                    : dict(visible=True),
             'trade_suggestDiscountingType'                     : dict(visible='@DiscountingTypeVisible')
            }
        )    
    # Visible Callbacks
    def DiscountingTypeVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().DiscountingType()
        
    def IsBarrier(self, attributeName):
        return self.Instrument().IsBarrier()
        
    def StrikeCurrencyEnabled(self, attributeName):
        return self.Instrument().QuantoOptionType() == 'Custom' or self.ins_underlyingType == 'Curr'
    
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_Warrant'
        
    def TradePanes(self):
        return 'CustomPanes_WarrantTrade'
