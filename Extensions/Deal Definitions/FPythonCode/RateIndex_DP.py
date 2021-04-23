import acm
from DealDevKit import DealDefinition, Settings
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, AddInfoDefinition, TradeIDDefinition, TradeDefinition
from DealSTI import DealSTI
 
@DealSTI('RateIndex')
@Settings(SheetDefaultColumns=['Instrument Market Price', 'Price Theor'])   
class RateIndexDefinition(DealDefinition):
    
    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    leg                 = LegDefinition( leg='Leg', trade='Trade' )
    
    trade               = TradeDefinition( trade='Trade' )    
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
       
    # Attribute override
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {'ins_startPeriod'                          : dict(label='Start Period'),
             'ins_endPeriod'                            : dict(label='End Period'),
             'ins_underlying'                           : dict(enabled='@UnderlyingEnabled',
                                                               visible='@UnderlyingVisible'),
             'ins_underlyingType'                       : dict(visible='@UnderlyingVisible'),
             'leg_payDayMethod'                         : dict(label='Day Method'),
             'leg_resets_resetCalendar'                 : dict(label='Res Cal 1'),
             'ins_quotation'                            : dict(visible='@IsShowModeInstrumentDetail'),
             'insID_categoryChlItem'                    : dict(visible=False),
             'insID_productTypeChlItem'                 : dict(visible=False)
            }
        )
        
        
    # Enabled callbacks
    def UnderlyingEnabled(self, *args):
        return self.ins_underlyingType == 'RateIndex'
        
    # Visible callbacks
    def UnderlyingVisible(self, *args):
        return self.UnderlyingEnabled() or self.IsShowModeInstrumentDetail()
        
        
    def InstrumentPanes(self):
        return 'CustomPanes_RateIndex'

    #OnSave override to not save trade
    def OnSave(self, saveConfig): 
        saveConfig.DealPackage("Exclude")
        DealDefinition.OnSave(self, saveConfig)
