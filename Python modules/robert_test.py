import acm

trade = acm.FTrade[40222591]
trade.AggregateTrade(8206259)
trade.ArchiveStatus(1)
trade.Commit()

trade = acm.FTrade[40222651]
trade.AggregateTrade(8206285)
trade.ArchiveStatus(1)
trade.Commit()


trade = acm.FTrade[40222355]
trade.AggregateTrade(900091)
trade.ArchiveStatus(1)
trade.Commit()
