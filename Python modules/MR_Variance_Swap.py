
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
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    for trades in i.trades():
        if MR_MainFunctions.ValidTradeNo(trades) == 0:
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                if (trades.trdnbr) not in InsL:
                    InsL.append(trades.trdnbr)
                    
                    outfile = open(filename, 'a')
                    #Base record
                    
                    BASFLAG                 =       'BAS'
                    HeaderName              =       'Variance Swap'
                    OBJECT                  =       'Variance SwapSPEC'
                    TYPE                    =       'Variance Swap'
                    
                    NAME                    =       i.insid + '_' + str(trades.trdnbr)
                    IDENTIFIER              =       'insaddr_'+str(i.insaddr) + '_' + str(trades.trdnbr)
                    
                    AnnlztFctrNB            =       ''
                    AvgSoFarCAL             =       ''
                    AvgSoFarDAYC            =       ''
                    AvgSoFarFUNC            =       '@GD2 historical volatility'
                    AvgSoFarPERD            =       ''
                    AvgSoFarUNIT            =       ''
                    AvgSoFarVAL             =       ''
                    AvgSoFarSTRG            =       ''
                    AvgStartDateDATE        =       MR_MainFunctions.Datefix(ael.date_today())
                    
                    for ExoticEvent in ins.ExoticEvents():
                        if AvgStartDateDATE >= MR_MainFunctions.Datefix(ExoticEvent.Date()):
                            AvgStartDateDATE = MR_MainFunctions.Datefix(ExoticEvent.Date())
                    
                    BusDayRuleRULE          =       'Following'
                    BusDayRuleBUSD          =       ''
                    BusDayRuleCONV          =       'Modified'
                    BusDayRuleCAL           =       ''
                    
                    CurrencyCAL             =       ''
                    CurrencyDAYC            =       ''
                    CurrencyPERD            =       ''
                    CurrencyUNIT            =       i.curr.insid
                    
                    DnmntrAdjstmFLAG        =       ''

                    DiscountCurveXREF   =       ins.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
                    
                    FixedTodayFLAG          =       ''
                    FixingRuleENUM          =       'Fixing Dates'
                    HistoricalCrvXREF       =       str(i.und_insaddr.insid) + '_HistoricalCurve'
                    
                    MaturityDATE            =       MR_MainFunctions.Datefix(i.exp_day)
                    
                    NotionalCAL             =       ''
                    NotionalDAYC            =       ''
                    NotionalFUNC            =       ''
                    NotionalPERD            =       ''
                    NotionalSTRG            =       ''
                    NotionalUNIT            =       i.curr.insid
                    NotionalVAL             =       i.contr_size
                    
                    NumofFixiDateNB         =       ''
                    
                    StlmntDayRuleBUSD       =       ''
                    StlmntDayRuleCAL        =       ''
                    StlmntDayRuleCONV       =       ''
                    StlmntDayRuleRULE       =       ''
                    SettlementProcFUNC      =       ''
                    SettlementTYPE          =       'Cash Settlement'
                    
                    StrikePriceCAL          =       ''
                    StrikePriceDAYC         =       ''
                    StrikePriceFUNC         =       ''
                    StrikePricePERD         =       ''
                    StrikePriceUNIT         =       i.curr.insid
                    
                    trade = acm.FTrade[trades.trdnbr]
                    StrikePriceVAL          =       trade.VolatilityStrike() / 100
                    StrikePriceSTRG         =       ''
                    
                    UnderlyingXREF          =       'insaddr_'+str(i.und_insaddr.insaddr)
                    
                    VolatilityCAL           =       ''
                    VolatilityDAYC          =       ''
                    VolatilityFUNC          =       ''
                    VolatilityPERD          =       ''
                    VolatilityUNIT          =       ''
                    VolatilityVAL           =       ''
                    VolatilitySTRG          =       ''
                    
                    #VolSurfaceXREF          =       ins.MappedVolatilityStructure().ParameterName() 
                    VolSurfaceXREF          =       ins.MappedVolatilityLink().LinkName()
                    
                    VrncNtnlCAL             =       ''
                    VrncNtnlDAYC            =       ''
                    VrncNtnlFUNC            =       '' #'@GD2 variance notional'
                    VrncNtnlPERD            =       ''
                    VrncNtnlSTRG            =       ''
                    VrncNtnlUNIT            =       i.curr.insid
                    VrncNtnlVAL             =       '10000'
                    
                    TheoModelXREF           =       'Variance Swap THEO'
                    MarketModelXREF         =       ''
                    
                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, AnnlztFctrNB, AvgSoFarCAL, AvgSoFarDAYC, AvgSoFarFUNC, AvgSoFarPERD, AvgSoFarUNIT, AvgSoFarVAL, AvgSoFarSTRG, AvgStartDateDATE, BusDayRuleRULE, BusDayRuleBUSD, BusDayRuleCONV, BusDayRuleCAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DnmntrAdjstmFLAG, DiscountCurveXREF, FixedTodayFLAG, FixingRuleENUM, HistoricalCrvXREF, MaturityDATE, NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalSTRG, NotionalUNIT, NotionalVAL, NumofFixiDateNB, StlmntDayRuleBUSD, StlmntDayRuleCAL, StlmntDayRuleCONV, StlmntDayRuleRULE, SettlementProcFUNC, SettlementTYPE, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, UnderlyingXREF, VolatilityCAL, VolatilityDAYC, VolatilityFUNC, VolatilityPERD, VolatilityUNIT, VolatilityVAL, VolatilitySTRG, VolSurfaceXREF, VrncNtnlCAL, VrncNtnlDAYC, VrncNtnlFUNC, VrncNtnlPERD, VrncNtnlSTRG, VrncNtnlUNIT, VrncNtnlVAL, TheoModelXREF, MarketModelXREF))
                    
                    # Roll Over Fixing dates
                    BASFLAG             =       'rm_ro'
                    HeaderName          =       'Variance Swap : Fixing Dates'
                    ATTRIBUTE           =       'Fixing Dates'
                    OBJECT              =       'Variance SwapSPEC'

                    for ExoticEvent in ins.ExoticEvents():
                        #if ExoticEvent.Date() >= acm.Time().DateToday():
                        FixingDatesDATE     =       MR_MainFunctions.Datefix(ExoticEvent.Date())

                        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FixingDatesDATE))
                    
                    outfile.close()

    for trades in i.trades():
        if MR_MainFunctions.ValidTradeNo(trades) == 0:
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                PositionFile.CreatePositionFwds(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

