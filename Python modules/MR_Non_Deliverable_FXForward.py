'''
/*
Purpose                           :Market Risk feed files
Department and Desk     	  :IT
Requester:                        :Gary Beukes
Developer                         :Mandlenkosi Ngcobo-Koyana
CR Number                         :
*/

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''

import ael, string, acm, PositionFile, MR_MainFunctions, re

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

def Write(t,FileDir,Filename,PositionName,i,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    Instrument = acm.FInstrument[t.insaddr.insid]
    FX_NDF_Flag = str(Instrument.IsFxNdf())
    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    underlying = Instrument.Underlying()

    if MR_MainFunctions.IsExcludedPortfolio(t) == False:
        if ((t.trdnbr) not in InsL) and FX_NDF_Flag == 'True':
            InsL.append(t.trdnbr)
            outfile = open(filename, 'a')

            #Base record attribute mapping
            BASFLAG             =    'BAS'
            HeaderName          =    'FX Forward'
            OBJECT              =    'Forex ForwardSPEC'
            TYPE                =    'Forex Forward'    
            NAME                =    str(t.insaddr.instype) + '_' + MR_MainFunctions.NameFix(str(t.insaddr.curr.insid))+ '_' + MR_MainFunctions.NameFix(str(t.curr.insid))+ '_' + str(t.value_day)+ '_' + str(t.trdnbr)
            IDENTIFIER          =    'insaddr_'+str(t.insaddr.insaddr)+'_'+str(t.trdnbr)
            CurrencyCAL         =    ''
            CurrencyDAYC        =    ''
            CurrencyPERD        =    ''
            CurrencyUNIT        =    Instrument.Underlying().Name()
            DiscountCurveXREF   =    str(Instrument.Currency().MappedDiscountLink(underlying, False, Instrument.DiscountingType()).Link())
            DiscountCurveXREF   =    DiscountCurveXREF[1:len(DiscountCurveXREF)-1]
            DiscountCurveXREF   =    string.replace(DiscountCurveXREF, ', Currency = ' + CurrencyUNIT, '')
            MaturityDATE        =    MR_MainFunctions.Datefix(i.exp_day) 
            UnderlyingXREF      =    'insaddr_'+str(t.curr.insaddr) 
            StrikePriceCAL      =    ''
            StrikePriceDAYC     =    ''
            StrikePriceFUNC     =    ''
            StrikePricePERD     =    ''
            StrikePriceUNIT     =    CurrencyUNIT
            StrikePriceVAL      =    t.price
            StrikePriceSTRG     =    ''
            RM_MapProcFUNC      =    ''
            TheoModelXREF       =    'FX Forward IP'
            MarketModelXREF     =    ''
            FairValueModelXREF  =    ''
            SettlementTYPE      =    ''
            SettlementProcFUNC  =    ''

            # Print Base Line
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                          %(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, MaturityDATE, UnderlyingXREF, StrikePriceCAL, StrikePriceDAYC, StrikePriceFUNC, StrikePricePERD, StrikePriceUNIT, StrikePriceVAL, StrikePriceSTRG, RM_MapProcFUNC, DiscountCurveXREF, TheoModelXREF, MarketModelXREF, FairValueModelXREF, SettlementTYPE, SettlementProcFUNC))
            outfile.close()

            #Position record attribute mapping
            outfile = open(PositionFilename, 'a')
            BASFLAG                 =    'BAS'
            HeaderName              =    'Position'
            OBJECT                  =    'PositionSPEC'
            TYPE                    =    'PositionSPEC'
            IDENTIFIER              =    'trdnbr_'+str(t.trdnbr)
            PositionUnitsCAL        =    ''
            PositionUnitsDAYC       =    ''
            PositionUnitsFUNC       =    ''
            PositionUnitsPERD       =    ''
            PositionUnitsSTRG       =    ''
            PositionUnitsUNIT       =    ''
            PositionUnitsVAL        =    -t.quantity / t.price # t.premium # t.quantity
            InstrumentXREF          =    'insaddr_'+str(t.insaddr.insaddr)+'_'+str(t.trdnbr)
            SettlmntAccntXREF       =    ''
            SettlementProcFUNC      =    ''
            PortfolioNAME           =    t.prfnbr.prfid
            InstrumentTYPE          =    t.insaddr.instype
            TradeAggregationNAME    =    IDENTIFIER

            if t.prfnbr:
                PortfolioXREF   =    'prfnbr_'+str(t.prfnbr.prfnbr)
            else:
                PortfolioXREF   =    ''

            if t.counterparty_ptynbr:
                CounterpartySTRG    =    t.counterparty_ptynbr.ptyid
            else:
                CounterpartySTRG    =    ''

            if t.owner_usrnbr:
                TraderNAME    =    t.owner_usrnbr.name
            else:
                TraderNAME    =       ''

            # Print Position Record
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE, TradeAggregationNAME))
            outfile.close()    

    return t.insaddr.insid

# WRITE - FILE ######################################################################################################

