'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 686048

Description             :Added string "nan" for exception handling

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-490
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''


import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
yesterday = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)


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


def get_YMtM(i, *rest):
    calc = i.Calculation()    
    Value = calc.MarketPrice(cs, yesterday, True, acm.FInstrument[i.Currency().Name()], False, acm.FParty['internal'], True).Value()
    return Value


# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
        
    ins = acm.FInstrument[i.insaddr]
    inscurr = acm.FInstrument[i.curr.insaddr]
    FX_NDF_Flag = str(ins.IsFxNdf())
    
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL and FX_NDF_Flag == 'False':
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'FX Futures'
        OBJECT                  =       'Forex FutureSPEC'
        TYPE                    =       'Forex Future'
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        ContractSizeVAL     =       ''
        if i.quote_type == 'Per 100 Units':
            ContractSizeVAL     = i.contr_size/100
        else:
            ContractSizeVAL     = i.contr_size

        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        CurrencyUNIT            =       i.curr.insid
        
        MaturityDATE            =       MR_MainFunctions.Datefix(i.exp_day)
        
        UnderlyingXREF          =       'insaddr_'+str(i.und_insaddr.insaddr)
        
        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       i.curr.insid
        SpotPriceVAL            =       ''
        SpotPriceSTRG           =       ''
            
        StrikePriceCAL          =       ''
        StrikePriceDAYC         =       ''
        StrikePriceFUNC         =       ''
        StrikePricePERD         =       ''
        StrikePriceUNIT         =       i.curr.insid

        StrikePriceVAL          =       ''        
        ymtm = get_YMtM(ins).Number()
        if str(ymtm) in ('1.#QNAN', 'NaN', 'nan'):
            StrikePriceVAL            = ''
        else:
            StrikePriceVAL            = get_YMtM(ins).Number()
        
        StrikePriceSTRG         =       ''
        
        RM_MapProcFUNC          =       ''
        
        NetBasisCAL             =       ''   
        NetBasisDAYC            =       ''
        NetBasisFUNC            =       ''
        NetBasisPERD            =       ''
        NetBasisUNIT            =       ''
        NetBasisVAL             =       ''
        NetBasisSTRG            =       ''
        
        DiscountCurveXREF   =       inscurr.MappedRepoLink(i.curr.insid).Value().Link().YieldCurveComponent().Curve().Name()

        TheoModelXREF           =       'FX Future THEO'
        MarketModelXREF         =       ''
        FairValueModelXREF      =       ''
        SettlementTYPE          =       ''
        SettlementProcFUNC      =       ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, ContractSizeVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, MaturityDATE, UnderlyingXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, RM_MapProcFUNC, NetBasisCAL, NetBasisDAYC, NetBasisFUNC, NetBasisPERD, NetBasisUNIT, NetBasisVAL, NetBasisSTRG, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
        
        outfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

