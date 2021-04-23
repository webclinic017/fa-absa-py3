import ael

def Simulator(temp,Indexs,StartDate,EndDate,SettleDays,*rest):
    Global=[]
    
    StartDate = StartDate
    EndDate = EndDate
    EndSett = EndDate.add_banking_day(ael.Instrument['ZAR'], SettleDays)
        
    ins = ael.Instrument[Indexs]
    SpotDays = ins.spot_banking_days_offset
    print SpotDays 
    
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
                
                IndexPoints = (wght/factor)*est.dividend    
                list4.append(IndexPoints)                   #IndexPoints
                
                 
                
                if est.ex_div_day > StartDate:
                    #??????????????
                    StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
                    #??????????????
                    yc = ins.used_yield_curve()
                    #ycf = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)']
                    
                    #print yc.ir_name
                    
                    yieldPV = yc.yc_rate(StartSpot, EndSett, 'Simple', 'Act/365', 'Spot Rate')
                    yieldFV = yc.yc_rate(est.pay_day, EndSett, 'Simple', 'Act/365', 'Spot Rate')
                
                    DivPV = (IndexPoints * (1 + yieldFV * est.pay_day.days_between(EndSett, 'Act/365')/365)) * (1/(1 + yieldPV * StartSpot.days_between(EndSett, 'Act/365')/365))
   
                    list4.append(DivPV)                         #DivPV      

                    #print est.pay_day
                
                    DivFV = (IndexPoints * (1 + yieldFV * est.pay_day.days_between(EndSett, 'Act/365')/365)) 
                    list4.append(DivFV)                         #DivFV
                
                else:
                
                    DivPV = 0
                    list4.append(DivPV)                         #DivPV
                    DivFV = 0
                    list4.append(DivFV)                         #DivFV
                
                Global.append(list4)                        #Add list4 to the Global list
                
                
                record = (str)(est.day)
                divs = (float)(est.dividend)
                dic[record] = divs
                               
                list1.append(list2)
            
            list1.sort()
            length = len(list1)
            
            
            count = st.div_per_year
            
            while count > 0:
            
                dat = list1[(length - count)]
                list3.append(dat)
                
                count = count - 1
                
            for da in list3: 
                
                for dat in da:
                    next = dat.add_years(1)
                    div = dic[(str)(dat)] * (1 + (st.annual_growth)/100)
    
                    while next <= EndDate:
                        
                        list5=[]
                                                
                        #//////////////////////////////////////////////////////////
                        list5.append(inst)                          #Stock
                        list5.append(next)                          #LDT
                        
                        Ex_Div_Day = next.add_days(3)       #Simulated Ex Div Day
                        Pay_Day = Ex_Div_Day                #Simulated Pay Day
                        
                        list5.append(Pay_Day)                       #Pay_Day
                        list5.append(div)                           #Dividend
                        
                        wght = lnk.weight
                        factor = ins.index_factor
                
                        IndexPoints = (wght/factor)*div
                        
                        list5.append(IndexPoints)                   #IndexPoints
                        
                        StartSpot = StartDate.add_banking_day(ael.Instrument['ZAR'], SpotDays)
                        
                        yc = ins.used_yield_curve()
                        #ycf = ael.YieldCurve['ZAR-SWAP-SPREAD(50bp)']
                        
                        yieldPV = yc.yc_rate(StartSpot, EndSett, 'Simple', 'Act/365', 'Spot Rate')
                        yieldFV = yc.yc_rate(Pay_Day, EndSett, 'Simple', 'Act/365', 'Spot Rate')
                        
                        DivPV = (IndexPoints * (1 + yieldFV * Pay_Day.days_between(EndSett, 'Act/365')/365)) * (1/(1 + yieldPV * StartSpot.days_between(EndSett, 'Act/365')/365))   
                        list5.append(DivPV)                         #DivPV                       
                        
                        DivFV = (IndexPoints * (1 + yieldFV * Pay_Day.days_between(EndSett, 'Act/365')/365)) 
                        list5.append(DivFV)                         #DivFV
                        
                        #Global.append(list5)                        #Add list5 to the Global list
                        
                        
                        
                        next = next.add_years(1)                    #next = Simulated Record Day
                        div = div * (1 + (st.annual_growth)/100)
    
                    
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
                 ('EndDate', 'EndDate', 'date', None, ael.date_today().add_years(5), 1),
                 ('SettleDays', 'SettleDays', 'int', None, 2, 1)]
    
#main
def ael_main(ael_dict):

    Indexs = ael_dict["Index"]
    StartDate = ael_dict["StartDate"] 
    EndDate = ael_dict["EndDate"]
    SettleDays = ael_dict["SettleDays"]
    print Simulator(1, Indexs, StartDate, EndDate, SettleDays)
    
    



