'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536,290307,522873, 632975

Description             :Logic for Repo and Discount curves when the underlying is a 

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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        for trades in i.trades():
            if trades.value_day > ael.date_today() and trades.premium != 0:
                
                outfile = open(filename, 'a')
                #Base record
                
                BASFLAG	        =	'BAS'
                HeaderName	=	'Bond Forward'
                OBJECT	        =	'Bond ForwardSPEC'
                TYPE	        =	'Bond Forward'
                NAME            =       MR_MainFunctions.NameFix(i.insid) + '_' + MR_MainFunctions.Datefix(trades.value_day)
                IDENTIFIER      =       'insaddr_'+str(i.insaddr) + '_' + str(trades.trdnbr)
                CurrencyCAL	=	''
                CurrencyDAYC	=	''
                CurrencyPERD	=	''
                CurrencyUNIT	=	i.curr.insid
                
                if ins.Underlying():
                    ContractSizeVAL	=	ins.ContractSize() / ins.Underlying().ContractSize()
                else:
                    ContractSizeVAL	=	'1'
                
                MaturityDATE	=	MR_MainFunctions.Datefix(trades.value_day)
                StrikePriceDAYC	=	''
                StrikePricePERD     =       ''
                
                Legs = i.legs()		
                for LegNbr in Legs:		
                    
                    for cf in LegNbr.cash_flows():
                        StrikePriceDAYC	=	MR_MainFunctions.DayCountFix(LegNbr.daycount_method)
                    
                    StrikePricePERD=MR_MainFunctions.RollingPeriodFix(LegNbr.rolling_period)
                
                StrikePriceCAL      =       ''
                
                StrikePriceFUNC     =       '@strike price given yield SA'
                StrikePriceUNIT     =       i.curr.insid
                StrikePriceVAL      =       ''
                StrikePriceSTRG     =       ''
                
                StriPric_YieUNIT    =       '%'
                StriPric_YieVAL     =       trades.price
                
                if i.instype == 'IndexLinkedBond':
                    StrikePriceFUNC = ''
                    StrikePriceVAL = str((i.clean_from_yield(trades.value_day, None, None, trades.price)/100)*i.contr_size)
                
                UnderlyingXREF      =       'insaddr_' + str(i.insaddr)
                
                SensTypeENUM	=       ''
                DiscountCurveXREF       =       ''
                RepoCurveXREF   =       ''
                sheetType = 'FDealSheet'
                calcSpace = acm.Calculations().CreateCalculationSpace( context, sheetType )
                
                InsCurr = acm.FInstrument[ins.Currency().Oid()]
                DiscountCurveXREF       =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
                RepoCurveXREF           =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
                
                TheoModelXREF       =       'SA Bond Forward'
                MarketModelXREF     =       'SA Bond Forward'
                FairValueModelXREF  =       ''
                SettlementTYPE      =       ''
                SettlementProcFUNC  =       ''
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL, MaturityDATE, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, StriPric_YieUNIT, StriPric_YieVAL, UnderlyingXREF, SensTypeENUM, DiscountCurveXREF, RepoCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
                outfile.close()
                
                if MR_MainFunctions.ValidTradeNo(trades) == 0:
                    if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                        PositionFile.CreatePositionFX(trades, PositionFilename)
    
    return i.insid
    
# WRITE - FILE ######################################################################################################



# WRITE2 - FILE ######################################################################################################
# Used for Bonds Forwards booked as Future Forward instruments

