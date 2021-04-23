import ael

#Instruments = ael.Instrument.select('instype = "Cap"')

def CheckTrades(temp, trdfilter, user_email, *rest):
    TradeFilter = ael.TradeFilter[trdfilter]
    Trades = TradeFilter.trades()
#    print len(Trades)
    Today = ael.date_today()

    #Create a list of trade numbers of trades expiring today
    TradeNumbers = []

    if len(Trades) > 0:
        MyOutput = '' 
        for t in Trades:
            
            MyOutput = MyOutput + 'Instrument ' + t.insaddr.insid + ' with FRONT trade number ' + str(t.trdnbr) + ' (' + str(t.optional_key) + ')' + ' expires ' + str(Today) + '\n\n'
   
        MySubject = "Instrument expiries for %s"% (Today)
#        print MySubject, MyOutput
        try:
            ael.sendmail(user_email, MySubject, MyOutput)
            return 'Mail sent successfully'
        except:
            return 'Error sending mail'
            
    else:
        return 'There are no trades expiring today'
    



#Specification of trade filters applicable to particular email address 
#print 'Starting Trade Check'
#CheckTrades(1, 'NLD_IROptions_Expiries', 'sjanevds@absa.co.za', 'francoiskr@absa.co.za', 'rishik@absa.co.za', 'justinn@absa.co.za', 'DevaS@absa.co.za')
#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'sjanevds@absa.co.za', 'francoiskr@absa.co.za', 'rishik@absa.co.za', 'justinn@absa.co.za', 'karaboma@absa.co.za')

#CheckTrades(1, 'NLD_IROptions_Expiries', 'sjanevds@absa.co.za')
#CheckTrades(1, 'NLD_IROptions_Expiries', 'francoiskr@absa.co.za')
#CheckTrades(1, 'NLD_IROptions_Expiries', 'rishik@absa.co.za')
#CheckTrades(1, 'NLD_IROptions_Expiries', 'justinn@absa.co.za')
#CheckTrades(1, 'NLD_IROptions_Expiries', 'DevaS@absa.co.za')

#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'sjanevds@absa.co.za')
#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'francoiskr@absa.co.za')
#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'rishik@absa.co.za')
#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'justinn@absa.co.za')
#CheckTrades(1, 'NLD_Curr&Gold_Expiries', 'karaboma@absa.co.za')

#print 'Trade Check complete'

