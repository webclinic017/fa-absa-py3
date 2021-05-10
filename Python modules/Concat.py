import ael
def CommCCY(t,*rest):
    
    ins = ael.Instrument.read('insaddr=%d'% t.insaddr.insaddr)
    
    a =  ins.curr.insid
    b =  ins.und_insaddr.insid
    output =  b + '-' + a
    return output
