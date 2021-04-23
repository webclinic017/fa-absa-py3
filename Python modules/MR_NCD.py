'''
Purpose                 :[Market Risk feed files],[Updated to cater for BulletBond NCDs]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel / Henk Nel],[Willie van der Bank]
CR Number               :[264536],[883286]

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

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
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        
        #Base record
        BASFLAG	        =	'BAS'
        HeaderName      =	'Bullet Bond'
        OBJECT	        =	'Bullet BondSPEC'
        TYPE	        =	'Bullet Bond'

        NAME            =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      =       'insaddr_' + str(i.insaddr)

        CurrencyCAL	=       ''
        CurrencyDAYC	=       ''
        CurrencyPERD	=       ''
        CurrencyUNIT	=       i.curr.insid
        
        NotionalCAL	=	''
        NotionalDAYC	=	''
        NotionalFUNC	=	''
        NotionalPERD	=	''
        NotionalUNIT	=	i.curr.insid
        NotionalVAL	=       i.contr_size
        NotionalSTRG	=       ''
                                
        MaturityDATE	=       MR_MainFunctions.Datefix(i.exp_day)
        IssueDATE       =       MR_MainFunctions.Datefix(i.legs()[0].start_day)

        CouponRateCAL	=	''
        CouponRateDAYC	=       MR_MainFunctions.DayCountFix(i.legs()[0].daycount_method)
        CouponRatePERD	=       'simple'
        CouponRateVAL	=       i.legs()[0].fixed_rate
        StateProcFUNC	=       '@cash flow generator'
        TermNB		=       ''
        TermUNIT	=       'Maturity'
        
        leg = acm.FLeg[i.legs()[0].legnbr]
        DiscountCurveXREF   =     MR_MainFunctions.NameFix(str(leg.MappedDiscountLink().Link()))
        
        TheoModelXREF       =     'Bullet Bond Model'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, IssueDATE, CouponRateCAL, CouponRateDAYC, CouponRatePERD, CouponRateVAL, StateProcFUNC, TermNB, TermUNIT, DiscountCurveXREF, TheoModelXREF))
        outfile.close()
        
        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


