import ael
today = ael.date_today()
optend = ['1D', '1W', '1M', '2M', '3M', '6M', '9M', '1Y', '2Y', '3Y', '4Y', '5Y', '6Y']
i = ael.Instrument['CAD-ZAR/0.9DEL/CALL/0W']
ic = i.clone()

for k in optend:
    newins = ael.Instrument.new('Option')
    #startdate = today
    expday = k
    print expday 
    #startdate, ': ', enddate
    
    newins.exp_period = k
    newins.exercise_type = i.exercise_type
    newins.call_option = i.call_option
    newins.strike_type = i.strike_type
    newins.strike_price = i.strike_price
    newins.und_insaddr = i.und_insaddr
    newins.curr = i.curr
    newins.strike_curr = i.strike_curr
    newins.product_chlnbr = i.product_chlnbr
    newins.settlement = i.settlement
    newins.pay_day_offset = i.pay_day_offset
    newins.insid = 'CAD-ZAR/0.9DEL/CALL/' + expday 
    ninsid = newins.insid
    newins.generic = 1
    newins.quote_type = i.quote_type
    newins.paytype = i.paytype
    newins.otc = i.otc
    try:
        newins.commit()
    except:
        print 'Not created'
    print ninsid
