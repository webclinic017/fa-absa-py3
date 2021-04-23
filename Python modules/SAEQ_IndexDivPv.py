import ael

def Simulator(temp,Indexs,StartDate,EndDate,*rest):#SettleDays,*rest):
    Global=[]
    
    StartDate = StartDate
    EndDate = EndDate
    
        
    ins = ael.Instrument[Indexs]
    SpotDays = ins.spot_banking_days_offset
    #print SpotDays 
    EndSpot = EndDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
    link = ins.combination_links()
    
    for lnk in link.members():
        
        inst = lnk.member_insaddr.insid
        #print lnk.member_insaddr.insid,lnk.member_insaddr.spot_banking_days_offset
                
        strm = ael.DividendStream.select('insaddr = "%d"' %(lnk.member_insaddr.insaddr))
        
        for st in strm:
            
            dic={}
            list1=[]
            list3=[]
            
            for est in st.estimates():
                list4=[]
                list2=[]
                list2.append(est.day)
                
                #////////////////////////////
                list4.append(inst)                          #Stock
                list4.append(est.day)                       #LDT
                list4.append(est.pay_day)                   #Pay_Day
                list4.append(est.dividend)                  #Dividend
                
                wght = lnk.weight
                factor = ins.index_factor
                
                
                #print StartSpot
                
                if est.pay_day > StartDate:
                
                    if est.pay_day > EndDate:
                    
                        IndexPoints = 0 
                        DivFV = 0
                        DivPV = 0
                        list4.append(IndexPoints) 
                        list4.append(DivPV)                         #DivPV  
                        list4.append(DivFV)                         #DivFV
                        
                    else:    
                        y = ins.used_repo_curve()
                        yc = ins.used_yield_curve()
                        ycf = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)']
                        
                        DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')                        
                        IndexPoints = (wght/factor)*est.dividend  
  
                        list4.append(IndexPoints)                   #IndexPoints  
                                    
                        DivFV = (IndexPoints * (DiscountFactor1/DiscountFactor2))
                        DivPV = DivFV * DiscountFactor3
       
                        
                        list4.append(DivPV)                         #DivPV  
                        list4.append(DivFV)                         #DivFV
                        #print est.pay_day                    
                
                else:
                
                    DivPV = 0
                    list4.append(DivPV)                         #DivPV
                    DivFV = 0
                    list4.append(DivFV)                         #DivFV
                
                Global.append(list4)                        #Add list4 to the Global list
                
                
                    
    Global.sort()
    
    outfile = 'C:\\DividendEstimates.csv'
    
    report = open(outfile, 'w')
    Headers=[]
    
    Headers = ['Stock', 'LDT', 'PayDate', 'Dividend', 'IndexPoints', 'DivPv', 'DivFv']
    
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
    print'Success'
    return 'The file has been saved at: C:\\DividendEstimates.csv'
    
    
def Index():
    Indexs = []
    for t in ael.Instrument.select('instype = "EquityIndex"'):
        Indexs.append(t.insid)
    Indexs.sort()
    return Indexs

ael_variables = [('Index', 'EquityIndex', 'string', Index(), 'ZAR/ALSID_FF', 1),
                ('StartDate', 'StartDate', 'date', None, ael.date_today(), 1),
                 ('EndDate', 'EndDate', 'date', None, ael.date_today().add_years(5), 1)]
                 #('SettleDays','SettleDays','int',None,0,1)]
    
#main
def ael_main(ael_dict):

    Indexs = ael_dict["Index"]
    StartDate = ael_dict["StartDate"] 
    EndDate = ael_dict["EndDate"]
    #SettleDays = ael_dict["SettleDays"]
    print Simulator(1, Indexs, StartDate, EndDate)#,SettleDays)
    
    



