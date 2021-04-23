import ael
try:
    f = open('C:\\dup.csv')
except:
    print('Not opened')
line = f.readline()
line = f.readline()
while line:
    line = line.rstrip()
    trd = ael.Trade[(int)(line)]
    trdc = trd.clone()
    trdc.status = 'Void'
    trdc.commit()
    print(trd)
    line = f.readline()
f.close()
