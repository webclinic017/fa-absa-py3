import ael

'''
This script is used as a Dividend Tool to upload the MARKIT dividends.
Jurg du Preez           2008-01-02
'''

'''
try:
    f = open('G:\\Data\\TheBlackSwan\\password.txt')
except:
    print 'Could not open password file'
line = f.readline()
list = []
line = line.rstrip()
if line:
    list = line.split(',')
print list
ael.connect("v036syb104001:9100",(str)(list[0]),(str)(list[1]))
f.close()
'''

#DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE	START
#DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE	START
#Create a file that contains all the dividend information 

try:
    f = open('C:\\TheBlackSwan\\password.txt')
except:
    print 'Could not open password file'
line = f.readline()
list = []
line = line.rstrip()
if line:
    list = line.split(',')
#print list
ael.connect("10.2.28.234:9100", (str)(list[0]), (str)(list[1]))
f.close()

try:
    b = open('C:\\TheBlackSwan\\password.txt', 'w')
except:
    print 'error'
b.close()
    
	
#DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE	START
#DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE	START
#Create a file that contains all the dividend information 

import string
Rates=[]
GlobalEST=[]
GlobalAct=[]
strm = ael.DividendStream.select()

dat = ael.date_today()

for st in strm.members():
    
    length = len(st.name)
    ins = st.insaddr
    div = ins.dividends()
    inst = st.insaddr.insid
    
    if length == 3 or length == 4:
    
        for d in div:
        
            listAct=[]
            listAct.append(inst)
            ExDivDay = d.ex_div_day
            listAct.append(ExDivDay)
            PayDay = d.pay_day
            listAct.append(PayDay)
            Div = d.dividend
            listAct.append(Div)
            Des = d.description
            listAct.append(Des)
        
            GlobalAct.append(listAct)
            
        GlobalAct.sort()
            
        for est in st.estimates():
                        
            list=[]
            strmname = st.name
            list.append(strmname)
            list.append(inst)
            ExDivDay = est.ex_div_day
            list.append(ExDivDay)
            PayDay = est.pay_day
            list.append(PayDay)
            Div = est.dividend
            list.append(Div)
            Des = est.description
            list.append(Des)
    
            GlobalEST.append(list)
            
        GlobalEST.sort()
#print Global

outfilebeforeAct = 'C:\\TheBlackSwan\\ActBefore\\' + dat.to_string('%Y%m%d') + '.csv'

report = open(outfilebeforeAct, 'w')
Headers=[]

Headers = ['Stock', 'ExDivDay', 'PayDate', 'Dividend', 'Description']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')
    

for lsts in GlobalAct:
    
    for ls in lsts:
        
        report.write((str)(ls))
        report.write(',')
    report.write('\n')
    
report.close()


outfilebeforeEST = 'C:\\TheBlackSwan\\EstBefore\\' + dat.to_string('%Y%m%d') + '.csv'

report = open(outfilebeforeEST, 'w')
Headers=[]

Headers = ['Stream', 'Stock', 'ExDivDay', 'PayDate', 'Dividend', 'Description']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')
    

for lsts in GlobalEST:
    
    for ls in lsts:
        
        report.write((str)(ls))
        report.write(',')
    report.write('\n')
    
report.close()

print 'The file that contains all the previous Actual Dividends has been saved at: C:\\TheBlackSwan\\ActBefore\\' + dat.to_string('%Y%m%d') + '.csv'
print 'The file that contains all the previous Estimated Dividends has been saved at: C:\\TheBlackSwan\\EstBefore\\' + dat.to_string('%Y%m%d') + '.csv'

#DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE DIVESTBEFORE	END
#DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE DIVACTBEFORE	END

file = 'C:\\TheBlackSwan\\Output\\' + dat.to_string('%Y%m%d') + '.csv'

try:
    sheet = open(file)
except:
    print 'Problem opening TheBlackSwanOutputSheet'

list = []
contain = []
contain1 = []
failed = []     #List that contains all the non-existent strm
failed1 = []    #List that contains all the non-existent strmtwo
line = sheet.readline()
l = string.split(line, ',')

