import ael

Lowest=[]

def Loop(filter,*rest):
    for p in filter.links().members():
    
        if p.member_prfnbr.compound == 0:
            Lowest.append(p.member_prfnbr)
        
        elif p.member_prfnbr.compound == 1:        
            Loop(p.member_prfnbr)
    return
    
    
def Portfolio():
    Ports = []
    for p in ael.Portfolio.select():
        Ports.append(p.prfid)
    Ports.sort()
    return Ports

ael_variables = [('Portfolio', 'Portfolio', 'string', Portfolio(), '9806', 1)]

def ael_main(ael_dict):
    Ports = ael_dict["Portfolio"]
    LowestLevel(1, Ports)

def LowestLevel(temp,Ports,*rest):        
    
    fil = ael.Portfolio[Ports]
    Loop(fil)
    outfile = 'C:\\Documents and Settings\\abfh101\\My Documents\\Work\\LowestLevelPortfolio.csv'
    report = open(outfile, 'w')
    
    Headers=['Portfolio']
    
    for i in Headers:
        report.write((str)(i))
        report.write('\n')
    
    for low in Lowest:
        report.write(low.prfid)
        report.write('\n')
    report.close()
    
    print 'The file has been saved at C:\LowestLevelPortfolio.csv'
    print 'Success'
    return    


