import ael
try:
    f = open('C:\\trade.tab')
except:
    print('could not open file')

line = f.readline()
while line:
    print(line)
    list = []
    line = f.readline()
    list = line.split('\t')
    print(list)
f.close()
