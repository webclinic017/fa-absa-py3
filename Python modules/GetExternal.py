import ael

def ExternalTrades(Trd):

        Trades = []
        ExpiryDate = Trd.insaddr.exp_day
        TradeDate = Trd.acquire_day
        StartDate = Trd.insaddr.legs()[1].start_day
        Nominal = Trd.nominal_amount()
        Rate = Trd.insaddr.legs()[1].fixed_rate 
        print "['Instrument', 'TradeNumber' , 'Nominal', 'Expiry Date' ,'TradeDate']"  
        for i in  ael.Instrument.select('instype=Swap'):
            for l in i.legs():  
                for t in i.trades():
                    if abs(l.fixed_rate - Rate)/100 <= 0.01 and t.nominal_amount() == Nominal and TradeDate > t.acquire_day and  abs(l.start_day.days_between(StartDate)) <= 31 and l.type == 'Fixed' and i.exp_day != None and( abs(i.exp_day.days_between(ExpiryDate)) <= 31 or ( ael.date_today().days_between(i.exp_day) > (6 * 365) and abs(i.exp_day.days_between(ExpiryDate)) <=  182 ))and  t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                        Trades.append([i.insid, t.trdnbr, t.nominal_amount(), i.exp_day, t.acquire_day]) 
        for i in  ael.Instrument.select('instype=FRA'):
            for l in i.legs():  
                for t in i.trades():
                    if abs(l.fixed_rate - Rate)/100 <= 0.01 and t.nominal_amount() == Nominal and TradeDate > t.acquire_day and  abs(l.start_day.days_between(StartDate)) <= 31 and l.type == 'Fixed' and i.exp_day != None and( abs(i.exp_day.days_between(ExpiryDate)) <= 31 or ( ael.date_today().days_between(i.exp_day) > (6 * 365) and abs(i.exp_day.days_between(ExpiryDate)) <=  182 ))and  t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                        Trades.append([i.insid, t.trdnbr, t.nominal_amount(), i.exp_day, t.acquire_day]) 

        return Trades
                    
            

ael_variables = [('trdnbr', 'TradeNumber', 'int', None, 0)]
                
                
                

def ael_main(dict):         
       
   for b in ExternalTrades(ael.Trade[dict.get('trdnbr')]):
        print b
