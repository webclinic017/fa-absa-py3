import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import DerivativeInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Future/Forward') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor', 'Portfolio Underlying Forward Price'])   
class FutureDefinition(DealDefinition):

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
            {'ins_currency'                                     : dict(onChanged='@OnInstrumentCurrencyChanged',
                                                                       label='@FutureCurrencyLabel'),
             'ins_discountingType'                              : dict(visible='@DiscountingTypeVisible'),
             'ins_fixingSource'                                 : dict(label='Exp Cutoff'),
             'ins_issuer'                                       : dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation'                                    : dict(onChanged='@OnQuotationChanged'),
             'ins_strikeCurrency'                               : dict(label='Ccy2'),
             'ins_underlying'                                   : dict(label='@FutureUnderlyingLabel'),
             'ins_quantoOptionType'                             : dict(choiceListSource=['None', 'Quanto']),
             'insProperties_spotBankingDaysOffset'              : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'trade_price'                                      : dict(visible=True),
             'trade_suggestDiscountingType'                     : dict(visible='@DiscountingTypeVisible'),
             'trade_valueDay'                                   : dict(visible='@ValueDayVisible')
            }
        )    
    # Visible Callbacks
    def DiscountingTypeVisible(self, attributeName):
        if self.Instrument().DiscountingType():
            return True
        elif self.IsShowModeDetail() and self.ins_underlying:
            if self.ins_payType != 'Contingent':
                if self.ins_underlying.InsType() not in ['ETF', 'CFD']:
                    return True
        else:
            return False
            
    def ValueDayVisible(self, attributeName):
        return (self.IsShowModeDetail2() or not self.Trade().Instrument().PayType() in ['Forward', 'Contingent'])
        
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_Future'
        
    def TradePanes(self):
        return 'CustomPanes_FutureTrade'
        
    def IsUnderlyingCurr(self):
        return 'Curr' == str(self.Instrument().UnderlyingType())
    
    def IsQuantoTypeQuanto(self):
        return 'Quanto' == str(self.Instrument().QuantoOptionType())
    
    # Label Callbacks
    def FutureCurrencyLabel(self, attributeName):
        if self.IsUnderlyingCurr():
            if self.IsQuantoTypeQuanto() and self.IsUnderlyingCurr():
                return 'Settle Curr'
            else:
                return 'Ccy2'
        else:
            return 'Currency'
    
    def FutureUnderlyingLabel(self, attributeName):
        return 'Ccy1' if self.IsUnderlyingCurr() else 'Underlying'
