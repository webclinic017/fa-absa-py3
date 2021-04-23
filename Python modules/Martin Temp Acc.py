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

    lst = (130601, 130614, 130615, 130621, 130626, 130627, 130635, 130643, 130646, 130648, 130653, 130660, 130671, 130673, 130677, 130685, 130692, 130698, 130711, 130712, 131185, 131186, 131366, 131449, 131450, 131451, 131453, 131518, 133292, 134905, 135191, 156694, 165449, 165456, 171973, 180066, 180213, 185945, 207134, 208195, 208308, 208353, 208530, 208554, 208555, 208560, 208655, 209162, 214082, 214085, 215939, 215953, 216082, 216083, 216085, 217526, 217533, 218343, 218363, 218371, 218394, 218401, 218513, 218516, 218518, 219803, 221397, 221413, 221421, 221525, 221942, 221944, 221946, 221948, 221949, 221950, 221952, 221954, 221955, 223414, 225500, 225501, 225519, 226208, 226331, 226345, 226350, 226361)


    

    for l in lst:

        print l

        lg = ael.Leg[l]        

        for cf in lg.cash_flows():

            if cf.pay_day > dt:

                if cf.start_day > dt:
                
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

    trds = (1025791, 1025821, 1025883, 1031812, 1033262, 1033268, 1033444, 1041206, 556747, 556760, 556761, 556767, 556771, 556772, 556780, 556788, 556791, 556793, 556798, 556805, 556815, 556817, 556821, 556825, 556830, 556832, 556843, 556844, 557315, 557316, 557496, 557579, 557580, 557581, 557583, 557648, 559422, 561035, 561321, 641731, 688556, 688565, 736062, 778745, 779465, 803337, 896984, 901623, 902089, 902409, 903145, 903356, 903380, 903383, 903812, 906443, 926212, 926783, 934484, 934521, 937167, 937198, 937200, 943210, 943249, 951016, 951103, 951147, 951376, 951409, 952131, 952144, 952154, 964449, 977080, 977156, 977191, 977830, 982438, 982442, 982448, 982452, 982454, 982456, 982460, 982464, 982466, 998010)   

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

                    if cf.pay_day > dt:

                        #print 'cf', cf.start_day, cf.end_day
                        
                        if cf.start_day > dt:

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

 

