import ael
def CommCCY(t,*rest):
    
    ins = ael.Instrument.read('insaddr=%d'% t.insaddr.insaddr)
    
    a =  t.counterparty_ptynbr.ptyid
    b =  t.prfnbr.prfid
    c =  'Bond'
    output =  c + b + a
    return output
