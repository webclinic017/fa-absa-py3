
import acm

from CommodityStripExtensionPoints import CustomChoiceListPopulator, StripDealTypeMapping
import ChoicesExprTrade
import ChoicesExprInstrument
from CommodityStripUtils import getTimeSortingKey, getTimePeriodSortingKey

def BaseUnderlyingPopulator(dp):
    group = dp.GetAttribute('instrumentGroup')
    if group:
        return group.Instruments().SortByProperty('Name')
    else:
        allCommodities = acm.FInstrument.Select("insType = 'Commodity'")
        allIndices = acm.FInstrument.Select("insType = 'Commodity Index'")
        allBaseUnderlyings = allCommodities.Union(allIndices)
        sortedUnderlyings = allBaseUnderlyings.AsIndexedCollection().SortByProperty('Name')
        return sortedUnderlyings

def UnderlyingPopulator(dp):
    possibleUnderlyings = acm.FArray()
    if not dp.GetAttribute('useCurrentFuture'):
        und = dp.GetAttribute('baseUnderlying')
        if und:
            possibleUnderlyings.Add(und)

            # All future/forwards
            allDerivatives = acm.FInstrument.Select("underlying = '%s' and currency = '%s' and otc = false and insType = 'Future/Forward' " % (und.Name(), und.Currency().Name()))
            generics = sorted([i for i in allDerivatives if i.Generic()], key=getTimePeriodSortingKey)
            futures = sorted([i for i in allDerivatives if not i.Generic() and acm.Time.DateDifference(acm.Time.AsDate(dp.FindEndDate()), i.ExpiryDateOnly()) <= 0], key=getTimeSortingKey)
            possibleUnderlyings.AddAll(generics)

            if dp.GetAttribute('stripType') != 'Bullet':
                rollingSchedules = acm.FRollingSchedule.Select("underlying = '%s'" % und.Name()).SortByProperty('Name')
                possibleUnderlyings.AddAll(rollingSchedules)

            possibleUnderlyings.AddAll(futures)
            
    return possibleUnderlyings

def QuotationPopulator(dp):
    und = dp.GetAttribute('underlying')
    if und:
        q = und.DefaultQuotations()
    else:
        q = acm.FQuotation.Select("")
    return q.SortByProperty('Name')

def CounterpartyPopulator(dp):
    cp = list(ChoicesExprTrade.getCounterparties().SortByProperty('Name'))
    cp.append(None)
    return cp
    
def CurrencyPopulator(dp):
    return acm.FInstrument.Select("insType = 'Curr'").SortByProperty('Name')

def PortfolioPopulator(dp):
    portfolios = list(ChoicesExprTrade.getPhysicalPortfolioChoices().SortByProperty('Name'))
    portfolios.append(None)
    return portfolios

def BrokerPopulator(dp):
    brokers = list(acm.FBroker.Select('').SortByProperty('Name'))
    brokers.append(None)
    return brokers

def AcquirerPopulator(dp):
    acquirers = list(ChoicesExprTrade.getAcquirers().SortByProperty('Name'))
    acquirers.append(None)
    return acquirers

def StripTypePopulator(dp, attrName):
    baseLine = list(StripDealTypeMapping().keys())
    if 'BulletOption' in baseLine:
        baseLine.remove('BulletOption')
    if 'Asian' in baseLine and dp.GetAttribute('isOptionStrip'):
        baseLine.remove('Asian')
    customerSelection = CustomChoiceListPopulator(dp, attrName)
    if customerSelection:
        return list(set(customerSelection) & set(baseLine))
    else:
        return baseLine

def FixingSourcePopulator():
    l = sorted([s for s in ChoicesExprInstrument.getFixingSources(False)])
    l.append(None)
    return l

def FxFixingRulePopulator():
    l = sorted([r for r in ChoicesExprInstrument.getFixingDateRules(None)])
    l.append(None)
    return l

def StructureTypePopulator(dp):
    structureTypes = []
    if not dp.GetAttribute('useCurrentFuture'):
        structureTypes.append('Single Leg')
    structureTypes.append('Strip')
    return structureTypes

def FixedValuesPopulator(attributeName):
    if attributeName == 'exerciseType':
        return ['American', 'European']
    if attributeName == 'payType':
        return ['Forward', 'Spot']
    if attributeName == 'settlementType':
        return ['Cash', 'Physical']

def ExpiryTypePopulator(dealPackage):
    expiryTypes = ['Standard']
    if dealPackage.GetAttribute('stripType') == 'Asian' or not dealPackage.GetAttribute('useCurrentFuture'):
        expiryTypes += ['Custom']
    if dealPackage.GetAttribute('stripType') == 'Asian':
        expiryTypes += ['Custom Settlement']
    return expiryTypes

def InstrumentGroupPopulator(dp):
    pageGroup = dp.GetAttribute('pageGroup')
    return pageGroup.SubGroups() if pageGroup else []

def CheckCustomCrossCurrency(source):
    if not None in source:
        l = [s for s in source]
        l.append(None)
        return l
    return source

def ChoiceListPopulator(dp, attrName):
    # Strip Type is treated slightly different than other fields
    if attrName == 'stripType':
        return StripTypePopulator(dp, attrName)

    # Check if customer has implemented a hook for this field
    customerSelection = CustomChoiceListPopulator(dp, attrName)
    if customerSelection is not None:
        # Cross currency specific lists must have value of None for query to work
        if attrName in ('fxSource', 'fxFixRule', 'fixingSource'):
            return CheckCustomCrossCurrency(customerSelection)
        return customerSelection

    # Standard handling
    if attrName == 'baseUnderlying':
        return BaseUnderlyingPopulator(dp)
    if attrName == 'underlying':
        return UnderlyingPopulator(dp)
    elif attrName == 'quotation':
        return QuotationPopulator(dp)
    elif attrName == 'counterParty':
        return CounterpartyPopulator(dp)
    elif attrName in ('currency', 'tradeCurrency'):
        return CurrencyPopulator(dp)
    elif attrName in ('portfolio', 'b2bPrf'):
        return PortfolioPopulator(dp)
    elif attrName == 'broker':
        return BrokerPopulator(dp)
    elif attrName in ('acquirer', 'b2bAcq'):
        return AcquirerPopulator(dp)
    elif attrName == 'fixingSource':
        return FixingSourcePopulator()
    elif attrName == 'fxSource':
        return FixingSourcePopulator()
    elif attrName == 'convType':
        return ChoicesExprInstrument.getCrossCurrencyCalculationOption().GetChoiceListSource()
    elif attrName == 'fxFixRule':
        return FxFixingRulePopulator()
    elif attrName == 'instrumentGroup':
        return InstrumentGroupPopulator(dp)
    elif attrName == 'expiryType':
        return ExpiryTypePopulator(dp)
    elif attrName == 'structureType':
        return StructureTypePopulator(dp)
    elif attrName in ('exerciseType', 'payType', 'settlementType'):
        return FixedValuesPopulator(attrName)

