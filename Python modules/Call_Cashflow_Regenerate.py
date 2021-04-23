import ael, string

file = 'C:/As_End_day/Call_Account/Call_Deposit_Upload_(Details).csv'
    
filename = open(file)
line = filename.readline()
line = filename.readline()
line = filename.readline()
line = filename.readline()
   
while line:
    lin = line.rstrip()
    lin = string.split(lin, ',')
    print lin[0]
    instrument = lin[0]
    line = filename.readline()
    ins = ael.Instrument[instrument]
    l = ins.legs()[0]
    lc = l.clone()
    lc.regenerate()
    lc.commit()
    ael.poll()
