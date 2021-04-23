import acm
import csv

with open( 'C:\\Temp\\1\\CA_Stock Input.csv', mode='r') as csv_file:
 readCSV = csv.DictReader(csv_file)

 print 'trade number', "|", 'instrument', "|", 'trade price', "|", 'Portfolio'
 for row in readCSV:   
     trade=acm.FTrade()
     trade.Instrument(row['Instrument'])
     trade.Quantity(row['Quantity'])
     trade.Price(row['Price'])
     trade.Acquirer(row['Acquirer'])
     trade.Portfolio(row['Portfolio'])
     trade.Counterparty("JSE")
     trade.Status('Simulated')
     trade.Currency('ZAR')
     trade.TradeTime('2021-01-04')
     trade.ValueDay('2021-01-07')
     trade.Commit()
     premium=trade.Quantity() *-1*trade.Price()/100
     trade.Premium(premium)
     trade.AcquireDay(trade.ValueDay())
     trade.Commit()
     
     
     print trade.Name(), "|", trade.Instrument().Name(), "|", trade.Price(), "|", trade.Portfolio().Name()
