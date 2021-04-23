import ael, string

infile = 'c:\\reset_supportfix_zar3.csv'

f = open(infile)
i = 0
line = f.readline()
ael.log('Started loading from %s.' %infile)
resetslist=[]
while line:
    rno, vd, cst, ced = string.split(line, ',')
    
    rst = ael.Reset.read('resnbr = %s' %rno)
    xc = rst.clone()
    xc.day = ael.date_from_string(vd)
    xc.start_day = ael.date_from_string(cst)
    xc.end_day = ael.date_from_string(ced)

    xc.commit()

    resetslist.append(rno)
    i = i + 1
    print i, rno
    line = f.readline()
    

print resetslist
