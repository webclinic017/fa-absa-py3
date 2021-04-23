import ael, acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

#'ABCAP CRT','ABSA BANK LTD','ABSA BANK LIMITED','ABSA BANK LIMITEDCOPY','ACQ STRUCT DERIV DESK','AFRICA DESK','ALCO DESK ISSUER','BOND DESK','BOWWOOD AND MAIN NO 36 PTY LYD','CM Spot Trading','COLLATERAL DESK','CREDIT DERIVATIVES DESK','Capital Market Desk','Credit Derivs','EQ Derivatives Desk','EQUITY DERIVATIVES','ETN ISSUANCE','EUROGET ESKROW ACCOUNT','FORWARDS DESK','Funding Desk','Gold Desk','IRD DESK NONCSA','IRP_FX Desk','LIQUID ASSET DESK','MONEY MARKET DERIVATIVES','Metals Desk','Money Market Desk','NLD DESK','PRIMARY MARKETS','PRIME SERVICES DESK','REPO DESK','STRUCT NOTES DESK','Swaps Desk','BARCLAYS BANK MAURITIUS LIMITED OFFSHOR','IRD DESK'


aliasUSD = acm.FPartyAlias[112045] #CITIUS33
aliasEUR = acm.FPartyAlias[112220] #SOGEFRPP

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
        for p in party.Accounts():
            if p.Currency():
                if p.Currency().Name() == 'USD':
                    if p.Account() == '50038826':
                        # change the account details to the following
                        p.CorrespondentBank('CITIBANK NA')
                        p.Account('10953008')
                        p.Bic(aliasUSD)
                        try:
                            p.Commit()
                        except Exception, e:
                            print 'Error in committing new details for Account: ', p.Name(), 'Party: ', party.Name(), 'with error :', e
                
                if p.Currency().Name() == 'USD':
                    if p.Account() == '050038826':
                        # change the account details to the following
                        p.CorrespondentBank('CITIBANK NA')
                        p.Account('010953008')
                        p.Bic(aliasUSD)
                        try:
                            p.Commit()
                        except Exception, e:
                            print 'Error in committing new details for Account: ', p.Name(), 'Party: ', party.Name(), 'with error :', e
                    
                if p.Currency().Name() == 'EUR':
                    if p.Account() == 'GB23BARC20325366986655':
                        # change the account details to the following
                        p.CorrespondentBank('SOCIETE GENERALE PARIS')
                        p.Account('003014382170')
                        p.Bic(aliasEUR)
                        try:
                            p.Commit()
                        except Exception, e:
                            print 'Error in committing new details for Account: ', p.Name(), 'Party: ', party.Name(), 'with error :', e
