import ael


def change_float_ref(temp, t, *rest):
    t = ael.Trade[t]
    flag = 0
    t_clone = t.clone()
    legs = t_clone.insaddr.legs()
    for l in legs:
        if l.type == 'Float' and l.float_rate.insid == 'ZAR-PRIME':
            print(l.float_rate.insid)
            new_float = ael.Instrument['ZAR-PRIME-3M']
            
            l_clone = l.clone()
            l_clone.float_rate = new_float
                        
            try:
                l_clone.commit()
            except:
                print('Error committing Trade ', t.trdnbr)
                flag = 1
                
    if flag == 0:
        return 'Success'
    else:
        return 'Failed'
        
        
#t_clone.premium = 4100000.00
#t_clone.commit()
