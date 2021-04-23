import acm

brokerTrades = [51404667,
51690292,
51849240,
51856636,
51860484,
51866058,
51881169,
51894137,
51897783,
51898335,
51908645,
51908674,
51908708,
51908799,
51908834,
51908864,
51908930,
51908961,
51909034,
51916309,
51942938,
51990308,
51999901]

for brokerTrade in brokerTrades:
    fTrade = acm.FTrade[brokerTrade]
    for payment in fTrade.Payments():
        print payment.Type()
        if fTrade.Status() not in ('Void'):
            if payment.Type() == 'Broker Fee':
                print 'Adjust this trade broker pay day', fTrade.Oid()
                payment.PayDay('2015-08-11')
                payment.Commit()
                print 'Done updating this trade', fTrade.Oid()    
