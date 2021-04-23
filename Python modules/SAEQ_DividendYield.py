import ael, math, SAEQTheor


def jpDivYieldMain(temp,Inst,StartDate,EndDate,CompoundType,*rest):

    ins = ael.Instrument[Inst]

    Type = ins.instype
    
    if (str)(Type) == 'EquityIndex':
        DividendPV = jpIndexDivPV(Inst, ael.date(StartDate), ael.date(EndDate))
        
    elif (str)(Type) == 'Stock':
        DividendPV = jpStockDivPV(Inst, ael.date(StartDate), ael.date(EndDate))
        
    else:
        print 'The instrument must be a Stock or an EquityIndex'
    
    if ins.quote_type == 'Per 100 Units':
    
        factor = 100
        
    elif ins.quote_type == 'Per Unit':
    
        factor = 1
    
    SpotDays = ins.spot_banking_days_offset
    StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    EndSpot = EndDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)    
    
    TimeToCarry = ((StartSpot.days_between(EndSpot))/365.00)
    
    SpotPrice = ins.used_price(ael.date_today(), ins.curr.insid) / factor
    
    if SpotPrice == 0:
    
        SpotPrice = SAEQTheor.Prices(1, ins.insid)
 
    if SpotPrice != 0 or TimeToCarry != 0 or DividendPV !=0:
    
        Diff = SpotPrice - DividendPV
        
        DivYield = (math.log(SpotPrice) - math.log(Diff)) * (1/TimeToCarry)
        
        if CompoundType == 'NACA':
        
            print 'Instrument', ins.insid
            print 'SpotPrice', SpotPrice
            print 'DividendPV', DividendPV
            print 'TimeToCarry', TimeToCarry
        
            CompoundYield = (((SpotPrice/Diff)**(1/TimeToCarry)) - 1) * 100
            
        elif CompoundType == 'NACC':
        
            CompoundYield = DivYield * 100
        
        DivYield *= 100
        
        #print 'The dividend yield (NACC) of the instrument: %s is %f'%(Inst,DivYield) + '% for the given time period' 
        
    else:   
     
        print 'The dividend yield of the instrument: %s is 0 for the given time period' %Inst
        
    return (float)(CompoundYield)
    

def jpIndexDivPV(Index, StartDate, EndDate):

    TotalIndexDivPv = 0
    
    ins = ael.Instrument[Index]
    SpotDays = ins.spot_banking_days_offset
    EndSpot = EndDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    link = ins.combination_links()
    
    for lnk in link.members():
    
        constituent = lnk.member_insaddr
        
        strm = ael.DividendStream.select('insaddr = "%d"' %(lnk.member_insaddr.insaddr))
        
        for member in strm:
        
            for est in member.estimates():
            
                if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) >= StartDate:
                
                    if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) < EndDate:
                    
                        y = ins.used_repo_curve()
                        
                        DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')  

                        wght = lnk.weight
                        factor = ins.index_factor
                        
                        IndexPoints = (wght/factor)*est.dividend
                        
                        DivFv = (IndexPoints * (DiscountFactor1/DiscountFactor2))
                        DivPv = DivFv * DiscountFactor3
                        
                        TotalIndexDivPv += DivPv
                        
    return (float)(TotalIndexDivPv)

def jpStockDivPV(Stock, StartDate, EndDate):    
                        
    TotalStockDivPv = 0
    
    ins = ael.Instrument[Stock]
    SpotDays = ins.spot_banking_days_offset
    EndSpot = EndDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    
    strm = ael.DividendStream.select('insaddr = "%d"' %(ins.insaddr))
    
    for member in strm.members():
    
        for est in member.estimates():
        
            if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) >= StartDate:
                
                    if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) < EndDate:
                    
                        y = ins.used_repo_curve()
                        
                        DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')  

                        DivEstimate = est.dividend
                        
                        DivFv = (DivEstimate * (DiscountFactor1/DiscountFactor2))
                        DivPv = DivFv * DiscountFactor3
                        
                        TotalStockDivPv += DivPv
                        
    return (float)(TotalStockDivPv)
        

        
