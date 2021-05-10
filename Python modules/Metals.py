import ael
def Metals_Total(v,date,cur,openingbal,start,filter,*rest):
    trad = ael.TradeFilter[filter].trades()
    total = openingbal
    for t in trad:
        if t.insaddr.instype == 'Curr':
            if t.value_day <= date and t.value_day >= start and t.curr.insid == cur:
                total = total + t.premium 
                flag = 1            

        else:
            if t.value_day >= start and t.curr.insid == cur:
                total = total + t.premium
                flag = 1
            ls = t.insaddr.legs()
            for l in ls:
                if l.curr.insid == cur:
                    cfs = l.cash_flows()
                    for c in cfs:
                        if c.pay_day <= date and c.pay_day >= start:
                            total = total + (c.projected_cf() * t.quantity)
    return total	    		
#Metals_Total(1,ael.date('2004-04-05'),'USD',20000,ael.date('2004-04-01'),'Metals Root Filter')
