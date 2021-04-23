'''
Purpose                 :[Market Risk feed files], [Updated DiscountCurveXREF]
Department and Desk     :[IT],[IT]
Requester:              :[Natalie Austin],[Jacqueline Calitz]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536,275268],[2013-01-18 732053]

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

def RepoMappings():
    allNames = []
    
    for l in ael.Context['ACMB Global'].links():
        if l.type in ('Repo') and l.mapping_type == 'Instrument':
            try:
                InsID = l.insaddr.insid
                allNames.append(InsID)
            except:
                a = 1
    #allNames.sort()
    return allNames

AllMappings = RepoMappings()

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

def Write(t,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    Instrument = acm.FInstrument[t.insaddr.insid]
    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    FX_NDF_Flag = str(Instrument.IsFxNdf())

    if MR_MainFunctions.IsExcludedPortfolio(t) == False:
        if (t.trdnbr) not in InsL and FX_NDF_Flag == 'False':
            InsL.append(t.trdnbr)

            outfile = open(filename, 'a')
            #Base record
            
            BASFLAG             =       'BAS'
            HeaderName          =       'FX Forward'
            OBJECT              =       'Forex ForwardSPEC'
            TYPE                =       'Forex Forward'    

            NAME                =       str(t.insaddr.instype) + '_' + MR_MainFunctions.NameFix(str(t.insaddr.curr.insid))+ '_' + MR_MainFunctions.NameFix(str(t.curr.insid))+ '_' + str(t.value_day)+ '_' + str(t.trdnbr)
            IDENTIFIER          =       'insaddr_'+str(t.insaddr.insaddr)+'_'+str(t.trdnbr)

            CurrencyCAL         =       ''
            CurrencyDAYC        =       ''
            CurrencyPERD        =       ''
            CurrencyUNIT        =       t.curr.insid
            
            MaturityDATE        =       MR_MainFunctions.Datefix(str(t.value_day))
            
            UnderlyingXREF      =       'insaddr_' + str(t.insaddr.insaddr) #'insaddr_'+str(t.insaddr.und_insaddr.insaddr) Dont change
            
            StrikePriceCAL      =       ''
            StrikePriceDAYC     =       ''
            StrikePriceFUNC     =       ''
            StrikePricePERD     =       ''
            StrikePriceUNIT     =       t.curr.insid
            StrikePriceVAL      =       t.price
            StrikePriceSTRG     =       ''
            
            RM_MapProcFUNC      =       ''    
            
            try:
                DiscountCurveXREF   =       Trade.Currency().MappedRepoLink(t.curr.insid).Value().Link().YieldCurveComponent().Curve().Name()
            except:
                DiscountCurveXREF   =       Trade.Currency().MappedRepoLink(t.curr.insid).Value().Link().YieldCurveComponent().Name()
            
            if t.curr.insid not in AllMappings:
                DiscountCurveXREF = t.curr.insid + '_DiscountCurve'
            
            #if DiscountCurveXREF == 'DEFAULT':
            #    DiscountCurveXREF = t.insaddr.curr.insid + '_DiscountCurve'
            
            TheoModelXREF       =       'FX Forward IP'
            
            MarketModelXREF     =       ''
            FairValueModelXREF  =       ''
            SettlementTYPE      =       ''
            SettlementProcFUNC  =       ''
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                          %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, MaturityDATE, UnderlyingXREF, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, RM_MapProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
            
            outfile.close()
            
            #Position
            if MR_MainFunctions.ValidTradeNo(t) == 0:
                PositionFile.CreatePositionFX(t, PositionFilename)

    return t.insaddr.insid

# WRITE - FILE ######################################################################################################

