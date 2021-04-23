import ael
trades = ael.Portfolio['291559 warrants'].trades()
for trdn in trades:
    print trdn
    tr = ael.Trade[trdn.trdnbr]
    trc = tr.clone()
    try:
    	trc.premium = trc.premium_from_quote(ael.date_today(), trc.price)
    	trc.commit()
    except:
    	print 'Could not commit: ', trc.trdnbr 
print 'done'
