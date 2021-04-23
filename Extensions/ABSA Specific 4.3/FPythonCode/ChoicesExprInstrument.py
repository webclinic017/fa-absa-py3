"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    ChoicesExprInstrument

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-30      Upgrade2018     Jaysen Naicker                                  Merge customizations with 2018 default code 
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from __future__ import print_function
import acm
from ChoicesExprCommon import allEnumValuesExcludeNone, listChoices, listChoicesWithEmpty, Decorate


def getMTMMarkets():
    MTMMarkets = acm.FMTMMarket.Select('')
    MTMMarkets.SortByProperty('StringKey', True)
    return MTMMarkets


'''** Reference Data Type **'''
def getReferenceDateTypeChoices(object):
    try:
        instrument = object
        if instrument.IndexType() == "None":
            return acm.FEnumeration['enum(ReferenceDateType)'].Enumerators()
        else:
            return allEnumValuesExcludeNone( acm.FEnumeration['enum(ReferenceDateType)'] )
    except Exception as e:
        print (e)
        raise (e)
    

def getCategories():
    return listChoicesWithEmpty("Category")

def getResetTypes(leg):
    if leg.LegType() in ['Call Fixed', 'Dividend Index']:
        return ['None']
    elif leg.LegType() == 'Call Fixed Adjustable':
        return ['Weighted']        
    elif leg.LegType() == 'Total Return':
        return ['Return']
    elif leg.LegType() in ['Collared LPI', 'Floored LPI', 'Capped LPI', 'Return Cap', 'Return Floor']:
        return ['Aggregate Return']
    else:
        return ['Single', 'Weighted', 'Unweighted', 'Compound', 'Flat Compound', 'Assertive', 'Weighted 1m Compound', 'Accretive', 'Simple Overnight', 'Total Weighted', 'Compound of Weighted', 'Compound Spread Excluded', 'Compound Float Fctr Included', 'Comp of Wght Float Fctr Inc']

def getCertificateUnderlyingTypes ( underlyingType ):
    return [ "Combination", "EquityIndex", "Commodity"]

def getPMDepositUnderlyingTypes( underlyingType ):
    return [ "Commodity", "Commodity Variant"]

def getCombCategories():
    return listChoicesWithEmpty("Comb Category")

def getExerciseTypeChoices( underlyingType ):
    if underlyingType == 'Commodity Variant':
        return ['European', 'American']
    elif underlyingType == 'Curr':
        return [e for e in acm.FEnumeration['enum(ExerciseType)'].Enumerators() if (e in ('American', 'European'))]
    else:
        return [e for e in acm.FEnumeration['enum(ExerciseType)'].Enumerators() if (e not in ('None', 'Amer GA'))]

def getEstimationMethods():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(StubEstimationMethod)'] )

def getFixingMethods():
    return ['Closest', 'Interpolate']
  
def getStubResetEstimationFixingRef(stubResetsEstimation):
    if not stubResetsEstimation:
        return []
    return acm.FInstrument.Select("insType='RateIndex' and currency='"+ stubResetsEstimation.Leg().FloatRateReference().FirstFixedLeg().Currency().Name() + "'")
    
def getExCouponMethods():
    enumValues = acm.FEnumeration['enum(ExCouponMethod)']
    values=[e for e in enumValues.Enumerators() if (e != 'AdditionalInfo')]  
    return values
    
def getFixingSources(onlyMtMMarketsWithTimeZone):
    if onlyMtMMarketsWithTimeZone:
        values = [market for market in getMTMMarkets() if market.TimeZone()]
    else:
        values = list(getMTMMarkets())
    return [''] + values

def getAutocallableStrikeTypes(leg):
    decorator = acm.FBusinessLogicDecorator.WrapObject(leg)
    return decorator.ChoiceListSource('AutocallableStrikeType')
    
def getTriggerRefInsTypeChoices(leg):
    decorator = acm.FBusinessLogicDecorator.WrapObject(leg)
    return decorator.ChoiceListSource('TriggerReferenceInstrumentType')

def getAutocallableTypes(leg):
    decorator = acm.FBusinessLogicDecorator.WrapObject(leg)
    return decorator.ChoiceListSource('AutocallableType')
        
def GetFloatRateReferences( leg ):
    legDeco = Decorate(leg)
    return legDeco.AllFloatRefs()

def IsAnnualRateIndex(cand):
    candDeco = Decorate(cand)
    return candDeco.RateType() == "Annual"

def GetFloatRateReferences2( leg ):
    choices = GetFloatRateReferences( leg)
    return [c for c in choices if not IsAnnualRateIndex(c)]

def getIncompleteChoices():
    enum=acm.FEnumeration['enum(CompletionStatus)']
    return [e for e in enum.Enumerators() if (e not in ('Pledged', 'Frozen'))]  

def getIndexTypeChoices( priceIndex ):
    return [ "None", "CPI -3Months (30)", "CPI -3Months", "CPI -4Months", "CPI JGB", "CPI -3Months NoInterpol", "CPI -2Months NoInterpol", "CPI AUD", "CPI -8Months NoInterpol", "CPI IPCA ProRata", "CPI IGP-M ProRata", "Custom"]

def getLimitedPriceIndexTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(LPIType)'] )

def getNominalScalingChoices(instrument):
    instrumentType = instrument.InsType()
    if IsPreciousMetalDeposit(instrument):
        return ['Price', 'Initial Price', 'None']
    elif instrumentType in ['TotalReturnSwap', 'Portfolio Swap', 'SecurityLoan']:
        return ['None', 'Initial Price', 'Price']
    elif instrumentType in ['MBS/ABS']:
        return ['None', 'Pass-Through']
    elif instrumentType in ['FreeDefCF']: 
        choices = acm.FArray()
        for enumVal in acm.FEnumeration['enum(NominalScaleType)'].Enumerators():
            if enumVal not in ['CPI', 'CPI Fixing In Arrears']:
                choices.Add(enumVal)
        return choices
    return acm.FEnumeration['enum(NominalScaleType)'].Enumerators()

def getInflationScalingRefChoices():
    return acm.FPriceIndex.Select("")
    
def getInflationScalingTypeChoices(insType):    
    if insType in ['IndexLinkedSwap']:
        return ['None', 'Start of Cash Flow', 'End of Cash Flow']
    elif insType in ['IndexLinkedBond']:
        return ['Start of Cash Flow', 'End of Cash Flow']
    return acm.FEnumeration['enum(InflationScalingType)'].Enumerators()
        
def getOptionTypeChoices( underlyingType ):
    if underlyingType in['Swap', 'CurrSwap', 'TotalReturnSwap', 'IndexLinkedSwap', 'CreditDefaultSwap']:
        return ['Receiver', 'Payer']
    if underlyingType == 'FRA':
        return ['Lender', 'Borrower']
    return ['Call', 'Put']

def getOtcChoices():
    return ['Yes', 'No']

def getPassingTypeChoices(object):
    enumValues = acm.FEnumeration['enum(PassingType)']
    return [e for e in enumValues.Enumerators() if (e != 'Amortising Payday')]  

def getPayOffSetMethodChoices(ins):
    if ins and ins.PayOffsetMethod() == 'Default':
        return ['Business Days', 'Calendar Days', 'Default']
    else:
        return ['Business Days', 'Calendar Days']
    
def getPortfolioSwapPortfolios():
    portfolios = list(acm.FPhysicalPortfolio.Select(""))
    portfolios.extend(acm.FCompoundPortfolio.Select(""))
    return portfolios
    
def getPledgeFrozenChoices():
    return ['None', 'Pledged', 'Frozen']

def getPriceFindingGroups():
    return listChoices('PriceFindingGroup')
    
def getProductTypes():
    return listChoicesWithEmpty("Product Type")

def getSeniorityChoices():
    return listChoices('Seniority')

def getStrikeTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(StrikeType)'] )

def getStrikeTypeFXOptionChoices(instrument):
    exotic = instrument.Exotic()
    if exotic:
        exoticDecorator = Decorate(exotic)
        if exoticDecorator.BaseType() == 'Straddle':
            enumValues = acm.FEnumeration['enum(StrikeType)']
            if exoticDecorator.StraddleType() == 'Relative Forward':
                return [e for e in enumValues.Enumerators() if (e == 'Rel Frw Pct 100')]
            else:
                return [e for e in enumValues.Enumerators() if (e.find('Absolute') == 0)]
    return getStrikeTypeChoices()
        
def getValuationGroups():
    return listChoicesWithEmpty("ValGroup")

def getYTMChoices(instrument):
    enum = acm.FEnumeration['enum(YtmMethod)']
    choices = [e for e in enum.Enumerators() \
            if (e != 'Discount') or (e == 'Discount' and instrument.InsType() == 'Zero')]
    return choices

def FilterOutPreciousMetals(underlyings):
    preciousMetals = acm.FArray()
    for underlying in underlyings:
        if underlying.IsPreciousMetal():
            preciousMetals.Add(underlying)
    return preciousMetals
        
def IsPreciousMetalSwap(ins):
    return ins.InsType() == 'Repo/Reverse' and ins.UnderlyingType() == 'Commodity Variant' and ins.Generic()

def IsPreciousMetalDeposit(ins):
    return ins.InsType() == 'SecurityLoan' and (ins.UnderlyingType() == 'Commodity Variant' or ins.UnderlyingType() == 'Commodity')

def getUnderlyingChoices(instrument):
    if not instrument:
        return []
    elif instrument.InsType() == 'Rolling Schedule':
        undType = 'Commodity'
    else:
        undType = instrument.UnderlyingType()
        
    if undType in ['Stock', 'Commodity', 'Curr', 'EquityIndex', 'Combination', 'Commodity Index', 'Commodity Variant', 'CreditIndex', 'Fund', 'ETF', 'Depositary Receipt']:
        underlyings = acm.FInstrument.Select( "insType='" + str(undType) + "'")
    else:
        underlyings=acm.FArray()
        nonExpired = acm.FInstrument.Select( "insType='" + str(undType) + "'" + "and expiryDate >="+str(acm.Time().DateToday()))        
        generics = acm.FInstrument.Select( "insType='" + str(undType) + "'" + "and generic = True")
        underlyings.AddAll(generics)
        underlyings.AddAll(nonExpired)
        underlyings.Sort()
    
    if IsPreciousMetalSwap(instrument):
        underlyings = FilterOutPreciousMetals(underlyings)
        
    underlyings.Remove(instrument.Originator())
    return underlyings
    
