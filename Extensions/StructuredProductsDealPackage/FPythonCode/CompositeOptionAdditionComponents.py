
import acm
import FUxCore
from CompositeComponentBase import CompositeBaseComponent
from SP_DealPackageHelper import AddExoticEvent
from SP_DealPackageHelper import GetInitialFixingValue, GetInitialFixingDate, SetInitialFixingValue, SetInitialFixingDate, SetInitialFixingUnderlying, SettlementTypeChoices, BarrierTypeChoices, OptionTypeChoices, BarrierMonitoringChoices, RainbowTypeChoices, BarrierStatusChoices
from functools import partial
from DealPackageDevKit import DealPackageException, DealPackageUserException, Object, InstrumentPart, ReturnDomainDecorator

class InitialFixingBase(CompositeBaseComponent):

    def Attributes(self):
    
        return {

            'initialFixing'     : Object ( objMapping = InstrumentPart(self.UniqueCallback("InitialFixingValue")),
                                           label = 'Initial Fixing',
                                           toolTip = 'The initial fixing value' ),

            'initialFixingDate' : Object ( objMapping = InstrumentPart(self.UniqueCallback("InitialFixingDate")),
                                           validate = self.UniqueCallback("@ValidateInitialFixingDate"),
                                           label = 'Initial Fixing Date',
                                           toolTip = 'The initial fixing date',
                                           transform = self.UniqueCallback("@TransformInitialFixingDate") )

            }

    def InitialFixingValue(self, value = '*READING*'):
        raise DealPackageException('Method InitialFixingValue not implemented')

    def InitialFixingDate(self, value = '*READING*'):
        raise DealPackageException('Method InitialFixingDate not implemented')

    def OnInit(self, optionName, **kwargs):
        self._optionName = optionName

    def Option(self):
        return self.GetMethod(self._optionName)()

    def ValidateInitialFixingDate(self, attrName, value):
        self.ValidateInitialFixingAndExpiry(value, self.GetMethod(self._optionName)().ExpiryDateTime())
    
    def TransformInitialFixingDate(self, attrName, value):
        if acm.Time().PeriodSymbolToDate(value):
            value = self.GetMethod(self._optionName)().ExpiryDateFromPeriod(value)
        return value

    def ValidateInitialFixingAndExpiry(self, initialFixingDate, expiryDate):
        if acm.Time().DateDifference(initialFixingDate, expiryDate) >= 0:
            raise DealPackageUserException( 'Expiry must be after initial fixing' )

    def GetInitialFixingEvents(self):
        return self.GetMethod(self._optionName)().GetExoticEventsOfKind('Initial Fixing')

    @classmethod
    def SetUp(self, definitionsSetUp):
        from DealPackageSetUp import ChoiceListSetUp
        definitionsSetUp.AddSetupItems(
                                    ChoiceListSetUp(
                                        list    = 'Exotic Event Types',
                                        entry   = 'Initial Fixing',
                                        descr   = 'Initial Fixing'
                                        ))

class InitialFixingSingle(InitialFixingBase):

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
                {'initialFixing': 
                            dict(validate= self.UniqueCallback("@ValidateInitialFixing"))})

    def OnNew(self):
        if self.initialFixing == -1.0:
            # No default value set for initial fixing, set it to market price
            self.SetInitialFixingToMarket(None, None, None)
        if self.initialFixing == -1.0:
            # No market price available, default to 1.0
            self.initialFixing = 1.0

    def Underlying(self):
        return self.Option().Underlying()

    @ReturnDomainDecorator('double')
    def InitialFixingValue(self, value = '*Reading*'):
        if value == '*Reading*':
            return GetInitialFixingValue(self.GetMethod(self._optionName)(), self.Underlying())
        else:
            SetInitialFixingValue(self.GetMethod(self._optionName)(), self.Underlying(), value)

    def ValidateInitialFixing(self, attrName, value):
        if not (value and value >= 0.0):
            raise DealPackageUserException( 'Initial fixing must be greater than 0' )

    @ReturnDomainDecorator('date')
    def InitialFixingDate(self, value = '*Reading*'):
        if value == '*Reading*':
            return GetInitialFixingDate(self.GetMethod(self._optionName)(), self.Underlying())
        else:
            SetInitialFixingDate(self.GetMethod(self._optionName)(), self.Underlying(), value)

    def SetInitialFixingToMarket(self, attrName, oldValue, newValue, *rest):
        if self.Underlying():
            price = self.Underlying().Calculation().MarketPrice(self.GetMethod("_GetStdCalcSpace")()).Value()
            if (price and price.Number() > 0.0):
                self.initialFixing = price.Number()

    def IsValid(self, exceptionAccumulator, aspect):

        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            # make sure that there is one initial fixing event
            if len(insToValidate.GetExoticEventsOfKind('Initial Fixing')) != 1:
                exceptionAccumulator('Option must have exactly one initial fixing event')


