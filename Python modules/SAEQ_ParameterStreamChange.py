import ael, string

Global=[]

strm = ael.DividendStream.select()

for mbr in strm.members():

    name = mbr.name
        
    if (string.find(name, '1') != -1):
    
        List=[]
        List.append(name)
        todate = ael.date_today().add_years(5)
        growth = mbr.annual_growth
        List.append(growth)
        divperyear = mbr.div_per_year
        List.append(divperyear)
        factor = mbr.adjustment_factor
        List.append(factor)
        cutter = name[0:3]
        
        Global.append(List)
        #print name
        #print cutter,growth,factor,divperyear

        if ael.DividendStream[cutter]:
            #print cutter
            clone = ael.DividendStream[cutter].clone()
            clone.date_to = todate
            clone.annual_growth = growth
            clone.adjustment_factor = factor
            clone.div_per_year = divperyear
            clone.commit()
            
            ael.poll()
            
            cutter = cutter
            growth = ael.DividendStream[cutter].annual_growth
            divperyear = ael.DividendStream[cutter].div_per_year
            factor = ael.DividendStream[cutter].adjustment_factor
            #print cutter,growth,factor,divperyear
            
            List=[]
            
            List.append(cutter)
            List.append(growth)
            List.append(divperyear)
            List.append(factor)
            
            Global.append(List)
            
Global.sort()

outfile = 'C:\\ParameterStreamCopy.csv'

report = open(outfile, 'w')
Headers=[]

Headers = ['Stream', 'Growth', 'DivPerYear', 'Factor']

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
print 'The file has been saved at: C:\\ParameterStreamCopy.csv'


            

        
        
