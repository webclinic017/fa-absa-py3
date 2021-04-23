import ael

try:
     fd = open('/services/frontnt/CounterpartiesToDelete.csv')
except:
     print 'Input file could not be opened'

try:
    fo = open('/services/frontnt/Counterparty_error_new.csv', 'w')
except:
    print 'Output file could not be opened'

line = fd.readline()
list = []
count = 0
while line:
    list = line.split(',')
    
    try:
        p = ael.Party[(int)(list[0])]
        pt = p.clone()
        ErrorLogDesc = (str)(p.ptynbr)+','+ p.ptyid + ',' 

        if (not pt.correspondent_bank):
            print pt.ptyid, ' ', pt.type, ' ', pt.ptynbr
            cont = pt.contacts() 

            for cp in cont:
                c = cp.clone()
                rule = cp.rules()
                for b in rule:
                    dr = b.clone()
                    print 'delete rules'
                    dr.delete()
                    print 'rules deleted'
                print 'delete contacts'
                c.delete()
                print 'contacts deleted'

            for a in pt.accounts():
                print 'delete accounts'
                a.delete()
                print 'accounts deleted'

            try:
                p.delete()
                print 'Counterparty sucessfully deleted'
                fo.write(ErrorLogDesc + 'COUNTERPARTY DELETED' + '\n')
            except:
                ael.log(p.ptyid)
                fo.write(ErrorLogDesc + 'COUNTERPARTY NOT DELETED - Check log' + '\n')
        else:
            print 'Counterparty is a Correspondent Bank'
            fo.write(ErrorLogDesc + 'COUNTERPARTY NOT DELETED - Correspondent Bank' + '\n')
    except:
        print 'Counterparty not found'
        fo.write(list[0] + ',' + 'Counterparty does not exist' + '\n')
        
    line = fd.readline()
    count = count + 1
    print count
fd.close()
fo.close()
