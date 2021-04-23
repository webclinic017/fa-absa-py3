import ael, string, acm


# times @ position 3 and 4        
e1 = []

# times @ position 2 and 3 
e2 = []

# times @ position 5 and 6 
e5 = []



def change_times(i, pld, data_nbr, new_start, new_end, *rest):
    count = 0
    t1 = 4
    t2 = 5
    '''
    if pld in e1:
        t1 = 3
        t2 = 4
    elif pld in e2:
        t1 = 2
        t2 = 3
    elif pld in e5:
        t1 = 5
        t2 = 6
    else:
        t1 = 4
        t2 = 5
    '''    
    price_split = string.split(pld, ' ')    
    for pl in price_split:
        if count == t1:
            price_split[t1] = new_start
        elif count == t2:
            price_split[t2] = new_end
        count = count + 1    

    if new_start and new_end == '0000':
        new_pld = 'blank'
    else:
        new_pld = string.join(price_split, ' ')

    pld_clone = ael.PriceDefinition[i.defnbr].clone()
    d = 'data[' + str(data_nbr) + ']'
    try:
        setattr(pld_clone, d, new_pld)
        #pld_clone.commit()
        return new_pld
    except:
        print 'Error ', pld_clone.defnbr, pld_clone.insaddr.insid
        return 'Error'
    
    
    

