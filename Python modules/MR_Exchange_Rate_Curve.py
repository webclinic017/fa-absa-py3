'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :275268

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003500355   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-461
'''

import ael, string, acm, MR_MainFunctions

global outputList
outputList = []
InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename            = FileDir + Filename

    del InsL[:]
    InsL[:] = []  

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(temp,p,FileDir,Filename,*rest):
    global outputList
    outputTuple = ()
    
    ins = acm.FInstrument[p.insaddr.insaddr]
    currins = acm.FInstrument[p.curr.insaddr]
    
    if (p.insaddr.insid + '/' + p.curr.insid + '_IP') not in InsL:
        InsL.append(p.insaddr.insid + '/' + p.curr.insid + '_IP')

        #Foreign Exchange instrument to handle 2 day settlement rule for FX prices
        BASFLAG                 =       'BAS'
        HeaderName              =       'Foreign Exchange'
        OBJECT                  =       'Foreign ExchangeSPEC'
        TYPE                    =       'Foreign Exchange'
        NAME                    =       p.insaddr.insid + '/' + p.curr.insid + '_IP_Spot'
        IDENTIFIER              =       p.insaddr.insid + '/' + p.curr.insid + '_IP_Spot'     
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        
        CurrencyUNIT            =       p.curr.insid
        
        ForeignCurrCAL          =       ''
        ForeignCurrDAYC         =       ''
        ForeignCurrPERD         =       ''
        ForeignCurrUNIT         =       p.insaddr.insid
        
        DiscountCurveXREF       =       MR_MainFunctions.NameFix(currins.MappedRepoLink(currins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        ForeignCurveXREF        =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        FwdCalibCrvXREF         =       ''
        
        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       p.curr.insid
        SpotPriceVAL            =       p.last
        SpotPriceSTRG           =       ''
        
        TradeDayRuleRULE        =       'Following'
        TradeDayRuleBUSD        =       '2'
        TradeDayRuleCONV        =       'Regular'
        TradeDayRuleCAL         =       'Weekends'
        
        TheoModelXREF           =       'Spot Price'
        MarketModelXREF         =       'Spot Price'
        
        outputSet1 = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ForeignCurrCAL, ForeignCurrDAYC, ForeignCurrPERD, ForeignCurrUNIT, DiscountCurveXREF, ForeignCurveXREF, FwdCalibCrvXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TradeDayRuleRULE, TradeDayRuleBUSD, TradeDayRuleCONV, TradeDayRuleCAL, TheoModelXREF, MarketModelXREF)
        
        #Base record
        BAS                     =       'BAS'
        Exchange_RateSPEC       =       'Exchange RateSPEC'
        OBJECT                  =       'Exchange RateSPEC'
        TYPE                    =       'Exchange Rate'
        IDENTIFIER              =       p.insaddr.insid + '/' + p.curr.insid + '_IP'
        
        NAME                    =       p.insaddr.insid + '/' + p.curr.insid + '_IP'
        
        ActiveFLAG              =       'TRUE'
        CurveFUNC               =       ''
        CurveUnitCAL            =       ''
        
        CurveUnitDAYC           =       MR_MainFunctions.DayCountFix('Act/365')
        
        CurveUnitPERD           =       'annual'
        CurveUnitUNIT           =       '%'
        DatumDATE               =       MR_MainFunctions.Datefix(acm.Time().DateNow())
        OriginOffsetNB          =       '0'
        
        RelativeCurveFLAG       =       'TRUE'
        StateProcFUNC           =       '@spot rate'
        TimeEvolutionFUNC       =       '@Interest Rate Parity'
        FunctionIdFLAG          =       'TRUE'
        GenExRatSfExt0FLAG      =       'TRUE'
        GenExchRtSfNod0SIN      =       '@CubicSpline'
        XchDomstcCrvXREF        =       MR_MainFunctions.NameFix(currins.MappedRepoLink(currins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        ExchForgnCrvXREF        =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        
        outputSet2 = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS, Exchange_RateSPEC, OBJECT, TYPE, IDENTIFIER, NAME, ActiveFLAG, CurveFUNC, CurveUnitCAL, CurveUnitDAYC, CurveUnitPERD, CurveUnitUNIT, DatumDATE, OriginOffsetNB, RelativeCurveFLAG, StateProcFUNC, TimeEvolutionFUNC, FunctionIdFLAG, GenExRatSfExt0FLAG, GenExchRtSfNod0SIN, XchDomstcCrvXREF, ExchForgnCrvXREF)
        
        # Roll Over Generic Zero Surface - price input only to cover case where FX instrument fails to load
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Exchange RateSPEC : Generic Exchange Rate Surface'
        ATTRIBUTE           =       'Generic Exchange Rate Surface'
        OBJECT              =       'Exchange RateSPEC'
        
        GenExchRtSfNod0AXS      =  0
        GenExchRtSfNodNODE      =      p.last
        
        outputSet3 = '%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, GenExchRtSfNod0AXS, GenExchRtSfNodNODE)
        
        # Roll Over Function Parameters
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Exchange RateSPEC : Function Parameters'
        ATTRIBUTE           =       'Function Parameters'
        OBJECT              =       'Exchange RateSPEC'
        FunctionParamsVAL   =       ''
        
        outputSet4 = None
        if FunctionParamsVAL  != '':
            outputSet4 = '%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, FunctionParamsVAL)
        
        # Roll Over Procedure Parameters - FX Spot mapped as input into curve
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Exchange RateSPEC : Procedure Parameter'
        ATTRIBUTE           =       'Procedure Parameter'
        OBJECT              =       'Exchange RateSPEC'
        ProcedureParamXREF  =       p.insaddr.insid + '/' + p.curr.insid + '_IP_Spot'  
        
        outputSet5 = None
        if ProcedureParamXREF  != '':
            outputSet5 = '%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ProcedureParamXREF)
        
        outputTuple = (outputSet1, outputSet2, outputSet3, outputSet4, outputSet5)
        outputList.append(outputTuple)

    return str(p.prinbr)

# WRITE - FILE ######################################################################################################

def WriteOutput(temp,FileDir,Filename,*rest):
    global outputList
    filename = FileDir + Filename
    
    outfile =  open(filename, 'w')

    for outputTuple in outputList:
        for outputItem in outputTuple:
            if outputItem != None:
                outfile.write(outputItem)
    
    outfile.close()
    return 'Successful'
