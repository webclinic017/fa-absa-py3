'''
Purpose                 :[Market Risk feed files],[Updated DiscountCurveXREF]
Department and Desk     :[IT],[IT]
Requester:              :[Natalie Austin],[Jacqueline Calitz]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536],[2013-01-18 732053]

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2018-11-01     CHG1001083227    Market RisK        Andile Biyana      http://abcap-jira/browse/ABITFA-5619
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
    
    outfile             =  open(filename, 'w')
    
    outfile.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename

    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Foreign Exchange'
        OBJECT                  =       'Foreign ExchangeSPEC'
        TYPE                    =       'Foreign Exchange'
        NAME                    =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER              =       'insaddr_'+str(i.insaddr)       
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''        
        CurrencyUNIT            =       'ZAR'        
        ForeignCurrCAL          =       ''
        ForeignCurrDAYC         =       ''
        ForeignCurrPERD         =       ''
        ForeignCurrUNIT         =       i.curr.insid
        
        DiscountCurveXREF       =       'ZAR-SWAP'
        
        if (ins.Currency().MappedRepoLink(ins.Currency()).MappedInContext()):
            ForeignCurveXREF    =       ins.Currency().MappedRepoLink(ins.Currency()).LinkName()
        else:
            try:
                ForeignCurveXREF    =       ins.MappedRepoLink(ins.Currency()).Value().Link().YieldCurveComponent().Curve().Name()
            except:
                ForeignCurveXREF    =       ins.MappedRepoLink(ins.Currency()).Value().Link().YieldCurveComponent().Name()
             
        if i.curr.insid not in AllMappings:        
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


def BaseCurr(Curr1, Curr2): 
    BASECURR = ['USD', 'GBP', 'EUR', 'ZAR']
    CurrL = []
    if Curr1 in BASECURR:
        CurrL.append(Curr1)
    if Curr2 in BASECURR:
        CurrL.append(Curr2)

    for Base in BASECURR:
        if Base not in CurrL:
            return Base
            break

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def FXRate(Lock, Reset, Base, date,*rest):    

    curr1 = acm.FCurrency[Reset]
    curr2 = acm.FCurrency[Lock]
    baseCurr = acm.FCurrency[Base]
    
    fxRateCurr1 = curr1.Calculation().FXRate( StandardCalcSpace.CALC_SPACE, baseCurr, date ).Number()
    fxRateCurr2 = baseCurr.Calculation().FXRate( StandardCalcSpace.CALC_SPACE, curr2, date ).Number()

    return fxRateCurr2 * fxRateCurr1
        

# WRITE2 - FILE ######################################################################################################

def Write2(temp,FileDir,Filename,PositionName,currpair,LockedLeg,ResetLeg,*rest):
    
    filename            = FileDir + Filename
    insLL = acm.FInstrument[LockedLeg]
    insRL = acm.FInstrument[ResetLeg]
    #Base record
    
    outfile = open(filename, 'a')
    
    BASFLAG                 =       'BAS'
    HeaderName              =       'Foreign Exchange'
    OBJECT                  =       'Foreign ExchangeSPEC'
    TYPE                    =       'Foreign Exchange'
    NAME                    =       str(currpair) + '_FX'
    IDENTIFIER              =       str(currpair) + '_FX'      
    CurrencyCAL             =       ''
    CurrencyDAYC            =       ''
    CurrencyPERD            =       ''
    CurrencyUNIT            =       insLL.Currency().Name()
    ForeignCurrCAL          =       ''
    ForeignCurrDAYC         =       ''
    ForeignCurrPERD         =       ''
    ForeignCurrUNIT         =       insRL.Currency().Name()    
    DiscountCurveXREF       =       insLL.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
    ForeignCurveXREF        =       insRL.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()                
    FwdCalibCrvXREF         =       ''
    SpotPriceCAL            =       ''
    SpotPriceDAYC           =       ''
    SpotPriceFUNC           =       ''
    SpotPricePERD           =       ''
    SpotPriceUNIT           =       insLL.Currency().Name()    
    RepDate = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
    Lock  = acm.FInstrument[LockedLeg]
    Reset = acm.FInstrument[ResetLeg]    
    Base = BaseCurr(Lock.Instrument().Name(), Reset.Instrument().Name())    
    SpotPriceVAL            =       FXRate(Lock.Instrument().Name(), Reset.Instrument().Name(), Base, RepDate.add_banking_day(ael.Instrument['ZAR'], 3))    
    SpotPriceSTRG           =       ''
    TradeDayRuleRULE        =       ''
    TradeDayRuleBUSD        =       ''
    TradeDayRuleCONV        =       ''
    TradeDayRuleCAL         =       ''
    TheoModelXREF           =       'Currency'
    MarketModelXREF         =       'Currency'
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ForeignCurrCAL, ForeignCurrDAYC, ForeignCurrPERD, ForeignCurrUNIT, DiscountCurveXREF, ForeignCurveXREF, FwdCalibCrvXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, TheoModelXREF, MarketModelXREF))
    
    outfile.close()

    return currpair

# WRITE2 - FILE ######################################################################################################
        
