'''
Purpose                 :Market Risk feed files, Changed weighting of CFDs
Department and Desk     :IT, Market Risk
Requester:              :Natalie Austin, Susan Kruger
Developer               :Douglas Finkel / Henk Nel, Willie van der Bank
CR Number               :264536, 790080 07/10/2011]

Change Log
----------------------------------------------------------------------------------------------------------------------------------------------
Date               Changed by          CR                        Description
----------------------------------------------------------------------------------------------------------------------------------------------      
2015-09-30         Chris Human         CHNG0003221889            Change requested to exclude non-live trades: http://abcap-jira/browse/MINT-378
2020-09-11         Heinrich Cronje     CHG0128302	         https://absa.atlassian.net/browse/CMRI-776
2021-03-11         Andile Biyana       CHG0158547                https://absa.atlassian.net/browse/FAFO-41
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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Synthetic Market Index'
        OBJECT              =       'Synthetic InstrumentSPEC'
        TYPE                =       'Synthetic InstrumentSPEC'
        
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        
        CostOfCarryCAL      =       ''
        CostOfCarryDAYC     =       ''
        CostOfCarryPERD     =       ''        
        divYield            =       Instrument.AdditionalInfo().DividendYield()
        if divYield:
            CostOfCarryVAL      =   divYield
        else:
            CostOfCarryVAL      =   ''
        
        StateProcFUNC       =       '@aggregate positions'
        
        try:
            DiscountCurveXREF       =       Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF       =       Instrument.Currency().MappedDiscountLink().Value().Link().YieldCurveComponent().Name()
        
        TheoModelXREF       =       'Basket Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, StateProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        port = acm.FPhysicalPortfolio[Instrument.FundPortfolio().Portfolio().Name()]
        
        context = acm.GetDefaultContext()
        sheet = 'FPortfolioSheet'
        column = 'Portfolio Position'
        calc_space = acm.Calculations().CreateCalculationSpace(context, sheet)
        
        topnode = calc_space.InsertItem(port)
        calc_space.Refresh()
        child = topnode.Iterator().FirstChild()
        while child:
            
            hasValidTrade = False
            for childTrade in child.Tree().Item().Trades():
                if childTrade.Status() not in ('Void', 'Terminated', 'Simulated'):
                    expiryDate = childTrade.Instrument().ExpiryDateOnly()
                    
                    if not expiryDate:
                        hasValidTrade = True
                        break
					# For PSwaps where the underlying components are FRA's
                    elif ael.Instrument[child.Tree().Item().StringKey()].instype == 'FRA':
                        for leg in childTrade.Instrument().Legs():
                            for cf in leg.CashFlows():
                                if MR_MainFunctions.Datefix(cf.PayDate()) > MR_MainFunctions.Datefix(acm.Time().DateToday()):
                                    hasValidTrade = True
                                    break
                    elif ael.date(expiryDate) > ael.date_today():
                        hasValidTrade = True
                        break
            
            if hasValidTrade:
                StockInsType = ael.Instrument[child.Tree().Item().StringKey()].instype
                StockInsaddr = ael.Instrument[child.Tree().Item().StringKey()].insaddr
        
                if StockInsType == 'BuySellback': 		
                    for childTrade in child.Tree().Item().Trades():
                        if (childTrade.Status() not in ('Void', 'Terminated', 'Simulated')) and (childTrade.Instrument().ExpiryDateOnly()> ael.date_today()):

                            #Rollover record            
                            BASFLAG     =	'rm_ro'
                            HeaderName	=	'Synthetic Market Index : Component Weights'
                            ATTRIBUTE	=	'Component Weights'
                            OBJECT      =       'Synthetic InstrumentSPEC'
							
                            #The evaluation returns the instruments currency. 
                            #The try catch tests whether the currency has been included and then caters for it
                            PortPosition = calc_space.CalculateValue(child.Tree(), column)
                            
                            #if ael.Portfolio[Instrument.FundPortfolio().Portfolio().Name()].add_info('PS_PortfolioType') == 'CFD':
                            #	try:
                            #		ComponentWghtVAL =  -1 * PortPosition.Number()
                            #	except:
                            #		ComponentWghtVAL =  -1 * PortPosition
                            #else:
                            #	try:
                            #		ComponentWghtVAL =  PortPosition.Number()
                            #	except:
                            #		ComponentWghtVAL =  PortPosition
                            
                            ComponentWghtVAL =  PortPosition / childTrade.Instrument().ContractSize()
                            
                            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
                            
                            #Rollover record            
                            BASFLAG     =	'rm_ro'
                            HeaderName	=	'Synthetic Market Index : Underlying Financial Entities'
                            ATTRIBUTE	=	'Underlying Financial Entities'
                            OBJECT      =       'Synthetic InstrumentSPEC'           
                            UndrFinEntitisXREF = 'insaddr_' + str(StockInsaddr) + '_' + str(childTrade.Name())
                            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))
                else:
    
                    if StockInsType == 'ETF':    
                        #StockInsaddr = ael.Instrument[childTrade.Instrument().Underlying().StringKey()].insaddr
                        StockInsaddr = ael.Instrument[childTrade.Instrument().StringKey()].insaddr
                    else:
                        StockInsaddr = ael.Instrument[child.Tree().Item().StringKey()].insaddr
                    #Rollover record            
                    BASFLAG     =	'rm_ro'
                    HeaderName	=	'Synthetic Market Index : Component Weights'
                    ATTRIBUTE	=	'Component Weights'
                    OBJECT      =       'Synthetic InstrumentSPEC'
                    
                    #The evaluation returns the instruments currency. 
                    #The try catch tests whether the currency has been included and then caters for it
                    PortPosition = calc_space.CalculateValue(child.Tree(), column)
                    
                    if ael.Portfolio[Instrument.FundPortfolio().Portfolio().Name()].add_info('PS_PortfolioType') == 'CFD':
                        try:
                            ComponentWghtVAL =  PortPosition.Number()
                        except:
                            ComponentWghtVAL =  PortPosition
                    else:
                        try:
                            ComponentWghtVAL =  PortPosition.Number() / childTrade.Instrument().ContractSize()
                        except:
                            ComponentWghtVAL =  PortPosition / childTrade.Instrument().ContractSize()
                    
                    outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
                    
                    #Rollover record            
                    BASFLAG     =	'rm_ro'
                    HeaderName	=	'Synthetic Market Index : Underlying Financial Entities'
                    ATTRIBUTE	=	'Underlying Financial Entities'
                    OBJECT      =       'Synthetic InstrumentSPEC'           
                    UndrFinEntitisXREF = 'insaddr_' + str(StockInsaddr)
                    
                    outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))

            child = child.NextSibling()

        outfile.close()
        
    for trades in i.trades():
        print trades.trdnbr, trades.status
        if MR_MainFunctions.ValidTradeNo(trades) == 0:
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                PositionFile.CreatePosition(trades, PositionFilename)        

    return i.insid

# WRITE - FILE ######################################################################################################
