import ael
try:
    f= open('C:\\delcfds1220.csv')
except:
    print('Unable to open file')
line = f.readline()
while line:
    list = []
    line = line.rstrip()
    list = line.split(',')
    trd = ael.Trade[(int)(list[0])]
    print(trd)
    trd.delete()
    line = f.readline()