def Write2(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        for t in i.trades():
            outfile = open(filename, 'a')
            #Base record

            BASFLAG	        =	'BAS'
            HeaderName	        =	'Bond Forward'
            OBJECT	        =	'Bond ForwardSPEC'
            TYPE	        =	'Bond Forward'
            
            NAME            =       MR_MainFunctions.NameFix(i.insid)+'_'+str(t.trdnbr)
            IDENTIFIER      =       'insaddr_'+str(i.insaddr)+'_'+str(t.trdnbr)

            CurrencyCAL	        =	''
            CurrencyDAYC	=	''
            CurrencyPERD	=	''
            CurrencyUNIT	=	i.curr.insid
            
            if i.und_insaddr:
                ContractSizeVAL =	i.contr_size/i.und_insaddr.contr_size
            else:
                ContractSizeVAL =	'1'
            
            MaturityDATE    =	MR_MainFunctions.Datefix(i.exp_day)
            StrikePriceCAL      =       ''
            StrikePriceDAYC     =       MR_MainFunctions.DayCountFix(ins.Underlying().RecLeg().DayCountMethod())
            StrikePriceFUNC     =       '@strike price given yield SA'
            StrikePricePERD     =       MR_MainFunctions.RollingPeriodFix(ins.Underlying().RecLeg().RollingPeriod())
            StrikePriceUNIT     =       i.curr.insid
            StrikePriceVAL      =       ''
            StrikePriceSTRG     =       ''
            StriPric_YieUNIT    =       '%'
            StriPric_YieVAL     =       t.price
            UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
            
            SensTypeENUM	=       ''
            DiscountCurveXREF   =       MR_MainFunctions.NameFix(ins.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
            RepoCurveXREF       =       ''
            RepoCurveXREF       =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
            
            TheoModelXREF       =       'SA Bond Forward'
            MarketModelXREF     =       'SA Bond Forward'
            FairValueModelXREF  =       ''
            SettlementTYPE      =       ''
            SettlementProcFUNC  =       ''
            
            if i.und_instype == 'IndexLinkedBond':
                StrikePriceFUNC = ''
                #StrikePriceVAL = str((i.und_insaddr.clean_from_yield(trades.value_day,None,None,t.price)/100)*i.contr_size)
                StrikePriceVAL = str((i.und_insaddr.clean_from_yield(t.value_day, None, None, t.price)/100)*i.contr_size)

            '''
            UnderlyingXREF      =       'insaddr_'+str(i.und_insaddr.insaddr)
            NetBasisCAL         =       ''
            NetBasisDAYC        =       ''
            NetBasisFUNC        =       '@net basis MKT'
            NetBasisPERD        =       ''
            NetBasisUNIT        =       '$'
            NetBasisVAL         =       ''
            NetBasisSTRG        =       ''
            SpotPriceCAL        =       ''
            SpotPriceDAYC       =       ''
            SpotPriceFUNC       =       ''#'@spot price given yield SA'
            SpotPricePERD       =       ''
            SpotPriceUNIT       =       i.curr.insid
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

                SpotPric_YiePERD=RollingPeriodFix(rolling_period)
                StriPric_YiePERD=RollingPeriodFix(rolling_period)
                
            cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            calc = ins.Calculation()
            TheoPrice = calc.TheoreticalPrice(cs)
            Price = calc.MarketPrice(cs)
            
            SpotPric_YieDAYC    =       ''
            SpotPric_YieFUNC    =       ''
            SpotPric_YieUNIT    =       '%'
            SpotPric_YieVAL     =       ''#Price.Number()
            SpotPric_YieSTRG    =       ''


            StrikePriceFUNC     =       '@strike price given yield SA'
            StrikePricePERD     =       ''
            StrikePriceUNIT     =       i.curr.insid
            StrikePriceVAL      =       ''
            StrikePriceSTRG     =       ''
            StriPric_YieCAL     =       ''

            StriPric_YieFUNC    =       ''

            StriPric_YieUNIT    =       '%'
            StriPric_YieVAL     =       t.price
            StriPric_YieSTRG    =       ''
            SensTypeENUM	=       ''
            DiscountCurveXREF   =       MR_MainFunctions.NameFix(ins.Currency().MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))

            RepoCurveXREF   =       ''
            RepoCurveXREF           =       MR_MainFunctions.NameFix(ins.MappedRepoLink(ins.Currency()).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))

            TheoModelXREF       =       'SA Bond Future'
            MarketModelXREF     =       'SA Bond Future'
            FairValueModelXREF  =       ''
            SettlementTYPE      =       ''
            SettlementProcFUNC  =       ''

            '''
            # Header file in Market Risk                                                                                 BASFLAG,HeaderName,OBJECT,TYPE,NAME,IDENTIFIER,CurrencyCAL,CurrencyDAYC,CurrencyPERD,CurrencyUNIT,ContractSizeVAL,MaturityDATE,StrikePriceCAL,StrikePriceDAYC,StrikePriceFUNC,StrikePricePERD,StrikePriceUNIT,StrikePriceVAL,StrikePriceSTRG,StriPric_YieUNIT,StriPric_YieVAL,UnderlyingXREF,SensTypeENUM,DiscountCurveXREF,RepoCurveXREF,TheoModelXREF,MarketModelXREF,FairValueModelXREF,SettlementTYPE,SettlementProcFUNC
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL, MaturityDATE, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, StriPric_YieUNIT, StriPric_YieVAL, UnderlyingXREF, SensTypeENUM, DiscountCurveXREF, RepoCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
            #outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG,HeaderName,OBJECT,TYPE,NAME,IDENTIFIER,CurrencyCAL,CurrencyDAYC,CurrencyPERD,CurrencyUNIT,ContractSizeVAL,MaturityDATE,UnderlyingXREF,NetBasisCAL,NetBasisDAYC,NetBasisFUNC,NetBasisPERD,NetBasisUNIT,NetBasisVAL,NetBasisSTRG,SpotPriceCAL,SpotPriceDAYC,SpotPriceFUNC,SpotPricePERD,SpotPriceUNIT,SpotPriceVAL,SpotPriceSTRG,SpotPric_YieCAL,SpotPric_YieDAYC,SpotPric_YieFUNC,SpotPric_YiePERD,SpotPric_YieUNIT,SpotPric_YieVAL,SpotPric_YieSTRG,StrikePriceCAL,StrikePriceDAYC,StrikePriceFUNC,StrikePricePERD,StrikePriceUNIT,StrikePriceVAL,StrikePriceSTRG,StriPric_YieCAL,StriPric_YieDAYC,StriPric_YieFUNC,StriPric_YiePERD,StriPric_YieUNIT,StriPric_YieVAL,StriPric_YieSTRG,DiscountCurveXREF,TheoModelXREF,MarketModelXREF,FairValueModelXREF))
            
            outfile.close()
        
            if MR_MainFunctions.ValidTradeNo(t) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(t) == False:
                    PositionFile.CreatePositionFX(t, PositionFilename)

    return i.insid
    
# WRITE - FILE ######################################################################################################
