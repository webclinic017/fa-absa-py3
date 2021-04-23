import ael

Global=[]

ins = ael.Instrument['ZAR/FNDI']

link = ins.combination_links()

for lnk in link.members():
    list=[]
    inst = lnk.member_insaddr.insid
    price1 = ael.Instrument[inst].spot_price()
    price = ael.Instrument[inst].used_price()
    
    list.append(inst)
    list.append(price1)
    list.append(price)
    Global.append(list)
    
Global.sort()

outfile1 = 'C:\\FNDI.csv'
    
report = open(outfile1, 'w')
Headers=[]

Headers = ['Constituent', 'Price']
#print 'Counts', counts

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

print 'FNDI.CSV'
