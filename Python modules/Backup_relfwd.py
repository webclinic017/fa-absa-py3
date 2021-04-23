import ael, string 

ins = ael.Instrument.select() 
for i in ins: 
    if i.instype == 'Cap' and i.generic and string.rfind(i.insid, 'RELFWD') > -1: 
    #if i.generic == 1 and i.instype == 'Cap' and string.rfind(i.insid,'RELFWD') > -1:
         for j in i.legs(): 
             oldl = j.clone() 
             oldl.strike = i.used_und_frw_price() 
             print i.insid, i.used_und_frw_price() 
	     print i.instype, i.generic, string.rfind(i.insid, 'RELFWD')
             #oldl.commit()
