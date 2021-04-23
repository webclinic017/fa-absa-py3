import ael, string
Global=[]

ins = ael.Instrument.select('instype = "EquityIndex"')

for i in ins.members():

    link = i.combination_links()
    
    for lnk in link.members():
        list=[]
        
        index = i.insid
        const = lnk.member_insaddr.insid
        weight = lnk.weight
        factor = i.index_factor
        mtm = lnk.member_insaddr.mtm_price(ael.date_today(), i.curr.insid, 0, 0)
        mtmindex = i.mtm_price(ael.date_today(), i.curr.insid, 0, 0)
        
        list.append(index)
        list.append(const)
        list.append(weight)
        list.append(factor)
        list.append(mtm)
        list.append(mtmindex)
        Global.append(list)

Global.sort()
print Global
               

outfile = 'C:\\IndexAfter.csv'

report = open(outfile, 'w')
Headers=[]

Headers = ['Index', 'Constituent', 'Weight', 'Factor', 'ConstPrice', 'IndexPrice']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')
    

for lsts in Global:
    
    for ls in lsts:
        
        report.write((str)(ls))
        report.write(',')
    report.write('\n')
    
report.close()
print 'Success'
print 'The file has been saved at: C:\\IndexAfter.csv'

