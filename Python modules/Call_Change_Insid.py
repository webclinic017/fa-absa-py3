import ael

def ChangeInsid(temp,insaddr,*rest):
    ins = ael.Instrument[insaddr]
    i = ins.clone()
    i.insid = ins.insid[0:18]
    print(i.insid)
    i.commit()
    return 'Done'
