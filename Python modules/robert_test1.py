import acm

trade = acm.FTrade[40289832]
trade.AggregateTrade(21465731)
trade.Status('BO Confirmed')
trade.ArchiveStatus(1)
trade.Commit()

 
trade = acm.FTrade[40289901]
trade.AggregateTrade(21465708)
trade.Status('BO Confirmed')
trade.ArchiveStatus(1)
trade.Commit()
