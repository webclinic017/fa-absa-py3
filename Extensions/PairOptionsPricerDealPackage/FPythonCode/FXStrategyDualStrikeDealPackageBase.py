import acm
from FxStrategyDealPackageBase import FxStrategyDealPackageBase
from DealPackageDevKit import Object, CalcVal

class FXStrategyDualStrikeDealPackageBase(FxStrategyDealPackageBase):
    strike2DomesticPerForeign = Object( label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.Strike2DomesticPerForeign',
                                        transform='@TransformStrikePrice',
                                        formatter='@StrikeFormatterCB',
                                        recreateCalcSpaceOnChange=True)
        
    strike2ForeignPerDomestic = Object( label='@StrikeForPerDomLabel',
                                        objMapping='PricingOptions.Strike2ForeignPerDomestic',
                                        transform='@TransformStrikePrice',
                                        formatter='@StrikeFormatterInverseCB',
                                        recreateCalcSpaceOnChange=True)
        
    solverStrike2DomPerFor =    Object( label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.Strike2DomesticPerForeignNoInputFormatter',
                                        solverParameter='@StrikeParamDomPerFor',
                                        onChanged='@SolverStrikeChanged')
                                     
    solverStrike2ForPerDom =    Object( label='@StrikeForPerDomLabel',
                                        objMapping='PricingOptions.Strike2ForeignPerDomesticNoInputFormatter',
                                        solverParameter='@StrikeParamForPerDom',
                                        onChanged='@SolverStrikeChanged')
                                            
    intrinsic2Fwd =             CalcVal(label='Fwd',
                                        calcMapping='CallQuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True)
                                        
    intrinsic2Spot =            CalcVal(label='Spot',
                                        calcMapping='CallQuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)

    deltaCall =                 CalcVal(label='Delta Call',
                                        calcMapping='ForeignStrategyOrTradeGreek:FDealSheet:Instrument Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                            
    deltaFlippedCall =          CalcVal(label='Delta Call',
                                        calcConfiguration='@DomesticColumnConfig',
                                        calcMapping='DomesticStrategyOrTradeGreek:FDealSheet:Instrument Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                            
    deltaPut =                  CalcVal(label='Delta Put',
                                        calcMapping='ForeignStrategyOrTradeGreek:FDealSheet:Instrument Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                            
    deltaFlippedPut =           CalcVal(label='Delta Put',
                                        calcConfiguration='@DomesticColumnConfig',
                                        calcMapping='DomesticStrategyOrTradeGreek:FDealSheet:Instrument Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
    
    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, Attr, AttrLabelLeft, AttrLabelMidBold, AttrLabelRight, AttrLeft
        strike2Row = Row([Attr('strike2DomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strike2DomesticPerForeign'), AttrLabelRight('flippedQuoteTradeCalcVal_theor'), AttrLeft('strike2ForeignPerDomestic')])        
        gridViewModel = super(FXStrategyDualStrikeDealPackageBase, self)._gridModelView_default()
        gridViewModel.insert(5, strike2Row)
        return gridViewModel
       
    '''*******************************************************
    * Label methods
    *******************************************************'''  
    def StrikeDomPerForLabel(self, attrName):
        if attrName == 'strike2DomesticPerForeign':
            return 'Call Strike'
        else:
            return 'Put Strike'
            
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''    
    def LeadTradeName(self):
        return 'putTrade' if abs(self.amountPutForeign or 0) < abs(self.amountCallForeign or 0) else 'callTrade'
        
    def CallStrike(self):
        return self.strike2DomesticPerForeign
        
    '''*************************************************************'''
    def SetDefaultStrike(self):
        self.DealPackage().SetAttribute('strikeDomesticPerForeign', '-2p')
        self.DealPackage().SetAttribute('strike2DomesticPerForeign', '-2p')

    def GetDeltaTraitsList(self):
        return ['deltaCall', 'deltaFlippedCall', 'deltaPut', 'deltaFlippedPut']
