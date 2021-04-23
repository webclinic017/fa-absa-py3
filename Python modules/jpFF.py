import ael

file = 'C:\\Frank.csv'

try:
    sheet = open(file)
except:
    print'Problem opening the file'

line = sheet.readline()

while line:
    line = sheet.readline()
    l = line.split(',')
    if (l[0] == '\n' or l[0] == ""): break
    
    list=[]
    
    for i in l:
        reg = i.lstrip()
        reg = reg.rstrip()
        list.append(reg)
    
    trade = ael.Trade[(int)(list[0])]
    
    if trade.prfnbr.prfid not in ['Equity Script Lending', 'CFD', 'SL Term Trades', 'Reserved_Stock', 'SL_Hold List']: 
                
                ins = trade.insaddr    
                new = trade.clone()
                
                new.acquire_day = ael.date_from_time(trade.time).add_banking_day(ael.Instrument[ins.curr.insid], ins.spot_banking_days_offset)
                new.value_day = ael.date_from_time(trade.time).add_banking_day(ael.Instrument[ins.curr.insid], ins.spot_banking_days_offset)
                
                try:
                    Updated = []
                    new.commit()            
                                    
                except:
                    print'Problem', trade.trdnbr
                    
        


