""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FExclusionListCustomFunctions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExclusionListCustomFunctions

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

def SubGroupsRecursive(exclusionList):
    returnGroups = []
    returnGroups.append(exclusionList)
    for subGroup in exclusionList.SubGroups():
        returnGroups.extend(SubGroupsRecursive(subGroup))
    return returnGroups

def InstrumentFilterFromPartyGroud(partyGroup):
    oids = [partyLink.Party().Oid() for partyLink in partyGroup.Parties()]
    return CreateInstrumentQuery("Issuer.Oid", oids)

def InstrumentFilterFromPartyAliasList(extensionValue, aliasType):
    partyAliasValues = KeysFromExtension(extensionValue)
    parties = [aliasType.Party(identifier) for identifier in partyAliasValues if aliasType.Party(identifier)]
    return CreateInstrumentQuery("Issuer", parties)

def InstrumentFilterFromPartyIdList(extensionValue):
    identifiers = KeysFromExtension(extensionValue)
    idAttrs = ["Issuer.Id", "Issuer.Id2", "Issuer.LegalEntityId", "Issuer.RedCode"]
    queries = [CreateInstrumentQuery(attr, identifiers) for attr in idAttrs]
    return CompositeInstrumentOrQuery(queries)

def InstrumentFilterFromIdList(extensionValue):
    identifiers = KeysFromExtension(extensionValue)
    idAttrs = ["Name", "Isin", "ExternalId1"]
    queries = [CreateInstrumentQuery(attr, identifiers) for attr in idAttrs]
    return CompositeInstrumentOrQuery(queries)
    
def KeysFromExtension(extensionValue):
    if extensionValue:
        return [isin.strip() for isin in extensionValue.Value().split('\n') if isin]
    else:
        return []

def CreateInstrumentQuery(attribute, values):
    if len(values) > 0:
        return acm.Filter.SimpleOrQuery("FInstrument", len(values)*[attribute], [], values)

def ApplyBlacklistFilter(instruments, filter, isBlacklist, clock):
    if filter.IsKindOf(acm.FPageGroup):
        filter = filter.InstrumentsRecursively()
    return instruments.Filter(filter) if isBlacklist else instruments.InverseFilter(filter)

def ApplyCurrencyPairBlacklistFilter(instruments, currencyPairs, isBlacklist):
    def filterInstruments(instruments, currencyPairs, isBlacklist):
        for i in instruments:
            if isinstance(i.Underlying(), acm._pyClass(acm.FCurrency)):
                currPair = i.Underlying().CurrencyPair(i.Currency())
                if isBlacklist:
                    if currPair in currencyPairs:
                        yield i
                else:
                    if currPair and currPair not in currencyPairs:
                        yield i
    return list(filterInstruments(instruments, currencyPairs, isBlacklist))

def CompositeInstrumentOrQuery(queries):
    if len(queries) == 0:
        return None
    elif len(queries) == 1:
        return queries[0]
    comp = acm.Filter.CompositeOrQuery("FInstrument", queries[0], queries[1])
    for q in queries[2:]:
        comp = acm.Filter.CompositeOrQuery("FInstrument", comp, q)
    return comp