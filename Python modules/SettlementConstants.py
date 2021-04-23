#  Developer           : Heinrich Cronje, Willie van der Bank, Heinrich Cronje, Heinrich Cronje
#  Purpose             : SND implementation, Bringing online of new desks, Check that party exist when
#                       determining VOSTRO settlement., Amended logic for Interbank indicator to handel all desks.
#  Department and Desk : Operations, Operations, RTB, Ops
#  Requester           : Miguel da Silva, Miguel da Silva, Shaun Steyn, Nicolette Burger
#  CR Number           : 662927, 852496 08/12/2011, 882500, 318308
'''
HISTORY
=================================================================================================================================
Date            Change no       Developer              Requester            Description
=================================================================================================================================
2012-08-08      396485          Heinrich Cronje        Ross Wood            PRIME SERVICES DESK Implementation
2014-12-11      CHNG0002447539  Sanele Macanda         Avantika Bhana       Trade loans 
2015-03-06      CHNG0002688966  Kovalenko, Dmitry      Vilakazi, Nomsa      Added four new accquirers
2015-03-31      ABITFA-3499	Lawrence Mucheka       Van Schalkwyk Willie Additional ABCAP CRT accquirers
2015-11-02      ABITFA-3691	Lawrence Mucheka       Van Schalkwyk Willie Additional COLLATERAL DESK accquirer
2016-04-19      ABITFA-4174     Gabriel Marko          Linda Breytenbanch   Enable Settlements on Deposits for Primary Markets Desk
2016-08-19      CHNG0003744247  Willie vd Bank                              Aded IMPUMELELO as part of Demat
2017-06-06      CHNG0004636076  Willie vd Bank                              Removed SETTLEMENT_ACQUIRERS and
                                                                            updated ACQUIRER_SHORTCODE
2017-12-07      CHNG0005212731  Willie vd Bank                              Added NON ZAR IRD
=================================================================================================================================
'''
import ael, acm

###################################################
## Constants for the desks using Settlements     ##
###################################################

ABCAP_CRT = 43067
ACQ_STRUCT_DERIV_DESK = 43001
AFRICA_DESK = 30248
BOND_DESK = 30326
COLLATERAL_DESK = 43417
CREDIT_DERIVATIVES_DESK = 6292
CREDIT_DERIVATIVES_DESK_NONCSA = 34298
EQ_DERIVATIVES_DESK = 9710
FOREX_DESK = 16219
FORWARDS_DESK = 215
FUNDING_DESK = 2247
GOLD_DESK = 16492
IRD_DESK = 30300
IRD_DESK_NONCSA = 34294
LIQUID_ASSET_DESK = 17657
METALS_DESK = 16491
MONEY_MARKET_DESK = 2246
NLD_DESK = 30311
STRUCT_NOTEST_DESK = 30301
REPO_DESK = 30327
NON_LINEAR_DERIV = 102
PRIMARY_MARKETS = 30539
PRIME_SERVICES_DESK = 32737
SWAPS_DESK = 17
TWC_SF = 42673
ZZZ_DO_NOT_USE_IRP_FX_DESK = 9693
IMPUMELELO = 42625
UHAMBO = 48168
NON_ZAR_IRD = 50909

ABSA_BANK = 'ABSA BANK LTD'

#used for SSI naming:
ACQUIRER_SHORTCODE = {
    FUNDING_DESK: 'FD', 
    EQ_DERIVATIVES_DESK: 'EQ',
    MONEY_MARKET_DESK: 'MM',
    IRD_DESK: 'IRD',
    LIQUID_ASSET_DESK: 'LA',
    REPO_DESK: 'RPO',
    FORWARDS_DESK: 'FRW',
    NON_LINEAR_DERIV: 'NLN',
    SWAPS_DESK: 'SWP',
    ZZZ_DO_NOT_USE_IRP_FX_DESK: 'IRP',
    NLD_DESK: 'NLD',
    BOND_DESK: 'BND',
    FOREX_DESK: 'FX',
    STRUCT_NOTEST_DESK: 'SND',
    CREDIT_DERIVATIVES_DESK: 'CDD',
    METALS_DESK: 'MET',
    GOLD_DESK: 'GLD',
    PRIME_SERVICES_DESK: 'PRS',
    PRIMARY_MARKETS: 'PM',
    IMPUMELELO: 'IMP',
    UHAMBO: 'UHM',
    NON_ZAR_IRD: 'NZI',
}

INSTYPE_SHORTCODE = {
    'Deposit':'Dep',
    'Option':'Opt',
    'Future/Forward':'Fut',
    'Zero':'Zero',
    'TotalReturnSwap':'TRS',
    'VarianceSwap':'VarSwap',
    'FRN':'FRN',
    'CD':'CD',
    'FRA':'FRA',
    'Cap':'Cap',
    'Floor':'Flr',
    'Swap':'Swp',
    'CurrSwap':'CSwp',
    'IndexLinkedSwap':'ILSwp',
    'FxSwap':'FxSwap',
    'Curr':'Curr',
    'Commodity':'Com'
}

