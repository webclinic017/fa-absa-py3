
import acm
import FUxCore
from DealPackageDevKit import DealPackageException, DealPackageUserException, CalcVal, Object, DealPackageChoiceListSource, InstrumentPart

from CompositeOptionComponents import GenericUnderlyingOption
from CompositeBasketComponents import Basket
from CompositeExoticComponents import Barrier, Rainbow, Asian
import inspect
from functools import partial


class BasketOption(GenericUnderlyingOption):
    
    def Attributes(self):
        attributeDict = super(BasketOption, self).Attributes()

        attributeDict['underlying'] = Basket( basketName         = self.UniqueCallback('Basket'),
                                              displayColumns     = self._basketColumns,
                                              basketUpdateAction = self._basketUpdateAction,
                                              totalBasketValue   = self._totalBasketValue)

        return attributeDict

    def AttributeOverrides(self, overrideAccumulator):
            overrideAccumulator(
                        {'quantoType': 
                                dict(visible = self.UniqueCallback('@VisibleQuantoTypeMulti'),
                                     onChanged = self.UniqueCallback('@SetFixFxRate'))
                                } )

    def VisibleQuantoTypeMulti(self, attrName, *rest):
        for combLink in self.underlying_instruments:
            if combLink.Instrument().Currency() != self.GetMethod(self._optionName)().Currency():
                return True
        return self.GetMethod('IsShowModeDetail')()

    def SetFixFxRate(self, *rest):
        if self.quantoType == 'Quanto' and self.Option().FixFxRate() == 0.0:
            self.Option().FixFxRate(1.0)

    def CreateInstrument(self, optionType = 'Option', existingBasket = None):
        ins = super(BasketOption, self).CreateInstrument(optionType)
        if existingBasket:
            assert existingBasket.IsKindOf(acm.FEquityIndex), 'Existing basket must be an equity index'
            und = existingBasket
        else:
            und = Basket.CreateInstrument()
            und.Quotation('Per Unit')
        ins.Underlying(und)
        return ins

    def OnInit(self, optionName, basketName, basketColumns = None, basketUpdateAction = None, totalBasketValue = None, **kwargs):
        self._optionName = optionName
        self._basketName = basketName
        self._basketColumns = basketColumns
        self._basketUpdateAction = basketUpdateAction
        self._totalBasketValue = totalBasketValue
        
    def Basket(self):
        return self.GetMethod(self._basketName)()

    def Option(self):
        return self.GetMethod(self._optionName)()

    def IsValid(self, exceptionAccumulator, aspect, allowExotic = False):
        super(BasketOption, self).IsValid(exceptionAccumulator, aspect, allowExotic)
        
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:
            # Make sure thet the option underlying is a basket
            if insToValidate.Underlying() is None:
                exceptionAccumulator.ValidationError('Option must have an underlying')
            if not insToValidate.Underlying().IsKindOf(acm.FCombination):
                exceptionAccumulator.ValidationError('A basket option must have an underlying that represents a basket')


class BasketExoticOption(BasketOption):

    def CreateInstrument(self, optionType = 'Option', existingBasket = None):
        ins = super(BasketExoticOption, self).CreateInstrument(optionType, existingBasket)
        ins.CreateExotic()
        return ins

    def IsValid(self, exceptionAccumulator, aspect):
        super(BasketExoticOption, self).IsValid(exceptionAccumulator, aspect, True)

class BasketBarrierOption(BasketExoticOption):

    def Attributes(self):
        attributeDict = super(BasketBarrierOption, self).Attributes()

        attributeDict['barrier'] = Barrier( optionName    = self._optionName )
        
        return attributeDict
        
class BasketRainbowOption(BasketExoticOption):    

    def Attributes(self):
        attributeDict = super(BasketRainbowOption, self).Attributes()

        attributeDict['rainbow'] = Rainbow( optionName    = self._optionName )
        
        return attributeDict

class BasketRainbowBarrierOption(BasketExoticOption):    

    def Attributes(self):
        attributeDict = super(BasketRainbowBarrierOption, self).Attributes()

        attributeDict['rainbow'] = Rainbow( optionName    = self._optionName )
        attributeDict['barrier'] = Barrier( optionName    = self._optionName )
        
        return attributeDict


class BasketAsianOption(BasketExoticOption):

    def Attributes(self):
        attributeDict = super(BasketAsianOption, self).Attributes()

        attributeDict['asian'] = Asian( optionName    = self._optionName,
                                        underlyingName = self._basketName, 
                                        eventTypes = self._eventTypes,
                                        showEventsAsButton = self._showEventsAsButton,
                                        eventLabel = self._eventLabel,
                                        eventUpdateAction = self._eventUpdateAction,
                                        eventDisplayColumns = self._eventColumns,
                                        mustBeAsian = True )
        return attributeDict

    def OnInit(self, optionName, 
                     basketName, 
                     basketColumns = None, 
                     basketUpdateAction = None,
                     totalBasketValue = None, 
                     eventTypes = ['Average strike', 'Average price'],
                     showEventsAsButton = True,
                     eventLabel = 'Average Fixings',
                     eventColumns = None,
                     eventUpdateAction = None,
                     **kwargs):
        
        super(BasketAsianOption, self).OnInit(optionName, basketName, basketColumns, basketUpdateAction, totalBasketValue)

        self._eventTypes = eventTypes
        self._showEventsAsButton = showEventsAsButton
        self._eventLabel = eventLabel
        self._eventUpdateAction = eventUpdateAction
        self._eventColumns = eventColumns


