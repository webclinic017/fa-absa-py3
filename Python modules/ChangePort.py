import ael

def ChangePortfolio(temp, t, portfolio,*rest):
    portnumber = ael.Portfolio.read('prfid="%s"'%portfolio).prfnbr
    new = t.clone()
    new.prfnbr = portnumber
    #print t.prfnbr.prfid
    #print new.prfnbr.prfid
    try:
        new.commit()
        return 'Successful'
    except:
        return 'Failed'
    
def ChangeAcquirer(temp, t, acquirer,*rest):
    acqnbr = ael.Party[acquirer].ptynbr
    new = t.clone()
    #print t.acquirer_ptynbr.ptyid
    new.acquirer_ptynbr = acqnbr
    try:
        new.commit()
        return 'Successful'
    except:
        return 'Failed'

