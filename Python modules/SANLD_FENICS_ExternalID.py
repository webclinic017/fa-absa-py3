import ael  
infile = open('C:\\NLDEXTERNALID.csv')
line = infile.readline()
line = infile.readline()
while line:
    a, b, c, d = line.split(',')
    trd = ael.Trade[(int)(a)]
    d = d.rstrip()
    print trd.trdnbr, trd.optional_key, d
    trdclone = trd.clone()
    trdclone.optional_key = d
    print trdclone.optional_key
    trdclone.commit()
    line = infile.readline()   
infile.close()
