import ael, string, math
 
def StockDiv(s,BDate,Outfile,*rest):
    Global=[]
    strm = ael.DividendStream.select()
    outfile = Outfile
    BusinessDate = BDate
    d0 = ael.date_today()
    d1 = ael.date_today().add_delta(1, 0, 0)
    end = 20
    divisor = 1
 
    
    for st in strm.members():
        divisor = 1
        length = len(st.name)    
        inst = st.insaddr.insid
 
        instPrice =  st.insaddr.used_price()
        if st.insaddr.quote_type == 'Per 100 Units':
            divisor = 100
        else:
            divisor = 1
 

        st.estimates().members().sort()
        
        if length == 3 or length == 4:
            for est in st.estimates():
                list=[]
                strmname = st.name
                list.append(strmname)
                list.append(inst)
                PayDay = est.pay_day
                list.append(PayDay)
                Div = est.dividend
                list.append(Div)
                
                #eeeee
                SpotDays = st.insaddr.spot_banking_days_offset
                EndSpot = PayDay.add_banking_day(ael.Instrument['ZAR'], SpotDays)
                StartSpot = d0.add_banking_day(ael.Instrument['ZAR'], SpotDays)
                
                y = st.insaddr.used_repo_curve()
                
                DiscountFactor1 = y.yc_rate(d0, PayDay, 'Simple', 'Act/365', 'Discount')
                DiscountFactor2 = y.yc_rate(d0, EndSpot, 'Simple', 'Act/365', 'Discount')
                DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')
                NACC_rate = y.yc_rate(StartSpot, EndSpot, 'Continuous', 'Act/365', 'Spot Rate')
                list.append(NACC_rate)
                DivFV = (Div * (DiscountFactor1/DiscountFactor2))
                DivPV = DivFV * DiscountFactor3
                TTM = StartSpot.years_between(EndSpot, 'Act/365')
                #print dir(TTM)
                list.append(TTM)
                if PayDay < d0:
                    list.append(0)
                
                else:
                    list.append(DivPV)
                
                
                StPrice = instPrice/divisor
                list.append(StPrice)
                list.append(DiscountFactor3)
                if PayDay < d0:
                    bucket = 'expired'
                    
                    list.append(bucket)
                    
                if PayDay == d0:
                    bucket = '0d'
                    list.append(bucket)
                    
                if PayDay > d0 and PayDay <=d1:
                    bucket = '1d'
                    list.append(bucket)
                
                elif PayDay > d1 and PayDay <= d0.add_delta(0, 24, 0):
                    
                    i = 1
                    
                    while i < 25 :
                        
                        if PayDay > ael.date_today().add_delta(0, i-1, 0) and PayDay <= ael.date_today().add_delta(0, i, 0):
                            bucket = str(i) + 'm'
                            list.append(bucket)
                            i = 25
                        
                        else:
                            i = i + 1
                
                    
                elif PayDay > d0.add_delta(0, 24, 0) and PayDay < d0.add_delta(0, 0, end):
                
                    i = 3
                    
                    while i < (end+1):
                    
                        if PayDay > ael.date_today().add_delta(0, 0, i-1) and PayDay <= ael.date_today().add_delta(0, 0, i): 
                            bucket = str(i) + 'y'
                            list.append(bucket)
                            i = (end+1)
                        
                        else:
                            i = i + 1
                list.append(BusinessDate)
                Global.append(list)
    Global.sort()
    #print Global
    
    #print Global[0][0]
    ii2 = 0
    CurStream = (str)(Global[0][0])
    SumPVDiv = 0
 
    list2 = []
    divylist = []
    
    divy=0
    len2 = len(Global)
    while ii2 < len2:
        #print CurStream, Global[ii2][0]
        if Global[ii2][0] == CurStream:
            SumPVDiv = SumPVDiv + Global[ii2][6]
        else:
            CurStream = Global[ii2][0]
            SumPVDiv = 0 + Global[ii2][6]
                    
        #print Global[ii2][0],Global[ii2][1],Global[ii2][2],Global[ii2][3],Global[ii2][4],Global[ii2][5],Global[ii2][6],Global[ii2][7],Global[ii2][8],Global[ii2][9],SumPVDiv
        if Global[ii2][5] == 0:
            divy = 0
        else:
            if Global[ii2][7] == 0:
                divy = 0
            else:
                if (((Global[ii2][7]-SumPVDiv)*math.exp(Global[ii2][4]*Global[ii2][5]))/Global[ii2][7])>0:
                    divy = round(-1/Global[ii2][5]*( math.log(((Global[ii2][7]-SumPVDiv)*math.exp(Global[ii2][4]*Global[ii2][5]))/Global[ii2][7])-Global[ii2][4]*Global[ii2][5]), 10)
                else:
                    divy = 0
        divylist.append(divy)
        list2.append(SumPVDiv)
        ii2 = ii2 + 1
    
    
    #outfile = '//services/frontnt/dart/ERM/StockDividends_yield.csv'
    #outfile = '//v036syb004001/DART/ERM/StockDividends_yield.csv'
    
    report = open(Outfile, 'w')
    Headers=[]
    #               0        1    2         3          4           5      6      7             8             9          10        11            12
    Headers = ['Stream', 'Stock', 'PayDate', 'Dividend', 'NACC_rate', 'TTM', 'DivPV', 'StockPrice', 'DiscFactor', 'Bucket', 'BusinessDate', 'SumPVDiv', 'divYield']
    currentStream = 'axxxxxzz'
    for i in Headers:
        
        report.write((str)(i))
        report.write(';')
    report.write('\n')
    report.write('\n')
        
    ii3 = 0
    for lsts in Global:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(';')
        report.write((str)(list2[ii3]))
        report.write(';')
        report.write((str)(divylist[ii3]))
        ii3 = ii3 + 1    
        report.write(';')
        report.write('\n')
        
    report.close()
    return 'Success'
    #print 'The file has been saved at: C:\\DeClercqStockDividends.csv'
