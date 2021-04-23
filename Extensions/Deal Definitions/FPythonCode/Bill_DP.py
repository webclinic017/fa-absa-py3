import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('Bill') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Market Price YTM', 'Price Theor', 'Portfolio Theoretical Value', 'Portfolio Delta Yield'])   
class BillDefinition(DealDefinition):

    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")
    
    leg                 = LegDefinition( leg='Leg', trade='Trade' )
    
    legCashFlows        = CashFlowDefinition( leg='Leg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade' )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")    
    
    def OnOpen(self):
        self.trade.OnOpen()
    
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency'                                     : dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_startDate'                                    : dict(onChanged='@OnInstrumentStartDateChanged'),
             'insProperties_spotBankingDaysOffset'              : dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_discountingType'                              : dict(visible='@IsShowModeInstrumentDetail'),
             'ins_quotation'                                    : dict(visible='@IsShowModeInstrumentDetail',
                                                                       onChanged='@OnQuotationChanged'),
             'ins_refPrice'                                     : dict(label='Issue Price'),
             'leg_rollingPeriod'                                : dict(label='YTM Period',
                                                                       visible='@IsShowModeInstrumentDetail'),
             'leg_payDayMethod'                                 : dict(label='Day Method'),
             'trade_price'                                      : dict(visible=True),
             'trade_premium'                                    : dict(visible=True)
            }
        )    
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_Bill'
        
    def TradePanes(self):
        return 'CustomPanes_BillTrade'