class InitialFixingMulti(InitialFixingBase):

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
                {'initialFixing': 
                            dict(columns = [ {'methodChain': 'Instrument.VerboseName', 'label': 'Instrument'},
                                             {'methodChain': 'EventValue',    'label': 'Initial Fixing'}
                                           ])})


    @ReturnDomainDecorator('FPersistentSet(FExoticEvent)')
    def InitialFixingValue(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.GetInitialFixingEvents()

    @ReturnDomainDecorator('date')
    def InitialFixingDate(self, value = '*Reading*'):
        events = self.GetInitialFixingEvents()
        if value == '*Reading*':
            if len(events) > 0:
                return self.GetInitialFixingEvents()[0].Date()
            else:
                return acm.Time.DateNow()
        else:
            for event in events:
                event.Date(value)

    def IsValid(self, exceptionAccumulator, aspect):
        # Validate that all initial fixing events have the same date
        dateFound = None
        for event in self.GetInitialFixingEvents():
            if dateFound is None:
                dateFound = event.Date()
            if dateFound != event.Date():
                exceptionAccumulator('All initial fixing events must have the same date')

    def RemoveInitialFixing(self, underlying):
        events = self.GetInitialFixingEvents()
        for event in events:
            if event.ComponentInstrument() == underlying:
                event.Unsimulate()

    def AddInitialFixing(self, underlying):
        AddExoticEvent(self.GetMethod(self._optionName)(), underlying, 'Initial Fixing', self.initialFixingDate, -1)

    def SetInitialFixingToMarket(self, underlying = None):
        events = self.GetInitialFixingEvents()
        for event in events:
            if underlying is not None and event.ComponentInstrument() != underlying:
                continue
            price = event.ComponentInstrument().Calculation().MarketPrice(self.GetMethod("_GetStdCalcSpace")()).Value()
            if (price and price.Number() > 0.0):
                event.EventValue(price.Number())

    def IsValid(self, exceptionAccumulator, aspect):

        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            # make sure that there is one initial fixing event
            if len(insToValidate.GetExoticEventsOfKind('Initial Fixing')) != len(insToValidate.Underlying().Instruments()):
                exceptionAccumulator('Option must have exactly one initial fixing event per underlying instrument')

# ######################################################################################
# Custom methods on combination link in order to display 
# the initial fixing ans performarnce since fixing as part of basket values

# NOTE: To use these method, the basket has to be added to the instrument package!

def InitialFixingMethodValidation(combMap, methodName):

    basket = combMap.Combination()
    underlying = combMap.Instrument()
    if basket is None:
        return None

    instrumentPackageLinks = basket.DealPackageInstrumentLinks()
    assert len(instrumentPackageLinks) == 1, 'Method %s on FCombInstrMap can only be used if the basket is part of exactly one instrument package' % methodName

    option = instrumentPackageLinks[0].InstrumentPackage().InstrumentAt('Option')
    assert option is not None, 'Method %s on FCombInstrMap can only be used if the instrumetn package of the basket also contains an option' % methodName

    events = [e for e in option.GetExoticEventsOfKind('Initial Fixing') if e.ComponentInstrument() == underlying]
    assert len(events) == 1, 'Method %s on FCombInstrMap can only be used if instrument package option contains the equivalent Initial Fixing exotic event' % methodName

    return events[0]

def InitialFixing(combMap, value = '*READ*'):

    event = InitialFixingMethodValidation(combMap, 'InitialFixing')

    if not event:
        return

    if value == '*READ*':
        return event.EventValue()
    else:
        event.EventValue(value)

def PerformanceSinceInitialFixing(combMap):
    
    event = InitialFixingMethodValidation(combMap, 'PerformanceSinceInitialFixing')

    if not event:
        return

    if event.EventValue() > 0.0:
        _calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        marketPrice = event.ComponentInstrument().Calculation().MarketPrice(
                                                _calcSpace).Value()

        if marketPrice and marketPrice.Number():
            return (marketPrice.Number() - event.EventValue()) / event.EventValue()

    return 0.0

class StrikePctSingle(CompositeBaseComponent):

    def Attributes(self):

        return {

            'strikePricePct' :    Object( objMapping = InstrumentPart(self._optionName + ".AdditionalInfo.StrikePricePct"),
                                          onChanged = self.UniqueCallback("@SetStrikeFromInitialFixingAndPctStrike"),
                                          label = 'Strike Price (%)',
                                          toolTip = 'Strike price expressed in percent of initial fixing',
                                          defaultValue = 1.0,
                                          formatter = "PercentShowZero",
                                          transform = self.UniqueCallback('@TransformStrikePrice'),
                                          solverParameter = self.UniqueCallback('@SolverParametersStrikePricePct'),
                                          backgroundColor = '@SolverColor'),

            'initialFixing'  :    InitialFixingSingle( self._optionName )

            }

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({'initialFixing_initialFixing' : dict(onChanged=self.UniqueCallback('@SetStrikeFromInitialFixingAndPctStrike'))
                            })
        
    def OnInit(self, optionName, setStrike, **kwargs):
        self._optionName = optionName
        self._setStrike = setStrike

    def TransformStrikePrice(self, attrName, value):
        return self.TransformSolver(attrName, value)

    def SolverParametersStrikePricePct(self, attrName, *rest):
        return [{'minValue':0.01, 'maxValue':200}]

    def SetStrikeFromInitialFixingAndPctStrike(self, *rest):
        self.GetMethod(self._setStrike)(self.strikePricePct * self.initialFixing_initialFixing)


    # -----------------------------------------------------
    # Set up method
    # -----------------------------------------------------
    @classmethod
    def SetUp(self, definitionsSetUp):
        InitialFixingSingle.SetUp(definitionsSetUp)
        from DealPackageSetUp import AddInfoSetUp, ChoiceListSetUp
        definitionsSetUp.AddSetupItems(
                                    AddInfoSetUp(
                                        recordType      = 'Instrument',
                                        fieldName       = 'StrikePricePct',
                                        dataType        = 'Double',
                                        description     = 'Strike price in % of initial fixing',
                                        dataTypeGroup   = 'Standard',
                                        subTypes        = ['Option'],
                                        defaultValue    = 1.0,
                                        mandatory       = False
                                        ))

    def IsValid(self, exceptionAccumulator, aspect, allowExotic = False):

        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            # Check that strike price is equal to strike % * initial fixing
            initialFixing = GetInitialFixingValue(insToValidate, insToValidate.Underlying())
            strikePercent = insToValidate.AdditionalInfo().StrikePricePct()
            if abs(insToValidate.StrikePrice() - (initialFixing * strikePercent)) > 0.001:
                exceptionAccumulator('The absolute strike price must agree to initial fixing and strike price percent')



class BarrierPctSingle(StrikePctSingle):

    def Attributes(self):
        
        attributes = super(BarrierPctSingle, self).Attributes()
        
        attributes['barrierLevelPct'] = Object (objMapping = InstrumentPart(self._optionName + ".AdditionalInfo.BarrierLevelPct"),
                                                onChanged = self.UniqueCallback("@SetBarrierFromInitialFixingAndPctBarrier"),
                                                label = 'Barrier (%)',
                                                toolTip = 'Barrier level expressed in percent of initial fixing',
                                                solverParameter = self.UniqueCallback('@SolverParametersBarrierLevelPct'),
                                                backgroundColor = '@SolverColor',
                                                formatter = 'PercentShowZero',
                                                transform = self.UniqueCallback("@TransformBarrierLevelPct"),
                                                defaultValue = 1.0 )
        
        return attributes

    def OnInit(self, optionName, setStrike, setBarrier, **kwargs):
        super(BarrierPctSingle, self).OnInit(optionName, setStrike)
        self._setBarrier = setBarrier

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({'initialFixing_initialFixing' : dict(onChanged=self.UniqueCallback('@SetBarrierFromInitialFixingAndPctBarrier'))
                            })

    def SetBarrierFromInitialFixingAndPctBarrier(self, *rest):
        self.GetMethod(self._setBarrier)(self.barrierLevelPct * self.initialFixing_initialFixing)
    
    def SolverParametersBarrierLevelPct(self, attrName, *rest):
        return [{'minValue':0.01, 'maxValue':200}]
    
    def TransformBarrierLevelPct(self, attrName, value):
        return self.TransformSolver(attrName, value)

    # -----------------------------------------------------
    # Set up method
    # ---------------------------------------------------
    @classmethod
    def SetUp(self, definitionsSetUp):
        from DealPackageSetUp import AddInfoSetUp
        super(BarrierPctSingle, self).SetUp(definitionsSetUp)
        definitionsSetUp.AddSetupItems(
                                AddInfoSetUp(
                                    recordType      = 'Instrument',
                                    fieldName       = 'BarrierLevelPct',
                                    dataType        = 'Double',
                                    description     = 'Barrier Level in % of initial fixing',
                                    dataTypeGroup   = 'Standard',
                                    subTypes        = ['Option'],
                                    defaultValue    = 1.0,
                                    mandatory       = False
                            ))


