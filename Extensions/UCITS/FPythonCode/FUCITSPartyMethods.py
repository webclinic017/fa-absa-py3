""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSPartyMethods.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSPartyMethods

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FUCITSHooks

GOVERNMENT_OR_STRONG_ENTITY = ['Government', 'Strong Entity']
AUTHORISED_CI = "Authorised Credit Institution"
ISSUER_OR_ULTIMATE_ISSUER = ['Issuer', 'UCITS UltimateIssuer',]
NO_UCITS_ISSUER_STATUS = 'No UCITS IssuerStatus'
'-------------------------------------------------------------------'
def IssuerStatusFromHook(party):
    try:
        return FUCITSHooks.IssuerStatus(party)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSIssuerStatus(party):
    issuerStatus = IssuerStatusFromHook(party)
    if str(issuerStatus) in GOVERNMENT_OR_STRONG_ENTITY:
        issuerStatus = "/".join(GOVERNMENT_OR_STRONG_ENTITY)
    return issuerStatus if issuerStatus else NO_UCITS_ISSUER_STATUS
'-------------------------------------------------------------------'
def UCITSPartyIsACI(party):
    issuerStatus = UCITSIssuerStatus(party)
    return issuerStatus if issuerStatus == AUTHORISED_CI else "Other"
'-------------------------------------------------------------------'
def UltimateIssuerFromHook(party):
    try:
        return FUCITSHooks.UltimateIssuer(party)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSUltimateIssuer(party):
    return UltimateIssuerFromHook(party)
'-------------------------------------------------------------------'
def TotalIssuedDebtFromHook(party):
    try:
        return FUCITSHooks.TotalIssuedDebt(party)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSTotalIssuedDebt(party):
    if party.RiskCountry() is None:
        raise ValueError("No country of risk specified")
    return acm.DenominatedValue(TotalIssuedDebtFromHook(party), CurrencyFromCountry(party.RiskCountry().Name()), None, None)
'-------------------------------------------------------------------'
def CurrencyFromCountry(countryAsString):
    conversionDict = FUCITSHooks.CountryToCurrencyDict()
    return conversionDict.get(str(countryAsString), 'EUR')
'-------------------------------------------------------------------'
def IsPartyGrouping(grouping):
    groupingValue = grouping.GroupingValue()
    if hasattr(groupingValue, 'IsKindOf'):
        return groupingValue.IsKindOf(acm.FParty)
    return False
'-------------------------------------------------------------------'
def IsIssuerOrUltimateIssuerGrouping(grouping):
    return str(grouping.Grouper().DisplayName()) in ISSUER_OR_ULTIMATE_ISSUER