'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :290307

Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :278978

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
2020-09-30     CHG0131147       Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/CMRI-707
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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')
	#Base record

        BASFLAG	        =	'BAS'
        HeaderName	=	'Bond Future'
        OBJECT	        =	'Bond FutureSPEC'
        TYPE	        =	'Bond Future'
        
        NAME            =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER      =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL	=	''
        CurrencyDAYC	=	''
        CurrencyPERD	=	''
        CurrencyUNIT	=	i.curr.insid
        ContractSizeVAL =       0
        
        try:
            ContractSizeVAL =	i.contr_size/i.und_insaddr.contr_size
        except:
            ContractSizeVAL =	0
        
        MaturityDATE    =	MR_MainFunctions.Datefix(i.exp_day)
        
        UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
        NetBasisCAL         =       ''
        NetBasisDAYC        =       ''
        if i.curr.insid == 'USD':
            NetBasisFUNC        =       '@net basis THEO'
        else:
            NetBasisFUNC        =       '@net basis MKT'
        NetBasisPERD        =       ''
        NetBasisUNIT        =       '$'
        NetBasisVAL         =       ''
        NetBasisSTRG        =       ''
        SpotPriceCAL        =       ''
        SpotPriceDAYC       =       ''
        SpotPriceFUNC       =       ''#'@spot price given yield SA'
        SpotPricePERD       =       ''
        SpotPriceUNIT       =       '$'
        SpotPriceVAL        =       ''
        SpotPriceSTRG       =       ''
        
        SpotPric_YieCAL     =       ''
        StriPric_YieDAYC    =       ''
        SpotPric_YiePERD    =       ''
        StriPric_YiePERD    =       ''
        
        Legs = i.legs()		
        for LegNbr in Legs:	
            SpotPric_YieCAL =       MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
            StriPric_YieDAYC =      MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
            
            if LegNbr.rolling_period=='1m':
                SpotPric_YiePERD='monthly'
                StriPric_YiePERD='monthly'
            elif LegNbr.rolling_period=='6m':
                SpotPric_YiePERD='semi-annual'
                StriPric_YiePERD='semi-annual'
            elif LegNbr.rolling_period=='3m':
                SpotPric_YiePERD='3monthly'
                StriPric_YiePERD='3monthly'
            elif LegNbr.rolling_period=='12m':
                SpotPric_YiePERD='annual'
                StriPric_YiePERD='annual'
            elif LegNbr.rolling_period=='1y':
                SpotPric_YiePERD='annual'
                StriPric_YiePERD='annual'
            elif LegNbr.rolling_period=='0d':
                SpotPric_YiePERD='0d'
                StriPric_YiePERD='0d'
            else:
                SpotPric_YiePERD='other1'
                StriPric_YiePERD='other1'

        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = ins.Calculation()
        TheoPrice = calc.TheoreticalPrice(cs)
        Price = calc.MarketPrice(cs)
        
        SpotPric_YieDAYC    =       ''
        SpotPric_YieFUNC    =       ''
        SpotPric_YieUNIT    =       '%'
        SpotPric_YieVAL     =       ''#Price.Number()
        SpotPric_YieSTRG    =       ''
        StrikePriceCAL      =       ''
        StrikePriceDAYC     =       ''
        if i.curr.insid  ==  'USD':
            StrikePriceFUNC     =       ''
        else:
            StrikePriceFUNC     =       '@strike price given yield SA'
        StrikePricePERD     =       ''
        StrikePriceUNIT     =       '$'
        if i.curr.insid  ==  'USD':
            StrikePriceVAL      =       round(10000*Price.Number(), 0) #''
        else:
            StrikePriceVAL      =       ''
        StrikePriceSTRG     =       ''
        StriPric_YieCAL     =       ''

        StriPric_YieFUNC    =       ''

        StriPric_YieUNIT    =       '%'
        if i.curr.insid  ==  'USD':
            StriPric_YieVAL     =       ''
        else:
            StriPric_YieVAL     =       TheoPrice.Number()
        StriPric_YieSTRG    =       ''
        DiscountCurveXREF   =       MR_MainFunctions.NameFix(ins.Currency().MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        TheoModelXREF       =       'SA Bond Future'
        MarketModelXREF     =       'SA Bond Future'
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL, MaturityDATE, UnderlyingXREF, NetBasisCAL, NetBasisDAYC, NetBasisFUNC, NetBasisPERD, NetBasisUNIT, NetBasisVAL, NetBasisSTRG, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, SpotPric_YieCAL, SpotPric_YieDAYC, SpotPric_YieFUNC, SpotPric_YiePERD, SpotPric_YieUNIT, SpotPric_YieVAL, SpotPric_YieSTRG, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, StriPric_YieCAL, StriPric_YieDAYC, StriPric_YieFUNC, StriPric_YiePERD, StriPric_YieUNIT, StriPric_YieVAL, StriPric_YieSTRG, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        BASFLAG	        =       'rm_ro'
        HeaderName	=       'Bond Future : Underlying Financial Entities'
        ATTRIBUTE	=       'Underlying Financial Entities'
        OBJECT	        =       'Bond FutureSPEC'
        UndrFinEntitisXREF  =   str(i.und_insaddr.insid) # 'R153_INV'
        UndrFinEntitisSEQ   =   ''
        UndrFinEntitisSSEQ  =   ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF, UndrFinEntitisSEQ, UndrFinEntitisSSEQ))

        BASFLAG	        =       'rm_ro'
        HeaderName	=       'Bond Future : Component Weights'
        ATTRIBUTE	=       'Component Weights'
        OBJECT	        =       'Bond FutureSPEC'
        ComponentWghtVAL   =    '1'
        ComponentWghtSEQ   =    ''
        ComponentWghtSSEQ  =    ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL, ComponentWghtSEQ, ComponentWghtSSEQ))

        outfile.close()
    
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid
    
# WRITE - FILE ######################################################################################################

