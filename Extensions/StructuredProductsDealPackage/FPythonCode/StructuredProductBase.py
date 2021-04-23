
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, Settings, UXDialogsWrapper, TradeActions, CorrectCommand, NovateCommand, CloseCommand, AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, CompositeAttributeDefinition, InstrumentPart, DealPart, ParseSuffixedFloat, ReturnDomainDecorator

from SP_DealPackageHelper import SafeDivision, AddFArrayItemToFDictionary

from CompositeTradeComponents import StructuredTradeInput

# ####################################################################################### #
# #                                                                                     # #
# # NOTE:                                                                               # #
# #                                                                                     # #
# # Any Deal Package that is using RegisterAlignmentAcrossComponents as well            # #
# # as implementing its own IsValid method MUST call super(myDpClass, self).IsValid()   # #
# # for the automatic validation of fields registersd to be aligned to be activated.    # #
# #                                                                                     # #
# ####################################################################################### #

class ComponentBasedDealPackage(DealPackageDefinition):

    def MapSolverTopValueToComponent(self, value, attrName, parameters):
        f = self.GetFormatter(attrName)
        # map([suffix], [keys])
        mappings = [
            (['C', 'COUPON', 'CO'], 
                ['coupon']),
            (['B', 'BARRIER', 'BA', 'BAR'], 
                ['barrierLevelPct', 'barrierLevel']),
            (['S', 'STR', 'STRIKE'],
                ['strikePricePct', 'strikePrice']),
            (['BSEC', 'SECOND', 'SEC'],
                ['doubleBarrierLevel'])
        ]
        
        for suffix, keys in mappings:
            goalValue = ParseSuffixedFloat(value, suffix=suffix, formatter=f)
            if goalValue is None:
                continue # Not candidate
            for key in keys:
                if key in parameters: # Match found
                    self.solverParameter = '_'.join([parameters[key], key])
                    return goalValue
        return value
        
    def TopValueFields(self):
        return {}

    def IsValid(self, exceptionAccumulator, aspect):
        # Validate that all fields that have been registered to be kept in sync
        # are not made "out of sync".
        if hasattr(self, '_alignFields'):
            failedPairs = acm.FDictionary()
            for attributeKey in self._alignFields.Keys().Sort():
                for dependentField in self._alignFields[attributeKey]:
                    if getattr(self, dependentField) != getattr(self, attributeKey):
                        if not self.HasAlreadyFoundFailedPair(failedPairs, attributeKey, dependentField):
                            exceptionAccumulator('Deal package fields %s and %s must be equal' %
                                                                 (attributeKey, dependentField) )
                            self.AddValidationFailedPair(failedPairs, attributeKey, dependentField)

    # ##################################################
    # Mapping methods with a general purpose
    # ##################################################

    @ReturnDomainDecorator('double')
    def SumOfTradePrices(self, value = '*Reading*'):
        if value == '*Reading*':
            price = 0.0
            for t in self.Trades():
                price += t.Price()
            return price

    @ReturnDomainDecorator('double')
    def SumOfPremiums(self, value = '*Reading*'):
        if value == '*Reading*':
            premium = 0.0
            premiumCurr = None
            for t in self.Trades():
                if premiumCurr is None:
                    premiumCurr = t.Currency()
                if premiumCurr != t.Currency():
                    raise DealPackageException("Cannot calculate a sum of premium for premiums defined in different currencies")
                premium += t.Premium()
            return premium

    # ##################################################
    # Functions for being able to link attribute updates
    # and to validate that they remian equal
    # ##################################################
    def AlignAcrossComponents(self, attrName, *rest):
        for dependentField in self._alignFields[attrName]:
            if getattr(self, dependentField) != getattr(self, attrName):
                setattr(self, dependentField, getattr(self, attrName))

    def RegisterAlignmentAcrossComponents(self, attrNames):
        self.RegisterCallbackOnAttributeChanged(self.AlignAcrossComponents, attrNames)
        
        if not hasattr(self, '_alignFields'):
            self._alignFields = acm.FDictionary()
        
        for attrName in attrNames:
            self._alignFields.AtPut(attrName, attrNames)

    def AddValidationFailedPair(self, failedPairs, attribute1, attribute2):
        failedPairs = AddFArrayItemToFDictionary(failedPairs, attribute1, attribute2)
        failedPairs = AddFArrayItemToFDictionary(failedPairs, attribute2, attribute1)
        return failedPairs

    def HasAlreadyFoundFailedPair(self, failedPairs, attribute1, attribute2):
        return (
                  (     failedPairs.HasKey(attribute1) 
                    and failedPairs[attribute1].IndexOfFirstEqual(attribute2) >= 0
                  )
                  or
                  (     failedPairs.HasKey(attribute2) 
                    and failedPairs[attribute2].IndexOfFirstEqual(attribute1) >= 0
                  )
                )

class ProductBase(ComponentBasedDealPackage):

    ipName              = Object  ( objMapping = 'InstrumentPackage.Name',
                                    label = 'Name' )

    notional            = Object  ( objMapping = InstrumentPart("Notional"),
                                    label = '@NotionalLabel',
                                    formatter = '@NotionalFormatter',
                                    domain = 'double',
                                    defaultValue = 1000.0 )

    currency            = Object ( label = 'Currency',
                                   domain = 'FCurrency',
                                   objMapping = (InstrumentPart("InstrumentPartCurrencies.Currency").
                                                 DealPart("DealPartCurrencies.Currency" ) ) )
    
    spotDays            = Object ( objMapping = "Instruments.SpotBankingDaysOffset",
                                   label = 'Spot Days',
                                   visible = '@VisibleSpotDays',
                                   validate = '@ValidateSpotDays')

    tradeInput          = StructuredTradeInput ( quantityMappingName  = "TradeQuantitySpecification",
                                                 priceLayout         = "PriceLayout" )

    def AttributeOverrides(self, overrideAccumulator):
        attrs = {}
        
        attrs['tradeInput'] = {
                'status' : dict(defaultValue = 'Simulated'),
                'quantity_value' : dict(defaultValue = 1.0 )
                }

        for composite in attrs:
            for field in attrs[composite]:
                overrideAccumulator({'%s_%s' % (composite, field) : attrs[composite][field] })

    # ################################################
    # Methods that must be implemented by sub classes
    # in order for object mappings to work
    # ################################################
    
    def InstrumentPartCurrencies(self, *rest):
        raise DealPackageException ( "Missing method InstrumentPartCurrencies." )
    
    def DealPartCurrencies(self, *rest):
        raise DealPackageException ( "Missing method DealPartCurrencies." )

    def Notional(self, *rest):
        raise DealPackageException ( "Missing method Notional for notional object mapping." )

    # ################################################
    # Methods used by product base attribute that 
    # can be implemented per product but are not 
    # required
    # ################################################

    def ValidateSpotDays(self, *rest):
        pass

    def NotionalLabel(self, *rest):
        return 'Notional'
    
    def NotionalFormatter(self, *rest):
        return acm.Get('formats/Volume')


    # ###############################################
    # Common methods that can be used as needed 
    #
    # NOTE: Potentially methods that should be moved to
    #       a help library
    # ###############################################

    def UpdatePremiums(self, *rest):
        for trade in self.Trades():
            trade.UpdatePremium(True)

    def AsPortfolio(self, *rest):
        return self.DealPackage().AsPortfolio()

    # #############################################
    # ToDo: Descriptions
    # #############################################
    def TradeQuantitySpecification(self):
        return self._tradeQuantityMapping

    def PriceLayout(self):
        return ''

    def VisibleSpotDays(self, *rest):
        return True

