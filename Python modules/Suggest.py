import ael
trds = ael.TradeFilter['SAFUND_No_Suggest'].trades()
for t in trds:
    instr = t.insaddr
    ins = instr.clone()
    print 'old', ins.insid
    ins.insid = ins.suggest_id()
    ins.commit()
    print 'new', ins.insid
