import ael, string

Global=[]
file = 'C:\\TelkomStructure.csv'

try:
    f = open(file)
    
except:
    print'Problem opening file'
    
line = f.readline()

while line:
    list=[]
    line = f.readline()
    line = line.rstrip()
    l = string.split(line, ',')
    if (l[0] == '\n' or l[0] == ''): break
    
    list.append(l[0])
    
    cutter = l[2] + '3'
    
    ins = ael.Instrument[l[0]]
    und = ins.und_insaddr.insid
    print l[0]
    list.append(und)
    
          
    list.append(cutter)
    
    ins = ins.clone()
    ins.und_insaddr = ael.Instrument[cutter]
    ins.commit()
    Global.append(list)
    #print cutter
    
f.close()

outfile = 'C:\\TelkomChanges.csv'

report = open(outfile, 'w')
Headers=[]
Headers = ['Instrument', 'UndIns', 'NewUnd']

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
print 'The file has been saved at: C:\\InstrChanges.csv'



