""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSHooks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSHooks

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


from FUCITSInsClassification import InstrumentDeterminationMethodsBase

'''Here it is possible to set from which modules the limit templates should be taken '''
UCITS_MODULES = ['UCITS', 'UCITS Germany',]

def UltimateIssuer(party):
    ultimate_issuer = party.AdditionalInfo().UCITSUltimateIssuer()
    return ultimate_issuer if ultimate_issuer else party.Name()

def FundType(instrument):
    return instrument.AdditionalInfo().UCITSFundType()

def IssuerStatus(party):
    return party.AdditionalInfo().UCITSIssuerStatus()

def VotingRights(instrument):
    return instrument.AdditionalInfo().UCITSVotingRights()

def TotalIssuedDebt(party):
    return party.AdditionalInfo().UCITSTotalDebt()

def IsTrashRatioSecurity(instrument):
    '''As default, trash ratio securities are MM-instruments which are not issued by ACI or Gov/Strong entity'''
    if InstrumentDeterminationMethods.IsMoneyMarketInstrument(instrument):
        if instrument.Issuer().UCITSIssuerStatus() not in ['Government/Strong Entity', 'Authorised Credit Institution',]:
            return True
    return False

def IsIssuerSensitive(instrument):
    return not instrument.Otc()

def IsCounterpartySensitive(instrument):
    return instrument.Otc()

class InstrumentDeterminationMethods(InstrumentDeterminationMethodsBase):
    pass
    
'''Functions for determining which extension attribute to use for different asset classes'''
class GeneralExposureMethods(object):
    
    determine = InstrumentDeterminationMethods
    
    @classmethod
    def IfOption(cls, ins):
        if cls.determine.IsOption(ins):
            return 'abs(instrumentOptionExposure)'

    @classmethod
    def IfFutureForward(cls, ins):
        if cls.determine.IsFutureForward(ins):
            return 'abs(instrumentFutureExposure)'

    @classmethod
    def IfSecurity(cls, ins):
        if cls.determine.IsNormalBond(ins) or \
           cls.determine.IsZero(ins) or \
           cls.determine.IsEquity(ins) or \
           cls.determine.IsCFD(ins):
            return 'marketValues'
    
    @classmethod
    def IfMoneyMarketInstrument(cls, ins):
        if cls.determine.IsMoneyMarketInstrument(ins):
            return 'marketValues'
    
    @classmethod
    def IfSecurityLending(cls, ins):
        if cls.determine.IsSecurityLending(ins):
            return 'abs(theoreticalValues)'
        
    @classmethod
    def IfSwap(cls, ins):
        if cls.determine.IsSwap(ins):
            return "abs(instrumentSwapExposure)"

    @classmethod
    def IfCurrencySwap(cls, ins):
        if cls.determine.IsCurrencySwap(ins):
            return "abs(instrumentCurrencySwapExposure)"

    @classmethod
    def IfTotalReturnSwap(cls, ins):
        if cls.determine.IsTRS(ins):
            return "abs(instrumentTotalReturnSwapExposure)"

    @classmethod
    def IfCreditDefaultSwap(cls, ins):
        if cls.determine.IsCDS(ins):
            return "abs(instrumentCreditDefaultSwapExposure)"

    @classmethod
    def IfConvertible(cls, ins):
        if cls.determine.IsConvertible(ins):
            return "abs(instrumentConvertibleExposure)"
    
    @classmethod
    def IfCombination(cls, ins):
        if cls.determine.IsCombination(ins):
            if ins.MtmFromFeed():
                return 'abs(marketValues)' 
            elif ins.SplitCombination(False):
                return 'abs(combinationLookthroughSegregatedExposure)'
            else:
                return 'abs(marketValues)'
                
    @classmethod
    def IfFund(cls, ins):
        if cls.determine.IsFundIns(ins):
            if ins.MtmFromFeed():
                return 'abs(marketValues)' 
            else:
                return 'abs(fundLookthroughSegregatedExposure)'
                

''' A mapping between the country of risk of debt securities and a currency. Used for determening which currency
the total issued debt of an issuer is in '''
def CountryToCurrencyDict():
    return {'AT': 'EUR',
            'AU': 'AUD',
            'BE': 'EUR',
            'BG': NotImplementedError,
            'BR': 'BRL',
            'CA': 'CAD',
            'CH': 'CHF',
            'DE': 'EUR',
            'DK': 'DKK',
            'ES': 'EUR',
            'FI': 'EUR',
            'FR': 'EUR',
            'GB': 'GBP',
            'GE': NotImplementedError,
            'GR': 'EUR',
            'HU': 'HUF',
            'IE': 'EUR',
            'IN': 'EUR',
            'IS': NotImplementedError,
            'IT': 'EUR',
            'JE': NotImplementedError,
            'JP': 'JPY',
            'KY': NotImplementedError,
            'LB': NotImplementedError,
            'LU': 'EUR',
            'LV': 'EUR',
            'MX': 'MXN',
            'NL': 'EUR',
            'NO': 'NOK',
            'PL': 'EUR',
            'RU': 'RUB',
            'SE': 'SEK',
            'SG': 'SGD',
            'SP': 'EUR',
            'TH': 'THB',
            'UK': 'GBP',
            'US': 'USD'}