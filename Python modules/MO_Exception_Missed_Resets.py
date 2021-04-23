import acm, ael, time, sys

def Main(output):

    outpath = output[0][0]

    dt_string = str(ael.date_today())
    print 'dt:', dt_string
    
    print 'Opening Files'

    f = open(outpath + 'MissedResetFile.xls', 'w')
    ffail = open(outpath + 'MissedResetFileFailed.xls', 'w')
    
    s = GenStrFromList('\t', 'Instrument', 'InstrumentType', 'LegType', 'CashFlowType', 'Trdnbr', 'LegNbr', 'CashFlowNbr', 'ResetNbr', 'ResetDay', 'CashFlowDay', 'TradeTime', 'ValueDay', 'InstrumentExpiry', 'ResetValue', 'ResetType', 'ReadTime', 'FloatRate', 'TradeStatus', 'MTMFromFeed', 'Portfolio',  'Type')
    sf = GenStrFromList('\t', 'Instrument', 'InstrumentType', 'LegType', 'CashFlowType', 'Trdnbr', 'TradeStatus', 'Portfolio',  'CashFlowNbr')
    f.write(s)
    ffail.write(sf)	
    
    reset_acm1 = acm.FReset.Select("fixingValue = 0.00 and day<" + dt_string)
    RType1 = 'ZERO RESET VALUE'
    reset_acm2 = acm.FReset.Select("fixingValue <> 0.00 and readTime = 01/01/1970")
    RType2 = 'ZERO READ-TIME'    
           
    print 'Phase 1 :  Reset Set 1'
    CheckResets(reset_acm1, RType1, outpath, f, ffail)
    
    print 'Phase 2 :  Reset Set 2' 
    CheckResets(reset_acm2, RType2, outpath, f, ffail)
    
    print 'Finished'
    
    f.close()
    ffail.close()
    
    

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


	
def CheckResets(ResetSet, RType, outpath, f, ffail):

   
    for r in ResetSet:
        cf = acm.FCashFlow[int(r.CashFlow().Oid())]
        l = acm.FLeg[int(cf.Leg().Oid())]
        i = acm.FInstrument[int(l.Instrument().Oid())]
        if l.LegType() not in ('Fixed', 'Call Fixed', 'Call Fixed Adjustable', 'Call Float'):
            for t in i.Trades():
                if t.Status() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated', 'FO Sales', 'Legally Confirmed'):
                    if l.FloatRateReference().Name() <> 'ICI_0%':
                        try:
                            s = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), l.Oid(), cf.Oid(), r.Oid(), r.Day(), cf.PayDate(), t.TradeTime(), t.ValueDay(), i.ExpiryDateOnly(), r.FixingValue(), r.ResetType(), r.ReadTime(), l.FloatRateReference().Name(), t.Status(), i.MtmFromFeed(), t.Portfolio().Name(), RType)   
                            f.write(s)
                        except:
                            sf = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), t.Status(), t.Portfolio().Name(), cf.Oid())
                            ffail.write(sf)          
        else:
            if l.LegType() == 'Fixed':
                for t in i.Trades():
                    if t.Status() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed', 'Terminated', 'FO Sales', 'Legally Confirmed'):                        
                        if l.FloatRateReference() == None: 
                            try:
                                s = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), l.Oid(), cf.Oid(), r.Oid(), r.Day(), cf.PayDate(), t.TradeTime(), t.ValueDay(), i.ExpiryDateOnly(), r.FixingValue(), r.ResetType(), r.ReadTime(), 'Fixed No FloatRef', t.Status(), i.MtmFromFeed(), t.Portfolio().Name(), RType)
                                f.write(s)     
                            except:
                                sf = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), t.Status(), t.Portfolio().Name(), cf.Oid())
                                ffail.write(sf)
                        else:
                            if l.FloatRateReference().Name() <> 'ICI_0%': 
                                try:
                                    s = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), l.Oid(), cf.Oid(), r.Oid(), r.Day(), cf.PayDate(), t.TradeTime(), t.ValueDay(), i.ExpiryDateOnly(), r.FixingValue(), r.ResetType(), r.ReadTime(), 'Fixed No FloatRef', t.Status(), i.MtmFromFeed(), t.Portfolio().Name(), RType)
                                    f.write(s)     
                                except:
                                    sf = GenStrFromList('\t', i.Name(), i.InsType(), l.LegType(), cf.CashFlowType(), t.Name(), t.Status(), t.Portfolio().Name(), cf.Oid())
                                    ffail.write(sf)