def getAverageForwardRefInsChoices(instype,endDate,ins=None):
    references=acm.FArray()
    if instype in ['Commodity', 'Commodity Index', 'Commodity Variant', 'Rolling Schedule']:
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "'"))
    elif instype == 'Average Future/Forward':
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "' and expiryDate>=" + endDate))
        if ins:
            references.Remove(ins)
    elif instype == 'Future/Forward':
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "' and underlyingType='Commodity' and expiryDate>=" + endDate))
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "' and underlyingType='Commodity' and generic=True"))
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "' and underlyingType='Commodity Variant' and expiryDate>=" + endDate))
        references.AddAll(acm.FInstrument.Select( "insType='" + instype + "' and underlyingType='Commodity Variant' and generic=True"))
        futReferences=acm.FInstrument.Select( "insType='" + instype + "'" + "underlyingType='Future/Forward'")
        for ref in futReferences:
            if ref.Underlying().UnderlyingType() in ['Commodity', 'Commodity Index']:
                if ref.ExpiryDate()>=endDate or ref.Generic():
                    references.Add(ref)
    return references
    
def getTriggerRefChoices(leg):
        if not leg:
            return []   
        triggerRefType = leg.TriggerReferenceInstrumentType()
        if triggerRefType in ['Stock', 'EquityIndex']:
            triggerRefs = acm.FInstrument.Select( "insType='" + str(triggerRefType) + "'")
        else:
            triggerRefs = []
        return triggerRefs
    
def getSettlementTypeChoices(instrument):
    if instrument.InsType() in ['CFD']:
        return ['Cash']
    if instrument.InsType() in ['Commodity', 'FreeDefCF', 'Portfolio Swap']:
        return ['None', 'Cash', 'Physical']
    else:
        return allEnumValuesExcludeNone( acm.FEnumeration['enum(SettlementTypeShortName)'] )
    
def getQuantoOptionTypeChoices( instrument ):
    return ['None', 'Quanto']
        
def getRateIndexRateTypeChoices(instrument):
    return ['Simple', 'Annual']

def getDigitalTypes( leg ):
    legDeco = Decorate(leg)
    return legDeco.AllDigitalTypes()

def getComparisonTypes( leg ):
    legDeco = Decorate(leg)
    return legDeco.AllComparisonTypes()
    
def getPriceInterpretationTypes():
    return ['All In', 'As Reference']

def getCrossCurrencyCalculationOption():
    return acm.FIndexedPopulator(acm.FEnumeration['enum(CrossCurrencyCalculationType)'].Enumerators())

def GetReferenceInstrumentTypes(instrument):
    if instrument.InsType() == 'Average Option':
        return ['Commodity', 'Commodity Variant']
    else:
        return ['Average Future/Forward', 'Commodity', 'Commodity Index', 'Future/Forward', 'Rolling Schedule']

def getPayTypeChoices(ins):
    payTypes = allEnumValuesExcludeNone(acm.FEnumeration['enum(PayType)'])
    if ins.IsAverageForward() or ins.IsCommoditySpread():
        payTypes = [e for e in payTypes if (e == 'Future' or e == 'Forward')]
    elif ins.IsVolatilityOrVarianceSwap():
        payTypes = [e for e in payTypes if (e == 'Forward')]
    elif ins.IsFuture():
        payTypes = [e for e in payTypes if (e != 'Spot')]
    elif ins.InsType() in ['BuySellback', 'Average Option']:
        payTypes = [e for e in payTypes if (e == 'Spot' or e == 'Forward')]
    elif ins.InsType() =='Option' and ins.Exotic():
        exoticDecorator = Decorate(ins.Exotic())
        if exoticDecorator.BaseType() == 'Straddle':
            payTypes = [e for e in payTypes if (e == 'Spot' or e == 'Forward')]
    choices = acm.FIndexedPopulator(payTypes)
    return choices

def getFixingDateRules(leg):
    fixingDateRules = acm.FFixingDateRule.Select('')
    return fixingDateRules

def getAmortGenerationChoices(leg):
    amortGenerations = allEnumValuesExcludeNone(acm.FEnumeration['enum(AmortGeneration)'])
    return acm.FIndexedPopulator(amortGenerations)

def getCreditEventSpecObligationCategory(instrument):
    return acm.FChoiceList.Select('list="ObligationCategory"')

def getInterestPaymentTimeTypes(instrument):
    return allEnumValuesExcludeNone(acm.FEnumeration['enum(PaymentTime)'])
    
def getFxStraddleCurrencies(instrument):
    currencies = []
    if instrument.StrikeCurrency():
        currencies.append(instrument.StrikeCurrency())
    if instrument.Underlying() and instrument.Underlying().InsType() == 'Curr':
        currencies.append(instrument.Underlying())
    return currencies
