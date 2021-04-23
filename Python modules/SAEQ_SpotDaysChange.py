import ael, string

def SpotDaysChange(temp,NewSpotDays,*rest):
    GlobalSpotChange=[]
    GlobalFail=[]
    file = ('C:\SpotDays.csv')
    
    try:
        sheet = open(file)
        
    except: 
        print 'Problem opening file'
    
    
    line = sheet.readline()
    
    while line:
    
        Success=[]
        
        line =sheet.readline()
        line = line.rstrip()
        l = string.split(line, ',')
        
        if (l[0] == '\n' or l[0] == ''): break
        
       
        ins = ael.Instrument[l[0]]
    
        new = ins.clone()
        new.spot_banking_days_offset = (int)(NewSpotDays)
        
        try:
            new.commit()
            
            ael.poll()
            
            Success.append(ins.insid)
            Success.append(ins.spot_banking_days_offset)
            
            GlobalSpotChange.append(Success)
            
            
        except:
            Fail=[]
            Fail.append(ins.insid)
            Fail.append(ins.spot_banking_days_offset)
            
            GlobalFail.append(Fail)
    
        
        
    sheet.close()
    
    GlobalSpotChange.sort()
    GlobalFail.sort()
    
    outfile1 = ('C:\\SpotDaysSuccess.csv')
    
    report1 = open(outfile1, 'w')
    
    Headers=[]
    
    Headers = ['Instrument', 'Spot_Days']
    
    for i in Headers:
        
        report1.write((str)(i))
        report1.write(',')
    report1.write('\n')
        
    
    for lsts in GlobalSpotChange:
        
        for ls in lsts:
            
            report1.write((str)(ls))
            report1.write(',')
        report1.write('\n')
    
    report1.close()
        
    print 'The file has been saved at C:\\SpotDaysSuccess.csv'
    #
    
    outfile2 = ('C:\\SpotDaysFail.csv')
    
    report2 = open(outfile2, 'w')
    
    Headers=[]
    
    Headers = ['Instrument', 'Spot_Days']
    
    for i in Headers:
        
        report2.write((str)(i))
        report2.write(',')
    report2.write('\n')
        
    
    for lsts in GlobalFail:
        
        for ls in lsts:
            
            report2.write((str)(ls))
            report2.write(',')
        report2.write('\n')
    
    report2.close()
        
    print 'The file has been saved at C:\\SpotDaysFail.csv'    
    return 'Success'
    
ael_variables = [('NewSpotDays', 'NewSpotDays', 'int', None, 5, 1)]              

def ael_main(ael_dict):

    NewSpotDays = ael_dict["NewSpotDays"]
    
    print SpotDaysChange(1, NewSpotDays)