while line:
    line = sheet.readline()
    l = string.split(line, ',')
    if (l[0] == '\n' or l[0] == ""): break
    
    if l[3] == "" or l[4] == "" or l[5] == "" :
        
        line = sheet.readline()
        l = string.split(line, ',')
        if (l[0] == '\n' or l[0] == ""): break    
    
    else:
        l[5] = ael.date(l[5].replace('/', '-'))      #ExDivDay
            
        if l[6] != "":
            l[6] = ael.date(l[6].replace('/', '-'))       #RecordDay
            
        else:
            l[6] = l[5]
            
        if l[7] != "":
            l[7] = ael.date(l[7].replace('/', '-'))       #PayDay
            
        else:
            l[7] = l[5]
            
        l[8] = (float)(l[8])        #Ordinary
        l[9] = (float)(l[9])        #Special
        
        one = l[3] + '1'
        
        hoax = 'fail'
        
        strm = ael.DividendStream[l[3]]
        strmtwo = ael.DividendStream[one]
        
        #ins = strm.insaddr.clone()
        
        if strm:
            hoax = 'player'
            strm = strm.clone()
            est = strm.estimates()
            
            if l[5] <= ael.date_today():

		rt=[]
                
                ins = strm.insaddr.clone()
                
                if l[3] not in contain:
                                
                    for child in ins.children():
                        if child.record_type == 'Dividend':
                            child.delete()
                            
                
                
                new = ael.Dividend.new(ins)
                new.ex_div_day = l[5]
                new.day = l[6]
                new.pay_day = l[7]
                total = l[8]
                
                #print l[3],l[5]
                FXrate = ael.Instrument[l[4]].used_price(l[5], 'ZAR')
		
		rt.append(l[3])
		rt.append(l[4])
		rt.append(l[5])
		rt.append(FXrate)
		Rates.append(rt)

                convert = total * FXrate
                new.dividend = convert
                new.curr = ael.Instrument['ZAR']
                new.tax_factor = 1
                new.description = l[12]
                new.commit()
                
                ins.commit()
                
                   
            elif l[5] > ael.date_today():     #The dividend information that must uploaded to the DividendEstimation tables
                
		rt=[]

		for i in est:
                    
                    if l[3] not in contain:
                        
                        i.delete()
                            
                contain.append(l[3])
                
                new = ael.DividendEstimate.new(strm)
                new.ex_div_day = l[5]
                new.day = l[6]
                new.pay_day = l[7]
                total = l[8]
                #print'l', l[3],l[5]
                FXrate = ael.Instrument[l[4]].used_price(ael.date_today(), 'ZAR')

		rt.append(l[3])
		rt.append(l[4])
		rt.append(l[5])
		rt.append(FXrate)
		Rates.append(rt)

                convert = total * FXrate
                new.dividend = convert
                new.curr = ael.Instrument['ZAR']
                new.tax_factor = 1
                new.description = l[12]
                new.commit()
                
                strm.commit()
        
        if hoax == 'fail' and l[3] not in failed:
            failed.append(l[3])
        
        hoax = 'fail1'
        if strmtwo:
            hoax = 'player1'
            strmtwo = strmtwo.clone()
            est = strmtwo.estimates()
            
            if l[5] <= ael.date_today():
                
                ins1 = strmtwo.insaddr.clone()
                
                if one not in contain1:
                
                    for child in ins1.children():
                        if child.record_type == 'Dividend':
                            child.delete()
                    
                new = ael.Dividend.new(ins1)
                new.ex_div_day = l[5]
                new.day = l[6]
                new.pay_day = l[7]
                total = l[8]+l[9]
                FXrate = ael.Instrument[l[4]].used_price(l[5], 'ZAR')
                convert = total * FXrate
                new.dividend = convert
                new.curr = ael.Instrument['ZAR']
                new.tax_factor = 1
                new.description = l[12]
                new.commit()
    
                ins1.commit()
    
    
            elif l[5] > ael.date_today():     #The dividend information that must uploaded to the DividendEstimation tables
                for i in est:
                
                    if one not in contain1:
                        
                        i.delete()
                            
                contain1.append(one)
                
                new = ael.DividendEstimate.new(strmtwo)
                new.ex_div_day = l[5]
                new.day = l[6]
                new.pay_day = l[7]
                total = l[8]+l[9]
                FXrate = ael.Instrument[l[4]].used_price(ael.date_today(), 'ZAR')
                convert = total * FXrate
                new.dividend = convert
                new.curr = ael.Instrument['ZAR']
                new.tax_factor = 1
                new.description = l[12]
                new.commit()
                
                strm.commit()
            
        if hoax == 'fail1' and one not in failed1:
            failed1.append(one)
            
