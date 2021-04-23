
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
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
    
    #DateValueDay = acm.GetFunction('DateValueDay',0)
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    Instrument = acm.FInstrument[i.insaddr]
#    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        for trades in i.trades():
            if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                outfile = open(filename, 'a')
                
                #Base record
                
                BASFLAG             =       'BAS'
                HeaderName	        =       'Synthetic'
                OBJECT	        =       'Synthetic InstrumentSPEC'
                TYPE	        =       'Synthetic Instrument'
                NAME                =       MR_MainFunctions.NameFix(i.insid) + '_' + str(trades.trdnbr)
                IDENTIFIER          =       'insaddr_'+str(i.insaddr) + '_' + str(trades.trdnbr)
                CurrencyCAL	        =       ''
                CurrencyDAYC	=       ''
                CurrencyPERD	=       ''
                CurrencyUNIT	=       i.curr.insid
                CostOfCarryCAL	=       ''
                CostOfCarryDAYC	=       'actual/365'
                CostOfCarryPERD	=       'continuous'
                CostOfCarryVAL	=       '0'
                TheoModelXREF	=       'Basket Instrument'
                MarketModelXREF	=       ''
                FairValueModelXREF =    ''
                
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
                
                
                BASFLAG	        =       'rm_ro'
                HeaderName	        =       'Synthetic : Component Weights'
                ATTRIBUTE	        =       'Component Weights'
                OBJECT	        =       'Synthetic InstrumentSPEC'
                
                ComponentWghtVAL    =       1
                '''
                if i.start_day > ael.date_today():
                    ComponentWghtVAL    =       1
                else:
                    ComponentWghtVAL    =       1/i.und_insaddr.contr_size
                '''
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))        
                
                ComponentWghtVAL    = 1 * -1
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))        
                
                BASFLAG	        =       'rm_ro'
                HeaderName	=       'Synthetic : Underlying Financial Entities'
                ATTRIBUTE	=       'Underlying Financial Entities'
                OBJECT	        =       'Synthetic InstrumentSPEC'
                
                
                if i.start_day > ael.date_today():
                    UndrFinEntitisXREF = 'insaddr_' + str(i.insaddr) + '_' + str(trades.trdnbr) + '_NearLeg'
                else:
                    UndrFinEntitisXREF = 'insaddr_' + str(i.und_insaddr.insaddr)
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))        
                
                UndrFinEntitisXREF = 'insaddr_'+str(i.insaddr) + '_' + str(trades.trdnbr) + '_FarLeg'
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))   
                
                outfile.close()
            
                #Position
                if MR_MainFunctions.ValidTradeNo(trades) == 0:
                    PositionFile.CreatePositionFX(trades, PositionFilename)
        
    return i.insid

# WRITE - FILE ######################################################################################################



