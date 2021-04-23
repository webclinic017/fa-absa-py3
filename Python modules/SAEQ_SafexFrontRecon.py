import ael, string

ael_variables = [('Server', 'Server', 'string', None, 'C:\SafexBookingFeeRecon', 1)]

def ael_main(ael_dict):

    Server = ael_dict["Server"]
    print Recon(Server)


def Recon(Server,*rest):
    co = 1
    Lnbr = 1
    failer = 0
    
    GlobalCorrect=[]
    GlobalNotInFA=[]
    GlobalReconDiff=[]
    GlobalFail=[]
    
    pta=[]
    totaal = 0
    probleme = 0
    
    ABLdicSAFEX={}
    ABLdicFRONT={}
    
    ABLMTM={}
    JFEMTM={}
    ABLFAMTM={}
    JFEFAMTM={}
    
    ABLNameList=[]
    
    JFEdicSAFEX={}
    JFEdicFRONT={}
    JFENameList=[]
    
    proba=[]
    probj=[] 
    
    FailFrontABL=[]
    FailFrontJFE=[] 
    
    JFE = ael.TradeFilter['Arbbaskets All SafexCP']
    ABL = ael.TradeFilter['ABL Trade accounts']
    
    dat = ael.date_today()
    
    file = Server + '\\SafexReport\\' + dat.to_string('%Y%m%d') + '.csv'
    
    try:
        f = open(file)
        
    except:
        print'Problem opening the' + dat.to_string('%Y%m%d') + '.csv file'
    
    line = f.readline()
        
    fails=[]
    lekkers=[]
    
    while line:
    
        fails=[]
        lekkers=[]
        
        line = f.readline()
        line = line.replace('"', '')
        #print dir(line)
        l = line.split(',')
        if (l[0] == '\n' or l[0] == ""): break
        
        Lnbr += 1
        co += 1
        
        list=[]
        for i in l:
            reg = i.lstrip()
            reg = reg.rstrip()
            list.append(reg)
            
        date = ael.date_from_string(list[6], '%d/%m/%Y')
        monthYear = date.to_string('%b%y')
        
        
        #Filtering through all the instruments within the ABL account file from SAFEX
        if l[1] == 'ABL' and l[2] == 'ABL':
            
            if list[3] == 'Future':
                
                if list[4] == 'Stock':
                
                    if list[5][3:4] == 'Q':
                        stock = list[5][:3]
                        
                    elif list[5][3:4] == 'V': 
                        stock = list[5][:4]
                        
                    else:
                        stock = list[5][:3]
                        
                    ABLname = 'ZAR/' + stock + '/' + (str)(monthYear.upper())
                    
                
                elif list[4] == 'Index':
                    index = list[5]
                    ABLname = 'ZAR/' + index + '/' + (str)(monthYear.upper())
                    
            elif list[3] == 'Option':
            
                if list[4] == 'Stock':
                
                    if list[5][3:4] == 'Q':
                        stock = list[5][:3]
                        
                    elif list[5][3:4] == 'V': 
                        stock = list[5][:4]
                        
                    else:
                        stock = list[5][:3]
                        
                    ABLname = 'ZAR/' + 'FUT/' + stock + '/' + str(monthYear.upper()) + '/' + (str(list[7])).upper() + '/' + '%.2f' %(float)(list[8])
                               
                elif list[4] == 'Index':
                    index = list[5]
                    ABLname = 'ZAR/' + 'FUT/' + index + '/' + str(monthYear.upper()) + '/' + (str(list[7])).upper() + '/' + '%.2f' %(float)(list[8])
            
            #ABLSAFEX's positions
            #ABLSAFEX's MTM
            if ael.Instrument[ABLname]:
            
                if ABLname not in ABLNameList:
                    ABLNameList.append(ABLname)
                    
                if ABLMTM.has_key(ABLname):
                    pass
                else:
                    ABLMTM[ABLname] = list[10]
                
                if ABLdicSAFEX.has_key(ABLname):
                    value = int(ABLdicSAFEX[ABLname])
                    ABLdicSAFEX[ABLname] = value + int(list[9])
                        
                else:            
                    ABLdicSAFEX[ABLname] = list[9]
                    
            else:
                NotInFA=[]
                NotInFA.append(Lnbr)
                NotInFA.append(ABLname)
                GlobalNotInFA.append(NotInFA)
                
        #Filtering through all the instruments within the JFE account file from SAFEX
        elif l[1] == 'JFE' and l[2] == 'JFE':
        
            if list[3] == 'Future':
            
                if list[4] == 'Stock':
                        stock = list[5][:3]
                        JFEname = 'ZAR/' + stock + '/' + (str)(monthYear.upper())
            
                elif list[4] == 'Index':
                    index = list[5]
                    JFEname = 'ZAR/' + index + '/' + (str)(monthYear.upper())
                    
            elif list[3] == 'Option':
            
                if list[4] == 'Stock':
                    stock = list[5][:3]
                    JFEname = 'ZAR/' + 'FUT/' + stock + '/' + str(monthYear.upper()) + '/' + (str(list[7])).upper() + '/' + '%.2f' %(float)(list[8])
                               
                elif list[4] == 'Index':
                    index = list[5]
                    JFEname = 'ZAR/' + 'FUT/' + index + '/' + str(monthYear.upper()) + '/' + (str(list[7])).upper() + '/' + '%.2f' %(float)(list[8])
    
            #JFESAFEX's positions
            #JFESAFEX's MTM
            if ael.Instrument[JFEname]:
            
                if JFEname not in JFENameList:
                    JFENameList.append(JFEname)
                    
                if JFEMTM.has_key(JFEname):
                    pass
                else:
                    JFEMTM[JFEname] = list[10]
                
                if JFEdicSAFEX.has_key(JFEname):
                    value = int(JFEdicSAFEX[JFEname])
                    JFEdicSAFEX[JFEname] = value + int(list[9])
                        
                else:            
                    JFEdicSAFEX[JFEname] = list[9]
                    
            else:
                NotInFA=[]
                NotInFA.append(Lnbr)
                NotInFA.append(JFEname)
                GlobalNotInFA.append(NotInFA)
    #ABLFront's positions
    for a in ABL.trades():
        
        FAABLins = a.insaddr
        ABLins = a.insaddr.insid
        
        if ABLFAMTM.has_key(ABLins):
            pass
        else:
            ABLFAMTM[ABLins] = FAABLins.mtm_price(ael.date_today(), FAABLins.curr.insid, 0, 0)
        
        if ABLdicFRONT.has_key(ABLins):
            value = int(ABLdicFRONT[ABLins])
            ABLdicFRONT[ABLins] = value + a.quantity
            
        else:    
            ABLdicFRONT[ABLins] = a.quantity
    
    #JFEFront's positions
    for j in JFE.trades():
        
        FAJFEins = j.insaddr
        JFEins = j.insaddr.insid
        
        if JFEFAMTM.has_key(JFEins):
            pass
        else:
            JFEFAMTM[JFEins] = FAJFEins.mtm_price(ael.date_today(), FAJFEins.curr.insid, 0, 0)
        
        if JFEdicFRONT.has_key(JFEins):
            value = int(JFEdicFRONT[JFEins])
            JFEdicFRONT[JFEins] = value + j.quantity
            
        else:    
            JFEdicFRONT[JFEins] = j.quantity              
    #Recon between ABLFront's and ABLSafex's positions
    for ab in ABLNameList:
        
        if ABLdicFRONT.has_key(ab):    
                        
            if int(ABLdicSAFEX[ab]) == int(ABLdicFRONT[ab]):
                Recon=[]
                Recon.append(ab)
                Recon.append(ABLdicSAFEX[ab])
                Recon.append(ABLdicFRONT[ab])
                Recon.append(ABLMTM[ab])                    #SafexMTM  
                Recon.append(ABLFAMTM[ab])                  #FAMTM
                GlobalCorrect.append(Recon)
            
            else:
                Prob=[]
                Prob.append(ab)
                Prob.append(ABLdicSAFEX[ab])
                Prob.append(ABLdicFRONT[ab])
                Prob.append(ABLMTM[ab])                     #SafexMTM
                Prob.append(ABLFAMTM[ab])                   #FAMTM
                GlobalReconDiff.append(Prob)
                
        else:
            Fail=[]
            Fail.append(ab)
            Fail.append(ABLdicSAFEX[ab])        
            GlobalFail.append(Fail)
        
            
    #Recon between JFEFront's and JFESafex's positions
    for jf in JFENameList:
        
        if JFEdicFRONT.has_key(jf):     
                        
            if int(JFEdicSAFEX[jf]) == int(JFEdicFRONT[jf]):
                Recon=[]
                Recon.append(jf)
                Recon.append(JFEdicSAFEX[jf])
                Recon.append(JFEdicFRONT[jf])
                Recon.append(JFEMTM[jf])                    #SafexMTM
                Recon.append(JFEFAMTM[jf])                  #FAMTM
                GlobalCorrect.append(Recon)
            
            else:
                Prob=[]
                Prob.append(jf)
                Prob.append(JFEdicSAFEX[jf])
                Prob.append(JFEdicFRONT[jf])
                Prob.append(JFEMTM[jf])                     #SafexMTM
                Prob.append(JFEFAMTM[jf])                   #FAMTM
                GlobalReconDiff.append(Prob)
                
        else:
            Fail=[]
            Fail.append(jf)
            Fail.append(JFEdicSAFEX[jf])
            GlobalFail.append(Fail)
    
    dat = ael.date_today()
    
    outfile = Server + '\\ReconReport\\' + 'Recon' + dat.to_string('%Y%m%d') + '.csv'
    
    report = open(outfile, 'w')
    
    Blank = []
    Headers1 = ['Instrument', 'SafexPos', 'FrontPos', 'SafexMTMPrice', 'FrontArenaMTM']
    Headers1i = ['Instrument reconciled incorrectly Instrument reconciled incorrectly Instrument reconciled incorrectly Instrument reconciled incorrectly']
    Headers2 = ['Instrument', 'SafexPos', 'FrontPos', 'SafexMTMPrice', 'FrontArenaMTM']
    Headers2i = ['Instrument reconciled correctly Instrument reconciled correctly Instrument reconciled correctly Instrument reconciled correctly'] 
    Headers3 = ['LineNbr', 'Instrument']
    Headers3i = ['Instrument does not exist in Front Arena Instrument does not exist in Front Arena Instrument does not exist in Front Arena']
    Headers4 = ['Instrument', 'SafexPos']
    Headers4i = ['Instrument do not have any trades Instrument do not have any trades Instrument do not have any trades Instrument do not have any trades'] 
    
    for i in Headers1i:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for i in Headers1:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for ls in GlobalReconDiff:
        for f in ls:    
            report.write((str)(f))
            report.write(',')
        report.write('\n')
    
    for i in Blank:
    
        report.write(i)
        report.write(',')
    report.write('\n')
    
    for i in Headers2i:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for i in Headers2:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for ls in GlobalCorrect:
        for f in ls:    
            report.write((str)(f))
            report.write(',')
        report.write('\n')
        
    for i in Blank:
    
        report.write(i)
        report.write(',')
    report.write('\n')
    
    for i in Headers3i:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for i in Headers3:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for ls in GlobalNotInFA:
        for f in ls:    
            report.write((str)(f))
            report.write(',')
        report.write('\n')
        
    for i in Blank:
    
        report.write(i)
        report.write(',')
    report.write('\n')
    
    for i in Headers4i:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for i in Headers4:
    
        report.write((str)(i))
        report.write(',')
    report.write('\n')
    
    for ls in GlobalFail:
        for f in ls:    
            report.write((str)(f))
            report.write(',')
        report.write('\n')
    
    report.close()
    
    print 'The file has been saved at' +  Server + '\\ReconReport\\' + 'Recon' + dat.to_string('%Y%m%d') + '.csv'

    return 'Success'




