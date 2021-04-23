import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CombinationInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition

from DealSTI import DealSTI
 
@DealSTI('EquityIndex') 
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class EquityIndexDefinition(DealDefinition):

    ins                 = CombinationInstrumentDefinition( instrument="Instrument" )
    
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
            {'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
             'ins_quotation': dict(onChanged='@OnQuotationChanged'),
             'ins_underlyings': dict(columns='@EquityIndexColumns'),
             'ins_editDialogDefinition': dict(defaultValue="""
                                                                                    selectedCIM_Ins;
                                                                                    selectedCIM_FixFxRate;
                                                                                    selectedCIM_Weight;
                                                                                    """),
             'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
             'trade_price': dict(visible=True),
             'trade_premium': dict(visible=True),
            }
        )  

    # Columns
    def EquityIndexColumns(self, *args):
        return [{'methodChain': 'Instrument.VerboseName', 'label': 'Insid'},
                {'methodChain': 'Instrument.InsType',     'label': 'Ins Type'},
                {'methodChain': 'Instrument.Currency',    'label': 'Curr'},
                {'methodChain': 'FixFxRate',              'label': 'Fix FX Rate'},
                {'methodChain': 'Weight',                 'label': 'Weight', 'formatter': 'Imprecise'}]
    
    # Util     
    def InstrumentPanes(self):
        return 'CustomPanes_EquityIndex'
        
    def TradePanes(self):
        return 'CustomPanes_EquityIndexTrade'
