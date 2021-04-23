'''
This is script has been written for the NOSTRO Migration of 
Barcalys Account information to Citi for USD and Socgen for EUR.
The first part deletes the extra EUR account as there are 2 and 
we will only correct the one line.
The second part takes in a predefined list of SSI names and 
replaces it with a new name as supplied by Operations. 

This is meant to be a once off script and not to be productionalised.
'''

import ael, acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

def change_party_si_names(party_name, change_from, change_to):
    party = acm.FParty[party_name]
    
    acm.BeginTransaction()
    
    try:
        for si in party.SettleInstructions():
            name = si.Name()
            if name.startswith(change_from):
                new_name = name.replace(change_from, change_to)
                si.Name(new_name)
                si.Commit()
                print "%s replaced with %s" % (name, new_name)
    except Exception as ex:
        print "ERROR: Change not successfull: %s" % ex
        acm.AbortTransaction()
        print "Operation aborted: No changes were saved."
    else:
        acm.CommitTransaction()
        print "Change successfully completed."

#change_party_si_names("ABSA BANK LTD", "ABMY", "ABMZ")        

#'ABCAP CRT','ABSA BANK LTD','ABSA BANK LIMITED','ABSA BANK LIMITEDCOPY','ACQ STRUCT DERIV DESK','AFRICA DESK','ALCO DESK ISSUER','BOND DESK','BOWWOOD AND MAIN NO 36 PTY LYD','CM Spot Trading','COLLATERAL DESK','CREDIT DERIVATIVES DESK','Capital Market Desk','Credit Derivs','EQ Derivatives Desk','EQUITY DERIVATIVES','ETN ISSUANCE','EUROGET ESKROW ACCOUNT','FORWARDS DESK','Funding Desk','Gold Desk','IRD DESK NONCSA','IRP_FX Desk','LIQUID ASSET DESK','MONEY MARKET DERIVATIVES','Metals Desk','Money Market Desk','NLD DESK','PRIMARY MARKETS','PRIME SERVICES DESK','REPO DESK','STRUCT NOTES DESK','Swaps Desk','BARCLAYS BANK MAURITIUS LIMITED OFFSHOR','IRD DESK'

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'NOSTRO_Migration_ChangeAccInfo'}
                      
ael_variables.add(
    'party',
    label = 'Party Name',
    cls = 'FParty',
    collection = None,
    default = None,
    mandatory = False,
    multiple = True,
    alt = 'Parties to amend'
    )

def ael_main(ael_dict):
    msg_box = acm.GetFunction('msgBox', 3)
    Party = ael_dict['party']
    for party in Party:
        for p in party.SettleInstructions():
            if p.Currency():
                if p.Currency().Name() == 'USD':
                    change_party_si_names(party.Name(), p.Name(), "CITI/10953008/USD")
                if p.Currency().Name() == 'EUR':
                    change_party_si_names(party.Name(), p.Name(), "SOGE/003014382170/EUR")
                    
    # Remove -> Party = ABSA BANK LTD; Account Number = 66986655
    party = acm.FParty['ABSA BANK LTD']

    for p in party.Accounts():
        if p.Account() == '66986655':
            try:
                p.Delete()
            except Exception, e:
                print 'Error in deleting Account: ', e

    # Remove -> Party = IRD DESK NONCSA; Account Number = 66986655
    party = acm.FParty['IRD DESK NONCSA']

    for p in party.Accounts():
        if p.Account() == '66986655':
            try:
                p.Delete()
            except Exception, e:
                print 'Error in deleting Account: ', e
