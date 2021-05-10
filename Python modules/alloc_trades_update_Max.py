#Sales Credit Clear
import acm
import at_addInfo

'''
trade = acm.FTrade[104090580]
a = trade.

print a

'''
trades = acm.FTradeSelection['SAFI_SalesCreditCorporate'].Trades()

for trade in trades:
    if trade.ExecutionTime() >= '2019-01-01':
        #print trade.AdditionalInfo()

        
        trade.AdditionalInfo().Sales_Credit2('')
        trade.AdditionalInfo().Sales_Person2(None)
        
        trade.AdditionalInfo().Sales_Credit3('')
        trade.AdditionalInfo().Sales_Person3(None)

        #print trade.AdditionalInfo().Sales_Credit3()
        #print trade.AdditionalInfo().Sales_Person3()

        trade.Touch()
        trade.Commit()
        #print trade.AdditionalInfo()'''

'''
at_addInfo.save_or_delete(trd, 'Sales_Credit3','')
at_addInfo.save_or_delete(trd, 'Sales_Person3','')
'''
