import ael
try:
    f = open('C:\\i.csv')
except:
    print('Could not open file')

line = f.readline()
list = []
while line:
    line = line.rstrip()
    list = line.split(',')
    ic = ael.Instrument[list[0]].clone()
    cl = ael.ChoiceList['SAEQ_WARRANTS']
    print(cl.entry)
    ic.product_chlnbr = cl
    print(ic.product_chlnbr.entry)
    #ic.commit()    
    line = f.readline()
f.close()
