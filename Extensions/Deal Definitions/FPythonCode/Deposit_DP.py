import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, AddInfoDefinition, TradeBODefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Deposit')
@Settings(SheetDefaultColumns=['Portfolio Theoretical Value', 'Portfolio Delta Yield', 'Fixed Rate'])   
class DepositDefinition(DealDefinition):
    
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
             'insProperties_exCouponMethod': dict(visible='@IsShowModeInstrumentDetail'),
             'insProperties_exCouponPeriod': dict(visible='@IsShowModeInstrumentDetail'),
             'trade_suggestDiscountingType': dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation': dict(visible='@IsShowModeInstrumentDetail',
                                                               onChanged='@OnQuotationChanged'),
             'ins_discountingType': dict(visible='@IsShowModeInstrumentDetail'),
             'ins_openEnd': dict(visible='@IsShowModeInstrumentDetail'), 
             'ins_noticePeriod': dict(visible='@IsShowModeInstrumentDetail'),
             'leg_interestPaymentTime': dict(onChanged='@OnInterestPaymentTimeChanged'),
             'leg_payCalendar': dict(visible='@IsShowModeInstrumentDetail'),
             'trade_flatAccrued': dict(visible='@IsShowModeTradeDetail'),
             'trade_openNominal': dict(label='Open Amount'),
             'trade_price': dict(visible='@IsShowModeTradeDetail'),
             'trade_tradeCategory': dict(visible='@IsShowModeTradeDetail'),
             'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
            }
        )   
        
    def InstrumentPanes(self):
        return 'CustomPanes_Deposit'
        
    def TradePanes(self):
        return 'CustomPanes_DepositTrade'
