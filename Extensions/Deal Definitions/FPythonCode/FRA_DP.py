import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('FRA') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Portfolio Present Value', 'Par Rate', 'Fixed Rate', 'Portfolio Delta Yield', 'Portfolio Forward Delta Yield'])   
class FRADefinition(DealDefinition):

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

    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'ins_quotation': dict(visible='@IsShowModeInstrumentDetail',
                                                                       onChanged='@OnQuotationChanged'),
             'leg_dayCountMethod': dict(visible='@IsShowModeInstrumentDetail'),
             'leg_payCalendar': dict(visible='@IsShowModeInstrumentDetail'),
             'leg_fixedRate': dict(visible=True),
             'leg_floatRateReference': dict(width=20),
             'leg_payDayMethod': dict(label='Day Method'),             
             'leg_resets_resetInArrear': dict(visible=False),
             'trade_valueDay': dict(visible='@IsShowModeTradeDetail'),
             'legCashFlows_cashFlows': dict(columns='@CashflowColumns'),
            }
        )    
    
    # Util
    def CashflowColumns(self,*args):
        columns=self.legCashFlows_Columns()
        del columns[7]
        columns.insert(7, {'methodChain': 'First.CashFlow.FloatRateOffset', 'label': 'Offset'})
        return columns
     
    def InstrumentPanes(self):
        return 'CustomPanes_FRA'
        
    def TradePanes(self):
        return 'CustomPanes_FRATrade'
        
def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
