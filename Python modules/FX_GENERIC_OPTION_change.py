import ael
try:
    f = open('C:\\FXOPT_Generics.csv')
except:
    print('Could not open file')
line = f.readline()
while line:
    line = line.rstrip()
    list = []
    list = line.split(',')
    i = ael.Instrument[list[0]]
    print(list[0])
    print(list[1])
    if i:
        print(list[0])
        ic = i.clone()
        print(list[1])
        ic.insid = list[1]
        try:
            ic.commit()
        except:
            print('Duplicate')
    line = f.readline()
f.close()
