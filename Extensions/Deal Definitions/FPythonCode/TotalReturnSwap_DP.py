import acm
from DealDevKit import DealDefinition, Settings, NoOverride
from CompositeAttributesLib import CashFlowInstrumentDefinition, InstrumentPropertiesDefinition, InstrumentIDDefinition, LegDefinition, CashFlowDefinition, TradeDefinition, TradeBODefinition, AddInfoDefinition, InstrumentRegulatoryInfoDefinition, TradeIDDefinition, TradeRegulatoryInfoDefinition
from DealSTI import DealSTI
 
@DealSTI('TotalReturnSwap') 
@Settings(SheetDefaultColumns=['Multi Leg Label', 'Portfolio Present Value', 'Fixed Rate', 'Par Rate', 'Float Spread', 'Par Spread', 'Portfolio Delta Yield'])   
class TotalReturnSwapDefinition(DealDefinition):

    ins                 = CashFlowInstrumentDefinition( instrument="Instrument" )
    
    insProperties       = InstrumentPropertiesDefinition( instrument="Instrument" )
    
    insID               = InstrumentIDDefinition( instrument="Instrument")

    tradeID             = TradeIDDefinition( trade="Trade")

    insRegulatoryInfo   = InstrumentRegulatoryInfoDefinition(insRegInfo="InstrumentRegulatoryInfo")

    payLeg              = LegDefinition( leg='PayLeg', trade='Trade' )
    
    recLeg              = LegDefinition( leg='ReceiveLeg', trade='Trade' )
    
    payCashFlows        = CashFlowDefinition( leg='PayLeg', trade='Trade')
    
    recCashFlows        = CashFlowDefinition( leg='ReceiveLeg', trade='Trade')
    
    trade               = TradeDefinition( trade='Trade', showBuySell=False )
    
    tradeBackOffice     = TradeBODefinition ( trade='Trade' )
    
    insAddInfo          = AddInfoDefinition( obj='Instrument' )
    
    tradeAddInfo        = AddInfoDefinition( obj='Trade' )
    
    tradeRegulatoryInfo = TradeRegulatoryInfoDefinition(tradeRegInfo="TradeRegulatoryInfo")

    # Attribute overrides
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            {
                'ins_currency': dict(onChanged='@OnInstrumentCurrencyChanged'),
                'ins_discountingType': dict(visible='@DiscountingTypeVisible'),
                'ins_dividendFactor': dict(label='Div Factor',
                                                               visible='@DividendFactorVisible'),
                'ins_quotation': dict(onChanged='@OnQuotationChanged',
                                                               visible='@IsShowModeInstrumentDetail'),
                'ins_settlementType': dict(label='Settlement'),
                'insProperties_spotBankingDaysOffset': dict(onChanged='@OnInstrumentSpotDaysChanged'),
                'payLeg_calculationPeriodDateRule': dict(visible='@RollOffsetVisible'),
                'payLeg_currency': dict(label='',
                                                               width=9),
                'payLeg_dayCountMethod': dict(visible='@DayCountVisible'),
                'payLeg_initialRate': dict(label='Initial Price',
                                                               visible='@InitialPriceVisible',
                                                               maxWidth=500),
                'recLeg_calculationPeriodDateRule': dict(visible='@RollOffsetVisible'),
                'recLeg_currency': dict(label='',
                                                               width=9),
                'recLeg_dayCountMethod': dict(visible='@DayCountVisible'),
                'recLeg_initialRate': dict(label='Initial Price',
                                                               visible='@InitialPriceVisible',
                                                               maxWidth=500),
                'recLeg_priceInterpretationType': dict(visible='@PriceInterpretationTypeVisible'),
                'trade_premium': dict(visible=True),
                'trade_price': dict(visible=True),
                'trade_salesCoverViceVersaPrice': dict(visible=False),
                'trade_suggestDiscountingType': dict(visible='@DiscountingTypeVisible'),
            }
        )  

    # Visible Callbacks
    def DiscountingTypeVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().DiscountingType()
        
    def DayCountVisible(self, attributeName):
        if attributeName == 'payLeg_dayCountMethod':
            return self.IsShowModeDetail() or self.PayLeg().LegType() != 'Total Return'
        if attributeName == 'recLeg_dayCountMethod':
            return self.IsShowModeDetail() or self.ReceiveLeg().LegType() != 'Total Return'
            
    def DividendFactorVisible(self, attributeName):
        for leg in self.Instrument().Legs():
            if leg.LegType()=='Total Return' and leg.FloatRateReference():
                if leg.FloatRateReference().InsType() != 'Bond':
                    return self.IsShowModeDetail()
        return False

    def InitialPriceVisible(self, attributeName):
        if attributeName == 'payLeg_initialRate':
            return self.PayLeg().LegType() == 'Total Return'
        if attributeName == 'recLeg_initialRate':
            return self.ReceiveLeg().LegType() == 'Total Return'
            
    def PriceInterpretationTypeVisible(self, attributeName):
        for leg in self.Instrument().Legs():
            if leg.LegType()=='Total Return' and leg.FloatRateReference():
                if leg.FloatRateReference().InsType() not in ['Stock', 'EquityIndex']:
                    return self.IsShowModeDetail()
        return False
                    
    def RollOffsetVisible(self, attributeName):
        if attributeName == 'payLeg_calculationPeriodDateRule':
            if self.PayLeg().LegType() != 'Total Return' and self.ReceiveLeg().LegType() == 'Total Return':
                return NoOverride
        if attributeName == 'recLeg_calculationPeriodDateRule':
            if self.ReceiveLeg().LegType() != 'Total Return' and self.PayLeg().LegType() == 'Total Return':
                return NoOverride
                
        
    # Util
    def InstrumentPanes(self):
        return 'CustomPanes_TotalReturnSwap'
        
    def TradePanes(self):
        return 'CustomPanes_TotalReturnSwapTrade'
 
        
def UpdateDefaultInstrument(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.UpdateLegFixedRateOrSpread()
