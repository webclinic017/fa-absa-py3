import ael, acm

def Main(output):

    outpath = output[0][0] 
    dt = ael.date_today()
    dt_string = str(dt)
    
    print 'Starting'
    
    f = open(outpath + 'DailyResetFile.xls', 'w')
    f2 = open(outpath + 'DailyResetFile_Failed.xls', 'w')
    f3 = open(outpath + 'DailyResetFile_IncorrectFixings.xls', 'w')
    
    resetData = acm.FReset.Select("day = " + dt_string)
    
    s = GenStrFromList('\t', 'Daily Reset Check', dt)
    f.write(s)
    f2.write(s)
    f3.write(s)
    s = GenStrFromList('\t', 'Trade', 'Portfolio', 'Status', 'Instrument Type', 'Reset Number', 'Reset Day', 'Reset Type', 'Fixing Value', 'Read Time', 'System Price', 'Floating Rate Reference', 'Leg Currency', 'Nominal Scaling Type', 'Scaling Ref', 'Alternate Leg Currency')
    f.write(s)
    f3.write(s)
    s = GenStrFromList('\t', 'Trade', 'Status', 'Instrument Type', 'Reset Type')
    f2.write(s)

    
    for r_acm in resetData:
        r_ael = ael.Reset[r_acm.Oid()]
        ins_ael =  r_ael.cfwnbr.legnbr.insaddr.insid
        leg_ael = r_ael.cfwnbr.legnbr
        ins_acm = acm.FInstrument[ins_ael]
        for t_acm in ins_acm.Trades():
            try:
                if r_acm.ResetType() not in ('Nominal Scaling', 'Return'):                    
                    s = GenStrFromList('\t', t_acm.Name(), t_acm.Portfolio().Name(), t_acm.Status(), ins_acm.InsType(), r_acm.Oid(), r_acm.Day(), r_acm.ResetType(), r_acm.FixingValue(), ael.date_from_time(r_ael.read_time), leg_ael.float_rate.used_price(dt), leg_ael.float_rate.insid, leg_ael.curr.insid, 'N/A', 'N/A', 'N/A')
                    f.write(s)
                    if (round(leg_ael.float_rate.used_price(dt), 6) <> round(r_acm.FixingValue(), 6)) or (r_acm.FixingValue() == 0):
                        s = GenStrFromList('\t', t_acm.Name(), t_acm.Portfolio().Name(), t_acm.Status(), ins_acm.InsType(), r_acm.Oid(), r_acm.Day(), r_acm.ResetType(), r_acm.FixingValue(), ael.date_from_time(r_ael.read_time), leg_ael.float_rate.used_price(dt), leg_ael.float_rate.insid, leg_ael.curr.insid, 'N/A', 'N/A', 'N/A')
                        f3.write(s)                 
                                                         
                else:                
                    legs_acm = ins_acm.Legs()
                    for l_acm in legs_acm:
                        l_ael = ael.Leg[l_acm.Oid()]
                        if l_ael.curr.insid <> leg_ael.curr.insid:
                            opp_curr = l_ael.curr                                
                    s = GenStrFromList('\t', t_acm.Name(), t_acm.Portfolio().Name(), t_acm.Status(), ins_acm.InsType(), r_acm.Oid(), r_acm.Day(), r_acm.ResetType(), r_acm.FixingValue(), ael.date_from_time(r_ael.read_time), 'N/A', leg_ael.float_rate.insid, leg_ael.curr.insid, leg_ael.nominal_scaling, leg_ael.index_ref.insid, opp_curr.insid)
                    f.write(s)
                    if leg_ael.nominal_scaling == 'FX':
                        if (leg_ael.index_ref.insid <>  opp_curr.insid) or (r_acm.FixingValue() == 0):
                            s = GenStrFromList('\t', t_acm.Name(), t_acm.Portfolio().Name(), t_acm.Status(), ins_acm.InsType(), r_acm.Oid(), r_acm.Day(), r_acm.ResetType(), r_acm.FixingValue(), ael.date_from_time(r_ael.read_time), 'N/A', leg_ael.float_rate.insid, leg_ael.curr.insid, leg_ael.nominal_scaling, leg_ael.index_ref.insid, opp_curr.insid)
                            f3.write(s)          
                   
            except:
                s = GenStrFromList('\t', t_acm.Name(), t_acm.Status(), ins_acm.InsType(), r_acm.ResetType())
                f2.write(s)
            
    
    
    f.close()
    f2.close()
    f3.close()
    print 'Finished'
     

def GenStrFromList(delim, *list):
    s = ''
    k = 0
    cnt = len(list)
    for o in list:
        k += 1
        if k < cnt:
            s = s + str(o) + delim
        else:
            s = s + str(o) + '\n'
    return s
    

