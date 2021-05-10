import ael


def ChangePartyType(temp, ptyid, type, *rest):
    result = '0'
    p = ael.Party[ptyid]
    if p.type:
        #print p.ptyid #, p.type
        if p.type != type:
            p_clone = p.clone()
            p_clone.type = type
            try:
                p_clone.commit()
                result = ptyid + ' committed'
            except:
                result = ptyid + ' failed to commit'
        else:
            result = 'Party already of type ' + type

        return result

    return result

    
#main
'''
PartyNames=['SECURITY SPV 3 PTY LTD']
for x in PartyNames:
    print ChangePartyType(1, x, 'Counterparty')
'''
    
