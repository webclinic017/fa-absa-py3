import ael, string

file = 'C:\\SIFISO2.csv'

try:
    sheet = open(file)
except:
    print 'Problem opening the file'
    
line = sheet.readline()

while line:
    
    line = sheet.readline()
    #print dir(line)
    l = line.split(',')
    if (l[0] == '\n' or l[0] == ""): break
    
    list=[]
    for i in l:
        reg = i.lstrip()
        reg = reg.rstrip()
        list.append(reg)
    
    ins = ael.Instrument[list[0]]
    
    if ins.strike_price > 0:
        
        new = ins.clone()
        new.strike_price = ins.strike_price * (-1)
        new.commit()
        ael.poll()
        
        print ins.strike_price
