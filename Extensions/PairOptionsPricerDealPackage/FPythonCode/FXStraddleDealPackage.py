import acm
from FxStrategyDealPackageBase import FxStrategyDealPackageBase
from PairOptionsUtil import SetFXTradeAndInstrumentAttributes, GetMaxMinBounderiesStrikeSolving, GetFloatFromCalculation
from DealPackageDevKit import CalcVal


class FXStraddleDefinition(FxStrategyDealPackageBase):
    strategyTypeDisplayName =  'Straddle'
    
    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, AttrCalc, AttrCalcLeft, AttrLabelLeft, AttrLabelRight, LabelParam, Label
        from PairOptionsPricerGridViewModel import AttrLabelCalcLeft, LabelCalc, AttrLabelCalcRight
        
        intrinsicRow = Row([AttrCalc('intrinsicFwd'), AttrLabelLeft('intrinsicFwd'), Label('Intrinsic %'), AttrLabelRight('intrinsicSpot'), AttrCalcLeft('intrinsicSpot')])
        
        gridViewModel = super(FXStraddleDefinition, self)._gridModelView_default()
        gridViewModel.insert(5, intrinsicRow)
        return gridViewModel

          
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(FXStraddleDefinition, self).OnInit()
        self._pricingOptions = acm.FFxStraddlePricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateStraddle(self.DealPackage().TradeAt('callTrade'), self.DealPackage().TradeAt('putTrade'))
        
    def AssemblePackage(self):
        callTradeDeco = self.DealPackage().CreateTrade('FX Option', 'callTrade')
        putTradeDeco = self.DealPackage().CreateTrade('FX Option', 'putTrade')
        SetFXTradeAndInstrumentAttributes(callTradeDeco)   
        SetFXTradeAndInstrumentAttributes(putTradeDeco)   
        callTradeDeco.Instrument().OptionType('Call')
        putTradeDeco.Instrument().OptionType('Put')
        self.PricingOptions().CreateStraddle(callTradeDeco, putTradeDeco)

    '''*******************************************************
    * Solver methods
    *******************************************************'''    
    def GetStrikeParams(self, fwdPrice):
        params = GetMaxMinBounderiesStrikeSolving(fwdPrice)
        paramsUpper = params.copy()
        params["maxValue"] = fwdPrice
        paramsUpper["minValue"] = fwdPrice
        return [params, paramsUpper]
    
    def StrikeParamDomPerFor(self, attributeName):
        fwdPrice = GetFloatFromCalculation(self.quoteTradeCalcVal_fwd)
        return self.GetStrikeParams(fwdPrice)
        
    def StrikeParamForPerDom(self, attributeName):
        fwdPrice = GetFloatFromCalculation(self.flippedQuoteTradeCalcVal_fwd)
        return self.GetStrikeParams(fwdPrice)
    
    def TransformDelta(self, name, newDelta):
        return super(FxStrategyDealPackageBase, self).TransformDelta(name, newDelta)
        
    def TransformFlippedDelta(self, name, newDelta):
        return super(FxStrategyDealPackageBase, self).TransformFlippedDelta(name, newDelta)
    
    '''*************************************************************'''
    def SetDefaultStrike(self):
        self.DealPackage().SetAttribute('solverStrikeDomPerFor', '0d')
