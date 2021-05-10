"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SAGEN_Missing_SSI

DESCRIPTION
    NONE
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-12-22      FAOPS-1022     Ncediso Nkambule         Kgomostso               Added Client party type to the party type check on the module
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import ael

def missingSSI(temp,trdnbr,*rest):
    t = ael.Trade[trdnbr]
    flag = 0
    exclCFType = []
    exclCFType.append('Interest Reinvestment')
    exclCFType.append('Redemption Amount')
    exclCFType.append('None')
    
    if t.trade_account_links().members() == []:
        return 0
    else:
        cashflowType = []
        cashflowType.append('Premium')
        i = t.insaddr
        for l in i.legs():
            for cf in l.cash_flows():
                if not exclCFType.__contains__(cf.type):
                    if not cashflowType.__contains__(cf.type):
                        cashflowType.append(cf.type)
        for tal in t.trade_account_links():
            if tal.party_type in ['Counterparty', 'Client'] and not exclCFType.__contains__(tal.settle_seqnbr.settle_cf_type) and cashflowType.__contains__(tal.settle_seqnbr.settle_cf_type):
                flag = 1
    if not flag:
        return 0
    else:
        return 1
