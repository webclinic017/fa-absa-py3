import ael



def change_exp(temp, trdnbr, day, *rest):

    olddate = ael.date_today().add_days(3)
    newdate = ael.date_today().add_days(6)   #'2008-05-05'
    #print olddate, newdate
    i = ael.Trade[trdnbr].insaddr.clone()
    i.exp_day = newdate
    try:
        i.commit()
        return 'Success'
    except:
        return 'not committed'
        
    return ''
    
    
def change_leg_end(temp, trdnbr, day, *rest):

    olddate = ael.date_today().add_days(3)
    newdate = ael.date_today().add_days(6)   #'2008-05-05'
    #print olddate, newdate
    l = ael.Trade[trdnbr].insaddr.legs()[0].clone()
    l.end_day = newdate
    try:
        l.commit()
        return 'Success'
    except:
        return 'not committed'
        
    return ''

