import ael, acm

def change(temp, cfwnbr, day, *rest):

    olddate = ael.date_today().add_days(3)
    newdate = ael.date_today().add_days(6)   #'2008-05-05'
    #print olddate, newdate
    c = ael.CashFlow[cfwnbr]

    if day == 'start':
        if c.start_day == olddate:
            new_c = c.clone()
            new_c.start_day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    elif day == 'end':
        if c.end_day == olddate:
            new_c = c.clone()
            new_c.end_day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    elif day == 'pay':
        if c.pay_day == olddate:
            new_c = c.clone()
            new_c.pay_day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    else:
        return ''
        
    return 'Success'
                
    
    




def change_reset(temp, resnbr, day, *rest):

    olddate = ael.date_today().add_days(3)
    newdate = ael.date_today().add_days(6)   #'2008-05-05'
    #print olddate, newdate
    c = ael.Reset[resnbr]

    if day == 'start':
        if c.start_day == olddate:
            new_c = c.clone()
            new_c.start_day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    elif day == 'end':
        if c.end_day == olddate:
            new_c = c.clone()
            new_c.end_day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    elif day == 'pay':
        if c.day == olddate:
            new_c = c.clone()
            new_c.day = newdate
            try:
                new_c.commit()
            except:
                return 'could not commit'
                
    else:
        return ''
        
    return 'Success'
                
    



def w_reset(temp, cfwnbr, day, *rest):    
    #print dir(ael)
    olddate = ael.date_today().add_days(3)
    newdate = ael.date_today().add_days(6)    
    c = ael.CashFlow[cfwnbr]
    count = 0
    
    for r in c.resets():
        tbr = 0
        if r.day == newdate:
            count = count + 1
            tbr = tbr + 1
        if r.start_day == newdate:
            count = count + 1
            tbr = tbr + 1
        if r.end_day == newdate:
            count = count + 1
            tbr = tbr + 1
        if tbr == 3:
            x = r
    return count
    #print count
    '''
    if count == 4:
        #count == 4 for last reset of period
        if x:
            
            cc = c.clone()
            for y in c.resets():
                
                if y.resnbr == x.resnbr:
                    print 'delete this: ','count', count,'cfwnbr', cfwnbr, 'reset', y.resnbr, y.day, y.start_day, y.end_day
                    #print y.pp()
                    try:
                        #print 'Cashew'
                        rr = acm.FReset[y.resnbr]
                        rr.Delete()
                        print 'Has been deleted'
                        return 'SUCCESS'
                        #y.delete()
                    #    return 'Success'
                    except:
                        print 'DID NOT DELETE!!!!!!!!!!!!!!!!'
                        return 'FAIL'
            #try:
            #x.delete()
            
            #except:
            #    return 'cannot delete'

    return ''
    '''
    
    
#main
#olddate = ael.date_today().add_days(3)
#newdate = ael.date_today().add_days(6)
#print olddate, newdate
#print w_reset(1, 2102578, 'del')
    
#main
#print change(1, 1918174, 'pay')

