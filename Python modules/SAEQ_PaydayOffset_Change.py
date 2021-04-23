import ael

def Filter():
    Filter=[]
    for f in ael.TradeFilter:
        Filter.append(f.fltid)
    Filter.sort()
    return Filter

ael_variables = [('Filter', 'Filter', 'string', Filter(), '', 1),
                 ('NumberDays', 'NumberDays', 'int', None, 1, 1),  
                 ('Server', 'Server', 'string', None, 'C:\\', 1)]
                 
def ael_main(ael_dict):
    
    Filter = ael_dict["Filter"]
    NumberDays = ael_dict["NumberDays"]
    Server = ael_dict["Server"]
    
    
    JdpValueAcqDayChange(Filter, NumberDays, Server)

def JdpValueAcqDayChange(sTf, NumberDays, sServer):
    
    GlobalUpdated=[]
    GlobalFailed=[]
    
    tf  = ael.TradeFilter[sTf]     
    
    for trade in tf.trades():
    
        trdDate = ael.date_from_time(trade.time)        
            
        ins = trade.insaddr    
        new = trade.clone()
        
        new.acquire_day = ael.date_from_time(trade.time).add_banking_day(ael.Instrument[ins.curr.insid], NumberDays)
        new.value_day = ael.date_from_time(trade.time).add_banking_day(ael.Instrument[ins.curr.insid], NumberDays)
        
        try:
            Updated = []
            new.commit()            
            Updated.append(new.trdnbr)
            Updated.append(new.prfnbr.prfid)
            GlobalUpdated.append(Updated)
                            
        except:
            Failed = []
            Failed.append(trade.trdnbr)
            Failed.append(trade.prfnbr.prfid)
            GlobalFailed.append(Failed)
    
    outfile1 = sServer + 'TradesUpdated' + ael.date_today().to_string('%Y%m%d') + '.csv'
    report1 = open(outfile1, 'w')
    
    for update in GlobalUpdated:
    
        for u in update:
        
            report1.write((str)(u))
            report1.write(',')
        report1.write('\n')
    
    report1.close()
    
    outfile2 = sServer + 'TradesFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    report2 = open(outfile2, 'w')
    
    for fail in GlobalFailed:
        
        for f in fail:
            report2.write((str)(f))
            report2.write(',')
        report2.write('\n')
    
    report2.close()
    
    print 'The file with the Updated stock trades has been saved at' + sServer + 'TradesUpdated' + ael.date_today().to_string('%Y%m%d') + '.csv'
    print 'The file with the Failed stock trades has been saved at' + sServer + 'TradesFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    
    return 'Success'
