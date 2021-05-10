""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSInstrumentMethods.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSInstrumentMethods

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FUCITSHooks

UCITS_FUND = "UCITS"
NON_UCITS_FUND = "Non UCITS Fund"
NOT_APPLICABLE = "Not Applicable"
NOT_AVAILABLE = "Not Available"
TSMM = 'TSMM'
OTHER = 'Other'
VOTING_RIGHT = 'Voting Rights'
NO_VOTING_RIGHT = 'No Voting Rights'
DEBT_SECURITY = 'Debt Security'
NOT_DEBT_SECURITY = 'Not Debt Security'
SECURITY_LENDING = 'Security Lending'
NOT_SECURITY_LENDING = 'Not Security Lending'
TRASH_RATIO_SECURITY = 'Trash Ratio Security'
NOT_TRASH_RATIO_SECURITY = 'Not Trash Ratio Security'


'-------------------------------------------------------------------'
def FundTypeFromHook(instrument):
    try:
        return FUCITSHooks.FundType(instrument)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSFundType(instrument):
    if FUCITSHooks.InstrumentDeterminationMethods.IsFund(instrument):
        fundType = FundTypeFromHook(instrument)
        return fundType if fundType else NOT_AVAILABLE
    else:
        return NOT_APPLICABLE
'-------------------------------------------------------------------'
def IsUCITSFund(instrument):
    fundType = UCITSFundType(instrument)
    if fundType == UCITS_FUND:
        return UCITS_FUND
    elif fundType == NOT_APPLICABLE:
        return NOT_APPLICABLE
    else:
        return NON_UCITS_FUND
'-------------------------------------------------------------------'
def UCITSInstrumentIsTSMM(obj):
    if FUCITSHooks.InstrumentDeterminationMethods.IsTSMM(obj):
        return TSMM
    else:
        return OTHER
'-------------------------------------------------------------------'
def VotingRightsFromHook(instrument):
    try:
        return FUCITSHooks.VotingRights(instrument)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSVotingRights(instrument):
    if FUCITSHooks.InstrumentDeterminationMethods.IsStock(instrument):
        vr = VotingRightsFromHook(instrument)
        if vr is None:
            return NOT_AVAILABLE
        elif vr:
            return VOTING_RIGHT
        else:
            return NO_VOTING_RIGHT

    else:
        return NOT_APPLICABLE
'-------------------------------------------------------------------'
def UCITSIsDebtSecurity(instrument):
    if FUCITSHooks.InstrumentDeterminationMethods.IsDebtSecurity(instrument):
        return DEBT_SECURITY
    return NOT_DEBT_SECURITY
'-------------------------------------------------------------------'
def UCITSIsSecurityLending(instrument):
    if FUCITSHooks.InstrumentDeterminationMethods.IsSecurityLending(instrument):
        return SECURITY_LENDING
    return NOT_SECURITY_LENDING
'-------------------------------------------------------------------'
def IsTrashRatioSecurityFromHook(instrument):
    try:
        return FUCITSHooks.IsTrashRatioSecurity(instrument)
    except Exception:
        return None
'-------------------------------------------------------------------'
def UCITSIsTrashRatioSecurity(instrument):
    if FUCITSHooks.InstrumentDeterminationMethods.IsTSMM(instrument):
        tr = IsTrashRatioSecurityFromHook(instrument)
        if tr is None:
            return NOT_APPLICABLE
        elif tr:
            return TRASH_RATIO_SECURITY
        else:
            return NOT_TRASH_RATIO_SECURITY
    return NOT_APPLICABLE
'-------------------------------------------------------------------'
def UCITSValuationIssuer(ins):
    return ValuationUnderlyingOrSelf(ins).CreditReferenceOrSelf().Issuer()
'-------------------------------------------------------------------'    
def ValuationUnderlyingOrSelf(ins):
    und = ins.ValuationUnderlying()
    if und is None:
        return ins
    else:
        return und
'-------------------------------------------------------------------'