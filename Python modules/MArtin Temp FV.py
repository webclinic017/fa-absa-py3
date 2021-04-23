import ael

 

def fixday():

    dt = ael.date_today()

 

    lst = (153656, 19831, 19839, 19851, 19869, 19873, 19893, 19911, 19915, 19935, 19945, 19963, 20001, 20021, 20029, 20503, 20925, 21877, 21933, 25385, 25387, 27152, 42071, 50187, 51434, 51497, 51499, 51508, 51523, 53995, 54115, 115277, 125698, 162704, 162495, 162631, 179520, 179578, 184108, 207134, 208195, 208308, 208353, 208530, 208555, 208560, 208655, 209162, 208554, 214082, 203722, 197847, 196980, 215223, 216082, 180031, 217526, 218343, 218363, 218371, 218394, 218401, 218513, 218516, 218518, 219803, 221397, 221413, 221421, 221525, 221942, 221944, 221946, 221948, 221949, 221950, 221952, 221954, 221955, 223414, 225500, 225501, 225519, 226208, 226345, 226350, 226361, 226331)

 

    for l in lst:        

        lg = ael.Leg[l]        

        for cf in lg.cash_flows():

            if cf.pay_day > dt:

                if len(cf.resets()) > 1:

                    print 'mult resets', lg.insaddr.insid

                else:                

                    for r in cf.resets():

                        if r.start_day <> cf.start_day:

                            print 'startday', lg.insaddr.insid, r.start_day, cf.start_day

                            rc = r.clone()

                            rc.start_day = cf.start_day

                            rc.commit()

                            

                        if r.end_day <> cf.end_day:

                            print 'endday', lg.insaddr.insid, r.end_day, cf.end_day

                            rc = r.clone()

                            rc.end_day = cf.end_day

                            rc.commit()

                            

                        if r.day <> r.start_day:

                            print 'payday', lg.insaddr.insid, r.day, r.start_day

                            rc = r.clone()

                            rc.day = r.start_day

                            rc.commit()

                      

#fixday()

def sprd():

    dt = ael.date_today()

    lst = (115276, 115277, 125698, 125699, 153656, 153657, 162494, 162495, 162630, 162631, 162703, 162704, 179520, 179521, 179577, 179578, 180030, 180031, 184108, 184109, 196979, 196980, 197847, 197848, 19831, 19832, 19839, 19840, 19851, 19852, 19869, 19870, 19873, 19874, 19893, 19894, 19911, 19912, 19915, 19916, 19935, 19936, 19945, 19946, 19963, 19964, 20001, 20002, 20021, 20022, 20029, 20030, 203722, 203723, 20503, 20504, 20925, 20926, 215223, 215224, 21877, 21878, 21933, 21934, 25385, 25386, 25387, 25388, 27151, 27152, 42071, 42072, 50186, 50187, 51434, 51435, 51496, 51497, 51498, 51499, 51508, 51509, 51523, 51524, 53995, 53996, 54115, 54116)
   

    for l in lst:

        print l

        lg = ael.Leg[l]        

        for cf in lg.cash_flows():

            if cf.pay_day > dt:
               
                
                sprdold = cf.spread                

                cfc = cf.clone()

                cfc.spread = 0.1                

                cfc.commit()

                print l, cf.cfwnbr, sprdold, cfc.spread, cf.spread

                

sprd()



 

pe = {}

fltref = []

save_chg = -1

 

def read_pe(float_ref):

    #print '===========>>>>  reading price entry for', float_ref.insid

    hp = float_ref.historical_prices()

    for prc in hp:

        tpl = (float_ref.insid, prc.day.to_string())        

        pe[tpl] = prc.settle

    

def check_fixings():

    dt = ael.date_today()

    trds = (641734, 642395, 642422, 642438, 642476, 642485, 642502, 642504, 642505, 642506, 642507, 642520, 642524, 642536, 642537, 642542, 642543, 642544, 642545, 642547, 642553, 642554, 642558, 642562, 642564, 642565, 642566, 642567, 642568, 642575, 642577, 642586, 642590, 688541, 688543, 688544, 778548, 779454, 800885, 920876, 934318, 934321, 934642, 940185)
   

    for trd in trds:

        ins = ael.Trade[trd].insaddr

        print'\n -----------------------------------------'

        print trd

        

        for leg in ins.legs():                    

            if leg.type == 'Float': 

                print '------------'

                flt = leg.float_rate.insid

                print 'leg', leg.curr.insid, flt                

                if flt not in fltref:                    

                    fltref.append(flt)

                    read_pe(leg.float_rate)

                    #print pe

                for cf in leg.cash_flows():                

                    #print 'cf', cf.start_day, cf.end_day
                    
                    if cf.pay_day > dt:

                            for r in cf.resets(): 
    
                                if r.type == 'Single': 
    
                                    if r.day > dt and r.value <> 0.0:
    
                                        if save_chg == -1:
    
                                            rc = r.clone()
    
                                            rc.value = 0.0
    
                                            rc.commit()                                    
    
                                        print 'fixing not due but has value', r.day, r.value, leg.insaddr.insid
    
                                    if r.day < dt:
    
                                        tpl = flt, r.day.to_string()
    
                                        if tpl in pe.keys():                                        
    
                                            if r.day <= dt and r.value <> pe[tpl]:
    
                                                if save_chg == -1:
    
                                                    rc = r.clone()
    
                                                    rc.value = pe[tpl]
    
                                                    rc.commit()                                            
    
                                                print 'fixing not equal to price netry', r.day, r.value, pe[tpl], r.value - pe[tpl]
    
                                        else:
    
                                            print '**ERROR**    price entry does not exist', tpl

                        

#check_fixings()
