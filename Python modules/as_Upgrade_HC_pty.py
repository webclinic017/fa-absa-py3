import ael

p_list = ael.Party.select()
for p in p_list:
    if p.parent_ptynbr:
        if p.parent_ptynbr.ptyid == p.ptyid:
            p_clone = p.clone()
            p_clone.parent_ptynbr = None
            try:
                p_clone.commit()
                print(p.ptyid + ' Success')
            except:
                print(p.ptyid + ' Error')

