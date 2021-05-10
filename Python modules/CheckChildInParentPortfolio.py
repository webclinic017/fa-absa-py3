import ael

Lowest=[]

def Loop(filter,*rest):
    for p in filter.links().members():
        if p.member_prfnbr.compound == 0:
            Lowest.append(p.member_prfnbr)
        elif p.member_prfnbr.compound == 1:        
            Loop(p.member_prfnbr)

    return Lowest
    
def Portfolio():
    Ports = []
    for p in ael.Portfolio.select():
        Ports.append(p.prfid)
    Ports.sort()
    return Ports

def LowestLevel(temp,Ports,prfid,*rest):        
    fil = ael.Portfolio[Ports]
    pf = Loop(fil)
    for p in pf:
        if prfid == p.prfid:
            return 1
    return 0
