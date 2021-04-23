import ael

port = ael.Portfolio['VOE']
today = ael.date_today()
ins_list = []
for t in port.trades():
    if t.insaddr.instype ==  'Option' and t.insaddr.exp_day < today:
        if t.premium == 0 and t.insaddr.und_insaddr.instype == 'Curr':
            if t.insaddr.curr != t.insaddr.und_insaddr:
                if t.insaddr not in ins_list:
                    ins_list.append(t.insaddr)
                
for i in ins_list:
    
    ic = i.clone()
    ic.curr = ic.und_insaddr
    try:
        ic.commit()
        print(ic.und_insaddr.insid, ic.curr.insid)
    except:
        print('Currency not changed for ', ic.insid)
