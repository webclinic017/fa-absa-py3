
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, CompositeAttributeDefinition, ValGroupChoices, InstrumentPart
from SP_DealPackageHelper import GetFxFormatter
from CompositeOptionAdditionComponents import StrikePctSingle, BarrierPctSingle
from CompositeExoticComponents import Barrier
from CompositeComponentBase import CompositeBaseComponent

from SP_DealPackageHelper import GetInitialFixingValue, GetInitialFixingDate, SetInitialFixingValue, SetInitialFixingDate, SetInitialFixingUnderlying, SettlementTypeChoices, BarrierTypeChoices, OptionTypeChoices, BarrierMonitoringChoices

class OptionBase(CompositeBaseComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def Attributes(self):
 
        attributeDict = {

                    'optionType'    : Object ( objMapping = InstrumentPart(self._optionName + ".OptionType"),
                                               label = 'Option Type',
                                               toolTip = 'Specify if the option is Call or Put',
                                               choiceListSource = self.UniqueCallback("@ChoicesOptionType") ),
                    
                    'settlementType': Object ( objMapping = InstrumentPart(self._optionName + ".SettlementType"),
                                               label = 'Settlement Type',
                                               toolTip = 'Cash or physical settlement',
                                               choiceListSource = self.UniqueCallback("@ChoicesSettlementType") ),

                    'quotation'     : Object ( objMapping = InstrumentPart(self._optionName + ".Quotation"),
                                               label = 'Quotation',
                                               toolTip = 'Quotation',
                                               choiceListSource = self.UniqueCallback("@QuotationChoices") ),

                    # Detailed view
                                               
                    'valuationGroup' : Object ( objMapping = InstrumentPart(self._optionName + '.ValuationGrpChlItem'),
                                                label = 'Val Group',
                                                toolTip = 'Valuation Group',
                                                visible = self.UniqueCallback("@IsShowModeDetail"),
                                                choiceListSource = ValGroupChoices() ),
                    
                    'settleDays'     : Object ( objMapping = InstrumentPart(self._optionName + '.PayDayOffset'),
                                                label = 'Settle Days',
                                                toolTip = 'Pay offset between expiry and pay day',
                                                visible = self.UniqueCallback("@IsShowModeDetail") ),
                    
                    'quantoType'     : Object ( objMapping = InstrumentPart(self._optionName + '.QuantoOptionType'),
                                                label = 'Quanto',
                                                toolTip = 'Quanto Type',
                                                visible = self.UniqueCallback("@VisibleQuantoType") )

                }
        
        return attributeDict

    def OnInit(self, optionName, **kwargs):
        self._optionName = optionName

    def CreateInstrument(self, optionType = 'Option'):
        ins = acm.DealCapturing().CreateNewInstrument(optionType)
        # Set values that we never want to take from the default instrument
        ins.Otc(True)
        ins.MtmFromFeed(False)
        return ins

    def ChoicesSettlementType(self, attrName, *rest):
        return SettlementTypeChoices(self.GetMethod(self._optionName)())

    def ChoicesOptionType(self, attrName, *rest):
        return OptionTypeChoices(self.GetMethod(self._optionName)())

    def QuotationChoices(self, attributeName):
        return self.GetMethod(self._optionName)().DefaultQuotations()

    def VisibleQuantoType(self, attrName, *rest):
        return (self.GetMethod('IsShowModeDetail')() 
                or 
                self.GetMethod(self._optionName)().Currency() != self.GetMethod(self._optionName)().StrikeCurrency() )

    def IsValid(self, exceptionAccumulator, aspect, allowExotic = False):
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            # Check instrument type:
            if insToValidate.InsType() != 'Option':
                exceptionAccumulator('Instrument type for option component must be option.')
            
            # Check that option is OTC
            if not insToValidate.Otc():
                exceptionAccumulator('Option must be OTC')
                        
            # Check that there are no exotic features - unless called from an exotic subclass
            if (not allowExotic) and insToValidate.ExoticType() == 'Other':
                exceptionAccumulator('Option must be without exotic features')


# ### Base FX Option
class FxOption(OptionBase):

    def Attributes(self):

        attributeDict = super(FxOption, self).Attributes()

        attributeDict['foreignCurrency']            = Object ( objMapping = InstrumentPart(self._optionName + ".ForeignCurrency"),
                                                               label = 'Foreign Currency',
                                                               toolTip = 'Foreign Currency' )
        
        attributeDict['domesticCurrency']           = Object ( objMapping = InstrumentPart(self._optionName + ".DomesticCurrency"),
                                                               label = 'Domestic Currency',
                                                               toolTip = 'Domestic Currency' )

        attributeDict['strikeForeignPerDomestic']   = Object ( objMapping = InstrumentPart(self._optionName + ".StrikeForeignPerDomestic" ),
                                                               label = 'Strike Foreign Per Domestic',
                                                               toolTip = 'Strike price expressed as foreign currency per domestic currency',
                                                               formatter = self.UniqueCallback('@FXRateFormatter') )
        
        attributeDict['strikeDomesticPerForeign']   = Object ( objMapping = InstrumentPart(self._optionName + ".StrikeDomesticPerForeign" ),
                                                               label = 'Strike Domestic Per Foreign',
                                                               toolTip = 'Strike price expressed as domestic currency per foreign currency',
                                                               formatter = self.UniqueCallback('@FXRateInverseFormatter') )
        
        attributeDict['expiryDate']                 = Object ( objMapping = InstrumentPart(self._optionName + ".FxoExpiryDate"),
                                                               label = "Expiry Date",
                                                               toolTip = 'Expiry Date' )
        
        attributeDict['fixingSource']               = Object ( objMapping = InstrumentPart(self._optionName + ".FixingSource"),
                                                               label = 'Fixing Source',
                                                               toolTip = 'Fixing Source' )

        return attributeDict


    def CreateInstrument(self):
        return super(FxOption, self).CreateInstrument('FX Option')

    # FX Rate formatters
    
    def FXRateInverseFormatter(self, *args):
        return GetFxFormatter(self.foreignCurrency, self.domesticCurrency)
        
    def FXRateFormatter(self, *args):
        return GetFxFormatter(self.domesticCurrency, self.foreignCurrency)

class GenericUnderlyingOption(OptionBase):
    # This class is used both my single and multi underlying options

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def Attributes(self):

        attributeDict = super(GenericUnderlyingOption, self).Attributes()
    
        attributeDict['strikePrice']    = Object ( objMapping = InstrumentPart(self._optionName + ".StrikePrice"),
                                                   label = 'Strike Price',
                                                   toolTip = 'Strike Price',
                                                   transform = self.UniqueCallback('@TransformStrikePrice'),
                                                   solverParameter = self.UniqueCallback('@SolverParametersStrikePrice'),
                                                   backgroundColor = '@SolverColor' )
                                                                                            
        attributeDict['contractSize']   = Object ( objMapping = InstrumentPart(self._optionName + ".ContractSize"),
                                                   label = 'Contract Size',
                                                   toolTip = 'Contract Size' )
                                               
        attributeDict['expiry']         = Object ( objMapping = InstrumentPart(self._optionName + ".ExpiryDateTime"),
                                                   label = 'Expiry',
                                                   toolTip = 'Expiry',
                                                   transform = self.UniqueCallback("@TransformExpiry") )
        
        return attributeDict


    # -----------------------------------------------
    # ##### Attribute callbacks that carry out
    # ##### specific tasks
    # -----------------------------------------------

    def TransformStrikePrice(self, attrName, value):
        return self.TransformSolver(attrName, value)

    def SolverParametersStrikePrice(self, attrName, *rest):
        return [{'minValue':0.01, 'maxValue':10000}]
                
    def TransformExpiry(self, attrName, value):
        if acm.Time().PeriodSymbolToDate(value):
            value = self.GetMethod(self._optionName)().ExpiryDateFromPeriod(value)
        return value

    # -----------------------------------------------
    # ##### Utility functions
    # -----------------------------------------------
    def SetStrikePrice(self, value):
        self.strikePrice = value
    
# ### Base single option composite class ###
class Option(GenericUnderlyingOption):
    # This is the basic single underlying option

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def Attributes(self):

        attributeDict = super(Option, self).Attributes()
    
                                              
        attributeDict['underlying']     = Object ( objMapping = InstrumentPart(self.UniqueCallback("UnderlyingMapping")),
                                                   choiceListSource = self.UniqueCallback('@ChoicesUnderlying'),
                                                   validate = self.UniqueCallback("@ValidateUnderlying"),
                                                   label = 'Underlying',
                                                   toolTip = 'Underlying instrument',
                                                   domain = acm.FInstrument )
                                              
        return attributeDict

    def OnInit(self, optionName, undType = acm.FInstrument, **kwargs):
        if not (hasattr(undType, 'IsSubtype') and undType.IsSubtype('FInstrument')):
            raise DealPackageException('Variable undType has to be an ACM instrument class')
        super(Option, self).OnInit(optionName)
        self._undType = undType
    
    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------

    def CreateInstrument(self, optionType = 'Option'):
        ins = super(Option, self).CreateInstrument(optionType)
        # Make sure that the underlying is of the correct instrument type
        if not (ins.Underlying() and ins.Underlying().IsKindOf(self._undType)):
            if len(self.ChoicesUnderlying(None)) == 0:
                raise DealPackageException('Cannot create create Option without any %s available in the database' % self._undType.Name())
            acm.FBusinessLogicDecorator.WrapObject(ins).Underlying(self.ChoicesUnderlying(None)[0])
        # Set values that we never want to take from the default instrument
        ins.StrikeType('Absolute')
        ins.ExerciseType('European')
        ins.PayType('Spot')
        return ins

    # -----------------------------------------------
    # ##### Methods for object mappings #####
    # -----------------------------------------------

    def UnderlyingMapping(self, value = '*Reading*'):
        if value == '*Reading*':
            return self.GetMethod(self._optionName)().Underlying()
        else:
            spotDays = self.GetMethod(self._optionName)().SpotBankingDaysOffset()
            self.GetMethod(self._optionName)().Underlying(value)
            self.GetMethod(self._optionName)().SpotBankingDaysOffset(spotDays)

    # -----------------------------------------------
    # ##### Attribute callbacks that carry out
    # ##### specific tasks
    # -----------------------------------------------

    def ChoicesUnderlying(self, attrName, *rest):
        return self._undType.Instances()

    def ValidateUnderlying(self, attrName, value):
        # This check is needed as error in FDerivative::StoredStrike is
        # thrown if no correct underlying is set
        if isinstance(value, str):
            value = acm.FInstrument[value]
            
        if not (value and value.IsKindOf(acm.FInstrument)):
            raise DealPackageUserException( 'Invalid underlying instrument' )

    # -----------------------------------------------
    # ##### Other class methods ###### #
    # -----------------------------------------------

    def IsValid(self, exceptionAccumulator, aspect, allowExotic = False):
    
        super(Option, self).IsValid(exceptionAccumulator, aspect, allowExotic)
    
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            # Check that exercise type is european
            if insToValidate.ExerciseType() != 'European':
                exceptionAccumulator('Exercise Type must be European')
            
            # Check that strike type is Absolute
            if insToValidate.StrikeType() != 'Absolute':
                exceptionAccumulator('Strike Type must be Absolute')
           
            # Check that pay type is Spot
            if insToValidate.PayType() != 'Spot':
                exceptionAccumulator('Pay Type must be Spot')

            # Check underlying type
            if not insToValidate.Underlying().IsKindOf(self._undType):
                exceptionAccumulator('Underlying must be of type %s' 
                                                      % self._undType.Name())


def _PctStrikeOverrides(obj):
    return { 'strikePrice' :  dict(enabled = False,
                                   solverParameter = False),
             'expiry'      :  dict(validate = obj.UniqueCallback("@ValidateExpiry")),
             'underlying'  :  dict(onChanged = obj.UniqueCallback("@SetInitialFixingUnderlying|SetInitialFixingToMarket")),
             'settleDays'  :  dict(enabled = False),
             'quotation'   :  dict(defaultValue = 'Per Contract')
             }

class OptionPctStrike(Option):

    def Attributes(self):
        attributeDict = super(OptionPctStrike, self).Attributes()
            
        attributeDict['pctStrike'] = StrikePctSingle(self._optionName,
                                                     self.UniqueCallback('SetStrikePrice'))
        
        return attributeDict

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(_PctStrikeOverrides(self))

    def OnNew(self):
        if self.pctStrike_initialFixing_initialFixing:
            if self.pctStrike_strikePricePct:
                self.strikePrice = self.pctStrike_strikePricePct * self.pctStrike_initialFixing_initialFixing

    def ValidateExpiry(self, attrName, value):
        validationInitialFixing = self.pctStrike.initialFixing.TransformInitialFixingDate('initialFixingDate', self.pctStrike_initialFixing_initialFixingDate)
        self.pctStrike.initialFixing.ValidateInitialFixingAndExpiry(validationInitialFixing, value)

    def SetInitialFixingUnderlying(self, *rest):
        SetInitialFixingUnderlying(self.GetMethod(self._optionName)(), self.underlying)

    def SetInitialFixingToMarket(self, attrName, oldValue, newValue, *rest):
        self.pctStrike.initialFixing.SetInitialFixingToMarket(attrName, oldValue, newValue)

    @classmethod
    def SetUp(self, definitionsSetUp):
        StrikePctSingle.SetUp(definitionsSetUp)


class BarrierOption(Option):

    def Attributes(self):
        attributeDict = super(BarrierOption, self).Attributes()

        attributeDict['barrier'] = Barrier(self._optionName)

        return attributeDict

    def CreateInstrument(self, optionType = 'Option'):
        ins = super(BarrierOption, self).CreateInstrument(optionType)
        ins.CreateExotic()
        return ins

    def SetBarrierLevel(self, value):
        self.barrier_barrierLevel = value

    def IsValid(self, exceptionAccumulator, aspect):
        super(BarrierOption, self).IsValid(exceptionAccumulator, aspect, True)


class BarrierOptionPctStrike(BarrierOption):

    def Attributes(self):
        attributeDict = super(BarrierOptionPctStrike, self).Attributes()

        attributeDict['pctBarrier'] = BarrierPctSingle(self._optionName,
                                                       self.UniqueCallback('SetStrikePrice'),
                                                       self.UniqueCallback('SetBarrierLevel') )

        return attributeDict

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(_PctStrikeOverrides(self))
        overrideAccumulator({'barrier_barrierLevel' : dict(enabled = False,
                                                           solverParameter = False)})

    def OnNew(self):
        if self.pctBarrier_initialFixing_initialFixing:
            if self.pctBarrier_strikePricePct:
                self.strikePrice = self.pctBarrier_strikePricePct * self.pctBarrier_initialFixing_initialFixing
            if self.pctBarrier_barrierLevelPct:
                self.barrier_barrierLevel = self.pctBarrier_barrierLevelPct * self.pctBarrier_initialFixing_initialFixing

    def ValidateExpiry(self, attrName, value):
        validationInitialFixing = self.pctBarrier.initialFixing.TransformInitialFixingDate('initialFixingDate', self.pctBarrier_initialFixing_initialFixingDate)
        self.pctBarrier.initialFixing.ValidateInitialFixingAndExpiry(validationInitialFixing, value)

    def SetInitialFixingUnderlying(self, *rest):
        SetInitialFixingUnderlying(self.GetMethod(self._optionName)(), self.underlying)

    def SetInitialFixingToMarket(self, attrName, oldValue, newValue, *rest):
        self.pctBarrier.initialFixing.SetInitialFixingToMarket(attrName, oldValue, newValue)

    @classmethod
    def SetUp(self, definitionsSetUp):
        BarrierPctSingle.SetUp(definitionsSetUp)

