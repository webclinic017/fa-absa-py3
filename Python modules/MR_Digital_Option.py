#------------------------------------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module replicates a digital option using two cap/floor instruments.
#  Department and Desk : Market Risk - Quantitative Analysis
#  Requester           : Sifiso Musundwa
#  CR Number           : 392413 
#------------------------------------------------------------------------------------------------------------------------------------------

import ael, csv
      
def write_file(name, data):
    
    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()
    
def Create_new_caps_floor(old_trd, path):
        
    List     = []
        
    Header = 'trdnbr', 'PV', 'Hedge Ref', 'Cap/Floor trdnbr', 'Cap/Floor insid', 'Type', 'Cap/Floor PV'
    List.append(Header)
    
    for trd in old_trd:
        
        t = ael.Trade[trd.trdnbr]
        
        if t.insaddr.instype in ('Cap', 'Floor'):
            if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                for l in t.insaddr.legs():
                    if l.digital == 1:
                        count = -1
                        ret = 0 
                        while count <= 0:
                        
                            try:
                                ins = t.insaddr 
                                ins_clone = ins.clone().new()
                                ins_clone.insid = ins_clone.suggest_id()
                                ins_clone.protection = 'W:R,O:R,G:RWD,U:RWD'
                                ins_clone.owner_usrnbr = 1025 
                                ins_clone.commit()
                            except Exception, e:
                                print e
                            
                            try:
                                for l in ins_clone.legs():
                                    if l.digital == 1:
                                        Cap_Strike = l.strike 
                                        Digital_fixed_Rate = l.fixed_rate
                                                    
                                        for i in ael.ValuationParameters:
                                            if i.digital_cap_floor_spread_type == 'Absolute':
                                                Spread_value = i.digital_cap_floor_spread_val
                                                Float_Factor =    (Digital_fixed_Rate/100)/Spread_value 
                                                
                                    l.digital           = 0
                                    l.fixed_rate        = 0
                                    l.digital_type      = 'None'
                                    l.comparison_type   = 'None'
                                    l.float_rate_factor = Float_Factor
                                    
                                    if ret == 0:
                                        l.strike = ((Cap_Strike/100 + 0.5*Spread_value)* Float_Factor)*100
                                    else:    
                                        l.strike = ((Cap_Strike/100 - 0.5*Spread_value)* Float_Factor)*100
                                                            
                                    l.regenerate() 
                                    l.commit()
                            except Exception, e:
                                print e
                                
                            try:    
                                new_t = ael.Trade[trd.trdnbr].new()
                                new_t.insaddr = ins_clone.insaddr
                                
                                if t.insaddr.instype == 'Cap':
                                    if ret == 0:
                                        new_t.quantity = new_t.quantity*-1
                                        Type = 'Short Cap'
                                    else:
                                        Type = 'Long Cap'     
                                    
                                elif t.insaddr.instype == 'Floor':
                                    if ret == 1:
                                        new_t.quantity = new_t.quantity*-1
                                        Type = 'Short Floor'
                                    else:
                                        Type = 'Long Floor'
                                                                
                            except Exception, e:
                                print e
                            new_t.commit()
                
                            count = count + 1
                            ret = 1
                                                   
                            try:
                                new_Trade = ael.Trade[new_t.trdnbr].new()
                                new_Trade.hedge_trdnbr = t.trdnbr
                                new_Trade.status = 'Simulated'
                                new_Trade.protection = 'W:R,O:R,G:RWD,U:RWD'
                                new_Trade.owner_usrnbr = 1025
                                new_Trade.commit()
                               
                            except Exception, e:
                                print e
                                
                            ael.poll()    
                                       
                            data = t.trdnbr, t.present_value(), new_Trade.hedge_trdnbr, new_Trade.trdnbr, new_Trade.insaddr.insid, Type, new_Trade.present_value()
                            
                            List.append(data)
                                   
                        write_file(path + '.csv', List)           

def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    
    return TrdFilter
    
ael_variables = [('TrdFilter', 'Trade Filter', 'string', TrdFilter(), 'MR_Digital_Option', 1),
                 ('Path', 'Output Directory', 'string', '', 'F:/ European Digital', 1)]   

def ael_main(dict):

    try:
        Outpath = dict['Path']
        tf      =  ael.TradeFilter[dict['TrdFilter']].trades().members()
        Create_new_caps_floor(tf, Outpath)
    except Exception, e:
        print e
