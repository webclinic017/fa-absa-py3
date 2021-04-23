import ael

filename = "C:\changeTrades.csv"
dateChange = ael.date_from_string("2008-03-19")

try:
    f = open(filename)
except:
    print('Could not open password file')
    
line = f.readline()
while line:
    print(int(line))
    InsCopy = ael.Trade[int(line)].clone()

    InsCopy.acquire_day = dateChange
    InsCopy.value_day = dateChange

    InsCopy.commit()
    
    line = f.readline()

f.close()
