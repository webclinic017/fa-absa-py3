import acm, datetime

ael_variables =[('insaddr', 'insaddr_insaddr', 'int')]

def ael_main(dict):
    ins = acm.FInstrument[dict['insaddr']]
    for p in ins.Prices():
        print 'Day ', p.Day()
        print 'Instrument ', ins.Name()
        print 'Currency ', p.Currency().Name()
        print 'Market ', p.Market().Name()
        print 'Bid = ', p.Bid() 
        print 'Ask = ', p.Ask()
        print 'Last = ', p.Last()
        print 'Settle = ', p.Settle() 
        print 'Update Time = ', datetime.datetime.fromtimestamp(p.UpdateTime())
        print '=============='
 
    
    
