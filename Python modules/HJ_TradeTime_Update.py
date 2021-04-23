import ael
try:
    f = open('C:\\tt.csv')
except:
    print('Could not open file')

line = f.readline()
list = []
while line:
    line = line.rstrip()
    list = line.split(',')
    trdc = ael.Trade[(int)(list[0])].clone()
    if trdc.time == -3599:
        trdc.time = ael.to_time(trdc.value_day)
    print(trdc.time)
    trdc.commit()    
    line = f.readline()
f.close()
