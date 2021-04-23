'''
Purpose                 :[Market Risk feed files],[Updated DiscountCurveXREF]
Department and Desk     :[IT],[IT]
Requester:              :[Natalie Austin],[Jacqueline Calitz]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536],[2013-01-18 732053]
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
    #PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    #outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    #outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    #PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Foreign Exchange'
        OBJECT                  =       'Foreign ExchangeSPEC'
        TYPE                    =       'Foreign Exchange'
        NAME                	=       str(MR_MainFunctions.NameFix(i.insid))+'_MIDAS'
        IDENTIFIER          	=       str(MR_MainFunctions.NameFix(i.insid))+'_MIDAS'
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        CurrencyUNIT            =       'ZAR'
        
        ForeignCurrCAL          =       ''
        ForeignCurrDAYC         =       ''
        ForeignCurrPERD         =       ''
        ForeignCurrUNIT         =       i.curr.insid
        
        DiscountCurveXREF        =       'ZAR-SWAP'
        
        if (ins.Currency().MappedRepoLink(ins.Currency()).MappedInContext()):
            ForeignCurveXREF    =       ins.Currency().MappedRepoLink(ins.Currency()).LinkName()
        else:
            try:
                ForeignCurveXREF    =       ins.MappedRepoLink(ins.Currency()).Value().Link().YieldCurveComponent().Curve().Name()
            except:
                ForeignCurveXREF    =       ins.MappedRepoLink(ins.Currency()).Value().Link().YieldCurveComponent().Name()

        if i.curr.insid not in AllMappings:
        #if ForeignCurveXREF in ('DEFAULT','ZAR-SWAP'):
            ForeignCurveXREF = i.curr.insid + '_DiscountCurve'
        
        FwdCalibCrvXREF         =       ''
        
        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       i.curr.insid
        SpotPriceVAL            =       ''
        SpotPriceSTRG           =       ''
        
        TradeDayRuleRULE        =       ''
        TradeDayRuleBUSD        =       ''
        TradeDayRuleCONV        =       ''
        TradeDayRuleCAL         =       ''
                
        TheoModelXREF           =       'Currency'
        MarketModelXREF         =       'Spot Price'

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ForeignCurrCAL, ForeignCurrDAYC, ForeignCurrPERD, ForeignCurrUNIT, DiscountCurveXREF, ForeignCurveXREF, FwdCalibCrvXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, TheoModelXREF, MarketModelXREF))

        outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################


