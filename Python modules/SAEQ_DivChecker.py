import ael, string
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
            
            if est.day >= ael.date_today():
                list=[]
                strmname = st.name
                list.append(strmname)
                list.append(inst)
                LDT = est.day
                list.append(LDT)
                PayDay = est.pay_day
                list.append(PayDay)
                Div = est.dividend
                list.append(Div)
        
                Global.append(list)
Global.sort()
print Global

outfile = 'C:\\DivChecker.csv'

report = open(outfile, 'w')
Headers=[]

Headers = ['Stream', 'Stock', 'LDT', 'PayDate', 'Dividend']

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
print 'Success'
print 'The file has been saved at: C:\\DivChecker.csv'



        #print m.estimates()
        #print st.annual_growth,st.div_per_year
'''        
        dic={}
        list1=[]
        list3=[]
        
        for est in st.estimates():
            
            list2=[]
            list2.append(est.day)
'''
