import ael, string, operator, SAEQ_DivType

def CalibrateDivTypes(divEst):
    return SAEQ_DivType.CalibrateDivTypes(divEst)

def Index(INDEXFILE):
    Index=[]
    
    fIndexInput = open(INDEXFILE, 'r')
    tmpStr = fIndexInput.readline()
    while tmpStr != "":
        for tmpIndex in tmpStr.split(','):
            Index.append(tmpIndex)
        tmpStr = fIndexInput.readline()
        
    Index.sort()
    fIndexInput.close()
    
    return Index

def Simulator(OUTPUTDIR, INDEXFILE):
    Global=[]

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
    
    outfile = OUTPUTDIR + 'SAEQ_MEIndexDivs_' + StartDate.to_string('%y%m%d') + '.txt'
    
    report = open(outfile, 'w')
    
    for lsts in Global:

        for ls in lsts:
            
            report.write((str)(ls))
            report.write(';')
        report.write('\n')

    report.close()
    
    print'Success'
    print 'The file has been saved as ' + outfile
    return
