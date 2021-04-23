import ael

def Call_Rolling_Interest(c,fromd,to,*rest):
    l = c.legnbr
    gendate = l.rolling_base_day
    
    if gendate == to:
        return 'in'
    else:
        return 'out'
    
    

def Call_Rolling_Interest2(c,fromd,to,*rest):
    l = c.legnbr
    gendate = l.rolling_base_day
    count = 1
    
    if l.rolling_period == '0d':
        return 'out'
        
    '''
    while (int)(gendate.to_string('%m')) < (int)(to.to_string('%m')) or ((int)(gendate.to_string('%m')) == 12 and (int)(gendate.to_string('%Y')) < (int)(to.to_string('%Y'))):
        gendate = gendate.add_period(l.rolling_period)
        print '2', gendate
    '''
    while gendate <= to.add_months(-1):
        gendate = gendate.add_period(l.rolling_period)
     
    gendate = gendate.adjust_to_banking_day(l.insaddr.curr, l.reset_day_method)    

    if gendate == to:
        return 'in'
    else:
        return 'out'




'''
c = ael.CashFlow[1999318]
#trdnbr = 1581997
d = ael.date_from_string('2008-04-30')
d2 = ael.date_from_string('2008-05-05')
print Call_Rolling_Interest2(c, d, d2)
'''
