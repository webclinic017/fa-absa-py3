import ael, string, acm, PositionFile, MR_MainFunctions


'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :278978
'''

'''
Purpose                 :Check the length of the currency instruments coming through.
Department and Desk     :IT
Requester:              :Susan Kruger
Developer               :Heinrich Cronje
CR Number               :CHNG0000729822
'''

InsL = []



# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()
    
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if ((i.curr.insid) not in InsL) and len(i.curr.insid) < 5:
        InsL.append(i.curr.insid)

        #Base record
        outfile = open(filename, 'a')
        
        BASFLAG                 =       'BAS'
        HeaderName	        =       'Cash Instrument'
        OBJECT	                =       'Cash InstrumentSPEC'
        TYPE	                =       'Cash Instrument'
        NAME	                =       MR_MainFunctions.NameFix(str(i.curr.insid))+'_Cash'
        IDENTIFIER	        =       MR_MainFunctions.NameFix(str(i.curr.insid))+'_Cash'
        CurrencyCAL	        =       ''
        CurrencyDAYC	        =       ''
        CurrencyPERD	        =       ''
        CurrencyUNIT	        =       MR_MainFunctions.NameFix(i.curr.insid)
        
        BorrowCurveXREF	        =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        LendingCurveXREF	=       BorrowCurveXREF
        
        #DiscountCurveXREF       =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        if ins.MappedMoneyMarketLink():
            DiscountCurveXREF       =       MR_MainFunctions.NameFix(ins.MappedMoneyMarketLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        else:
            DiscountCurveXREF       =       MR_MainFunctions.NameFix(ins.Currency().MappedMoneyMarketLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        TheoModelXREF	        =       'ZAR Cash Account'
        MarketModelXREF	        =       'ZAR Cash Account'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, BorrowCurveXREF, LendingCurveXREF, DiscountCurveXREF, TheoModelXREF, MarketModelXREF))
        
        outfile.close()

#       The position file is created through ASQL using the PositionFile.CreatePositionCash        
#        for trades in i.trades():
#            if MR_MainFunctions.ValidTradeNo(trades) == 0:
#                PositionFile.CreatePositionCash(trades,PositionFilename)
    
    return str(i.insid)

# WRITE - FILE ######################################################################################################



