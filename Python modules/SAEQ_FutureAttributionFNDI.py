import ael, string

list2 = ['ZAR/FNDI']         

#main

def ael_main(ael_dict):

    StartDate = ael_dict["StartDate"] 
    EndDate = ael_dict["EndDate"]
    Server = ael_dict["Server"]
    tel=0       
    for u in list2:

        tel += 1
        Simulator(1, str(u), StartDate, EndDate, tel, Server)
ael_variables = [('StartDate', 'StartDate', 'date', None, ael.date_today().add_banking_day(ael.Instrument['ZAR'], 0), 1),
                 ('EndDate', 'EndDate', 'date', None, ael.date('2008-09-18'), 1),
                 ('Server', 'Server', 'string', None, '//services/frontnt/BackOffice/Atlas-End-Of-Day/', 1)]                
        
def Simulator(temp,Indexs,StartDate,EndDate,tel,Server,*rest):
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
        
        con = lnk.member_insaddr
                        
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
                list4.append(StartDate)
                list4.append(StartSpot)
                list4.append(EndDate)
                list4.append(EndSpot)
                list4.append(Indexs)                        #Index
                
                IndexPrice = ins.used_price(ael.date(StartDate), 'ZAR', '', 0, 'SPOT')
                list4.append(IndexPrice)                    #IndexPrice
                
                list4.append(con.insid)                     #Constituent
                
                ConstituentPrice = con.used_price(ael.date(StartDate), 'ZAR', '', 0, 'SPOT')
                list4.append(ConstituentPrice)             #ConstituentPrice
                
                list4.append(est.day)                       #LDT
                list4.append(est.pay_day)                   #Pay_Day
                list4.append(est.dividend)                  #Dividend
                
                wght = lnk.weight
                factor = ins.index_factor
                
                
                #print StartSpot
                
                #LDT = est.ex_div_day.add_banking_day(ael.Instrument['ZAR'],-1)
                
                if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) >= StartDate:
                
                    if est.ex_div_day.add_banking_day(ael.Instrument['ZAR'], -1) >= EndDate:
                    
                        IndexPoints = 0 
                        #DivFV = 0
                        DivPV = 0
                        
                        list4.append(IndexPoints) 
                        list4.append(DivPV)                         #DivPV                         
                        DiscountFactorTplusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, StartSpot, None, None, 'Discount', 0, 'ZAR')
                        list4.append(DiscountFactorTplusSpot)
                        
                        DiscountFactorTtoExpPlusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, EndSpot, None, None, 'Discount', 0, 'ZAR')
                        list4.append(DiscountFactorTtoExpPlusSpot)
                        #list4.append(DivFV)                         #DivFV
                        
                    else:    
                    
                        y = ins.used_repo_curve()
                        
                        #print y.und_ir_name
                        
                        yc = ins.used_yield_curve()
                        
                        ycf = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)']                                             

                        #print dir(ycf)
                        
                        DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                        DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')                        
                        IndexPoints = (wght/factor)*est.dividend  
  
                        list4.append(IndexPoints)                   #IndexPoints  
                                    
                        DivFV = (IndexPoints * (DiscountFactor1/DiscountFactor2))
                        DivPV = DivFV * DiscountFactor3
       
                        
                        list4.append(DivPV)                         #DivPV  
                        
                        DiscountFactorTplusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, StartSpot, None, None, 'Discount', 0, 'ZAR')
                        list4.append(DiscountFactorTplusSpot)
                        
                        DiscountFactorTtoExpPlusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, EndSpot, None, None, 'Discount', 0, 'ZAR')
                        list4.append(DiscountFactorTtoExpPlusSpot)
                        #list4.append(DivFV)                         #DivFV
                        #print est.pay_day                    
                
                else:
                    
                    IndexPoints = 0
                    list4.append(IndexPoints)
                    DivPV = 0
                    list4.append(DivPV)                         #DivPV
                    DiscountFactorTplusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, StartSpot, None, None, 'Discount', 0, 'ZAR')
                    list4.append(DiscountFactorTplusSpot)
                    
                    DiscountFactorTtoExpPlusSpot = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)'].yc_rate(StartDate, EndSpot, None, None, 'Discount', 0, 'ZAR')
                    list4.append(DiscountFactorTtoExpPlusSpot)
                    #DivFV = 0
                    #list4.append(DivFV)                         #DivFV
                
                Global.append(list4)                        #Add list4 to the Global list
                
                
                    
    Global.sort()
    
    outfile = Server  + 'FutureForwardVariables_' + str(tel) + '_' + StartDate.to_string('%y%m%d') + 'FNDI' + '.csv'
    print outfile
    report = open(outfile, 'w')
    Headers=[]
    
    Headers = ['StartDate', 'StartPlusSpot', 'Expiry', 'ExpiryPlusSpot', 'Index', 'IndexPrice', 'Constituent', 'ConstituentPrice', 'LDT', 'PayDate', 'Dividend', 'IndexPoints', 'DivPv', 'DiscountFactorTplusSpot', 'DiscountFactorTtoExpPlusSpot']
    
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
    print 'The file has been saved at:' + Server + 'FutureForwardVariables_' + str(tel) + '_' + StartDate.to_string('%y%m%d') + 'FNDI' + '.csv'
    return
    

  



