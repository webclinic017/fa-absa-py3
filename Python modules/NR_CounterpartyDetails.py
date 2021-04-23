import ael

try:
     fd = open('C:\\CounterpartiesToDelete.csv')
except:
     print 'Input file could not be opened'

try:
    fo = open('C:\\Counterparty_Detail.csv', 'w')
except:
    print 'Output file could not be opened'
    
line = fd.readline()
list = []

fo.write('PtyNbr,PtyID,FullName,Type,Correspondent_Bank,Issuer,Create_Time,Can_Delete,FICA_Compliant' + '\n')

while line:
    list = line.split(',')
    
    p = ael.Party[(int)(list[0])]
    fo.write((str)(p.ptynbr) + ',' + p.ptyid.replace(',', '-') + ',' + p.fullname.replace(',', '-') + ',' + p.type + ',' 
                + (str)(p.correspondent_bank) + ',' + (str)(p.issuer) + ',' 
                + (str)(ael.date_from_time(p.creat_time))+ ',' + p.add_info('Cpty_Delete') + ',' + p.add_info('FICA_Compliant') + '\n')
    
    line = fd.readline()

fd.close()
fo.close()
