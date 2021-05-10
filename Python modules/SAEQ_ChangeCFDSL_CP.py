import ael
trds = ael.Portfolio['CFD'].trades()
for t in trds:
    tc = t.clone()
    flag = 0
    if t.status != 'Void' and t.status != 'Simulated':
        if t.counterparty_ptynbr.ptyid == 'AED':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES ASLCFD COLLATERAL']
            flag = 1
        if flag == 1:
            tc.commit()
