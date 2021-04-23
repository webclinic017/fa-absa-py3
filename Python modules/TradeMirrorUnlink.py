import acm

numbers = [53790002]
for number in numbers:
    trade = acm.FTrade[number]
    trade.MirrorTrade(None)
    trade.Commit()
    print('Mirror broken: %s' % number)
