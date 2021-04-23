
from DealPackageDevKit import CompositeAttributeDefinition, CalcVal, ParseFloat

class SetCallbacksToClass(object):
    def __init__(self, inherited, base):
        self._inherited = inherited
        self._base = base
    def __enter__(self):
        self._name = self._inherited.get_name()
        self._inherited.set_name(self._base.get_name())
    def __exit__(self, type, value, traceback):
        self._inherited.set_name(self._name)


class OneVolVolatility(CompositeAttributeDefinition):
    def OnInit(self, quoteTradeName, callVolObjectsName, putVolObjectsName):
        self._quoteTradeName = quoteTradeName
        self._callVolObjectsName = callVolObjectsName
        self._putVolObjectsName = putVolObjectsName
        
    def Attributes(self):
        return {'volatility':           CalcVal(label = 'Vol %',
                                                calcMapping=self.QuoteTradeName() + ':FDealSheet:Portfolio One Volatility',
                                                onChanged='@SimulateVolatility',
                                                transform='@TransformVolatility',
                                                solverParameter='@VolatilityParam'),
                                            
                'callVolatility':       CalcVal(label='@CallVolatilityLabel',
                                                calcMapping=self.CallVolObjectsNameName() + ':FDealSheet:Portfolio Volatility FXOStrat',
                                                onChanged='@ValueSimulated|UnsimulateOneVolatility',
                                                transform='@TransformVolatility',
                                                solverParameter='@VolatilityParam'),

                'putVolatility':        CalcVal(label='@PutVolatilityLabel',
                                                calcMapping=self.PutVolObjectsNameName() + ':FDealSheet:Portfolio Volatility FXOStrat',
                                                onChanged='@ValueSimulated|UnsimulateOneVolatility',
                                                transform='@TransformVolatility',
                                                solverParameter='@VolatilityParam')
                } if self.CallVolObjectsNameName() else {}
    '''*******************************************************
    * 1Vol get methods
    *******************************************************'''                                
    def QuoteTradeName(self):
        return self._quoteTradeName

    def CallVolObjectsNameName(self):
        return self._callVolObjectsName

    def PutVolObjectsNameName(self):
        return self._putVolObjectsName


