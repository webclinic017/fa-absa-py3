import ael

InsList = ['ZAR/DTOP/JUN09', 'ZAR/SWIX/JUN09/MINCOP/OTC/FWD', 'ZAR/SWIX/JUN09/SENCOP/OTC/FWD', 'ZAR/SWIX/JUN09/TELCRP/OTC/FWD', 'ZAR/FNDI/JUN09/OTC/FWD', 'ZAR/SWIX/JUN09/OTC/FWD', 'ZAR/FNDI/JUN09', 'ZAR/ALSI/JUN09']

length = len(InsList)

def ael_main(ael_dict):

    StartDate = ael_dict["StartDate"]
    Server = ael_dict["Server"]
    
    tel=0
    
    for element in InsList:
        if ael.Instrument[(str)(element)]:
            tel += 1
            jpIndAttribution(element, StartDate, Server, tel, length)
        
ael_variables = [('StartDate', 'StartDate', 'date', None, ael.date_today(), 1),
                 ('Server', 'Server', 'string', None, 'C:\\', 1)]
        

def jpIndAttribution(ins, StartDate, Server, tel, length):

    Global=[]

    ins = ael.Instrument[(str)(ins)]
        
    StartDate = StartDate
    InsExp = ins.exp_day
    
    if  ins.und_insaddr:
    
        und = ins.und_insaddr       
        
        if und.instype == 'Stock':
    
            InputParamList = jpStockDivPV(ins.insid, und.insid, StartDate, InsExp)
        
        elif und.instype == 'EquityIndex':
        
            InputParamList = jpIndexDivPV(ins.insid, und.insid, StartDate, InsExp)
            
        else:
        
            print 'The underlying must be either a Stock or an EquityIndex'
        
        if und.used_price(ael.date(StartDate), (str)(und.curr.insid)) == 0:
        
            SpotPrice = und.mtm_price(ael.date(StartDate), (str)(und.curr.insid))
        
        else:
        
            SpotPrice = und.used_price(ael.date(StartDate), (str)(und.curr.insid))       
        
        Global.append(ins.insid)
        Global.append(und.insid)
        Global.append(SpotPrice)
        
        Global.append(InputParamList[0])        #DivPv 
        Global.append(InputParamList[1])        #RepoDiscountFactorTplusSpot
        Global.append(InputParamList[2])        #RepoDiscountFactorTtoExpPlusSpot
        Global.append(InputParamList[3])        #DiscountRateTplusSpottoExpplusSpot   
        Global.append(InputParamList[4])        #StartSpotDate
        Global.append(InputParamList[5])        #EndSpotDate        
    
            
    else:
        print 'The specified instrument does not have an underlying instrument'
        pass
            
    outfile = Server + 'FutureAttributionOTC' + StartDate.to_string('%y%m%d') + '.csv'    

    report = open(outfile, 'a')
    
    if tel == 1:
    
        Headers = ['InstrName', 'UndInstrName', 'UndSpotPrice', 'DivPv', 'RepoDiscountFactorTplusSpot', 'RepoDiscountFactorTToExpPlusSpot', 'DiscountRateTplusSpotToExpplusSpot', 'StartSpotDate', 'EndSpotDate']
        
        for i in Headers:
        
            report.write((str)(i))
            report.write(',')
        report.write('\n')        
            
        for ls in Global:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
            
    else:        
        
        for ls in Global:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
        
                
    if tel == length:
    
        print 'Success'
        print 'The file has been saved at:' + Server + 'FutureAttributionOTC' + StartDate.to_string('%y%m%d') + '.csv'
    
    report.close()
    
    return 
    
    
def jpIndexDivPV(Derivative, Index, StartDate, EndDate):
    
    IndexList=[]
    
    TotalIndexDivPv = 0
    
    ins = ael.Instrument[Index]
    SpotDays = ins.spot_banking_days_offset
    EndSpot = EndDate.add_banking_day(ael.Instrument[ins.curr.insid], SpotDays)
    StartSpot = StartDate.add_banking_day(ael.Instrument[ins.curr.insid], SpotDays)
    link = ins.combination_links()
    
    for lnk in link.members():
    
        constituent = lnk.member_insaddr
        
        strm = ael.DividendStream.select('insaddr = "%d"' %(lnk.member_insaddr.insaddr))
        
        for member in strm:
        
            for est in member.estimates():
            
                if est.ex_div_day.add_banking_day(ael.Instrument[ins.curr.insid], -1) >= StartDate:
                
                    if est.ex_div_day.add_banking_day(ael.Instrument[ins.curr.insid], -1) < EndDate:
                    
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
        
    RepoDiscountFactorTplusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, StartSpot, None, None, 'Discount', 0, 'ZAR')
    RepoDiscountFactorTtoExpPlusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, EndSpot, None, None, 'Discount', 0, 'ZAR')
    
    Deriv = ael.Instrument[Derivative].used_yield_curve()
    
    DiscountRateTplusSpottoExpplusSpot = Deriv.yc_rate(StartDate, EndSpot, None, None, 'Discount', 0,)

    IndexList.append((float)(TotalIndexDivPv))
    IndexList.append((float)(RepoDiscountFactorTplusSpot))
    IndexList.append((float)(RepoDiscountFactorTtoExpPlusSpot))
    IndexList.append((float)(DiscountRateTplusSpottoExpplusSpot))
    IndexList.append(StartSpot)
    IndexList.append(EndSpot)
    
        
    return IndexList

def jpStockDivPV(Derivative, Stock, StartDate, EndDate):    
    
    StockList=[]
                    
    TotalStockDivPv = 0
    
    ins = ael.Instrument[Stock]
    SpotDays = ins.spot_banking_days_offset
    EndSpot = EndDate.add_banking_day(ael.Instrument[ins.curr.insid], SpotDays)
    StartSpot = StartDate.add_banking_day(ael.Instrument[ins.curr.insid], SpotDays)
    
    strm = ael.DividendStream.select('insaddr = "%d"' %(ins.insaddr))
    
    for member in strm.members():
    
        for est in member.estimates():
        
            if est.ex_div_day.add_banking_day(ael.Instrument[ins.curr.insid], -1) >= StartDate:
                
                    if est.ex_div_day.add_banking_day(ael.Instrument[ins.curr.insid], -1) < EndDate:
                    
                        y = ins.used_repo_curve()
                        
                        DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')  

                        DivEstimate = est.dividend
                        
                        DivFv = (DivEstimate * (DiscountFactor1/DiscountFactor2))
                        DivPv = DivFv * DiscountFactor3
                        
                        TotalStockDivPv += DivPv
                        
        RepoDiscountFactorTplusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, StartSpot, None, None, 'Discount', 0, 'ZAR')
        RepoDiscountFactorTtoExpPlusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, EndSpot, None, None, 'Discount', 0, 'ZAR')
        
        Deriv = ael.Instrument[Derivative].used_yield_curve()
        
        DiscountRateTplusSpottoExpplusSpot = Deriv.yc_rate(StartSpot, EndSpot, None, None, 'Discount', 0,)
    
        StockList.append((float)(TotalStockDivPv))
        StockList.append((float)(RepoDiscountFactorTplusSpot))
        StockList.append((float)(RepoDiscountFactorTtoExpPlusSpot))
        StockList.append((float)(DiscountRateTplusSpottoExpplusSpot))
        StockList.append(StartSpot)
        StockList.append(EndSpot)
                        
    return StockList

 

    
    
    

