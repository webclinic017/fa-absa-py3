import ael, string, operator


#General Utils
#-------------

def CalibrateDivTypes(divEst):
    divType = string.rstrip(string.lstrip(string.lower(divEst.description)))
    if divType in ("spec", "special", "s", "special div"):
        divType = "Special"
    elif divType in ("final", "f", "fin"):
        divType = "Final"
    elif divType in ("interim", "intrim", "i", "int"):
        divType = "Interim"
        
    if not divType in ("Final", "Special", "Interim"):
        divType = "Final_" + divType

    return divType

#Index Exporter
#--------------

def Index(IndexFile):
    Index=[]
    
    fIndexInput = open(IndexFile, 'r')
    tmpStr = fIndexInput.readline()
    while tmpStr != "":
        for tmpIndex in tmpStr.split(','):
            Index.append(tmpIndex)
        tmpStr = fIndexInput.readline()

    Index.sort()
    fIndexInput.close()

    return Index

def ExportEquityIndex(OUTPUTDIR, INDEXFILE):
    Global = []

    tmpIndex = Index(INDEXFILE)

    for i in tmpIndex:
        ins = ael.Instrument[i]
        link = ins.combination_links()
        
        for lnk in link.members():
            
            con = lnk.member_insaddr
                            
            strm = ael.DividendStream.select('insaddr = "%d"' %(lnk.member_insaddr.insaddr))
            
            for st in strm:
                
                for est in st.estimates():
                    
                    wght = lnk.weight
                    factor = ins.index_factor

                    if est.ex_div_day > ael.date_today():

                        if CalibrateDivTypes(est) <> "Special":
                            list=[]
                            
                            list.append(i)                                          #Index
                            list.append(est.ex_div_day)                             #ExDivDay
                            list.append(est.dividend*(wght/factor))                 #IndexPoints
                            list.append(est.pay_day)                                #PayDay
                            list.append(CalibrateDivTypes(est))                     #Type
                            list.append(con.insid)                                  #Constituent
                            
                            Global.append(list)
    
    Global.sort(lambda a, b: cmp(a[3], b[3]) )
    Global.sort(lambda a, b: cmp(a[1], b[1]) )
    Global.sort(lambda a, b: cmp(a[0], b[0]) )
    
    StartDate = ael.date_today()
    
    outfile = OUTPUTDIR + 'MEIndexDivs_' + StartDate.to_string('%y%m%d') + '.txt'
    
    report = open(outfile, 'w')
    
    for lsts in Global:

        for ls in lsts:
            
            report.write((str)(ls))
            report.write(';')
        report.write('\n')

    report.close()
    
    print 'The file has been saved as ' + outfile
    return

#SS Exporter
#-----------

def ExportSingleStockDiv(OutDir):
    GlobalDivs = []

    #Actual Dividends
    divs = ael.Dividend

    for d in divs:
        description = CalibrateDivTypes(d)

        if description not in ("Special", "Yield", "A"):
            list=[]
            list.append(d.insaddr.insid)
            list.append(d.ex_div_day.to_string('%Y-%m-%d'))
            list.append(d.dividend)
            list.append(d.pay_day.to_string('%Y-%m-%d'))
            list.append(description)
            
            if list != []:
                GlobalDivs.append(list)

    GlobalDivs.sort()
    
    #Dividend Estimates
    strm = ael.DividendStream.select()

    for st in strm.members():
        length = len(st.name)
        instr = st.insaddr.insid
        for est in st.estimates():
            list=[]
            
            description = CalibrateDivTypes(est)
            exdivday = est.ex_div_day

            if description not in ("Special", "Yield", "A") and exdivday > ael.date_today(): # Don't add special divs
                list.append(instr)
                list.append(exdivday.to_string('%Y-%m-%d'))
                list.append(est.dividend*100)
                list.append(est.pay_day.to_string('%Y-%m-%d'))
                list.append(CalibrateDivTypes(est))
            
                if list != []:
                    GlobalDivs.append(list)
                    
    #Sort and Export
    GlobalDivs.sort()

    dt = ael.date_today().to_string('%y%m%d')
    FileName = OutDir + "SSDivEstimates_" + dt + ".txt"

    Headers=[]
    Headers = ["Underlying", "ExDivDay", "Dividend", "PayDay", "DivType"]

    report = open(FileName, "w")
    try:
        for s in Headers:
            report.write((str)(s))
            report.write(';')
            
        report.write('\n')
            
        for lsts in GlobalDivs:
            for ls in lsts:
                report.write((str)(ls))
                report.write(';')
            report.write('\n')

	print "The file has been saved as " + FileName
    finally:
        report.close()
    
    return

#Top 40 Exporter
#---------------

def ExportTop40(OutputDir):
    ins = ael.Instrument["ZAR/ALSI"]
    dt = ael.date_today().to_string('%y%m%d')

    FileName = OutputDir + "JSETop40_" + dt + ".txt"
    
    fReport = open(FileName, "w")
    try:
        link = ins.combination_links()    
        for lnk in link.members():
            con = lnk.member_insaddr
            fReport.write(con.insid + "\n")

	print "The file has been saved as " + FileName
    finally:
        fReport.close()

    return

#RIC to Front Code Exporter
#--------------------------

def ExportRICToFrontMappings(OutputDir):
    InstrumentList = []

    #Add all instruments to our Instrument List which have a corresponding div stream
    strm = ael.DividendStream.select()
    for st in strm.members():
        InstrumentList.append(st.insaddr.insaddr)

    #Build RIC-Front Mappings
    ExportList = []
    for insaddr in InstrumentList:
        Instrument = ael.Instrument[insaddr]
        #Filter out unwanted divs by instrument name length
        if ((Instrument.instype == "Stock") and len(Instrument.insid) == 7):
            PriceDef = ael.PriceDefinition.select("insaddr = %d" % insaddr)
    
            for m in PriceDef.members():
                v = getattr(m, 'data[0]')
                ExportList.append([v.split(" ")[1], ael.Instrument[insaddr].insid])
    
    ExportList.sort()
    
    #Export To File
    dt = ael.date_today().to_string('%y%m%d')
    FileName = OutputDir + "SAEQ_RICToFrontMapping_" + dt + ".txt"
    report = open(FileName, "w")
    try:
        for lst in ExportList:
            report.write(lst[0] + "," + lst[1] + "\n")
        print "The file has been saved as " + FileName
    finally:
        report.close()
        
    return

#Main
#-----

ExportDir = "Y:\\Jhb\\SAEQ\\Data\\DataFromAbCapServer\\"

#Export Index Divs
ExportEquityIndex(ExportDir, "Y:\\Jhb\\SAEQ\\Data\\Settings\\Indeces.txt")

#Export Single Stock Divs
ExportSingleStockDiv(ExportDir)

#Export the constituents of ZAR/ALSI (Top 40)
ExportTop40(ExportDir)

#Export RIC to Front Code Mappings
ExportRICToFrontMappings(ExportDir)
