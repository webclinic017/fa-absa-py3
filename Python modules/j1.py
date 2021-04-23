import ael

EndDate = ael.date('2012-08-20')
#strm = ael.DividendStream['AGL1']

ins = ael.Instrument['ZAR/ALSID_TEST1']

print dir(ins)

link = ins.combination_links()

for lnk in link.members():
    
    #print dir(lnk)
    #print lnk.member_insaddr.insid
    inst = lnk.member_insaddr.insid
    
    #print dir(list)
    
    strm = ael.DividendStream.select('insaddr = "%d"' %(lnk.member_insaddr.insaddr))
    #print strm
    
    for st in strm:
        print inst
        print 'AnnualGrowth:%s Div per year:%f'%(st.annual_growth, st.div_per_year)
        
        dic={}
        list1=[]
        list3=[]
        
        for est in st.estimates():
            list2=[]
            list2.append(est.day)
            record = (str)(est.day)
            divs = (float)(est.dividend)
            dic[record] = divs
            #list2.append(est.dividend)
            list1.append(list2)
        #print list1
        list1.sort()
        print dic
        print list1
        length = len(list1)
        print 'length', length
        print 'div_per_year', st.div_per_year
        
        count = st.div_per_year
        
        while count > 0:
        
            dat = list1[(length - count)]
            list3.append(dat)
            
            count = count - 1
            
        print list3
        
        for da in list3: 
            
            for dat in da:
                next = dat.add_years(1)
                div = dic[(str)(dat)] * (1 + (st.annual_growth)/100)
                #print 'next',next,EndDate                

                while next <= EndDate:
                    
                    print 'Record Day:%s  div:%f' %(next, div)
                    
                    Ex_Div_Day = next.add_days(3)       #Simulated Ex Div Day
                    Pay_Day = Ex_Div_Day                #Simulated Pay Day
                    
                    next = next.add_years(1)            #next = Simulated Record Day
                    div = div * (1 + (st.annual_growth)/100)

                #print 'dat',dat
                #next = dat.add_years(1)
                #print 'next',next
            
            
        
            
            

