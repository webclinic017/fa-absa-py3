import acm

trades= [100094311, 100094310, 100094308, 100094309, 100000200, 100000199 ]

for t in trades:
    trade = acm.FTrade[t]
    trade.GroupTrdnbr = None
    trade.Commit()
    
    trade.Status = "Void"
    trade.Commit()
    
