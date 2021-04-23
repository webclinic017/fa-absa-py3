import ael

 

new_port_id =  'CM_Graveyard'

new_port = ael.Portfolio[new_port_id]

 

sfile = 'c:\\temp1\\exp.txt'

 

f = open(sfile, 'r')

 

s = f.readline()

 

while s <> '':    

    trdnbr = int(s)

    trd = ael.Trade[trdnbr]

    port = trd.prfnbr.prfid

    print('changing trade', trd.trdnbr, port)

    if trd.prfnbr <> new_port:

        ctrd = trd.clone()

        ctrd.prfnbr = new_port

        ctrd.commit()

        trd = ael.Trade[trdnbr]

        print('changed', trdnbr, trd.prfnbr.prfid)

    else:

        print('trade already changed')

    

    print('')

    s = f.readline()

 

f.close()

 
