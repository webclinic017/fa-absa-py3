import ael
try:
    f = open('C:\\lindaCP2Broker.csv')
except:
    print('Could not open file')
line = f.readline()
while line:
    list = []
    line = line.rstrip()
    list = line.split(',')
    cp = ael.Party[list[0]]
    cpc = cp.clone()
    cpc.type = 'Broker'
    print(cpc.ptyid)
    cpc.commit()
    line = f.readline()
