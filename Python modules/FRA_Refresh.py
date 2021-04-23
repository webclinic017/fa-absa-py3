
#runs daily at 11:10 am to refresh all FRAs with a reset today

import ael, SAGEN_Resets

def FraChecker(temp, *rest):
    ins = ael.Instrument.select('instype = "FRA"')
    for i in ins:
    #i = ael.Instrument['ZAR/FRA/JI/071018-071130/10.50']
        for l in i.legs():
            #print ael.date_from_string(SAGEN_Resets.CurrentReset(1, l.legnbr, ael.date_today(), 3))
            if ael.date_from_string(SAGEN_Resets.CurrentReset(1, l.legnbr, ael.date_today(), 3)) == ael.date_today():
                for t in i.trades():
                        #print t.time
                        tc = t.clone()
                        tc.time = t.time + 1
                        try:
                            tc.commit()
                        except:
                            print('Cannot change trade ', t.trdnbr)
                            
#main
FraChecker(1)
