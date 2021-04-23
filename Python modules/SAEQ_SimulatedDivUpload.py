import ael, string
    
def SimDivUpload(EndDate, AnnualGrowth, Server):


    EndDate = EndDate
    GrowthFactor = (float)(AnnualGrowth)
    
    strm = ael.DividendStream.select()
    #print dir(strm)
    Updated = []
    Failed = []
    for st in strm.members():
       
            list1=[]
            list3=[]
            dic={}
            
            length = len(st.name)
            
            if st.name.__contains__('1') != 1 and length == 3:                
                
                for est in st.estimates():
                    
                    list2=[]
                    list2.append(est.day)
                    
                    record = (str)(est.day)
                    divs = (float)(est.dividend)
                    dic[record] = divs
                    
                    list1.append(list2)
                
                list1.sort()
                
                length = len(list1)
    
                if length != 0 and st.div_per_year <= length:                    
                    
                    count = st.div_per_year
                    
                    while count > 0:
                        
                        dat = list1[(length - count)]
                        list3.append(dat)
                        
                        count = count - 1
                    
                    for da in list3:
                        for dat in da:
                            next = dat.add_years(1)
    
                            div = dic[(str)(dat)] * (1 + (GrowthFactor)/100)
                            #print dat
                            
                            while next <= EndDate:
                                strms = st.clone()
                                if st.name not in Updated:
                                    Updated.append(st.name)
                                    
                                new = ael.DividendEstimate.new(strms) 
                            
                                new.day = next                      #LDT
                                new.ex_div_day = next.add_banking_day(ael.Instrument['ZAR'], 1)   #ex_div_day
                                new.pay_day = next.add_banking_day(ael.Instrument['ZAR'], 6)      #pay_day
                                new.dividend = div                  #dividend
                                new.curr = ael.Instrument['ZAR']    #curr
                                new.tax_factor = 1                  #tax_factor
                                new.description = 'Simulated'       #description
                                new.commit()
                                
                                next = next.add_years(1)   
                                div = div * (1 + (GrowthFactor)/100)
                            
                                strms.commit()
            
            elif st.name.__contains__('1') == 1 and length == 4:                
                
                for est in st.estimates():
                    
                    list2=[]
                    list2.append(est.day)
                    
                    record = (str)(est.day)
                    divs = (float)(est.dividend)
                    dic[record] = divs
                    
                    list1.append(list2)
                
                list1.sort()
                
                length = len(list1)
    
                if length != 0 and st.div_per_year <= length:                    
                    
                    count = st.div_per_year
                    
                    while count > 0:
                        
                        dat = list1[(length - count)]
                        list3.append(dat)
                        
                        count = count - 1
                    
                    for da in list3:
                        for dat in da:
                            next = dat.add_years(1)
    
                            div = dic[(str)(dat)] * (1 + (GrowthFactor)/100)
                            #print dat
                            
                            while next <= EndDate:
                                strms = st.clone()
                                if st.name not in Updated:
                                    Updated.append(st.name)
                                    
                                new = ael.DividendEstimate.new(strms) 
                            
                                new.day = next                      #LDT
                                new.ex_div_day = next.add_banking_day(ael.Instrument['ZAR'], 1)   #ex_div_day
                                new.pay_day = next.add_banking_day(ael.Instrument['ZAR'], 6)      #pay_day
                                new.dividend = div                  #dividend
                                new.curr = ael.Instrument['ZAR']    #curr
                                new.tax_factor = 1                  #tax_factor
                                new.description = 'Simulated'       #description
                                new.commit()
                                
                                next = next.add_years(1)   
                                div = div * (1 + (GrowthFactor)/100)
                            
                                strms.commit()

            
            
            if st.name not in Updated:
                Failed.append(st.name)
            
            
    #print 'Updated:',Updated
    #print 'Failed:',Failed
    
    outfile1 = Server + 'SimulatedDivsUpdated\\' + 'SimUpload' + ael.date_today().to_string('%Y%m%d') + '.csv'
    report1 = open(outfile1, 'w')
    
    for u in Updated:
    
        report1.write((str)(u))
        report1.write(',')
        report1.write('\n')
    
    report1.close()
    
    outfile2 = Server + 'SimulatedDivsFailed\\' + 'SimFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    report2 = open(outfile2, 'w')
    
    for f in Failed:
    
        report2.write((str)(f))
        report2.write(',')
        report2.write('\n')
    
    report2.close()
    
    print 'The file with the Simulated Updated dividend streams has been saved at' + Server + 'SimulatedDivsUpdated\\' + 'SimUpload' + ael.date_today().to_string('%Y%m%d') + '.csv'
    print 'The file with the Simulated Failed dividend streams has been saved at' + Server + 'SimulatedDivsFailed\\' + 'SimFailed' + ael.date_today().to_string('%Y%m%d') + '.csv'
    return 'Success'
            
                
ael_variables = [('EndDate', 'EndDate', 'date', None, ael.date_today().add_years(12), 1),
                ('AnnualGrowth', 'AnnualGrowth', 'float', None, 10, 1),
                ('Server', 'Server', 'string', None, 'C:\\', 1)]
    
#main
def ael_main(ael_dict):

    EndDate = ael_dict["EndDate"]
    AnnualGrowth = ael_dict["AnnualGrowth"]
    Server = ael_dict["Server"]
    
    SimDivUpload(EndDate, AnnualGrowth, Server)
    
                    
