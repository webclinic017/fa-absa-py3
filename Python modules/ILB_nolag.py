
import ael

def cpi_int(ins, day):
    date=day
    d=date.day_of_month()
    fdm=date.first_day_of_month()
    ldm=date.days_in_month()
    
    d1=fdm.add_months(-4)
    d2=fdm.add_months(-3)
    
    p1 = ins.used_price(d1)
    p2 = ins.used_price(d2)
    
    result = p1 + (p2-p1)*(d-1)/ldm
    
    return result
    
def cpi_int_string(ins,day,*rest):
    # date=ael.date_from_string(day)
    date=day
    d=date.day_of_month()
    fdm=date.first_day_of_month()
    ldm=date.days_in_month()
    
    d1=fdm.add_months(-4)
    d2=fdm.add_months(-3)
    
    p1 = ins.used_price(d1)
    p2 = ins.used_price(d2)
    
    result = p1 + (p2-p1)*(d-1) * 1.0/ldm * 1.0
    
    return result
       
    
