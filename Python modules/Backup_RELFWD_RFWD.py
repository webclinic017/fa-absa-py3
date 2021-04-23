import ael, string
 
ins = ael.Instrument.select() 
for i in ins:
   if i.instype == 'Cap' and i.generic and  string.rfind(i.insid, 'RELFWD') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price() 
            print i.insid, i.used_und_frw_price() 
            oldl.commit()
   elif i.instype == 'Cap' and i.generic and  string.rfind(i.insid, 'RFWD+1') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price() + 1 
            print i.insid, i.used_und_frw_price() + 1 
            oldl.commit() 
   elif i.instype == 'Cap' and i.generic and  string.rfind(i.insid, 'RFWD-1') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price() - 1 
            print i.insid, i.used_und_frw_price() - 1 
            oldl.commit()
   elif i.instype == 'Floor' and i.generic and  string.rfind(i.insid, 'RELFWD') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price()  
            print i.insid, i.used_und_frw_price()  
            oldl.commit() 
   elif i.instype == 'Floor' and i.generic and  string.rfind(i.insid, 'RFWD+1') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price() + 1 
            print i.insid, i.used_und_frw_price() + 1 
            oldl.commit()
   elif i.instype == 'Floor' and i.generic and  string.rfind(i.insid, 'RFWD-1') > -1: 
        for j in i.legs(): 
            oldl = j.clone() 
            oldl.strike = i.used_und_frw_price() - 1 
            print i.insid, i.used_und_frw_price() - 1 
            oldl.commit()
