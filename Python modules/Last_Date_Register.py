import ael

def bcd_ldr(ins,day,*rest):

    bcd=ael.date_from_string(day)
    
    bcd_split=bcd.to_ymd()
    today_split=ael.date_today().to_ymd()
        
    cy, cm, cd=today_split
    y, m, d=bcd_split
    
    new_bcd=ael.date_from_ymd(cy, m, d)
    
    
    
    ldr=new_bcd.add_days(-1)
    
    
    return ldr

def bcd(ins,day,*rest):

    bcd=ael.date_from_string(day)
    
    bcd_split=bcd.to_ymd()
    today_split=ael.date_today().to_ymd()
        
    cy, cm, cd=today_split
    y, m, d=bcd_split
    
    new_bcd=ael.date_from_ymd(cy, m, d)
    
    
    
    return new_bcd

def length(party,hostid,*rest):

    long=len(hostid)
    return long
    
        
    
    
