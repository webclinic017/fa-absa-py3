
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT, Market Risk
Requester:              :Natalie Austin, Susan Kruger
Developer               :Douglas Finkel, Heinrich Cronje
CR Number               :264536, 275268, 278978, 686048, 891943

Description             :Added string "nan" for exception handling
                        :891943: Added logic for UnderlyingXREF for future paying ETF Future/Forward

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
2021-03-11     CHG0158547       Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/FAFO-41 
'''


import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
yesterday = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
    
    outfile = open(filename, 'w')
    outfileP = open(PositionFilename, 'w')
    
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

def Write(i,FileDir,Filename,PositionName,TradeFilter,*rest):
    
    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
        
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
        #Base record

        BASFLAG = 'BAS'
        HeaderName = 'Commodity Future'
        OBJECT = 'Equity FutureSPEC'
        TYPE = 'Equity Future'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)

        ContractSizeVAL = i.contr_size

        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = i.curr.insid

        DiscountCurveXREF = ins.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

        ForwardCurveXREF = ''

        MaturityDATE = MR_MainFunctions.Datefix(i.exp_day)

        if i.und_insaddr:
            UnderlyingXREF = 'insaddr_'+str(i.und_insaddr.insaddr)
            
        SettlementProcFUNC = ''
        SettlementTYPE = ''
        SpotPriceCAL = ''
        SpotPriceDAYC = ''
        SpotPriceFUNC = ''
        SpotPricePERD = ''
        SpotPriceUNIT = ''
        SpotPriceVAL = ''
        SpotPriceSTRG = ''
        StrikePriceCAL = ''
        StrikePriceDAYC = ''
        StrikePriceFUNC = ''
        StrikePricePERD = ''
        StrikePriceUNIT = i.curr.insid
        
        ymtm = get_YMtM(ins).Number()
        
        if str(ymtm) in ('1.#QNAN', 'NaN', 'nan'):
            StrikePriceVAL = ''
        else:
            if i.und_insaddr.quote_type == 'Per 100 Units':
                StrikePriceVAL = get_YMtM(ins).Number() / 100
            else:
                StrikePriceVAL = get_YMtM(ins).Number()
        

        StrikePriceSTRG = '' 
        TheoModelXREF = 'Equity/Commodity Future THEO'
        MarketModelXREF = ''
        FairValueModelXREF = ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, ContractSizeVAL, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, ForwardCurveXREF, MaturityDATE, UnderlyingXREF, SettlementProcFUNC, SettlementTYPE, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        outfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades, TradeFilter) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid


