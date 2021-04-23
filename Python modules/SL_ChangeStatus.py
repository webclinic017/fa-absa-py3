import ael
def change_to_fo(i,port,*rest):
    p = ael.Portfolio[port].prfnbr
    print p
    trds = ael.Trade.select('prfnbr = %d' %(p))
    print trds
    list = []
    for t in trds:
        if t.status == 'Simulated':
            tc = t.clone()
            tc.status = 'FO Confirmed'
            print tc.trdnbr, ' ', tc.status
            try:
                tc.commit()
            except:
                list.append((tc.trdnbr, tc.counterparty_ptynbr.ptyid))
            #tc.commit()
    print list
    return 'Success'
#change_to_fo(1,'CFD')
