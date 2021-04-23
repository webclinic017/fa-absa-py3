
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536

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
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Synthetic'
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
        CostOfCarryVAL      =   	''
        
        TheoModelXREF       =       'Basket Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        Legs = i.legs()
        for l in Legs:
            if l.type in ('Float', 'Total Return', 'Fixed', 'Call Fixed'):
                Dividend = 0
                if l.end_day >= ael.date_today():
                    for cf in l.cash_flows():
                        if cf.type == 'Dividend':
                            Dividend = 1

                    if Dividend != 1:
                        if (l.cash_flows()):
                            #Rollover record            
                            BASFLAG         =	'rm_ro'
                            HeaderName	=	'Synthetic : Component Weights'
                            ATTRIBUTE	=	'Component Weights'
                            OBJECT          =	'Synthetic InstrumentSPEC'
                            
                            if i.instype == 'CurrSwap':
                                ComponentWghtVAL = 1
                            else:
                                if l.payleg:
                                    ComponentWghtVAL      =	-1
                                if not l.payleg:
                                    ComponentWghtVAL      =	1

                            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
                            
                            #Rollover record            
                            BASFLAG     =	'rm_ro'
                            HeaderName	=	'Synthetic : Underlying Financial Entities'
                            ATTRIBUTE	=	'Underlying Financial Entities'
                            OBJECT      =	'Synthetic InstrumentSPEC'           
                            UndrFinEntitisXREF = 'insaddr_'+str(i.insaddr)+'_'+str(l.legnbr)
                            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))

        outfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################

#MR_Equity_Swap_Synth
#MR_Crs_Cur_Swap_Synth


