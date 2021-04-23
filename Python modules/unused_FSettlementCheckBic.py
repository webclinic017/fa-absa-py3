""" Settlement:1.2.2.hotfix23 """

import ael
import re

'''
# FValidation can be implemented in the following way
import ael, FSettlementCheckBic

def validate_transaction(transaction_list, *rest):
    for (o, op) in transaction_list:
        if o.record_type == "Party" and op not in ('Delete'):
            if FSettlementCheckBic.check_party_bics(o) == 0:            
                raise "FValidation:Invalid Party BIC code(s)"
    return transaction_list

# From Information manager:
select 
    p.ptyid 'Party',
    p.swift 'Party.swift',  
    ael_s(p,'FSettlementCheckBic.check_party_bics',1,1,1) 'Validation',
    ael_s(p,'FSettlementCheckBic.get_party_aliases',1) 'SWIFT Party Alias',
    ael_s(p,'FSettlementCheckBic.check_party_bics',2,1,1) 'Validation'
from party p
order by 3,5

'''

not_upper_case= re.compile(r'[^A-Z]') 
lower_case= re.compile(r'[a-z]') 
digit = re.compile(r'[0-9]') 
not_digit = re.compile(r'[^0-9]') 
alphanumeric = re.compile(r'[\da-zA-Z]')
not_alphanumeric = re.compile(r'[^\da-zA-Z]')
alphanumeric_onlyuppercase = re.compile(r'[\dA-Z]')
non_alphanumeric_onlyuppercase = re.compile(r'[^\dA-Z]')
strange_sign = re.compile(r'[\W]')
swift_alias = ael.InstrAliasType['SWIFT']
NO_SWIFT_ALIAS = 'NO SWIFT alias'

def check_bic_code(party,partyalias=None,mode=1,noLog=0):
    '''
    Returns 1 if BIC ok. BIC can be either party.swift or 
    SWIFT Party alias. Mode = 1 means that party.swift is checked
    while mode == 2 is SWIFT Party alias.
    
    Bank identifier code (BIC)
    An International Organisation for Standardisation, 
    technical code that uniquely identifies a financial institution. 
    SWIFT is the registration authority for BICs. 
    The BIC consists of eight or eleven characters, comprising a 
    financial institution code (four characters), 
    a country code (two characters), 
    a location code (two characters), 
    and for FIN and IFT, an optional branch code (three characters).
    
    Example of a valid BIC: NDEASEGGXXX
    '''
    #BANKCCLLO
    ERR0="Err0: BIC code should be 8 or 11 characters long"

    #aaaaaa21
    ERR1="Err1: Only capital letters are allowed in the institution code"

    #a1aaaa21
    ERR2="Err2: No numbers are allowed in the institution code"

    #AAAAAA1B
    ERR3="Err3: Only capital letters are allowed in the country code"

    #AAAA1A1B
    ERR4="Err4: No numbers are allowed in the country code"

    #AAAAAABb
    ERR5="Err5: Only capital letters and numbers are allowed in the location code"

    #AAAAAA21333, AAAAAA2133A
    ERR6="Err6: Optional branch code must be 3 characters long"

    ERR7="Err7: Only capital letters and numbers are allowed in the Optional branch code"
    ERR8="Err8: Strange character in the"

    ERR10 = "is not valid"
    VALOK = 'validated OK\n'
    
    ptyid = ''
    str = "\n-- Checking SWIFT Bic code(s) --"
    modeStr = 'party.swift'
    if mode==2:
        modeStr='SWIFT Party alias'
        
    str = '%s (mode: %s)' % (str, modeStr)
    if noLog != 1:
        ael.log(str)
    
    if not partyalias and mode==2:                        
        return 1

    if not party:
        ael.log('No Party deployed to FSettlementCheckBic.check_bic_code')
        return 0
    else:
        ptyid = party.ptyid
              
    if noLog != 1:    
        str = "Party %s has %s = %s" % (ptyid, modeStr, partyalias)
        ael.log(str)

    ok_bic = 1 # not eroneus bic
    le = len(partyalias) 
    if le==0 and mode==1:
        # party.swift is ok empty
        return 1
    
    if not (le in [8, 11]):
        ok_bic = 0
        ael.log("%s (%s)" % (ERR0, partyalias))

        if le > 11:
            ael.log("%s" % (ERR6))
        
    else:      
        bank_code = partyalias[:4]
        country_code = partyalias[4:6]
        location_code = partyalias[6:8]
        branch_code = None

        if le == 11:
            branch_code = partyalias[8:]                       

        if not_upper_case.search(bank_code):
            ok_bic = 0
            if lower_case.search(bank_code):
                ael.log("%s %s" % (ERR1, bank_code))

            if digit.search(bank_code):
                ael.log("%s %s" % (ERR2, bank_code))

            if strange_sign.search(bank_code):
                ael.log("%s %s" % (ERR8, bank_code))

        if not_upper_case.search(country_code):
            ok_bic = 0
            if lower_case.search(country_code):
                ael.log("%s %s" % (ERR3, country_code))

            if digit.search(country_code):
                ael.log("%s %s" % (ERR4, country_code))

            if strange_sign.search(country_code):
                ael.log("%s %s" % (ERR8, bank_code))

        if non_alphanumeric_onlyuppercase.search(location_code):
            ael.log("%s %s" % (ERR5, location_code))
            ok_bic = 0

        if branch_code:
            if non_alphanumeric_onlyuppercase.search(branch_code):
                ael.log("%s %s" % (ERR7, branch_code))
                ok_bic = 0

    if not ok_bic:
        ael.log("%s: %s %s (%s)\n" % (ptyid, partyalias, ERR10, modeStr))
    elif noLog != 1:
        ael.log("%s %s" % (partyalias, VALOK))

    return ok_bic


