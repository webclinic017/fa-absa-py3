'''
Purpose                 :[Market Risk feed files, added string "nan" for exception handling],[Updated StrikePriceVAL]
Department and Desk     :[IT],[MR]
Requester:              :[Natalie Austin],[Susan Kruger]
Developer               :[Douglas Finkel],[Willie van der Bank]
CR Number               :[264536, 686048],[824244 11/11/2011]

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

    Instrument = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG             =       'BAS'
        HeaderName          =       'EuroDollar Future'
        OBJECT              =       'EuroDollar FutureSPEC'
        TYPE                =       'EuroDollar Future'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)

        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        ContractSizeVAL     =       '1'
        
        NotionalCAL         =       ''
        NotionalDAYC        =       ''
        NotionalFUNC        =       ''
        NotionalPERD        =       ''
        NotionalUNIT        =       i.curr.insid
        NotionalVAL         =       i.contr_size #Trade.Quantity()
        NotionalSTRG        =       ''
        
        MaturityDATE        =       MR_MainFunctions.Datefix(str(Instrument.ExpiryDateOnly()))
        
        
        
        UndrMaturityDATE    =      MR_MainFunctions.Datefix(str(i.exp_day.add_period(i.und_insaddr.exp_period)))
        
        
        
        NetBasisCAL         =       ''
        NetBasisDAYC        =       ''
        NetBasisFUNC        =       ''
        NetBasisPERD        =       ''
        NetBasisUNIT        =       ''
        NetBasisVAL         =       ''
        NetBasisSTRG        =       ''
        
        DaycountBasisCAL    =       ''
        DaycountBasisDAYC   =       ''

        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       ''
        SpotPriceVAL        =       ''
        SpotPriceSTRG       =       ''
        
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        StrikePriceFUNC     =       ''
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       Instrument.StrikePriceCurrency().Name()

        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = Instrument.Calculation()
        TheoPrice = calc.TheoreticalPrice(cs)
        
        if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
            StrikePriceVAL      = ''
        else:
            for p in i.historical_prices():
                if p.ptynbr.ptyid in ('SPOT', 'internal') and p.day == i.historical_prices()[len(i.historical_prices()) - 1].day:
                    StrikePriceVAL      = p.settle

        StrikePriceSTRG     =       ''
       
        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        except:
            try:
                DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
            except:
                DiscountCurveXREF   =       ''
        
        TheoModelXREF       =       'EuroDollar Future'
        
        MarketModelXREF     =       ''
        
        FairValueModelXREF  =       ''
        
        SettlementTYPE      =       ''
        
        SettlementProcFUNC  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                      %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL,
                        NotionalCAL, NotionalDAYC, NotionalFUNC, NotionalPERD, NotionalUNIT, NotionalVAL, NotionalSTRG, MaturityDATE, UndrMaturityDATE,
                        NetBasisCAL, NetBasisDAYC, NetBasisFUNC, NetBasisPERD, NetBasisUNIT, NetBasisVAL, NetBasisSTRG, DaycountBasisCAL, DaycountBasisDAYC,
                        SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, StrikePriceCAL, StrikePriceDAYC,
                        StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, DiscountCurveXREF, TheoModelXREF,
                        MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))

        outfile.close()
        
        
        #Position
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################




