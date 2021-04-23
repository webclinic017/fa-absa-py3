
'''
Purpose                 [Market Risk feed files],[Discount curve should be money market curve]
Department and Desk     [IT],[MR]
Requester               [Natalie Austin],[Susan Kruger]
Developer               [Douglas Finkel  Henk Nel],[Willie van der Bank]
CR Number               [264536],[289168],[816235 04/11/11]

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

#MoneyMarket Curve
def getMMYC(i):
    instrument = acm.FInstrument[i.insid]
    '''
    global calcSpace
    global collectLimit
    global collect
    '''
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    #component = instrument.Calculation().DiscountYieldCurveComponent(calcSpace)
    component = instrument.Calculation().MoneyMarketYieldCurveComponents(calcSpace)
    if component:
        if component.IsKindOf('FYieldCurve'):
            return component.Name()
        if component.IsKindOf('FArray') and component.Size() > 0:
            for c in component:
                if c.Currency().Name() == instrument.Currency().Name():
                    return c.Name()
        #if component.IsKindOf('FInstrumentSpread') or component.IsKindOf('FYCAttribute'):
        #    return component.Curve().Name()
    return ''

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
#    PositionFilename    = FileDir + PositionName 
    
    outfile             =  open(filename, 'w')
#    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
#    outfileP.close()
    
    del InsL[:]
    InsL[:] = []  
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    #DateValueDay = acm.GetFunction('DateValueDay',0)
    filename            = FileDir + Filename
#    PositionFilename    = FileDir + PositionName
    
    Instrument = acm.FInstrument[i.insaddr]
#    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        for trades in i.trades():
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                if i.start_day >= ael.date_today():
                    
                    outfile = open(filename, 'a')
                    
                    #Base record
                    
                    BASFLAG	                =       'BAS'
                    HeaderName	        =       'Bond Forward'
                    OBJECT	                =       'Bond ForwardSPEC'
                    TYPE	                =       'Bond Forward'
                    
                    NAME                    =       MR_MainFunctions.NameFix(i.insid)[0:30] + '_' + str(trades.trdnbr) + '_NearLeg'
                    IDENTIFIER              =       'insaddr_'+str(i.insaddr) + '_' + str(trades.trdnbr) + '_NearLeg'
                    
                    CurrencyCAL	        =       ''
                    CurrencyDAYC	        =       ''
                    CurrencyPERD	        =       ''
                    CurrencyUNIT	        =       i.curr.insid
                    ContractSizeVAL	        =       i.contr_size/i.und_insaddr.contr_size
                    MaturityDATE	        =       MR_MainFunctions.Datefix(i.start_day)
                    
                    StrikePriceCAL	=       ''
                    StrikePriceDAYC	=       '' #MR_MainFunctions.DayCountFix(i.daycount_method)
                    StrikePriceFUNC	=       '@strike price given yield SA'
                    StrikePricePERD	=       '' #'semi-annual'
                    StrikePriceUNIT	=       i.curr.insid
                    StrikePriceVAL  =       ''
                    if  i.und_insaddr.instype in ('Bill', 'CD', 'Zero', 'IndexLinkedBond'):
                        StrikePriceFUNC = ''
                        StrikePriceVAL = str((i.und_insaddr.clean_from_yield(i.start_day, None, None, trades.price)/100)*i.und_insaddr.contr_size)
                    StrikePriceSTRG	        =       ''
                    
                    StriPric_YieUNIT    =       '%'
                    StriPric_YieVAL     =       trades.price
                    
                    UnderlyingXREF	        =       'insaddr_' + str(i.und_insaddr.insaddr)
                    SensTypeENUM	        =       ''
                    #DiscountCurveXREF	=       MR_MainFunctions.NameFix(Instrument.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip(').rstrip('))
                    DiscountCurveXREF	=       MR_MainFunctions.NameFix(getMMYC(i))
                    RepoCurveXREF	        =       MR_MainFunctions.NameFix(Instrument.MappedDiscountLink().Link().AsString().rsplit(',')[0].lstrip(').rstrip('))
                    TheoModelXREF	        =       'SA Bond Forward'
                    MarketModelXREF 	=       'SA Bond Forward'
                    FairValueModelXREF	=       ''
                    SettlementTYPE	        =       ''
                    SettlementProcFUNC	=       ''
                    
                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL, MaturityDATE, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, StriPric_YieUNIT, StriPric_YieVAL, UnderlyingXREF, SensTypeENUM, DiscountCurveXREF, RepoCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
                    
                    outfile.close()
            
        #Position
        
#        for trades in i.trades()
#            if MR_MainFunctions.ValidTradeNo(trades) == 0
#                PositionFile.CreatePosition(trades,PositionFilename)
    
    return i.insid

# WRITE - FILE ######################################################################################################


