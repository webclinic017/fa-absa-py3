'''
Purpose: [Created to book mirror trades.]
Department: [PCG MONEY MARKET]
Requester: [Haroon Mansoor]
Developer: [Willie van der Bank]
CR Number: [C392817 (05/08/2010)]
'''

import acm, ael

def createAddInfo(t, name, value):
    #Creates the additional info for a trade
    
    ais = ael.AdditionalInfoSpec[name]
    for ai in t.additional_infos():
        if ai.addinf_specnbr == ais:
            ai.value = value
    return t  
    
def Set(temp,trd,*rest):
    print 'Original trade: ', trd
    trade = ael.Trade[trd]
    tradenom = trade.nominal_amount(trade.value_day)
    ins = trade.insaddr
    insnew = ins.new()
    insnew.issuer_ptynbr = 2247               #Funding Desk
    insnew.insid = insnew.suggest_id()
    newaddr = insnew.insaddr
    insnew.commit()
    ael.poll()
    print 'New instrument: ', insnew.insid
    tradenew = trade.new()
    tradenew.insaddr = insnew.insaddr
    tradenew.counterparty_ptynbr = 2247       #Funding Desk
    tradenew.status = 'Simulated'
    tradenew.document_type_chlnbr = 0
    tradenew.guarantor_ptynbr = 0
    tradenew.optional_key = ''
    tradenew.calcagent = 'None'
    
    #Update add infos
    if tradenom > 0:
        tradenew = createAddInfo(tradenew, 'Funding Instype', 'CL')
    else:
        tradenew = createAddInfo(tradenew, 'Funding Instype', 'CD')
    if tradenom > 0:
        tradenew = createAddInfo(tradenew, 'MM_Instype', 'CL')
    else:
        tradenew = createAddInfo(tradenew, 'MM_Instype', 'CD')
            
    #Delete add infos
    aisInsType = ael.AdditionalInfoSpec['Instype'].specnbr
    aisSafeCustody = ael.AdditionalInfoSpec['SafeCustody'].specnbr
    for add in tradenew.additional_infos():
        i = 1
        while i <= 11:
            AddInfo = 'Denom' + str(i)
            ais = ael.AdditionalInfoSpec[AddInfo].specnbr
            if (add.addinf_specnbr.specnbr == ais) or (add.addinf_specnbr.specnbr == aisInsType) or (add.addinf_specnbr.specnbr == aisSafeCustody):
                add.delete()
                break
            i = i + 1
    
    tradenew.commit()
    ael.poll()
    print 'New trade: ', tradenew.trdnbr
    return 'Updated...'
