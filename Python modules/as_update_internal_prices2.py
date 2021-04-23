import ael, datetime

p_list = []
for p in ael.Price.select('day = "2009-06-26"'):
    if p.ptynbr.ptyid == 'internal':
        #if p.insaddr.insid == 'ZAR/SHP':
        tup = (p.prinbr, p.day)
        p_list.append(tup)
        

for l in p_list:
    x = l[0]
    new_p = ael.Price[x].new()
    new_p.day = l[1].add_days(2)
    try:
        new_p.commit()
    except:
        print('cannot commit price for ', new_p.insaddr.insid)





