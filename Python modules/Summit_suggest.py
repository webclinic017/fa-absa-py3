import ael
trds = ael.Portfolio['Summit Portfolio'].trades()
for t in trds:
    instr = t.insaddr
    if instr.instype in ('Cap', 'Floor'):
        ins = instr.clone()
        print 'old', ins.insid
        ins.insid = ins.suggest_id()
        try:
            ins.commit()
            print 'new', ins.insid
        except:
            print t.trdnbr, ' not changed'
