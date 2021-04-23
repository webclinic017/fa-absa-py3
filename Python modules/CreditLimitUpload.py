import ael, string, FCreditLimit
try:
    f = open('C:\\Credit.csv')
    print '.......Credit Limit Upload Process Begin....... \n'
except:
    print 'File not opened'
line = (f.readline()).strip()
failed_list = []
p1 = ael.Party['Funding Desk']
while line != '':
    l = []
    l = string.split(line, ',')
    party = ael.Party[l[0]]
    if party != None:
        flag =0
        if party.group_limit:
            if party.parent_ptynbr: # not a parent
                cls = ael.CreditLimit.select('ptynbr=%d' %party.parent_ptynbr.ptynbr)
                flag = 1
            else:
                cls = ael.CreditLimit.select('ptynbr=%d' %party.ptynbr)
                flag = 2
        else:
            cls = ael.CreditLimit.select('ptynbr=%d' % party.ptynbr)
        if cls:
            if len(cls) == 1:
                cl = cls[0] 
                lim = getattr(cl, 'limit[0]')
            else:
                for x in cls:
                    if x.depnbr:
                        if x.depnbr.ptynbr == p1.ptynbr:
                            lim = getattr(x, 'limit[0]')
                            cl = x
                            break

            util =  FCreditLimit.credit_tot_cp(party)
            if util <= float(l[1]):
                cl_clone = cl.clone()
                setattr(cl_clone, 'limit[0]', float(l[1]))
                try:
                    cl_clone.commit()
                    print 'SUCCESS:', l[0], l[1], 'limit updated'
                except:
                    print 'FAILURE: Limit for counterparty', l[0], 'not uploaded.'
            else:
                print 'FAILURE: Limit for counterparty', l[0], 'not uploaded. New limit would violate current credit utilization'
        else:
            cl = ael.CreditLimit.new()
            cl.ptynbr = party.ptynbr
            cl.depnbr = p1.ptynbr
            setattr(cl, 'limit[0]', float(l[1]))
            try:
                cl.commit()
                print 'SUCCESS:', l[0], l[1], 'limit added'
            except:
                print 'FAILURE: Limit for counterparty not loaded', l[0]
            
    else:
        print l[0], 'FAILURE: Party not found'
 
    
    line = (f.readline()).strip()

     
f.close()
print '\n.......Credit Limit Upload Process Completed....... \n'