outfilefail = 'C:\\TheBlackSwan\\FailList\\' + dat.to_string('%Y%m%d') + '.csv'

report = open(outfilefail, 'w')
Headers = []

Headers = ['Stream']

for i in Headers:

    report.write((str)(i))
    report.write(',')
report.write('\n')

for ls in failed:

    report.write((str)(ls))
    report.write(',')
report.write('\n')

for ls in failed1:

    report.write((str)(ls))
    report.write(',')
report.write('\n')

report.close()
print 'The failed list has been saved at C:\\TheBlackSwan\\FailList\\' + dat.to_string('%Y%m%d') + '.csv'
sheet.close()

ael.poll()

#DIVESTAFTER DIVESTAFTER DIVESTAFTER DIVESTAFTER        START   
#DIVACTAFTER DIVACTAFTER DIVACTAFTER DIVACTAFTER        START       

GlobalEST=[]
GlobalAct=[]
strm = ael.DividendStream.select()

for st in strm.members():
    
    length = len(st.name) 
    ins = st.insaddr
    div = ins.dividends()
    inst = st.insaddr.insid
    
    if length == 3 or length == 4:
    
        for d in div:
        
            listAct=[]
            listAct.append(inst)
            ExDivDay = d.ex_div_day
            listAct.append(ExDivDay)
            PayDay = d.pay_day
            listAct.append(PayDay)
            Div = d.dividend
            listAct.append(Div)
            Des = d.description
            listAct.append(Des)
        
            GlobalAct.append(listAct)
            
        GlobalAct.sort()

        
        for est in st.estimates():
            
            list=[]
            strmname = st.name
            list.append(strmname)
            list.append(inst)
            ExDivDay = est.ex_div_day
            list.append(ExDivDay)
            PayDay = est.pay_day
            list.append(PayDay)
            Div = est.dividend
            list.append(Div)
            Des = est.description
            list.append(Des)
    
            GlobalEST.append(list)
            
        GlobalEST.sort()
#print Global

outfileafterAct = 'C:\\TheBlackSwan\\ActAfter\\' + dat.to_string('%Y%m%d') + '.csv'

report = open(outfileafterAct, 'w')
Headers=[]

Headers = ['Stock', 'ExDivDay', 'PayDate', 'Dividend', 'Description']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')
    

for lsts in GlobalAct:
    
    for ls in lsts:
        
        report.write((str)(ls))
        report.write(',')
    report.write('\n')
    
report.close()

print 'The file that contains all the new Actual Dividends has been saved at: C:\\TheBlackSwan\\ActAfter\\' + dat.to_string('%Y%m%d') + '.csv'

outfileafterEST = 'C:\\TheBlackSwan\\EstAfter\\' + dat.to_string('%Y%m%d') + '.csv'
report = open(outfileafterEST, 'w')
Headers=[]

Headers = ['Stream', 'Stock', 'ExDivDay', 'PayDate', 'Dividend', 'Description']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')
    

for lsts in GlobalEST:
    
    for ls in lsts:
        
        report.write((str)(ls))
        report.write(',')
    report.write('\n')
    
report.close()

print 'The file that contains all the new Estimated Dividends has been saved at: C:\\TheBlackSwan\\EstAfter\\' + dat.to_string('%Y%m%d') + '.csv'

#DIVESTAFTER DIVESTAFTER DIVESTAFTER DIVESTAFTER        END
#DIVACTAFTER DIVACTAFTER DIVACTAFTER DIVACTAFTER        END   

Rates.sort()

print Rates

outfileFXRates = 'C:\\TheBlackSwan\\FXRates\\' + 'Rates' + '.csv'

report = open(outfileFXRates, 'w')
Headers=[]

Headers = ['StockCode', 'Currency', 'ExDivDay', 'FXRate']

for i in Headers:
    
    report.write((str)(i))
    report.write(',')
report.write('\n')


for r in Rates:
    
    for ra in r:
        
        report.write((str)(ra))
        report.write(',')
    report.write('\n')
    
report.close()

print 'The file that contains all the FX rates has been saved at: C:\\TheBlackSwan\\FXRates\\' + 'Rates' + '.csv' 
print 'Success'
ael.disconnect()
