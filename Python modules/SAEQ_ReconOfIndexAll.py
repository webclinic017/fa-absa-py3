import ael
list=[]
index = ael.Instrument.select('instype = "EquityIndex"')

for i in index.members():
    list.append(i.insid)
    print(i.insid)
    ins = ael.Instrument[i.insid]
    ins = ins.clone()
    link = ins.combination_links()
    if link.members():
        for lnk in link.members():
            if lnk.member_insaddr.instype == 'Stock':
                list.append(i.insid)
                print(i.insid)
                cutter = lnk.member_insaddr.insid[0:7]
                cutter = (str)(cutter)
                clone = lnk.clone()
                clone.member_insaddr = ael.Instrument[cutter]
                clone.commit()
    ins.commit()
    
print(list)
