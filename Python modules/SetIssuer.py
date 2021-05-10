'''
Purpose: Adds Issuer to trades. Is Called by SetIssuer ASQL.
Department: PCG MONEY MARKET
Requester: Gill Dailey
Developer: Willie van der Bank
CR Number: C2826 (16/03/2010)(C000000253926)
'''

import acm, ael

def Set(temp,trd,iss,*rest):
    trade = ael.Trade[trd]
    ins = trade.insaddr
    insclone = ins.clone()
    insclone.issuer_ptynbr = iss
    insclone.commit()
    ael.poll()
    return 'Updated...'
