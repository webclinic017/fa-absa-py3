import ael
try:
    f = open('C:\\sep09.csv')
except:
    print 'Could not open file'
line = f.readline()
while line:
    mat = ['-90%', '-80%', '-70%', '-60%', '-50%', '-30%', '-25%', '-20%', '-15%', '-12.5%', '-10%', '-7.5%', '-5%', '-2.5%', '+0%', '+2.5%', '+5%', '+7.5%', '+10%', '+12.5%', '+15%', '+20%', '+25%', '+30%', '+50%', '+60%', '+70%', '+80%', '+90%', '+100%']
    line = line.rstrip()
    list = line.split(',')
    for m in mat:
        print list[0]
        
        ins = ael.Instrument[list[0]]
        insc = ins.new()
        plek = m.find('%')            
        insc.strike_price = (float)(m[0:plek])
        inspre = list[0][0:23]
        insc.insid = inspre + m
        try:
            insc.commit()
        except:
            print 'Not commited', insc.insid
        print (float)(m[0:plek]), insc.pp()
    line = f.readline()
f.close()
