import ael

def  PostCash(Portfolio, Currency, Amount):
    if Amount != 0:
        party = ael.Party['FMAINTENANCE'].ptynbr
        DateEnd = ael.date('31/12/2006')
        
        NewCash = ael.Trade.new(ael.Instrument['CashAggregate'])
        NewCash.prfnbr = ael.Portfolio[Portfolio].prfnbr                   
        NewCash.counterparty_ptynbr= party
        NewCash.value_day = DateEnd
        NewCash.acquire_day = DateEnd
        NewCash.time = DateEnd.to_time()
        payment=ael.Payment.new(NewCash)
        payment.payday= DateEnd
        payment.ptynbr= party
        payment.type='Cash'
        payment.amount= Amount
        payment.curr=Currency
#        NewCash.commit()
        print 'Posted --->', NewCash.trdnbr, Portfolio, Currency, Amount
    return
    
def displayTF():
    filterlst = []
    for f in ael.TradeFilter.select():
        filterlst.append(f.fltid)
    filterlst.sort()
    return filterlst


ael_variables = [('flt', 'Filter', 'string', displayTF(), None, 0, 0)]
    
def ael_main(parameter):
    
    AggCash = []
    for trd in ael.TradeFilter[parameter.get('flt')].trades():
        for c in trd.insaddr.cash_flows():
            print 'Projected- >', trd.trdnbr, c.projected_cf(), c.nominal_amount(), c.cash_balance() 
            AggCash.append([ trd.prfnbr.prfid, c.legnbr.curr.insid, c.cash_balance()])
        for c in trd.payments():
            AggCash.append([ trd.prfnbr.prfid, c.curr.insid, c.amount])
    AggCash.sort()
      
    
    OldPort = AggCash[0][0]
    OldCurr = AggCash[0][1]
    SumAgg = 0
 

    for a in AggCash:
       
        NewPort = a[0]
        NewCurr = a[1]
        
        if OldCurr != NewCurr or OldPort != NewPort :
             PostCash(OldPort, OldCurr, SumAgg)
             SumAgg = 0
             
        SumAgg = SumAgg + a[2]   
        print a  
        OldPort = NewPort 
        OldCurr = NewCurr
    PostCash(OldPort, OldCurr, SumAgg) 

