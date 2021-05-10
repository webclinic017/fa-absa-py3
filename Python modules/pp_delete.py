import ael
t = ael.Trade[822300]
i = t.insaddr
legs = i.legs()

if legs[0].nominal_at_start == 1 and legs[1].nominal_at_start == 1 and \
   legs[0].nominal_at_end == 0 and legs[1].nominal_at_end == 0: 
    
    for l in legs:
            
        lc = l.clone()
        lc.nominal_at_end = lc.nominal_at_start
        lc.nominal_at_start = l.nominal_at_end
        lc.start_day = ael.date_from_time(t.time)
        lc.commit()
        
    tc = t.clone()
    tc.value_day= ael.date_from_time(t.time)
    tc.acquire_day= ael.date_from_time(t.time)
    tc.commit()
