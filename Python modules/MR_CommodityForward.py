'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536,394236

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

                    BASFLAG             = 'BAS'
                    HeaderName          = 'Commodity Forward'
                    OBJECT              = 'Commodity ForwardSPEC'
                    TYPE                = 'Commodity Forward'

                    NAME                = i.und_insaddr.insid + i.und_insaddr.instype + i.paytype #str(i.instype) + str(i.insaddr)
                    IDENTIFIER          = 'insaddr_'+str(i.insaddr)+'_'+str(trades.trdnbr)

                    CurrencyCAL         = ''
                    CurrencyDAYC        = ''
                    CurrencyPERD        = ''
                    CurrencyUNIT        = i.curr.insid
                    
                    # 29 October 2010
                    # Changed by: Douglas Finkel
                    # Contract size neds to be proportinal to the quote type on the instrument
                    
                    if i.quote_type == 'Per 100 Units':
                        ContractSizeVAL     = i.contr_size/100
                    else:
                        ContractSizeVAL     = i.contr_size
                    #ContractSizeVAL     = i.contr_size
                    
                    StrikePriceCAL      = ''
                    StrikePriceDAYC     = ''
                    StrikePriceFUNC     = ''
                    StrikePricePERD     = ''
                    StrikePriceUNIT     = i.curr.insid
                    StrikePriceVAL      = trades.price
                    StrikePriceSTRG     = ''

                    UnderlyingXREF      = 'insaddr_'+str(i.und_insaddr.insaddr)
                    MaturityDATE        = MR_MainFunctions.Datefix(i.exp_day)

                    try:
                        DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
                    except:
                        DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

                    TheoModelXREF       = 'Commodity Forward'

                    MarketModelXREF     = ''
                    FairValueModelXREF  = ''

                    SettlementProcFUNC  = ''
                    SettlementTYPE      = ''

                    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, ContractSizeVAL, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, UnderlyingXREF, MaturityDATE, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementProcFUNC, SettlementTYPE))
                    outfile.close()

                    
                    
                    '''
                    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                    calc = ins.Calculation()
                    TheoPrice = calc.TheoreticalPrice(cs)
                    try:
                        if str(TheoPrice.Number()) in ('1.#QNAN','NaN'):
                            StrikePriceVAL      = ''
                        else:
                            StrikePriceVAL      = TheoPrice.Number() #i.mtm_price(ael.date_today())                
                    except:
                        try:
                            StrikePriceVAL      = TheoPrice
                        except:
                            StrikePriceVAL      = ''
                    #return 'Instrument Skipped'
                    '''
            
    for trades in i.trades():
        if MR_MainFunctions.ValidTradeNo(trades) == 0:
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                PositionFile.CreatePositionFwds(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