CASHFLOWTYPE_SHORTCODE = {
    'Redemption Amount':'RedAmt',
    'Fixed Amount':'FixAmt',
    'Fixed Rate':'FixRate',
    'Call Fixed Rate Adjustable':'CFRA',
    'Premium':'Prem',
    'Fixed Rate Adjustable':'FixRateAdj',
    'Payout':'Payout',
    'Float Rate':'FltRate',
    'Security Nominal':'SecNom',
    'Redemption':'Redemption',
    'Cashflow Dividend':'CashDiv',
    'Coupon':'Coupon',
    'Total Return':'TotRet',
    'Caplet':'Cap',
    'Floorlet':'Floor',
    'Digital Caplet':'DigiCap',
    'Digital Floorlet':'DigiFlr',
    'Return':'Return',
    'Zero Coupon Fixed':'ZCFixed',
    'Fixed Rate Accretive':'FixRteAcr'
}

SETTLEMENT_RESTRICTED_FIELDS = {
    'Adjusted' : ['amount', 'curr', 'value_day', 'acquirer_ptyid', 'acquirer_accname', 'party_ptyid'],
    'Split' : ['party_ptyid'],
    'Ad Hoc Net' : ['acquirer_ptyid', 'acquirer_accname'],
    'Good Value' : ['value_day'],
    'Fair Value' : ['value_day']
}

EURO_COUNTRIES = set([
    'AT', 'BE', 'CH', 'DE', 'DK', 'ES', 'FI', 'FR', 'GB',
    'GR', 'HU', 'IE', 'IT', 'LU', 'NO', 'NL', 'PO', 'PT',
    'RO', 'RU', 'SE', 'TR' 
])

def is_foreign_payment(settl):
    '''Determines whether settlement done with foreign institution'''
    if settl.their_corr_bank2 != ''\
        or settl.their_corr_bank3 != ''\
        or settl.their_corr_bank4 != ''\
        or settl.their_corr_bank5 != '':
        return False
    # Country code embedded in the 4th and 5th character of BIC code
    if settl.their_corr_bank != '':
        country = ael.Party[settl.their_corr_bank].swift[4:6]
        for a in acm.FParty[settl.their_corr_bank].Aliases():
            if a.Type().Name() == 'SWIFT':
                country = a.Name()[4:6]
    else:
        return False
    curr = settl.curr.insid

    # Euro countries are aspecial case
    if country in EURO_COUNTRIES and curr == 'EUR':
        return True

    # General case
    if country != curr[:2]:
        return True

    return False


def isVostro(settlement):
    """Used to be able to identify if a settlement is marked as VOSTRO"""
    retVal = False
    #if (settlement.acquirer_ptynbr.ptyid in ('IRD DESK')):
    party = settlement.counterparty_ptynbr
    curr = settlement.curr.insid
    if party and curr == 'ZAR':
        bankIndicator = 'No'
        if party.business_status_chlnbr:
            if party.business_status_chlnbr.entry == 'Interbank':
                bankIndicator = 'Yes'            
        
        if bankIndicator == 'Yes':            
            foreignClient = 'No'
            if party.free2_chlnbr:
                foreignClient = party.free2_chlnbr.entry
            
            if foreignClient == 'Yes':
                if settlement.their_corr_bank != '':
                    if settlement.their_corr_bank == ABSA_BANK:
                        if settlement.party_account:
                            if 'ZAR' in settlement.party_account:
                                retVal = True
    return retVal


def get_is_internal(settl):
    internal = False
    if settl.their_corr_bank != '':
        if settl.their_corr_bank == ABSA_BANK:
            internal = True
    return internal

def get_Message_Type(settl):

    message_type = 'MT103'
    
    if get_is_internal(settl):
        message_type = 'MT103'
    else:
        party = settl.counterparty_ptynbr
        if not party:
            return message_type
        curr = settl.curr.insid
        
        bankIndicator = 'No'
        desk = settl.acquirer_ptynbr.ptyid
        if settl.party_account.__contains__('DIRECT'):
                bankIndicator = 'Yes'
        if bankIndicator == 'No':
            if party.business_status_chlnbr:
                if party.business_status_chlnbr.entry == 'Interbank':
                    bankIndicator = 'Yes'
        
        if curr == 'ZAR':
            if bankIndicator == 'No':
                if is_foreign_payment(settl):
                    message_type = 'MT205C103'
                else:
                    message_type = 'MT103'
            else:
                message_type = 'MT205'
        else:
            if bankIndicator == 'No':
                if is_foreign_payment(settl):
                    message_type = 'MT202C103'
                else:
                    message_type = 'MT103'
            else:
                message_type = 'MT202'
            
    return message_type