class OneVolatility(OneVolVolatility):
    def OnInit(self, quoteTradeName, saveTradeName, altQuoteTradeName = None, saveTradeFlippedName = None, callVolObjectsName = None, putVolObjectsName = None):
        OneVolVolatility.OnInit(self, quoteTradeName, callVolObjectsName, putVolObjectsName)
        self._altQuoteTradeName = altQuoteTradeName
        self._saveTradeName = saveTradeName
        self._flippedSide = None
        if saveTradeFlippedName:
            self._flippedSide = OneVolatility( 'Flipped%s' % quoteTradeName,
                                                saveTradeFlippedName,
                                               'Flipped%s' % altQuoteTradeName if altQuoteTradeName else '')
            self._flippedSide.set_name('flipped')
            
    def DeltaAttributes(self, callBackName, suffix = ''):
        return {'deltaBS%s'%suffix:     CalcVal(label='Delta BS (1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=callBackName + ':FDealSheet:Instrument Delta One Vol FXOStrat',
                                                transform=self.UniqueCallback('@SolveOneVolDelta'),
                                                solverTopValue=True),

                'deltaBS%sCall'%suffix: CalcVal(label='Delta BS Call(1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=callBackName + ':FDealSheet:Instrument Delta Call One Vol FXOStrat',
                                                solverTopValue='solverStrike2DomPerFor'),

                'deltaBS%sPut'%suffix:  CalcVal(label='Delta BS Call(1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=callBackName + ':FDealSheet:Instrument Delta Put One Vol FXOStrat',
                                                solverTopValue='solverStrikeDomPerFor')
                } if callBackName else {}

    def FwdDeltaAttributes(self):
        return {'fwdDeltaBS':           CalcVal(label='Fwd Delta BS(1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=self.SaveTradeName() + ':FDealSheet:Instrument Forward Delta One Vol FXOStrat',
                                                transform=self.UniqueCallback('@SolveOneVolDelta'),
                                                solverTopValue=True),

                'fwdDeltaBSCall':       CalcVal(label='Fwd Delta BS Call(1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=self.SaveTradeName() + ':FDealSheet:Instrument Forward Delta Call One Vol FXOStrat',
                                                solverTopValue='solverStrike2DomPerFor'),

                'fwdDeltaBSPut':        CalcVal(label='Fwd Delta BS Put(1Vol)',
                                                calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                                calcMapping=self.SaveTradeName() + ':FDealSheet:Instrument Forward Delta Put One Vol FXOStrat',
                                                solverTopValue='solverStrikeDomPerFor')
               }
    
    def FlippedAttributes(self):
        attrs = {}
        if self._flippedSide:
            with SetCallbacksToClass(self._flippedSide, self):
                flippedAttributes = self._flippedSide.Attributes()
            for attr, trait in flippedAttributes.items():
                attrs[self._flippedSide.PrefixedName(attr)] = trait
        return attrs
    
    def Attributes(self):    
        attrs = OneVolVolatility.Attributes(self)
        attrs.update(self.DeltaAttributes(self.QuoteTradeName()))
        attrs.update(self.DeltaAttributes(self.AltQuoteTradeName(), 'Alt'))
        attrs.update(self.FwdDeltaAttributes())
        attrs.update(self.FlippedAttributes())
        return attrs
     
     
    '''*******************************************************
    * 1Vol get methods
    *******************************************************'''                                        
    def AltQuoteTradeName(self):
        return self._altQuoteTradeName
        
    def SaveTradeName(self):
        return self._saveTradeName

    def SolveOneVolDelta(self, attrName, value):
        # slow solver, first creating one copy and then each solver in the loop will create an own copy of that copy
        # code should be optimized to do all solving operations in the same deal package copy
        precision = 0.0001
        maxIterations = 5
        dpCopy = self.Owner().DealPackage().Copy()
        dpCopy.SetAttribute('bidAskMode', False)
        dpCopy.Refresh()
        
        callAttr = attrName + 'Call'
        putAttr = attrName + 'Put'
        
        callSolverParam = self.Owner().GetAttributeMetaData(callAttr, 'solverTopValue')()
        putSolverParam = self.Owner().GetAttributeMetaData(putAttr, 'solverTopValue')()
        
        callValue = ParseFloat(value, formatter=dpCopy.GetAttribute(callAttr))
        
        if (dpCopy.GetAttribute(callAttr).Value().Number() > 0) != (callValue > 0):
            callValue = -callValue
        putValue = -callValue
        
        for i in range(maxIterations):
            dpCopy.SetAttribute('solverParameter', callSolverParam)
            dpCopy.SetAttribute(callAttr, callValue)
            dpCopy.SetAttribute('solverParameter', putSolverParam)
            dpCopy.SetAttribute(putAttr, putValue)
        
            if abs(dpCopy.GetAttribute(callAttr).Value().Number() - callValue) <= precision:
                break
        else:
            print (callAttr, dpCopy.GetAttribute(callAttr).Value(), putAttr, dpCopy.GetAttribute(putAttr).Value())
            raise DealPackageException("No solution found for '%s' that gives expected '%s' of %s. "
                                        "(Using boundary conditions precision = %f, max iterations = %d)."
                                        %('strikes', attrName, value, precision, maxIterations))
        
        for attribute in ('strikeDomesticPerForeign', 'strike2DomesticPerForeign'):
            self.Owner().SetAttribute(attribute, dpCopy.GetAttribute(attribute))
        return self.Owner().GetValueToStore(attrName, dpCopy.GetAttribute(attrName).Value())
        
