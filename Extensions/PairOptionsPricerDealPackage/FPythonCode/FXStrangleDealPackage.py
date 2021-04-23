import acm
from FXStrategyDualStrikeDealPackageBase import FXStrategyDualStrikeDealPackageBase
from PairOptionsUtil import SetFXTradeAndInstrumentAttributes, lot
from PairOptionsOneVolatility import OneVolatility
from DealPackageDevKit import Object, CalcVal
from DealPackageUtil import DealPackageException


class FXStrangleDefinition(FXStrategyDualStrikeDealPackageBase):
    strategyTypeDisplayName =  'Strangle'

    oneVol =                        OneVolatility(quoteTradeName='QuoteCombinationTrade',
                                                altQuoteTradeName='AltQuoteCombinationTrade',
                                                saveTradeName='ForeignStrategyOrTradeGreek',
                                                saveTradeFlippedName='DomesticStrategyOrTradeGreek',
                                                callVolObjectsName='VolatilityCallObjectsAsLot',
                                                putVolObjectsName='VolatilityPutObjectsAsLot')
                                                

    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, Attr, AttrLeft, AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrCalcLeft, AttrLabelLeft, AttrLabelRight, AttrLabelMarketDataLeft, AttrLabelMarketDataRight, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import AttrLabelCalcLeft, AttrLabelCalcRight, AttrActionForeignCurr, AttrActionDomesticCurr, AttrLabelMidBold, Label, LabelCalc, LabelParam, AttrCalcMarketDataLot, AttrCalcMarketDataLotLeft
        
        deltaBSRow = Row([AttrCalc('oneVol_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta (1-Vol)'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBS'), AttrCalcLeft('oneVol_flipped_deltaBS')])
        fwdDeltaRow = Row([AttrCalc('oneVol_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_delta'), LabelCalc('Fwd Delta (1-Vol)'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_delta'), AttrCalcLeft('oneVol_flipped_fwdDeltaBS')])
        deltaAltRow = Row([AttrCalc('oneVol_deltaBSAlt'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBSAlt'), LabelCalc('Delta (1-Vol)'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBSAlt'), AttrCalcLeft('oneVol_flipped_deltaBSAlt')])
        deltaOptRow = Row([AttrCalc('oneVol_deltaBSCall'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Call    |    Put'), AttrLabelCalcRight('quoteTradeCalcVal_deltaBS'), AttrCalcLeft('oneVol_deltaBSPut')])
        deltaOptAltRow = Row([AttrCalc('oneVol_deltaBSAltCall'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBSAlt'), LabelCalc('Call   Alt   Put'), AttrLabelCalcRight('quoteTradeCalcVal_deltaBSAlt'), AttrCalcLeft('oneVol_deltaBSAltPut')])
        deltaOptFlippedRow = Row([AttrCalc('oneVol_flipped_deltaBSCall'), AttrLabelCalcLeft('flippedQuoteTradeCalcVal_deltaBS'), LabelCalc('Call Flipped Put'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBS'), AttrCalcLeft('oneVol_flipped_deltaBSPut')])
        deltaOptFlippedAltRow = Row([AttrCalc('oneVol_flipped_deltaBSAltCall'), AttrLabelCalcLeft('flippedQuoteTradeCalcVal_deltaBSAlt'), LabelCalc('Call FlipAlt Put'), AttrLabelRight('flippedQuoteTradeCalcVal_deltaBSAlt'), AttrCalcLeft('oneVol_flipped_deltaBSAltPut')])
        volatilityRow = Row([AttrCalcMarketData('oneVol_volatility'), AttrLabelMarketDataLeft('oneVol_volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')])
        putCallVolRow = Row([AttrCalcMarketDataLot('oneVol_callVolatility'), AttrLabelMarketDataLeft('oneVol_callVolatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('oneVol_putVolatility'), AttrCalcMarketDataLotLeft('oneVol_putVolatility')])
        
        gridViewModel = super(FXStrangleDefinition, self)._gridModelView_default()
        gridViewModel[14] = volatilityRow
        gridViewModel[18] = deltaBSRow
        gridViewModel[19] = deltaAltRow
        #gridViewModel.insert(15, deltaOptFlippedAltRow)
        #gridViewModel.insert(15, deltaOptFlippedRow)
        #gridViewModel.insert(15, deltaOptAltRow)
        #gridViewModel.insert(15, deltaOptRow)
        gridViewModel.insert(15, putCallVolRow)
        gridViewModel[21] = fwdDeltaRow
        
        return gridViewModel

    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(FXStrangleDefinition, self).OnInit()
        self._pricingOptions = acm.FFxStranglePricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateStrangle(self.DealPackage().TradeAt('callTrade'), self.DealPackage().TradeAt('putTrade'))
        
    def AssemblePackage(self):
        callTradeDeco = self.DealPackage().CreateTrade('FX Option', 'callTrade')
        putTradeDeco = self.DealPackage().CreateTrade('FX Option', 'putTrade')
        SetFXTradeAndInstrumentAttributes(callTradeDeco)   
        SetFXTradeAndInstrumentAttributes(putTradeDeco)   
        callTradeDeco.Instrument().OptionType('Call')
        putTradeDeco.Instrument().OptionType('Put')
        self.PricingOptions().CreateStrangle(callTradeDeco, putTradeDeco)
    
    def IsVolatilitySimulated(self):
        retVal = False
        for volatility in ['oneVol_callVolatility', 'oneVol_putVolatility', 'oneVol_volatility']:
            if self.GetAttributeMetaData(volatility, 'isCalculationSimulated')():
                retVal = True
        return retVal
        
    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def TransformVolatility(self, attrName, value):
        if attrName is not "volatility":
            if value in ('', None):
                self.bidAskModeVol = self.bidAskMode
            elif isinstance(value, str) and len(value.split('/')) == 2:
                self.bidAskModeVol = True
            else:
                self.bidAskModeVol = False
        return self.TransformBidAskSplit(attrName, value)
