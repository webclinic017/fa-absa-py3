import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import DerivativeInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition, ExoticDefinition, ExoticEvent
from DealSTI import DealSTI
 
@DealSTI('VolatilitySwap') 
@Settings(SheetDefaultColumns=['Price Theor', 'Price Theor Vol', 'Portfolio Underlying Price', 'Portfolio Carry Cost', 'Historical Variance', 'Future Variance', 'Instrument Delta'])   
class VolatilitySwapDefinition(DealDefinition):

    ins                 = DerivativeInstrumentDefinition( instrument='Instrument', trade='Trade' )
    
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
    
    exoticEvents        = ExoticEvent( optionName     = 'Instrument', 
                                       underlyingName = 'Underlying',
                                       eventTypes     = ['Price Fixing'],
                                       eventLabel     = 'Exotic Events...',
                                       showAsButton   = True,
                                       sizeToFit      = True)

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged',
                                                                       label='@CurrencyLabel'),
             'ins_discountingType': dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation': dict(onChanged='@OnQuotationChanged'),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_quantoOptionType': dict(choiceListSource=['None', 'Quanto']),
             'ins_strikeCurrency': dict(label='Ccy2'),
             'ins_underlying': dict(label='@UnderlyingLabel'),
             'trade_nominal_buySell': dict(visible='@IsShowModeTradeDetail'),
             'trade_nominal_value': dict(visible='@IsShowModeTradeDetail'),
             'trade_quantity_buySell': dict(visible='@IsShowModeTradeDetail'),
             'trade_quantity_value': dict(visible='@IsShowModeTradeDetail'),
             'trade_price': dict(visible='@IsShowModeTradeDetail'),
             'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
            }
        )    
    # Visible Callbacks
    def DiscountingTypeVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().DiscountingType()
        
        
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_VolatilitySwap'
        
    def TradePanes(self):
        return 'CustomPanes_VolatilitySwapTrade'
        
    def IsUnderlyingCurr(self):
        return 'Curr' == str(self.Instrument().UnderlyingType())
    
    def IsQuantoTypeQuanto(self):
        return 'Quanto' == str(self.Instrument().QuantoOptionType())

    # Label Callbacks
    def CurrencyLabel(self, attributeName):
        if self.IsUnderlyingCurr():
            if self.IsQuantoTypeQuanto() and self.IsUnderlyingCurr():
                return 'Settle Curr'
            else:
                return 'Ccy2'
        else:
            return 'Currency'
    
    def UnderlyingLabel(self, attributeName):
        return 'Ccy1' if self.IsUnderlyingCurr() else 'Underlying'
