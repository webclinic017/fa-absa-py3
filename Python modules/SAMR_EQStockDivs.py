import ael, string

def StockDiv(s,Outfile,*rest):
    Global=[]
    strm = ael.DividendStream.select()
    
    d0 = ael.date_today()
    d1 = ael.date_today().add_delta(1, 0, 0)
    end = 20
    
    for st in strm.members():
        
        length = len(st.name)    
        inst = st.insaddr.insid
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
                
                DivFV = (Div * (DiscountFactor1/DiscountFactor2))
                DivPV = DivFV * DiscountFactor3
                
                if PayDay < d0:
                    list.append(0)
                
                else:
                    list.append(DivPV)
            
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
                
                SpotPrice = st.insaddr.used_price()
                list.append(SpotPrice)
                
                Global.append(list)
    Global.sort()
    print Global
    
    #outfile = '//services/frontnt/dart/ERM/StockDividends.csv'
    outfile = Outfile
    
    report = open(outfile, 'w')
    Headers=[]
    
    Headers = ['Stream', 'Stock', 'PayDate', 'Dividend', 'DivPV', 'Bucket', 'SpotPrice']
    
    for i in Headers:
        
        report.write((str)(i))
        report.write(',')
    report.write('\n')
        
    
    for lsts in Global:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
        
    report.close()
    return 'Success'
    #print 'The file has been saved at: C:\\DeClercqStockDividends.csv'
    
    
