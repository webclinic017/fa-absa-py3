import ael, acm

prices = acm.FPrice.Select('market = "SPOT"')

for p in prices:
        try:
            ins = ael.Instrument[p.Instrument().Oid()]
        except Exception, e:
            #if p.Instrument():
            #print p.Instrument().Name()
            #    pass
            #else:
            print '*******', e
            print '--------', p
        #ins = ael.Instrument[p.Instrument().Oid()]
        #print ins.insid  
