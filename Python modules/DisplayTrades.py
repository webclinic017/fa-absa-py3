import ael
import string

src=open('C:\\ccc\\trades.csv', 'r')
line=src.readline()
rows=[]
i = 1
deli = "|"
while line != '':
    rows.append(string.split(line, '\t'))
    line=src.readline()
    trd = string.split(line, ',')[0]
    if len(trd) > 0:
        trds = ael.Trade[int(trd)]
        print trd, deli, trds.status, deli, trds.insaddr.instype, deli, trds.insaddr.exp_day
    i=i+1
        #print ael.Trade[line].trdnbr 
src.close()