def check_party_bics(party,mode=0,asqlMode=0,noLog=1,*rest):
    ''' 
    party    - party entity
    mode     - 0 Checks both party.swift and SWIFT Party alias
               1 Checks party.swift
               2 Checks SWIFT Party alias
    asqlMode - 0 returns boolean
               1 returns stringpresentation
    noLog    - default 1 errors and info will be logged
               0 nothing will be logged to AEL Console
    '''
    ok_alias = 1
    aliases = get_party_aliases(party, 0, noLog)
    if len(aliases):        
        for pa in aliases:    
            if check_bic_code(party, pa.alias, 2, noLog) == 0:
                ok_alias=0
                break
    ok_bic = check_bic_code(party, party.swift, 1, noLog)                
    if mode==1:
        ok_alias=1
    if mode==2:
        ok_bic = 1
    
    ret = ok_bic and ok_alias
    if asqlMode and ret:
        return 'OK'
    elif asqlMode and not ret:
        return 'Invalid'
    else:
        return ret


def get_party_aliases(party,asqlMode=0,noLog=1,*rest):
    '''Retrieve all Party aliases
    party    - party entity
    asqlMode - 0 returns a list
               1 returns a stringpresentation of the aliases
    noLog    - default 1 errors and info will be logged
               0 nothing will be logged to AEL Console
    '''
    pas = []
    swift_pas = [] #more then one swift alias is possible
    
    if party:        
        pas = party.aliases()
    elif noLog != 1:
        ael.log('get_party_aliases: no party deployed')
        
    for pa in pas:        
        if pa.type == swift_alias: 
            swift_pas.append(pa)
    
    if len(swift_pas) > 1:
        if noLog!=1:
            ael.log('Party %s has %d SWIFT aliases! (first will be used)'%(party.ptyid, len(swift_pas)))

    if asqlMode:
        tmp = swift_pas
        swift_pas = ''
        for al in tmp:
            swift_pas = "%s %s" % (swift_pas, al.alias)
            
    return swift_pas
    

def check_allparty_bics(party=None,noLog=0):
    ''' Checks bic code of all parties.
    Logging will done in this case.'''

    for party in ael.Party.select():
        if party.swift:
            check_bic_code(party, party.swift, 'party.swift', noLog)
            
            
def test():
    '''Test function for bic code validation'''
    test = ['BANKCCLL', 'BaNKCCLL', 'BA1KCCLL', 'Ba1KCCLL', 'BAN@CCLL', 'BANKcCLL',
'BANKC1LL', 'BANK*CLL', 'BANKCC2L', 'BANKCCLa', 'BANKCC33', 'BANKCCLLXX1', 'BANKCCLLXc1',
'BANKCCLLcXX', 'BANKCCLL1XX', 'BANK', 'BANKBANBB']

    for t in test:
        check_bic_code(ael.Party.select()[0], t)


def test_all_parties():
    '''Test function for all parties, both SWIFT Party alias and party.swift is validated.'''
    for p in ael.Party.select():    
        check_party_bics(p, 0, 0)

#test_all_parties()


