import ael

def change(temp, i, *rest):
    cfs = i.cash_flows()
    for c in cfs:
        print(c.pay_day.to_string())
        if c.pay_day.to_string() == '2007/06/28':
            
            new_c = c.clone()
            new_c.pay_day = c.pay_day.add_days(1)
            print(new_c.pp())
    
    
    
    
#main
t = ael.Trade[1027391].insaddr
print(change(1, t))
